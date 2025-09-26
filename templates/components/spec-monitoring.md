# Monitoring Component
<!-- Reference in templates with: See components/spec-monitoring.md -->

## Observability Overview

### Monitoring Strategy
- **Approach**: [metrics|logs|traces|distributed_tracing|all]
- **Tools**: [MONITORING_TOOLS]  # e.g., Prometheus, Datadog, New Relic
- **Retention**: [NUMBER] days for metrics, [NUMBER] days for logs

## Metrics

### Key Performance Indicators (KPIs)
- **Availability**: [TARGET]% uptime (e.g., 99.9%)
- **Latency**: P95 < [NUMBER]ms, P99 < [NUMBER]ms
- **Throughput**: [NUMBER] requests/second
- **Error Rate**: < [NUMBER]% errors

### Application Metrics
```yaml
metrics:
  # Request Metrics
  - name: [METRIC_NAME_requests_total]
    type: counter
    labels: [method, endpoint, status]
    description: Total number of requests

  - name: [METRIC_NAME_request_duration_seconds]
    type: histogram
    buckets: [0.001, 0.01, 0.1, 0.5, 1, 5, 10]
    labels: [method, endpoint]
    description: Request duration in seconds

  # Business Metrics
  - name: [METRIC_NAME_operations_total]
    type: counter
    labels: [operation_type, status]
    description: Total business operations

  # Resource Metrics
  - name: [METRIC_NAME_active_connections]
    type: gauge
    description: Number of active connections

  # Error Metrics
  - name: [METRIC_NAME_errors_total]
    type: counter
    labels: [error_type, error_code]
    description: Total errors by type
```

### System Metrics
- **CPU Usage**: Alert if > [NUMBER]%
- **Memory Usage**: Alert if > [NUMBER]%
- **Disk I/O**: Alert if > [NUMBER] IOPS
- **Network I/O**: Alert if > [NUMBER] Mbps

## Logging

### Log Levels
- **FATAL**: System-critical failures requiring immediate action
- **ERROR**: Error conditions that need investigation
- **WARN**: Warning conditions that may need attention
- **INFO**: Normal operational messages
- **DEBUG**: Detailed information for debugging (dev/staging only)

### Structured Logging Format
```json
{
  "timestamp": "2024-01-15T10:30:00.000Z",
  "level": "INFO|ERROR|WARN",
  "service": "[SERVICE_NAME]",
  "trace_id": "[TRACE_ID]",
  "span_id": "[SPAN_ID]",
  "message": "[LOG_MESSAGE]",
  "context": {
    "user_id": "[USER_ID]",
    "request_id": "[REQUEST_ID]",
    "operation": "[OPERATION_NAME]",
    "duration_ms": [NUMBER]
  },
  "error": {
    "type": "[ERROR_TYPE]",
    "message": "[ERROR_MESSAGE]",
    "stack_trace": "[STACK_TRACE]"
  }
}
```

### Log Retention
- **Production**: [NUMBER] days
- **Staging**: [NUMBER] days
- **Development**: [NUMBER] days

### Sensitive Data Handling
- **PII Redaction**: [enabled|disabled]
- **Fields to Redact**: [password, ssn, credit_card, email, phone]
- **Redaction Pattern**: [REDACTED|***|hash]

## Tracing

### Distributed Tracing
- **Tool**: [Jaeger|Zipkin|OpenTelemetry|AWS_X-Ray]
- **Sampling Rate**: [NUMBER]% of requests
- **Trace Context Propagation**: [W3C_Trace_Context|B3|custom]

### Spans to Track
```yaml
spans:
  - name: [SPAN_NAME]
    operation: [OPERATION_TYPE]
    attributes:
      - service.name: [SERVICE_NAME]
      - operation.type: [read|write|query]
      - resource.id: [RESOURCE_IDENTIFIER]
    events:
      - name: [EVENT_NAME]
        attributes: [KEY_VALUE_PAIRS]
```

### Critical Paths
- [PATH_1]: [DESCRIPTION]
- [PATH_2]: [DESCRIPTION]

## Alerts

### Alert Rules

#### Availability Alerts
```yaml
- name: [SERVICE_NAME_down]
  condition: up{job="[SERVICE_NAME]"} == 0
  duration: 1m
  severity: critical
  description: "[SERVICE_NAME] is down"
  action: Page on-call engineer

- name: [SERVICE_NAME_high_error_rate]
  condition: rate(errors_total[5m]) / rate(requests_total[5m]) > 0.05
  duration: 5m
  severity: warning
  description: "Error rate above 5%"
  action: Notify team channel
```

#### Performance Alerts
```yaml
- name: [SERVICE_NAME_high_latency]
  condition: histogram_quantile(0.95, request_duration_seconds) > [NUMBER]
  duration: 10m
  severity: warning
  description: "P95 latency above threshold"
  action: Investigate performance

- name: [SERVICE_NAME_slow_queries]
  condition: query_duration_seconds > [NUMBER]
  duration: 5m
  severity: info
  description: "Slow database queries detected"
  action: Review query performance
```

#### Resource Alerts
```yaml
- name: [SERVICE_NAME_high_memory]
  condition: memory_usage_percent > [NUMBER]
  duration: 5m
  severity: warning
  description: "Memory usage above [NUMBER]%"
  action: Check for memory leaks

- name: [SERVICE_NAME_disk_full]
  condition: disk_usage_percent > [NUMBER]
  duration: 1m
  severity: critical
  description: "Disk usage above [NUMBER]%"
  action: Free up disk space immediately
```

### Alert Routing
- **Critical**: Page on-call engineer via [PAGING_SYSTEM]
- **Warning**: Post to [TEAM_CHANNEL]
- **Info**: Log only, review during business hours

### Escalation Policy
1. **Initial Alert**: On-call engineer notified
2. **After [NUMBER]min**: Escalate to secondary
3. **After [NUMBER]min**: Escalate to engineering manager
4. **After [NUMBER]min**: Escalate to VP Engineering

## Dashboards

### Primary Dashboard
**Panels to Include:**
- Request rate (requests/sec)
- Error rate (%)
- Latency (P50, P95, P99)
- Active connections
- Resource utilization (CPU, Memory)
- Alert status

### Business Dashboard
**Panels to Include:**
- [BUSINESS_METRIC_1] over time
- [BUSINESS_METRIC_2] by region
- Conversion funnel
- Revenue impact metrics

### SLO Dashboard
**Service Level Objectives:**
- **Availability SLO**: [NUMBER]% uptime
- **Latency SLO**: P95 < [NUMBER]ms
- **Error Budget**: [NUMBER]% remaining
- **Time to Detect**: < [NUMBER]min
- **Time to Resolve**: < [NUMBER]min

## Health Checks

### Endpoint Configuration
```yaml
healthcheck:
  path: /health
  interval: 30s
  timeout: 5s
  healthy_threshold: 2
  unhealthy_threshold: 3

readiness:
  path: /ready
  checks:
    - database_connection
    - cache_connection
    - external_api_reachable
    - required_config_loaded

liveness:
  path: /alive
  checks:
    - process_responsive
    - no_deadlocks
```

### Health Check Response Format
```json
{
  "status": "healthy|degraded|unhealthy",
  "timestamp": "2024-01-15T10:30:00.000Z",
  "checks": {
    "database": {
      "status": "healthy",
      "latency_ms": 5
    },
    "cache": {
      "status": "healthy",
      "latency_ms": 2
    },
    "external_api": {
      "status": "degraded",
      "latency_ms": 150,
      "message": "High latency detected"
    }
  }
}
```

## Incident Response

### Runbooks
- **Location**: [RUNBOOK_LOCATION]
- **Format**: [Markdown|Wiki|Confluence]
- **Update Frequency**: After each incident

### On-Call Rotation
- **Schedule**: [ROTATION_SCHEDULE]  # e.g., weekly, 24/7
- **Handoff Process**: [HANDOFF_PROCEDURE]
- **Escalation Path**: [ESCALATION_CONTACTS]

## Continuous Improvement

### Post-Incident Reviews
- **Frequency**: After every [severity_level] incident
- **Participants**: [TEAM_ROLES]
- **Action Items**: Track in [TRACKING_SYSTEM]

### Monitoring Reviews
- **Frequency**: [weekly|monthly|quarterly]
- **Focus**: Alert noise, false positives, missing monitors
- **Owner**: [TEAM_OR_ROLE]

## Notes
- Review alert thresholds regularly to reduce false positives
- Ensure all critical paths have tracing
- Test alert routing during business hours
- Keep runbooks up-to-date with actual procedures