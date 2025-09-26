<!-- See components/spec-header.md for header format -->
---
id: W-[XXX]
name: [descriptive-kebab-case-name]
type: Workflow
status: draft
related: []
hash_timestamp: [ISO_8601_TIMESTAMP]  # Updated on every save
---

# {name}

## Overview
[Brief description of the end-to-end workflow]

## Actors
- **[Actor 1]**: [Role and responsibilities]
- **[Actor 2]**: [Role and responsibilities]

## Triggers
- **[Trigger 1]**: [What initiates this workflow]
- **[Trigger 2]**: [Alternative trigger]

## Preconditions
- [Condition that must be true before workflow can start]
- [Another precondition]

## Process Flow

### Step 1: [Step Name]
**Actor**: [Who performs this]
**Action**: [What they do]
**Input**: [What's needed]
**Output**: [What's produced]
**Next**: [What happens next]

### Step 2: [Step Name]
**Actor**: [Who performs this]
**Action**: [What they do]
**Decision Point**: [If applicable]
- If [condition]: Go to Step 3
- If [condition]: Go to Step 4

### Step 3: [Step Name]
[Continue pattern]

## Decision Points
- **[Decision 1]**: [Criteria and outcomes]
- **[Decision 2]**: [Criteria and outcomes]

## Exception Paths

### Exception 1: [Exception Name]
**Trigger**: [What causes this exception]
**Handling**: [How it's handled]
**Recovery**: [How to get back to main flow]

### Exception 2: [Exception Name]
[Continue pattern]

## Postconditions
- [State after successful completion]
- [What should be true]

## Business Rules
- [Rule that governs the workflow]
- [Another rule]

## SLAs/Timing
- **End-to-end**: [Target completion time]
- **Step X**: [Specific timing requirement]

## Notifications
- **[Event]**: Notify [Actor] via [Channel]
- **[Event]**: Notify [Actor] via [Channel]

## Metrics
- [What to measure]
- [Success criteria]

## API Contract
endpoints:
  - operation_id: [operationName]
    path: /api/[resource]
    method: [GET|POST|PUT|DELETE|PATCH]
    auth: [required|optional]
    request:
      headers:
        - name: [header_name]
          type: string
          required: [true|false]
      params:
        - name: [param_name]
          type: [string|number|boolean]
          required: [true|false]
      body:
        type: object
        required: [field1, field2]
        properties:
          field1:
            type: [string|number|boolean|array|object]
            format: [email|uri|date|datetime]
            minLength: [number]
            maxLength: [number]
            pattern: [regex]
          field2:
            type: [type]
    response:
      200:
        description: Success response
        body:
          type: object
          properties:
            [response_field]: {type: [type]}
      400:
        description: Validation error
        body:
          $ref: '#/components/schemas/Error'
      401:
        description: Unauthorized
      404:
        description: Not found
    performance:
      p50: < [N]ms
      p95: < [N]ms
      p99: < [N]ms

<!-- See components/spec-validation-cases.md for validation case format -->
## Validation Cases

### Test Cases
- [ ] [TC-XXX: Test description](/specs/test-cases/TC-XXX.yaml)

### Scenario Cases
- [ ] [SC-XXX: Scenario description](/specs/scenario-cases/SC-XXX.yaml)

<!-- See components/spec-implementation-refs.md for implementation reference format -->
## Implementation References

- Workflow implementation: `[path/to/workflow/implementation]`
- API endpoints: `[path/to/api/endpoints]`
- Tests: `[path/to/workflow/tests]`

<!-- See components/spec-uncertainties.md for uncertainties format -->
## Uncertainties

- [ ] [Describe uncertainty or question]

## Related Workflows
- **[Workflow Name]**: [Relationship]
- **[Workflow Name]**: [Relationship]