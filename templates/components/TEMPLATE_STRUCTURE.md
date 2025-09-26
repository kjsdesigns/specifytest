# Template Structure Guide

This document defines the standard section ordering for all Specify templates.

## Standard Section Order

All specification templates should follow this general ordering pattern:

### 1. Header (REQUIRED)
```markdown
<!-- See components/spec-header.md for header format -->
---
id: [TYPE]-[XXX]
name: [descriptive-kebab-case-name]
type: [SpecType]
status: draft
related: []
hash_timestamp: [ISO_8601_TIMESTAMP]
---

# {name}
```

### 2. Core Definition Sections (REQUIRED)
The first sections define what the spec is about. Order varies by spec type:

**For most specs:**
- Purpose / Definition / Overview
- Core characteristics or properties
- Relationships to other specs

**Type-specific variations:**
- Workflow: Actors, Triggers, Process Flow
- Page: Purpose, User Context, Page Structure
- Concept: Definition, Purpose, Characteristics
- Data: Purpose, Schema Definition
- Contract: Purpose, Contract Definition
- Integration: Purpose, Service Configuration
- Security: Purpose, Threat Model
- Configuration: Purpose, Environment Variables
- Technology: Goals, Context, Architecture

### 3. Detailed Specifications (REQUIRED/OPTIONAL mix)
Type-specific detailed sections in logical order:

- Technical details
- Behaviors / Operations
- States / Transitions
- Validation rules
- Business rules
- Examples
- Error handling
- Performance considerations
- Security considerations

### 4. Cross-References Section (REQUIRED when applicable)
**Always near the end**, in this order:

```markdown
## Validation Cases
<!-- See components/spec-validation-cases.md -->

### Test Cases
- [ ] [TC-XXX: Test description](/specs/test-cases/TC-XXX.yaml)

### Scenario Cases
- [ ] [SC-XXX: Scenario description](/specs/scenario-cases/SC-XXX.yaml)
```

### 5. Implementation Section (REQUIRED)
```markdown
## Implementation References
<!-- See components/spec-implementation-refs.md -->

- Main implementation: `[PATH]`
- Tests: `[PATH]`
- Additional references as needed
```

### 6. Meta Sections (OPTIONAL)
**Always at the very end:**

```markdown
## Uncertainties
<!-- See components/spec-uncertainties.md -->
- [ ] [DESCRIBE_UNCERTAINTY]

## Notes / Glossary / Related
- Additional meta information
```

## Section Ordering Rules

### MUST Rules
1. **Header MUST be first** - YAML frontmatter and title
2. **Core definition MUST come before details** - What before How
3. **Validation Cases MUST come before Implementation References**
4. **Uncertainties MUST be near the end** - Meta information last

### SHOULD Rules
1. **Group related sections together** - Keep logical flow
2. **Order by dependency** - Definitions before usage
3. **Order by importance** - Critical information first
4. **Order by audience** - Business context before technical details

### MAY Rules
1. **Reorder type-specific sections** - As long as logical flow is maintained
2. **Omit optional sections** - If truly not applicable
3. **Add type-specific sections** - In appropriate position

## Required vs Optional Sections

### REQUIRED Sections (All Templates)
- Header with YAML frontmatter
- Core definition/purpose section
- Validation Cases (even if empty initially)
- Implementation References

### OPTIONAL Sections
Mark with comment:
```markdown
## OPTIONAL: Section Name
Content here
```

Use for:
- Examples
- Anti-patterns
- Glossary
- Notes
- Type-specific advanced sections

## Template-Specific Notes

### Workflow Templates
- Process Flow is core (REQUIRED)
- API Contract is type-specific (OPTIONAL)
- Notifications and Metrics are (OPTIONAL)

### Integration Templates
- Service Configuration is core (REQUIRED)
- Retry Policy, Circuit Breaker are reliability concerns (OPTIONAL)
- Monitoring is operational (OPTIONAL)

### Security Templates
- Threat Model is core (REQUIRED)
- All security controls listed are context-dependent (OPTIONAL individually)

### Contract Templates
- Interface/Schema is core (REQUIRED)
- Providers/Consumers lists are tracking (OPTIONAL but recommended)
- Versioning and Migration guides are lifecycle (OPTIONAL initially)

## Validation

Use `.specify/scripts/validate-specs.py` to check:
- Required sections are present
- Section ordering follows guidelines
- Components are referenced correctly

## Examples

See existing templates in `.specify/templates/spec-*.md` for reference implementations.

## Updates

This guide should be updated whenever:
- New spec types are added
- New components are created
- Section ordering consensus changes

Update the constitution when making breaking changes to required sections.