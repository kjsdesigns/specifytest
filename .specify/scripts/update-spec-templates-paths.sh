#!/bin/bash

# Update all spec templates to use file paths in validation_cases sections

TEMPLATE_DIR="/Users/keith/claude/specifytest/.specify/templates"

for template in "$TEMPLATE_DIR"/spec-*.md; do
    echo "Updating $(basename "$template")..."

    # Update Test Cases section to use paths
    sed -i '' 's/^- TC-\([0-9]\{3\}\): /- \/test-cases\/TC-\1.yaml: /g' "$template"

    # Update Scenario Cases section to use paths
    sed -i '' 's/^- SC-\([0-9]\{3\}\): /- \/scenario-cases\/SC-\1.yaml: /g' "$template"

    # Update inline references in validation_cases sections
    sed -i '' 's/References to standalone test cases/References to standalone test cases by file path/g' "$template"
    sed -i '' 's/References to end-to-end scenarios/References to end-to-end scenarios by file path/g' "$template"
done

echo "All spec templates updated to use file path references"