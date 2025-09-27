
# Specification-Driven Development Constitution

## Core Principles

**Important Clarification**: Test Cases, Scenario Cases, and Precondition Cases
ARE specifications (specs), not separate from specs. They are specialized types
of specifications focused on validation and testing. All spec-* templates in
`.specify/templates/` define different types of specifications.

### I. Test-Driven Development (NON-NEGOTIABLE)
Development begins by authoring Test Cases, Scenario Cases, and Precondition Cases
as standalone specifications in their dedicated directories. The workflow enforces:
First define all Cases in `/specs/test-cases/`, `/specs/scenario-cases/`, and
`/specs/precondition-cases/` with automatic timestamp tracking on save. Then create
plans under `/plans/` capturing the Git commit SHA and listing all Cases that
must be developed, tested, and passed. Then create tasks referencing spec files
by relative paths. Implementation follows only after Cases are defined, with
timestamp references proving test-first development. Red-Green-Refactor cycles
proceed with Cases written first (generating initial timestamps), tests failing
initially, then implemented to pass while preserving temporal alignment.

### II. Standalone Case Architecture with Timestamp Tracking
All Test Cases, Scenario Cases, and Precondition Cases MUST be defined as
standalone specification artifacts in dedicated directories with automatic timestamp tracking.
No Test, Scenario, or Precondition Case may be defined inline within another spec file.
Each Case is an independent specification with its own ID and hash_timestamp field
that MUST be updated to the current ISO 8601 timestamp whenever the file is
modified and saved. Specs reference Cases by relative file paths (e.g.,
`/specs/test-cases/TC-001.yaml`), enabling agent navigation while timestamp changes
signal specification updates. This architecture ensures simple change detection
through timestamp comparison, independent versioning, and clean traceability
across the entire system.

### III. Independent Identifier Standards
All identifiers must conform to consistent patterns with stable IDs and single prefixes:
- Specs: Type prefix + number (W-001, P-012, UI-003, INT-204, DATA-015, SEC-008, EVENT-001, MESSAGE-001)
- Test Cases: TC prefix + number (TC-001, TC-002, TC-003)
- Scenario Cases: SC prefix + number (SC-001, SC-002, SC-003)
- Precondition Cases: PC prefix + number (PC-001, PC-002, PC-003)

**Single Prefix Rule:** Each spec type has exactly one prefix. No spec type may have multiple prefixes.

**File Extension Standards:**
- Test Cases, Scenario Cases, and Precondition Cases MUST use `.yaml` extension only
- All other spec types (Workflows, Pages, UI Components, etc.) MUST use `.md` extension only
- The `.yml` extension is not permitted and will fail validation

IDs remain stable across updates while the hash_timestamp field tracks when
changes occurred. Human-readable names use kebab-case alongside IDs. File paths
follow pattern: `/[case-type]/[ID].yaml` for Cases and `/[spec-type]/[ID].md` for other specs.
All references to Cases MUST use full file paths (e.g., `/specs/test-cases/TC-001.yaml`).
Invalid IDs, missing timestamps, wrong file extensions, or non-path references must block
in enforce mode with actionable error messages.

### IV. Complete Case Documentation
Every Test Case MUST include: id, name, hash_timestamp (ISO 8601 datetime),
purpose, preconditions (file paths to PC files), steps, validations, teardown,
inputs, expected_outputs, environment, and pass_criteria fields. Scenario Cases
MUST specify: id, name, hash_timestamp, purpose, phases (containing phase_id,
phase_name, description, preconditions array, test_cases array), phase_execution
(mode, continue_on_failure), timeout, and cache_strategy. Each phase organizes
preconditions and test_cases with descriptive labels for better readability and
execution tracking. Precondition Cases MUST document: id, name, hash_timestamp,
purpose, setup_steps, context_provided, validation_checks, teardown_procedures,
compatibility, cache_strategy, and resources_touched. The hash_timestamp MUST
be updated to current UTC time whenever the Case file is modified and saved.

### V. Specs Reference Cases by Path
Specifications contain requirements and design decisions, while referencing
validation Cases by absolute file paths from repository root. Each spec artifact
MUST contain a `validation_cases` section listing all Test Case paths (e.g.,
`/specs/test-cases/TC-001.yaml`) and Scenario Case paths that validate its assertions.
This enables agents to navigate directly to Case files while timestamps detect
changes. Test and Scenario Cases reference Precondition Cases by absolute file
paths. Non-case specs (workflows, pages, UI components, etc.) MUST NOT reference
Precondition Cases directly - only Test Cases and Scenario Cases should reference
Precondition Cases. Precondition Cases are standalone and do not reference other
artifacts, ensuring they remain reusable setup/teardown components.

### VI. Mandatory Template Usage (NON-NEGOTIABLE)
All specifications, Cases, plans, and tasks MUST use the exact templates provided
in `.specify/templates/`. Templates define required sections including hash_timestamp
field, field structures, and validation rules. When generating new Test Cases,
Scenario Cases, Precondition Cases, plans, or tasks, always load and apply the
appropriate template from `.specify/templates/`. Templates specify timestamp format
and file path references. Missing required fields or deviating from template
structure constitutes a constitution violation that blocks in enforce mode.

### VII. Plans Track Git State and Tasks Reference Paths
Plans MUST live under `/plans/` and capture the Git commit SHA at plan creation.
Each plan MUST list all Test Cases, Scenario Cases, and Precondition Cases by
file path that need to be developed, tested, and passed. The git_commit_sha field
provides an immutable reference point for change detection. Tasks within plans
MUST reference spec files by relative paths (e.g., `/specs/workflows/W-001/spec.md`)
and list the Case file paths they implement or validate. This enables precise
navigation and change tracking without manual versioning.

### VIII. Implementation Timestamp References
Implementation files (test files, source code) MUST include timestamp references
to their source specifications. Test implementations embed only the hash_timestamp
of Cases they implement as comments or metadata. When a Case's hash_timestamp
changes (is newer than the implementation's reference), the implementation is
automatically flagged as stale. This creates simple bidirectional traceability:
Cases know when they were last modified, implementations know which timestamp
version they implement, and timestamp comparison triggers update requirements.
No complex hashing or checksums are required - just timestamp comparison.

### IX. Timestamp-Only Versioning (NON-NEGOTIABLE)
The system operates through timestamp tracking rather than content hashing or
manual version numbers. Every Case file includes a hash_timestamp field in ISO
8601 format (YYYY-MM-DDTHH:MM:SSZ) that MUST be updated whenever the file is
saved with modifications. Implementation files reference ONLY this timestamp,
not any hash values. Change detection occurs by simple timestamp comparison:
if Case timestamp > implementation timestamp reference, the implementation is
stale. This eliminates complexity of hash computation, reduces maintenance
burden, and provides clear temporal understanding of changes. The rule is
simple: whenever a Case file is modified and saved, update its hash_timestamp
to the current UTC time.

## Architectural Standards

### Directory Structure and Locations

All Cases MUST be organized in dedicated directories at the repository root:

```
/specs/
├── test-cases/           # All Test Case artifacts with timestamps
│   ├── TC-001.yaml       # hash_timestamp: 2024-01-15T10:30:00Z
│   ├── TC-002.yaml       # hash_timestamp: 2024-01-15T10:31:00Z
│   └── TC-003.yaml       # hash_timestamp: 2024-01-15T10:32:00Z
├── scenario-cases/       # All Scenario Case artifacts with timestamps
│   ├── SC-001.yaml       # hash_timestamp: 2024-01-15T11:00:00Z
│   ├── SC-002.yaml       # hash_timestamp: 2024-01-15T11:05:00Z
│   └── SC-003.yaml       # hash_timestamp: 2024-01-15T11:10:00Z
├── precondition-cases/   # All Precondition Case artifacts with timestamps
│   ├── PC-001.yaml       # hash_timestamp: 2024-01-15T09:00:00Z
│   ├── PC-002.yaml       # hash_timestamp: 2024-01-15T09:05:00Z
│   └── PC-003.yaml       # hash_timestamp: 2024-01-15T09:10:00Z

├── workflows/        # Workflow specs (W-xxx)
├── pages/           # Page specs (P-xxx)
├── ui-components/   # UI Component specs (UI-xxx)
├── concepts/        # Concept specs (C-xxx)
├── integrations/    # Integration specs (INT-xxx)
├── data/            # Data specs (DATA-xxx)
├── security/        # Security specs (SEC-xxx)
├── technology/      # Technology specs (TECH-xxx)
├── configuration/   # Configuration specs (CONFIG-xxx)
├── contracts/       # Contract specs (CONTRACT-xxx)
├── events/          # Event specs (EVENT-xxx)
└── messages/        # Message specs (MESSAGE-xxx)

/plans/              # Execution plans with Git SHA tracking
├── plan-001/
│   ├── plan.md     # git_commit_sha: abc123..., plan_created: 2024-01-15T12:00:00Z
│   └── tasks.md    # References specs by file path with timestamps
└── plan-002/
    ├── plan.md     # git_commit_sha: def456..., plan_created: 2024-01-16T09:00:00Z
    └── tasks.md    # References specs by file path with timestamps
```

### Timestamp-Based Reference Model

**Specs reference Cases by file path:**
```yaml
# In /specs/workflows/W-001/spec.md
validation_cases:
  test_cases:
    - path: /specs/test-cases/TC-001.yaml  # Login with valid credentials
    - path: /specs/test-cases/TC-002.yaml  # Login with invalid password
    - path: /specs/test-cases/TC-003.yaml  # Login with non-existent user
  scenario_cases:
    - path: /specs/scenario-cases/SC-001.yaml  # Complete authentication flow
    - path: /specs/scenario-cases/SC-002.yaml  # Password reset journey
```

**Test Cases include only timestamp and reference paths:**
```yaml
# In /specs/test-cases/TC-001.yaml
id: TC-001
name: login-valid-credentials
hash_timestamp: 2024-01-15T10:30:00Z  # Updated on every save
preconditions:
  - /specs/precondition-cases/PC-001.yaml  # Database with test users
  - /specs/precondition-cases/PC-002.yaml  # Clean browser session
```

**Implementation files reference ONLY the timestamp:**
```python
# In tests/test_auth.py
def test_login_valid_credentials():
    """
    Implements: /specs/test-cases/TC-001.yaml
    Case Timestamp: 2024-01-15T10:30:00Z
    """
    # Test implementation
```

**Plans capture Git state with timestamp:**
```markdown
# In /plans/plan-001/plan.md
---
git_commit_sha: 8a9b0c1d2e3f4a5b6c7d8e9f0
plan_created: 2024-01-15T12:00:00Z
---
## Cases to Develop
### Test Cases
- /specs/test-cases/TC-001.yaml: Login with valid credentials
- /specs/test-cases/TC-002.yaml: Login with invalid password
```

**Tasks reference by path with timestamps only:**
```markdown
# In /plans/plan-001/tasks.md
## Task 001: Implement authentication test cases
- Validates Spec: /specs/workflows/W-001/spec.md
- Implements Cases:
  - /specs/test-cases/TC-001.yaml (timestamp: 2024-01-15T10:30:00Z)
  - /specs/test-cases/TC-002.yaml (timestamp: 2024-01-15T10:31:00Z)
- Uses Preconditions:
  - /specs/precondition-cases/PC-001.yaml
  - /specs/precondition-cases/PC-002.yaml
- File: tests/test_auth.py
```

### Timestamp Update Rules

**When to Update hash_timestamp:**
1. Any modification to Case file content (except the timestamp itself)
2. Manual save action by developer or tool
3. Automated saves from editors or IDEs
4. Git hooks on pre-commit (optional)

**Timestamp Format:**
- MUST be ISO 8601 UTC format: YYYY-MM-DDTHH:MM:SSZ
- Example: 2024-01-15T10:30:00Z
- Always use UTC (Z suffix) to avoid timezone issues

## Development Workflow

### TDD Flow with Timestamp Tracking

1. **Author Cases with Initial Timestamps**
   - Create Test Cases in `/specs/test-cases/` with current timestamp
   - Create Scenario Cases in `/specs/scenario-cases/` with current timestamp
   - Create Precondition Cases in `/specs/precondition-cases/` with current timestamp
   - Set hash_timestamp to current UTC time on creation

2. **Update Specifications with Paths**
   - Add Case file paths to `validation_cases` section
   - Specs reference `/specs/test-cases/TC-001.yaml` not just TC-001
   - Enables direct navigation by agents and tools

3. **Create Plan with Git SHA and Timestamp**
   - Create plan under `/plans/[plan-name]/plan.md`
   - Capture current git_commit_sha in plan header
   - Record plan_created timestamp
   - List all Case file paths needing implementation

4. **Define Tasks with Path and Timestamp References**
   - Create tasks in `/plans/[plan-name]/tasks.md`
   - Reference spec files by path: `/specs/workflows/W-001/spec.md`
   - List Case file paths with their current timestamps
   - Include target implementation file paths

5. **Execute with Timestamp Verification**
   - Implement Cases following Red-Green-Refactor
   - Embed Case timestamp in implementation files
   - Tests fail initially (Red) with timestamp reference
   - Implementation makes tests pass (Green) preserving timestamp
   - Refactor while maintaining timestamp alignment

6. **Detect Changes via Simple Timestamp Comparison**
   - When Case is modified, hash_timestamp updates to current time
   - Implementation with older timestamp automatically flagged
   - No complex hashing or checksumming needed
   - Changes detected by simple date comparison

### Change Detection Workflow

**Specification Changes:**
1. Modify Case YAML file
2. Update hash_timestamp to current UTC time
3. Save file
4. Implementations referencing older timestamp become stale
5. CI/CD detects timestamp mismatches
6. Triggers update workflow

**Implementation Sync:**
1. Read Case file and extract hash_timestamp
2. Read implementation file and extract referenced timestamp
3. Compare timestamps
4. If Case timestamp > implementation timestamp: stale
5. Update implementation
6. Update timestamp reference in implementation
7. Commit with both files in sync

**Staleness Detection (Simplified):**
```python
# Pseudo-code for staleness detection
case_timestamp = parse_iso8601(case_yaml['hash_timestamp'])
impl_timestamp = parse_iso8601(extract_timestamp_from_implementation(impl_file))

if case_timestamp > impl_timestamp:
    days_stale = (case_timestamp - impl_timestamp).days
    flag_as_stale(impl_file, case_file, days_stale)
```

## Quality Standards

### Timestamp Integrity Requirements
- All Cases MUST have valid hash_timestamp in ISO 8601 format (UTC)
- Timestamp MUST be updated when file content changes
- Implementation files MUST reference Case timestamps
- Timestamp mismatches MUST trigger staleness warnings
- Plans MUST capture valid git_commit_sha and plan_created timestamp

### Path Reference Standards
- All Case references use absolute paths from repo root
- Paths must resolve to existing files
- Format: `/[directory]/[ID].yaml`
- No relative paths (../), only absolute (/specs/test-cases/)
- Broken path references block in enforce mode

### Validation at Sync
- Verify all hash_timestamp fields are valid ISO 8601
- Check implementation timestamp references match Cases
- Validate all file paths resolve correctly
- Ensure git_commit_sha in plans is valid
- Ensure plan_created timestamp is present and valid
- Flag any timestamp mismatches for update

### Enforcement Modes
- **Report Mode**: Log timestamp mismatches, allow continuation
- **Enforce Mode**: Block on timestamp mismatches, require sync
- Invalid timestamps must block with clear error messages
- Missing timestamp fields must prevent Case creation
- Broken path references must block execution
- Timestamps in non-ISO 8601 format must be rejected

## Template Enforcement

### Required Templates with Timestamp Support

All artifacts MUST use templates from `.specify/templates/` with timestamp fields:

| Artifact Type | Template File | Required Fields |
|--------------|---------------|-----------------|
| **Test Case** | spec-test-case.yaml | hash_timestamp (ISO 8601) |
| **Scenario Case** | spec-scenario-case.yaml | hash_timestamp (ISO 8601) |
| **Precondition Case** | spec-precondition-case.yaml | hash_timestamp (ISO 8601) |
| **Plan** | plan-template.md | git_commit_sha (from git), plan_created (ISO 8601) |
| **Tasks** | tasks-template.md | Case paths with timestamps |

### Template Validation Rules

- **T-TPL1.** All Cases MUST include hash_timestamp in ISO 8601 format
- **T-TPL2.** Plans MUST capture git_commit_sha and plan_created timestamp
- **T-TPL3.** Tasks MUST reference specs and Cases by file path with timestamps
- **T-TPL4.** Implementation files MUST include timestamp comments only
- **T-TPL5.** Path references MUST be absolute from repo root
- **T-TPL6.** Timestamp MUST update on every content modification
- **T-TPL7.** Git SHA and timestamps MUST be captured at plan creation
- **T-TPL8.** All path references MUST resolve to existing files
- **T-TPL9.** Timestamp format MUST be ISO 8601 UTC (YYYY-MM-DDTHH:MM:SSZ)

## Timestamp-Based Governance

The constitution enforces simple specification tracking through timestamp
comparison rather than complex hashing or manual versioning. All tools,
specifications, Cases, plans, and tasks must conform to timestamp-based
change detection. Enforcement happens through:
- Automatic timestamp update on file save
- Git SHA capture for plan baselines with creation timestamps
- File path references for navigation
- Timestamp embedding in implementations
- Simple date comparison for staleness detection
- Prioritization based on staleness age

Benefits of timestamp-only approach:
- **Simple**: Just compare timestamps, no complex hashing
- **Automatic**: Timestamps update on save
- **Transparent**: Clear when changes occurred
- **Maintainable**: No special scripts or tools needed
- **Navigable**: Direct file paths for agents
- **Verifiable**: Simple date comparison detects changes
- **Temporal**: Understand when changes occurred and staleness duration
- **Prioritizable**: Address oldest stale implementations first

Amendment procedure requires:
- Document change rationale and impact
- Update timestamp rules if needed
- Migrate existing Cases to remove content_hash fields
- Update all affected templates
- Version increment following semantic versioning

Templates are mandatory and located at `.specify/templates/`.
All artifacts must adopt templates exactly, including timestamp format and path
reference formats.

## Clarifying Questions

### MANDATORY Format Requirements
ALL clarifying questions MUST follow this EXACT format. Every rule listed below is mandatory and must be followed precisely:

**Required Format Rules:**
1. Question number followed by period and single space
2. Question text ending with question mark
3. EXACTLY 3 spaces of indentation before each letter option
4. Letter (lowercase) followed by closing parenthesis, single space, then option text
5. `(recommended)` indicator added after option text where applicable
6. EXACTLY one blank line between questions (two consecutive newlines)
7. No additional formatting, bullets, or deviations

**Correct Format Template:**
```
1. [Question text]?
   a) [Option 1]
   b) [Option 2] (recommended)
   c) [Option 3]


2. [Next question]?
   a) [Option 1]
   b) [Option 2]
```

**Complete Example:**
```
1. What is your preferred approach?
   a) Option A
   b) Option B (recommended)
   c) Option C


2. How should this be handled?
   a) Approach one
   b) Approach two
```

This format allows users to respond concisely (e.g., "1a, 2b") while maintaining
clarity about available options. The number of options per question should match
the context - use as many or as few as needed.

**CRITICAL:** Deviation from this format is not permitted. Always verify formatting includes exact indentation (3 spaces) and double line breaks between questions.

## Specification Filename Standards

### XII. Mandatory Filename Pattern

**Validation Rules:** All validation rules are defined in `.specify/schemas/template-schema.json`

**Spec Types and Prefixes:** See `.specify/schemas/type-registry.yaml` for the complete list of spec types, their prefixes, naming guidelines, and examples.

All specification files MUST follow the exact pattern:
```
[PREFIX]-[NUMBER]-[descriptive-name].[ext]
```

Where:
- `[PREFIX]` = Spec type prefix (W, CON, TC, etc.)
- `[NUMBER]` = Three-digit sequential number (001, 002, 099, 100)
- `[descriptive-name]` = Snake_case descriptive name (1-4 words)
- `[ext]` = File extension (.yaml for cases, .md for other specs)

**Examples:**
- `W-001-user_registration.md` (Workflow)
- `TC-042-validate_password.yaml` (Test Case)
- `CON-003-user_account.md` (Concept)
- `DATA-015-order_schema.md` (Data)

### Cross-Reference Format
When specs reference other specs, use format:
```
[ID] [Descriptive Name with Title Case]
```

Examples:
- `W-001 User Registration`
- `TC-042 Validate Password`
- `CON-003 User Account`

### Deprecation Handling
Deprecated specs MUST be moved to `deprecated/` subdirectory within their type directory:
```
/specs/workflows/deprecated/W-005-old_login.md
/specs/concepts/deprecated/CON-010-legacy_user.md
```

Status field MUST be set to `deprecated` and file moved to deprecated subdirectory.

## UI Component Specifications

### X. UI Component Architecture
UI Components are reusable interface elements that can be embedded within Pages
or other UI Components. UI Components MUST be defined as standalone specification
artifacts in `/specs/ui-components/` with identifier pattern `UI-XXX`. Each UI
Component specification MUST include hash_timestamp tracking like all other specs.

**Key Principles:**
- **Standalone Specs**: UI Components have their own spec files with full documentation
- **Nestable**: UI Components can reference other UI Components
- **Reusable**: Same UI Component can be embedded in multiple Pages
- **Props/Parameters**: UI Components define configurable props for customization
- **Test Inheritance**: Pages inherit test cases indirectly through embedded UI Components

### XI. Page and Component Structure Standards
Pages and UI Components MUST describe their structure from left-to-right,
top-to-bottom as users encounter elements. When embedding UI Components within
Pages or other UI Components, reference by absolute path and provide context
about what object or data the component represents.

**Structure Reference Format:**
```markdown
### Elements
- **User Profile Card**: `/specs/ui-components/UI-001.md` (displays current user's profile)
- **Action Button**: Primary "Save Changes" button
- **Notification List**: `/specs/ui-components/UI-012.md` (shows user's unread notifications)
```

### XII. Test Case Inheritance Model
When a Page embeds a UI Component, the Page indirectly inherits all Test Cases
and Scenario Cases referenced by that UI Component. Pages MUST NOT duplicate
these inherited test references in their own validation_cases section. Only list
test cases that directly validate the Page's unique functionality beyond its
embedded components.

Test Cases and Scenario Cases SHOULD include conditions describing when they
apply. This allows inherited cases to be evaluated in the context of the embedding
Page without requiring explicit selective inheritance mechanisms.

**Version**: 7.0.0 | **Ratified**: 2025-09-25 | **Last Amended**: 2025-09-27