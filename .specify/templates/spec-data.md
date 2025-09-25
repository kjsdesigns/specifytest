---
id: DATA-[XXX]
type: DataSchema
name: [Schema Name]
status: draft
related: [Related spec IDs]
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
fixtures:
  location: fixtures/data/[schema_name]/
  factory: factories/[ModelName]Factory

## Uncertainties
[List any areas of uncertainty, ambiguity, or questions that need to be resolved]

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
