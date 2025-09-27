#!/usr/bin/env bash
#
# Install Git hooks for Specify framework
#

# Find repository root
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)

if [ -z "$REPO_ROOT" ]; then
    echo "Error: Not in a git repository"
    exit 1
fi

# Colors
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}Installing Specify Git hooks...${NC}"

# Create git hooks directory if it doesn't exist
GIT_HOOKS_DIR="$REPO_ROOT/.git/hooks"
mkdir -p "$GIT_HOOKS_DIR"

# Source hooks directory
HOOKS_SOURCE="$REPO_ROOT/.specify/hooks"

if [ ! -d "$HOOKS_SOURCE" ]; then
    echo -e "${RED}Error: Hooks source directory not found: $HOOKS_SOURCE${NC}"
    exit 1
fi

# Install each hook
HOOKS_INSTALLED=0
HOOKS_SKIPPED=0

for hook_file in "$HOOKS_SOURCE"/*; do
    if [ -f "$hook_file" ]; then
        hook_name=$(basename "$hook_file")
        target="$GIT_HOOKS_DIR/$hook_name"

        # Check if hook already exists
        if [ -f "$target" ]; then
            echo -e "${YELLOW}Hook already exists: $hook_name${NC}"
            read -p "Overwrite? (y/n) " -n 1 -r
            echo
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                echo -e "${YELLOW}Skipped: $hook_name${NC}"
                HOOKS_SKIPPED=$((HOOKS_SKIPPED + 1))
                continue
            fi
        fi

        # Copy hook and make executable
        cp "$hook_file" "$target"
        chmod +x "$target"

        echo -e "${GREEN}✓ Installed: $hook_name${NC}"
        HOOKS_INSTALLED=$((HOOKS_INSTALLED + 1))
    fi
done

echo ""
echo "================================================"
echo " Git Hooks Installation Summary"
echo "================================================"
echo -e "Installed: ${GREEN}$HOOKS_INSTALLED${NC}"
echo -e "Skipped:   ${YELLOW}$HOOKS_SKIPPED${NC}"
echo ""

if [ $HOOKS_INSTALLED -gt 0 ]; then
    echo -e "${GREEN}✓ Git hooks installed successfully${NC}"
    echo ""
    echo "Installed hooks:"
    echo "  - pre-commit: Validates templates and specs before commit"
    echo ""
    echo "To disable hooks temporarily:"
    echo "  git commit --no-verify"
else
    echo -e "${YELLOW}⚠ No new hooks were installed${NC}"
fi