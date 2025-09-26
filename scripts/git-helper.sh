#!/usr/bin/env bash
#
# Git Helper Script - Abstraction layer for git operations
# Provides fallback behavior for non-git environments
#
# Usage: source git-helper.sh

set -e

# Check if we're in a git repository
is_git_repo() {
    git rev-parse --git-dir >/dev/null 2>&1 && echo "true" || echo "false"
}

# Get current branch name or return a default
get_current_branch() {
    if [[ "$(is_git_repo)" == "true" ]]; then
        git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "main"
    else
        echo "no-git"
    fi
}

# Get current commit SHA or return a placeholder
get_commit_sha() {
    if [[ "$(is_git_repo)" == "true" ]]; then
        git rev-parse HEAD 2>/dev/null || echo "0000000000000000000000000000000000000000"
    else
        # Return a timestamp-based identifier for non-git projects
        echo "no-git-$(date +%Y%m%d%H%M%S)"
    fi
}

# Check if working directory is clean
is_working_dir_clean() {
    if [[ "$(is_git_repo)" == "true" ]]; then
        if [[ -z "$(git status --porcelain 2>/dev/null)" ]]; then
            echo "true"
        else
            echo "false"
        fi
    else
        # Always return true for non-git projects
        echo "true"
    fi
}

# Get repository root directory
get_repo_root() {
    if [[ "$(is_git_repo)" == "true" ]]; then
        git rev-parse --show-toplevel 2>/dev/null || pwd
    else
        # For non-git projects, find .specify directory and use its parent
        local current="$PWD"
        while [[ "$current" != "/" ]]; do
            if [[ -d "$current/.specify" ]]; then
                echo "$current"
                return
            fi
            current="$(dirname "$current")"
        done
        # Default to current directory if no .specify found
        pwd
    fi
}

# Safe git add (no-op for non-git)
safe_git_add() {
    if [[ "$(is_git_repo)" == "true" ]]; then
        git add "$@" 2>/dev/null || true
    fi
}

# Safe git commit (no-op for non-git)
safe_git_commit() {
    if [[ "$(is_git_repo)" == "true" ]]; then
        git commit "$@" 2>/dev/null || true
    fi
}

# Check if a branch exists
branch_exists() {
    local branch="$1"
    if [[ "$(is_git_repo)" == "true" ]]; then
        git show-ref --verify --quiet "refs/heads/$branch" && echo "true" || echo "false"
    else
        echo "false"
    fi
}

# Create a new branch (no-op for non-git)
create_branch() {
    local branch="$1"
    if [[ "$(is_git_repo)" == "true" ]]; then
        git checkout -b "$branch" 2>/dev/null || {
            echo "Warning: Could not create branch $branch" >&2
            return 1
        }
    fi
}

# Export common variables
export GIT_IS_REPO="$(is_git_repo)"
export GIT_CURRENT_BRANCH="$(get_current_branch)"
export GIT_COMMIT_SHA="$(get_commit_sha)"
export GIT_REPO_ROOT="$(get_repo_root)"
export GIT_WORKING_CLEAN="$(is_working_dir_clean)"

# Provide informative output if sourced directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    echo "Git Helper Information:"
    echo "  Repository: $GIT_IS_REPO"
    echo "  Root: $GIT_REPO_ROOT"
    echo "  Branch: $GIT_CURRENT_BRANCH"
    echo "  Commit: $GIT_COMMIT_SHA"
    echo "  Clean: $GIT_WORKING_CLEAN"
fi