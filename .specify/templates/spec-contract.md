<!-- See components/spec-header.md for header format -->
---
id: CONTRACT-[XXX]
name: [descriptive-kebab-case-name]
type: Contract
status: draft
category: [api|data|ui|event|message]
consumers: []
providers: []
related: []
hash_timestamp: [ISO_8601_TIMESTAMP]  # Updated on every save (YYYY-MM-DDTHH:MM:SSZ)
---

# {name}

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
interface {ContractName} {
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
- **Format**: [SPECIFIC_FORMAT]
- **Validation**: [VALIDATION_RULES]
- **Example**: "example_value"
- **Description**: Detailed description of field purpose

### field2
- **Type**: number
- **Required**: Yes
- **Range**: [MIN_MAX]
- **Default**: [DEFAULT_VALUE]
- **Example**: 42
- **Description**: Detailed description of field purpose

## Usage Patterns

### Provider Implementation
How providers should implement this contract:
```typescript
class ProviderExample implements {ContractName} {
  // Implementation details
}
```

### Consumer Usage
How consumers should use this contract:
```typescript
function consumeContract(data: {ContractName}) {
  // Usage example
}
```

## Versioning
### Current Version: 1.0.0
- Initial contract definition

### Migration Guide
Instructions for migrating between versions (when applicable):
- From 0.9.x to 1.0.0: [MIGRATION_STEPS]

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
- [PROVIDER_COMPONENT_1] ([SPEC_ID]): Description of what it provides
- [PROVIDER_COMPONENT_2] ([SPEC_ID]): Description of what it provides

## Consumers
List of components that consume/use this contract:
- [CONSUMER_COMPONENT_1] ([SPEC_ID]): How it uses the contract
- [CONSUMER_COMPONENT_2] ([SPEC_ID]): How it uses the contract

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

<!-- See components/spec-validation-cases.md for validation case format -->
## Validation Cases

### Test Cases
- [ ] [TC-XXX: Test description](/specs/test-cases/TC-XXX.yaml)

### Scenario Cases
- [ ] [SC-XXX: Scenario description](/specs/scenario-cases/SC-XXX.yaml)

<!-- See components/spec-implementation-refs.md for implementation reference format -->
## Implementation References

- Schema location: `contracts/[CONTRACT_NAME]/`
- Validation: `src/contracts/[CONTRACT_NAME].validator.ts`
- Types: `src/types/contracts/[CONTRACT_NAME].ts`

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

<!-- See components/spec-uncertainties.md for uncertainties format -->
## Uncertainties

- [ ] [DESCRIBE_UNCERTAINTY]

## Notes
- [SPECIAL_CONSIDERATIONS]
- [KNOWN_LIMITATIONS]
- [FUTURE_ENHANCEMENTS]
