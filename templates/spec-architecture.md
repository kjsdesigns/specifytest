<!--
Template Metadata (used by type registry generator)
type: Architecture
id_prefix: ARCH
name_guidelines: "Architectural pattern or style"
name_examples: ["microservices", "event_driven", "three_tier", "hexagonal", "layered"]
file_extension: md

Validation rules: see .specify/schemas/template-schema.json
-->
<!-- See components/spec-header.md for header format -->
---
id: ARCH-[XXX]
name: [descriptive_snake_case_name]
type: Architecture
status: draft
related: []
hash_timestamp: [ISO_8601_TIMESTAMP]  # Updated on every save
---

# {name}

## Overview
[High-level description of this architectural component or pattern and its role in the system]

## Purpose
[Why this architecture exists and what problems it solves]

## Components
### Component 1: [Name]
**Purpose**: [What this component does]
**Responsibilities**:
- [Responsibility 1]
- [Responsibility 2]

### Component 2: [Name]
**Purpose**: [What this component does]
**Responsibilities**:
- [Responsibility 1]
- [Responsibility 2]

## Layers
- **[Layer 1]**: [Description and purpose]
  - Components: [List components in this layer]
  - Dependencies: [What this layer depends on]
- **[Layer 2]**: [Description and purpose]
  - Components: [List components in this layer]
  - Dependencies: [What this layer depends on]

## Data Flow
[Describe how data flows through the architecture]

```
[Diagram or description of data flow]
Source -> Component A -> Component B -> Destination
```

## Integration Points
- **[Integration 1]**: [Description and protocol]
- **[Integration 2]**: [Description and protocol]

## Patterns
- **[Pattern 1]**: [Why and how it's used]
- **[Pattern 2]**: [Why and how it's used]

## Constraints
- [Architectural constraint 1]
- [Architectural constraint 2]
- [Architectural constraint 3]

## Quality Attributes
### Performance
[Performance requirements and considerations]

### Scalability
[Scalability approach and limitations]

### Security
[Security considerations and mechanisms]

### Reliability
[Reliability requirements and approaches]

### Maintainability
[Maintainability considerations]

## Technology Stack
- **[Technology Category]**: [Technology name and version]
  - Purpose: [Why this technology is used]
  - Constraints: [Any constraints or limitations]

## Deployment
[How this architecture is deployed and configured]

## Monitoring and Observability
[How this architecture is monitored and observed]

## Trade-offs
- **[Trade-off 1]**: [What was chosen and why]
- **[Trade-off 2]**: [What was chosen and why]

## Alternatives Considered
### Alternative 1: [Name]
**Description**: [What this alternative was]
**Rejected Because**: [Why it wasn't chosen]

### Alternative 2: [Name]
**Description**: [What this alternative was]
**Rejected Because**: [Why it wasn't chosen]

## Migration Strategy
[If applicable, how to migrate to/from this architecture]

<!-- See components/spec-validation-cases.md for validation case format -->
## Validation Cases

### Test Cases
- [ ] [TC-XXX: Test description](/specs/test-cases/TC-XXX.yaml)

### Scenario Cases
- [ ] [SC-XXX: Scenario description](/specs/scenario-cases/SC-XXX.yaml)

<!-- See components/spec-implementation-refs.md for implementation reference format -->
## Implementation References

- Main implementation: `[PATH_TO_IMPLEMENTATION]`
- Configuration: `[PATH_TO_CONFIG]`
- Infrastructure as Code: `[PATH_TO_IAC]`
- Tests: `[PATH_TO_TESTS]`

<!-- See components/spec-uncertainties.md for uncertainties format -->
## Uncertainties

- [ ] [DESCRIBE_UNCERTAINTY]

## Glossary
- **[TERM]**: [DEFINITION]