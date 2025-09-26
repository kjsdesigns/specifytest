# Retry Policy Component
<!-- Reference in templates with: See components/spec-retry-policy.md -->

## Retry Configuration

### Retry Strategy
- **Strategy**: [exponential_backoff|fixed_interval|linear_backoff]
- **Max Attempts**: [NUMBER] retries
- **Initial Delay**: [NUMBER]ms
- **Max Delay**: [NUMBER]ms
- **Backoff Multiplier**: [NUMBER]x (for exponential/linear strategies)

### Retry Conditions
Retry on the following conditions:
- [ ] Network timeouts
- [ ] Connection errors
- [ ] HTTP 5xx errors
- [ ] HTTP 429 (rate limit)
- [ ] HTTP 408 (request timeout)
- [ ] Specific error codes: [[ERROR_CODE_1], [ERROR_CODE_2]]

### Non-Retryable Conditions
Do NOT retry on:
- [ ] HTTP 4xx errors (except 408, 429)
- [ ] Authentication failures (401, 403)
- [ ] Validation errors (400)
- [ ] Specific business logic errors: [[ERROR_CODE_1]]

### Idempotency
- **Idempotent Operations**: [true|false]
- **Idempotency Key**: [HEADER_NAME or N/A]
- **Notes**: [IDEMPOTENCY_CONSIDERATIONS]

## Circuit Breaker Configuration

### Thresholds
- **Failure Threshold**: [NUMBER] failures to trip circuit
- **Success Threshold**: [NUMBER] successes to close circuit
- **Timeout**: [NUMBER]ms for circuit breaker timeout
- **Half-Open Requests**: [NUMBER] test requests when half-open

### States
- **Closed**: Normal operation, requests flow through
- **Open**: Circuit tripped, requests fail fast
- **Half-Open**: Testing if service recovered

### Monitoring
- **Failure Rate Window**: [NUMBER]s rolling window
- **Volume Threshold**: Minimum [NUMBER] requests before evaluating
- **Error Rate Threshold**: Open circuit at [NUMBER]% error rate

## Fallback Strategy

### Fallback Options
- **Strategy**: [cache|default_value|degraded_mode|fail_fast|alternate_service]
- **Cache TTL**: [NUMBER]s (if using cached response)
- **Default Value**: [DEFAULT_RESPONSE] (if returning default)
- **Alternate Service**: [SERVICE_URL] (if using backup)

### Fallback Behavior
```
IF circuit_open OR max_retries_exceeded:
  [DESCRIBE_FALLBACK_BEHAVIOR]
```

## Rate Limiting

### Limits
- **Requests Per Second**: [NUMBER]
- **Requests Per Minute**: [NUMBER]
- **Burst Capacity**: [NUMBER] requests
- **Scope**: [per_user|per_ip|per_api_key|global]

### Rate Limit Headers
- `X-RateLimit-Limit`: Total requests allowed
- `X-RateLimit-Remaining`: Requests remaining in window
- `X-RateLimit-Reset`: Unix timestamp when limit resets
- `Retry-After`: Seconds until retry allowed (on 429 response)

## Timeout Configuration

### Timeouts
- **Connection Timeout**: [NUMBER]ms - Time to establish connection
- **Read Timeout**: [NUMBER]ms - Time to receive response
- **Total Timeout**: [NUMBER]ms - End-to-end request timeout

### Deadline Propagation
- **Enable Deadline**: [true|false]
- **Header**: [DEADLINE_HEADER_NAME] (e.g., X-Request-Deadline)
- **Format**: [ISO_8601|unix_timestamp|relative_ms]

## Monitoring & Alerting

### Metrics to Track
- [ ] Retry attempt count
- [ ] Circuit breaker state changes
- [ ] Fallback invocation count
- [ ] Rate limit hits
- [ ] Timeout occurrences
- [ ] Overall success/failure rate
- [ ] P50, P95, P99 latencies

### Alert Conditions
- **High Retry Rate**: > [NUMBER]% requests require retries
- **Circuit Open**: Circuit breaker stays open > [NUMBER]s
- **High Failure Rate**: > [NUMBER]% failures after retries
- **Rate Limit Exceeded**: > [NUMBER] rate limit hits per minute

## Example Configuration

```yaml
retry:
  max_attempts: 3
  initial_delay_ms: 100
  max_delay_ms: 5000
  strategy: exponential_backoff
  multiplier: 2
  retry_on: [timeout, 5xx, 429]

circuit_breaker:
  failure_threshold: 5
  success_threshold: 2
  timeout_ms: 60000
  half_open_requests: 1

fallback:
  strategy: cache
  cache_ttl_seconds: 300

rate_limit:
  requests_per_minute: 100
  burst: 20
  scope: per_user

timeout:
  connection_ms: 3000
  read_ms: 10000
  total_ms: 15000
```

## Notes
- Adjust retry delays based on SLA requirements
- Circuit breaker prevents cascading failures
- Always log retry attempts for debugging
- Consider distributed rate limiting for scaled systems
- Test fallback behavior thoroughly