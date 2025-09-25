---
description: Create or update specifications and their validation cases from natural language requirements.
---

The user input to you can be provided directly by the agent or as a command argument - you **MUST** consider it before proceeding with the prompt (if not empty).

User input:

$ARGUMENTS

The text the user typed after `/specify` in the triggering message **is** the requirements description. Assume you always have it available in this conversation even if `$ARGUMENTS` appears literally below. Do not ask the user to repeat it unless they provided an empty command.

## Execution Flow

Given the requirements description, follow this workflow:

### 1. Requirement Analysis
Parse the requirements to identify all affected domains:
- User interactions/flows → Workflow specs (W-xxx)
- UI elements/screens → Page specs (P-xxx)
- Business entities/rules → Concept specs (C-xxx)
- Data structures/schemas → Data specs (DATA-xxx)
- API endpoints → Contract specs (CONTRACT-xxx)
- External integrations → Integration specs (INT-xxx)
- Security requirements → Security specs (SEC-xxx)
- Configuration needs → Configuration specs (CONFIG-xxx)
- Technology decisions → Technology specs (TECH-xxx)

### 2. Spec Evaluation
For each identified domain:
- Check if relevant specs already exist in `/specs/[type]/`
- Determine if this requires:
  - Creating new spec(s)
  - Updating existing spec(s)
  - Potentially removing obsolete spec(s)

### 3. Case Analysis
For each spec created/updated, determine needed validation cases:
- **Test Cases** (TC-xxx): Individual test scenarios
  - Unit tests for isolated components
  - Integration tests for component interactions
  - API tests for contract validation
- **Scenario Cases** (SC-xxx): End-to-end workflows
  - User journey validations
  - Multi-step process verification
- **Precondition Cases** (PC-xxx): Reusable setup/teardown
  - Database states
  - Authentication contexts
  - Environment configurations

### 4. DRY Implementation
Apply requirements following DRY principles:
- Each requirement must appear in exactly ONE spec
- Each test validation in exactly ONE Case
- Avoid duplication by proper type selection
- Cross-reference related specs and Cases using IDs
- Maintain clear ownership boundaries

### 5. Spec Generation/Updates
For each affected spec:
- Load the appropriate type-specific template from `.specify/templates/spec-[type].md`
- Create new specs using template structure
- Update existing specs preserving their structure
- Add Case IDs to the `validation_cases` section
- Ensure all references use independent Case IDs (TC-xxx, SC-xxx, PC-xxx)

### 6. Case Generation
Create standalone Case files:
- **Test Cases**: Create TC-xxx.yaml files in `/test-cases/`
  - Use `.specify/templates/test-case-template.yaml`
  - Assign next available TC number
  - Reference needed PC-xxx preconditions
  - Compute content_hash and hash_timestamp after creation
- **Scenario Cases**: Create SC-xxx.yaml files in `/scenario-cases/`
  - Use `.specify/templates/scenario-case-template.yaml`
  - Assign next available SC number
  - Reference TC-xxx tests and PC-xxx preconditions
  - Compute content_hash and hash_timestamp after creation
- **Precondition Cases**: Create PC-xxx.yaml files in `/precondition-cases/`
  - Use `.specify/templates/precondition-case-template.yaml`
  - Assign next available PC number
  - Ensure self-contained (no references to other artifacts)
  - Compute content_hash and hash_timestamp after creation

### 6a. Hash and Timestamp Generation
For each Case file created:
- Compute content_hash as SHA-256 of canonical YAML (excluding hash fields)
- Generate hash_timestamp in ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ)
- Use `.specify/scripts/compute-case-hash.sh` if available, or inline computation
- Ensure both fields are populated before finalizing the Case file

### 8. Update Spec Validation Cases
For each spec, update the `validation_cases` section:
```markdown
## Validation Cases

### Test Cases
References to standalone test cases that validate this spec:
- TC-001: Login with valid credentials
- TC-002: Login with invalid password
- TC-003: Password reset flow

### Scenario Cases
References to end-to-end scenarios involving this spec:
- SC-001: Complete user authentication journey
- SC-002: Account recovery process
```

### 9. Output Summary
Report all changes:
- List of specs created/updated with their IDs and paths
- List of Test Cases created with IDs
- List of Scenario Cases created with IDs
- List of Precondition Cases created with IDs
- Cross-references established
- Any specs or Cases marked for deletion

## Example Requirement Distribution

For "User authentication with email/password":

**Creates/Updates Specs:**
- `/specs/workflows/W-001-auth/spec.md` - Login, registration, reset flows
- `/specs/pages/P-001-login/spec.md` - Login page UI
- `/specs/pages/P-002-register/spec.md` - Registration page UI
- `/specs/concepts/C-001-user/spec.md` - User entity and auth logic
- `/specs/data/DATA-001-user/spec.md` - User schema and credentials
- `/specs/contracts/CONTRACT-001-auth/spec.md` - Auth API endpoints
- `/specs/security/SEC-001-auth/spec.md` - Password policy, sessions

**Creates Standalone Cases:**
- `/test-cases/TC-001.yaml` - Login with valid credentials
- `/test-cases/TC-002.yaml` - Login with invalid password
- `/test-cases/TC-003.yaml` - Registration with new email
- `/test-cases/TC-004.yaml` - Password reset request
- `/scenario-cases/SC-001.yaml` - Complete authentication flow
- `/scenario-cases/SC-002.yaml` - Account recovery journey
- `/precondition-cases/PC-001.yaml` - Database with test users
- `/precondition-cases/PC-002.yaml` - Clean browser session

## Important Notes
- DO NOT create inline test cases in specs
- ALWAYS create standalone Case files with independent IDs
- Test Cases use TC-xxx numbering
- Scenario Cases use SC-xxx numbering
- Precondition Cases use PC-xxx numbering
- Specs only reference Cases by ID, never contain definitions
- Use templates from `.specify/templates/`
- ENSURE proper modular organization
- MAINTAIN constitutional compliance
- FOLLOW Test-Driven Development principles