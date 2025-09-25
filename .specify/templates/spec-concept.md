---
id: C-[XXX]
type: Concept
name: [Concept Name]
status: draft
related: [Related spec IDs]
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

## Uncertainties
[List any areas of uncertainty, ambiguity, or questions that need to be resolved]

## Domain Contract
entity:
  name: [EntityName]
  table: [table_name]
  fields:
    - name: id
      type: [string|number|boolean|datetime]
      format: [cuid|uuid|email|url]
      constraints:
        primary: [true|false]
        required: [true|false]
        unique: [true|false]
        maxLength: [number]
    - name: [field_name]
      type: [type]
      constraints: {}
  relationships:
    - name: [relationship_name]
      type: [hasOne|hasMany|belongsTo|manyToMany]
      target: [TargetEntity]
      foreign_key: [field_name]
      through: [junction_table]  # For manyToMany
  invariants:
    - [Business rule that must always be true]
    - [Another invariant]
  indexes:
    - fields: [field1, field2]
      unique: [true|false]
      name: [index_name]

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
test_data:
  fixtures: fixtures/[entity_name]/
  factories: factories/[entity_name]Factory

## Glossary
- **[Term 1]**: [Definition]
- **[Term 2]**: [Definition]
