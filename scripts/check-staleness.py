#!/usr/bin/env python3
"""
Staleness Detection Tool (Python Version)
Compares Case timestamps with implementation references
Provides priority-based reporting based on staleness age
"""

import re
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from collections import defaultdict
import argparse

# Color codes for terminal output
class Colors:
    RED = '\033[0;31m'
    YELLOW = '\033[1;33m'
    GREEN = '\033[0;32m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color

class StaleEntry:
    """Represents a stale implementation."""
    def __init__(self, impl_file: Path, case_file: Path, case_timestamp: datetime,
                 impl_timestamp: datetime, days_stale: int):
        self.impl_file = impl_file
        self.case_file = case_file
        self.case_timestamp = case_timestamp
        self.impl_timestamp = impl_timestamp
        self.days_stale = days_stale

    def __str__(self):
        return (f"  {self.impl_file} → {self.case_file.name}\n"
                f"    Case: {self.case_timestamp.isoformat()}\n"
                f"    Impl: {self.impl_timestamp.isoformat()}\n"
                f"    Stale: {self.days_stale} days")

def parse_iso_timestamp(timestamp_str: str) -> Optional[datetime]:
    """Parse ISO 8601 timestamp string."""
    try:
        # Handle with or without Z suffix
        if timestamp_str.endswith('Z'):
            timestamp_str = timestamp_str[:-1] + '+00:00'
        return datetime.fromisoformat(timestamp_str)
    except:
        return None

def get_case_timestamp(case_file: Path) -> Optional[datetime]:
    """Extract timestamp from a Case YAML file."""
    if not case_file.exists():
        return None

    try:
        with open(case_file, 'r') as f:
            for line in f:
                if line.startswith('hash_timestamp:'):
                    timestamp_str = line.split(':', 1)[1].strip()
                    return parse_iso_timestamp(timestamp_str)
    except Exception as e:
        print(f"Error reading {case_file}: {e}", file=sys.stderr)

    return None

def find_implementation_references(repo_root: Path) -> Dict[Path, List[Tuple[Path, datetime]]]:
    """Find all implementation files that reference Case files."""
    references = defaultdict(list)

    # Common implementation file patterns
    impl_patterns = [
        "**/*.py", "**/*.js", "**/*.ts", "**/*.java", "**/*.go",
        "**/*.rb", "**/*.cs", "**/*.cpp", "**/*.c", "**/*.rs"
    ]

    # Exclude directories
    exclude_dirs = {'.git', 'node_modules', 'venv', '__pycache__', 'target', 'build', 'dist'}

    for pattern in impl_patterns:
        for impl_file in repo_root.glob(pattern):
            # Skip excluded directories
            if any(part in exclude_dirs for part in impl_file.parts):
                continue

            try:
                content = impl_file.read_text()

                # Find Case references in various comment styles
                # Pattern: Implements: /specs/xxx-cases/YY-NNN.yaml
                case_pattern = r'(?:Implements|implements):\s*(/specs/(?:test|scenario|precondition)-cases/[A-Z]+-\d+\.yaml)'
                timestamp_pattern = r'(?:Case Timestamp|case_timestamp):\s*([0-9T:\-Z]+)'

                case_matches = re.findall(case_pattern, content)
                timestamp_matches = re.findall(timestamp_pattern, content)

                # Pair up case references with timestamps
                for i, case_path in enumerate(case_matches):
                    if i < len(timestamp_matches):
                        timestamp = parse_iso_timestamp(timestamp_matches[i])
                        if timestamp:
                            full_case_path = repo_root / case_path.lstrip('/')
                            references[impl_file].append((full_case_path, timestamp))

            except Exception:
                # Skip files that can't be read as text
                continue

    return references

def calculate_staleness(repo_root: Path) -> Dict[str, List[StaleEntry]]:
    """Calculate staleness for all implementations."""
    staleness = {
        'critical': [],  # >30 days
        'high': [],      # 7-30 days
        'medium': [],    # 1-7 days
        'low': [],       # <1 day
        'up_to_date': [] # Matching timestamps
    }

    references = find_implementation_references(repo_root)

    for impl_file, case_refs in references.items():
        for case_file, impl_timestamp in case_refs:
            case_timestamp = get_case_timestamp(case_file)

            if not case_timestamp:
                print(f"Warning: Cannot read timestamp from {case_file}", file=sys.stderr)
                continue

            # Calculate staleness
            if case_timestamp > impl_timestamp:
                days_stale = (case_timestamp - impl_timestamp).days
                entry = StaleEntry(impl_file, case_file, case_timestamp, impl_timestamp, days_stale)

                if days_stale > 30:
                    staleness['critical'].append(entry)
                elif days_stale > 7:
                    staleness['high'].append(entry)
                elif days_stale >= 1:
                    staleness['medium'].append(entry)
                else:
                    staleness['low'].append(entry)
            else:
                entry = StaleEntry(impl_file, case_file, case_timestamp, impl_timestamp, 0)
                staleness['up_to_date'].append(entry)

    return staleness

def print_report(staleness: Dict[str, List[StaleEntry]], verbose: bool = False):
    """Print staleness report with color coding."""

    print("\n" + "="*60)
    print(" STALENESS DETECTION REPORT")
    print("="*60)

    # Summary
    total_stale = sum(len(entries) for key, entries in staleness.items() if key != 'up_to_date')
    total_current = len(staleness['up_to_date'])

    print(f"\nSummary:")
    print(f"  Total Implementations: {total_stale + total_current}")
    print(f"  Stale: {total_stale}")
    print(f"  Up-to-date: {total_current}")

    # Critical issues
    if staleness['critical']:
        print(f"\n{Colors.RED}CRITICAL (>30 days stale):{Colors.NC}")
        for entry in staleness['critical']:
            print(entry)

    # High priority
    if staleness['high']:
        print(f"\n{Colors.YELLOW}HIGH (7-30 days stale):{Colors.NC}")
        for entry in staleness['high']:
            print(entry)

    # Medium priority
    if staleness['medium']:
        print(f"\n{Colors.BLUE}MEDIUM (1-7 days stale):{Colors.NC}")
        for entry in staleness['medium']:
            print(entry)

    # Low priority
    if staleness['low']:
        print(f"\nLOW (<1 day stale):")
        for entry in staleness['low']:
            print(entry)

    # Up-to-date (only if verbose)
    if verbose and staleness['up_to_date']:
        print(f"\n{Colors.GREEN}UP-TO-DATE:{Colors.NC}")
        for entry in staleness['up_to_date']:
            print(f"  {entry.impl_file} → {entry.case_file.name}")

    print("\n" + "="*60)

    # Exit code based on critical issues
    if staleness['critical']:
        print(f"{Colors.RED}⚠ Critical staleness detected - immediate update required{Colors.NC}")
        return 2
    elif staleness['high']:
        print(f"{Colors.YELLOW}⚠ High priority updates needed{Colors.NC}")
        return 1
    elif staleness['medium'] or staleness['low']:
        print("Minor staleness detected - consider updating")
        return 0
    else:
        print(f"{Colors.GREEN}✓ All implementations are up-to-date{Colors.NC}")
        return 0

def ensure_case_directories(repo_root: Path):
    """Ensure Case directories exist."""
    directories = [
        repo_root / 'specs' / 'test-cases',
        repo_root / 'specs' / 'scenario-cases',
        repo_root / 'specs' / 'precondition-cases'
    ]

    for directory in directories:
        if not directory.exists():
            print(f"Creating directory: {directory}")
            directory.mkdir(parents=True, exist_ok=True)

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Check for stale test implementations"
    )

    parser.add_argument(
        "directory",
        nargs="?",
        default=".",
        help="Repository root directory (default: current directory)"
    )

    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Show up-to-date implementations"
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Output in JSON format"
    )

    args = parser.parse_args()

    repo_root = Path(args.directory).resolve()

    if not repo_root.exists():
        print(f"Error: Directory not found: {repo_root}", file=sys.stderr)
        sys.exit(2)

    # Ensure directories exist
    ensure_case_directories(repo_root)

    # Calculate staleness
    staleness = calculate_staleness(repo_root)

    # Output results
    if args.json:
        import json
        # Convert to JSON-serializable format
        json_data = {}
        for priority, entries in staleness.items():
            json_data[priority] = [
                {
                    'implementation': str(e.impl_file),
                    'case': str(e.case_file),
                    'case_timestamp': e.case_timestamp.isoformat(),
                    'impl_timestamp': e.impl_timestamp.isoformat(),
                    'days_stale': e.days_stale
                }
                for e in entries
            ]
        print(json.dumps(json_data, indent=2))

        # Exit code based on staleness
        if staleness['critical']:
            sys.exit(2)
        elif staleness['high']:
            sys.exit(1)
    else:
        exit_code = print_report(staleness, args.verbose)
        sys.exit(exit_code)

if __name__ == "__main__":
    main()