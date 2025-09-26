#!/usr/bin/env python3
"""
Specification Validation Tool
Validates specs against template requirements and constitution rules
"""

import os
import re
import sys
import yaml
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple, Optional
from collections import defaultdict

class Colors:
    """Terminal colors for output"""
    RED = '\033[0;31m'
    YELLOW = '\033[1;33m'
    GREEN = '\033[0;32m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'

class ValidationError:
    """Represents a validation error"""
    def __init__(self, file_path: Path, severity: str, message: str, line: Optional[int] = None):
        self.file_path = file_path
        self.severity = severity  # 'error', 'warning', 'info'
        self.message = message
        self.line = line

    def __str__(self):
        location = f":{self.line}" if self.line else ""
        severity_color = {
            'error': Colors.RED,
            'warning': Colors.YELLOW,
            'info': Colors.BLUE
        }.get(self.severity, Colors.NC)

        return f"{severity_color}{self.severity.upper()}{Colors.NC}: {self.file_path}{location}: {self.message}"

class SpecValidator:
    """Validates specification files"""

    # Required fields for different spec types
    REQUIRED_FIELDS = {
        'TestCase': ['id', 'name', 'type', 'hash_timestamp', 'purpose', 'steps'],
        'ScenarioCase': ['id', 'name', 'type', 'hash_timestamp', 'purpose', 'test_cases'],
        'PreconditionCase': ['id', 'name', 'type', 'hash_timestamp', 'purpose', 'setup_steps'],
        'Workflow': ['id', 'name', 'type', 'hash_timestamp'],
        'Page': ['id', 'name', 'type', 'hash_timestamp'],
        'Concept': ['id', 'name', 'type', 'hash_timestamp'],
        'DataSchema': ['id', 'name', 'type', 'hash_timestamp'],
        'Contract': ['id', 'name', 'type', 'hash_timestamp'],
        'Integration': ['id', 'name', 'type', 'hash_timestamp'],
        'Security': ['id', 'name', 'type', 'hash_timestamp'],
        'Configuration': ['id', 'name', 'type', 'hash_timestamp'],
        'Technology': ['id', 'name', 'type', 'hash_timestamp'],
        'Event': ['id', 'name', 'type', 'hash_timestamp'],
        'Message': ['id', 'name', 'type', 'hash_timestamp'],
    }

    # Valid ID prefixes for each type
    ID_PREFIXES = {
        'TestCase': 'TC',
        'ScenarioCase': 'SC',
        'PreconditionCase': 'PC',
        'Workflow': 'W',
        'Page': 'P',
        'Concept': 'C',
        'DataSchema': 'DATA',
        'Contract': 'CONTRACT',
        'Integration': 'INT',
        'Security': 'SEC',
        'Configuration': 'CONFIG',
        'Technology': 'TECH',
        'Event': 'EVENT',
        'Message': 'MESSAGE',
    }

    # Valid status values
    VALID_STATUSES = ['draft', 'ready', 'active', 'deprecated']

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.errors: List[ValidationError] = []

    def validate_timestamp(self, timestamp: str, file_path: Path) -> bool:
        """Validate ISO 8601 timestamp format"""
        pattern = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$'
        if not re.match(pattern, timestamp):
            self.errors.append(ValidationError(
                file_path,
                'error',
                f"Invalid timestamp format: '{timestamp}'. Must be YYYY-MM-DDTHH:MM:SSZ"
            ))
            return False

        # Try parsing to ensure it's a valid date
        try:
            datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
        except ValueError as e:
            self.errors.append(ValidationError(
                file_path,
                'error',
                f"Invalid timestamp value: '{timestamp}'. {str(e)}"
            ))
            return False

        return True

    def validate_id_format(self, spec_id: str, spec_type: str, file_path: Path) -> bool:
        """Validate spec ID format"""
        expected_prefix = self.ID_PREFIXES.get(spec_type)
        if not expected_prefix:
            self.errors.append(ValidationError(
                file_path,
                'warning',
                f"Unknown spec type: '{spec_type}'"
            ))
            return False

        pattern = f"^{expected_prefix}-[0-9]+$"
        if not re.match(pattern, spec_id):
            self.errors.append(ValidationError(
                file_path,
                'error',
                f"Invalid ID format: '{spec_id}'. Must match pattern '{expected_prefix}-XXX'"
            ))
            return False

        return True

    def validate_scenario_phases(self, content: Dict, file_path: Path) -> bool:
        """Validate phase structure in ScenarioCase"""
        phases = content.get('phases', [])

        if not isinstance(phases, list):
            self.errors.append(ValidationError(
                file_path,
                'error',
                "'phases' must be a list"
            ))
            return False

        if len(phases) == 0:
            self.errors.append(ValidationError(
                file_path,
                'warning',
                "ScenarioCase has empty 'phases' list"
            ))
            return False

        phase_ids = set()
        for idx, phase in enumerate(phases):
            if not isinstance(phase, dict):
                self.errors.append(ValidationError(
                    file_path,
                    'error',
                    f"Phase {idx+1} must be a dictionary"
                ))
                continue

            # Check required phase fields
            required_phase_fields = ['phase_id', 'phase_name', 'description', 'preconditions', 'test_cases']
            for field in required_phase_fields:
                if field not in phase:
                    self.errors.append(ValidationError(
                        file_path,
                        'error',
                        f"Phase {idx+1} missing required field: '{field}'"
                    ))

            # Validate phase_id uniqueness
            phase_id = phase.get('phase_id')
            if phase_id:
                if phase_id in phase_ids:
                    self.errors.append(ValidationError(
                        file_path,
                        'error',
                        f"Duplicate phase_id: '{phase_id}'"
                    ))
                phase_ids.add(phase_id)

            # Validate preconditions array
            preconditions = phase.get('preconditions', [])
            if not isinstance(preconditions, list):
                self.errors.append(ValidationError(
                    file_path,
                    'error',
                    f"Phase '{phase_id}' preconditions must be a list"
                ))
            else:
                for pc_idx, precondition in enumerate(preconditions):
                    if isinstance(precondition, dict):
                        if 'path' not in precondition:
                            self.errors.append(ValidationError(
                                file_path,
                                'error',
                                f"Phase '{phase_id}' precondition {pc_idx+1} missing 'path' field"
                            ))
                        else:
                            self.validate_case_path(precondition['path'], 'PC', file_path)

            # Validate test_cases array
            test_cases = phase.get('test_cases', [])
            if not isinstance(test_cases, list):
                self.errors.append(ValidationError(
                    file_path,
                    'error',
                    f"Phase '{phase_id}' test_cases must be a list"
                ))
            else:
                for tc_idx, test_case in enumerate(test_cases):
                    if isinstance(test_case, dict):
                        if 'path' not in test_case:
                            self.errors.append(ValidationError(
                                file_path,
                                'error',
                                f"Phase '{phase_id}' test_case {tc_idx+1} missing 'path' field"
                            ))
                        else:
                            self.validate_case_path(test_case['path'], 'TC', file_path)

        return True

    def validate_case_path(self, path: str, expected_prefix: str, file_path: Path) -> bool:
        """Validate case file path format"""
        if not path.startswith('/specs/'):
            self.errors.append(ValidationError(
                file_path,
                'error',
                f"Invalid case path: '{path}'. Must start with '/specs/'"
            ))
            return False

        # Check path matches expected pattern
        if expected_prefix == 'TC' and not path.startswith('/specs/test-cases/'):
            self.errors.append(ValidationError(
                file_path,
                'warning',
                f"Test case path should start with '/specs/test-cases/': '{path}'"
            ))
        elif expected_prefix == 'PC' and not path.startswith('/specs/precondition-cases/'):
            self.errors.append(ValidationError(
                file_path,
                'warning',
                f"Precondition case path should start with '/specs/precondition-cases/': '{path}'"
            ))

        # Check file extension
        if not path.endswith('.yaml') and not path.endswith('.yml'):
            self.errors.append(ValidationError(
                file_path,
                'warning',
                f"Case path should end with .yaml or .yml: '{path}'"
            ))

        return True

    def validate_yaml_case(self, file_path: Path) -> bool:
        """Validate YAML case file (TC, SC, PC)"""
        try:
            with open(file_path, 'r') as f:
                content = yaml.safe_load(f)

            if not content:
                self.errors.append(ValidationError(
                    file_path,
                    'error',
                    "Empty YAML file"
                ))
                return False

            # Check spec type
            spec_type = content.get('type')
            if not spec_type:
                self.errors.append(ValidationError(
                    file_path,
                    'error',
                    "Missing 'type' field"
                ))
                return False

            # Check required fields
            required = self.REQUIRED_FIELDS.get(spec_type, [])
            for field in required:
                if field not in content:
                    self.errors.append(ValidationError(
                        file_path,
                        'error',
                        f"Missing required field: '{field}'"
                    ))

            # Validate ID format
            if 'id' in content and 'type' in content:
                self.validate_id_format(content['id'], content['type'], file_path)

            # Validate timestamp
            if 'hash_timestamp' in content:
                self.validate_timestamp(content['hash_timestamp'], file_path)

            # Validate status
            if 'status' in content:
                if content['status'] not in self.VALID_STATUSES:
                    self.errors.append(ValidationError(
                        file_path,
                        'warning',
                        f"Invalid status: '{content['status']}'. Valid values: {', '.join(self.VALID_STATUSES)}"
                    ))

            # Validate phase structure for ScenarioCase
            if spec_type == 'ScenarioCase' and 'phases' in content:
                self.validate_scenario_phases(content, file_path)

            return True

        except yaml.YAMLError as e:
            self.errors.append(ValidationError(
                file_path,
                'error',
                f"YAML parsing error: {str(e)}"
            ))
            return False
        except Exception as e:
            self.errors.append(ValidationError(
                file_path,
                'error',
                f"Validation error: {str(e)}"
            ))
            return False

    def validate_markdown_spec(self, file_path: Path) -> bool:
        """Validate Markdown spec file"""
        try:
            with open(file_path, 'r') as f:
                content = f.read()

            # Extract YAML frontmatter
            yaml_match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
            if not yaml_match:
                self.errors.append(ValidationError(
                    file_path,
                    'error',
                    "Missing YAML frontmatter"
                ))
                return False

            frontmatter_text = yaml_match.group(1)
            frontmatter = yaml.safe_load(frontmatter_text)

            # Check spec type
            spec_type = frontmatter.get('type')
            if not spec_type:
                self.errors.append(ValidationError(
                    file_path,
                    'error',
                    "Missing 'type' field in frontmatter"
                ))
                return False

            # Check required fields
            required = self.REQUIRED_FIELDS.get(spec_type, [])
            for field in required:
                if field not in frontmatter:
                    self.errors.append(ValidationError(
                        file_path,
                        'error',
                        f"Missing required field: '{field}'"
                    ))

            # Validate ID format
            if 'id' in frontmatter and 'type' in frontmatter:
                self.validate_id_format(frontmatter['id'], frontmatter['type'], file_path)

            # Validate timestamp
            if 'hash_timestamp' in frontmatter:
                self.validate_timestamp(frontmatter['hash_timestamp'], file_path)

            # Validate status
            if 'status' in frontmatter:
                if frontmatter['status'] not in self.VALID_STATUSES:
                    self.errors.append(ValidationError(
                        file_path,
                        'warning',
                        f"Invalid status: '{frontmatter['status']}'. Valid values: {', '.join(self.VALID_STATUSES)}"
                    ))

            # Check for required sections (informational)
            required_sections = ['## Validation Cases', '## Implementation References']
            for section in required_sections:
                if section not in content:
                    self.errors.append(ValidationError(
                        file_path,
                        'info',
                        f"Missing recommended section: '{section}'"
                    ))

            return True

        except yaml.YAMLError as e:
            self.errors.append(ValidationError(
                file_path,
                'error',
                f"YAML frontmatter parsing error: {str(e)}"
            ))
            return False
        except Exception as e:
            self.errors.append(ValidationError(
                file_path,
                'error',
                f"Validation error: {str(e)}"
            ))
            return False

    def validate_file(self, file_path: Path) -> bool:
        """Validate a single spec file"""
        if file_path.suffix in ['.yaml', '.yml']:
            return self.validate_yaml_case(file_path)
        elif file_path.suffix == '.md':
            return self.validate_markdown_spec(file_path)
        else:
            return True  # Skip unknown file types

    def validate_directory(self, directory: Path, recursive: bool = True) -> Dict[str, int]:
        """Validate all spec files in a directory"""
        stats = {
            'total': 0,
            'passed': 0,
            'errors': 0,
            'warnings': 0,
            'info': 0
        }

        # Find all spec files
        patterns = ['**/*.yaml', '**/*.yml', '**/*.md'] if recursive else ['*.yaml', '*.yml', '*.md']

        for pattern in patterns:
            for file_path in directory.glob(pattern):
                # Skip templates and non-spec files
                if '.specify/templates' in str(file_path):
                    continue
                if 'README' in file_path.name:
                    continue

                # Only validate files in specs/ or plans/
                if 'specs/' not in str(file_path) and 'plans/' not in str(file_path):
                    continue

                stats['total'] += 1
                errors_before = len([e for e in self.errors if e.severity == 'error'])

                self.validate_file(file_path)

                errors_after = len([e for e in self.errors if e.severity == 'error'])
                if errors_after == errors_before:
                    stats['passed'] += 1

        # Count errors by severity
        for error in self.errors:
            if error.severity == 'error':
                stats['errors'] += 1
            elif error.severity == 'warning':
                stats['warnings'] += 1
            elif error.severity == 'info':
                stats['info'] += 1

        return stats

    def print_report(self, stats: Dict[str, int]):
        """Print validation report"""
        print("\n" + "="*60)
        print(" SPECIFICATION VALIDATION REPORT")
        print("="*60)

        print(f"\nFiles Validated: {stats['total']}")
        print(f"Passed: {Colors.GREEN}{stats['passed']}{Colors.NC}")
        print(f"Errors: {Colors.RED}{stats['errors']}{Colors.NC}")
        print(f"Warnings: {Colors.YELLOW}{stats['warnings']}{Colors.NC}")
        print(f"Info: {Colors.BLUE}{stats['info']}{Colors.NC}")

        if self.errors:
            print(f"\n{Colors.RED}Validation Issues:{Colors.NC}\n")
            for error in self.errors:
                print(error)

        print("\n" + "="*60)

        if stats['errors'] > 0:
            print(f"{Colors.RED}✗ Validation failed with {stats['errors']} errors{Colors.NC}")
            return 1
        elif stats['warnings'] > 0:
            print(f"{Colors.YELLOW}⚠ Validation passed with {stats['warnings']} warnings{Colors.NC}")
            return 0
        else:
            print(f"{Colors.GREEN}✓ All specs are valid{Colors.NC}")
            return 0

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Validate Specify framework specifications",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s /specs/                    # Validate all specs
  %(prog)s /specs/test-cases/         # Validate test cases only
  %(prog)s /specs/test-cases/TC-001.yaml  # Validate single file
  %(prog)s --no-recursive /specs/     # Validate only top-level files
        """
    )

    parser.add_argument(
        "path",
        help="Path to spec file or directory"
    )

    parser.add_argument(
        "--no-recursive",
        action="store_true",
        help="Don't recurse into subdirectories"
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Output in JSON format"
    )

    args = parser.parse_args()

    path = Path(args.path)
    if not path.exists():
        print(f"Error: Path not found: {path}", file=sys.stderr)
        sys.exit(2)

    # Find repo root
    repo_root = path
    while repo_root.parent != repo_root:
        if (repo_root / '.specify').exists():
            break
        repo_root = repo_root.parent

    validator = SpecValidator(repo_root)

    if path.is_file():
        # Validate single file
        validator.validate_file(path)
        stats = {
            'total': 1,
            'passed': 1 if not validator.errors else 0,
            'errors': len([e for e in validator.errors if e.severity == 'error']),
            'warnings': len([e for e in validator.errors if e.severity == 'warning']),
            'info': len([e for e in validator.errors if e.severity == 'info'])
        }
    else:
        # Validate directory
        stats = validator.validate_directory(path, not args.no_recursive)

    if args.json:
        import json
        json_output = {
            'stats': stats,
            'errors': [
                {
                    'file': str(e.file_path),
                    'severity': e.severity,
                    'message': e.message,
                    'line': e.line
                }
                for e in validator.errors
            ]
        }
        print(json.dumps(json_output, indent=2))
        sys.exit(1 if stats['errors'] > 0 else 0)
    else:
        exit_code = validator.print_report(stats)
        sys.exit(exit_code)

if __name__ == "__main__":
    main()