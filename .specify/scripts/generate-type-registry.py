#!/usr/bin/env python3
"""
Type Registry Generator
Scans template files and generates a registry of all spec types with their metadata
"""

import os
import re
import sys
import yaml
import argparse
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple

class TypeRegistryGenerator:
    """Generates type registry from template files"""

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        # Try multiple locations for templates
        possible_dirs = [
            repo_root / '.specify' / 'templates',
            repo_root / 'templates'
        ]
        self.template_dir = None
        for template_dir in possible_dirs:
            if template_dir.exists():
                self.template_dir = template_dir
                break
        self.types: Dict[str, Dict] = {}

    def extract_template_metadata(self, template_file: Path) -> Optional[Dict]:
        """Extract type metadata from a template file"""
        try:
            if template_file.suffix == '.yaml':
                with open(template_file, 'r') as f:
                    # Read first 50 lines to get metadata
                    lines = []
                    for i, line in enumerate(f):
                        if i >= 50:
                            break
                        lines.append(line)

                    content = ''.join(lines)

                    # Parse YAML to get fields
                    parsed = yaml.safe_load(content)
                    if not parsed:
                        return None

                    type_name = parsed.get('type')
                    if not type_name:
                        return None

                    return {
                        'type': type_name,
                        'prefix': parsed.get('id_prefix', ''),
                        'extension': parsed.get('file_extension', 'yaml'),
                        'guidelines': parsed.get('name_guidelines', ''),
                        'examples': parsed.get('name_examples', []),
                        'template': str(template_file.relative_to(self.repo_root))
                    }

            elif template_file.suffix == '.md':
                with open(template_file, 'r') as f:
                    content = f.read(2000)  # Read first 2000 chars

                # First try to extract metadata from HTML comment
                comment_match = re.search(r'<!--\s*Template Metadata.*?type:\s*([^\n]+)\s*id_prefix:\s*([^\n]+)\s*name_guidelines:\s*"([^"]+)"\s*name_examples:\s*\[(.*?)\]\s*file_extension:\s*([^\n]+)', content, re.DOTALL)

                if comment_match:
                    type_name = comment_match.group(1).strip()
                    prefix = comment_match.group(2).strip()
                    guidelines = comment_match.group(3).strip()
                    examples_str = comment_match.group(4).strip()
                    extension = comment_match.group(5).strip()

                    # Parse examples from string like: "example1", "example2"
                    examples = []
                    for match in re.finditer(r'"([^"]+)"', examples_str):
                        examples.append(match.group(1))

                    return {
                        'type': type_name,
                        'prefix': prefix,
                        'extension': extension,
                        'guidelines': guidelines,
                        'examples': examples,
                        'template': str(template_file.relative_to(self.repo_root))
                    }

                # Fallback: Try YAML frontmatter
                yaml_match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL | re.MULTILINE)
                if not yaml_match:
                    return None

                frontmatter = yaml.safe_load(yaml_match.group(1))
                if not frontmatter:
                    return None

                type_name = frontmatter.get('type')
                if not type_name:
                    return None

                # Try to extract from id field pattern
                prefix = ''
                spec_id = frontmatter.get('id', '')
                prefix_match = re.match(r'^([A-Z]+)-\[', spec_id)
                if prefix_match:
                    prefix = prefix_match.group(1)

                return {
                    'type': type_name,
                    'prefix': prefix,
                    'extension': 'md',
                    'guidelines': '',
                    'examples': [],
                    'template': str(template_file.relative_to(self.repo_root))
                }

        except Exception as e:
            print(f"Warning: Could not parse {template_file}: {e}", file=sys.stderr)
            return None

        return None

    def scan_templates(self):
        """Scan all template files and collect type information"""
        if not self.template_dir:
            print(f"Error: Template directory not found", file=sys.stderr)
            sys.exit(1)

        # Find all template files
        for pattern in ['spec-*.yaml', 'spec-*.md']:
            for template_file in self.template_dir.glob(pattern):
                metadata = self.extract_template_metadata(template_file)
                if metadata:
                    type_name = metadata['type']

                    # Check for duplicate types
                    if type_name in self.types:
                        print(f"Warning: Duplicate type '{type_name}' found in {template_file}", file=sys.stderr)
                        continue

                    # Check for duplicate prefixes
                    prefix = metadata['prefix']
                    for existing_type, existing_meta in self.types.items():
                        if existing_meta['prefix'] == prefix and prefix:
                            print(f"Error: Duplicate prefix '{prefix}' for types '{type_name}' and '{existing_type}'", file=sys.stderr)
                            sys.exit(1)

                    self.types[type_name] = metadata

    def generate_registry(self, existing_timestamp: Optional[str] = None) -> str:
        """Generate the type registry YAML content

        Args:
            existing_timestamp: Preserve existing timestamp if content hasn't changed
        """
        # Use existing timestamp or generate new one
        timestamp = existing_timestamp or datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

        # Header
        header = f"""# AUTO-GENERATED FILE - DO NOT EDIT
# Generated from templates in .specify/templates/
# Run: python .specify/scripts/generate-type-registry.py
# Last generated: {timestamp}

"""

        # Build registry
        registry = {'types': {}}

        # Sort types alphabetically for consistency
        for type_name in sorted(self.types.keys()):
            metadata = self.types[type_name]
            registry['types'][type_name] = {
                'prefix': metadata['prefix'],
                'extension': metadata['extension'],
                'guidelines': metadata['guidelines'],
                'examples': metadata['examples'],
                'template': metadata['template']
            }

        # Convert to YAML
        registry_yaml = yaml.dump(registry, default_flow_style=False, sort_keys=False, allow_unicode=True)

        return header + registry_yaml

    def extract_content_without_timestamp(self, content: str) -> str:
        """Extract registry content excluding the timestamp line"""
        lines = content.split('\n')
        filtered_lines = [line for line in lines if not line.startswith('# Last generated:')]
        return '\n'.join(filtered_lines)

    def extract_timestamp(self, content: str) -> Optional[str]:
        """Extract timestamp from registry content"""
        for line in content.split('\n'):
            if line.startswith('# Last generated:'):
                return line.replace('# Last generated:', '').strip()
        return None

    def write_registry(self, output_path: Path, force: bool = False) -> bool:
        """Write the registry to file only if content changed

        Args:
            output_path: Path to write registry file
            force: Force write even if content hasn't changed

        Returns:
            True if file was written, False if unchanged
        """
        # Read existing registry if it exists
        existing_content = None
        existing_timestamp = None

        if output_path.exists() and not force:
            with open(output_path, 'r') as f:
                existing_content = f.read()
            existing_timestamp = self.extract_timestamp(existing_content)

        # Generate new registry (with existing timestamp if content unchanged)
        new_content = self.generate_registry(existing_timestamp)

        # Compare content without timestamps
        if existing_content and not force:
            existing_core = self.extract_content_without_timestamp(existing_content)
            new_core = self.extract_content_without_timestamp(new_content)

            if existing_core == new_core:
                print(f"Type registry is up to date: {output_path}")
                print(f"  Found {len(self.types)} spec types (no changes)")
                return False

        # Content changed or force write - update timestamp
        new_content = self.generate_registry()  # Generate with new timestamp

        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w') as f:
            f.write(new_content)

        print(f"Generated type registry: {output_path}")
        print(f"  Found {len(self.types)} spec types")
        return True

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Generate type registry from template metadata",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "--check",
        action="store_true",
        help="Check if registry would change (exit 1 if changes needed)"
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help="Force regeneration even if content unchanged"
    )

    args = parser.parse_args()

    # Find repository root
    script_path = Path(__file__).resolve()
    repo_root = script_path.parent.parent.parent  # Go up from .specify/scripts/

    # Create generator
    generator = TypeRegistryGenerator(repo_root)

    # Scan templates
    generator.scan_templates()

    # Generate and write registry
    output_path = repo_root / '.specify' / 'schemas' / 'type-registry.yaml'

    if args.check:
        # Check mode: don't write, just check if changes would be made
        existing_content = None
        if output_path.exists():
            with open(output_path, 'r') as f:
                existing_content = f.read()
            existing_timestamp = generator.extract_timestamp(existing_content)
            new_content = generator.generate_registry(existing_timestamp)
            existing_core = generator.extract_content_without_timestamp(existing_content)
            new_core = generator.extract_content_without_timestamp(new_content)

            if existing_core != new_core:
                print("Type registry needs update")
                return 1
            else:
                print("Type registry is up to date")
                return 0
        else:
            print("Type registry does not exist")
            return 1

    # Normal mode: write registry
    changed = generator.write_registry(output_path, force=args.force)
    return 0

if __name__ == "__main__":
    sys.exit(main())