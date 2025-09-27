<!--
Template Metadata (used by type registry generator)
type: Event
id_prefix: EVENT
name_guidelines: "Event name"
name_examples: ["user_created", "order_placed", "payment_completed", "inventory_updated"]
file_extension: md

Validation rules: see .specify/schemas/template-schema.json
-->
<!-- See components/spec-header.md for header format -->
---
id: EVENT-[XXX]
name: [descriptive_snake_case_name]
type: Event
status: draft
related: []
hash_timestamp: [ISO_8601_TIMESTAMP]  # Updated on every save (YYYY-MM-DDTHH:MM:SSZ)
---

# {name}

## Purpose
[Describe the business purpose of this event and what it represents]

## Event Classification
- **Type**: [domain_event|integration_event|notification_event|command_event]
- **Category**: [user_action|system_action|state_change|external_trigger]
- **Criticality**: [critical|high|medium|low]

## Event Definition

### Event Type
- **Name**: `[event.type.name]` (use dot notation, e.g., `order.created`, `user.updated`)
- **Version**: [SEMVER]  # e.g., 1.0.0
- **Description**: [Detailed description of when this event is emitted]

### Trigger Conditions
This event is published when:
- [CONDITION_1]
- [CONDITION_2]
- [CONDITION_3]

Should NOT be published when:
- [EXCLUSION_CONDITION_1]
- [EXCLUSION_CONDITION_2]

## Event Schema
<!-- See components/spec-inline-contracts.yaml for schema patterns -->

```yaml
event_schema:
  event_type: [EVENT_TYPE_NAME]
  version: "[VERSION]"

  metadata:
    event_id:
      type: string
      format: uuid
      required: true
      description: Unique identifier for this event instance
      example: "550e8400-e29b-41d4-a716-446655440000"

    event_type:
      type: string
      required: true
      description: Type of event
      example: "[event.type.name]"

    event_version:
      type: string
      required: true
      description: Schema version
      example: "[VERSION]"

    timestamp:
      type: string
      format: iso8601
      required: true
      description: When the event occurred (ISO 8601)
      example: "2024-01-15T10:30:00.000Z"

    source:
      type: string
      required: true
      description: Service that produced the event
      example: "[SOURCE_SERVICE]"

    correlation_id:
      type: string
      format: uuid
      required: false
      description: Links related events together
      example: "660e8400-e29b-41d4-a716-446655440000"

    causation_id:
      type: string
      format: uuid
      required: false
      description: ID of the event that caused this event
      example: "770e8400-e29b-41d4-a716-446655440000"

    user_id:
      type: string
      required: false
      description: User who triggered the event (if applicable)
      example: "USER_12345"

    trace_id:
      type: string
      required: false
      description: Distributed tracing identifier
      example: "4bf92f3577b34da6a3ce929d0e0e4736"

    span_id:
      type: string
      required: false
      description: Span identifier within the trace
      example: "00f067aa0ba902b7"

  payload:
    type: object
    required: [REQUIRED_FIELD_1, REQUIRED_FIELD_2]
    properties:
      field1:
        type: [string|number|boolean|object|array]
        description: [FIELD_PURPOSE]
        example: "[EXAMPLE_VALUE]"

      field2:
        type: [TYPE]
        description: [FIELD_PURPOSE]
        example: [EXAMPLE_VALUE]

      before:
        type: object
        description: State before the change (for update events)
        properties:
          [FIELD_NAME]:
            type: [TYPE]
            description: [PREVIOUS_VALUE_DESCRIPTION]

      after:
        type: object
        description: State after the change (for update events)
        properties:
          [FIELD_NAME]:
            type: [TYPE]
            description: [NEW_VALUE_DESCRIPTION]
```

## Event Example

### Valid Event
```json
{
  "metadata": {
    "event_id": "550e8400-e29b-41d4-a716-446655440000",
    "event_type": "[event.type.name]",
    "event_version": "[VERSION]",
    "timestamp": "2024-01-15T10:30:00.000Z",
    "source": "[SOURCE_SERVICE]",
    "correlation_id": "660e8400-e29b-41d4-a716-446655440000",
    "user_id": "USER_12345"
  },
  "payload": {
    "field1": "example_value",
    "field2": 12345
  }
}
```

## Publishing

### Publisher
- **Service**: [SERVICE_NAME]
- **Component**: [COMPONENT_PATH]
- **Method**: [METHOD_NAME]
- **Trigger Point**: [WHERE_IN_CODE_THIS_IS_PUBLISHED]

### Publishing Rules
- **Transactional**: [yes|no] - Publish within database transaction?
- **Async**: [yes|no] - Async publishing (outbox pattern)?
- **Guaranteed**: [at_least_once|at_most_once|exactly_once]
- **Retry**: [NUMBER] attempts on failure
- **Timeout**: [NUMBER]ms

### Outbox Pattern (if applicable)
```yaml
outbox:
  enabled: [true|false]
  table: [OUTBOX_TABLE_NAME]
  polling_interval: [NUMBER]ms
  batch_size: [NUMBER]
  cleanup_after: [NUMBER] hours
```

## Subscription & Routing

### Event Bus Configuration
- **System**: [Kafka|RabbitMQ|EventBridge|PubSub|SNS|SQS|Custom]
- **Topic/Queue**: `[TOPIC_NAME]`
- **Partition Key**: [PARTITION_KEY_FIELD]  # For Kafka/Kinesis
- **Routing Key**: `[ROUTING_KEY]`  # For RabbitMQ

### Subscribers
```yaml
subscribers:
  - service: [SERVICE_NAME_1]
    handler: [HANDLER_COMPONENT]
    purpose: [WHY_THIS_SERVICE_SUBSCRIBES]
    processing: [sync|async]
    idempotent: [yes|no]
    dead_letter: [enabled|disabled]

  - service: [SERVICE_NAME_2]
    handler: [HANDLER_COMPONENT]
    purpose: [WHY_THIS_SERVICE_SUBSCRIBES]
    processing: [sync|async]
    idempotent: [yes|no]
    dead_letter: [enabled|disabled]
```

### Fan-Out Pattern
- **Fan-Out**: [yes|no]
- **Max Subscribers**: [NUMBER|unlimited]
- **Broadcast**: [all|filtered]

## Delivery Guarantees

### Delivery Semantics
- **Guarantee**: [at_least_once|at_most_once|exactly_once]
- **Ordering**: [none|per_partition|per_key|global]
- **Durability**: [persistent|transient]

### Retry Policy
<!-- See components/spec-retry-policy.md for detailed patterns -->
- **Max Retries**: [NUMBER]
- **Backoff**: [exponential|fixed|linear]
- **Initial Delay**: [NUMBER]ms
- **Max Delay**: [NUMBER]ms

### Dead Letter Queue
- **Enabled**: [yes|no]
- **Queue Name**: `[DLQ_NAME]`
- **Retention**: [NUMBER] days
- **Alert On**: [first_message|threshold|always]

## Event Processing

### Consumer Idempotency
- **Idempotency Required**: [yes|no]
- **Idempotency Key**: [event_id|custom_field]
- **Deduplication Window**: [NUMBER] seconds/minutes
- **Deduplication Store**: [database|cache|event_store]

### Processing Guarantees
- **Transactional**: [yes|no]
- **Saga Pattern**: [yes|no]
- **Compensating Actions**: [LIST_IF_APPLICABLE]

### Error Handling
```yaml
error_handling:
  - error_type: [ERROR_TYPE]
    action: [retry|dlq|ignore|alert]
    max_retries: [NUMBER]
    alert: [yes|no]

  - error_type: [ANOTHER_ERROR_TYPE]
    action: [ACTION]
    fallback: [FALLBACK_BEHAVIOR]
```

## Versioning & Evolution

### Schema Evolution Rules
- **Breaking Changes**: Require major version bump
- **Non-Breaking Changes**: Allow minor version bump
- **Backward Compatibility**: [NUMBER] versions supported

### Deprecation Strategy
- **Deprecation Notice**: [NUMBER] months advance notice
- **Support Period**: [NUMBER] months after deprecation
- **Migration Path**: [DESCRIBE_MIGRATION_APPROACH]

### Version History
- **v[VERSION]**: [CHANGE_DESCRIPTION]
- **v[PREVIOUS_VERSION]**: [CHANGE_DESCRIPTION]

## OPTIONAL: Performance Considerations
<!-- See components/spec-performance.md for detailed patterns -->

### Throughput
- **Expected Rate**: [NUMBER] events/second
- **Peak Rate**: [NUMBER] events/second
- **Burst Capacity**: [NUMBER] events

### Size Limits
- **Typical Size**: [NUMBER]KB
- **Max Size**: [NUMBER]KB
- **Compression**: [enabled|disabled]

### Latency
- **Publication**: < [NUMBER]ms
- **Delivery**: < [NUMBER]ms (P95)
- **End-to-End**: < [NUMBER]ms (P95)

## OPTIONAL: Monitoring
<!-- See components/spec-monitoring.md for detailed patterns -->

### Metrics
- `[event_type]_published_total`: Counter of events published
- `[event_type]_consumed_total`: Counter of events consumed
- `[event_type]_processing_duration_seconds`: Processing time histogram
- `[event_type]_errors_total`: Counter of processing errors

### Alerts
- **Publication Failure**: Alert if publication fails > [NUMBER] times/minute
- **Processing Lag**: Alert if lag > [NUMBER] seconds
- **Dead Letter Queue**: Alert on first message in DLQ
- **Schema Validation**: Alert on validation failures

## OPTIONAL: Security Considerations

### Authorization
- **Publisher Auth**: [REQUIRED_PERMISSIONS]
- **Subscriber Auth**: [REQUIRED_PERMISSIONS]
- **Encryption**: [at_rest|in_transit|both|none]

### Data Sensitivity
- **PII Present**: [yes|no]
- **PII Fields**: [LIST_IF_APPLICABLE]
- **Redaction Required**: [yes|no]
- **Retention Period**: [NUMBER] days (GDPR/compliance)

### Audit
- **Audit Trail**: [enabled|disabled]
- **Audit Events**: [all|failures_only|critical_only]
- **Retention**: [NUMBER] days

## Event Sourcing (if applicable)

### Event Store
- **Used**: [yes|no]
- **Event Store**: [STORE_NAME]
- **Aggregate**: [AGGREGATE_NAME]
- **Aggregate ID**: [ID_FIELD]

### Projections
- **Read Models**: [LIST_OF_READ_MODELS]
- **Rebuild Strategy**: [full|incremental]

### Snapshots
- **Enabled**: [yes|no]
- **Frequency**: Every [NUMBER] events
- **Retention**: Last [NUMBER] snapshots

## OPTIONAL: Testing Strategy

### Test Events
- **Test Event ID Pattern**: `test-[UUID]`
- **Test Environment**: Separate topic/queue for testing
- **Mock Publishers**: [YES_OR_NO_AND_LOCATION]

### Contract Testing
- **Schema Registry**: [REGISTRY_LOCATION]
- **Contract Tests**: [TEST_LOCATION]
- **CI Integration**: [enabled|disabled]

## Business Rules

- [RULE_1]
- [RULE_2]
- [RULE_3]

## Dependencies
- **Upstream**: [EVENTS_THAT_TRIGGER_THIS]
- **Downstream**: [EVENTS_THIS_TRIGGERS]
- **External Systems**: [EXTERNAL_DEPENDENCIES]

## OPTIONAL: Migration Notes
[Notes about migrating from old event schema or system]

## Cascade Effects
[Describe what happens in the system when this event is published]

<!-- See components/spec-validation-cases.md for validation case format -->
## Validation Cases

### Test Cases
- [ ] [TC-XXX: Test event publishing](/specs/test-cases/TC-XXX.yaml)
- [ ] [TC-XXX: Test event consumption](/specs/test-cases/TC-XXX.yaml)
- [ ] [TC-XXX: Test idempotency](/specs/test-cases/TC-XXX.yaml)
- [ ] [TC-XXX: Test error handling](/specs/test-cases/TC-XXX.yaml)

### Scenario Cases
- [ ] [SC-XXX: End-to-end event flow](/specs/scenario-cases/SC-XXX.yaml)
- [ ] [SC-XXX: Failure recovery](/specs/scenario-cases/SC-XXX.yaml)

<!-- See components/spec-implementation-refs.md for implementation reference format -->
## Implementation References

- Event definition: `[PATH_TO_EVENT_DEFINITION]`
- Publisher: `[PATH_TO_PUBLISHER]`
- Subscribers: `[PATH_TO_SUBSCRIBERS]`
- Schema: `[PATH_TO_SCHEMA]`
- Tests: `[PATH_TO_TESTS]`

<!-- See components/spec-uncertainties.md for uncertainties format -->
## Uncertainties

- [ ] [DESCRIBE_UNCERTAINTY]

## Related Events
- **[Related Event 1]** (EVENT-XXX): [RELATIONSHIP]
- **[Related Event 2]** (EVENT-XXX): [RELATIONSHIP]