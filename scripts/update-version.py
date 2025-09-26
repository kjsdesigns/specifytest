#!/usr/bin/env python3
"""
Version Management Script for Specification-Driven Development Constitution
Handles semantic versioning and automatic date updates
"""

import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Tuple, Optional

CONSTITUTION_PATH = Path(__file__).parent.parent / "memory" / "constitution.md"

def parse_version(version_str: str) -> Tuple[int, int, int]:
    """Parse semantic version string into tuple."""
    match = re.match(r"(\d+)\.(\d+)\.(\d+)", version_str)
    if not match:
        raise ValueError(f"Invalid version format: {version_str}")
    return tuple(map(int, match.groups()))

def format_version(version: Tuple[int, int, int]) -> str:
    """Format version tuple as string."""
    return f"{version[0]}.{version[1]}.{version[2]}"

def get_current_version(content: str) -> Tuple[int, int, int]:
    """Extract current version from constitution content."""
    pattern = r"\*\*Version\*\*:\s*(\d+\.\d+\.\d+)"
    match = re.search(pattern, content)
    if not match:
        raise ValueError("Could not find version in constitution")
    return parse_version(match.group(1))

def update_version(content: str, new_version: Tuple[int, int, int], update_date: bool = True) -> str:
    """Update version and optionally the last amended date."""
    version_str = format_version(new_version)

    # Update version
    content = re.sub(
        r"(\*\*Version\*\*):\s*\d+\.\d+\.\d+",
        f"\\1: {version_str}",
        content
    )

    # Update last amended date if requested
    if update_date:
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        content = re.sub(
            r"(\*\*Last Amended\*\*):\s*\d{4}-\d{2}-\d{2}",
            f"\\1: {today}",
            content
        )

    return content

def increment_version(
    version: Tuple[int, int, int],
    change_type: str
) -> Tuple[int, int, int]:
    """Increment version based on change type."""
    major, minor, patch = version

    if change_type == "major":
        return (major + 1, 0, 0)
    elif change_type == "minor":
        return (major, minor + 1, 0)
    elif change_type == "patch":
        return (major, minor, patch + 1)
    else:
        raise ValueError(f"Invalid change type: {change_type}")

def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Update constitution version",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Change Types:
  major - Breaking changes to principles (X.0.0)
  minor - New principles or sections (x.X.0)
  patch - Clarifications and fixes (x.x.X)

Examples:
  %(prog)s patch                    # Increment patch version
  %(prog)s minor                    # Increment minor version
  %(prog)s major                    # Increment major version
  %(prog)s --set 7.0.0             # Set specific version
  %(prog)s --show                   # Show current version
        """
    )

    parser.add_argument(
        "change_type",
        nargs="?",
        choices=["major", "minor", "patch"],
        help="Type of version change"
    )

    parser.add_argument(
        "--set",
        metavar="VERSION",
        help="Set specific version (e.g., 7.0.0)"
    )

    parser.add_argument(
        "--show",
        action="store_true",
        help="Show current version without changing"
    )

    parser.add_argument(
        "--no-date",
        action="store_true",
        help="Don't update the Last Amended date"
    )

    args = parser.parse_args()

    # Read constitution
    if not CONSTITUTION_PATH.exists():
        print(f"Error: Constitution not found at {CONSTITUTION_PATH}", file=sys.stderr)
        sys.exit(1)

    content = CONSTITUTION_PATH.read_text()
    current_version = get_current_version(content)

    # Show current version
    if args.show:
        print(f"Current version: {format_version(current_version)}")
        return

    # Determine new version
    if args.set:
        try:
            new_version = parse_version(args.set)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    elif args.change_type:
        new_version = increment_version(current_version, args.change_type)
    else:
        parser.print_help()
        sys.exit(1)

    # Update constitution
    updated_content = update_version(
        content,
        new_version,
        update_date=not args.no_date
    )

    # Write back
    CONSTITUTION_PATH.write_text(updated_content)

    # Report changes
    print(f"Constitution updated:")
    print(f"  Version: {format_version(current_version)} → {format_version(new_version)}")
    if not args.no_date:
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        print(f"  Last Amended: → {today}")

    # Suggest commit message
    change_desc = {
        "major": "breaking changes",
        "minor": "new features",
        "patch": "fixes and clarifications"
    }

    if args.change_type:
        desc = change_desc.get(args.change_type, "updates")
        print(f"\nSuggested commit message:")
        print(f"  chore: Update constitution to v{format_version(new_version)} ({desc})")

if __name__ == "__main__":
    main()