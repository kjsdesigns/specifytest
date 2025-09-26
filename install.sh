#!/usr/bin/env bash

# Specifytest Installation Script
# Adds the specifytest repository as a git submodule to your project

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Default specifytest repository URL
SPECIFYTEST_REPO="https://github.com/kjsdesigns/specifytest.git"
SPECIFYTEST_DIR=".specify"

# Function to print colored output
print_color() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

# Function to check prerequisites
check_prerequisites() {
    if ! command -v git &> /dev/null; then
        print_color "$RED" "Error: git is not installed"
        exit 1
    fi

    if ! git rev-parse --is-inside-work-tree &>/dev/null; then
        print_color "$RED" "Error: Not in a git repository"
        print_color "$YELLOW" "Please initialize a git repository first with: git init"
        exit 1
    fi

    if [[ -e "$SPECIFYTEST_DIR" ]]; then
        print_color "$RED" "Error: $SPECIFYTEST_DIR already exists"
        print_color "$YELLOW" "Please remove or rename the existing directory first"
        exit 1
    fi
}

# Function to install specifytest
install_specifytest() {
    print_color "$GREEN" "Installing Specifytest..."

    print_color "$YELLOW" "Adding specifytest as git submodule..."
    if git submodule add "$SPECIFYTEST_REPO" "$SPECIFYTEST_DIR"; then
        print_color "$GREEN" "✓ Submodule added successfully"
    else
        print_color "$RED" "Error: Failed to add submodule"
        exit 1
    fi

    print_color "$YELLOW" "Initializing submodule..."
    if git submodule update --init --recursive; then
        print_color "$GREEN" "✓ Submodule initialized"
    else
        print_color "$RED" "Error: Failed to initialize submodule"
        exit 1
    fi

    print_color "$YELLOW" "Creating commit..."
    git add .gitmodules "$SPECIFYTEST_DIR"
    git commit -m "Add specifytest submodule

- Added specification-driven development framework
- Includes templates, scripts, and constitution
- Repository: $SPECIFYTEST_REPO"

    print_color "$GREEN" "✓ Commit created"
}

# Function to display post-installation instructions
show_instructions() {
    echo
    print_color "$GREEN" "=========================================="
    print_color "$GREEN" " Specifytest Installation Complete!"
    print_color "$GREEN" "=========================================="
    echo
    echo "Next steps:"
    echo "1. Review the constitution: cat .specify/memory/constitution.md"
    echo "2. Check available templates: ls .specify/templates/"
    echo "3. Run staleness check: .specify/scripts/check-staleness.sh"
    echo
    echo "To update specifytest in the future:"
    echo "  cd .specify && git pull origin main && cd .. && git add .specify && git commit -m 'Update specifytest'"
    echo
    echo "For more information, see: https://github.com/kjsdesigns/specifytest"
}

# Main execution
main() {
    print_color "$GREEN" "Specifytest Installation Script"
    print_color "$GREEN" "============================"
    echo

    while [[ $# -gt 0 ]]; do
        case $1 in
            --repo)
                SPECIFYTEST_REPO="$2"
                shift 2
                ;;
            --dir)
                SPECIFYTEST_DIR="$2"
                shift 2
                ;;
            --help|-h)
                echo "Usage: $0 [options]"
                echo "Options:"
                echo "  --repo URL    Specify custom repository URL"
                echo "  --dir PATH    Specify custom installation directory (default: .specify)"
                echo "  --help        Show this help message"
                exit 0
                ;;
            *)
                print_color "$RED" "Unknown option: $1"
                echo "Use --help for usage information"
                exit 1
                ;;
        esac
    done

    check_prerequisites
    install_specifytest
    show_instructions
}

main "$@"