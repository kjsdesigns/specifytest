<!--
Template Metadata (used by type registry generator)
type: Message
id_prefix: MSG
name_guidelines: "Message type"
name_examples: ["order_request", "payment_response", "user_notification", "status_update"]
file_extension: md

Validation rules: see .specify/schemas/template-schema.json
-->
<!-- See components/spec-header.md for header format -->
---
id: MESSAGE-[XXX]
name: [descriptive_snake_case_name]
type: Message
status: draft
related: []
hash_timestamp: [ISO_8601_TIMESTAMP]  # Updated on every save (YYYY-MM-DDTHH:MM:SSZ)
---

# {name}

## Purpose
[Describe the purpose of this message type and its role in system communication]

## Message Classification
- **Pattern**: [request_response|command|query|notification|fire_and_forget]
- **Direction**: [request|response|bidirectional]
- **Protocol**: [HTTP|gRPC|AMQP|MQTT|WebSocket|Custom]
- **Synchronicity**: [synchronous|asynchronous]

## Message Definition

### Message Type
- **Name**: `[message.type.name]` (use dot notation, e.g., `order.process`, `user.fetch`)
- **Version**: [SEMVER]  # e.g., 1.0.0
- **Description**: [Detailed description of this message's purpose]

### Use Cases
- [USE_CASE_1]
- [USE_CASE_2]
- [USE_CASE_3]

## Message Schema
<!-- See components/spec-inline-contracts.yaml for schema patterns -->

### Message Structure
```yaml
message_schema:
  message_type: [MESSAGE_TYPE]
  version: "[VERSION]"
  protocol: [HTTP|gRPC|AMQP|MQTT|WebSocket]

  headers:
    message_id:
      type: string
      format: uuid
      required: true
      description: Unique message identifier
      example: "550e8400-e29b-41d4-a716-446655440000"

    message_type:
      type: string
      required: true
      description: Type of message
      example: "[message.type.name]"

    version:
      type: string
      required: true
      description: Schema version
      example: "[VERSION]"

    timestamp:
      type: integer
      format: unix_timestamp
      required: true
      description: When message was created
      example: 1705318200

    correlation_id:
      type: string
      format: uuid
      required: false
      description: Links request with response
      example: "660e8400-e29b-41d4-a716-446655440000"

    reply_to:
      type: string
      required: false
      description: Where to send response (queue/topic name)
      example: "[REPLY_QUEUE_NAME]"

    content_type:
      type: string
      required: true
      values: [application/json, application/xml, application/protobuf]
      example: "application/json"

    priority:
      type: integer
      range: [0-9]
      required: false
      description: Message priority (0=lowest, 9=highest)
      example: 5

    ttl:
      type: integer
      required: false
      description: Time to live in seconds
      example: 300

    custom_header:
      type: string
      required: [true|false]
      description: [CUSTOM_HEADER_PURPOSE]

  body:
    type: object
    format: [json|xml|protobuf|avro]
    required: [REQUIRED_FIELD_1, REQUIRED_FIELD_2]
    properties:
      field1:
        type: [string|number|boolean|object|array]
        description: [FIELD_PURPOSE]
        validation: [VALIDATION_RULES]
        example: "[EXAMPLE_VALUE]"

      field2:
        type: [TYPE]
        description: [FIELD_PURPOSE]
        example: [EXAMPLE_VALUE]
```

## Request Message (if applicable)

### Request Format
```json
{
  "headers": {
    "message_id": "550e8400-e29b-41d4-a716-446655440000",
    "message_type": "[message.type.name].request",
    "version": "[VERSION]",
    "timestamp": 1705318200,
    "correlation_id": "660e8400-e29b-41d4-a716-446655440000",
    "reply_to": "[REPLY_QUEUE]",
    "content_type": "application/json"
  },
  "body": {
    "field1": "example_value",
    "field2": 12345
  }
}
```

### Request Validation
```yaml
validation_rules:
  - field: [FIELD_NAME]
    rules:
      - type: required
        message: "[FIELD_NAME] is required"
      - type: format
        format: [FORMAT]
        message: "[VALIDATION_MESSAGE]"
```

## Response Message (if applicable)

### Response Format
```json
{
  "headers": {
    "message_id": "770e8400-e29b-41d4-a716-446655440000",
    "message_type": "[message.type.name].response",
    "version": "[VERSION]",
    "timestamp": 1705318205,
    "correlation_id": "660e8400-e29b-41d4-a716-446655440000",
    "content_type": "application/json"
  },
  "body": {
    "status": "success|error",
    "data": {
      "result_field1": "value",
      "result_field2": 67890
    },
    "error": {
      "code": "[ERROR_CODE]",
      "message": "[ERROR_MESSAGE]",
      "details": {}
    }
  }
}
```

### Success Response
```yaml
success_response:
  status: success
  data:
    type: object
    properties:
      [RESULT_FIELD]:
        type: [TYPE]
        description: [FIELD_PURPOSE]
```

### Error Response
```yaml
error_response:
  status: error
  error:
    code:
      type: string
      description: Error code
      examples: [INVALID_INPUT, NOT_FOUND, TIMEOUT]
    message:
      type: string
      description: Human-readable error message
    details:
      type: object
      description: Additional error context
```

## Message Transport

### Queue/Topic Configuration
- **Transport**: [Queue|Topic|Direct|Fanout]
- **Name**: `[QUEUE_TOPIC_NAME]`
- **Exchange**: `[EXCHANGE_NAME]` (if using AMQP)
- **Routing Key**: `[ROUTING_KEY]` (if using AMQP)
- **Durability**: [durable|transient]

### Connection Settings
- **Protocol**: [AMQP|MQTT|STOMP|Custom]
- **Host**: [HOST_ADDRESS]
- **Port**: [PORT_NUMBER]
- **Virtual Host**: [VHOST] (if applicable)
- **SSL/TLS**: [enabled|disabled]

### Publisher
- **Service**: [SERVICE_NAME]
- **Component**: [COMPONENT_PATH]
- **Method**: [METHOD_NAME]

### Consumer
- **Service**: [SERVICE_NAME]
- **Component**: [COMPONENT_PATH]
- **Handler**: [HANDLER_METHOD]
- **Concurrency**: [NUMBER] workers
- **Prefetch**: [NUMBER] messages

## Message Processing

### Processing Pattern
- **Pattern**: [one_to_one|one_to_many|many_to_one|publish_subscribe]
- **Acknowledgment**: [auto|manual]
- **Requeue On Error**: [yes|no]

### Idempotency
- **Required**: [yes|no]
- **Idempotency Key**: [message_id|custom_field]
- **Deduplication**: [enabled|disabled]
- **Deduplication Window**: [NUMBER] seconds
- **Deduplication Store**: [database|cache|in_memory]

### Timeout
- **Processing Timeout**: [NUMBER]ms
- **Response Timeout**: [NUMBER]ms (for request/response)
- **Message TTL**: [NUMBER]s

## Retry & Error Handling
<!-- See components/spec-retry-policy.md for detailed patterns -->

### Retry Configuration
```yaml
retry:
  max_attempts: [NUMBER]
  initial_delay_ms: [NUMBER]
  max_delay_ms: [NUMBER]
  strategy: [exponential_backoff|fixed_interval|linear_backoff]
  retry_on: [LIST_OF_RETRYABLE_CONDITIONS]
```

### Dead Letter Queue
- **Enabled**: [yes|no]
- **Queue Name**: `[DLQ_NAME]`
- **Routing**: [direct|after_retries|immediate]
- **Retention**: [NUMBER] days
- **Alert**: [enabled|disabled]

### Error Scenarios
```yaml
error_scenarios:
  - error: [ERROR_TYPE]
    cause: [ERROR_CAUSE]
    handling: [retry|dlq|reject|ignore]
    alert: [yes|no]

  - error: [ANOTHER_ERROR]
    cause: [CAUSE]
    handling: [HANDLING_STRATEGY]
    alert: [yes|no]
```

## Message Ordering

### Ordering Guarantee
- **Ordering**: [strict|per_key|best_effort|none]
- **Partition Key**: [PARTITION_KEY_FIELD] (if using partitioned queues)
- **Sequence Number**: [enabled|disabled]

### Out-of-Order Handling
- **Strategy**: [buffer|reject|accept]
- **Buffer Size**: [NUMBER] messages
- **Buffer Timeout**: [NUMBER]ms

## OPTIONAL: Performance Considerations
<!-- See components/spec-performance.md for detailed patterns -->

### Throughput
- **Expected Rate**: [NUMBER] messages/second
- **Peak Rate**: [NUMBER] messages/second
- **Burst Capacity**: [NUMBER] messages

### Message Size
- **Typical Size**: [NUMBER]KB
- **Max Size**: [NUMBER]KB
- **Compression**: [enabled|disabled]

### Latency
- **P50**: < [NUMBER]ms
- **P95**: < [NUMBER]ms
- **P99**: < [NUMBER]ms

### Resource Limits
- **Connection Pool**: [NUMBER] connections
- **Channel Pool**: [NUMBER] channels
- **Consumer Threads**: [NUMBER]

## OPTIONAL: Monitoring
<!-- See components/spec-monitoring.md for detailed patterns -->

### Metrics
- `[message_type]_sent_total`: Counter of messages sent
- `[message_type]_received_total`: Counter of messages received
- `[message_type]_processing_duration_seconds`: Processing time histogram
- `[message_type]_errors_total`: Counter of processing errors
- `[message_type]_retries_total`: Counter of retry attempts

### Alerts
- **Send Failure**: Alert if send fails > [NUMBER] times/minute
- **Processing Lag**: Alert if unprocessed messages > [NUMBER]
- **DLQ Messages**: Alert on first message in DLQ
- **High Error Rate**: Alert if error rate > [NUMBER]%

## OPTIONAL: Security

### Authentication
- **Auth Method**: [SASL|TLS_Client_Cert|Username_Password|OAuth|API_Key]
- **Credentials**: [CREDENTIAL_LOCATION]

### Authorization
- **Publisher Permissions**: [REQUIRED_PERMISSIONS]
- **Consumer Permissions**: [REQUIRED_PERMISSIONS]

### Encryption
- **In Transit**: [TLS|DTLS|none]
- **At Rest**: [enabled|disabled]
- **Message Signing**: [enabled|disabled]

### Data Sensitivity
- **PII Present**: [yes|no]
- **PII Fields**: [LIST_IF_APPLICABLE]
- **Redaction**: [enabled|disabled]

## Versioning

### Schema Evolution
- **Breaking Changes**: Require major version bump
- **Non-Breaking Additions**: Allow minor version bump
- **Backward Compatibility**: [NUMBER] versions supported

### Version Handling
- **Version in**: [header|body|routing_key]
- **Multiple Versions**: [supported|not_supported]
- **Default Version**: [VERSION]

### Migration Strategy
- **Approach**: [blue_green|canary|gradual_rollout]
- **Rollback Plan**: [ROLLBACK_PROCEDURE]

## Protocol-Specific Details

### For HTTP/REST
- **Endpoint**: [HTTP_ENDPOINT]
- **Method**: [GET|POST|PUT|DELETE|PATCH]
- **Status Codes**: [200, 400, 404, 500]

### For gRPC
- **Service**: [SERVICE_NAME]
- **Method**: [METHOD_NAME]
- **Proto File**: [PATH_TO_PROTO]

### For AMQP
- **Exchange Type**: [direct|topic|fanout|headers]
- **Binding**: [BINDING_CONFIGURATION]

### For MQTT
- **QoS Level**: [0|1|2]
- **Retain**: [yes|no]
- **Clean Session**: [yes|no]

## Message Flow

### Sequence Diagram
```
[SENDER] -->> [QUEUE/TOPIC] : Publish Message
[QUEUE/TOPIC] -->> [CONSUMER] : Deliver Message
[CONSUMER] -->> [CONSUMER] : Process Message
[CONSUMER] -->> [QUEUE/TOPIC] : Acknowledge
alt Success Path
    [CONSUMER] -->> [REPLY_QUEUE] : Send Response (if applicable)
else Error Path
    [CONSUMER] -->> [DLQ] : Send to Dead Letter Queue
end
```

## Business Rules
- [RULE_1]
- [RULE_2]
- [RULE_3]

## Dependencies
- **Upstream Messages**: [MESSAGES_THAT_TRIGGER_THIS]
- **Downstream Messages**: [MESSAGES_THIS_TRIGGERS]
- **External Systems**: [EXTERNAL_DEPENDENCIES]

## OPTIONAL: Testing

### Test Messages
- **Test Message Pattern**: `test-[UUID]`
- **Test Queue**: [TEST_QUEUE_NAME]
- **Mock Consumers**: [MOCK_LOCATION]

### Contract Testing
- **Schema Location**: [SCHEMA_REGISTRY_OR_FILE]
- **Contract Tests**: [TEST_LOCATION]
- **CI Integration**: [enabled|disabled]

<!-- See components/spec-validation-cases.md for validation case format -->
## Validation Cases

### Test Cases
- [ ] [TC-XXX: Test message publishing](/specs/test-cases/TC-XXX.yaml)
- [ ] [TC-XXX: Test message consumption](/specs/test-cases/TC-XXX.yaml)
- [ ] [TC-XXX: Test idempotency](/specs/test-cases/TC-XXX.yaml)
- [ ] [TC-XXX: Test error handling](/specs/test-cases/TC-XXX.yaml)
- [ ] [TC-XXX: Test message validation](/specs/test-cases/TC-XXX.yaml)

### Scenario Cases
- [ ] [SC-XXX: End-to-end message flow](/specs/scenario-cases/SC-XXX.yaml)
- [ ] [SC-XXX: Failure and retry](/specs/scenario-cases/SC-XXX.yaml)

<!-- See components/spec-implementation-refs.md for implementation reference format -->
## Implementation References

- Message definition: `[PATH_TO_MESSAGE_DEFINITION]`
- Publisher: `[PATH_TO_PUBLISHER]`
- Consumer: `[PATH_TO_CONSUMER]`
- Schema: `[PATH_TO_SCHEMA]`
- Tests: `[PATH_TO_TESTS]`

<!-- See components/spec-uncertainties.md for uncertainties format -->
## Uncertainties

- [ ] [DESCRIBE_UNCERTAINTY]

## Related Messages
- **[Related Message 1]** (MESSAGE-XXX): [RELATIONSHIP]
- **[Related Message 2]** (MESSAGE-XXX): [RELATIONSHIP]

## Notes
[Additional notes, considerations, or context]