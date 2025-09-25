#!/usr/bin/env bash

set -e

JSON_MODE=false
ARGS=()
for arg in "$@"; do
    case "$arg" in
        --json) JSON_MODE=true ;;
        --help|-h) echo "Usage: $0 [--json] <feature_description>"; exit 0 ;;
        *) ARGS+=("$arg") ;;
    esac
done

FEATURE_DESCRIPTION="${ARGS[*]}"
if [ -z "$FEATURE_DESCRIPTION" ]; then
    echo "Usage: $0 [--json] <feature_description>" >&2
    exit 1
fi

# Function to find the repository root by searching for existing project markers
find_repo_root() {
    local dir="$1"
    while [ "$dir" != "/" ]; do
        if [ -d "$dir/.git" ] || [ -d "$dir/.specify" ]; then
            echo "$dir"
            return 0
        fi
        dir="$(dirname "$dir")"
    done
    return 1
}

# Resolve repository root. Prefer git information when available, but fall back
# to searching for repository markers so the workflow still functions in repositories that
# were initialised with --no-git.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if git rev-parse --show-toplevel >/dev/null 2>&1; then
    REPO_ROOT=$(git rev-parse --show-toplevel)
    HAS_GIT=true
else
    REPO_ROOT="$(find_repo_root "$SCRIPT_DIR")"
    if [ -z "$REPO_ROOT" ]; then
        echo "Error: Could not determine repository root. Please run this script from within the repository." >&2
        exit 1
    fi
    HAS_GIT=false
fi

cd "$REPO_ROOT"

# Ensure modular spec directories exist
SPECS_DIR="$REPO_ROOT/specs"
mkdir -p "$SPECS_DIR"
mkdir -p "$SPECS_DIR/workflows"
mkdir -p "$SPECS_DIR/pages"
mkdir -p "$SPECS_DIR/concepts"
mkdir -p "$SPECS_DIR/data"
mkdir -p "$SPECS_DIR/contracts"
mkdir -p "$SPECS_DIR/integrations"
mkdir -p "$SPECS_DIR/security"
mkdir -p "$SPECS_DIR/technology"
mkdir -p "$SPECS_DIR/configuration"

# Create plans directory for execution tracking
PLANS_DIR="$REPO_ROOT/plans"
mkdir -p "$PLANS_DIR"

# Generate a plan name based on feature description
PLAN_NAME=$(echo "$FEATURE_DESCRIPTION" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/-\+/-/g' | sed 's/^-//' | sed 's/-$//')
WORDS=$(echo "$PLAN_NAME" | tr '-' '\n' | grep -v '^$' | head -3 | tr '\n' '-' | sed 's/-$//')

# Find the next available plan number
HIGHEST=0
if [ -d "$PLANS_DIR" ]; then
    for dir in "$PLANS_DIR"/*; do
        [ -d "$dir" ] || continue
        dirname=$(basename "$dir")
        number=$(echo "$dirname" | grep -o '^[0-9]\+' || echo "0")
        number=$((10#$number))
        if [ "$number" -gt "$HIGHEST" ]; then HIGHEST=$number; fi
    done
fi

NEXT=$((HIGHEST + 1))
PLAN_NUM=$(printf "%03d" "$NEXT")
PLAN_NAME="${PLAN_NUM}-${WORDS}"

# Create plan directory
PLAN_DIR="$PLANS_DIR/$PLAN_NAME"
mkdir -p "$PLAN_DIR"

# Note: We do NOT create any spec files here - that's the job of /specify command
# which will evaluate requirements and create/update appropriate type-specific specs

# Set environment variable for current session
export SPECIFY_FEATURE="$PLAN_NAME"

if $JSON_MODE; then
    printf '{"PLAN_NAME":"%s","SPECS_DIR":"%s","PLANS_DIR":"%s","PLAN_NUM":"%s"}\n' "$PLAN_NAME" "$SPECS_DIR" "$PLAN_DIR" "$PLAN_NUM"
else
    echo "PLAN_NAME: $PLAN_NAME"
    echo "SPECS_DIR: $SPECS_DIR"
    echo "PLAN_DIR: $PLAN_DIR"
    echo "PLAN_NUM: $PLAN_NUM"
    echo ""
    echo "Modular spec directories prepared at: $SPECS_DIR"
    echo "Plan directory created at: $PLAN_DIR"
    echo "SPECIFY_FEATURE environment variable set to: $PLAN_NAME"
    echo ""
    echo "The /specify command will now evaluate requirements and create/update"
    echo "appropriate type-specific specs based on the requirement analysis."
fi