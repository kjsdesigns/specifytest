<!-- See components/spec-header.md for header format -->
---
id: DATA-[XXX]
name: [descriptive-kebab-case-name]
type: Data
status: draft
related: []
hash_timestamp: [ISO_8601_TIMESTAMP]  # Updated on every save
---

# {name}

## Purpose
[What this data schema represents and why it exists]

## Entity Overview
**Domain**: [Business domain this belongs to]
**Lifecycle**: [How this data is created, updated, and retired]
**Volume**: [Expected data volume]

## Schema Definition

### Core Fields
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | identifier | Yes | Unique identifier |
| [field_name] | [type] | [Yes/No] | [Description] |
| [field_name] | [type] | [Yes/No] | [Description] |

### Relationships
| Related Entity | Relationship Type | Cardinality | Description |
|---------------|-------------------|-------------|-------------|
| [Entity] | [has_many/belongs_to/etc] | [1:1, 1:N, N:M] | [Purpose] |

### Computed Fields
| Field | Derivation | Update Frequency |
|-------|------------|------------------|
| [field_name] | [How calculated] | [When updated] |

## Validation Rules
- **[Field]**: [Validation rule]
- **[Field]**: [Validation rule]
- **Cross-field**: [Multi-field validation]

## Constraints
- **Uniqueness**: [Which fields must be unique]
- **Referential Integrity**: [Foreign key constraints]
- **Business Constraints**: [Domain-specific rules]

## States & Transitions
### States
- **[State 1]**: [Description]
- **[State 2]**: [Description]

### Valid Transitions
- [State A] → [State B]: [Condition]
- [State B] → [State C]: [Condition]

## Access Patterns
### Query Patterns
- **[Pattern 1]**: [Common query need]
- **[Pattern 2]**: [Common query need]

### Index Requirements
- **Primary**: [Primary key/index]
- **Secondary**: [Additional indexes needed]

## Data Governance
### Retention
- **Active Period**: [How long kept active]
- **Archive Policy**: [When and how archived]
- **Deletion Policy**: [When permanently removed]

### Privacy
- **PII Fields**: [List of personally identifiable information]
- **Encryption**: [Which fields need encryption]
- **Access Control**: [Who can access what]

## Migration Notes
[If replacing existing schema, migration approach]

## Schema Contract
```prisma
model [ModelName] {
  id         String   @id @default(cuid())
  createdAt  DateTime @default(now())
  updatedAt  DateTime @updatedAt

  // Core fields
  [field_name]  [Type]   @[decorators]
  [field_name]  [Type]?  // Optional field

  // Relations
  [relation_name]  [RelatedModel]   @relation(["relationName"])
  [relation_id]    String

  // Indexes
  @@index([field1, field2])
  @@unique([field3])
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

- Main implementation: `[path/to/implementation]`
- Tests: `[path/to/tests]`
- Configuration: `[path/to/config]`

<!-- See components/spec-uncertainties.md for uncertainties format -->
## Uncertainties

- [ ] [Describe uncertainty or question]

## Examples
### Example 1: [Scenario]
```json
{
  "field1": "value1",
  "field2": "value2"
}
```

### Example 2: [Scenario]
```json
{
  "field1": "value1",
  "field2": "value2"
}
```
