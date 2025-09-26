# How Specs and Validations Work

This document explains the complete architecture of the Specify framework's specification and validation system.

## Table of Contents
1. [Core Concepts](#core-concepts)
2. [Constitution Governance](#constitution-governance)
3. [Templates, Specs, Plans, and Tasks](#templates-specs-plans-and-tasks)
4. [Validation Architecture](#validation-architecture)
5. [All Specification Types](#all-specification-types)
6. [Template Components](#template-components)
7. [Type Selection Logic](#type-selection-logic)

---

## Core Concepts

### Specifications ARE Validations

**Critical Understanding**: Test Cases, Scenario Cases, and Precondition Cases ARE specifications, not separate from specs. They are specialized types of specifications focused on validation and testing.

The framework supports **14 specification types**:
- **11 Core Types**: Workflow, Page, Concept, Data, Contract, Integration, Security, Configuration, Technology, Event, Message
- **3 Validation Types**: Test Case, Scenario Case, Precondition Case

All live under `/specs/` in dedicated directories.

### Timestamp-Based Versioning

Every specification includes a `hash_timestamp` field (ISO 8601 format) that MUST be updated whenever the file is modified and saved. This simple timestamp comparison drives change detection:

```
Case timestamp > implementation timestamp = stale implementation
```

No complex hashing, no manual version numbers - just timestamps.

---

## Constitution Governance

The constitution (`.specify/memory/constitution.md`) enforces 9 core principles:

### I. Test-Driven Development (NON-NEGOTIABLE)
- Define Cases FIRST in `/specs/test-cases/`, `/specs/scenario-cases/`, `/specs/precondition-cases/`
- Then create plans capturing Git SHA
- Then create tasks referencing spec paths
- Implementation follows only after Cases are defined
- Red-Green-Refactor: Cases → failing tests → passing implementation

### II. Standalone Case Architecture
- All Cases are independent specification artifacts
- No inline Cases within other specs
- Each has unique ID and `hash_timestamp`
- References use absolute file paths: `/specs/test-cases/TC-001.yaml`

### III. Independent Identifier Standards
- **Specs**: Type prefix + number (W-001, DATA-015, EVENT-001)
- **Test Cases**: TC-001, TC-002, TC-003
- **Scenario Cases**: SC-001, SC-002, SC-003
- **Precondition Cases**: PC-001, PC-002, PC-003
- IDs stable; timestamp tracks changes

### IV. Complete Case Documentation
**Test Cases** require: id, name, hash_timestamp, purpose, preconditions, steps, validations, teardown, inputs, expected_outputs, environment, pass_criteria

**Scenario Cases** require: id, name, hash_timestamp, purpose, **phases** (phase_id, phase_name, description, preconditions array, test_cases array), phase_execution, timeout, cache_strategy

**Precondition Cases** require: id, name, hash_timestamp, purpose, setup_steps, context_provided, validation_checks, teardown_procedures, compatibility, cache_strategy, resources_touched

### V. Specs Reference Cases by Path
- Each spec has `validation_cases` section
- Lists Test Case paths: `/specs/test-cases/TC-001.yaml`
- Lists Scenario Case paths: `/specs/scenario-cases/SC-001.yaml`
- Cases reference Precondition Cases by path
- Preconditions are standalone (no outbound references)

### VI. Mandatory Template Usage (NON-NEGOTIABLE)
- All artifacts MUST use templates from `.specify/templates/`
- Templates define required fields and structure
- Deviation constitutes constitution violation

### VII. Plans Track Git State
- Plans live under `/plans/`
- Capture `git_commit_sha` at creation
- List all Cases by path
- Tasks reference specs and Cases by path

### VIII. Implementation Timestamp References
- Test implementations embed Case timestamps as comments
- When Case timestamp > implementation timestamp = stale
- Bidirectional traceability via timestamp comparison

### IX. Timestamp-Only Versioning (NON-NEGOTIABLE)
- No content hashing, no manual versions
- Just ISO 8601 timestamps updated on save
- Change detection by simple date comparison

---

## Templates, Specs, Plans, and Tasks

### Workflow Overview

```
1. Requirements → 2. Specs + Cases → 3. Plan → 4. Tasks → 5. Implementation
                        ↓
                   Templates
```

### 1. Templates (`.specify/templates/`)

**Purpose**: Define structure and required fields for all artifacts

**Spec Templates** (11 types):
- `spec-workflow.md` - User journeys (W-xxx)
- `spec-page.md` - UI pages (P-xxx)
- `spec-concept.md` - Business logic (C-xxx)
- `spec-data.md` - Data models (DATA-xxx)
- `spec-contract.md` - API contracts (CONTRACT-xxx)
- `spec-integration.md` - External systems (INT-xxx)
- `spec-security.md` - Security policies (SEC-xxx)
- `spec-config.md` - Configuration (CONFIG-xxx)
- `spec-technology.md` - Tech stack (TECH-xxx)
- `spec-event.md` - Async events (EVENT-xxx)
- `spec-message.md` - Message queues (MESSAGE-xxx)

**Validation Templates** (3 types):
- `spec-test-case.yaml` - Individual tests (TC-xxx)
- `spec-scenario-case.yaml` - End-to-end flows (SC-xxx)
- `spec-precondition-case.yaml` - Setup/teardown (PC-xxx)

**Plan & Task Templates**:
- `plan-template.md` - Execution plans with Git SHA
- `tasks-template.md` - Task lists with spec references

### 2. Specifications (`/specs/`)

**Structure**:
```
/specs/
├── workflows/              # W-xxx specs
├── pages/                  # P-xxx specs
├── concepts/               # C-xxx specs
├── data/                   # DATA-xxx specs
├── contracts/              # CONTRACT-xxx specs
├── integrations/           # INT-xxx specs
├── security/               # SEC-xxx specs
├── configuration/          # CONFIG-xxx specs
├── technology/             # TECH-xxx specs
├── events/                 # EVENT-xxx specs
├── messages/               # MESSAGE-xxx specs
├── test-cases/             # TC-xxx.yaml
├── scenario-cases/         # SC-xxx.yaml
└── precondition-cases/     # PC-xxx.yaml
```

**Each spec includes**:
- YAML frontmatter with id, name, type, hash_timestamp
- Requirements and design decisions
- `validation_cases` section listing TC and SC paths
- Implementation references section

**Example spec validation_cases**:
```markdown
## Validation Cases

### Test Cases
- /specs/test-cases/TC-001.yaml: Login with valid credentials
- /specs/test-cases/TC-002.yaml: Login with invalid password

### Scenario Cases
- /specs/scenario-cases/SC-001.yaml: Complete authentication flow
```

### 3. Plans (`/plans/`)

**Purpose**: Capture Git baseline and list Cases to implement

**Structure**:
```
/plans/plan-001/
├── plan.md      # Git SHA, plan_created timestamp, Cases list
└── tasks.md     # Task breakdown with spec paths
```

**plan.md includes**:
```markdown
---
git_commit_sha: abc123def456...
plan_created: 2024-01-15T12:00:00Z
---

## Cases to Develop
- /specs/test-cases/TC-001.yaml: Login with valid credentials
- /specs/test-cases/TC-002.yaml: Login with invalid password
- /specs/scenario-cases/SC-001.yaml: Complete auth flow
```

### 4. Tasks (`/plans/*/tasks.md`)

**Purpose**: Break down work with spec and Case references

**Example**:
```markdown
## Task 001: Implement authentication tests
- Validates Spec: /specs/workflows/W-001/spec.md
- Implements Cases:
  - /specs/test-cases/TC-001.yaml (timestamp: 2024-01-15T10:30:00Z)
  - /specs/test-cases/TC-002.yaml (timestamp: 2024-01-15T10:31:00Z)
- Uses Preconditions:
  - /specs/precondition-cases/PC-001.yaml
- File: tests/test_auth.py
```

### 5. Implementation Files

**Include timestamp references**:
```python
def test_login_valid_credentials():
    """
    Implements: /specs/test-cases/TC-001.yaml
    Case Timestamp: 2024-01-15T10:30:00Z
    """
    # Test implementation
```

---

## Validation Architecture

### Three Types of Validation Specs

#### 1. Test Cases (TC-xxx)
**File**: `/specs/test-cases/TC-001.yaml`

**Purpose**: Individual test scenarios validating specific functionality

**Structure**:
```yaml
id: TC-001
name: login-valid-credentials
type: TestCase
hash_timestamp: 2024-01-15T10:30:00Z

purpose: Verify user can login with valid email and password

preconditions:
  - /specs/precondition-cases/PC-001.yaml  # Database with test users
  - /specs/precondition-cases/PC-002.yaml  # Clean browser session

steps:
  - Navigate to login page
  - Enter valid email
  - Enter valid password
  - Click login button

validations:
  - User is redirected to dashboard
  - Session cookie is set
  - Welcome message displays user name

expected_outputs:
  status_code: 200
  redirect_url: "/dashboard"

pass_criteria:
  - All validations pass
  - Response time < 2 seconds
```

**When to use**: Single, focused test scenario

#### 2. Scenario Cases (SC-xxx)
**File**: `/specs/scenario-cases/SC-001.yaml`

**Purpose**: End-to-end flows orchestrating multiple test cases

**Key Feature**: **Phase-based organization** - groups preconditions and test cases into logical stages

**Structure**:
```yaml
id: SC-001
name: complete-authentication-flow
type: ScenarioCase
hash_timestamp: 2024-01-15T11:00:00Z

purpose: Validate entire authentication journey from registration to logout

phases:
  - phase_id: setup
    phase_name: "Setup & Preparation"
    description: "Initialize environment and prepare test data"
    preconditions:
      - path: /specs/precondition-cases/PC-001.yaml
        description: "Database with clean state"
      - path: /specs/precondition-cases/PC-002.yaml
        description: "Email service mock"
    test_cases: []

  - phase_id: registration
    phase_name: "User Registration"
    description: "Test account creation"
    preconditions: []
    test_cases:
      - path: /specs/test-cases/TC-003.yaml
        description: "Register with valid email"
      - path: /specs/test-cases/TC-004.yaml
        description: "Reject duplicate email"

  - phase_id: authentication
    phase_name: "Login & Session"
    description: "Test login and session management"
    preconditions:
      - path: /specs/precondition-cases/PC-003.yaml
        description: "Verified user account"
    test_cases:
      - path: /specs/test-cases/TC-001.yaml
        description: "Login with valid credentials"
      - path: /specs/test-cases/TC-002.yaml
        description: "Reject invalid password"

  - phase_id: cleanup
    phase_name: "Cleanup"
    description: "Remove test data"
    preconditions: []
    test_cases:
      - path: /specs/test-cases/TC-099.yaml
        description: "Verify cleanup completed"

phase_execution:
  mode: sequential
  continue_on_failure: false
  phase_timeout: 300

timeout: 1800
cache_strategy: none
```

**Phase Output Example**:
```
Scenario: Complete Authentication Flow (SC-001)
═══════════════════════════════════════════════════

Phase 1/4: Setup & Preparation
  ✓ PC-001: Database with clean state (0.5s)
  ✓ PC-002: Email service mock (0.2s)

Phase 2/4: User Registration
  ✓ TC-003: Register with valid email (1.2s)
  ✓ TC-004: Reject duplicate email (0.8s)

Phase 3/4: Login & Session
  ✓ TC-001: Login with valid credentials (1.1s)
  ✓ TC-002: Reject invalid password (0.9s)

Phase 4/4: Cleanup
  ✓ TC-099: Verify cleanup completed (0.3s)

═══════════════════════════════════════════════════
Scenario passed: 4/4 phases completed (5.0s total)
```

**When to use**: Complex user journeys, multi-step workflows, integration testing

#### 3. Precondition Cases (PC-xxx)
**File**: `/specs/precondition-cases/PC-001.yaml`

**Purpose**: Reusable setup and teardown procedures

**Structure**:
```yaml
id: PC-001
name: database-with-test-users
type: PreconditionCase
hash_timestamp: 2024-01-15T09:00:00Z

purpose: Setup database with test user accounts for authentication tests

setup_steps:
  - Connect to test database
  - Clear existing test users
  - Insert user fixtures (user1@test.com, user2@test.com)
  - Verify users created successfully

context_provided:
  - Test users with known credentials
  - Clean database state
  - User IDs available in test context

validation_checks:
  - Database connection successful
  - Exactly 2 test users exist
  - Users have valid password hashes

teardown_procedures:
  - Delete test users by email pattern
  - Verify cleanup successful
  - Close database connection

compatibility:
  - Works with PostgreSQL 12+
  - Thread-safe for parallel tests
  - Can be cached per test session

cache_strategy: session
resources_touched:
  - users table
  - Test database connection
```

**When to use**: Reusable setup needed by multiple tests

### Reference Flow

```
Spec (W-001)
    │
    ├─ references → Scenario Case (SC-001)
    │                    │
    │                    ├─ Phase 1: Setup
    │                    │    ├─ uses → Precondition (PC-001)
    │                    │    └─ uses → Precondition (PC-002)
    │                    │
    │                    ├─ Phase 2: Main Flow
    │                    │    ├─ runs → Test Case (TC-001)
    │                    │    └─ runs → Test Case (TC-002)
    │                    │
    │                    └─ Phase 3: Cleanup
    │                         └─ runs → Test Case (TC-099)
    │
    └─ references → Test Case (TC-003)
                         │
                         └─ uses → Precondition (PC-001)
```

---

## All Specification Types

### Core Specifications (11 Types)

#### 1. Workflow (W-xxx) - `spec-workflow.md`
**User journeys, business processes, multi-step operations**

Example: `W-001` - User registration workflow

Contains:
- Actor/role definitions
- Step-by-step flow
- Alternative paths
- Error handling
- State transitions

#### 2. Page (P-xxx) - `spec-page.md`
**UI pages, screens, visual components**

Example: `P-001` - Login page

Contains:
- Layout structure
- Component hierarchy
- Visual design requirements
- Responsive behavior
- Accessibility requirements

#### 3. Concept (C-xxx) - `spec-concept.md`
**Business entities, domain logic, core algorithms**

Example: `C-001` - User account concept

Contains:
- Business rules
- Invariants
- Constraints
- State management
- Validation logic

#### 4. Data (DATA-xxx) - `spec-data.md`
**Data models, schemas, storage requirements**

Example: `DATA-001` - User data model

Contains:
- Schema definition
- Relationships
- Indexes
- Constraints
- Migration notes

#### 5. Contract (CONTRACT-xxx) - `spec-contract.md`
**API contracts, interfaces, service boundaries**

Example: `CONTRACT-001` - User authentication API

Contains:
- Endpoints
- Request/response schemas
- Headers
- Status codes
- Error responses
- Authentication requirements

#### 6. Integration (INT-xxx) - `spec-integration.md`
**External systems, third-party services**

Example: `INT-001` - Stripe payment integration

Contains:
- External service details
- Authentication method
- API endpoints used
- Data mapping
- Error handling
- Retry policies

#### 7. Security (SEC-xxx) - `spec-security.md`
**Security policies, authentication, authorization**

Example: `SEC-001` - OAuth2 authentication

Contains:
- Authentication mechanism
- Authorization rules
- Token management
- Security constraints
- Compliance requirements

#### 8. Configuration (CONFIG-xxx) - `spec-config.md`
**System settings, environment variables, feature flags**

Example: `CONFIG-001` - Application environment config

Contains:
- Configuration variables
- Default values
- Environment-specific overrides
- Validation rules
- Dependencies

#### 9. Technology (TECH-xxx) - `spec-technology.md`
**Tech stack, architecture decisions, technical constraints**

Example: `TECH-001` - Microservices architecture

Contains:
- Technology choices
- Architecture patterns
- Performance requirements
- Scalability considerations
- Trade-offs and rationale

#### 10. Event (EVENT-xxx) - `spec-event.md`
**Asynchronous events for pub/sub, event-driven architectures**

Example: `EVENT-001` - Order created event

Contains:
- Event name and type
- Payload schema
- Publishers
- Subscribers
- Delivery guarantees
- Ordering requirements

#### 11. Message (MESSAGE-xxx) - `spec-message.md`
**Message formats for queues, commands, queries, RPC**

Example: `MESSAGE-001` - Process order command

Contains:
- Message type (command/query/event)
- Payload structure
- Routing information
- Processing requirements
- Response format

### Validation Specifications (3 Types)

#### 12. Test Case (TC-xxx) - `spec-test-case.yaml`
**Individual test scenarios**

See [Validation Architecture](#validation-architecture) above

#### 13. Scenario Case (SC-xxx) - `spec-scenario-case.yaml`
**End-to-end flows with phase organization**

See [Validation Architecture](#validation-architecture) above

#### 14. Precondition Case (PC-xxx) - `spec-precondition-case.yaml`
**Reusable setup/teardown**

See [Validation Architecture](#validation-architecture) above

---

## Template Components

Reusable components in `.specify/templates/components/` for DRY principles:

### Documentation Components

#### `spec-header.md`
Common YAML frontmatter structure for all markdown specs

```yaml
---
id: [ID]
name: [kebab-case-name]
type: [SpecType]
status: draft
related: []
hash_timestamp: [ISO_8601_TIMESTAMP]
---
```

#### `spec-validation-cases.md`
Standard section for listing validation references

```markdown
## Validation Cases

### Test Cases
- /specs/test-cases/TC-001.yaml: [Description]

### Scenario Cases
- /specs/scenario-cases/SC-001.yaml: [Description]
```

#### `spec-implementation-refs.md`
Section for tracking implementation files

```markdown
## Implementation References

### Source Files
- `src/auth/login.py`: Login implementation (timestamp: 2024-01-15T10:30:00Z)

### Test Files
- `tests/test_login.py`: Login tests (timestamp: 2024-01-15T10:30:00Z)
```

#### `spec-uncertainties.md`
Template for documenting unknowns and assumptions

```markdown
## Uncertainties & Assumptions

### Known Unknowns
- [Question that needs answering]

### Assumptions
- [Assumption being made]

### Risks
- [Potential risk]
```

#### `TEMPLATE_STRUCTURE.md`
Defines standard section ordering for all templates

### YAML Components

#### `spec-base-fields.yaml`
Common fields for YAML case files

```yaml
id: [ID]
name: [name]
type: [Type]
status: draft
related: []
hash_timestamp: [ISO_8601_TIMESTAMP]
```

#### `spec-api-contract.yaml`
Reusable API endpoint patterns

```yaml
endpoints:
  - path: /api/users
    method: POST
    request_schema: {}
    response_schema: {}
    status_codes:
      - 201: Created
      - 400: Validation error
```

#### `spec-inline-contracts.yaml`
YAML schema patterns for inline contracts

```yaml
schema:
  type: object
  required: [field1, field2]
  properties:
    field1:
      type: string
    field2:
      type: integer
```

#### `spec-scenario-phases.yaml`
Phase organization patterns for scenario cases

Includes patterns:
- Setup → Execute → Verify → Cleanup
- Multi-step sequential
- Authentication flow
- E-commerce purchase
- Data migration/ETL

### Operational Components

#### `spec-retry-policy.md`
Retry and circuit breaker patterns

```markdown
## Retry Policy
- Max attempts: 3
- Backoff: Exponential
- Timeout: 30s per attempt

## Circuit Breaker
- Failure threshold: 50%
- Reset timeout: 60s
```

#### `spec-monitoring.md`
Observability patterns

```markdown
## Metrics
- Request count
- Error rate
- Latency (p50, p95, p99)

## Logs
- Error logs with stack traces
- Audit logs for sensitive operations

## Alerts
- Error rate > 5%: Page on-call
```

#### `spec-performance.md`
Performance requirement patterns

```markdown
## Performance Requirements
- Response time: p95 < 500ms
- Throughput: 1000 req/s
- Concurrent users: 10,000

## Load Testing
- Ramp up: 0 to 1000 users over 5 minutes
- Sustained load: 30 minutes
```

---

## Type Selection Logic

### Decision Tree

```
Is it about...
├── User interactions or processes? → Workflow (W-xxx)
├── UI/UX elements or screens? → Page (P-xxx)
├── Business logic or domain rules? → Concept (C-xxx)
├── Data structures or storage? → Data (DATA-xxx)
├── API endpoints or interfaces? → Contract (CONTRACT-xxx)
├── External system connections? → Integration (INT-xxx)
├── Security policies or auth? → Security (SEC-xxx)
├── System settings or env vars? → Configuration (CONFIG-xxx)
├── Tech stack or architecture? → Technology (TECH-xxx)
├── Async events or pub/sub? → Event (EVENT-xxx)
├── Message queues or commands? → Message (MESSAGE-xxx)
└── Validation and testing?
    ├── Individual test scenario? → Test Case (TC-xxx)
    ├── End-to-end journey? → Scenario Case (SC-xxx)
    └── Setup/teardown procedure? → Precondition Case (PC-xxx)
```

### Selection Rules

#### Use **Workflow** when:
- Describing multi-step user journeys
- Defining business processes
- Mapping user stories to system behavior
- State transitions are important

#### Use **Page** when:
- Designing UI layouts
- Specifying component hierarchies
- Defining visual requirements
- Describing responsive behavior

#### Use **Concept** when:
- Defining business entities
- Documenting domain logic
- Establishing invariants
- Core algorithms

#### Use **Data** when:
- Designing database schemas
- Defining data relationships
- Specifying storage requirements
- Planning migrations

#### Use **Contract** when:
- Defining REST API endpoints
- Specifying GraphQL schemas
- Documenting RPC interfaces
- Defining service boundaries

#### Use **Integration** when:
- Connecting to third-party services
- Defining external dependencies
- Specifying API clients
- Managing external system interactions

#### Use **Security** when:
- Defining authentication mechanisms
- Specifying authorization rules
- Documenting security policies
- Compliance requirements

#### Use **Configuration** when:
- Defining environment variables
- Specifying feature flags
- System settings and parameters
- Deployment configurations

#### Use **Technology** when:
- Documenting tech stack choices
- Architecture decisions
- Performance requirements
- Infrastructure specifications

#### Use **Event** when:
- Defining domain events
- Pub/sub patterns
- Event-driven architectures
- Async notifications

#### Use **Message** when:
- Defining message queue formats
- Command/query patterns
- Request/response protocols
- Message-based communication

#### Use **Test Case** when:
- Single focused test
- Specific functionality validation
- Edge case testing
- Performance benchmarks

#### Use **Scenario Case** when:
- End-to-end user journey
- Multi-step workflow validation
- Integration testing
- Complex business flow testing

#### Use **Precondition Case** when:
- Reusable test setup
- Common teardown procedures
- Shared test fixtures
- Environment preparation

### Common Patterns

**E-commerce Application**:
- `W-001`: Shopping workflow
- `P-001`: Product listing page
- `C-001`: Shopping cart logic
- `DATA-001`: Product database
- `CONTRACT-001`: Product API
- `INT-001`: Payment gateway
- `SEC-001`: User authentication
- `TC-001`: Add to cart test
- `SC-001`: Complete purchase flow
- `PC-001`: Product catalog fixture

**SaaS Dashboard**:
- `W-001`: Onboarding workflow
- `P-001`: Dashboard page
- `C-001`: Account management
- `DATA-001`: User data model
- `CONTRACT-001`: Analytics API
- `CONFIG-001`: Feature flags
- `TC-001`: Dashboard loads test
- `SC-001`: Onboarding journey
- `PC-001`: Test account setup

**Event-Driven Microservices**:
- `W-001`: Order processing workflow
- `EVENT-001`: OrderCreated event
- `MESSAGE-001`: ProcessOrder command
- `CONTRACT-001`: Order service API
- `INT-001`: Payment service
- `DATA-001`: Order data model
- `TECH-001`: Event sourcing architecture
- `SC-001`: End-to-end order flow
- `TC-001`: Event publishing test
- `PC-001`: Event store setup

---

## Commands

### `/specify [requirements]`

Creates specifications and validation cases from natural language requirements.

**Process**:
1. Analyze requirements text
2. Determine spec types needed (uses type selection logic)
3. Create spec files using templates
4. Generate Test Cases, Scenario Cases, Precondition Cases
5. Set timestamps on all artifacts
6. Update validation_cases sections with paths
7. Report all created files

**Example**:
```
/specify "User authentication with email/password"
```

Creates:
- `/specs/workflows/W-001/spec.md` - Auth workflow
- `/specs/pages/P-001/spec.md` - Login page
- `/specs/concepts/C-001/spec.md` - User concept
- `/specs/security/SEC-001/spec.md` - Auth policy
- `/specs/test-cases/TC-001.yaml` - Login with valid credentials
- `/specs/test-cases/TC-002.yaml` - Login with invalid password
- `/specs/scenario-cases/SC-001.yaml` - Complete auth flow
- `/specs/precondition-cases/PC-001.yaml` - Test user database

### `/constitution`

Updates the constitution and syncs dependent templates.

**Process**:
1. Load constitution from `.specify/memory/constitution.md`
2. Collect values for placeholders
3. Update content with changes
4. Sync dependent templates if affected
5. Generate sync impact report
6. Save updated constitution

---

## Summary

The Specify framework uses:

- **14 specification types** (11 core + 3 validation)
- **Timestamp-based versioning** for simple change detection
- **Standalone Case architecture** for modularity
- **Phase-based Scenario organization** for complex flows
- **Mandatory templates** enforced by constitution
- **File path references** for navigation
- **Git SHA baselines** in plans
- **Constitution governance** with 9 core principles

All specifications and validations are first-class artifacts with timestamps, enabling automatic staleness detection and maintaining temporal alignment between specs and implementations.