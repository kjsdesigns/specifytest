# Specification Naming Standards

This guide explains the naming conventions for specification files in the Specify framework.

## Overview

All specification files follow a standardized naming pattern that combines three elements:
1. **Type Prefix** - Identifies the specification type (e.g., TC, W, PAGE)
2. **Numeric ID** - Sequential number within that type (e.g., 001, 042)
3. **Descriptive Name** - Human-readable identifier (e.g., user_login, payment_flow)

## Filename Format

```
[PREFIX]-[NUMBER]-[descriptive_name].[ext]
```

**Examples:**
- `TC-001-valid_login.yaml` - Test case for valid login
- `W-042-checkout_flow.md` - Workflow for checkout process
- `PAGE-015-dashboard.md` - Dashboard page specification
- `CON-008-order.md` - Order concept specification

## Naming Rules

### 1. Type Prefix

Each specification type has a unique prefix:

| Type | Prefix | Extension | Example |
|------|--------|-----------|---------|
| TestCase | `TC` | `.yaml` | `TC-001-user_auth.yaml` |
| ScenarioCase | `SC` | `.yaml` | `SC-001-end_to_end.yaml` |
| PreconditionCase | `PC` | `.yaml` | `PC-001-clean_db.yaml` |
| Workflow | `W` | `.md` | `W-001-registration.md` |
| Page | `PAGE` | `.md` | `PAGE-001-login.md` |
| UIComponent | `UI` | `.md` | `UI-001-button.md` |
| Concept | `CON` | `.md` | `CON-001-user.md` |
| Data | `DATA` | `.md` | `DATA-001-user_profile.md` |
| Contract | `CONTRACT` | `.md` | `CONTRACT-001-api_response.md` |
| Event | `EVENT` | `.md` | `EVENT-001-user_created.md` |
| Integration | `INT` | `.md` | `INT-001-stripe_payment.md` |
| Message | `MSG` | `.md` | `MSG-001-order_request.md` |
| Security | `SEC` | `.md` | `SEC-001-jwt_auth.md` |
| Technology | `TECH` | `.md` | `TECH-001-postgres_db.md` |
| Architecture | `ARCH` | `.md` | `ARCH-001-microservices.md` |
| Configuration | `CFG` | `.md` | `CFG-001-database_config.md` |

### 2. Numeric ID

- Must be a **positive integer** (no leading zeros in display, but use leading zeros in filenames for sorting)
- Sequential within each type (TC-001, TC-002, TC-003...)
- Start at 001 for the first spec of each type
- Numbers are unique within their type prefix (TC-001 and W-001 are different specs)

### 3. Descriptive Name

The descriptive name must follow these rules:

#### Format
- **Lowercase only** - No uppercase letters
- **snake_case** or **kebab-case** - Use underscores `_` or hyphens `-` to separate words
- **Maximum 4 words** - Keep names concise and focused
- **Valid characters** - Only `a-z`, `0-9`, `_`, `-`
- **No spaces** - Use `_` or `-` instead

#### Good Examples
✅ `user_login`
✅ `payment-processing`
✅ `order_history`
✅ `api_response`
✅ `checkout_flow`
✅ `password_reset`

#### Bad Examples
❌ `UserLogin` - Contains uppercase
❌ `user login` - Contains space
❌ `user_login_with_oauth_provider` - More than 4 words
❌ `login!` - Invalid character
❌ `the_user_login_page` - Article words waste word limit

### 4. Name Field Synchronization

The descriptive name in the filename **MUST match** the `name` field in the spec:

**Filename:** `TC-001-user_login.yaml`

**Spec content:**
```yaml
id: TC-001
name: user_login  # Must match filename
type: TestCase
```

### 5. Type-Specific Naming Guidelines

Each spec type has specific naming conventions:

#### Test Cases (TC)
- **Focus**: What is being tested
- **Format**: `action_being_tested`
- **Examples**: `valid_login`, `invalid_password`, `missing_email`, `successful_checkout`

#### Scenario Cases (SC)
- **Focus**: End-to-end workflow or user journey
- **Format**: `journey_or_flow_name`
- **Examples**: `auth_flow`, `checkout_journey`, `user_onboarding`, `order_fulfillment`

#### Precondition Cases (PC)
- **Focus**: Setup or state being established
- **Format**: `state_or_setup_name`
- **Examples**: `clean_database`, `test_users`, `mock_payment`, `seeded_products`

#### Workflows (W)
- **Focus**: Business process or user flow
- **Format**: `process_or_flow_name`
- **Examples**: `user_registration`, `order_checkout`, `password_reset`, `account_recovery`

#### Pages (PAGE)
- **Focus**: UI page or screen
- **Format**: `page_name`
- **Examples**: `login`, `dashboard`, `settings`, `profile`

#### UI Components (UI)
- **Focus**: Reusable UI element
- **Format**: `component_name`
- **Examples**: `button`, `input_field`, `dropdown`, `modal`

#### Concepts (CON)
- **Focus**: Domain entity (singular)
- **Format**: `entity_name`
- **Examples**: `user`, `order`, `product`, `account`

#### Data (DATA)
- **Focus**: Data structure or schema
- **Format**: `entity_or_schema_name`
- **Examples**: `user_profile`, `order_history`, `product_catalog`, `transaction_log`

#### Contracts (CONTRACT)
- **Focus**: API or interface contract
- **Format**: `contract_purpose`
- **Examples**: `api_response`, `user_schema`, `payment_request`, `order_payload`

#### Events (EVENT)
- **Focus**: Domain event
- **Format**: `event_name`
- **Examples**: `user_created`, `order_placed`, `payment_completed`, `inventory_updated`

#### Integrations (INT)
- **Focus**: External service integration
- **Format**: `service_purpose`
- **Examples**: `stripe_payment`, `sendgrid_email`, `google_maps`, `aws_s3`

#### Messages (MSG)
- **Focus**: Message type
- **Format**: `message_purpose`
- **Examples**: `order_request`, `payment_response`, `user_notification`, `status_update`

#### Security (SEC)
- **Focus**: Security pattern or control
- **Format**: `security_mechanism`
- **Examples**: `jwt_auth`, `rate_limiting`, `data_encryption`, `rbac_policy`

#### Technology (TECH)
- **Focus**: Technology or tool
- **Format**: `technology_purpose`
- **Examples**: `react_frontend`, `postgres_db`, `redis_cache`, `docker_containers`

#### Architecture (ARCH)
- **Focus**: Architectural pattern or style
- **Format**: `architecture_pattern`
- **Examples**: `microservices`, `event_driven`, `three_tier`, `hexagonal`

#### Configuration (CFG)
- **Focus**: Configuration area
- **Format**: `config_area`
- **Examples**: `database_config`, `api_keys`, `feature_flags`, `env_variables`

## Uniqueness Requirements

### ID Uniqueness
- No two specs can have the same ID across the **entire repository**
- `TC-001` can only exist once (even across different directories)

### Name Uniqueness
- No two specs **of the same type** can have the same name
- `TC-001-user_login` and `TC-002-user_login` would conflict (same name)
- `TC-001-user_login` and `W-001-user_login` are allowed (different types)

## Migration from Old Format

If you have existing specs using the old format (`TC-001.yaml`), use the migration tool:

```bash
# Preview migration (dry run)
python scripts/migrate-spec-names.py /specs/

# Apply migration
python scripts/migrate-spec-names.py /specs/ --apply
```

The migration tool will:
1. Analyze existing spec files
2. Suggest descriptive names based on content
3. Rename files to new format
4. Report any conflicts or issues

## Validation

The validator enforces all naming rules:

```bash
# Validate all specs
python scripts/validate-specs.py /specs/

# Verbose output
python scripts/validate-specs.py /specs/ --verbose
```

**Validation checks:**
- ✓ Filename format matches `[PREFIX]-[NUMBER]-[name].[ext]`
- ✓ Prefix matches spec type
- ✓ Number is numeric
- ✓ Descriptive name matches `name` field
- ✓ Name follows pattern (lowercase, 4 words max)
- ✓ No duplicate IDs
- ✓ No duplicate names within type
- ✓ Correct file extension (.yaml vs .md)

## Best Practices

### 1. Keep Names Short and Focused
- **Good**: `user_login`
- **Bad**: `user_login_with_password_validation`

### 2. Avoid Articles and Prepositions
- **Good**: `payment_flow`
- **Bad**: `the_payment_flow`

### 3. Use Domain Language
- **Good**: `order_checkout`
- **Bad**: `buy_stuff`

### 4. Be Consistent Within Type
If you use `user_login`, continue with:
- `user_logout`
- `user_register`
- `user_password_reset`

Not:
- `logout_user` (inconsistent ordering)
- `registration` (different word form)

### 5. Avoid Redundancy with Type
Since the prefix indicates the type, don't repeat it:
- **Good**: `TC-001-valid_input.yaml`
- **Bad**: `TC-001-test_valid_input.yaml`

### 6. Use Underscores for Multi-Word Concepts
When a single concept requires multiple words, keep them together:
- `user_profile` (user profile as one concept)
- `order_history` (order history as one concept)

## Examples by Scenario

### User Authentication System

```
specs/
├── workflows/
│   ├── W-001-user_registration.md
│   ├── W-002-user_login.md
│   └── W-003-password_reset.md
├── pages/
│   ├── PAGE-001-login.md
│   ├── PAGE-002-register.md
│   └── PAGE-003-forgot_password.md
├── concepts/
│   ├── CON-001-user.md
│   └── CON-002-session.md
├── data/
│   ├── DATA-001-user_profile.md
│   └── DATA-002-auth_tokens.md
├── test-cases/
│   ├── TC-001-valid_login.yaml
│   ├── TC-002-invalid_password.yaml
│   ├── TC-003-new_registration.yaml
│   └── TC-004-password_reset.yaml
└── scenario-cases/
    ├── SC-001-auth_flow.yaml
    └── SC-002-account_recovery.yaml
```

## Quick Reference

| Element | Rule | Example |
|---------|------|---------|
| Prefix | Type-specific uppercase | `TC`, `W`, `PAGE` |
| Number | Sequential, numeric | `001`, `042`, `999` |
| Name | lowercase, 4 words max, snake_case/kebab-case | `user_login`, `checkout-flow` |
| Extension | `.yaml` for cases, `.md` for others | `.yaml`, `.md` |
| Full Pattern | `[PREFIX]-[NUM]-[name].[ext]` | `TC-001-user_login.yaml` |

## Getting Help

- See template files in `/templates/` for examples
- Check `_meta` section in templates for type-specific rules
- Run validator with `--verbose` for detailed error messages
- Check `constitution.md` for governance rules

## Version History

- **v1.0** - Initial naming standards with descriptive filenames
- **v1.1** - Added uniqueness requirements for names
- **v1.2** - Expanded type-specific naming guidelines