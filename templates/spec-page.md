<!--
Template Metadata (used by type registry generator)
type: Page
id_prefix: PAGE
name_guidelines: "UI page or screen"
name_examples: ["login", "dashboard", "settings", "profile"]
file_extension: md

Validation rules: see .specify/schemas/template-schema.json
-->
<!-- See components/spec-header.md for header format -->
---
id: PAGE-[XXX]
name: [descriptive_snake_case_name]
type: Page
status: draft
related: []
hash_timestamp: [ISO_8601_TIMESTAMP]  # Updated on every save
---

# {name}

## Purpose
[What this page/interface allows users to accomplish]

## User Context
**Primary Users**: [Who will use this page]
**Entry Points**: [How users get to this page]
**User Goals**: [What users want to achieve]

<!-- See components/spec-ui-structure.md for structure format -->
## Page Structure

### Layout
[Description of the overall page layout from left-to-right, top-to-bottom]

### Elements
[Description of each element in the order they appear, left-to-right, top-to-bottom]

- **[Element 1]**: [What it shows/does]
  - [If this is a UI component, reference: `/specs/ui-components/UI-XXX.md` with context about what object/data it represents]

- **[Element 2]**: [What it shows/does]
  - [If nested UI component: path and context]

- **[Element 3]**: [What it shows/does]

### Actions/Controls
- **[Action 1]**: [What it does]
- **[Action 2]**: [What it does]
- **[Action 3]**: [What it does]

## Data Display
- **[Data Element 1]**: [What it shows and why]
- **[Data Element 2]**: [What it shows and why]

## User Interactions

### Primary Actions
1. **[Action]**: [Expected behavior]
2. **[Action]**: [Expected behavior]

### Secondary Actions
- [List of less common actions]

## States
- **Loading**: [What users see while loading]
- **Empty**: [What users see with no data]
- **Error**: [Error handling display]
- **Success**: [Success feedback]

## Responsive Behavior
- **Desktop**: [Layout/behavior]
- **Tablet**: [Layout/behavior]
- **Mobile**: [Layout/behavior]

## Navigation
**Previous Page**: [Where users come from]
**Next Steps**: [Where users typically go next]
**Breadcrumbs**: [Navigation context]

## Validation
- [Field validation rules]
- [Error messages]
- [Success confirmations]

## Accessibility
- [Keyboard navigation requirements]
- [Screen reader considerations]
- [WCAG compliance notes]

## Performance
- **Initial Load**: [Target time]
- **Interactions**: [Response time targets]
- **Data Updates**: [Refresh strategy]

## UI Contract
components:
  - id: [component_id]
    type: [input|dropdown|button|list|dialog|etc]
    data_testid: [test-identifier]
    props:
      - name: [prop_name]
        type: [string|number|boolean|etc]
        required: [true|false]
        default: [value]
    state:
      - name: [state_variable]
        type: [type]
        initial: [value]
    events:
      - name: [event_name]
        payload:
          [field]: [type]
    validation:
      - field: [field_name]
        rules:
          - required: [true|false]
          - pattern: [regex]
          - min: [value]
          - max: [value]
    accessibility:
      aria_label: [label]
      role: [role]
      tab_index: [number]

<!-- See components/spec-validation-cases.md for validation case format -->
## Validation Cases

### Test Cases
- [ ] [TC-XXX: Test description](/specs/test-cases/TC-XXX.yaml)

### Scenario Cases
- [ ] [SC-XXX: Scenario description](/specs/scenario-cases/SC-XXX.yaml)

**Note**: Pages that embed UI components indirectly inherit test and scenario cases from those components. Only list cases here that directly test this page's unique functionality.

<!-- See components/spec-implementation-refs.md for implementation reference format -->
## Implementation References

- Page component: `[path/to/page/component]`
- Page tests: `[path/to/page/tests]`
- Page objects: `[path/to/page/objects]`

<!-- See components/spec-uncertainties.md for uncertainties format -->
## Uncertainties

- [ ] [Describe uncertainty or question]
