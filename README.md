# Specifytest

A comprehensive specification-driven development framework with timestamp-based versioning for tracking specification changes and implementation staleness.

## Overview

Specifytest provides templates, scripts, and governance for implementing specification-driven development in any project. It uses simple ISO 8601 timestamps to track changes and detect when implementations become outdated.

## Installation

### As a Git Submodule (Recommended)

Add specifytest to your project as a submodule at `.specify/`:

```bash
git submodule add https://github.com/kjsdesigns/specifytest.git .specify
git submodule update --init --recursive
git commit -m "Add specifytest framework"
```

Or use the installation script:

```bash
curl -sSL https://raw.githubusercontent.com/kjsdesigns/specifytest/main/install.sh | bash
```

## Repository Structure

```
/
├── memory/
│   └── constitution.md         # Framework principles and governance
├── scripts/
│   ├── check-staleness.sh      # Detect outdated implementations
│   ├── check-staleness.py      # Python version with reports
│   ├── validate-specs.py       # Validate spec compliance
│   ├── generate-test-stub.py   # Generate test stubs from cases
│   └── bash/                   # Bash helper scripts
├── templates/
│   ├── components/             # Reusable template components
│   ├── spec-test-case.yaml     # Test case template
│   ├── spec-scenario-case.yaml # Scenario template
│   ├── spec-precondition-case.yaml # Precondition template
│   ├── spec-workflow.md        # Workflow specs
│   ├── spec-page.md            # Page/UI specs
│   ├── spec-concept.md         # Domain concept specs
│   ├── spec-data.md            # Data model specs
│   ├── spec-contract.md        # API contract specs
│   ├── spec-integration.md     # Integration specs
│   ├── spec-security.md        # Security specs
│   ├── spec-config.md          # Configuration specs
│   ├── spec-technology.md      # Technology decision specs
│   ├── spec-event.md           # Event specs
│   ├── spec-message.md         # Message specs
│   ├── plan-template.md        # Execution plan template
│   └── tasks-template.md       # Tasks template
├── commands/
│   ├── specify.md              # /specify command for Claude Code
│   ├── constitution.md         # /constitution command
│   ├── plan.md                 # /plan command
│   ├── tasks.md                # /tasks command
│   ├── implement.md            # /implement command
│   ├── analyze.md              # /analyze command
│   └── clarify.md              # /clarify command
├── install.sh                  # Installation helper
└── README.md                   # This file
```

## Key Features

- **Timestamp-Based Versioning**: Simple ISO 8601 timestamps track changes
- **14 Specification Types**: Templates for all aspects of development
- **Automatic Staleness Detection**: Know when implementations are outdated
- **Constitution-Based Governance**: Enforced principles and standards
- **Test-Driven Development**: Cases as standalone, versioned artifacts
- **Claude Code Integration**: Custom commands for AI-assisted development
- **No Special Tools Required**: Any editor can update timestamps

## Quick Start

### 1. Install in Your Project

```bash
cd your-project
git submodule add https://github.com/kjsdesigns/specifytest.git .specify
```

### 2. Link Commands for Claude Code (Optional)

If you're using Claude Code, create symlinks so the commands are available:

```bash
mkdir -p .claude/commands
cd .claude/commands
ln -s ../../.specify/commands/specify.md specify.md
ln -s ../../.specify/commands/constitution.md constitution.md
ln -s ../../.specify/commands/plan.md plan.md
ln -s ../../.specify/commands/tasks.md tasks.md
ln -s ../../.specify/commands/implement.md implement.md
ln -s ../../.specify/commands/analyze.md analyze.md
ln -s ../../.specify/commands/clarify.md clarify.md
cd ../..
```

Or use a loop to link all commands:

```bash
mkdir -p .claude/commands
for cmd in .specify/commands/*.md; do
  ln -s "../../$cmd" ".claude/commands/$(basename "$cmd")"
done
```

### 3. Create Your First Spec

```bash
# Create specs directory
mkdir -p specs/test-cases

# Copy template
cp .specify/templates/spec-test-case.yaml specs/test-cases/TC-001.yaml

# Edit with your test details
# Remember to update hash_timestamp to current UTC time
```

### 4. Run Staleness Check

```bash
.specify/scripts/check-staleness.sh
```

## Usage in Projects

Once installed as `.specify/`, the framework provides:

- **Templates**: Access via `.specify/templates/`
- **Scripts**: Run via `.specify/scripts/`
- **Constitution**: Review at `.specify/memory/constitution.md`
- **Commands**: Symlinked to `.claude/commands/` for Claude Code users (if set up during installation)

### Example: Creating a Test Case

```yaml
# specs/test-cases/TC-001.yaml
id: TC-001
name: user-login-valid-credentials
hash_timestamp: 2024-09-26T15:30:00Z  # Update on every save!

purpose: Verify users can login with valid credentials

preconditions:
  - /specs/precondition-cases/PC-001.yaml  # Database with test users

steps:
  - step: 1
    action: Navigate to login page
    expected: Login form is displayed

  - step: 2
    action: Enter valid username and password
    expected: Credentials are accepted

  - step: 3
    action: Click login button
    expected: User is redirected to dashboard

validations:
  - User session is created
  - Dashboard shows user data
  - Login timestamp is recorded

pass_criteria:
  - All validations pass
  - No error messages shown
```

### Example: Implementing with Timestamp Reference

```python
# tests/test_auth.py
def test_user_login_valid_credentials():
    """
    Implements: /specs/test-cases/TC-001.yaml
    Case Timestamp: 2024-09-26T15:30:00Z
    """
    # Test implementation here
    pass
```

When the spec changes, update its `hash_timestamp`. The staleness checker will automatically detect that this implementation is outdated.

## Updating Specifytest

To get the latest version:

```bash
cd .specify
git pull origin main
cd ..
git add .specify
git commit -m "Update specifytest framework"
```

## Constitution Principles

The framework enforces 9 core principles (see `.specify/memory/constitution.md`):

1. **Test-Driven Development** - Write cases first
2. **Standalone Case Architecture** - Cases are independent files
3. **Independent Identifier Standards** - Consistent ID patterns
4. **Complete Case Documentation** - All required fields
5. **Specs Reference Cases by Path** - File path references
6. **Mandatory Template Usage** - Use provided templates
7. **Plans Track Git State** - Git SHA in plans
8. **Implementation Timestamp References** - Track what you implement
9. **Timestamp-Only Versioning** - Simple timestamp comparison

## For Claude Code Users

If using Claude Code, the framework includes custom slash commands:

- `/specify [requirements]` - Create specs from requirements
- `/constitution` - Update constitution
- `/plan` - Create implementation plan
- `/tasks` - Generate task list
- `/implement` - Execute tasks
- `/analyze` - Analyze consistency
- `/clarify` - Ask clarification questions

## Contributing

Contributions welcome! To contribute:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test in a real project
5. Submit a pull request

## License

[Specify your license]

## Support

- **Issues**: https://github.com/kjsdesigns/specifytest/issues
- **Documentation**: See `.specify/memory/constitution.md` after installation

## Author

Specification-Driven Development framework maintained by Keith Seim.