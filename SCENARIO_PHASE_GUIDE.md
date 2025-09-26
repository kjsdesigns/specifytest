# Scenario Phase Organization Guide

This guide explains how to organize scenario cases using the phase-based structure introduced in the Specify framework.

## Overview

Scenario cases now support organizing preconditions and test cases into **phases** - logical groupings that represent stages in an end-to-end test flow. Phases improve readability, maintainability, and provide clear execution tracking in test runner output.

## Why Use Phases?

**Without phases** (flat structure):
```yaml
preconditions:
  - /specs/precondition-cases/PC-001.yaml
  - /specs/precondition-cases/PC-002.yaml
  - /specs/precondition-cases/PC-003.yaml
test_cases:
  - /specs/test-cases/TC-001.yaml
  - /specs/test-cases/TC-002.yaml
  - /specs/test-cases/TC-003.yaml
  - /specs/test-cases/TC-004.yaml
  - /specs/test-cases/TC-005.yaml
```

**With phases** (organized structure):
```yaml
phases:
  - phase_id: setup
    phase_name: "Setup & Preparation"
    description: "Initialize environment and prepare test data"
    preconditions:
      - path: /specs/precondition-cases/PC-001.yaml
        description: "Database with test users"
      - path: /specs/precondition-cases/PC-002.yaml
        description: "Clean browser session"
    test_cases: []

  - phase_id: authentication
    phase_name: "User Authentication"
    description: "Test login and session management"
    preconditions:
      - path: /specs/precondition-cases/PC-003.yaml
        description: "Active user account"
    test_cases:
      - path: /specs/test-cases/TC-001.yaml
        description: "Login with valid credentials"
      - path: /specs/test-cases/TC-002.yaml
        description: "Login with invalid password"

  - phase_id: main_flow
    phase_name: "Main User Flow"
    description: "Execute primary business operations"
    preconditions: []
    test_cases:
      - path: /specs/test-cases/TC-003.yaml
        description: "Create new order"
      - path: /specs/test-cases/TC-004.yaml
        description: "Process payment"

  - phase_id: cleanup
    phase_name: "Cleanup"
    description: "Restore original state"
    preconditions: []
    test_cases:
      - path: /specs/test-cases/TC-005.yaml
        description: "Verify cleanup completed"
```

## Phase Structure

Each phase contains:

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `phase_id` | Yes | string | Unique identifier (kebab-case) |
| `phase_name` | Yes | string | Human-readable name shown in output |
| `description` | Yes | string | What this phase accomplishes |
| `preconditions` | Yes | array | Setup requirements for this phase |
| `test_cases` | Yes | array | Tests executed in this phase |

### Preconditions and Test Cases Format

Within each phase, preconditions and test cases use this structure:

```yaml
preconditions:
  - path: /specs/precondition-cases/PC-001.yaml
    description: "What this precondition provides"

test_cases:
  - path: /specs/test-cases/TC-001.yaml
    description: "What this test validates"
```

The `description` field helps readers understand the purpose without opening each file.

## Common Phase Patterns

### 1. Setup → Execute → Verify → Cleanup

Most common pattern for end-to-end scenarios:

```yaml
phases:
  - phase_id: setup
    phase_name: "Setup & Preparation"
    description: "Initialize environment and prepare test data"
    preconditions: [...]
    test_cases: []

  - phase_id: execute
    phase_name: "Execute Main Flow"
    description: "Perform the primary business operation"
    preconditions: []
    test_cases: [...]

  - phase_id: verify
    phase_name: "Verification"
    description: "Verify expected outcomes and side effects"
    preconditions: []
    test_cases: [...]

  - phase_id: cleanup
    phase_name: "Cleanup"
    description: "Restore original state"
    preconditions: []
    test_cases: [...]
```

### 2. Multi-Step Sequential Flow

For scenarios with distinct sequential steps:

```yaml
phases:
  - phase_id: setup
    phase_name: "Setup"
    description: "Prepare environment"
    preconditions: [...]
    test_cases: []

  - phase_id: step_1
    phase_name: "Step 1: User Registration"
    description: "Create new user account"
    preconditions: []
    test_cases: [...]

  - phase_id: step_2
    phase_name: "Step 2: Email Verification"
    description: "Verify email address"
    preconditions: []
    test_cases: [...]

  - phase_id: step_3
    phase_name: "Step 3: Profile Completion"
    description: "Complete user profile"
    preconditions: []
    test_cases: [...]

  - phase_id: cleanup
    phase_name: "Cleanup"
    description: "Remove test data"
    preconditions: []
    test_cases: []
```

### 3. Authentication Flow

Specialized pattern for auth scenarios:

```yaml
phases:
  - phase_id: setup
    phase_name: "Setup"
    description: "Prepare test users and clean sessions"
    preconditions: [...]
    test_cases: []

  - phase_id: login
    phase_name: "User Login"
    description: "Test login functionality"
    preconditions: []
    test_cases: [...]

  - phase_id: session_management
    phase_name: "Session Management"
    description: "Verify session handling"
    preconditions: [...]
    test_cases: [...]

  - phase_id: logout
    phase_name: "User Logout"
    description: "Test logout and session cleanup"
    preconditions: []
    test_cases: [...]

  - phase_id: cleanup
    phase_name: "Cleanup"
    description: "Remove test data"
    preconditions: []
    test_cases: []
```

See `.specify/templates/components/spec-scenario-phases.yaml` for more patterns including e-commerce purchase flows and data migration scenarios.

## Phase Execution Configuration

Control how phases execute with `phase_execution`:

### Sequential (Default)

```yaml
phase_execution:
  mode: sequential
  continue_on_failure: false
  phase_timeout: 300
```

Each phase runs after the previous completes. Stops on first failure.

### Continue on Failure

```yaml
phase_execution:
  mode: sequential
  continue_on_failure: true
  phase_timeout: 300
```

Runs all phases even if some fail. Useful for collecting all failures.

### Parallel Phases

```yaml
phase_execution:
  mode: parallel_phases
  continue_on_failure: false
  phase_timeout: 300
```

Run multiple phases concurrently when safe (independent phases only).

### Custom Dependencies

```yaml
phase_execution:
  mode: custom
  continue_on_failure: false
  phase_timeout: 300
  phase_dependencies:
    setup: []
    phase_1: [setup]
    phase_2: [setup]
    phase_3: [phase_1, phase_2]
    cleanup: [phase_3]
```

Explicit control over execution order. Phases with same dependencies can run in parallel.

## Phase Output Example

When a test runner processes phased scenarios, output shows clear progress:

```
Scenario: Complete User Registration (SC-001)
═══════════════════════════════════════════════════

Phase 1/5: Setup & Preparation
  ✓ PC-001: Database with clean state (0.5s)
  ✓ PC-002: Email service mock (0.2s)

Phase 2/5: User Registration
  ✓ TC-001: Register with valid email (1.2s)
  ✓ TC-002: Reject duplicate email (0.8s)

Phase 3/5: Email Verification
  ✓ TC-003: Send verification email (0.5s)
  ✓ TC-004: Click verification link (0.9s)

Phase 4/5: Profile Setup
  ✓ TC-005: Complete profile information (1.1s)

Phase 5/5: Cleanup
  ✓ TC-006: Remove test user (0.3s)

═══════════════════════════════════════════════════
Scenario passed: 5/5 phases completed (5.5s total)
```

## Best Practices

### 1. Use Descriptive Phase Names

**Good:**
- "User Authentication"
- "Create Order"
- "Process Payment"
- "Verify Email Sent"

**Avoid:**
- "Phase 1"
- "Test"
- "Check"
- "Do stuff"

### 2. Keep Phases Focused

Each phase should represent a single concern or stage:

```yaml
# Good - focused phases
- phase_id: create_order
  phase_name: "Create Order"
  description: "User creates a new order"

- phase_id: process_payment
  phase_name: "Process Payment"
  description: "Payment gateway processes order"

# Avoid - mixing concerns
- phase_id: create_and_pay
  phase_name: "Create Order and Pay"
  description: "User creates order and pays"
```

### 3. Setup Phase Typically Has No Test Cases

```yaml
- phase_id: setup
  phase_name: "Setup & Preparation"
  description: "Initialize environment"
  preconditions:
    - path: /specs/precondition-cases/PC-001.yaml
      description: "Database setup"
  test_cases: []  # Setup phase prepares, doesn't test
```

### 4. Include Cleanup Phase

Always clean up after tests to ensure isolation:

```yaml
- phase_id: cleanup
  phase_name: "Cleanup & Teardown"
  description: "Restore original state"
  preconditions: []
  test_cases:
    - path: /specs/test-cases/TC-099.yaml
      description: "Verify cleanup completed"
```

### 5. Aim for 3-7 Phases

Not including setup/cleanup:
- **Too few** (1-2): Consider if you need a scenario or just test cases
- **Just right** (3-7): Clear stages, manageable complexity
- **Too many** (8+): Consider splitting into multiple scenarios

### 6. Add Descriptions to References

Help readers understand without opening files:

```yaml
preconditions:
  - path: /specs/precondition-cases/PC-001.yaml
    description: "Database with test users and products"  # Context!

test_cases:
  - path: /specs/test-cases/TC-001.yaml
    description: "User searches for product by name"  # Purpose!
```

### 7. Group Related Tests Together

```yaml
# Good - related tests in same phase
- phase_id: form_validation
  phase_name: "Form Validation"
  description: "Test all form validation rules"
  test_cases:
    - path: /specs/test-cases/TC-010.yaml
      description: "Email format validation"
    - path: /specs/test-cases/TC-011.yaml
      description: "Password strength validation"
    - path: /specs/test-cases/TC-012.yaml
      description: "Required fields validation"

# Avoid - unrelated tests mixed together
- phase_id: misc_tests
  phase_name: "Miscellaneous"
  test_cases:
    - path: /specs/test-cases/TC-010.yaml
    - path: /specs/test-cases/TC-050.yaml
    - path: /specs/test-cases/TC-099.yaml
```

## Migration from Flat Structure

If you have existing scenario cases with flat `preconditions` and `test_cases` arrays, migrate to phases:

**Before:**
```yaml
id: SC-001
name: user-registration
type: ScenarioCase
hash_timestamp: 2024-01-15T10:00:00Z

preconditions:
  - /specs/precondition-cases/PC-001.yaml
  - /specs/precondition-cases/PC-002.yaml

test_cases:
  - /specs/test-cases/TC-001.yaml
  - /specs/test-cases/TC-002.yaml
  - /specs/test-cases/TC-003.yaml
```

**After:**
```yaml
id: SC-001
name: user-registration
type: ScenarioCase
hash_timestamp: 2024-01-15T10:30:00Z  # Updated!

phases:
  - phase_id: setup
    phase_name: "Setup"
    description: "Prepare test environment"
    preconditions:
      - path: /specs/precondition-cases/PC-001.yaml
        description: "Database with clean state"
      - path: /specs/precondition-cases/PC-002.yaml
        description: "Email service mock"
    test_cases: []

  - phase_id: registration
    phase_name: "User Registration"
    description: "Test registration flow"
    preconditions: []
    test_cases:
      - path: /specs/test-cases/TC-001.yaml
        description: "Register with valid data"
      - path: /specs/test-cases/TC-002.yaml
        description: "Reject invalid email"
      - path: /specs/test-cases/TC-003.yaml
        description: "Prevent duplicate email"

phase_execution:
  mode: sequential
  continue_on_failure: false
```

## Validation

The validation script checks phase structure:

```bash
./.specify/scripts/validate-specs.py /specs/scenario-cases/
```

Validates:
- Required phase fields present (phase_id, phase_name, description, preconditions, test_cases)
- `phase_id` uniqueness within scenario
- Preconditions and test_cases are arrays
- Path references follow correct format
- File paths point to correct directories

## See Also

- **Template**: `.specify/templates/spec-scenario-case.yaml` - Base template with phase structure
- **Patterns**: `.specify/templates/components/spec-scenario-phases.yaml` - Common phase patterns
- **Constitution**: `.specify/memory/constitution.md` - Principle IV defines phase requirements
- **Guide**: `SPEC_TYPE_GUIDE.md` - When to use Scenario Cases vs Test Cases