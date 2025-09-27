#!/usr/bin/env python3
"""
Template Validator
Validates spec template files for structural integrity and consistency
"""

import os
import re
import sys
import yaml
from pathlib import Path
from typing import List, Dict, Optional

class Colors:
    """Terminal colors for output"""
    RED = '\033[0;31m'
    YELLOW = '\033[1;33m'
    GREEN = '\033[0;32m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'

class TemplateValidator:
    """Validates template files and documentation references"""

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.template_dir = None
        self.errors: List[str] = []
        self.warnings: List[str] = []

        # Find templates directory
        possible_dirs = [
            repo_root / '.specify' / 'templates',
            repo_root / 'templates'
        ]
        for template_dir in possible_dirs:
            if template_dir.exists():
                self.template_dir = template_dir
                break

    def validate_template_metadata(self, template_file: Path) -> Optional[Dict]:
        """Validate that template has required metadata"""
        try:
            if template_file.suffix == '.yaml':
                with open(template_file, 'r') as f:
                    lines = []
                    for i, line in enumerate(f):
                        if i >= 20:
                            break
                        lines.append(line)
                    content = ''.join(lines)

                # Parse YAML
                parsed = yaml.safe_load(content)
                if not parsed:
                    self.errors.append(f"{template_file.name}: Cannot parse YAML")
                    return None

                # Check required fields
                required = ['type', 'id_prefix', 'name_guidelines', 'name_examples', 'file_extension']
                for field in required:
                    if field not in parsed:
                        self.errors.append(f"{template_file.name}: Missing required field '{field}'")
                        return None

                return parsed

            elif template_file.suffix == '.md':
                with open(template_file, 'r') as f:
                    content = f.read(2000)

                # Extract metadata from HTML comment
                comment_match = re.search(r'<!--\s*Template Metadata.*?type:\s*([^\n]+)\s*id_prefix:\s*([^\n]+)\s*name_guidelines:\s*"([^"]+)"\s*name_examples:\s*\[(.*?)\]\s*file_extension:\s*([^\n]+)', content, re.DOTALL)

                if not comment_match:
                    self.errors.append(f"{template_file.name}: Missing or invalid template metadata comment")
                    return None

                type_name = comment_match.group(1).strip()
                prefix = comment_match.group(2).strip()
                guidelines = comment_match.group(3).strip()
                examples_str = comment_match.group(4).strip()
                extension = comment_match.group(5).strip()

                # Parse examples
                examples = []
                for match in re.finditer(r'"([^"]+)"', examples_str):
                    examples.append(match.group(1))

                if not examples:
                    self.warnings.append(f"{template_file.name}: No name examples provided")

                return {
                    'type': type_name,
                    'id_prefix': prefix,
                    'name_guidelines': guidelines,
                    'name_examples': examples,
                    'file_extension': extension
                }

        except Exception as e:
            self.errors.append(f"{template_file.name}: Error parsing template: {e}")
            return None

        return None

    def validate_templates(self) -> bool:
        """Validate all template files"""
        if not self.template_dir:
            self.errors.append("Template directory not found")
            return False

        templates = {}
        prefixes_used = {}

        # Validate each template
        for pattern in ['spec-*.yaml', 'spec-*.md']:
            for template_file in self.template_dir.glob(pattern):
                metadata = self.validate_template_metadata(template_file)
                if not metadata:
                    continue

                type_name = metadata['type']
                prefix = metadata['id_prefix']

                # Check for duplicate types
                if type_name in templates:
                    self.errors.append(f"Duplicate type '{type_name}' in {template_file.name} and {templates[type_name]}")
                else:
                    templates[type_name] = template_file.name

                # Check for duplicate prefixes
                if prefix and prefix in prefixes_used:
                    self.errors.append(f"Duplicate prefix '{prefix}' used by '{type_name}' and '{prefixes_used[prefix]}'")
                elif prefix:
                    prefixes_used[prefix] = type_name

        return len(self.errors) == 0

    def validate_type_registry(self) -> bool:
        """Validate that type registry is up to date"""
        registry_path = self.repo_root / '.specify' / 'schemas' / 'type-registry.yaml'

        if not registry_path.exists():
            self.errors.append("Type registry not found: .specify/schemas/type-registry.yaml")
            self.errors.append("Run: python .specify/scripts/generate-type-registry.py")
            return False

        # Check if registry is stale
        registry_mtime = registry_path.stat().st_mtime

        # Check if any template is newer than registry
        stale = False
        for pattern in ['spec-*.yaml', 'spec-*.md']:
            for template_file in self.template_dir.glob(pattern):
                if template_file.stat().st_mtime > registry_mtime:
                    stale = True
                    self.warnings.append(f"Type registry is older than {template_file.name}")

        if stale:
            self.warnings.append("Run: python .specify/scripts/generate-type-registry.py")

        return True

    def validate_documentation_references(self) -> bool:
        """Validate that documentation files reference the schema correctly"""
        schema_path = ".specify/schemas/template-schema.json"
        registry_path = ".specify/schemas/type-registry.yaml"

        # Check specify.md
        specify_path = self.repo_root / 'commands' / 'specify.md'
        if specify_path.exists():
            with open(specify_path, 'r') as f:
                content = f.read()

            # Check for schema reference
            if schema_path not in content:
                self.warnings.append(f"specify.md should reference {schema_path}")

            # Check for registry reference
            if registry_path not in content:
                self.warnings.append(f"specify.md should reference {registry_path}")

        # Check constitution.md
        constitution_path = self.repo_root / 'memory' / 'constitution.md'
        if constitution_path.exists():
            with open(constitution_path, 'r') as f:
                content = f.read()

            # Check for schema reference
            if schema_path not in content:
                self.warnings.append(f"constitution.md should reference {schema_path}")

        return True

    def print_report(self):
        """Print validation report"""
        print("\n" + "="*60)
        print(" TEMPLATE VALIDATION REPORT")
        print("="*60)

        if self.errors:
            print(f"\n{Colors.RED}Errors ({len(self.errors)}):{Colors.NC}")
            for error in self.errors:
                print(f"  {Colors.RED}✗{Colors.NC} {error}")

        if self.warnings:
            print(f"\n{Colors.YELLOW}Warnings ({len(self.warnings)}):{Colors.NC}")
            for warning in self.warnings:
                print(f"  {Colors.YELLOW}⚠{Colors.NC} {warning}")

        print("\n" + "="*60)

        if self.errors:
            print(f"{Colors.RED}✗ Template validation failed{Colors.NC}")
            return 1
        elif self.warnings:
            print(f"{Colors.YELLOW}⚠ Template validation passed with warnings{Colors.NC}")
            return 0
        else:
            print(f"{Colors.GREEN}✓ All templates are valid{Colors.NC}")
            return 0

def main():
    """Main entry point"""
    # Find repository root
    script_path = Path(__file__).resolve()
    repo_root = script_path.parent.parent.parent  # Go up from .specify/scripts/

    # Create validator
    validator = TemplateValidator(repo_root)

    # Run validation
    validator.validate_templates()
    validator.validate_type_registry()
    validator.validate_documentation_references()

    # Print report
    exit_code = validator.print_report()
    return exit_code

if __name__ == "__main__":
    sys.exit(main())