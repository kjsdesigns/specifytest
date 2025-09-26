# SpecifyTest

A Specification-Driven Development framework with simplified timestamp-based versioning for tracking specification changes and implementation staleness.

## Overview

SpecifyTest implements a comprehensive specification system that uses timestamps to automatically track changes and detect when implementations become outdated. The framework enforces Test-Driven Development (TDD) principles through a constitution-based governance model.

## Key Features

- **Timestamp-Only Versioning**: Simple ISO 8601 timestamps track when specifications change (no complex hashing)
- **Automatic Staleness Detection**: Compare timestamps to identify outdated implementations with age-based prioritization
- **14 Specification Types**: Comprehensive templates for workflows, pages, concepts, data, contracts, integrations, security, configuration, technology, events, and messages, plus 3 validation case types
- **Reusable Components**: DRY-compliant template components for common patterns (API contracts, retry policies, monitoring, performance)
- **Constitution-Based Governance**: Enforced principles and standards (currently v6.0.0)
- **Standalone Case Architecture**: Test cases, scenario cases, and precondition cases as independent artifacts
- **Simple Maintenance**: Just update timestamp on save - no special tools needed

## Project Structure

```
.specify/
├── memory/
│   └── constitution.md         # Governance and principles (v6.0.0)
├── scripts/
│   ├── check-staleness.sh      # Detect outdated implementations via timestamp comparison
│   ├── check-staleness.py      # Python version with detailed reporting
│   ├── validate-specs.py       # Validate spec compliance (NEW)
│   └── generate-test-stub.py   # Generate test stubs from cases
└── templates/
    ├── components/             # Reusable template components (DRY principle)
    │   ├── spec-header.md      # Common YAML frontmatter
    │   ├── spec-validation-cases.md
    │   ├── spec-uncertainties.md
    │   ├── spec-implementation-refs.md
    │   ├── spec-base-fields.yaml
    │   ├── spec-api-contract.yaml  # API endpoint patterns (NEW)
    │   ├── spec-retry-policy.md    # Retry & circuit breaker (NEW)
    │   ├── spec-monitoring.md      # Observability patterns (NEW)
    │   ├── spec-inline-contracts.yaml  # YAML schema patterns (NEW)
    │   ├── spec-performance.md     # Performance requirements (NEW)
    │   ├── TEMPLATE_STRUCTURE.md  # Section ordering guide (NEW)
    │   └── README.md
    ├── spec-test-case.yaml
    ├── spec-scenario-case.yaml
    ├── spec-precondition-case.yaml
    ├── spec-workflow.md
    ├── spec-page.md
    ├── spec-concept.md
    ├── spec-data.md
    ├── spec-contract.md         # Updated: CONTRACT-xxx ID format
    ├── spec-integration.md
    ├── spec-security.md
    ├── spec-config.md
    ├── spec-technology.md
    ├── spec-event.md            # NEW: Event specifications
    ├── spec-message.md          # NEW: Message specifications
    ├── plan-template.md
    └── tasks-template.md

.claude/
└── commands/
    ├── specify.md              # /specify command implementation
    └── constitution.md         # /constitution command

specs/                         # All specifications and cases
├── test-cases/                # Test case definitions (TC-xxx)
├── scenario-cases/            # End-to-end scenarios (SC-xxx)
├── precondition-cases/        # Reusable setup/teardown (PC-xxx)
└── [type directories]         # Modular specifications by type
plans/                         # Execution plans with Git SHA tracking
```

## Quick Start

### 1. Create a Test Case

```bash
# Create a new test case using the template
cp .specify/templates/spec-test-case.yaml specs/test-cases/TC-001.yaml
# Edit the file with your test details
# Set hash_timestamp to current UTC time (update on every save)
```

### 2. Validate Specifications

```bash
# Validate all specifications for compliance
./.specify/scripts/validate-specs.py /specs/

# Checks:
# - Required fields present
# - Valid timestamp format
# - Correct ID formats (TC-xxx, EVENT-xxx, etc.)
# - Status values
# - Template compliance
```

### 3. Check for Stale Implementations

```bash
# Scan entire repository for outdated implementations
./.specify/scripts/check-staleness.sh

# Or use Python version for detailed reports
./.specify/scripts/check-staleness.py

# Output shows staleness by priority based on timestamp comparison:
# CRITICAL (>30 days), HIGH (7-30 days), MEDIUM (1-7 days), LOW (<1 day)
```

### 4. Reference Cases in Implementations

```python
def test_user_login():
    """
    Implements: /specs/test-cases/TC-001.yaml
    Case Timestamp: 2024-01-15T10:30:00Z
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
8. **Implementation Timestamp References**
9. **Timestamp-Only Versioning** (NON-NEGOTIABLE)

## Timestamp-Based Change Detection

Every Case file includes:
- `hash_timestamp`: ISO 8601 timestamp updated on every save

Implementation files reference only the timestamp, enabling automatic detection of:
- Which implementations are outdated (Case timestamp > implementation timestamp)
- How long they've been outdated (simple date arithmetic)
- Priority for updates based on staleness age

The system is intentionally simple: just compare timestamps, no complex hashing needed.

For detailed guidance, see [TIMESTAMP_GUIDE.md](./TIMESTAMP_GUIDE.md).

## Specification Types

The framework supports 14 specification types:

### Core Specifications (11 types)
- **Workflow** (W-xxx): User journeys and business processes
- **Page** (P-xxx): UI pages and screens
- **Concept** (C-xxx): Business entities and domain logic
- **Data** (DATA-xxx): Data models and schemas
- **Contract** (CONTRACT-xxx): API contracts and interfaces
- **Integration** (INT-xxx): External system connections
- **Security** (SEC-xxx): Security policies and controls
- **Configuration** (CONFIG-xxx): System settings
- **Technology** (TECH-xxx): Technology stack decisions
- **Event** (EVENT-xxx): Async events and pub/sub patterns **[NEW]**
- **Message** (MESSAGE-xxx): Message queues and commands **[NEW]**

### Validation Specifications (3 types)
- **Test Case** (TC-xxx): Individual test scenarios
- **Scenario Case** (SC-xxx): End-to-end test flows organized into phases
- **Precondition Case** (PC-xxx): Reusable setup/teardown

See [SPEC_TYPE_GUIDE.md](./SPEC_TYPE_GUIDE.md) for detailed selection guidance.
See [SCENARIO_PHASE_GUIDE.md](./SCENARIO_PHASE_GUIDE.md) for phase organization patterns.

## Tools & Validation

### Validation Tool
```bash
# Validate all specs
./.specify/scripts/validate-specs.py /specs/

# Validate specific file
./.specify/scripts/validate-specs.py /specs/test-cases/TC-001.yaml

# JSON output for CI/CD
./.specify/scripts/validate-specs.py --json /specs/
```

### Staleness Detection
```bash
# Check for stale implementations
./.specify/scripts/check-staleness.sh
# or
./.specify/scripts/check-staleness.py --verbose
```

### Test Stub Generation
```bash
# Generate test stub from case
./.specify/scripts/generate-test-stub.py /specs/test-cases/TC-001.yaml pytest
```

## Commands

### For Claude Code Users

The project includes custom commands in `.claude/commands/`:

- `/specify [requirements]` - Create or update specifications from natural language
- `/constitution` - Update the project constitution

## Benefits

- **Dead Simple**: Just timestamps, no complex hashing or versioning
- **Temporal Awareness**: Know exactly when specs changed and staleness duration
- **Prioritized Updates**: Address oldest implementations first
- **Low Maintenance**: Update timestamp on save - that's it
- **CI/CD Ready**: Scripts return appropriate exit codes for automation
- **No Special Tools**: Any editor can update a timestamp field

## Contributing

1. Follow the constitution principles in `.specify/memory/constitution.md`
2. Use templates from `.specify/templates/` for all new artifacts
3. Run staleness detection before committing
4. Update implementation hash references when specs change

## License

[Add your license here]

## Author

Created with Specification-Driven Development principles and Claude Code assistance.