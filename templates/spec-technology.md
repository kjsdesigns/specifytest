<!--
Template Metadata (used by type registry generator)
type: Technology
id_prefix: TECH
name_guidelines: "Technology or tool"
name_examples: ["react_frontend", "postgres_db", "redis_cache", "docker_containers"]
file_extension: md

Validation rules: see .specify/schemas/template-schema.json
-->
<!-- See components/spec-header.md for header format -->
---
id: TECH-[XXX]
name: [descriptive_snake_case_name]
type: Technology
status: draft
related: []
hash_timestamp: [ISO_8601_TIMESTAMP]  # Updated on every save
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

<!-- See components/spec-validation-cases.md for validation case format -->
## Validation Cases

### Test Cases
- [ ] [TC-XXX: Test description](/specs/test-cases/TC-XXX.yaml)

### Scenario Cases
- [ ] [SC-XXX: Scenario description](/specs/scenario-cases/SC-XXX.yaml)

<!-- See components/spec-implementation-refs.md for implementation reference format -->
## Implementation References

- Main implementation: `[path/to/implementation]`
- Tests: `[path/to/tests]`
- Configuration: `[path/to/config]`

<!-- See components/spec-uncertainties.md for uncertainties format -->
## Uncertainties

- [ ] [Describe uncertainty or question]

## References
- [Link to documentation]
- [Link to vendor site]
- [Link to internal docs]
