<!--
Template Metadata (used by type registry generator)
type: Configuration
id_prefix: CFG
name_guidelines: "Configuration area or setting"
name_examples: ["database_config", "api_keys", "feature_flags", "env_variables"]
file_extension: md

Validation rules: see .specify/schemas/template-schema.json
-->
<!-- See components/spec-header.md for header format -->
---
id: CFG-[XXX]
name: [descriptive_snake_case_name]
type: Configuration
status: draft
related: []
hash_timestamp: [ISO_8601_TIMESTAMP]  # Updated on every save
---

# {name}

## Configuration Purpose
[Why this configuration exists and what it controls]

## Configuration Scope
- **Applies To**: [Components/services affected]
- **Environments**: [Which environments use this config]
- **Override Hierarchy**: [How configs cascade/override]

## Environment Variables
```yaml
environment_variables:
  # Core Settings
  - name: NODE_ENV
    type: string
    required: true
    default: development
    values: [development, staging, production]
    description: Application environment

  - name: PORT
    type: number
    required: false
    default: 3000
    validation: range(1024, 65535)
    description: Server port

  - name: DATABASE_URL
    type: string
    required: true
    secret: true
    format: postgresql://[user]:[password]@[host]:[port]/[database]
    description: PostgreSQL connection string

  - name: REDIS_URL
    type: string
    required: true
    secret: true
    format: redis://[user]:[password]@[host]:[port]
    description: Redis connection string

  # Feature Flags
  - name: FEATURE_[FEATURE_NAME]
    type: boolean
    required: false
    default: false
    description: Enable/disable feature
```

## Application Configuration
```yaml
application:
  # Server Configuration
  server:
    host: ${HOST:-0.0.0.0}
    port: ${PORT:-3000}
    timeout:
      request: 30000
      keepAlive: 5000
    cors:
      enabled: true
      origins: ${CORS_ORIGINS:-*}
      credentials: true

  # Database Configuration
  database:
    url: ${DATABASE_URL}
    pool:
      min: 2
      max: 10
      idle: 10000
      acquire: 30000
    migrations:
      auto: ${AUTO_MIGRATE:-false}
      directory: /migrations

  # Cache Configuration
  cache:
    provider: redis
    url: ${REDIS_URL}
    ttl:
      default: 300
      session: 3600
      static: 86400
    prefix: ${CACHE_PREFIX:-app}

  # Logging Configuration
  logging:
    level: ${LOG_LEVEL:-info}
    format: ${LOG_FORMAT:-json}
    transports:
      - console
      - ${LOG_FILE:-/var/log/app.log}
    sensitive_fields:
      - password
      - token
      - api_key
```

## Feature Flags
```yaml
feature_flags:
  - name: copilotkit_integration
    description: Enable CopilotKit for chat interface
    default: true
    environments:
      development: true
      staging: true
      production: true
    rollout:
      strategy: percentage
      value: 100

  - name: media_generation
    description: Enable AI media generation
    default: true
    environments:
      development: true
      staging: true
      production: true
    dependencies:
      - imagen_api
      - suno_api

  - name: public_stories
    description: Allow stories to be made public
    default: false
    environments:
      development: true
      staging: true
      production: false
    rollout:
      strategy: user_group
      groups: [beta_testers, staff]

  - name: upload_images
    description: Allow user image uploads
    default: true
    constraints:
      max_file_size: 10MB
      allowed_types: [jpg, png, webp, gif]
```

## Service Endpoints
```yaml
services:
  internal:
    api:
      development: http://localhost:3000/api
      staging: https://staging-api.example.com
      production: https://api.example.com

    graphql:
      development: http://localhost:3000/graphql
      staging: https://staging-api.example.com/graphql
      production: https://api.example.com/graphql

  external:
    openai:
      base_url: https://api.openai.com/v1
      timeout: 30000
      retry: 3

    imagen:
      base_url: ${IMAGEN_API_URL}
      timeout: 60000
      retry: 2

    suno:
      base_url: ${SUNO_API_URL}
      timeout: 180000
      retry: 1
```

## Security Configuration
```yaml
security:
  # Authentication
  auth:
    provider: ${AUTH_PROVIDER:-nextauth}
    session:
      secret: ${SESSION_SECRET}
      duration: 86400
      refresh: true
    jwt:
      secret: ${JWT_SECRET}
      algorithm: HS256
      expiration: 3600

  # API Security
  api:
    rate_limiting:
      enabled: true
      provider: redis
      limits:
        anonymous: 10/minute
        authenticated: 100/minute
        premium: 500/minute

    cors:
      origins: ${CORS_ORIGINS}
      methods: [GET, POST, PUT, DELETE, PATCH]
      headers: [Content-Type, Authorization]
      credentials: true

  # Secrets Management
  secrets:
    provider: ${SECRET_PROVIDER:-env}
    vault:
      url: ${VAULT_URL}
      namespace: ${VAULT_NAMESPACE}
      auth_method: token
```

## Performance Configuration
```yaml
performance:
  # Caching
  caching:
    strategy: ${CACHE_STRATEGY:-redis}
    layers:
      - name: memory
        size: 100MB
        ttl: 60
      - name: redis
        ttl: 300
      - name: cdn
        ttl: 3600

  # Connection Pooling
  pools:
    database:
      min: ${DB_POOL_MIN:-2}
      max: ${DB_POOL_MAX:-10}
    redis:
      min: ${REDIS_POOL_MIN:-1}
      max: ${REDIS_POOL_MAX:-5}

  # Throttling
  throttling:
    cpu_threshold: 80
    memory_threshold: 90
    action: [scale, alert, throttle]
```

## Monitoring Configuration
```yaml
monitoring:
  # Metrics
  metrics:
    enabled: ${METRICS_ENABLED:-true}
    provider: ${METRICS_PROVIDER:-prometheus}
    port: 9090
    interval: 10000

  # Tracing
  tracing:
    enabled: ${TRACING_ENABLED:-false}
    provider: ${TRACING_PROVIDER:-jaeger}
    sampling_rate: 0.1
    endpoint: ${JAEGER_ENDPOINT}

  # Health Checks
  health:
    endpoint: /health
    checks:
      - name: database
        critical: true
        timeout: 5000
      - name: redis
        critical: false
        timeout: 2000
      - name: external_apis
        critical: false
        timeout: 10000

  # Alerts
  alerts:
    provider: ${ALERT_PROVIDER:-email}
    channels:
      - email: ${ALERT_EMAIL}
      - slack: ${SLACK_WEBHOOK}
    rules:
      - metric: error_rate
        threshold: 0.05
        severity: warning
      - metric: response_time_p99
        threshold: 2000
        severity: critical
```

## Deployment Configuration
```yaml
deployment:
  # Container Configuration
  container:
    image: ${DOCKER_IMAGE:-app:latest}
    registry: ${DOCKER_REGISTRY}
    resources:
      limits:
        memory: ${MEMORY_LIMIT:-512Mi}
        cpu: ${CPU_LIMIT:-500m}
      requests:
        memory: ${MEMORY_REQUEST:-256Mi}
        cpu: ${CPU_REQUEST:-250m}

  # Scaling Configuration
  scaling:
    min_replicas: ${MIN_REPLICAS:-1}
    max_replicas: ${MAX_REPLICAS:-10}
    metrics:
      - type: cpu
        target: 70
      - type: memory
        target: 80
      - type: requests_per_second
        target: 1000

  # Update Strategy
  update:
    strategy: ${UPDATE_STRATEGY:-rolling}
    max_surge: 1
    max_unavailable: 0
    health_check_interval: 10
```

## Configuration Validation
```yaml
validation:
  rules:
    - field: NODE_ENV
      rule: enum(development, staging, production)
      required: true

    - field: DATABASE_URL
      rule: regex(^postgresql://.*$)
      required: true

    - field: PORT
      rule: range(1024, 65535)
      required: false

    - field: LOG_LEVEL
      rule: enum(debug, info, warn, error)
      required: false

  on_invalid:
    action: [fail, warn, use_default]
    log: true
```

## Migration Strategy
```yaml
migration:
  from_version: [previous_version]
  to_version: [current_version]

  changes:
    - type: [add|remove|modify|rename]
      field: [config_field]
      migration:
        script: [migration_script]
        rollback: [rollback_script]

  compatibility:
    backward: [true|false]
    forward: [true|false]
    deprecation_period: [days]
```

## Environment-Specific Overrides

### Development
```yaml
development:
  logging:
    level: debug
  cache:
    enabled: false
  security:
    csrf: false
```

### Staging
```yaml
staging:
  logging:
    level: info
  monitoring:
    sampling_rate: 1.0
```

### Production
```yaml
production:
  logging:
    level: warn
  cache:
    ttl: 3600
  security:
    strict: true
```

## Configuration Management

### Storage
- **Location**: [Where configs are stored]
- **Format**: [YAML|JSON|ENV]
- **Encryption**: [At rest encryption details]

### Access Control
- **Read Access**: [Who can read]
- **Write Access**: [Who can modify]
- **Audit**: [Change tracking]

### Versioning
- **Strategy**: [How configs are versioned]
- **Rollback**: [Rollback procedure]

<!-- See components/spec-validation-cases.md for validation case format -->
## Validation Cases

### Test Cases
- [ ] [TC-XXX: Test description](/specs/test-cases/TC-XXX.yaml)

### Scenario Cases
- [ ] [SC-XXX: Scenario description](/specs/scenario-cases/SC-XXX.yaml)

<!-- See components/spec-implementation-refs.md for implementation reference format -->
## Implementation References

- Main implementation: `[path/to/implementation]`
- Tests: `[path/to/tests]`
- Configuration: `[path/to/config]`

<!-- See components/spec-uncertainties.md for uncertainties format -->
## Uncertainties

- [ ] [Describe uncertainty or question]