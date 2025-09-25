---
id: SEC-[XXX]
type: Security
name: [Security Pattern Name]
status: draft
category: [authentication|authorization|encryption|audit|compliance]
related: []
---
# {name}

## Security Objective
[Clear statement of what security goal this specification addresses]

## Threat Model

### Assets to Protect
- **[Asset 1]**: [Description and sensitivity level]
- **[Asset 2]**: [Description and sensitivity level]

### Threat Actors
- **[Actor Type]**: [Capabilities and motivation]
- **[Actor Type]**: [Capabilities and motivation]

### Attack Vectors
1. **[Vector Name]**: [How the attack would work]
   - **Likelihood**: [Low|Medium|High]
   - **Impact**: [Low|Medium|High|Critical]
   - **Risk Level**: [Low|Medium|High|Critical]

2. **[Vector Name]**: [How the attack would work]
   - **Likelihood**: [Low|Medium|High]
   - **Impact**: [Low|Medium|High|Critical]
   - **Risk Level**: [Low|Medium|High|Critical]

## Security Controls

### Preventive Controls
```yaml
prevention:
  - control: [Control name]
    type: [technical|administrative|physical]
    implementation:
      description: [How it's implemented]
      location: [Where in the system]
      responsibility: [Who maintains it]
    effectiveness: [percentage or rating]
```

### Detective Controls
```yaml
detection:
  - control: [Monitoring/logging control]
    type: [real-time|batch|manual]
    alerts:
      - condition: [When to alert]
        severity: [critical|high|medium|low]
        response_time: [SLA for response]
    logs:
      - what: [What is logged]
        where: [Log destination]
        retention: [How long kept]
        pii_handling: [How PII is handled]
```

### Corrective Controls
```yaml
response:
  - incident_type: [Type of incident]
    response_plan:
      - step: [Response step]
        owner: [Who does this]
        timeframe: [How quickly]
    recovery:
      - action: [Recovery action]
        rto: [Recovery time objective]
      - action: [Recovery action]
        rpo: [Recovery point objective]
```

## Authentication & Authorization

### Authentication
```yaml
authentication:
  methods:
    - type: [password|mfa|sso|biometric|certificate]
      strength: [weak|medium|strong]
      factors: [something_you_know|have|are]

  session_management:
    token_type: [JWT|session|api_key]
    storage: [cookie|localStorage|sessionStorage|header]
    expiration: [duration]
    refresh: [true|false]
    refresh_window: [duration]

  password_policy:
    min_length: [number]
    complexity: [requirements]
    history: [number_of_previous]
    expiration: [days]
    lockout_attempts: [number]
    lockout_duration: [minutes]
```

### Authorization
```yaml
authorization:
  model: [RBAC|ABAC|MAC|DAC]

  roles:
    - name: [role_name]
      permissions:
        - resource: [resource_name]
          actions: [create, read, update, delete]
      inherits: [parent_role]

  policies:
    - name: [policy_name]
      rule: [policy_expression]
      enforcement: [strict|permissive]

  access_control:
    default: [deny|allow]
    evaluation: [first_match|all_match]
    cache_ttl: [seconds]
```

## Data Protection

### Encryption
```yaml
encryption:
  at_rest:
    algorithm: [AES-256|RSA]
    key_management:
      storage: [HSM|KMS|vault]
      rotation: [frequency]
      escrow: [true|false]

  in_transit:
    protocol: [TLS 1.3|TLS 1.2]
    cipher_suites:
      - [cipher_suite_name]
    certificate:
      type: [self-signed|CA|lets_encrypt]
      validation: [strict|relaxed]

  field_level:
    - field: [field_name]
      algorithm: [algorithm]
      searchable: [true|false]
```

### Data Classification
```yaml
classification:
  levels:
    - name: [Public|Internal|Confidential|Restricted]
      handling:
        storage: [requirements]
        transmission: [requirements]
        access: [requirements]
        retention: [duration]
        disposal: [method]
```

## Compliance Requirements

### Regulatory
```yaml
regulations:
  - name: [GDPR|CCPA|HIPAA|PCI-DSS|SOC2]
    requirements:
      - [Specific requirement]
      - [Specific requirement]
    evidence:
      - [How compliance is demonstrated]
    audit_frequency: [annual|quarterly]
```

### Privacy
```yaml
privacy:
  pii_handling:
    identification: [How PII is identified]
    minimization: [How data is minimized]
    anonymization: [Techniques used]
    consent: [How consent is obtained]
    portability: [How data export works]
    deletion: [Right to be forgotten process]
```

## Security Testing

### Test Types
```yaml
testing:
  static_analysis:
    tools: [tool_names]
    frequency: [on_commit|daily|weekly]
    blocking: [true|false]

  dynamic_analysis:
    tools: [tool_names]
    frequency: [per_deployment|weekly|monthly]
    environments: [dev|staging|prod]

  penetration_testing:
    frequency: [annual|bi-annual|quarterly]
    scope: [full|targeted]
    provider: [internal|external]

  vulnerability_scanning:
    dependencies: [true|false]
    containers: [true|false]
    infrastructure: [true|false]
    frequency: [continuous|daily|weekly]
```

### Security Test Cases

#### Authentication Tests
- id: SEC-[XXX].001
  name: [Brute force protection]
  scenario:
    given:
      - User account exists
    when:
      - Multiple failed login attempts
    then:
      - Account locked after threshold
      - Notification sent
      - Audit logged

#### Authorization Tests
- id: SEC-[XXX].002
  name: [Privilege escalation prevention]
  scenario:
    given:
      - User with basic role
    when:
      - Attempt to access admin resource
    then:
      - Access denied
      - Attempt logged
      - No information leakage

#### Data Protection Tests
- id: SEC-[XXX].003
  name: [Encryption verification]
  scenario:
    given:
      - Sensitive data in system
    when:
      - Data at rest
    then:
      - Data encrypted with approved algorithm
      - Keys properly managed
      - No plaintext copies

## Incident Response

### Response Plan
```yaml
incident_response:
  team:
    - role: [Incident Commander]
      contact: [contact_method]
    - role: [Security Lead]
      contact: [contact_method]

  severity_levels:
    critical:
      response_time: [minutes]
      escalation: [immediate]
      communication: [executive|customers|public]

    high:
      response_time: [hours]
      escalation: [within_X_hours]
      communication: [stakeholders]

  playbooks:
    - incident_type: [data_breach]
      steps:
        - [Contain]
        - [Investigate]
        - [Remediate]
        - [Recover]
        - [Review]
```

## Monitoring & Audit

### Security Monitoring
```yaml
monitoring:
  events:
    - event: [login_attempt]
      log_level: [info|warn|error]
      retention: [days]
    - event: [permission_change]
      log_level: [warn]
      retention: [days]
    - event: [data_access]
      log_level: [info]
      retention: [days]

  alerts:
    - condition: [failed_logins > threshold]
      action: [notify|block|investigate]
    - condition: [unusual_data_access]
      action: [notify|investigate]

  dashboards:
    - name: [Security Overview]
      metrics:
        - [Failed authentication rate]
        - [Suspicious activity score]
        - [Compliance status]
```

### Audit Requirements
```yaml
audit:
  trail:
    what: [All security events]
    format: [structured|json|syslog]
    integrity: [signed|hash_chain|immutable]
    retention: [years]

  reviews:
    access_review:
      frequency: [quarterly]
      scope: [all_privileged_accounts]

    log_review:
      frequency: [monthly]
      scope: [security_events]
```

## Security Architecture

### Network Security
```yaml
network:
  segmentation:
    - zone: [DMZ|Internal|Restricted]
      access: [Inbound/Outbound rules]

  firewall_rules:
    - source: [source_zone]
      destination: [dest_zone]
      ports: [allowed_ports]
      protocol: [TCP|UDP]
```

### Application Security
```yaml
application:
  input_validation:
    strategy: [whitelist|blacklist]
    encoding: [UTF-8]
    sanitization: [HTML|SQL|NoSQL|Command]

  output_encoding:
    context: [HTML|JSON|XML|URL]
    method: [encode|escape|sanitize]

  error_handling:
    user_messages: [generic]
    detailed_logs: [server_only]
    stack_traces: [never_to_user]
```

## Security Tools & Technologies
- **WAF**: [Web Application Firewall details]
- **SIEM**: [Security Information Event Management]
- **DLP**: [Data Loss Prevention]
- **Secret Management**: [Vault/KMS configuration]
- **Certificate Management**: [PKI details]

## Implementation References
- Security Library: `/src/security/`
- Auth Implementation: `/src/auth/`
- Encryption Utils: `/src/crypto/`
- Audit Logger: `/src/audit/`
- Security Tests: `/tests/security/`

## Compliance Evidence
- **Artifacts Location**: `/compliance/[regulation]/`
- **Audit Reports**: `/audits/[year]/`
- **Pen Test Reports**: `/security/pentests/`

## Uncertainties
[Security questions or concerns to be addressed]

## Security Contacts
- **Security Team**: [Contact]
- **Incident Response**: [24/7 Contact]
- **Compliance Officer**: [Contact]
