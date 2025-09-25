
# Implementation Plan: [PLAN_NAME]

**Date**: [DATE]
**Git Commit SHA**: [GIT_COMMIT_SHA]  # Capture with: git rev-parse HEAD
**Plan Created**: [PLAN_CREATED_TIMESTAMP]  # ISO 8601: date -u +"%Y-%m-%dT%H:%M:%SZ"
**Input**: Modular specifications from `/specs/*` relevant to this plan

## Execution Flow (/plan command scope)
```
1. Identify relevant modular specs from `/specs/*` directories
   → Load specs based on plan requirements
   → If critical specs missing: ERROR "Required specs not found"
2. Fill Technical Context (scan for NEEDS CLARIFICATION)
   → Detect Project Type from context (web=frontend+backend, mobile=app+api)
   → Set Structure Decision based on project type
3. Fill the Constitution Check section based on Test-Driven Development principles
4. Evaluate Constitution Check section below
   → Verify TDD compliance (Test Cases defined before implementation)
   → Check Single Source of Truth (no duplicate Case definitions)
   → Validate identifier standards and documentation completeness
   → If violations exist: Document in Complexity Tracking
   → If no justification possible: ERROR "Fix violations first"
   → Update Progress Tracking: Initial Constitution Check
5. Execute Phase 0 → update relevant modular specs with research
   → If NEEDS CLARIFICATION remain: ERROR "Resolve unknowns"
6. Execute Phase 1 → update modular specs with contracts, data models, quickstart docs, agent-specific template file (e.g., `CLAUDE.md` for Claude Code, `.github/copilot-instructions.md` for GitHub Copilot, `GEMINI.md` for Gemini CLI, `QWEN.md` for Qwen Code or `AGENTS.md` for opencode).
7. Re-evaluate Constitution Check section
   → If new violations: Refactor design, return to Phase 1
   → Update Progress Tracking: Post-Design Constitution Check
8. Plan Phase 2 → Describe task generation approach (DO NOT create tasks.md)
9. STOP - Ready for /tasks command
```

**IMPORTANT**: The /plan command STOPS at step 7. Phases 2-4 are executed by other commands:
- Phase 2: /tasks command creates tasks.md
- Phase 3-4: Implementation execution (manual or via tools)

## Summary
[Extract from relevant modular specs: primary requirements + technical approach from research]

## Delta Analysis
*Identifies gaps between current codebase state and target spec requirements*

### Current State Assessment
- **Existing Implementation**: [What's already built, if anything]
- **Test Coverage**: [Current test cases and their status]
- **Spec Compliance**: [Which specs are partially/fully met]

### Target State (from Baseline Specs)
- **Required Specs**: [List modular spec IDs this plan targets]
  - `/specs/workflows/[W-xxx]`: [Brief description]
  - `/specs/data/[DATA-xxx]`: [Brief description]
  - `/specs/contracts/[CONTRACT-xxx]`: [Brief description]
- **Test Cases Required**: [Total count of Test/Scenario Cases to implement]
- **Success Metrics**: [How we measure spec compliance]

### Gap Summary
| Spec Area | Current State | Target State | Delta |
|-----------|--------------|--------------|-------|
| [e.g., User Auth] | [No implementation] | [W-001 compliant] | [Full implementation needed] |
| [e.g., Data Model] | [Partial schema] | [DATA-001 compliant] | [Add missing fields, constraints] |

## Cases to Develop
*Lists all Test Cases, Scenario Cases, and Precondition Cases to be created/updated with file paths*

### Test Cases
Test cases to create/update in `/test-cases/`:
- /test-cases/TC-001.yaml: [Description] - Status: [New/Update]
- /test-cases/TC-002.yaml: [Description] - Status: [New/Update]
- /test-cases/TC-003.yaml: [Description] - Status: [New/Update]

### Scenario Cases
Scenario cases to create/update in `/scenario-cases/`:
- /scenario-cases/SC-001.yaml: [Description] - Status: [New/Update]
- /scenario-cases/SC-002.yaml: [Description] - Status: [New/Update]

### Precondition Cases
Precondition cases to create/update in `/precondition-cases/`:
- /precondition-cases/PC-001.yaml: [Description] - Status: [New/Update]
- /precondition-cases/PC-002.yaml: [Description] - Status: [New/Update]

## Technical Context
**Language/Version**: [e.g., Python 3.11, Swift 5.9, Rust 1.75 or NEEDS CLARIFICATION]  
**Primary Dependencies**: [e.g., FastAPI, UIKit, LLVM or NEEDS CLARIFICATION]  
**Storage**: [if applicable, e.g., PostgreSQL, CoreData, files or N/A]  
**Testing**: [e.g., pytest, XCTest, cargo test or NEEDS CLARIFICATION]  
**Target Platform**: [e.g., Linux server, iOS 15+, WASM or NEEDS CLARIFICATION]
**Project Type**: [single/web/mobile - determines source structure]  
**Performance Goals**: [domain-specific, e.g., 1000 req/s, 10k lines/sec, 60 fps or NEEDS CLARIFICATION]  
**Constraints**: [domain-specific, e.g., <200ms p95, <100MB memory, offline-capable or NEEDS CLARIFICATION]  
**Scale/Scope**: [domain-specific, e.g., 10k users, 1M LOC, 50 screens or NEEDS CLARIFICATION]

## Constitution Check
*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### TDD Compliance
- [ ] Test/Scenario/Precondition Cases defined at spec level before implementation
- [ ] Red-Green-Refactor workflow enforced
- [ ] Plans and tasks precede implementation

### Single Source of Truth
- [ ] Each Test/Scenario Case owned by exactly one spec artifact
- [ ] Precondition Cases stored under `/preconditions/`
- [ ] No duplicate Case definitions

### Identifier Standards
- [ ] All IDs match regex patterns (W-001, W-001.1, W-001.SC001, PC-AUTH.001)
- [ ] Human names use kebab-case

### Documentation Completeness
- [ ] Test Cases include all required fields (purpose, steps, validations, etc.)
- [ ] Scenario Cases specify test cases, preconditions, cache strategy
- [ ] Precondition Cases document setup/teardown and resources

### Plan/Spec Alignment
- [ ] Plans reference only canonical Case IDs from specs
- [ ] No addition/removal/contradiction of spec-defined Cases
- [ ] Status changes only after Pass Criteria met

## Plan Artifacts & Locations

### Plan Documentation Structure
```
plans/[plan-name]/
├── plan.md              # This file (/plan command output)
└── tasks.md             # Phase 2 output (/tasks command - NOT created by /plan)
```

### Modular Spec Documentation (where research & decisions are recorded)
```
specs/
├── workflows/           # Workflow specs (W-xxx)
├── pages/              # Page specs (P-xxx)
├── concepts/           # Concept specs (C-xxx)
├── integrations/       # Integration specs (INT-xxx)
├── data/               # Data specs (DATA-xxx)
├── security/           # Security specs (SEC-xxx)
├── technology/         # Technology specs (TECH-xxx)
├── configuration/      # Configuration specs (CONFIG-xxx)
└── contracts/          # Contract specs (CONTRACT-xxx)
```

**IMPORTANT**: Research findings, design decisions, and rationale discovered during
the plan phase MUST be recorded in the appropriate spec documents, not in the plan.
The plan is for execution tracking only.

### Implementation Structure (repository root)
```
# Option 1: Single project (DEFAULT)
src/
├── models/
├── services/
├── cli/
└── lib/

tests/
├── contract/
├── integration/
└── unit/

# Option 2: Web application (when "frontend" + "backend" detected)
backend/
├── src/
│   ├── models/
│   ├── services/
│   └── api/
└── tests/

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
└── tests/

# Option 3: Mobile + API (when "iOS/Android" detected)
api/
└── [same as backend above]

ios/ or android/
└── [platform-specific structure]
```

**Structure Decision**: [DEFAULT to Option 1 unless Technical Context indicates web/mobile app]

## Phase 0: Outline & Research
1. **Extract unknowns from Technical Context** above:
   - For each NEEDS CLARIFICATION → research task
   - For each dependency → best practices task
   - For each integration → patterns task

2. **Generate and dispatch research agents**:
   ```
   For each unknown in Technical Context:
     Task: "Research {unknown} for {plan context}"
   For each technology choice:
     Task: "Find best practices for {tech} in {domain}"
   ```

3. **Update relevant modular specs** with findings:
   - Technology decisions → `/specs/technology/[TECH-xxx]/spec.md`
   - Data research → `/specs/data/[DATA-xxx]/spec.md`
   - Integration patterns → `/specs/integrations/[INT-xxx]/spec.md`
   - Format: Decision, Rationale, Alternatives considered

**Output**: Updated modular specs with all NEEDS CLARIFICATION resolved

## Phase 1: Design & Contracts
*Prerequisites: Research phase complete in modular specs*

1. **Update data specs** with entities:
   - Create/update `/specs/data/[DATA-xxx]/spec.md`
   - Entity definitions, fields, relationships
   - Validation rules from requirements
   - State transitions if applicable

2. **Update contract specs** from functional requirements:
   - Create/update `/specs/contracts/[CONTRACT-xxx]/spec.md`
   - For each user action → endpoint specification
   - Use standard REST/GraphQL patterns
   - Output OpenAPI/GraphQL schemas

3. **Generate contract tests** from contract specs:
   - One test file per endpoint
   - Assert request/response schemas
   - Tests must fail (no implementation yet)

4. **Update workflow specs** with test scenarios:
   - Update `/specs/workflows/[W-xxx]/spec.md`
   - Each user story → integration test scenario
   - Quickstart test = story validation steps

5. **Update agent file incrementally** (O(1) operation):
   - Run `.specify/scripts/bash/update-agent-context.sh claude`
     **IMPORTANT**: Execute it exactly as specified above. Do not add or remove any arguments.
   - If exists: Add only NEW tech from current plan
   - Preserve manual additions between markers
   - Update recent changes (keep last 3)
   - Keep under 150 lines for token efficiency
   - Output to repository root

**Output**:
- Updated `/specs/data/[DATA-xxx]/spec.md` - Data design decisions
- Updated `/specs/contracts/[CONTRACT-xxx]/spec.md` - API specifications
- Updated workflow/page specs with quickstart documentation
- Failing tests in implementation directories
- Agent-specific file at repository root

## Phase 2: Task Planning Approach
*This section describes what the /tasks command will do - DO NOT execute during /plan*

**Task Generation Strategy**:
- Load `.specify/templates/tasks-template.md` as base
- For each gap identified in Delta Analysis:
  - Generate tasks to close the gap
  - Reference baseline spec IDs
  - List Test/Scenario Cases to develop/pass
- Each contract spec → contract test task [P]
- Each data spec entity → model creation task [P]
- Each workflow spec story → integration test task
- Implementation tasks to make tests pass
- Output to `/plans/[plan-name]/tasks.md`

**Task Requirements per Constitution**:
- Each task MUST reference baseline specs
- Each task MUST list Test/Scenario Case IDs to implement
- Each task MUST define success criteria

**Ordering Strategy**:
- TDD order: Tests before implementation 
- Dependency order: Models before services before UI
- Mark [P] for parallel execution (independent files)

**Estimated Output**: 25-30 numbered, ordered tasks in `/plans/[plan-name]/tasks.md`

**IMPORTANT**: This phase is executed by the /tasks command, NOT by /plan

## Phase 3+: Future Implementation
*These phases are beyond the scope of the /plan command*

**Phase 3**: Task execution (/tasks command creates tasks.md)  
**Phase 4**: Implementation (execute tasks.md following constitutional principles)  
**Phase 5**: Validation (run tests, execute quickstart.md, performance validation)

## Complexity Tracking
*Fill ONLY if Constitution Check has violations that must be justified*

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |


## Progress Tracking
*This checklist is updated during execution flow*

**Phase Status**:
- [ ] Phase 0: Research complete (/plan command)
- [ ] Phase 1: Design complete (/plan command)
- [ ] Phase 2: Task planning complete (/plan command - describe approach only)
- [ ] Phase 3: Tasks generated (/tasks command)
- [ ] Phase 4: Implementation complete
- [ ] Phase 5: Validation passed

**Gate Status**:
- [ ] Initial Constitution Check: PASS
- [ ] Post-Design Constitution Check: PASS
- [ ] All NEEDS CLARIFICATION resolved
- [ ] Complexity deviations documented

---
*Based on Constitution v3.1.0 - See `.specify/memory/constitution.md`*
