#!/bin/bash

# Compute SHA-256 hash and timestamp for Case YAML files
# Usage: compute-case-hash.sh <case-file.yaml>
#
# This script:
# 1. Loads a YAML Case file
# 2. Removes existing content_hash and hash_timestamp fields
# 3. Computes SHA-256 hash of the canonical content
# 4. Generates ISO 8601 timestamp (UTC)
# 5. Updates the file with the new hash and timestamp

set -e

# Check arguments
if [ $# -ne 1 ]; then
    echo "Usage: $0 <case-file.yaml>"
    echo "Example: $0 /test-cases/TC-001.yaml"
    exit 1
fi

CASE_FILE="$1"

# Check if file exists
if [ ! -f "$CASE_FILE" ]; then
    echo "Error: File '$CASE_FILE' not found"
    exit 1
fi

# Check if file is YAML
if [[ ! "$CASE_FILE" =~ \.(yaml|yml)$ ]]; then
    echo "Error: File must be a YAML file (.yaml or .yml)"
    exit 1
fi

# Function to compute hash of YAML content
compute_yaml_hash() {
    local file="$1"

    # Create temporary file for canonical YAML
    local temp_file=$(mktemp)

    # Remove content_hash and hash_timestamp fields, sort keys canonically
    # Using grep -v to exclude the hash fields, then compute SHA-256
    grep -v -E '^\s*(content_hash|hash_timestamp):' "$file" | \
        sed 's/[[:space:]]*$//' | \
        sha256sum | \
        cut -d' ' -f1

    rm -f "$temp_file"
}

# Function to get current timestamp in ISO 8601 format (UTC)
get_iso_timestamp() {
    date -u +"%Y-%m-%dT%H:%M:%SZ"
}

# Function to update YAML file with hash and timestamp
update_yaml_with_hash() {
    local file="$1"
    local hash="$2"
    local timestamp="$3"

    # Create backup
    cp "$file" "${file}.bak"

    # Check if file already has content_hash field
    if grep -q '^content_hash:' "$file"; then
        # Update existing fields
        sed -i '' "s/^content_hash:.*/content_hash: sha256:$hash/" "$file"
        sed -i '' "s/^hash_timestamp:.*/hash_timestamp: $timestamp/" "$file"
    else
        # Insert new fields after 'name:' field
        # This maintains field order as specified in templates
        awk -v hash="$hash" -v ts="$timestamp" '
            /^name:/ {
                print $0
                print "content_hash: sha256:" hash "  # Auto-computed from YAML content"
                print "hash_timestamp: " ts "  # When hash was generated"
                next
            }
            { print }
        ' "${file}.bak" > "$file"
    fi

    # Clean up backup
    rm -f "${file}.bak"
}

# Main execution
echo "Processing: $CASE_FILE"

# Compute hash of current content (excluding existing hash fields)
CONTENT_HASH=$(compute_yaml_hash "$CASE_FILE")
echo "  Computed hash: sha256:$CONTENT_HASH"

# Get current timestamp
HASH_TIMESTAMP=$(get_iso_timestamp)
echo "  Timestamp: $HASH_TIMESTAMP"

# Update the file with new hash and timestamp
update_yaml_with_hash "$CASE_FILE" "$CONTENT_HASH" "$HASH_TIMESTAMP"

echo "  ✓ File updated successfully"
echo ""
echo "Updated fields:"
echo "  content_hash: sha256:$CONTENT_HASH"
echo "  hash_timestamp: $HASH_TIMESTAMP"