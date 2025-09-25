#!/bin/bash

# Script to update all spec templates to remove inline test cases and add validation cases section

TEMPLATES_DIR="/Users/keith/claude/specifytest/.specify/templates"

# Function to update a spec template
update_template() {
    local template_file="$1"
    local temp_file="${template_file}.tmp"

    echo "Updating $template_file..."

    # Read the file and process it
    awk '
    BEGIN {
        in_test_section = 0
        printed_validation = 0
    }

    # When we hit the Test Cases section, start skipping
    /^## Test Cases/ {
        in_test_section = 1
        # Print the new Validation Cases section instead
        if (!printed_validation) {
            print "## Validation Cases"
            print ""
            print "### Test Cases"
            print "References to standalone test cases that validate this spec:"
            print "- TC-001: [Brief description of what this test validates]"
            print "- TC-002: [Brief description of what this test validates]"
            print "- TC-003: [Brief description of what this test validates]"
            print ""
            print "### Scenario Cases"
            print "References to end-to-end scenarios involving this spec:"
            print "- SC-001: [Brief description of the scenario]"
            print "- SC-002: [Brief description of the scenario]"
            print ""
            print "### Notes"
            print "- Test cases are defined in `/test-cases/` directory"
            print "- Scenario cases are defined in `/scenario-cases/` directory"
            print "- Precondition cases referenced by tests are in `/precondition-cases/` directory"
            print ""
            printed_validation = 1
        }
        next
    }

    # When we hit the next major section after Test Cases, stop skipping
    /^## [^T]/ || /^## I/ || /^## U/ || /^## R/ {
        if (in_test_section && $0 !~ /^## Test/) {
            in_test_section = 0
        }
    }

    # Skip lines in the test section
    in_test_section { next }

    # Print all other lines
    { print }
    ' "$template_file" > "$temp_file"

    # Replace the original file
    mv "$temp_file" "$template_file"
    echo "Updated $template_file"
}

# Update each spec template (excluding the ones we're deleting)
for template in "$TEMPLATES_DIR"/spec-*.md; do
    basename=$(basename "$template")

    # Skip the templates we're going to delete
    if [[ "$basename" == "spec-test-case.md" ]] || \
       [[ "$basename" == "spec-scenario-case.md" ]] || \
       [[ "$basename" == "spec-precondition-case.md" ]]; then
        echo "Skipping $basename (will be deleted)"
        continue
    fi

    # Skip if already updated (workflow already done manually)
    if [[ "$basename" == "spec-workflow.md" ]]; then
        echo "Skipping $basename (already updated)"
        continue
    fi

    update_template "$template"
done

echo "All spec templates updated!"