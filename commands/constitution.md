---
description: Update the project constitution and sync dependent templates.
---

User input: $ARGUMENTS

## Execution Flow

1. **Load Constitution**
   - Read `.specify/memory/constitution.md`
   - Identify placeholder tokens `[ALL_CAPS_IDENTIFIER]`

2. **Collect Values**
   - Use provided user input or infer from context
   - Increment version using semantic versioning:
     - MAJOR: Breaking changes to principles
     - MINOR: New principles or sections
     - PATCH: Clarifications and fixes
   - Set `LAST_AMENDED_DATE` to today if modified

3. **Update Content**
   - Replace placeholders with concrete values
   - Ensure each principle has name, rules, and rationale
   - Include governance section with amendment procedure

4. **Sync Templates**
   - Update dependent templates if constitution changes affect them:
     - `.specify/templates/plan-template.md`
     - `.specify/templates/spec-*.md` files
     - `.specify/templates/tasks-template.md`
     - `.claude/commands/*.md` files
     - `README.md` and documentation

5. **Generate Report**
   - Add sync impact report as HTML comment in constitution
   - List version change and modified principles
   - Flag templates requiring updates

6. **Save and Summarize**
   - Write updated constitution to `.specify/memory/constitution.md`
   - Provide version change summary and suggested commit message
