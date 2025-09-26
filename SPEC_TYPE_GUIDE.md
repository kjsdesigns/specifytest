# Specification Type Selection Guide

This guide helps you choose the correct specification type for your requirements. The Specify framework supports 14 distinct specification types: 11 for system design and architecture, plus 3 specialized types for validation and testing.

## Quick Decision Tree

```
Is it about...
├── User interactions or processes? → **Workflow (W-xxx)**
├── UI/UX elements or screens? → **Page (P-xxx)**
├── Business logic or domain rules? → **Concept (C-xxx)**
├── Data structures or storage? → **Data (DATA-xxx)**
├── API endpoints or interfaces? → **Contract (CONTRACT-xxx)**
├── External system connections? → **Integration (INT-xxx)**
├── Security policies or auth? → **Security (SEC-xxx)**
├── System settings or env vars? → **Configuration (CONFIG-xxx)**
├── Tech stack or architecture? → **Technology (TECH-xxx)**
├── Async events or pub/sub? → **Event (EVENT-xxx)**
├── Message queues or commands? → **Message (MESSAGE-xxx)**
└── Validation and testing?
    ├── Individual test scenario? → **Test Case (TC-xxx)**
    ├── End-to-end journey? → **Scenario Case (SC-xxx)**
    └── Setup/teardown procedure? → **Precondition Case (PC-xxx)**
```

## Detailed Specification Types

### 1. Workflow Specifications (W-xxx)
**Purpose**: Define user journeys, business processes, and multi-step operations

**Use when you have**:
- User stories or use cases
- Multi-step processes
- State transitions
- User journeys through the system
- Business process automation

**Examples**:
- `W-001`: User registration workflow
- `W-002`: Order checkout process
- `W-003`: Document approval workflow

**Template**: `.specify/templates/spec-workflow.md`

---

### 2. Page Specifications (P-xxx)
**Purpose**: Define UI pages, screens, and visual components

**Use when you have**:
- UI mockups or wireframes
- Screen layouts
- Component hierarchies
- Visual design requirements
- Responsive design needs

**Examples**:
- `P-001`: Login page
- `P-002`: Dashboard screen
- `P-003`: User profile view

**Template**: `.specify/templates/spec-page.md`

---

### 3. Concept Specifications (C-xxx)
**Purpose**: Define business entities, domain logic, and core concepts

**Use when you have**:
- Business rules
- Domain entities
- Core algorithms
- Business logic validation
- Invariants and constraints

**Examples**:
- `C-001`: User account concept
- `C-002`: Shopping cart logic
- `C-003`: Pricing calculation rules

**Template**: `.specify/templates/spec-concept.md`

---

### 4. Data Specifications (DATA-xxx)
**Purpose**: Define data models, schemas, and storage requirements

**Use when you have**:
- Database schemas
- Data relationships
- Storage requirements
- Data validation rules
- Migration needs

**Examples**:
- `DATA-001`: User data model
- `DATA-002`: Product catalog schema
- `DATA-003`: Analytics data structure

**Template**: `.specify/templates/spec-data.md`

---

### 5. Contract Specifications (CONTRACT-xxx)
**Purpose**: Define API contracts, interfaces, and service boundaries

**Use when you have**:
- REST API endpoints
- GraphQL schemas
- RPC interfaces
- WebSocket protocols
- Service contracts

**Examples**:
- `CONTRACT-001`: User authentication API
- `CONTRACT-002`: Payment service interface
- `CONTRACT-003`: Notification webhook contract

**Template**: `.specify/templates/spec-contract.md`

---

### 6. Integration Specifications (INT-xxx)
**Purpose**: Define connections to external systems and third-party services

**Use when you have**:
- Third-party API integrations
- External service dependencies
- Message queue connections
- Database connections
- File system integrations

**Examples**:
- `INT-001`: Stripe payment integration
- `INT-002`: AWS S3 file storage
- `INT-003`: SendGrid email service

**Template**: `.specify/templates/spec-integration.md`

---

### 7. Security Specifications (SEC-xxx)
**Purpose**: Define security policies, authentication, and authorization

**Use when you have**:
- Authentication requirements
- Authorization rules
- Security policies
- Encryption needs
- Compliance requirements

**Examples**:
- `SEC-001`: OAuth2 authentication
- `SEC-002`: Role-based access control
- `SEC-003`: Data encryption policy

**Template**: `.specify/templates/spec-security.md`

---

### 8. Configuration Specifications (CONFIG-xxx)
**Purpose**: Define system configuration, environment variables, and settings

**Use when you have**:
- Environment variables
- Feature flags
- System settings
- Deployment configurations
- Runtime parameters

**Examples**:
- `CONFIG-001`: Application environment config
- `CONFIG-002`: Feature toggle settings
- `CONFIG-003`: Database connection config

**Template**: `.specify/templates/spec-config.md`

---

### 9. Technology Specifications (TECH-xxx)
**Purpose**: Define technology stack, architecture decisions, and technical constraints

**Use when you have**:
- Technology stack decisions
- Architecture patterns
- Performance requirements
- Scalability needs
- Infrastructure requirements

**Examples**:
- `TECH-001`: Microservices architecture
- `TECH-002`: Frontend framework selection
- `TECH-003`: Database technology choice

**Template**: `.specify/templates/spec-technology.md`

---

### 10. Event Specifications (EVENT-xxx)
**Purpose**: Define asynchronous events for pub/sub, messaging, and event-driven architectures

**Use when you have**:
- Domain events to publish
- System events to broadcast
- Event-driven architecture patterns
- Async notifications
- Event sourcing requirements

**Examples**:
- `EVENT-001`: Order created event
- `EVENT-002`: User updated event
- `EVENT-003`: Payment processed event

**Template**: `.specify/templates/spec-event.md`

---

### 11. Message Specifications (MESSAGE-xxx)
**Purpose**: Define message formats for queues, commands, queries, and RPC

**Use when you have**:
- Message queue patterns
- Command/Query messages
- Request/Response protocols
- Message-based integrations
- Async communication needs

**Examples**:
- `MESSAGE-001`: Process order command
- `MESSAGE-002`: Fetch user query
- `MESSAGE-003`: Email notification message

**Template**: `.specify/templates/spec-message.md`

---

## Validation Specifications (Cases)

In addition to the 11 specification types above, the framework includes 3 special types of specifications focused on validation and testing. These are also specifications, stored in `/specs/` subdirectories:

### Test Case Specifications (TC-xxx)
**Purpose**: Define individual test scenarios for validating functionality

**Location**: `/specs/test-cases/`

**Use when you have**:
- Specific functionality to validate
- User acceptance criteria
- Edge cases to test
- Error conditions to verify
- Performance benchmarks to meet

**Examples**:
- `TC-001`: Login with valid credentials
- `TC-002`: Form validation errors
- `TC-003`: API response under load

**Template**: `.specify/templates/spec-test-case.yaml`

### Scenario Case Specifications (SC-xxx)
**Purpose**: Define end-to-end scenarios that orchestrate multiple test cases organized into phases

**Location**: `/specs/scenario-cases/`

**Use when you have**:
- Complex user journeys to validate
- Multi-step workflows to test
- Integration scenarios
- System-wide behaviors to verify

**Key Feature - Phase Organization**:
Scenario cases organize preconditions and test cases into phases - logical groupings that represent stages in an end-to-end flow. Each phase has a clear name, description, and set of tests, making complex scenarios easier to understand and maintain.

**Example Phase Structure**:
```yaml
phases:
  - phase_id: setup
    phase_name: "Setup & Preparation"
    description: "Initialize environment"
    preconditions: [...]
    test_cases: []

  - phase_id: main_flow
    phase_name: "Execute Purchase"
    description: "User completes purchase"
    preconditions: []
    test_cases: [...]

  - phase_id: verification
    phase_name: "Verify Results"
    description: "Check order created"
    preconditions: []
    test_cases: [...]

  - phase_id: cleanup
    phase_name: "Cleanup"
    description: "Remove test data"
    preconditions: []
    test_cases: [...]
```

**Examples**:
- `SC-001`: Complete purchase flow
- `SC-002`: User onboarding journey
- `SC-003`: Data migration process

**Template**: `.specify/templates/spec-scenario-case.yaml`

**See Also**: `SCENARIO_PHASE_GUIDE.md` for detailed phase organization patterns

### Precondition Case Specifications (PC-xxx)
**Purpose**: Define reusable setup and teardown procedures

**Location**: `/specs/precondition-cases/`

**Use when you have**:
- Test data to prepare
- System state to configure
- External dependencies to mock
- Cleanup procedures to define

**Examples**:
- `PC-001`: Database with test users
- `PC-002`: Clean browser session
- `PC-003`: Mock API responses

**Template**: `.specify/templates/spec-precondition-case.yaml`

---

## Specification Relationships

Specifications often reference each other. Here's how they typically relate:

```
Workflow (W) ──uses──> Page (P)
     │                    │
     └──implements──>  Concept (C)
                          │
Contract (CONTRACT) <──exposes──┘
     │                    │
     └──stores──>     Data (DATA)
                          │
Integration (INT) ──connects──┘
     │
Security (SEC) ──protects──> All
     │
Configuration (CONFIG) ──configures──> All
     │
Technology (TECH) ──enables──> All
```

## Common Patterns

### E-commerce Application
- `W-001`: Shopping workflow
- `P-001`: Product listing page
- `P-002`: Cart page
- `C-001`: Product concept
- `C-002`: Cart logic
- `DATA-001`: Product database
- `CONTRACT-001`: Product API
- `INT-001`: Payment gateway
- `SEC-001`: User authentication

### SaaS Dashboard
- `W-001`: Onboarding workflow
- `P-001`: Dashboard page
- `C-001`: Account management
- `DATA-001`: User data model
- `CONTRACT-001`: Analytics API
- `SEC-001`: Multi-tenant security
- `CONFIG-001`: Feature flags

### Mobile App
- `W-001`: User journey
- `P-001`: Home screen
- `C-001`: Core features
- `DATA-001`: Local storage
- `CONTRACT-001`: Backend API
- `INT-001`: Push notifications
- `SEC-001`: Biometric auth

## Best Practices

1. **Start with Workflows**: Define user journeys first
2. **One Concern Per Spec**: Don't mix different types
3. **Use Cross-References**: Link related specs
4. **Keep Specs Focused**: Small, manageable units
5. **Version Everything**: Use timestamps consistently
6. **Test Each Spec**: Create Test Cases for validation

## Need Help?

If you're unsure which type to use:
1. Start with the decision tree above
2. Look at the examples for each type
3. Check if similar specs already exist
4. When in doubt, choose the most specific type
5. Remember: you can always refactor later

## Command Usage

To create specifications of any type:

```bash
/specify "Your requirements description here"
```

The command will automatically:
- Analyze your requirements
- Choose appropriate spec types
- Create the necessary specifications
- Generate Test Cases for validation
- Update cross-references