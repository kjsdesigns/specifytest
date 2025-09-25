---
id: W-[XXX]
type: Workflow
name: [Workflow Name]
status: draft
related: [Related spec IDs]
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

## Validation Cases

### Test Cases
References to standalone test cases by file path that validate this workflow:
- /test-cases/TC-001.yaml: [Brief description of what this test validates]
- /test-cases/TC-002.yaml: [Brief description of what this test validates]
- /test-cases/TC-003.yaml: [Brief description of what this test validates]

### Scenario Cases
References to end-to-end scenarios by file path involving this workflow:
- /scenario-cases/SC-001.yaml: [Brief description of the scenario]
- /scenario-cases/SC-002.yaml: [Brief description of the scenario]

### Notes
- Test cases are defined in `/test-cases/` directory
- Scenario cases are defined in `/scenario-cases/` directory
- Precondition cases referenced by tests are in `/precondition-cases/` directory

## Implementation References
preconditions:
  location: /precondition-cases/
  shared: [List of reusable precondition IDs]
api_client:
  location: tests/api/
  class: [WorkflowName]ApiClient
test_data:
  fixtures: fixtures/workflows/[workflow_name]/

## Uncertainties
[List any areas of uncertainty, ambiguity, or questions that need to be resolved]

## Related Workflows
- **[Workflow Name]**: [Relationship]
- **[Workflow Name]**: [Relationship]