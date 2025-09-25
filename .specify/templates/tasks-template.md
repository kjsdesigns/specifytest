# Tasks: [PLAN_NAME]

**Input**: Plan from `/plans/[plan-name]/plan.md` with Git SHA baseline and modular specs from `/specs/*`
**Prerequisites**: plan.md with git_commit_sha and delta analysis (required), baseline modular specs
**Purpose**: Bridge the gap between current codebase state and target spec compliance using file path references

## Execution Flow (main)
```
1. Load plan.md from /plans/[plan-name]/ directory
   → If not found: ERROR "No implementation plan found"
   → Extract: Delta Analysis section (current vs target state)
   → Extract: tech stack, libraries, structure, baseline spec IDs
2. Load baseline specs from /specs/*/ based on plan references:
   → /specs/data/*/spec.md: Extract entities → model tasks
   → /specs/contracts/*/spec.md: Each contract → contract test task
   → /specs/technology/*/spec.md: Extract decisions → setup tasks
   → /specs/workflows/*/spec.md: Extract test cases → test implementation tasks
3. Generate tasks from Delta Analysis:
   → For each gap identified:
     - Create task with baseline spec reference
     - List Test/Scenario Cases to implement/pass
     - Define success criteria from spec
   → Categories: Setup, Tests (TDD), Core, Integration, Polish
4. Apply task rules:
   → Different files = mark [P] for parallel
   → Same file = sequential (no [P])
   → Tests before implementation (TDD)
5. Number tasks sequentially (T001, T002...)
6. Generate dependency graph
7. Create parallel execution examples
8. Validate task completeness:
   → All contracts have tests?
   → All entities have models?
   → All endpoints implemented?
9. Return: SUCCESS (tasks ready for execution)
```

## Task Format

### Task Structure
```
[ID] [P?] Task Title
  Validates Specs: /specs/workflows/W-001/spec.md, /specs/pages/P-002/spec.md
  Implements Cases: /test-cases/TC-001.yaml, /test-cases/TC-002.yaml
  Uses Preconditions: /precondition-cases/PC-001.yaml, /precondition-cases/PC-002.yaml
  Current State: [what exists now]
  Target State: [what spec requires]
  Success Criteria: [measurable outcome]
  Implementation File: [exact path to modify/create]
  Hash References: [content hashes with timestamps to embed in implementation]
```

- **[P]**: Can run in parallel (different files, no dependencies)
- Each task MUST reference baseline specs and test cases

## Path Conventions
- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 3.1: Setup
- [ ] T001 Create project structure per implementation plan
- [ ] T002 Initialize [language] project with [framework] dependencies
- [ ] T003 [P] Configure linting and formatting tools

## Phase 3.2: Tests First (TDD) ⚠️ MUST COMPLETE BEFORE 3.3
**CRITICAL: These tests MUST be written and MUST FAIL before ANY implementation**

- [ ] T004 [P] Contract test POST /api/users
  - Validates Specs: /specs/contracts/CONTRACT-001/spec.md
  - Implements Cases: /test-cases/TC-004.yaml, /test-cases/TC-005.yaml
  - Uses Preconditions: /precondition-cases/PC-001.yaml
  - Current State: No test exists
  - Target State: Failing contract test per spec
  - Success Criteria: Test exists and fails (no implementation)
  - Implementation File: tests/contract/test_users_post.py
  - Hash References: TC-004 (sha256:abc123..., 2024-01-15T10:30:00Z), TC-005 (sha256:def456..., 2024-01-15T10:31:00Z)

- [ ] T005 [P] Contract test GET /api/users/{id}
  - Validates Specs: /specs/contracts/CONTRACT-001/spec.md
  - Implements Cases: /test-cases/TC-006.yaml
  - Uses Preconditions: /precondition-cases/PC-001.yaml, /precondition-cases/PC-002.yaml
  - Current State: No test exists
  - Target State: Failing contract test per spec
  - Success Criteria: Test exists and fails
  - Implementation File: tests/contract/test_users_get.py
  - Hash References: TC-006 (sha256:789abc..., 2024-01-15T10:32:00Z)

- [ ] T006 [P] Integration test user registration
  - Validates Specs: /specs/workflows/W-001/spec.md
  - Implements Cases: /scenario-cases/SC-001.yaml
  - Uses Preconditions: /precondition-cases/PC-001.yaml, /precondition-cases/PC-003.yaml
  - Current State: No test coverage
  - Target State: End-to-end test per workflow spec
  - Success Criteria: Test validates full registration flow
  - Implementation File: tests/integration/test_registration.py
  - Hash References: SC-001 (sha256:def789..., 2024-01-15T11:00:00Z)

## Phase 3.3: Core Implementation (ONLY after tests are failing)

- [ ] T008 [P] User model implementation
  - Validates Specs: /specs/data/DATA-001/spec.md
  - Implements Cases: /test-cases/TC-007.yaml, /test-cases/TC-008.yaml
  - Uses Preconditions: /precondition-cases/PC-004.yaml
  - Current State: No model exists
  - Target State: Model matching spec schema
  - Success Criteria: Model passes all spec validation rules
  - Implementation File: src/models/user.py
  - Hash References: DATA-001 (sha256:aaa111..., 2024-01-15T09:00:00Z)

- [ ] T009 [P] UserService CRUD operations
  - Validates Specs: /specs/concepts/C-001/spec.md
  - Implements Cases: /test-cases/TC-009.yaml through /test-cases/TC-013.yaml
  - Uses Preconditions: /precondition-cases/PC-001.yaml, /precondition-cases/PC-004.yaml
  - Current State: No service layer
  - Target State: Service implementing business rules
  - Success Criteria: All CRUD operations per spec
  - Implementation File: src/services/user_service.py
  - Hash References: C-001 (sha256:bbb222..., 2024-01-15T09:15:00Z)

- [ ] T011 POST /api/users endpoint
  - Validates Specs: /specs/contracts/CONTRACT-001/spec.md
  - Implements Cases: /test-cases/TC-004.yaml, /test-cases/TC-005.yaml
  - Uses Preconditions: /precondition-cases/PC-001.yaml
  - Current State: Test failing (from T004)
  - Target State: Endpoint passes contract test
  - Success Criteria: Contract test T004 passes
  - Implementation File: src/api/users.py
  - Hash References: CONTRACT-001 (sha256:ccc333..., 2024-01-15T09:20:00Z)

## Phase 3.4: Integration
- [ ] T015 Connect UserService to DB
- [ ] T016 Auth middleware
- [ ] T017 Request/response logging
- [ ] T018 CORS and security headers

## Phase 3.5: Polish
- [ ] T019 [P] Unit tests for validation in tests/unit/test_validation.py
- [ ] T020 Performance tests (<200ms)
- [ ] T021 [P] Update docs/api.md
- [ ] T022 Remove duplication
- [ ] T023 Run manual-testing.md

## Dependencies
- Tests (T004-T007) before implementation (T008-T014)
- T008 blocks T009, T015
- T016 blocks T018
- Implementation before polish (T019-T023)

## Parallel Example
```
# Launch T004-T007 together:
Task: "Contract test POST /api/users in tests/contract/test_users_post.py"
Task: "Contract test GET /api/users/{id} in tests/contract/test_users_get.py"
Task: "Integration test registration in tests/integration/test_registration.py"
Task: "Integration test auth in tests/integration/test_auth.py"
```

## Notes
- [P] tasks = different files, no dependencies
- Verify tests fail before implementing
- Commit after each task
- Avoid: vague tasks, same file conflicts

## Task Generation Rules
*Applied during main() execution based on Delta Analysis*

1. **From Delta Gaps**:
   - Each gap → one or more tasks to close it
   - Tasks reference baseline specs causing the gap
   - Tasks list all Test/Scenario Cases involved

2. **From Baseline Specs**:
   - Contract specs → contract test tasks [P]
   - Data specs → model creation tasks [P]
   - Workflow specs → integration test tasks [P]
   - Concept specs → business logic tasks

3. **Task Requirements** (per Constitution v3.1.0):
   - MUST reference baseline spec IDs
   - MUST list current vs target state
   - MUST enumerate Test/Scenario Cases
   - MUST define measurable success criteria

4. **Ordering**:
   - Setup → Tests (TDD) → Implementation → Integration → Polish
   - Dependencies block parallel execution

## Validation Checklist
*GATE: Checked by main() before returning*

- [ ] All gaps from Delta Analysis have tasks
- [ ] Each task references baseline specs
- [ ] Each task lists Test/Scenario Cases
- [ ] All tests come before implementation (TDD)
- [ ] Tasks show current → target state progression
- [ ] Success criteria are measurable
- [ ] Parallel tasks truly independent
- [ ] Each task specifies exact file path
- [ ] No task modifies same file as another [P] task