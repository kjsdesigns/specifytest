<!-- See components/spec-header.md for header format -->
---
id: UI-[XXX]
name: [descriptive-kebab-case-name]
type: UI Component
status: draft
related: []
hash_timestamp: [ISO_8601_TIMESTAMP]  # Updated on every save
---

# {name}

## Purpose
[What this UI component allows users to accomplish]

## User Context
**Primary Users**: [Who will use this component]
**Usage Context**: [Where and when this component is used]
**User Goals**: [What users want to achieve with this component]

<!-- See components/spec-ui-structure.md for structure format -->
## Component Structure

### Layout
[Description of the component's visual layout from left-to-right, top-to-bottom]

### Elements
[Description of each element within the component, left-to-right, top-to-bottom]
- **[Element 1]**: [What it shows/does]
  - [If this is a nested UI component, reference: `/specs/ui-components/UI-XXX.md` with context]
- **[Element 2]**: [What it shows/does]
- **[Element 3]**: [What it shows/does]

### Actions/Controls
- **[Action 1]**: [What it does]
- **[Action 2]**: [What it does]

## Props/Parameters
[Configuration values that can be passed to this component when embedded]

| Prop | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| [prop_name] | [string/number/boolean/object/array] | [Yes/No] | [default_value] | [What this prop controls] |

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
- **Default**: [Normal state appearance/behavior]
- **Loading**: [What users see while loading]
- **Empty**: [What users see with no data]
- **Error**: [Error handling display]
- **Disabled**: [Non-interactive state]
- **Hover/Focus**: [Interactive feedback]
- **Active/Selected**: [Selection state]

## Responsive Behavior
- **Desktop**: [Layout/behavior]
- **Tablet**: [Layout/behavior]
- **Mobile**: [Layout/behavior]

## Validation
- [Field validation rules if applicable]
- [Error messages]
- [Success confirmations]

## Accessibility
- [Keyboard navigation requirements]
- [Screen reader considerations]
- [WCAG compliance notes]
- [Focus management]

## Performance
- **Render Time**: [Target time]
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

**Note**: Pages that embed this UI component will indirectly inherit these test and scenario cases. Test cases should include conditions describing when they apply.

<!-- See components/spec-implementation-refs.md for implementation reference format -->
## Implementation References

- Component: `[path/to/component]`
- Component tests: `[path/to/component/tests]`
- Storybook: `[path/to/stories]`

<!-- See components/spec-uncertainties.md for uncertainties format -->
## Uncertainties

- [ ] [Describe uncertainty or question]