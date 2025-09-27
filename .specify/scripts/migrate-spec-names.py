#!/usr/bin/env python3
"""
Specification Name Migration Tool
Helps migrate existing specs to the new descriptive filename format
"""

import os
import re
import sys
import yaml
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Tuple

class Colors:
    """Terminal colors for output"""
    RED = '\033[0;31m'
    YELLOW = '\033[1;33m'
    GREEN = '\033[0;32m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'

class SpecMigrator:
    """Migrates spec files to new naming convention"""

    def __init__(self, repo_root: Path, dry_run: bool = True, verbose: bool = False):
        self.repo_root = repo_root
        self.dry_run = dry_run
        self.verbose = verbose
        self.migrations: List[Tuple[Path, Path]] = []
        self.errors: List[str] = []

    def suggest_name_from_content(self, spec_type: str, content: any, file_path: Path) -> Optional[str]:
        """Suggest a descriptive name based on spec content"""
        # Try to extract meaningful name from spec
        if isinstance(content, dict):
            # For YAML specs
            name = content.get('name', '')
            purpose = content.get('purpose', '')

            # If name is placeholder, try to derive from purpose or description
            if name and not any(placeholder in name.lower() for placeholder in ['placeholder', 'example', 'todo', '[', 'xxx']):
                # Clean up the name
                name = name.lower()
                name = re.sub(r'[^a-z0-9_-]', '_', name)
                name = re.sub(r'_+', '_', name)
                name = name.strip('_')
                # Limit to 4 words
                parts = name.split('_')[:4]
                return '_'.join(parts)

            # Try to extract from purpose
            if purpose and not any(placeholder in purpose.lower() for placeholder in ['placeholder', 'example', '[', 'xxx']):
                # Extract first few meaningful words
                words = re.findall(r'\b[a-z][a-z]+\b', purpose.lower())
                if words:
                    return '_'.join(words[:4])

        elif isinstance(content, str):
            # For Markdown specs, extract from title
            title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
            if title_match:
                title = title_match.group(1).lower()
                title = re.sub(r'[^a-z0-9_-]', '_', title)
                title = re.sub(r'_+', '_', title)
                title = title.strip('_')
                parts = title.split('_')[:4]
                return '_'.join(parts)

        return None

    def parse_spec_file(self, file_path: Path) -> Optional[Tuple[str, str, str, any]]:
        """Parse spec file and extract ID, type, name, and content"""
        try:
            if file_path.suffix == '.yaml':
                with open(file_path, 'r') as f:
                    content = yaml.safe_load(f)

                if not content:
                    return None

                spec_id = content.get('id', '')
                spec_type = content.get('type', '')
                spec_name = content.get('name', '')

                return (spec_id, spec_type, spec_name, content)

            elif file_path.suffix == '.md':
                with open(file_path, 'r') as f:
                    content = f.read()

                # Extract frontmatter
                yaml_match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
                if not yaml_match:
                    return None

                frontmatter = yaml.safe_load(yaml_match.group(1))
                if not frontmatter:
                    return None

                spec_id = frontmatter.get('id', '')
                spec_type = frontmatter.get('type', '')
                spec_name = frontmatter.get('name', '')

                return (spec_id, spec_type, spec_name, content)

        except Exception as e:
            self.errors.append(f"Error parsing {file_path}: {str(e)}")
            return None

        return None

    def extract_prefix_and_number(self, spec_id: str) -> Optional[Tuple[str, str]]:
        """Extract prefix and number from spec ID"""
        match = re.match(r'^([A-Z]+)-(\d+)$', spec_id)
        if match:
            return (match.group(1), match.group(2))
        return None

    def generate_new_filename(self, spec_id: str, spec_name: str, extension: str) -> Optional[str]:
        """Generate new filename in format: PREFIX-NUMBER-descriptive_name.ext"""
        parts = self.extract_prefix_and_number(spec_id)
        if not parts:
            return None

        prefix, number = parts

        # Clean and validate name
        clean_name = spec_name.lower()
        clean_name = re.sub(r'[^a-z0-9_-]', '_', clean_name)
        clean_name = re.sub(r'_+', '_', clean_name)
        clean_name = clean_name.strip('_')

        if not clean_name or any(placeholder in clean_name for placeholder in ['placeholder', 'example', 'todo']):
            return None

        return f"{prefix}-{number}-{clean_name}{extension}"

    def migrate_file(self, file_path: Path) -> bool:
        """Migrate a single spec file to new naming convention"""
        result = self.parse_spec_file(file_path)
        if not result:
            return False

        spec_id, spec_type, spec_name, content = result

        # Check if filename already matches new format
        current_filename = file_path.stem
        if re.match(r'^[A-Z]+-\d+-[a-z0-9_-]+$', current_filename):
            if self.verbose:
                print(f"{Colors.GREEN}✓{Colors.NC} {file_path.name} already uses new format")
            return True

        # If no name or placeholder name, try to suggest one
        if not spec_name or any(placeholder in spec_name.lower() for placeholder in ['placeholder', 'example', 'todo', '[', 'xxx']):
            suggested = self.suggest_name_from_content(spec_type, content, file_path)
            if suggested:
                print(f"{Colors.YELLOW}Suggested name for {file_path.name}:{Colors.NC} {suggested}")
                spec_name = suggested
            else:
                print(f"{Colors.YELLOW}⚠ Could not auto-generate name for {file_path.name} - manual intervention needed{Colors.NC}")
                return False

        # Generate new filename
        new_filename = self.generate_new_filename(spec_id, spec_name, file_path.suffix)
        if not new_filename:
            print(f"{Colors.YELLOW}⚠ Could not generate new filename for {file_path.name}{Colors.NC}")
            return False

        new_path = file_path.parent / new_filename

        # Check if target already exists
        if new_path.exists() and new_path != file_path:
            self.errors.append(f"Target file already exists: {new_path}")
            return False

        # Record migration
        self.migrations.append((file_path, new_path))

        if self.dry_run:
            print(f"{Colors.BLUE}Would rename:{Colors.NC} {file_path.name} → {new_filename}")
        else:
            try:
                file_path.rename(new_path)
                print(f"{Colors.GREEN}✓ Renamed:{Colors.NC} {file_path.name} → {new_filename}")
            except Exception as e:
                self.errors.append(f"Error renaming {file_path}: {str(e)}")
                return False

        return True

    def migrate_directory(self, directory: Path, recursive: bool = True) -> Dict[str, int]:
        """Migrate all spec files in a directory"""
        stats = {
            'total': 0,
            'migrated': 0,
            'already_compliant': 0,
            'failed': 0
        }

        # Find all spec files
        patterns = ['**/*.yaml', '**/*.md'] if recursive else ['*.yaml', '*.md']

        spec_files = []
        for pattern in patterns:
            for file_path in directory.glob(pattern):
                # Skip templates and non-spec files
                if 'templates' in str(file_path):
                    continue
                if 'README' in file_path.name:
                    continue

                # Only migrate files in specs/ directory
                if 'specs/' not in str(file_path):
                    continue

                spec_files.append(file_path)

        for file_path in spec_files:
            stats['total'] += 1

            result = self.parse_spec_file(file_path)
            if not result:
                stats['failed'] += 1
                continue

            spec_id, spec_type, spec_name, content = result

            # Check if already compliant
            current_filename = file_path.stem
            if re.match(r'^[A-Z]+-\d+-[a-z0-9_-]+$', current_filename):
                stats['already_compliant'] += 1
                continue

            # Try to migrate
            if self.migrate_file(file_path):
                stats['migrated'] += 1
            else:
                stats['failed'] += 1

        return stats

    def print_report(self, stats: Dict[str, int]):
        """Print migration report"""
        print("\n" + "="*60)
        print(" SPECIFICATION MIGRATION REPORT")
        print("="*60)

        print(f"\nFiles Processed: {stats['total']}")
        print(f"Already Compliant: {Colors.GREEN}{stats['already_compliant']}{Colors.NC}")
        print(f"Migrated: {Colors.BLUE}{stats['migrated']}{Colors.NC}")
        print(f"Failed: {Colors.RED}{stats['failed']}{Colors.NC}")

        if self.errors:
            print(f"\n{Colors.RED}Errors:{Colors.NC}")
            for error in self.errors:
                print(f"  {error}")

        if self.dry_run:
            print(f"\n{Colors.YELLOW}DRY RUN - No files were actually renamed{Colors.NC}")
            print(f"Run with --apply to perform the migration")

        print("\n" + "="*60)

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Migrate specification files to new descriptive naming convention",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s /specs/                    # Dry run migration (preview)
  %(prog)s /specs/ --apply            # Actually perform migration
  %(prog)s /specs/test-cases/         # Migrate only test cases
  %(prog)s /specs/ --verbose          # Show detailed output
        """
    )

    parser.add_argument(
        "path",
        help="Path to spec directory"
    )

    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually perform the migration (default is dry run)"
    )

    parser.add_argument(
        "--no-recursive",
        action="store_true",
        help="Don't recurse into subdirectories"
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output"
    )

    args = parser.parse_args()

    path = Path(args.path)
    if not path.exists():
        print(f"Error: Path not found: {path}", file=sys.stderr)
        sys.exit(2)

    if not path.is_dir():
        print(f"Error: Path must be a directory: {path}", file=sys.stderr)
        sys.exit(2)

    # Find repo root
    repo_root = path
    while repo_root.parent != repo_root:
        if (repo_root / '.specify').exists() or (repo_root / 'templates').exists():
            break
        repo_root = repo_root.parent

    migrator = SpecMigrator(
        repo_root,
        dry_run=not args.apply,
        verbose=args.verbose
    )

    stats = migrator.migrate_directory(path, not args.no_recursive)
    migrator.print_report(stats)

    sys.exit(1 if stats['failed'] > 0 else 0)

if __name__ == "__main__":
    main()