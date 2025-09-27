#!/usr/bin/env python3
"""
Fix Spec References Tool
Automatically fixes common reference issues in specification files
"""

import os
import re
import sys
import yaml
from pathlib import Path
from typing import List, Dict, Tuple
from datetime import datetime

class Colors:
    """Terminal colors for output"""
    RED = '\033[0;31m'
    YELLOW = '\033[1;33m'
    GREEN = '\033[0;32m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'

class ReferenceFixer:
    """Fixes common reference issues in spec files"""

    def __init__(self, repo_root: Path, dry_run: bool = True):
        self.repo_root = repo_root
        self.dry_run = dry_run
        self.fixes_applied = 0
        self.files_modified = 0
        self.errors: List[str] = []

        # Build index of all spec IDs and their names
        self.spec_index = self._build_spec_index()

    def _build_spec_index(self) -> Dict[str, Dict]:
        """Build index of all specs with their IDs, names, and paths"""
        index = {}

        specs_dir = self.repo_root / 'specs'
        if not specs_dir.exists():
            return index

        # Find all spec files
        for pattern in ['**/*.yaml', '**/*.md']:
            for file_path in specs_dir.glob(pattern):
                try:
                    if file_path.suffix == '.yaml':
                        with open(file_path, 'r') as f:
                            content = yaml.safe_load(f)
                            if content and 'id' in content and 'name' in content:
                                index[content['id']] = {
                                    'name': content['name'],
                                    'path': file_path,
                                    'type': content.get('type', 'Unknown')
                                }
                    elif file_path.suffix == '.md':
                        with open(file_path, 'r') as f:
                            content = f.read()
                            yaml_match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
                            if yaml_match:
                                frontmatter = yaml.safe_load(yaml_match.group(1))
                                if frontmatter and 'id' in frontmatter and 'name' in frontmatter:
                                    index[frontmatter['id']] = {
                                        'name': frontmatter['name'],
                                        'path': file_path,
                                        'type': frontmatter.get('type', 'Unknown')
                                    }
                except Exception as e:
                    pass  # Skip files that can't be parsed

        return index

    def fix_yaml_file(self, file_path: Path) -> int:
        """Fix references in a YAML case file"""
        fixes = 0

        try:
            with open(file_path, 'r') as f:
                content = yaml.safe_load(f)
                original_yaml = f.read()

            if not content:
                return 0

            modified = False
            new_content = content.copy()

            # Fix preconditions array if present
            if 'preconditions' in content:
                fixed_preconditions = []
                for pc in content['preconditions']:
                    if isinstance(pc, str):
                        # Convert string to path object
                        if not pc.startswith('/specs/'):
                            pc = f"/specs/precondition-cases/{pc}.yaml" if not pc.endswith('.yaml') else f"/specs/precondition-cases/{pc}"
                        fixed_preconditions.append({'path': pc, 'description': ''})
                        modified = True
                        fixes += 1
                    elif isinstance(pc, dict) and 'path' in pc:
                        # Already in correct format
                        fixed_preconditions.append(pc)
                    else:
                        fixed_preconditions.append(pc)

                if modified:
                    new_content['preconditions'] = fixed_preconditions

            # Fix related array if present - ensure IDs exist
            if 'related' in content and isinstance(content['related'], list):
                fixed_related = []
                for ref in content['related']:
                    ref_id = ref if isinstance(ref, str) else ref.get('id')
                    if ref_id and ref_id in self.spec_index:
                        fixed_related.append(ref_id)
                    elif ref_id:
                        self.errors.append(f"{file_path}: Referenced spec '{ref_id}' not found")

                if len(fixed_related) != len(content['related']):
                    new_content['related'] = fixed_related
                    modified = True
                    fixes += 1

            # Update timestamp if we modified the file
            if modified:
                new_content['hash_timestamp'] = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

                if not self.dry_run:
                    with open(file_path, 'w') as f:
                        yaml.dump(new_content, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
                    self.files_modified += 1

        except Exception as e:
            self.errors.append(f"{file_path}: Error fixing file: {e}")

        return fixes

    def fix_markdown_file(self, file_path: Path) -> int:
        """Fix references in a Markdown spec file"""
        fixes = 0

        try:
            with open(file_path, 'r') as f:
                content = f.read()

            original_content = content
            modified = False

            # Fix case references in validation_cases section
            # Convert: - TC-001: Description
            # To:      - /specs/test-cases/TC-001-name.yaml: Description
            def fix_case_reference(match):
                nonlocal fixes, modified
                prefix = match.group(1)
                case_id = match.group(2)
                description = match.group(3)

                # Try to find the actual file
                if case_id in self.spec_index:
                    spec_info = self.spec_index[case_id]
                    path = spec_info['path'].relative_to(self.repo_root)
                    modified = True
                    fixes += 1
                    return f"- /{path}: {description}"
                else:
                    return match.group(0)  # Keep original if not found

            # Fix test case references
            content = re.sub(
                r'^(\s*)-\s*(TC-\d+):\s*(.+)$',
                fix_case_reference,
                content,
                flags=re.MULTILINE
            )

            # Fix scenario case references
            content = re.sub(
                r'^(\s*)-\s*(SC-\d+):\s*(.+)$',
                fix_case_reference,
                content,
                flags=re.MULTILINE
            )

            # Fix precondition case references
            content = re.sub(
                r'^(\s*)-\s*(PC-\d+):\s*(.+)$',
                fix_case_reference,
                content,
                flags=re.MULTILINE
            )

            # Update timestamp in frontmatter if modified
            if modified:
                yaml_match = re.match(r'^(---\s*\n)(.*?)(\n---)', content, re.DOTALL)
                if yaml_match:
                    frontmatter = yaml.safe_load(yaml_match.group(2))
                    frontmatter['hash_timestamp'] = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
                    new_frontmatter = yaml.dump(frontmatter, default_flow_style=False, sort_keys=False)
                    content = yaml_match.group(1) + new_frontmatter + yaml_match.group(3) + content[yaml_match.end():]

                if not self.dry_run:
                    with open(file_path, 'w') as f:
                        f.write(content)
                    self.files_modified += 1

        except Exception as e:
            self.errors.append(f"{file_path}: Error fixing file: {e}")

        return fixes

    def fix_directory(self, directory: Path) -> Dict[str, int]:
        """Fix all spec files in a directory"""
        stats = {
            'files_scanned': 0,
            'files_modified': 0,
            'fixes_applied': 0,
            'errors': 0
        }

        # Find all spec files
        for pattern in ['**/*.yaml', '**/*.md']:
            for file_path in directory.glob(pattern):
                # Skip templates
                if 'templates' in str(file_path):
                    continue

                stats['files_scanned'] += 1

                if file_path.suffix == '.yaml':
                    fixes = self.fix_yaml_file(file_path)
                elif file_path.suffix == '.md':
                    fixes = self.fix_markdown_file(file_path)
                else:
                    continue

                if fixes > 0:
                    stats['fixes_applied'] += fixes
                    print(f"{Colors.GREEN}✓{Colors.NC} Fixed {fixes} issues in {file_path}")

        stats['files_modified'] = self.files_modified
        stats['errors'] = len(self.errors)

        return stats

    def print_report(self, stats: Dict[str, int]):
        """Print fix report"""
        print("\n" + "="*60)
        print(" REFERENCE FIX REPORT")
        print("="*60)

        mode = "DRY RUN - No changes made" if self.dry_run else "APPLIED CHANGES"
        print(f"\nMode: {Colors.YELLOW if self.dry_run else Colors.GREEN}{mode}{Colors.NC}")

        print(f"\nFiles Scanned: {stats['files_scanned']}")
        print(f"Files Modified: {Colors.GREEN}{stats['files_modified']}{Colors.NC}")
        print(f"Fixes Applied: {Colors.GREEN}{stats['fixes_applied']}{Colors.NC}")
        print(f"Errors: {Colors.RED}{stats['errors']}{Colors.NC}")

        if self.errors:
            print(f"\n{Colors.RED}Errors:{Colors.NC}\n")
            for error in self.errors:
                print(f"  {Colors.RED}✗{Colors.NC} {error}")

        print("\n" + "="*60)

        if self.dry_run and stats['fixes_applied'] > 0:
            print(f"{Colors.YELLOW}⚠ Run with --apply to make changes{Colors.NC}")
        elif stats['fixes_applied'] > 0:
            print(f"{Colors.GREEN}✓ Applied {stats['fixes_applied']} fixes{Colors.NC}")
        else:
            print(f"{Colors.GREEN}✓ No fixes needed{Colors.NC}")

def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Automatically fix common reference issues in spec files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s /specs/                    # Dry run - show what would be fixed
  %(prog)s /specs/ --apply           # Apply fixes
  %(prog)s /specs/test-cases/        # Fix only test cases
        """
    )

    parser.add_argument(
        "path",
        help="Path to spec directory"
    )

    parser.add_argument(
        "--apply",
        action="store_true",
        help="Apply fixes (default is dry run)"
    )

    args = parser.parse_args()

    path = Path(args.path)
    if not path.exists():
        print(f"Error: Path not found: {path}", file=sys.stderr)
        sys.exit(2)

    # Find repo root
    repo_root = path if path.is_dir() else path.parent
    while repo_root.parent != repo_root:
        if (repo_root / '.specify').exists() or (repo_root / 'specs').exists():
            break
        repo_root = repo_root.parent

    fixer = ReferenceFixer(repo_root, dry_run=not args.apply)

    print(f"{Colors.BLUE}Building spec index...{Colors.NC}")
    print(f"Found {len(fixer.spec_index)} specs")

    print(f"\n{Colors.BLUE}Scanning for reference issues...{Colors.NC}")
    stats = fixer.fix_directory(path)

    fixer.print_report(stats)

    sys.exit(1 if stats['errors'] > 0 else 0)

if __name__ == "__main__":
    main()