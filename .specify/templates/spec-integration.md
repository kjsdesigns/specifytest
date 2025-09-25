---
id: INT-[XXX]
type: Integration
name: [Integration Name]
status: draft
service: [Service Name]
related: []
---
# {name}

## Service Overview
[Brief description of the external service and its purpose in the system]

## Integration Type
- **Protocol**: [REST/GraphQL/WebSocket/gRPC]
- **Authentication**: [API Key/OAuth/JWT/Basic]
- **Data Format**: [JSON/XML/Binary]
- **Communication**: [Synchronous/Asynchronous]

## Service Configuration
```yaml
service:
  name: [service_name]
  version: [version]
  base_url: [production_url]
  environments:
    development: [dev_url]
    staging: [staging_url]
    production: [prod_url]

authentication:
  type: [api_key|oauth|jwt|basic]
  config:
    key_location: [header|query|body]
    key_name: [Authorization|X-API-Key|etc]
    token_refresh: [true|false]
    expires_in: [seconds]

timeouts:
  connect: [ms]
  read: [ms]
  write: [ms]
  total: [ms]
```

## Rate Limits
```yaml
rate_limits:
  requests_per_second: [number]
  requests_per_minute: [number]
  requests_per_hour: [number]
  burst_size: [number]

throttling:
  strategy: [fixed_window|sliding_window|token_bucket]
  retry_after: [seconds]
  backoff_multiplier: [number]
```

## Retry Policy
```yaml
retry:
  max_attempts: [number]
  initial_delay: [ms]
  max_delay: [ms]
  backoff: [exponential|linear|fixed]
  jitter: [true|false]
  retry_on:
    - [status_code]
    - [status_code]
  retry_conditions:
    - [network_error]
    - [timeout]
    - [service_unavailable]
```

## Circuit Breaker
```yaml
circuit_breaker:
  enabled: [true|false]
  failure_threshold: [number]
  success_threshold: [number]
  timeout: [seconds]
  half_open_requests: [number]

monitoring:
    metrics_enabled: [true|false]
    alert_on_open: [true|false]
```

## API Endpoints

### [Endpoint Name]
```yaml
endpoint:
  path: [/path/to/endpoint]
  method: [GET|POST|PUT|DELETE|PATCH]
  description: [What this endpoint does]

request:
  headers:
    - name: [header_name]
      required: [true|false]
      value: [value_or_pattern]

  parameters:
    - name: [param_name]
      in: [query|path|header]
      type: [string|number|boolean]
      required: [true|false]
      description: [description]

  body:
    content_type: [application/json]
    schema:
      $ref: '#/components/schemas/[SchemaName]'

response:
  success:
    status: [200|201|204]
    content_type: [application/json]
    schema:
      $ref: '#/components/schemas/[ResponseSchema]'

  errors:
    '400':
      description: [Bad Request]
      schema:
        $ref: '#/components/schemas/Error'
    '429':
      description: [Rate Limited]
      retry_after: [header_name]

performance:
  p50: < [ms]
  p95: < [ms]
  p99: < [ms]
```

## Data Mappings

### Inbound Mapping
```yaml
inbound:
  - external_field: [their_field_name]
    internal_field: [our_field_name]
    transform: [transformation_function]
    required: [true|false]
```

### Outbound Mapping
```yaml
outbound:
  - internal_field: [our_field_name]
    external_field: [their_field_name]
    transform: [transformation_function]
    default: [default_value]
```

## Error Handling
```yaml
error_mapping:
  - external_code: [their_error_code]
    internal_code: [our_error_code]
    message: [user_friendly_message]
    action: [retry|fail|fallback]

fallback_behavior:
  strategy: [cache|default|queue|circuit_break]
  cache_ttl: [seconds]
  default_response: [response_object]
```

## Monitoring & Observability
```yaml
monitoring:
  metrics:
    - request_count
    - error_rate
    - response_time
    - throughput

  logging:
    level: [debug|info|warn|error]
    include_headers: [true|false]
    include_body: [true|false]
    mask_sensitive: [true|false]

  alerts:
    - condition: error_rate > [threshold]
      severity: [critical|warning|info]
      channel: [email|slack|pagerduty]
    - condition: response_time > [ms]
      severity: [warning]
```

## Cost Management
```yaml
costs:
  pricing_model: [per_request|per_gb|per_minute|subscription]

  tiers:
    - name: [tier_name]
      limit: [number]
      cost: [amount]
      unit: [request|gb|minute]

  budget:
    monthly_limit: [amount]
    alert_at: [percentage]
    hard_stop: [true|false]
```

## Security Considerations
- **Data Encryption**: [In transit/At rest requirements]
- **Secret Management**: [How API keys/secrets are stored]
- **Audit Logging**: [What is logged for compliance]
- **Data Retention**: [How long external data is cached]
- **GDPR/Privacy**: [Data handling requirements]

## Testing Strategy
```yaml
testing:
  unit_tests:
    mock_responses: [true|false]
    fixtures_location: [/path/to/fixtures]

  integration_tests:
    use_sandbox: [true|false]
    sandbox_url: [url]
    test_credentials: [vault_path]

  contract_tests:
    provider: [service_name]
    pact_location: [/path/to/pacts]
```

## Dependencies
- **Internal Services**: [List of our services that depend on this]
- **Libraries**: [Client libraries used]
- **Infrastructure**: [Required infrastructure components]

## Migration & Versioning
```yaml
versioning:
  strategy: [header|url|query]
  current: [v1]
  supported: [v1, v2]
  deprecation_schedule:
    v1: [date]
```

## SLA Requirements
- **Availability**: [99.9%]
- **Response Time**: [p99 < Xms]
- **Error Rate**: [< X%]
- **Support Hours**: [24/7|Business hours]

## Documentation
- **API Docs**: [URL to external API documentation]
- **Client Library**: [URL to client library if available]
- **Support Contact**: [Email/URL for support]

## Validation Cases

### Test Cases
References to standalone test cases by file path that validate this spec:
- /test-cases/TC-001.yaml: [Brief description of what this test validates]
- /test-cases/TC-002.yaml: [Brief description of what this test validates]
- /test-cases/TC-003.yaml: [Brief description of what this test validates]

### Scenario Cases
References to end-to-end scenarios by file path involving this spec:
- /scenario-cases/SC-001.yaml: [Brief description of the scenario]
- /scenario-cases/SC-002.yaml: [Brief description of the scenario]

### Notes
- Test cases are defined in `/test-cases/` directory
- Scenario cases are defined in `/scenario-cases/` directory
- Precondition cases referenced by tests are in `/precondition-cases/` directory

## Implementation References
- Client Library: `/src/integrations/[service_name]/`
- Configuration: `/config/integrations/[service_name].yaml`
- Mocks: `/tests/mocks/[service_name]/`
- Monitoring Dashboard: [URL to dashboard]

## Uncertainties
[List any uncertainties about the integration]
