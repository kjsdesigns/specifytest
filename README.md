# SpecifyTest

A Specification-Driven Development framework with hash-based versioning and datetime stamps for tracking specification changes and implementation staleness.

## Overview

SpecifyTest implements a comprehensive specification system that uses content hashing and timestamps to automatically track changes and detect when implementations become outdated. The framework enforces Test-Driven Development (TDD) principles through a constitution-based governance model.

## Key Features

- **Hash-Based Versioning**: Automatic SHA-256 content hashing for all test cases, scenario cases, and precondition cases
- **Temporal Tracking**: ISO 8601 timestamps track when specifications change
- **Staleness Detection**: Automatically identify outdated implementations with age-based prioritization
- **Modular Specifications**: Type-specific templates for workflows, pages, concepts, data, contracts, security, and more
- **Constitution-Based Governance**: Enforced principles and standards (currently v5.1.0)
- **Standalone Case Architecture**: Test cases, scenario cases, and precondition cases as independent artifacts

## Project Structure

```
.specify/
├── memory/
│   └── constitution.md         # Governance and principles (v5.1.0)
├── scripts/
│   ├── compute-case-hash.sh    # Generate hashes for Case files
│   ├── check-staleness.sh      # Detect outdated implementations
│   └── bash/                   # Additional utility scripts
└── templates/
    ├── test-case-template.yaml
    ├── scenario-case-template.yaml
    ├── precondition-case-template.yaml
    ├── plan-template.md
    ├── tasks-template.md
    └── spec-*.md               # Type-specific spec templates

.claude/
└── commands/
    ├── specify.md              # /specify command implementation
    └── constitution.md         # /constitution command

test-cases/                     # Test case definitions (TC-xxx)
scenario-cases/                 # End-to-end scenarios (SC-xxx)
precondition-cases/            # Reusable setup/teardown (PC-xxx)
specs/                         # Modular specifications by type
plans/                         # Execution plans with Git SHA tracking
```

## Quick Start

### 1. Create a Test Case

```bash
# Create a new test case using the template
cp .specify/templates/test-case-template.yaml test-cases/TC-001.yaml
# Edit the file with your test details
# Generate hash and timestamp
./.specify/scripts/compute-case-hash.sh test-cases/TC-001.yaml
```

### 2. Check for Stale Implementations

```bash
# Scan entire repository for outdated implementations
./.specify/scripts/check-staleness.sh

# Output shows staleness by priority:
# CRITICAL (>30 days), HIGH (7-30 days), MEDIUM (1-7 days), LOW (<1 day)
```

### 3. Reference Cases in Implementations

```python
def test_user_login():
    """
    Implements: /test-cases/TC-001.yaml
    Spec Hash: sha256:a1b2c3d4e5f6...
    Hash Timestamp: 2024-01-15T10:30:00Z
    """
    # Your test implementation
```

## Constitution Principles

The project follows 9 core principles defined in `.specify/memory/constitution.md`:

1. **Test-Driven Development** (NON-NEGOTIABLE)
2. **Standalone Case Architecture**
3. **Independent Identifier Standards**
4. **Complete Case Documentation**
5. **Specs Reference Cases by Path**
6. **Mandatory Template Usage** (NON-NEGOTIABLE)
7. **Plans Track Git State and Tasks Reference Paths**
8. **Implementation Hash References**
9. **Stateless Hash-Based Versioning with Timestamps** (NON-NEGOTIABLE)

## Hash-Based Change Detection

Every Case file includes:
- `content_hash`: SHA-256 hash of canonical YAML content
- `hash_timestamp`: ISO 8601 timestamp of when hash was generated

Implementation files reference these hashes, enabling automatic detection of:
- Which implementations are outdated
- How long they've been outdated
- Priority for updates based on staleness age

## Commands

### For Claude Code Users

The project includes custom commands in `.claude/commands/`:

- `/specify [requirements]` - Create or update specifications from natural language
- `/constitution` - Update the project constitution

## Benefits

- **No Manual Versioning**: Hashes automatically track changes
- **Temporal Awareness**: Know when specs changed and staleness duration
- **Prioritized Updates**: Address oldest implementations first
- **Complete Traceability**: Bidirectional tracking between specs and implementations
- **CI/CD Ready**: Scripts return appropriate exit codes for automation

## Contributing

1. Follow the constitution principles in `.specify/memory/constitution.md`
2. Use templates from `.specify/templates/` for all new artifacts
3. Run staleness detection before committing
4. Update implementation hash references when specs change

## License

[Add your license here]

## Author

Created with Specification-Driven Development principles and Claude Code assistance.