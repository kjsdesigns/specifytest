#!/usr/bin/env python3
"""
Test Generation Assistant
Generates test stubs based on Test Case YAML files
Supports multiple test frameworks
"""

import argparse
import sys
import yaml
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any, Optional

# Template mappings for different test frameworks
TEST_TEMPLATES = {
    "pytest": """def test_{test_name}():
    \"\"\"
    Implements: {case_path}
    Case Timestamp: {timestamp}
    Purpose: {purpose}
    \"\"\"
    # Preconditions
{preconditions}

    # Test Steps
{steps}

    # Validations
{validations}

    # Teardown
{teardown}
""",

    "jest": """describe('{test_id}', () => {{
    test('{test_name}', async () => {{
        /*
         * Implements: {case_path}
         * Case Timestamp: {timestamp}
         * Purpose: {purpose}
         */

        // Preconditions
{preconditions}

        // Test Steps
{steps}

        // Validations
{validations}

        // Teardown
{teardown}
    }});
}});
""",

    "go": """func Test{test_name_camel}(t *testing.T) {{
    // Implements: {case_path}
    // Case Timestamp: {timestamp}
    // Purpose: {purpose}

    // Preconditions
{preconditions}

    // Test Steps
{steps}

    // Validations
{validations}

    // Teardown
{teardown}
}}
""",

    "java": """@Test
public void test{test_name_camel}() {{
    // Implements: {case_path}
    // Case Timestamp: {timestamp}
    // Purpose: {purpose}

    // Preconditions
{preconditions}

    // Test Steps
{steps}

    // Validations
{validations}

    // Teardown
{teardown}
}}
""",
}

def to_snake_case(text: str) -> str:
    """Convert kebab-case to snake_case."""
    return text.replace("-", "_")

def to_camel_case(text: str) -> str:
    """Convert kebab-case to CamelCase."""
    parts = text.split("-")
    return "".join(word.capitalize() for word in parts)

def load_test_case(file_path: Path) -> Dict[str, Any]:
    """Load and validate a test case YAML file."""
    if not file_path.exists():
        raise FileNotFoundError(f"Test case not found: {file_path}")

    with open(file_path, 'r') as f:
        case = yaml.safe_load(f)

    # Validate required fields
    required = ['id', 'name', 'hash_timestamp', 'purpose']
    missing = [field for field in required if field not in case]
    if missing:
        raise ValueError(f"Missing required fields: {', '.join(missing)}")

    return case

def format_preconditions(preconditions: List[str], framework: str) -> str:
    """Format preconditions for the test stub."""
    if not preconditions:
        return "    # No preconditions"

    comment_char = "//" if framework in ["jest", "go", "java"] else "#"
    indent = "        " if framework == "jest" else "    "

    lines = []
    for pc in preconditions:
        lines.append(f"{indent}{comment_char} Load: {pc}")

    return "\n".join(lines)

def format_steps(steps: List[Dict], framework: str) -> str:
    """Format test steps for the stub."""
    if not steps:
        return "    # No steps defined"

    comment_char = "//" if framework in ["jest", "go", "java"] else "#"
    indent = "        " if framework == "jest" else "    "

    lines = []
    for step in steps:
        step_num = step.get('step', '?')
        action = step.get('action', 'No action defined')
        expected = step.get('expected', 'No expectation defined')

        lines.append(f"{indent}{comment_char} Step {step_num}: {action}")
        lines.append(f"{indent}{comment_char} Expected: {expected}")
        lines.append(f"{indent}{comment_char} TODO: Implement step {step_num}")
        lines.append("")

    return "\n".join(lines).rstrip()

def format_validations(validations: List[str], framework: str) -> str:
    """Format validations for the stub."""
    if not validations:
        return "    # No validations defined"

    comment_char = "//" if framework in ["jest", "go", "java"] else "#"
    indent = "        " if framework == "jest" else "    "

    lines = []
    for validation in validations:
        lines.append(f"{indent}{comment_char} Validate: {validation}")
        lines.append(f"{indent}{comment_char} TODO: Add assertion")

    return "\n".join(lines)

def format_teardown(teardown: List[str], framework: str) -> str:
    """Format teardown steps for the stub."""
    if not teardown:
        return "    # No teardown needed"

    comment_char = "//" if framework in ["jest", "go", "java"] else "#"
    indent = "        " if framework == "jest" else "    "

    lines = []
    for step in teardown:
        lines.append(f"{indent}{comment_char} Teardown: {step}")

    return "\n".join(lines)

def generate_stub(case_file: Path, framework: str) -> str:
    """Generate a test stub from a test case file."""
    case = load_test_case(case_file)

    template = TEST_TEMPLATES.get(framework)
    if not template:
        raise ValueError(f"Unsupported framework: {framework}")

    # Prepare variables
    test_name = to_snake_case(case['name'])
    test_name_camel = to_camel_case(case['name'])

    # Format the stub
    stub = template.format(
        test_id=case['id'],
        test_name=test_name,
        test_name_camel=test_name_camel,
        case_path=f"/specs/{case_file.parent.name}/{case_file.name}",
        timestamp=case['hash_timestamp'],
        purpose=case['purpose'],
        preconditions=format_preconditions(case.get('preconditions', []), framework),
        steps=format_steps(case.get('steps', []), framework),
        validations=format_validations(case.get('validations', []), framework),
        teardown=format_teardown(case.get('teardown', []), framework)
    )

    return stub

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate test stubs from Test Case YAML files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Supported Frameworks:
  pytest   - Python with pytest
  jest     - JavaScript with Jest
  go       - Go with testing package
  java     - Java with JUnit

Examples:
  %(prog)s /test-cases/TC-001.yaml pytest
  %(prog)s /test-cases/TC-002.yaml jest --output tests/auth.test.js
  %(prog)s --batch /test-cases/*.yaml pytest --output tests/
        """
    )

    parser.add_argument(
        "case_file",
        help="Path to test case YAML file"
    )

    parser.add_argument(
        "framework",
        choices=["pytest", "jest", "go", "java"],
        help="Test framework to generate for"
    )

    parser.add_argument(
        "--output",
        "-o",
        help="Output file path (default: stdout)"
    )

    parser.add_argument(
        "--batch",
        action="store_true",
        help="Process multiple files (case_file becomes pattern)"
    )

    args = parser.parse_args()

    try:
        if args.batch:
            # Batch processing
            from glob import glob
            files = glob(args.case_file)
            if not files:
                print(f"No files matching pattern: {args.case_file}", file=sys.stderr)
                sys.exit(1)

            for file_path in files:
                stub = generate_stub(Path(file_path), args.framework)
                if args.output:
                    # Generate output filename
                    case_name = Path(file_path).stem
                    ext = {
                        "pytest": ".py",
                        "jest": ".test.js",
                        "go": "_test.go",
                        "java": "Test.java"
                    }[args.framework]

                    output_file = Path(args.output) / f"test_{case_name.lower()}{ext}"
                    output_file.parent.mkdir(parents=True, exist_ok=True)
                    output_file.write_text(stub)
                    print(f"Generated: {output_file}")
                else:
                    print(f"\n# Generated from {file_path}")
                    print(stub)
        else:
            # Single file processing
            stub = generate_stub(Path(args.case_file), args.framework)

            if args.output:
                output_file = Path(args.output)
                output_file.parent.mkdir(parents=True, exist_ok=True)
                output_file.write_text(stub)
                print(f"Test stub generated: {output_file}")
            else:
                print(stub)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()