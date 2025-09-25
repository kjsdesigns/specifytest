---
id: TECH-[XXX]
type: TechnologyDecision
name: [Technology Name]
status: draft
related: [Related spec IDs]
---
# {name}

## Goals
- [Primary objective of this technology decision]
- [Secondary objectives]
- [Expected outcomes]

## Context
[Brief description of why this technology decision is needed]

## Architecture
**Component**: [Where this fits in the system]
**Integration Points**: [How it connects with other parts]
**Data Flow**: [How data moves through this component]

## Standards
- **[Standard 1]**: [Description]
- **[Standard 2]**: [Description]
- **[Standard 3]**: [Description]

## Requirements
- **Performance**: [Performance requirements]
- **Scalability**: [Scalability requirements]
- **Security**: [Security requirements]
- **Reliability**: [Reliability requirements]

## Constraints
- [Technical constraints]
- [Business constraints]
- [Resource constraints]

## Alternatives Considered
- **[Alternative 1]**: [Why not chosen]
- **[Alternative 2]**: [Why not chosen]

## Migration Strategy
[If replacing existing technology, describe the migration approach]

## Success Metrics
- [Metric 1 and target]
- [Metric 2 and target]
- [Metric 3 and target]

## Risks and Mitigations
- **Risk**: [Description] → **Mitigation**: [Strategy]
- **Risk**: [Description] → **Mitigation**: [Strategy]

## Integration Contract
configuration:
  environment_variables:
    - name: [ENV_VAR_NAME]
      type: string
      required: [true|false]
      default: [value]
      description: [What it controls]

  dependencies:
    - package: [package_name]
      version: [version_constraint]
      purpose: [Why needed]

  services:
    - name: [service_name]
      type: [internal|external]
      endpoint: [URL or path]
      authentication: [method]
      retry_policy:
        max_attempts: [number]
        backoff: [strategy]

  performance:
    - operation: [operation_name]
      p50: < [N]ms
      p95: < [N]ms
      p99: < [N]ms
      throughput: > [N] ops/sec

## Validation Cases

### Test Cases
References to standalone test cases by file path that validate this spec:
- /test-cases/TC-001.yaml: [Brief description of what this test validates]
- /test-cases/TC-002.yaml: [Brief description of what this test validates]
- /test-cases/TC-003.yaml: [Brief description of what this test validates]

### Scenario Cases
References to end-to-end scenarios by file path involving this spec:
- /scenario-cases/SC-001.yaml: [Brief description of the scenario]
- /scenario-cases/SC-002.yaml: [Brief description of the scenario]

### Notes
- Test cases are defined in `/test-cases/` directory
- Scenario cases are defined in `/scenario-cases/` directory
- Precondition cases referenced by tests are in `/precondition-cases/` directory

## Implementation References
preconditions:
  location: .specify/preconditions/
  shared: [List of reusable precondition IDs]
config_examples:
  location: config/examples/[tech_name]/
integration_tests:
  location: tests/integration/[tech_name]/

## Uncertainties
[List any areas of uncertainty, ambiguity, or questions that need to be resolved]

## References
- [Link to documentation]
- [Link to vendor site]
- [Link to internal docs]
