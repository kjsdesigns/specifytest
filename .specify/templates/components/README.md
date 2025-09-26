# Template Components

This directory contains reusable components for specification templates, following the DRY (Don't Repeat Yourself) principle.

## Components

### spec-header.md
Common YAML frontmatter for all specification types. Includes:
- id, name, type, status, related, hash_timestamp fields
- Instructions for replacing placeholders

### spec-validation-cases.md
Standard section for listing validation cases (test, scenario, precondition).
Used by specs that need to reference their validation approach.

### spec-uncertainties.md
Template section for documenting uncertainties and open questions.
Should be removed from specs once all uncertainties are resolved.

### spec-implementation-refs.md
Standard format for linking to implementation files.
Used by specs that have corresponding code implementations.

### spec-base-fields.yaml
Base YAML structure for Case specifications (TC, SC, PC).
Defines the minimum required fields for any Case.

## Usage

These components are referenced by the spec templates to:
1. Ensure consistency across all specification types
2. Reduce maintenance burden (update once, affect all)
3. Make it easier to add new specification types
4. Enforce standard structure and naming conventions

## Maintenance

When updating these components:
1. Consider impact on all templates that use them
2. Update timestamp fields to track changes
3. Ensure backwards compatibility when possible
4. Document breaking changes in constitution