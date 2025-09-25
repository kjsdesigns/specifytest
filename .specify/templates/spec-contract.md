---
id: CON-XXX
type: Contract
name: [Contract Name]
status: draft
category: [api|data|ui|event|message]
consumers: []
providers: []
related: []
---
# [Contract Name]

## Purpose
Define the shared contract/interface that multiple components use to communicate, ensuring consistency and compatibility across the system.

## Category
- **api**: REST/GraphQL API contracts
- **data**: Shared data structures and schemas
- **ui**: UI component interfaces and props
- **event**: Event bus and messaging contracts
- **message**: Queue and async message formats

## Contract Definition

### Interface
```typescript
// TypeScript interface definition
interface [ContractName] {
  // Required fields
  field1: type;
  field2: type;

  // Optional fields
  field3?: type;
}
```

### Schema
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "field1": {
      "type": "string",
      "description": "Field description"
    },
    "field2": {
      "type": "number",
      "minimum": 0
    }
  },
  "required": ["field1", "field2"]
}
```

## Field Specifications

### field1
- **Type**: string
- **Required**: Yes
- **Format**: [specific format if any]
- **Validation**: [validation rules]
- **Example**: "example_value"
- **Description**: Detailed description of field purpose

### field2
- **Type**: number
- **Required**: Yes
- **Range**: [min-max if applicable]
- **Default**: [default value if any]
- **Example**: 42
- **Description**: Detailed description of field purpose

## Usage Patterns

### Provider Implementation
How providers should implement this contract:
```typescript
class ProviderExample implements [ContractName] {
  // Implementation details
}
```

### Consumer Usage
How consumers should use this contract:
```typescript
function consumeContract(data: [ContractName]) {
  // Usage example
}
```

## Versioning
### Current Version: 1.0.0
- Initial contract definition

### Migration Guide
Instructions for migrating between versions (when applicable):
- From 0.9.x to 1.0.0: [migration steps]

## Validation Rules
Comprehensive validation requirements:
- [ ] Field1 must be unique within context
- [ ] Field2 cannot be negative
- [ ] Combined fields must satisfy business rule X

## Error Handling
### Error Codes
- `INVALID_FIELD1`: Field1 validation failed
- `MISSING_REQUIRED`: Required field missing
- `TYPE_MISMATCH`: Field type incorrect

### Error Response Format
```json
{
  "error": "ERROR_CODE",
  "message": "Human readable message",
  "field": "field_name",
  "value": "submitted_value"
}
```

## Providers
List of components that provide/implement this contract:
- [[Provider Component 1]](SPEC-ID): Description of what it provides
- [[Provider Component 2]](SPEC-ID): Description of what it provides

## Consumers
List of components that consume/use this contract:
- [[Consumer Component 1]](SPEC-ID): How it uses the contract
- [[Consumer Component 2]](SPEC-ID): How it uses the contract

## Examples

### Valid Examples
```json
{
  "field1": "valid_example",
  "field2": 123
}
```

### Invalid Examples
```json
{
  "field1": "", // Empty string not allowed
  "field2": -1  // Negative not allowed
}
```

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
schema_location: contracts/[contract_name]/
validation: src/contracts/[contract_name].validator.ts
types: src/types/contracts/[contract_name].ts

## Breaking Changes
Track breaking changes and migration requirements:
- **v1.0.0**: Initial release
- **v2.0.0** (planned): [description of breaking changes]

## Performance Considerations
- Serialization overhead: ~X ms
- Validation overhead: ~Y ms
- Maximum payload size: Z KB

## Security Considerations
- [ ] PII data handling requirements
- [ ] Encryption requirements
- [ ] Authentication/authorization needs
- [ ] Rate limiting considerations

## Notes
- [Special considerations]
- [Known limitations]
- [Future enhancements]
