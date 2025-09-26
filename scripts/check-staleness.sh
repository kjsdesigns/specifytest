#!/bin/bash

# Staleness Detection Tool (Simplified Timestamp-Only Version)
# Compares Case timestamps with implementation references
# Usage: check-staleness.sh [directory]
#
# Output: Staleness report grouped by priority based on age

set -euo pipefail

# Error handler
error_exit() {
    echo "Error: $1" >&2
    exit ${2:-1}
}

# Trap errors
trap 'error_exit "Script failed at line $LINENO"' ERR

# Configuration
REPO_ROOT="${1:-.}"  # Default to current directory if not specified

# Validate directory exists
if [[ ! -d "$REPO_ROOT" ]]; then
    error_exit "Directory not found: $REPO_ROOT" 2
fi

TEST_CASES_DIR="$REPO_ROOT/specs/test-cases"
SCENARIO_CASES_DIR="$REPO_ROOT/specs/scenario-cases"
PRECONDITION_CASES_DIR="$REPO_ROOT/specs/precondition-cases"

# Check if Case directories exist
if [[ ! -d "$TEST_CASES_DIR" ]] && [[ ! -d "$SCENARIO_CASES_DIR" ]] && [[ ! -d "$PRECONDITION_CASES_DIR" ]]; then
    echo "Warning: No Case directories found. Creating them..." >&2
    mkdir -p "$TEST_CASES_DIR" "$SCENARIO_CASES_DIR" "$PRECONDITION_CASES_DIR"
    echo "Info: Case directories created. No Cases to check yet." >&2
    exit 0
fi

# Color codes for output
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Arrays to store staleness findings
declare -a CRITICAL_STALE  # >30 days
declare -a HIGH_STALE      # 7-30 days
declare -a MEDIUM_STALE    # 1-7 days
declare -a LOW_STALE       # <1 day
declare -a UP_TO_DATE      # Matching timestamps

# Function to extract timestamp from Case file
get_case_timestamp() {
    local case_file="$1"

    if [[ ! -f "$case_file" ]]; then
        echo "ERROR: File not found" >&2
        return 1
    fi

    local timestamp=$(grep '^hash_timestamp:' "$case_file" 2>/dev/null | sed 's/hash_timestamp: *//')

    if [[ -z "$timestamp" ]]; then
        echo "ERROR: Missing timestamp" >&2
        return 1
    fi

    # Validate ISO 8601 format
    if ! echo "$timestamp" | grep -qE '^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z?$'; then
        echo "ERROR: Invalid timestamp format" >&2
        return 1
    fi

    echo "$timestamp"
}

# Function to calculate days between two ISO timestamps
calculate_days_diff() {
    local timestamp1="$1"
    local timestamp2="$2"

    # Convert ISO timestamps to Unix epoch (macOS compatible)
    local epoch1=$(date -j -f "%Y-%m-%dT%H:%M:%SZ" "$timestamp1" "+%s" 2>/dev/null || echo "0")
    local epoch2=$(date -j -f "%Y-%m-%dT%H:%M:%SZ" "$timestamp2" "+%s" 2>/dev/null || echo "0")

    if [ "$epoch1" -eq 0 ] || [ "$epoch2" -eq 0 ]; then
        # Fallback for Linux systems
        epoch1=$(date -d "$timestamp1" "+%s" 2>/dev/null || echo "0")
        epoch2=$(date -d "$timestamp2" "+%s" 2>/dev/null || echo "0")
    fi

    local diff=$((epoch2 - epoch1))
    local days=$((diff / 86400))

    echo "$days"
}

# Function to scan implementation files for timestamp references
scan_implementation_files() {
    local search_dirs=("$REPO_ROOT/src" "$REPO_ROOT/tests" "$REPO_ROOT/test")

    echo "Scanning for implementation files with timestamp references..."
    echo ""

    for dir in "${search_dirs[@]}"; do
        if [ ! -d "$dir" ]; then
            continue
        fi

        # Find files with timestamp references (Python, JavaScript, TypeScript, etc.)
        find "$dir" -type f \( -name "*.py" -o -name "*.js" -o -name "*.ts" -o -name "*.java" \) | while read -r impl_file; do
            # Look for patterns like:
            # Implements: /test-cases/TC-001.yaml
            # Case Timestamp: 2024-01-15T10:30:00Z

            local case_ref=$(grep -E "Implements:.*\.(yaml|yml)" "$impl_file" 2>/dev/null | head -1 | sed 's/.*Implements: *//' | sed 's/[[:space:]]*$//')
            local impl_timestamp=$(grep -E "Case Timestamp:|Timestamp:" "$impl_file" 2>/dev/null | head -1 | sed 's/.*Timestamp: *//' | sed 's/[[:space:]\"]*$//')

            if [ -n "$case_ref" ] && [ -n "$impl_timestamp" ]; then
                check_staleness "$impl_file" "$case_ref" "$impl_timestamp"
            fi
        done
    done
}

# Function to check staleness of a single implementation
check_staleness() {
    local impl_file="$1"
    local case_ref="$2"
    local impl_timestamp="$3"

    # Resolve case file path
    local case_file="$REPO_ROOT$case_ref"

    # Get current case timestamp
    local case_timestamp=$(get_case_timestamp "$case_file")

    if [[ "$case_timestamp" == "ERROR:"* ]]; then
        echo "  Warning: Cannot check $impl_file - $case_timestamp for $case_ref"
        return
    fi

    # Compare timestamps - simple comparison, Case timestamp > implementation timestamp means stale
    local case_epoch=$(date -j -f "%Y-%m-%dT%H:%M:%SZ" "$case_timestamp" "+%s" 2>/dev/null || date -d "$case_timestamp" "+%s" 2>/dev/null || echo "0")
    local impl_epoch=$(date -j -f "%Y-%m-%dT%H:%M:%SZ" "$impl_timestamp" "+%s" 2>/dev/null || date -d "$impl_timestamp" "+%s" 2>/dev/null || echo "0")

    if [ "$case_epoch" -le "$impl_epoch" ]; then
        # Implementation is up to date
        UP_TO_DATE+=("$impl_file → $case_ref")
    else
        # Calculate staleness in days
        local days_stale=$(calculate_days_diff "$impl_timestamp" "$case_timestamp")
        local staleness_msg="$impl_file → $case_ref (${days_stale} days stale)"

        # Categorize by staleness
        if [ "$days_stale" -gt 30 ]; then
            CRITICAL_STALE+=("$staleness_msg")
        elif [ "$days_stale" -gt 7 ]; then
            HIGH_STALE+=("$staleness_msg")
        elif [ "$days_stale" -gt 1 ]; then
            MEDIUM_STALE+=("$staleness_msg")
        else
            LOW_STALE+=("$staleness_msg")
        fi
    fi
}

# Function to print staleness report
print_report() {
    echo "========================================"
    echo "    TIMESTAMP-BASED STALENESS REPORT   "
    echo "========================================"
    echo ""

    local has_issues=false

    if [ ${#CRITICAL_STALE[@]} -gt 0 ]; then
        has_issues=true
        echo -e "${RED}CRITICAL (>30 days stale):${NC}"
        for item in "${CRITICAL_STALE[@]}"; do
            echo "  ✗ $item"
        done
        echo ""
    fi

    if [ ${#HIGH_STALE[@]} -gt 0 ]; then
        has_issues=true
        echo -e "${RED}HIGH (7-30 days stale):${NC}"
        for item in "${HIGH_STALE[@]}"; do
            echo "  ✗ $item"
        done
        echo ""
    fi

    if [ ${#MEDIUM_STALE[@]} -gt 0 ]; then
        has_issues=true
        echo -e "${YELLOW}MEDIUM (1-7 days stale):${NC}"
        for item in "${MEDIUM_STALE[@]}"; do
            echo "  ⚠ $item"
        done
        echo ""
    fi

    if [ ${#LOW_STALE[@]} -gt 0 ]; then
        has_issues=true
        echo -e "${YELLOW}LOW (<1 day stale):${NC}"
        for item in "${LOW_STALE[@]}"; do
            echo "  ⚠ $item"
        done
        echo ""
    fi

    if [ ${#UP_TO_DATE[@]} -gt 0 ]; then
        echo -e "${GREEN}UP TO DATE:${NC}"
        echo "  ✓ ${#UP_TO_DATE[@]} implementations match their specification timestamps"
        echo ""
    fi

    # Summary
    echo "----------------------------------------"
    echo "SUMMARY:"
    local total_stale=$((${#CRITICAL_STALE[@]} + ${#HIGH_STALE[@]} + ${#MEDIUM_STALE[@]} + ${#LOW_STALE[@]}))
    local total_current=${#UP_TO_DATE[@]}
    local total=$((total_stale + total_current))

    echo "  Total implementations checked: $total"
    echo "  Stale implementations: $total_stale"
    echo "  Current implementations: $total_current"

    if [ "$total_stale" -gt 0 ]; then
        echo ""
        echo "  Action Required:"
        if [ ${#CRITICAL_STALE[@]} -gt 0 ]; then
            echo "  - ${#CRITICAL_STALE[@]} CRITICAL updates needed immediately"
        fi
        if [ ${#HIGH_STALE[@]} -gt 0 ]; then
            echo "  - ${#HIGH_STALE[@]} HIGH priority updates needed soon"
        fi
        if [ ${#MEDIUM_STALE[@]} -gt 0 ]; then
            echo "  - ${#MEDIUM_STALE[@]} MEDIUM priority updates needed"
        fi
        if [ ${#LOW_STALE[@]} -gt 0 ]; then
            echo "  - ${#LOW_STALE[@]} LOW priority updates (recently changed)"
        fi
    else
        echo -e "  ${GREEN}✓ All implementations are up to date!${NC}"
    fi

    echo ""
    echo "========================================"
    echo "Note: This uses simple timestamp comparison."
    echo "Update Case file hash_timestamp on every save."
    echo "========================================"

    # Exit with error code if critical issues found
    if [ ${#CRITICAL_STALE[@]} -gt 0 ]; then
        exit 2
    elif [ ${#HIGH_STALE[@]} -gt 0 ]; then
        exit 1
    else
        exit 0
    fi
}

# Main execution
main() {
    echo "Timestamp-Based Staleness Detection v2.0"
    echo "Repository: $REPO_ROOT"
    echo ""

    # Check if Case directories exist
    if [ ! -d "$TEST_CASES_DIR" ] && [ ! -d "$SCENARIO_CASES_DIR" ]; then
        echo "Warning: No Case directories found. Have Cases been created yet?"
        echo "Expected directories:"
        echo "  - $TEST_CASES_DIR"
        echo "  - $SCENARIO_CASES_DIR"
        echo "  - $PRECONDITION_CASES_DIR"
        exit 0
    fi

    # Scan for stale implementations
    scan_implementation_files

    # Print report
    print_report
}

# Run main function
main "$@"