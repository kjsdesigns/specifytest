# Performance Component
<!-- Reference in templates with: See components/spec-performance.md -->

## Performance Requirements

### Service Level Objectives (SLOs)

#### Latency
- **P50 (Median)**: < [NUMBER]ms
- **P95**: < [NUMBER]ms
- **P99**: < [NUMBER]ms
- **P99.9**: < [NUMBER]ms
- **Max Acceptable**: < [NUMBER]ms

#### Throughput
- **Expected RPS**: [NUMBER] requests/second
- **Peak RPS**: [NUMBER] requests/second
- **Sustained RPS**: [NUMBER] requests/second
- **Target Capacity**: [NUMBER] concurrent users/connections

#### Availability
- **Uptime Target**: [NUMBER]% (e.g., 99.9% = 43.2min downtime/month)
- **Error Budget**: [NUMBER]% (100% - uptime target)
- **MTBF**: Mean Time Between Failures = [NUMBER] hours
- **MTTR**: Mean Time To Recovery = [NUMBER] minutes

### Resource Limits

#### Compute
- **CPU**: Average < [NUMBER]%, Peak < [NUMBER]%
- **Memory**: Average < [NUMBER]GB, Peak < [NUMBER]GB
- **Threads**: Max [NUMBER] concurrent threads
- **Processes**: Max [NUMBER] worker processes

#### Storage
- **Disk I/O**: < [NUMBER] IOPS
- **Disk Space**: < [NUMBER]GB
- **Database Connections**: Max [NUMBER] connections
- **Cache Size**: Max [NUMBER]MB

#### Network
- **Bandwidth**: < [NUMBER] Mbps
- **Connections**: Max [NUMBER] concurrent connections
- **Request Size**: Max [NUMBER]KB per request
- **Response Size**: Target < [NUMBER]KB, Max [NUMBER]KB

### Scalability

#### Horizontal Scaling
- **Min Instances**: [NUMBER]
- **Max Instances**: [NUMBER]
- **Scale-Up Trigger**: CPU > [NUMBER]% OR RPS > [NUMBER]
- **Scale-Down Trigger**: CPU < [NUMBER]% AND RPS < [NUMBER]
- **Cool-Down Period**: [NUMBER] minutes between scaling actions

#### Vertical Scaling
- **Current Instance Size**: [INSTANCE_TYPE]
- **Min Instance Size**: [INSTANCE_TYPE]
- **Max Instance Size**: [INSTANCE_TYPE]
- **Scaling Strategy**: [manual|automated|hybrid]

#### Data Scaling
- **Sharding Strategy**: [hash|range|geographic|none]
- **Partition Key**: [PARTITION_KEY_FIELD]
- **Replication**: [master_replica|multi_master|none]
- **Read Replicas**: [NUMBER]

## Performance Optimization

### Caching Strategy

#### Cache Layers
```yaml
caches:
  - level: cdn
    type: edge_cache
    ttl: [NUMBER]s
    hit_ratio_target: > [NUMBER]%
    invalidation: [push|pull|ttl]

  - level: application
    type: in_memory
    implementation: [Redis|Memcached|in-process]
    ttl: [NUMBER]s
    max_size: [NUMBER]MB
    eviction_policy: [LRU|LFU|FIFO]

  - level: database
    type: query_cache
    ttl: [NUMBER]s
    max_entries: [NUMBER]
```

#### Cache Keys
- **Pattern**: `[PREFIX]:[RESOURCE_TYPE]:[IDENTIFIER]:[VERSION]`
- **Example**: `api:user:12345:v2`
- **Vary By**: [user_id, locale, device_type]

#### Cache Invalidation
- **Strategy**: [time_based|event_based|manual|hybrid]
- **TTL**: [NUMBER] seconds
- **Purge Events**: [EVENT_LIST]
- **Stale-While-Revalidate**: [enabled|disabled]

### Database Optimization

#### Query Performance
- **Query Timeout**: [NUMBER]ms
- **Slow Query Threshold**: > [NUMBER]ms
- **Connection Pool Size**: [NUMBER]
- **Prepared Statements**: [enabled|disabled]

#### Indexing Strategy
```yaml
indexes:
  - name: [INDEX_NAME]
    table: [TABLE_NAME]
    columns: [COL_1, COL_2]
    type: [btree|hash|gin|gist]
    purpose: [PURPOSE_DESCRIPTION]
    cardinality: [high|medium|low]

  - name: [COMPOSITE_INDEX_NAME]
    table: [TABLE_NAME]
    columns: [COL_1, COL_2, COL_3]
    order: [COL_1_ASC, COL_2_DESC]
    partial: WHERE [CONDITION]
    purpose: [PURPOSE_DESCRIPTION]
```

#### Query Patterns
- **N+1 Prevention**: Use [eager_loading|joins|batching]
- **Pagination**: [offset|cursor|keyset]
- **Page Size**: Default [NUMBER], Max [NUMBER]
- **Bulk Operations**: Batch size [NUMBER]

### API Optimization

#### Response Optimization
- **Compression**: [gzip|brotli|none]
- **Compression Threshold**: > [NUMBER]KB
- **Field Filtering**: [enabled|disabled] - Allow clients to specify fields
- **Pagination**: [enabled|disabled] - Required for collections
- **Partial Responses**: [enabled|disabled] - Support partial/incremental updates

#### Request Optimization
- **Request Batching**: [enabled|disabled]
- **Max Batch Size**: [NUMBER] operations
- **GraphQL DataLoader**: [enabled|disabled] (if using GraphQL)
- **Debouncing**: [NUMBER]ms client-side debounce recommended

### Frontend Performance

#### Load Time Targets
- **First Contentful Paint (FCP)**: < [NUMBER]s
- **Largest Contentful Paint (LCP)**: < [NUMBER]s
- **Time to Interactive (TTI)**: < [NUMBER]s
- **First Input Delay (FID)**: < [NUMBER]ms
- **Cumulative Layout Shift (CLS)**: < [NUMBER]

#### Optimization Techniques
- [ ] Code splitting / Lazy loading
- [ ] Image optimization (WebP, lazy loading)
- [ ] Asset minification
- [ ] Tree shaking
- [ ] Service worker / PWA
- [ ] Preloading critical resources
- [ ] HTTP/2 or HTTP/3
- [ ] CDN for static assets

## Performance Testing

### Load Testing

#### Test Scenarios
```yaml
scenarios:
  - name: [SCENARIO_NAME]
    type: [load|stress|spike|soak]
    duration: [NUMBER] minutes
    users: [NUMBER] concurrent users
    ramp_up: [NUMBER] seconds
    target_rps: [NUMBER]
    endpoints:
      - path: [ENDPOINT_PATH]
        weight: [NUMBER]%  # Traffic distribution
        payload: [PAYLOAD_DESCRIPTION]
```

#### Success Criteria
- **Latency**: P95 < [NUMBER]ms under load
- **Error Rate**: < [NUMBER]% at target load
- **Throughput**: Sustain [NUMBER] RPS
- **Resource Usage**: CPU < [NUMBER]%, Memory < [NUMBER]GB

### Stress Testing
- **Max Load**: [NUMBER]x normal load
- **Break Point**: Identify at what load system fails
- **Recovery Time**: < [NUMBER] minutes after load reduction

### Endurance Testing
- **Duration**: [NUMBER] hours/days
- **Load**: [NUMBER]% of peak capacity
- **Memory Leak Detection**: Monitor for growth over time
- **Resource Degradation**: Acceptable < [NUMBER]% degradation

## Monitoring & Profiling

### Performance Metrics
```yaml
metrics:
  - name: [OPERATION_NAME_duration]
    type: histogram
    buckets: [0.001, 0.01, 0.1, 0.5, 1, 5, 10]
    labels: [operation, status]

  - name: [RESOURCE_NAME_pool_utilization]
    type: gauge
    description: Resource pool utilization percentage

  - name: [CACHE_NAME_hit_rate]
    type: gauge
    description: Cache hit rate percentage
```

### Profiling
- **CPU Profiling**: [always|on-demand|sampling]
- **Memory Profiling**: [always|on-demand|sampling]
- **Flame Graphs**: [enabled|disabled]
- **Sampling Rate**: [NUMBER]%

### Performance Budgets
```yaml
budgets:
  - resource: javascript
    budget: [NUMBER]KB
    current: [NUMBER]KB
    status: [under|at|over]

  - resource: images
    budget: [NUMBER]KB
    current: [NUMBER]KB

  - resource: total_page_size
    budget: [NUMBER]KB
    current: [NUMBER]KB

  - metric: load_time
    budget: [NUMBER]s
    current: [NUMBER]s
```

## Bottleneck Analysis

### Known Bottlenecks
- **Bottleneck**: [DESCRIPTION]
  - **Impact**: [IMPACT_ON_PERFORMANCE]
  - **Mitigation**: [MITIGATION_STRATEGY]
  - **Status**: [identified|mitigated|accepted]

### Performance Anti-Patterns to Avoid
- [ ] Synchronous external API calls
- [ ] N+1 query problems
- [ ] Large payload transfers
- [ ] Unbounded result sets
- [ ] Missing indexes on query columns
- [ ] Inefficient algorithms (O(n²) or worse)

## Capacity Planning

### Growth Projections
- **Current Load**: [NUMBER] RPS
- **6-Month Projection**: [NUMBER] RPS ([NUMBER]% growth)
- **12-Month Projection**: [NUMBER] RPS ([NUMBER]% growth)
- **Infrastructure**: Scale from [CURRENT] to [PROJECTED] instances

### Cost Optimization
- **Current Cost**: $[NUMBER]/month
- **Cost Per Request**: $[NUMBER]
- **Target Cost Per Request**: $[NUMBER]
- **Optimization Opportunities**: [LIST_OPPORTUNITIES]

## Notes
- Performance requirements should align with user expectations and business needs
- Always measure before and after optimizations
- Consider performance in design phase, not as afterthought
- Document performance assumptions and constraints
- Review and update performance budgets regularly