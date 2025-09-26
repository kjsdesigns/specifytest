
# Implementation Plan: [PLAN_NAME]

**Date**: [DATE]
**Git Commit SHA**: [GIT_COMMIT_SHA]  # Capture with: git rev-parse HEAD
**Plan Created**: [PLAN_CREATED_TIMESTAMP]  # ISO 8601: date -u +"%Y-%m-%dT%H:%M:%SZ"
**Input**: Modular specifications from `/specs/*` relevant to this plan

## Execution Flow (/plan command scope)
1. Load relevant modular specs from `/specs/*` directories
2. Fill Technical Context (identify any NEEDS CLARIFICATION items)
3. Evaluate Constitution Check for TDD compliance
4. Execute Phase 0: Research and update specs
5. Execute Phase 1: Design contracts, data models, and documentation
6. Re-evaluate Constitution Check
7. Plan Phase 2: Describe task generation approach (DO NOT create tasks.md)
8. STOP - Ready for /tasks command

**Note**: The /plan command stops after planning. The /tasks command creates tasks.md.

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
Test cases to create/update in `/specs/test-cases/`:
- /specs/test-cases/TC-001.yaml: [Description] - Status: [New/Update]
- /specs/test-cases/TC-002.yaml: [Description] - Status: [New/Update]
- /specs/test-cases/TC-003.yaml: [Description] - Status: [New/Update]

### Scenario Cases
Scenario cases to create/update in `/specs/scenario-cases/`:
- /specs/scenario-cases/SC-001.yaml: [Description] - Status: [New/Update]
- /specs/scenario-cases/SC-002.yaml: [Description] - Status: [New/Update]

### Precondition Cases
Precondition cases to create/update in `/specs/precondition-cases/`:
- /specs/precondition-cases/PC-001.yaml: [Description] - Status: [New/Update]
- /specs/precondition-cases/PC-002.yaml: [Description] - Status: [New/Update]

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
1. Extract unknowns from Technical Context
2. Research dependencies and best practices
3. Update relevant modular specs with findings:
   - Technology decisions → `/specs/technology/`
   - Data research → `/specs/data/`
   - Integration patterns → `/specs/integrations/`

**Output**: Updated specs with all unknowns resolved

## Phase 1: Design & Contracts
1. Update data specs with entities and validation rules
2. Update contract specs with endpoint specifications
3. Generate failing contract tests
4. Update workflow specs with test scenarios
5. Update agent context file if needed

**Output**: Updated specs, failing tests, and documentation

## Phase 2: Task Planning Approach
*Describes what /tasks command will do - not executed by /plan*

**Strategy**: Generate tasks from Delta Analysis gaps
- Tests before implementation (TDD)
- Mark [P] for parallel execution
- Reference baseline specs and Cases

**Output**: Tasks in `/plans/[plan-name]/tasks.md` (created by /tasks command)

## Phases 3-5: Implementation
*Beyond /plan scope - handled by /tasks and implementation commands*

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
*Based on current Constitution - See `.specify/memory/constitution.md`*
