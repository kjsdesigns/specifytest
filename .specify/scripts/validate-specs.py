#!/usr/bin/env python3
"""
Specification Validation Tool
Validates specs against template-schema.json and type-registry.yaml
Single source of truth for all validation rules
"""

import os
import re
import sys
import yaml
import json
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

    # Valid status values
    VALID_STATUSES = ['draft', 'ready', 'active', 'deprecated']

    def __init__(self, repo_root: Path, check_filenames: bool = True, check_refs: bool = False, verbose: bool = False):
        self.repo_root = repo_root
        self.errors: List[ValidationError] = []
        self.check_filenames = check_filenames
        self.check_refs = check_refs
        self.verbose = verbose
        self.all_spec_ids: Dict[str, Path] = {}
        self.all_spec_names: Dict[str, Path] = {}  # Track unique names
        self.all_spec_files: List[Path] = []

        # Load validation schema (single source of truth)
        self.schema = self._load_schema()

        # Load type registry (generated from templates)
        self.type_registry = self._load_type_registry()

        # Build spec type info from registry
        self.spec_type_info = self._build_type_info()

    def _load_schema(self) -> Dict:
        """Load template-schema.json as single source of truth"""
        schema_paths = [
            self.repo_root / '.specify' / 'schemas' / 'template-schema.json',
            self.repo_root / 'schemas' / 'template-schema.json'
        ]

        for schema_path in schema_paths:
            if schema_path.exists():
                try:
                    with open(schema_path, 'r') as f:
                        schema = json.load(f)
                    if self.verbose:
                        print(f"{Colors.BLUE}Using validation schema:{Colors.NC} {schema_path}")
                    return schema
                except Exception as e:
                    if self.verbose:
                        print(f"{Colors.YELLOW}Warning: Could not load schema: {e}{Colors.NC}")

        if self.verbose:
            print(f"{Colors.YELLOW}Warning: No schema found, using built-in defaults{Colors.NC}")
        return {}

    def _load_type_registry(self) -> Dict:
        """Load type-registry.yaml generated from templates"""
        registry_paths = [
            self.repo_root / '.specify' / 'schemas' / 'type-registry.yaml',
            self.repo_root / 'schemas' / 'type-registry.yaml'
        ]

        for registry_path in registry_paths:
            if registry_path.exists():
                try:
                    with open(registry_path, 'r') as f:
                        registry = yaml.safe_load(f)
                    if self.verbose:
                        print(f"{Colors.BLUE}Using type registry:{Colors.NC} {registry_path}")
                    return registry
                except Exception as e:
                    if self.verbose:
                        print(f"{Colors.YELLOW}Warning: Could not load type registry: {e}{Colors.NC}")

        if self.verbose:
            print(f"{Colors.YELLOW}Warning: No type registry found{Colors.NC}")
        return {'types': {}}

    def _build_type_info(self) -> Dict[str, Dict]:
        """Build spec type info from type registry"""
        spec_types = {}

        if not self.type_registry or 'types' not in self.type_registry:
            return {}

        for type_name, type_data in self.type_registry['types'].items():
            spec_types[type_name] = {
                'type': type_name,
                'prefix': type_data.get('prefix', ''),
                'file_extension': type_data.get('extension', 'md'),
                'name_guidelines': type_data.get('guidelines', ''),
                'name_examples': type_data.get('examples', []),
                'required_fields': ['id', 'name', 'type', 'status', 'hash_timestamp']
            }

        return spec_types

    def get_name_pattern(self, spec_type: str) -> Optional[str]:
        """Get name pattern from schema for a spec type"""
        if not self.schema or 'definitions' not in self.schema:
            return None

        # Get common fields pattern
        common_fields = self.schema.get('definitions', {}).get('commonFields', {})
        name_field = common_fields.get('properties', {}).get('name', {})
        return name_field.get('pattern')

    def get_word_limit(self, spec_type: str) -> int:
        """Get word limit for spec names (default 4)"""
        # Word limit is defined in schema description: "max 4 words"
        return 4

    def validate_name_field(self, name: str, spec_type: str, file_path: Path) -> bool:
        """Validate the descriptive name field against schema rules"""
        # Check name pattern from schema
        name_pattern = self.get_name_pattern(spec_type)
        if name_pattern:
            if not re.match(name_pattern, name):
                type_info = self.spec_type_info.get(spec_type, {})
                guidelines = type_info.get('name_guidelines', 'descriptive name')
                self.errors.append(ValidationError(
                    file_path,
                    'error',
                    f"Invalid name format: '{name}'. Must match pattern {name_pattern} ({guidelines})"
                ))
                return False

        # Check word limit from schema
        word_limit = self.get_word_limit(spec_type)
        if word_limit:
            # Count words (split by underscores, hyphens, or spaces)
            words = re.split(r'[_\-\s]+', name)
            word_count = len([w for w in words if w])  # Filter empty strings
            if word_count > word_limit:
                self.errors.append(ValidationError(
                    file_path,
                    'error',
                    f"Name too long: '{name}' has {word_count} words, limit is {word_limit}"
                ))
                return False

        return True

    def check_duplicate_name(self, name: str, spec_type: str, file_path: Path) -> bool:
        """Check for duplicate spec names within the same type"""
        # Create composite key: type + name
        name_key = f"{spec_type}:{name}"

        if name_key in self.all_spec_names:
            existing_file = self.all_spec_names[name_key]
            self.errors.append(ValidationError(
                file_path,
                'error',
                f"Duplicate spec name '{name}' for type '{spec_type}'. Also exists in {existing_file}"
            ))
            return False

        self.all_spec_names[name_key] = file_path
        return True

    def validate_filename(self, file_path: Path, spec_id: str, spec_name: str, spec_type: str) -> bool:
        """Validate that filename matches expected pattern: [PREFIX]-[NUMBER]-[descriptive-name].[ext]"""
        if not self.check_filenames:
            return True

        filename = file_path.stem
        type_info = self.spec_type_info.get(spec_type)

        if not type_info:
            return True

        # Expected filename format: [PREFIX]-[NUMBER]-[descriptive-name]
        expected_prefix = type_info['prefix']

        # Parse filename into parts
        filename_parts = filename.split('-', 2)  # Split into at most 3 parts

        if len(filename_parts) < 3:
            self.errors.append(ValidationError(
                file_path,
                'error',
                f"Invalid filename format: '{filename}'. Expected format: {expected_prefix}-XXX-{spec_name}"
            ))
            return False

        prefix_part, number_part, name_part = filename_parts

        # Validate prefix matches
        if prefix_part != expected_prefix:
            self.errors.append(ValidationError(
                file_path,
                'error',
                f"Filename prefix '{prefix_part}' doesn't match expected '{expected_prefix}'"
            ))
            return False

        # Validate number part
        if not number_part.isdigit():
            self.errors.append(ValidationError(
                file_path,
                'error',
                f"Filename number part '{number_part}' must be numeric"
            ))
            return False

        # Validate descriptive name part matches spec name field
        if name_part != spec_name:
            self.errors.append(ValidationError(
                file_path,
                'warning',
                f"Filename descriptive part '{name_part}' doesn't match spec name field '{spec_name}'. Expected: {expected_prefix}-{number_part}-{spec_name}"
            ))
            return False

        if file_path.suffix.lower() == '.yaml':
            if spec_type not in ['TestCase', 'ScenarioCase', 'PreconditionCase']:
                self.errors.append(ValidationError(
                    file_path,
                    'error',
                    f"YAML file extension used for non-case spec type '{spec_type}'. Expected .md"
                ))
        elif file_path.suffix.lower() == '.yml':
            self.errors.append(ValidationError(
                file_path,
                'error',
                f"Invalid file extension '.yml'. Must use '.yaml' extension"
            ))
        elif file_path.suffix.lower() == '.md':
            if spec_type in ['TestCase', 'ScenarioCase', 'PreconditionCase']:
                self.errors.append(ValidationError(
                    file_path,
                    'error',
                    f"Markdown file extension used for case type '{spec_type}'. Expected .yaml"
                ))

        return True

    def validate_timestamp(self, timestamp: str, file_path: Path) -> bool:
        """Validate ISO 8601 timestamp format"""
        # Handle datetime objects parsed by YAML
        if isinstance(timestamp, datetime):
            timestamp_str = timestamp.strftime("%Y-%m-%dT%H:%M:%SZ")
            return True

        if not isinstance(timestamp, str):
            self.errors.append(ValidationError(
                file_path,
                'error',
                f"Invalid timestamp type: expected string, got {type(timestamp).__name__}"
            ))
            return False

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
        """Validate spec ID format using template-defined prefix"""
        type_info = self.spec_type_info.get(spec_type)

        if not type_info:
            self.errors.append(ValidationError(
                file_path,
                'warning',
                f"Unknown spec type: '{spec_type}' (no template found)"
            ))
            return False

        expected_prefix = type_info['prefix']
        pattern = f"^{expected_prefix}-[0-9]+$"

        if not re.match(pattern, spec_id):
            self.errors.append(ValidationError(
                file_path,
                'error',
                f"Invalid ID format: '{spec_id}'. Must match pattern '{expected_prefix}-XXX' for type '{spec_type}'"
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

    def check_duplicate_id(self, spec_id: str, file_path: Path) -> bool:
        """Check for duplicate spec IDs across files"""
        if spec_id in self.all_spec_ids:
            existing_file = self.all_spec_ids[spec_id]
            self.errors.append(ValidationError(
                file_path,
                'error',
                f"Duplicate spec ID '{spec_id}' found. Also exists in {existing_file}"
            ))
            return False

        self.all_spec_ids[spec_id] = file_path
        return True

    def validate_references(self, references: List, file_path: Path) -> bool:
        """Validate that referenced spec IDs exist"""
        if not self.check_refs or not references:
            return True

        for ref in references:
            ref_id = ref if isinstance(ref, str) else ref.get('id') if isinstance(ref, dict) else None
            if ref_id and ref_id not in self.all_spec_ids:
                self.errors.append(ValidationError(
                    file_path,
                    'warning',
                    f"Referenced spec ID '{ref_id}' not found in repository"
                ))

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
        if not path.endswith('.yaml'):
            self.errors.append(ValidationError(
                file_path,
                'error',
                f"Case path must end with .yaml: '{path}'"
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

            # Check required fields from template
            type_info = self.spec_type_info.get(spec_type)
            if type_info:
                required = type_info['required_fields']
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

                # Validate name field
                if 'name' in content:
                    self.validate_name_field(content['name'], content['type'], file_path)
                    self.check_duplicate_name(content['name'], content['type'], file_path)
                    self.validate_filename(file_path, content['id'], content['name'], content['type'])

                self.check_duplicate_id(content['id'], file_path)

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

            # Validate references
            if 'related' in content:
                self.validate_references(content['related'], file_path)

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

            # Check required fields from template
            type_info = self.spec_type_info.get(spec_type)
            if type_info:
                required = type_info['required_fields']
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

                # Validate name field
                if 'name' in frontmatter:
                    self.validate_name_field(frontmatter['name'], frontmatter['type'], file_path)
                    self.check_duplicate_name(frontmatter['name'], frontmatter['type'], file_path)
                    self.validate_filename(file_path, frontmatter['id'], frontmatter['name'], frontmatter['type'])

                self.check_duplicate_id(frontmatter['id'], file_path)

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

            # Validate references
            if 'related' in frontmatter:
                self.validate_references(frontmatter['related'], file_path)

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
        if file_path.suffix == '.yaml':
            return self.validate_yaml_case(file_path)
        elif file_path.suffix == '.yml':
            self.errors.append(ValidationError(
                file_path,
                'error',
                "Invalid file extension '.yml'. Must use '.yaml' extension"
            ))
            return False
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
        patterns = ['**/*.yaml', '**/*.md'] if recursive else ['*.yaml', '*.md']

        spec_files = []
        for pattern in patterns:
            for file_path in directory.glob(pattern):
                # Skip templates and non-spec files
                if 'templates' in str(file_path):
                    continue
                if 'README' in file_path.name:
                    continue

                # Only validate files in specs/ or plans/
                if 'specs/' not in str(file_path) and 'plans/' not in str(file_path):
                    continue

                spec_files.append(file_path)

        # First pass: collect all spec IDs (for cross-reference validation)
        if self.check_refs:
            for file_path in spec_files:
                try:
                    if file_path.suffix == '.yaml':
                        with open(file_path, 'r') as f:
                            content = yaml.safe_load(f)
                            if content and 'id' in content:
                                self.all_spec_ids[content['id']] = file_path
                    elif file_path.suffix == '.md':
                        with open(file_path, 'r') as f:
                            content = f.read()
                            yaml_match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
                            if yaml_match:
                                frontmatter = yaml.safe_load(yaml_match.group(1))
                                if frontmatter and 'id' in frontmatter:
                                    self.all_spec_ids[frontmatter['id']] = file_path
                except:
                    pass

            # Clear the IDs dict to re-populate during validation (for duplicate detection)
            self.all_spec_ids.clear()
            self.all_spec_names.clear()

        # Second pass: validate all files
        for file_path in spec_files:
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

    parser.add_argument(
        "--no-check-filenames",
        action="store_true",
        help="Skip filename validation"
    )

    parser.add_argument(
        "--check-refs",
        action="store_true",
        help="Enable cross-reference validation (checks if referenced spec IDs exist)"
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output with detailed validation information"
    )

    args = parser.parse_args()

    path = Path(args.path)
    if not path.exists():
        print(f"Error: Path not found: {path}", file=sys.stderr)
        sys.exit(2)

    # Find repo root (look for .specify or templates directory)
    repo_root = path if path.is_dir() else path.parent
    while repo_root.parent != repo_root:
        if (repo_root / '.specify').exists() or (repo_root / 'templates').exists():
            break
        repo_root = repo_root.parent

    validator = SpecValidator(
        repo_root,
        check_filenames=not args.no_check_filenames,
        check_refs=args.check_refs,
        verbose=args.verbose
    )

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