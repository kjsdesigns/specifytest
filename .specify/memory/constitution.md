<!-- Sync Impact Report
Version Change: 5.0.0 → 5.1.0 (MINOR: Added datetime stamps to hash versioning)
Modified Principles:
  - Principle IV: Added hash_timestamp field requirement
  - Principle IX: Enhanced with datetime stamp tracking
Modified Sections:
  - Hash-Based Reference Model: Added hash_timestamp examples
  - Hash Computation Rules: Added timestamp capture
  - Quality Standards: Added timestamp validation
  - Template Enforcement: Added hash_timestamp to required fields
Templates Requiring Updates:
  ⚠ test-case-template.yaml needs hash_timestamp field
  ⚠ scenario-case-template.yaml needs hash_timestamp field
  ⚠ precondition-case-template.yaml needs hash_timestamp field
  ✅ plan-template.md already has datetime support
  ✅ tasks-template.md compatible with timestamps
Follow-up TODOs:
  - Update Case templates to include hash_timestamp
  - Update /specify command for timestamp generation
  - Update hash computation tools to add timestamps
-->

# Specification-Driven Development Constitution

## Core Principles

### I. Test-Driven Development (NON-NEGOTIABLE)
Development begins by authoring Test Cases, Scenario Cases, and Precondition Cases
as standalone artifacts in their dedicated directories. The workflow enforces:
First define all Cases in `/test-cases/`, `/scenario-cases/`, and
`/precondition-cases/` with automatic content hashing and timestamp tracking. Then
create plans under `/plans/` capturing the Git commit SHA and listing all Cases
that must be developed, tested, and passed. Then create tasks referencing spec
files by relative paths. Implementation follows only after Cases are defined, with
hash references and timestamps proving test-first development. Red-Green-Refactor
cycles proceed with Cases written first (generating initial hashes with timestamps),
tests failing initially, then implemented to pass while preserving hash integrity.

### II. Standalone Case Architecture
All Test Cases, Scenario Cases, and Precondition Cases MUST be defined as
standalone artifacts in dedicated directories with automatic content hashing and
timestamp tracking. No Test, Scenario, or Precondition Case may be defined inline
within a spec file. Each Case is an independent artifact with its own ID,
content_hash computed from its YAML content, and hash_timestamp recording when the
hash was generated. Specs reference Cases by relative file paths (e.g.,
`/test-cases/TC-001.yaml`), enabling agent navigation while hash changes and
timestamps signal specification updates. This architecture ensures stateless change
detection with temporal tracking, independent versioning, and clean traceability
across the entire system.

### III. Independent Identifier Standards
All identifiers must conform to consistent patterns with stable IDs:
- Specs: Type prefix + number (W-001, P-012, INT-204, DATA-015, SEC-008)
- Test Cases: TC prefix + number (TC-001, TC-002, TC-003)
- Scenario Cases: SC prefix + number (SC-001, SC-002, SC-003)
- Precondition Cases: PC prefix + number (PC-001, PC-002, PC-003)
IDs remain stable across updates while content_hash and hash_timestamp fields track
changes and their timing. Human-readable names use kebab-case alongside IDs. File
paths follow pattern: `/[case-type]/[ID].yaml` for direct navigation. Invalid IDs,
missing hash fields, or missing timestamps must block in enforce mode with
actionable error messages.

### IV. Complete Case Documentation
Every Test Case MUST include: id, name, content_hash (auto-computed), hash_timestamp
(ISO 8601 datetime), purpose, preconditions (file paths to PC files), steps,
validations, teardown, inputs, expected_outputs, environment, and pass_criteria
fields. Scenario Cases MUST specify: id, name, content_hash, hash_timestamp, purpose,
test_cases (file paths to TC files), preconditions (file paths to PC files),
nested_scenarios (file paths to SC files), timeout, and cache_strategy. Precondition
Cases MUST document: id, name, content_hash, hash_timestamp, purpose, setup_steps,
context_provided, validation_checks, teardown_procedures, compatibility,
cache_strategy, and resources_touched. Each content_hash is SHA-256 of the canonical
YAML representation excluding the hash and timestamp fields themselves.

### V. Specs Reference Cases by Path
Specifications contain requirements and design decisions, while referencing
validation Cases by relative file paths. Each spec artifact MUST contain a
`validation_cases` section listing all Test Case paths (e.g.,
`/test-cases/TC-001.yaml`) and Scenario Case paths that validate its assertions.
This enables agents to navigate directly to Case files while content hashes and
timestamps detect changes. Test and Scenario Cases reference Precondition Cases by
file paths. Precondition Cases are standalone and do not reference other artifacts,
ensuring they remain reusable setup/teardown components.

### VI. Mandatory Template Usage (NON-NEGOTIABLE)
All specifications, Cases, plans, and tasks MUST use the exact templates provided
in `/Users/keith/claude/specifytest/.specify/templates/`. Templates define required
sections including content_hash computation, hash_timestamp generation, field
structures, and validation rules. When generating new Test Cases, Scenario Cases,
Precondition Cases, plans, or tasks, always load and apply the appropriate template
from `.specify/templates/`. Templates specify how to compute content hashes, generate
timestamps, and format file path references. Missing required fields or deviating
from template structure constitutes a constitution violation that blocks in enforce
mode.

### VII. Plans Track Git State and Tasks Reference Paths
Plans MUST live under `/plans/` and capture the Git commit SHA at plan creation.
Each plan MUST list all Test Cases, Scenario Cases, and Precondition Cases by
file path that need to be developed, tested, and passed. The git_commit_sha field
provides an immutable reference point for change detection. Tasks within plans
MUST reference spec files by relative paths (e.g., `/specs/workflows/W-001/spec.md`)
and list the Case file paths they implement or validate. This enables precise
navigation and change tracking without manual versioning.

### VIII. Implementation Hash References
Implementation files (test files, source code) MUST include hash references and
timestamps to their source specifications. Test implementations embed the content_hash
and hash_timestamp of Cases they implement as comments or metadata. When a Case's
content_hash changes, the implementation is automatically flagged as stale. Production
code includes spec content hashes with timestamps to track compliance. This creates
bidirectional traceability: Cases know their current hash and when generated,
implementations know which hash version and timestamp they implement, and mismatches
trigger update requirements.

### IX. Stateless Hash-Based Versioning with Timestamps (NON-NEGOTIABLE)
The system operates statelessly through content hashing with datetime stamps rather
than manual version tracking. Every Case file includes a content_hash field computed
as SHA-256 of its canonical YAML content (excluding the hash and timestamp fields)
and a hash_timestamp field in ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ) recording when
the hash was generated. Plans capture git_commit_sha at creation time, providing an
immutable baseline with temporal context. Tasks reference specs and Cases by file
paths for navigation while tracking hash timestamps. Implementation files include
hash comments with timestamps proving which specification version they implement and
when. Change detection occurs by comparing: Case content_hash in file vs hash
reference in implementation, with timestamps providing temporal context for changes.
No manual version numbers required. Hash mismatches with timestamp differences
automatically flag staleness and trigger update workflows.

## Architectural Standards

### Directory Structure and Locations

All Cases MUST be organized in dedicated directories at the repository root:

```
/test-cases/           # All Test Case artifacts with hashes and timestamps
├── TC-001.yaml       # content_hash: sha256..., hash_timestamp: 2024-01-15T10:30:00Z
├── TC-002.yaml       # content_hash: sha256..., hash_timestamp: 2024-01-15T10:31:00Z
└── TC-003.yaml       # content_hash: sha256..., hash_timestamp: 2024-01-15T10:32:00Z

/scenario-cases/       # All Scenario Case artifacts with hashes and timestamps
├── SC-001.yaml       # content_hash: sha256..., hash_timestamp: 2024-01-15T11:00:00Z
├── SC-002.yaml       # content_hash: sha256..., hash_timestamp: 2024-01-15T11:05:00Z
└── SC-003.yaml       # content_hash: sha256..., hash_timestamp: 2024-01-15T11:10:00Z

/precondition-cases/   # All Precondition Case artifacts with hashes and timestamps
├── PC-001.yaml       # content_hash: sha256..., hash_timestamp: 2024-01-15T09:00:00Z
├── PC-002.yaml       # content_hash: sha256..., hash_timestamp: 2024-01-15T09:05:00Z
└── PC-003.yaml       # content_hash: sha256..., hash_timestamp: 2024-01-15T09:10:00Z

/specs/               # Modular specifications referencing Cases by path
├── workflows/        # Workflow specs (W-xxx)
├── pages/           # Page specs (P-xxx)
├── concepts/        # Concept specs (C-xxx)
├── integrations/    # Integration specs (INT-xxx)
├── data/            # Data specs (DATA-xxx)
├── security/        # Security specs (SEC-xxx)
├── technology/      # Technology specs (TECH-xxx)
├── configuration/   # Configuration specs (CONFIG-xxx)
└── contracts/       # Contract specs (CONTRACT-xxx)

/plans/              # Execution plans with Git SHA tracking
├── plan-001/
│   ├── plan.md     # git_commit_sha: abc123..., plan_created: 2024-01-15T12:00:00Z
│   └── tasks.md    # References specs by file path with hash timestamps
└── plan-002/
    ├── plan.md     # git_commit_sha: def456..., plan_created: 2024-01-16T09:00:00Z
    └── tasks.md    # References specs by file path with hash timestamps
```

### Hash-Based Reference Model with Timestamps

**Specs reference Cases by file path:**
```yaml
# In /specs/workflows/W-001/spec.md
validation_cases:
  test_cases:
    - path: /test-cases/TC-001.yaml  # Login with valid credentials
    - path: /test-cases/TC-002.yaml  # Login with invalid password
    - path: /test-cases/TC-003.yaml  # Login with non-existent user
  scenario_cases:
    - path: /scenario-cases/SC-001.yaml  # Complete authentication flow
    - path: /scenario-cases/SC-002.yaml  # Password reset journey
```

**Test Cases include content hash with timestamp and reference paths:**
```yaml
# In /test-cases/TC-001.yaml
id: TC-001
name: login-valid-credentials
content_hash: sha256:a1b2c3d4e5f6...  # Auto-computed from YAML content
hash_timestamp: 2024-01-15T10:30:00Z  # When hash was generated
preconditions:
  - path: /precondition-cases/PC-001.yaml  # Database with test users
  - path: /precondition-cases/PC-002.yaml  # Clean browser session
```

**Implementation files reference source hashes with timestamps:**
```python
# In tests/test_auth.py
def test_login_valid_credentials():
    """
    Implements: /test-cases/TC-001.yaml
    Spec Hash: sha256:a1b2c3d4e5f6...
    Hash Timestamp: 2024-01-15T10:30:00Z
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
- /test-cases/TC-001.yaml: Login with valid credentials
- /test-cases/TC-002.yaml: Login with invalid password
```

**Tasks reference by path with hash timestamps:**
```markdown
# In /plans/plan-001/tasks.md
## Task 001: Implement authentication test cases
- Validates Spec: /specs/workflows/W-001/spec.md
- Implements Cases:
  - /test-cases/TC-001.yaml (hash: sha256:a1b2c3..., timestamp: 2024-01-15T10:30:00Z)
  - /test-cases/TC-002.yaml (hash: sha256:b2c3d4..., timestamp: 2024-01-15T10:31:00Z)
- Uses Preconditions:
  - /precondition-cases/PC-001.yaml
  - /precondition-cases/PC-002.yaml
- File: tests/test_auth.py
```

### Hash Computation Rules

**Content Hash Calculation with Timestamp:**
1. Load YAML file content
2. Parse to data structure
3. Remove content_hash and hash_timestamp fields if present
4. Serialize to canonical YAML format (sorted keys, consistent spacing)
5. Compute SHA-256 hash of canonical YAML
6. Generate ISO 8601 timestamp (UTC)
7. Store as content_hash and hash_timestamp fields in file

**Hash Sync Detection with Temporal Context:**
```python
# Pseudo-code for staleness detection with timestamps
case_hash = compute_hash(case_yaml)
case_timestamp = case_yaml['hash_timestamp']
impl_hash, impl_timestamp = extract_hash_and_timestamp_from_implementation(impl_file)

if case_hash != impl_hash:
    time_diff = parse_datetime(case_timestamp) - parse_datetime(impl_timestamp)
    flag_as_stale(impl_file, case_file, time_diff)
    require_update(f"Case updated {time_diff} after implementation")
```

**Git SHA and Timestamp Capture:**
```bash
# When creating a plan
git_sha=$(git rev-parse HEAD)
timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
echo "git_commit_sha: $git_sha" >> plan.md
echo "plan_created: $timestamp" >> plan.md
```

## Development Workflow

### TDD Flow with Hash and Timestamp Tracking

1. **Author Cases with Initial Hashes and Timestamps**
   - Create Test Cases in `/test-cases/` with auto-computed content_hash
   - Generate hash_timestamp in ISO 8601 format (UTC)
   - Create Scenario Cases in `/scenario-cases/` with hash and timestamp
   - Create Precondition Cases in `/precondition-cases/` with hash and timestamp
   - Templates automatically compute and insert both fields

2. **Update Specifications with Paths**
   - Add Case file paths to `validation_cases` section
   - Specs reference `/test-cases/TC-001.yaml` not just TC-001
   - Enables direct navigation by agents and tools

3. **Create Plan with Git SHA and Timestamp**
   - Create plan under `/plans/[plan-name]/plan.md`
   - Capture current git_commit_sha in plan header
   - Record plan_created timestamp
   - List all Case file paths needing implementation
   - Git SHA and timestamp provide immutable temporal baseline

4. **Define Tasks with Path and Timestamp References**
   - Create tasks in `/plans/[plan-name]/tasks.md`
   - Reference spec files by path: `/specs/workflows/W-001/spec.md`
   - List Case file paths with their current hashes and timestamps
   - Include target implementation file paths

5. **Execute with Hash and Timestamp Verification**
   - Implement Cases following Red-Green-Refactor
   - Embed source content_hash and hash_timestamp in implementation files
   - Tests fail initially (Red) with hash and timestamp reference
   - Implementation makes tests pass (Green) preserving hash integrity
   - Refactor while maintaining hash and timestamp alignment

6. **Detect Changes via Hash Comparison with Temporal Context**
   - When Case content changes, content_hash and hash_timestamp update
   - Implementation with old hash automatically flagged with time delta
   - No manual version tracking needed
   - Changes detected statelessly by hash mismatch with temporal awareness

### Change Detection Workflow

**Specification Changes:**
1. Modify Case YAML file
2. Recompute content_hash
3. Generate new hash_timestamp
4. Save with new hash and timestamp
5. Implementations referencing old hash become stale with time delta
6. CI/CD detects hash mismatches and reports age of staleness
7. Triggers update workflow with temporal priority

**Implementation Sync:**
1. Read Case file and extract content_hash and hash_timestamp
2. Read implementation file and extract referenced hash and timestamp
3. Compare hashes
4. If mismatch: Calculate time delta between timestamps
5. Report staleness with temporal context
6. Update implementation
7. Update hash and timestamp reference in implementation
8. Commit with both files in sync

**Plan Baseline with Temporal Tracking:**
1. Plan captures git_commit_sha and plan_created timestamp
2. Can detect all changes since plan created with temporal context
3. `git diff $git_commit_sha HEAD -- /test-cases/`
4. Shows all Case modifications since plan baseline with timestamps
5. Prioritize updates based on age of changes

## Quality Standards

### Hash and Timestamp Integrity Requirements
- All Cases MUST have valid content_hash fields
- All Cases MUST have valid hash_timestamp in ISO 8601 format (UTC)
- Hash MUST be SHA-256 of canonical YAML (excluding hash and timestamp fields)
- Timestamp MUST be generated when hash is computed
- Implementation files MUST reference source hashes with timestamps
- Hash mismatches MUST trigger staleness warnings with temporal context
- Plans MUST capture valid git_commit_sha and plan_created timestamp

### Path Reference Standards
- All Case references use absolute paths from repo root
- Paths must resolve to existing files
- Format: `/[directory]/[ID].yaml`
- No relative paths (../), only absolute (/test-cases/)
- Broken path references block in enforce mode

### Validation at Sync
- Verify all content_hash fields are current
- Verify all hash_timestamp fields are valid ISO 8601
- Check implementation hash and timestamp references match Cases
- Validate all file paths resolve correctly
- Ensure git_commit_sha in plans is valid
- Ensure plan_created timestamp is present and valid
- Flag any hash mismatches with temporal delta for prioritization

### Enforcement Modes
- **Report Mode**: Log hash mismatches with time deltas, allow continuation
- **Enforce Mode**: Block on hash mismatches, require sync, prioritize by age
- Invalid hashes or timestamps must block with clear error messages
- Missing hash or timestamp fields must prevent Case creation
- Broken path references must block execution
- Timestamps in non-ISO 8601 format must be rejected

## Template Enforcement

### Required Templates with Hash and Timestamp Support

All artifacts MUST use templates from `.specify/templates/` with hash and timestamp fields:

| Artifact Type | Template File | Required Hash Fields |
|--------------|---------------|---------------------|
| **Test Case** | test-case-template.yaml | content_hash (auto-computed), hash_timestamp (ISO 8601) |
| **Scenario Case** | scenario-case-template.yaml | content_hash (auto-computed), hash_timestamp (ISO 8601) |
| **Precondition Case** | precondition-case-template.yaml | content_hash (auto-computed), hash_timestamp (ISO 8601) |
| **Plan** | plan-template.md | git_commit_sha (from git), plan_created (ISO 8601) |
| **Tasks** | tasks-template.md | Case paths with hashes and timestamps |

### Template Validation Rules

- **H-TPL1.** All Cases MUST include content_hash field
- **H-TPL2.** All Cases MUST include hash_timestamp in ISO 8601 format
- **H-TPL3.** Plans MUST capture git_commit_sha and plan_created timestamp
- **H-TPL4.** Tasks MUST reference specs and Cases by file path with timestamps
- **H-TPL5.** Implementation files MUST include hash and timestamp comments
- **H-TPL6.** Hash computation MUST follow canonical YAML format
- **H-TPL7.** Path references MUST be absolute from repo root
- **H-TPL8.** Templates MUST auto-compute hashes and timestamps on creation
- **H-TPL9.** Hash mismatches MUST be detected with temporal context
- **H-TPL10.** Git SHA and timestamps MUST be captured at plan creation
- **H-TPL11.** All path references MUST resolve to existing files
- **H-TPL12.** Timestamp format MUST be ISO 8601 UTC (YYYY-MM-DDTHH:MM:SSZ)

## Hash-Based Governance with Temporal Tracking

The constitution enforces stateless specification tracking through content hashing
with datetime stamps rather than manual versioning. All tools, specifications, Cases,
plans, and tasks must conform to hash-based change detection with temporal awareness.
Enforcement happens through:
- Automatic hash computation for all Cases with timestamp generation
- Git SHA capture for plan baselines with creation timestamps
- File path references for navigation
- Hash and timestamp embedding in implementations
- Mismatch detection with temporal context triggering updates
- Prioritization based on staleness age

Benefits of hash-based approach with timestamps:
- **Stateless**: No version numbers to maintain
- **Automatic**: Hashes and timestamps computed from content
- **Immutable**: Changes always generate new hashes with new timestamps
- **Traceable**: Implementation → Case via hash with temporal context
- **Navigable**: Direct file paths for agents
- **Verifiable**: Hash comparison detects changes with age awareness
- **Temporal**: Understand when changes occurred and staleness duration
- **Prioritizable**: Address oldest stale implementations first

Amendment procedure requires:
- Document change rationale and impact
- Update hash and timestamp computation if needed
- Migrate existing Cases to include hashes and timestamps
- Update all affected templates
- Version increment following semantic versioning

Templates are mandatory and located at `/Users/keith/claude/specifytest/.specify/templates/`.
All artifacts must adopt templates exactly, including hash computation, timestamp
generation, and path reference formats.

**Version**: 5.1.0 | **Ratified**: TODO(RATIFICATION_DATE) | **Last Amended**: 2025-09-25