<!-- See components/spec-header.md for header format -->
---
id: C-[XXX]
name: [descriptive-kebab-case-name]
type: Concept
status: draft
related: []
hash_timestamp: [ISO_8601_TIMESTAMP]  # Updated on every save
---

# {name}

## Definition
[Clear, concise definition of this domain concept]

## Purpose
[Why this concept exists in the system and what problem it solves]

## Characteristics
- **[Property 1]**: [Description and purpose]
- **[Property 2]**: [Description and purpose]
- **[Property 3]**: [Description and purpose]

## Relationships
- **[Related Concept 1]**: [Nature of relationship]
- **[Related Concept 2]**: [Nature of relationship]

## Behaviors
[Key behaviors or operations associated with this concept]

## States
[If applicable, the different states this concept can have]
- **[State 1]**: [When and why]
- **[State 2]**: [When and why]

## Validation Rules
- [Rule 1]
- [Rule 2]
- [Rule 3]

## Business Rules
- [Business rule 1]
- [Business rule 2]

## Examples
### Example 1: [Scenario Name]
[Concrete example showing the concept in use]

### Example 2: [Scenario Name]
[Another concrete example]

## Anti-patterns
[What this concept is NOT, common misconceptions]

## Domain Contract
<!-- See components/spec-inline-contracts.yaml for common YAML patterns -->
entity:
  name: [ENTITY_NAME]
  table: [TABLE_NAME]
  fields:
    - name: id
      type: [string|number|boolean|datetime]
      format: [cuid|uuid|email|url]
      constraints:
        primary: [true|false]
        required: [true|false]
        unique: [true|false]
        maxLength: [NUMBER]
    - name: [FIELD_NAME]
      type: [TYPE]
      constraints: {}
  relationships:
    - name: [RELATIONSHIP_NAME]
      type: [hasOne|hasMany|belongsTo|manyToMany]
      target: [TARGET_ENTITY]
      foreign_key: [FOREIGN_KEY_FIELD]
      through: [JUNCTION_TABLE]  # For manyToMany only
  invariants:
    - [Business rule that must always be true]
    - [Another invariant]
  indexes:
    - fields: [field1, field2]
      unique: [true|false]
      name: [INDEX_NAME]

<!-- See components/spec-validation-cases.md for validation case format -->
## Validation Cases

### Test Cases
- [ ] [TC-XXX: Test description](/specs/test-cases/TC-XXX.yaml)

### Scenario Cases
- [ ] [SC-XXX: Scenario description](/specs/scenario-cases/SC-XXX.yaml)

<!-- See components/spec-implementation-refs.md for implementation reference format -->
## Implementation References

- Main implementation: `[PATH_TO_IMPLEMENTATION]`
- Tests: `[PATH_TO_TESTS]`
- Test data fixtures: `fixtures/[ENTITY_NAME]/`
- Test factories: `factories/[ENTITY_NAME]Factory`

<!-- See components/spec-uncertainties.md for uncertainties format -->
## Uncertainties

- [ ] [DESCRIBE_UNCERTAINTY]

## Glossary
- **[TERM]**: [DEFINITION]
