# Queue Design (RabbitMQ) - AI Camera Counting System

## 📊 Tổng quan

Tài liệu này mô tả thiết kế queue RabbitMQ cho hệ thống AI Camera Counting, bao gồm các exchange, queue, routing patterns, message formats, và các chiến lược xử lý message đáng tin cậy.

## 🎯 Mục tiêu queue

- **Reliability**: Đảm bảo message delivery 99.99%
- **Scalability**: Hỗ trợ hàng nghìn messages/second
- **Performance**: Latency < 100ms cho message processing
- **Fault Tolerance**: Automatic recovery và retry mechanisms
- **Monitoring**: Real-time queue monitoring và alerting

## 🏗️ Queue Architecture Overview

### High-Level Queue Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              QUEUE ARCHITECTURE OVERVIEW                        │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              PRODUCER LAYER                                │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Camera    │  │   Worker    │  │   API       │  │   System    │        │ │
│  │  │   Services  │  │   Services  │  │   Gateway   │  │   Services  │        │ │
│  │  │             │  │             │  │             │  │             │        │ │
│  │  │ • Frame     │  │ • Detection │  │ • User      │  │ • Analytics │        │ │
│  │  │   Events    │  │   Results   │  │   Actions   │  │   Jobs      │        │ │
│  │  │ • Status    │  │ • Processing│  │ • Alerts    │  │ • Reports   │        │ │
│  │  │   Updates   │  │   Events    │  │ • Notifications│ • Maintenance│        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                             │
│                                    ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              EXCHANGE LAYER                                │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Camera    │  │   Analytics │  │   System    │  │   Dead      │        │ │
│  │  │   Exchange  │  │   Exchange  │  │   Exchange  │  │   Letter    │        │ │
│  │  │             │  │             │  │             │  │   Exchange  │        │ │
│  │  │ • Direct    │  │ • Topic     │  │ • Fanout    │  │ • Direct    │        │ │
│  │  │ • Routing   │  │ • Pattern   │  │ • Broadcast │  │ • Error     │        │ │
│  │  │ • Priority  │  │ • Wildcard  │  │ • Events    │  │ • Handling  │        │ │
│  │  │ • Filtering │  │ • Routing   │  │ • Alerts    │  │ • Recovery  │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                             │
│                                    ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              QUEUE LAYER                                   │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Camera    │  │   Analytics │  │   Notification│  │   Dead      │        │ │
│  │  │   Queues    │  │   Queues    │  │   Queues    │  │   Letter    │        │ │
│  │  │             │  │             │  │             │  │   Queues    │        │ │
│  │  │ • Frame     │  │ • Processing│  │ • Email     │  │ • Failed    │        │ │
│  │  │   Processing│  │ • Aggregation│  │ • SMS       │  │   Messages  │        │ │
│  │  │ • Detection │  │ • Reporting │  │ • Webhook   │  │ • Retry     │        │ │
│  │  │   Results   │  │ • Export    │  │ • Push      │  │   Queue     │        │ │
│  │  │ • Status    │  │ • Backup    │  │ • Slack     │  │ • Error     │        │ │
│  │  │   Updates   │  │ • Archive   │  │ • Teams     │  │   Log       │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                             │
│                                    ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              CONSUMER LAYER                                │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   AI Model  │  │   Analytics │  │   Notification│  │   Monitoring│        │ │
│  │  │   Workers   │  │   Workers   │  │   Workers   │  │   Workers   │        │ │
│  │  │             │  │             │  │             │  │             │        │ │
│  │  │ • Detection │  │ • Data      │  │ • Email     │  │ • Health    │        │ │
│  │  │   Engine    │  │   Processing│  │   Service   │  │   Checks    │        │ │
│  │  │ • Counting  │  │ • Report    │  │ • SMS       │  │ • Metrics   │        │ │
│  │  │   Logic     │  │   Generator │  │   Service   │  │ • Alerts    │        │ │
│  │  │ • Tracking  │  │ • Export    │  │ • Webhook   │  │ • Logging   │        │ │
│  │  │   Algorithm │  │   Service   │  │   Service   │  │ • Recovery  │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Message Flow Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              MESSAGE FLOW ARCHITECTURE                          │
│                                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐      │
│  │   Producer  │    │   Exchange  │    │   Queue     │    │   Consumer  │      │
│  │   (Camera)  │    │   (Router)  │    │   (Buffer)  │    │   (Worker)  │      │
│  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘      │
│         │                   │                   │                   │          │
│         │ 1. Publish        │                   │                   │          │
│         │ Message           │                   │                   │          │
│         │ (Frame Data)      │                   │                   │          │
│         │──────────────────►│                   │                   │          │
│         │                   │                   │                   │          │
│         │                   │ 2. Route          │                   │          │
│         │                   │ Message           │                   │          │
│         │                   │ (Routing Key)     │                   │          │
│         │                   │──────────────────►│                   │          │
│         │                   │                   │                   │          │
│         │                   │                   │ 3. Store          │          │
│         │                   │                   │ Message           │          │
│         │                   │                   │ (Persistent)      │          │
│         │                   │                   │──────────────────►│          │
│         │                   │                   │                   │          │
│         │                   │                   │ 4. Consume        │          │
│         │                   │                   │ Message           │          │
│         │                   │                   │ (Process)         │          │
│         │                   │                   │──────────────────►│          │
│         │                   │                   │                   │          │
│         │                   │                   │ 5. Acknowledge    │          │
│         │                   │                   │ (Success/Failure)│          │
│         │                   │                   │◄──────────────────┤          │
│         │                   │                   │                   │          │
│         │                   │                   │ 6. Retry/Dead     │          │
│         │                   │                   │ Letter            │          │
│         │                   │                   │ (If Failed)       │          │
│         │                   │                   │◄──────────────────┤          │
│         │                   │                   │                   │          │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 📋 Exchange Types

### 1. Camera Exchange (Direct)

**Mục đích**: Route camera events đến specific queues.

**Configuration**:
```javascript
const cameraExchange = {
  name: 'camera.events',
  type: 'direct',
  durable: true,
  autoDelete: false,
  arguments: {
    'x-message-ttl': 300000, // 5 minutes
    'x-max-length': 10000
  }
};
```

**Routing Keys**:
- `camera.frame.{camera_id}` - Frame processing
- `camera.detection.{camera_id}` - Detection results
- `camera.status.{camera_id}` - Status updates
- `camera.error.{camera_id}` - Error events

### 2. Analytics Exchange (Topic)

**Mục đích**: Route analytics jobs với pattern matching.

**Configuration**:
```javascript
const analyticsExchange = {
  name: 'analytics.jobs',
  type: 'topic',
  durable: true,
  autoDelete: false,
  arguments: {
    'x-message-ttl': 3600000, // 1 hour
    'x-max-length': 5000
  }
};
```

**Routing Keys**:
- `analytics.hourly.{camera_id}` - Hourly analytics
- `analytics.daily.{camera_id}` - Daily analytics
- `analytics.weekly.{camera_id}` - Weekly analytics
- `analytics.monthly.{camera_id}` - Monthly analytics
- `analytics.report.{report_type}` - Report generation

### 3. System Exchange (Fanout)

**Mục đích**: Broadcast system events đến tất cả consumers.

**Configuration**:
```javascript
const systemExchange = {
  name: 'system.events',
  type: 'fanout',
  durable: true,
  autoDelete: false,
  arguments: {
    'x-message-ttl': 60000 // 1 minute
  }
};
```

**Events**:
- `system.maintenance` - Maintenance events
- `system.alert` - System alerts
- `system.health` - Health checks
- `system.config` - Configuration updates

### 4. Dead Letter Exchange (Direct)

**Mục đích**: Handle failed messages và retry logic.

**Configuration**:
```javascript
const deadLetterExchange = {
  name: 'dead.letter',
  type: 'direct',
  durable: true,
  autoDelete: false
};
```

**Routing Keys**:
- `dead.letter.retry` - Messages for retry
- `dead.letter.error` - Failed messages
- `dead.letter.discard` - Discarded messages

## 📋 Queue Categories

### 1. Camera Event Queues

#### Frame Processing Queue

**Mục đích**: Xử lý frame data từ camera streams.

**Configuration**:
```javascript
const frameProcessingQueue = {
  name: 'camera.frame.processing',
  durable: true,
  autoDelete: false,
  arguments: {
    'x-message-ttl': 300000, // 5 minutes
    'x-max-length': 1000,
    'x-overflow': 'drop-head',
    'x-dead-letter-exchange': 'dead.letter',
    'x-dead-letter-routing-key': 'dead.letter.retry',
    'x-max-priority': 10
  }
};
```

**Message Format**:
```json
{
  "message_id": "uuid-12345",
  "camera_id": 1,
  "zone_id": 2,
  "timestamp": "2024-01-15T10:30:00Z",
  "frame_data": {
    "frame_id": "frame-12345",
    "image_data": "base64-encoded-image",
    "resolution": {
      "width": 1920,
      "height": 1080
    },
    "fps": 25,
    "quality": 0.95
  },
  "metadata": {
    "processing_priority": 5,
    "retry_count": 0,
    "source": "camera_stream"
  }
}
```

**Consumer Configuration**:
```javascript
const frameConsumer = {
  queue: 'camera.frame.processing',
  prefetch: 1,
  noAck: false,
  exclusive: false,
  priority: 5
};
```

#### Detection Results Queue

**Mục đích**: Xử lý kết quả detection từ AI model.

**Configuration**:
```javascript
const detectionResultsQueue = {
  name: 'camera.detection.results',
  durable: true,
  autoDelete: false,
  arguments: {
    'x-message-ttl': 600000, // 10 minutes
    'x-max-length': 2000,
    'x-overflow': 'drop-head',
    'x-dead-letter-exchange': 'dead.letter',
    'x-dead-letter-routing-key': 'dead.letter.retry'
  }
};
```

**Message Format**:
```json
{
  "message_id": "uuid-12346",
  "camera_id": 1,
  "zone_id": 2,
  "timestamp": "2024-01-15T10:30:00Z",
  "detection_results": {
    "detections": [
      {
        "class": "person",
        "confidence": 0.95,
        "bbox": [100, 200, 300, 400],
        "track_id": "track-123"
      }
    ],
    "total_count": 3,
    "processing_time": 45,
    "model_version": "yolo-v8-1.0.0"
  },
  "counting_data": {
    "count_in": 1,
    "count_out": 0,
    "total_count": 3,
    "zone_analysis": {
      "zone_id": 2,
      "direction": "bidirectional"
    }
  },
  "metadata": {
    "frame_id": "frame-12345",
    "retry_count": 0,
    "source": "ai_model"
  }
}
```

### 2. Analytics Queues

#### Analytics Processing Queue

**Mục đích**: Xử lý analytics jobs và data aggregation.

**Configuration**:
```javascript
const analyticsProcessingQueue = {
  name: 'analytics.processing',
  durable: true,
  autoDelete: false,
  arguments: {
    'x-message-ttl': 3600000, // 1 hour
    'x-max-length': 500,
    'x-overflow': 'drop-head',
    'x-dead-letter-exchange': 'dead.letter',
    'x-dead-letter-routing-key': 'dead.letter.retry',
    'x-max-priority': 5
  }
};
```

**Message Format**:
```json
{
  "message_id": "uuid-12347",
  "job_type": "analytics_aggregation",
  "period_type": "hourly",
  "camera_id": 1,
  "zone_id": 2,
  "period_start": "2024-01-15T10:00:00Z",
  "period_end": "2024-01-15T11:00:00Z",
  "parameters": {
    "aggregation_type": "sum",
    "metrics": ["count_in", "count_out", "total_count"],
    "group_by": ["camera_id", "zone_id"]
  },
  "metadata": {
    "priority": 3,
    "retry_count": 0,
    "source": "scheduler"
  }
}
```

#### Report Generation Queue

**Mục đích**: Generate reports và exports.

**Configuration**:
```javascript
const reportGenerationQueue = {
  name: 'analytics.report.generation',
  durable: true,
  autoDelete: false,
  arguments: {
    'x-message-ttl': 7200000, // 2 hours
    'x-max-length': 100,
    'x-overflow': 'drop-head',
    'x-dead-letter-exchange': 'dead.letter',
    'x-dead-letter-routing-key': 'dead.letter.retry'
  }
};
```

**Message Format**:
```json
{
  "message_id": "uuid-12348",
  "report_type": "daily_summary",
  "report_format": "pdf",
  "camera_ids": [1, 2, 3],
  "date_range": {
    "start": "2024-01-15T00:00:00Z",
    "end": "2024-01-15T23:59:59Z"
  },
  "recipients": [
    {
      "email": "admin@example.com",
      "name": "System Admin"
    }
  ],
  "parameters": {
    "include_charts": true,
    "include_details": true,
    "timezone": "UTC"
  },
  "metadata": {
    "priority": 2,
    "retry_count": 0,
    "source": "user_request"
  }
}
```

### 3. Notification Queues

#### Email Notification Queue

**Mục đích**: Send email notifications và alerts.

**Configuration**:
```javascript
const emailNotificationQueue = {
  name: 'notification.email',
  durable: true,
  autoDelete: false,
  arguments: {
    'x-message-ttl': 300000, // 5 minutes
    'x-max-length': 1000,
    'x-overflow': 'drop-head',
    'x-dead-letter-exchange': 'dead.letter',
    'x-dead-letter-routing-key': 'dead.letter.retry'
  }
};
```

**Message Format**:
```json
{
  "message_id": "uuid-12349",
  "notification_type": "alert",
  "template": "camera_offline_alert",
  "recipients": [
    {
      "email": "admin@example.com",
      "name": "System Admin"
    }
  ],
  "data": {
    "camera_id": 1,
    "camera_name": "Main Entrance",
    "alert_type": "camera_offline",
    "severity": "high",
    "timestamp": "2024-01-15T10:30:00Z",
    "message": "Camera Main Entrance is offline"
  },
  "metadata": {
    "priority": 8,
    "retry_count": 0,
    "source": "alert_system"
  }
}
```

#### Webhook Notification Queue

**Mục đích**: Send webhook notifications đến external systems.

**Configuration**:
```javascript
const webhookNotificationQueue = {
  name: 'notification.webhook',
  durable: true,
  autoDelete: false,
  arguments: {
    'x-message-ttl': 60000, // 1 minute
    'x-max-length': 500,
    'x-overflow': 'drop-head',
    'x-dead-letter-exchange': 'dead.letter',
    'x-dead-letter-routing-key': 'dead.letter.retry'
  }
};
```

**Message Format**:
```json
{
  "message_id": "uuid-12350",
  "webhook_url": "https://api.example.com/webhook",
  "method": "POST",
  "headers": {
    "Content-Type": "application/json",
    "Authorization": "Bearer token-12345"
  },
  "payload": {
    "event_type": "counting_result",
    "camera_id": 1,
    "zone_id": 2,
    "timestamp": "2024-01-15T10:30:00Z",
    "data": {
      "count_in": 15,
      "count_out": 8,
      "total_count": 7
    }
  },
  "metadata": {
    "priority": 5,
    "retry_count": 0,
    "source": "counting_system"
  }
}
```

### 4. Dead Letter Queues

#### Retry Queue

**Mục đích**: Retry failed messages với exponential backoff.

**Configuration**:
```javascript
const retryQueue = {
  name: 'dead.letter.retry',
  durable: true,
  autoDelete: false,
  arguments: {
    'x-message-ttl': 300000, // 5 minutes
    'x-max-length': 1000,
    'x-overflow': 'drop-head',
    'x-dead-letter-exchange': 'dead.letter',
    'x-dead-letter-routing-key': 'dead.letter.error'
  }
};
```

#### Error Queue

**Mục đích**: Store permanently failed messages cho analysis.

**Configuration**:
```javascript
const errorQueue = {
  name: 'dead.letter.error',
  durable: true,
  autoDelete: false,
  arguments: {
    'x-message-ttl': 86400000, // 24 hours
    'x-max-length': 10000,
    'x-overflow': 'drop-head'
  }
};
```

## 🔧 Queue Configuration

### RabbitMQ Configuration

```conf
# RabbitMQ Configuration for AI Camera Counting System

# Memory Management
vm_memory_high_watermark.relative = 0.6
vm_memory_high_watermark_paging_ratio = 0.5

# Disk Management
disk_free_limit.relative = 2.0
disk_free_limit.absolute = 2GB

# Network
tcp_listen_options.backlog = 128
tcp_listen_options.nodelay = true
tcp_listen_options.exit_on_close = false

# Security
default_user = admin
default_pass = your_rabbitmq_password
default_vhost = /

# Performance
heartbeat = 60
frame_max = 131072
channel_max = 2047

# Clustering
cluster_formation.peer_discovery_backend = rabbit_peer_discovery_classic_config
cluster_formation.classic_config.nodes.1 = rabbit@node1
cluster_formation.classic_config.nodes.2 = rabbit@node2
```

### Connection Configuration

```javascript
// RabbitMQ Connection Configuration
const rabbitmqConfig = {
  hostname: process.env.RABBITMQ_HOST || 'localhost',
  port: process.env.RABBITMQ_PORT || 5672,
  username: process.env.RABBITMQ_USERNAME || 'admin',
  password: process.env.RABBITMQ_PASSWORD,
  vhost: process.env.RABBITMQ_VHOST || '/',
  
  // Connection Settings
  heartbeat: 60,
  frameMax: 131072,
  channelMax: 2047,
  
  // SSL/TLS
  ssl: process.env.RABBITMQ_SSL === 'true' ? {
    cert: fs.readFileSync('/path/to/client-cert.pem'),
    key: fs.readFileSync('/path/to/client-key.pem'),
    ca: [fs.readFileSync('/path/to/ca-cert.pem')],
    passphrase: process.env.RABBITMQ_SSL_PASSPHRASE
  } : undefined,
  
  // Connection Pool
  connectionTimeout: 30000,
  heartbeatInterval: 60000,
  
  // Retry Settings
  retry: {
    attempts: 3,
    delay: 1000,
    backoff: 'exponential'
  }
};
```

## 📊 Queue Performance Metrics

### Key Performance Indicators (KPIs)

```javascript
// Queue Performance Metrics
const queueMetrics = {
  // Message Throughput
  throughput: {
    target: 1000, // messages/second
    current: 850,
    threshold: 800
  },
  
  // Message Latency
  latency: {
    target: 100, // milliseconds
    current: 75,
    threshold: 150
  },
  
  // Queue Depth
  queueDepth: {
    target: 100, // messages
    current: 45,
    threshold: 500
  },
  
  // Error Rate
  errorRate: {
    target: 0.01, // 1%
    current: 0.005,
    threshold: 0.05
  }
};
```

### Monitoring Queries

```sql
-- Queue Statistics
SELECT 
  name,
  messages,
  messages_ready,
  messages_unacknowledged,
  consumers,
  memory,
  disk_reads,
  disk_writes
FROM rabbitmq_queue_stats 
WHERE name LIKE 'camera.%' OR name LIKE 'analytics.%';

-- Message Rate
SELECT 
  queue_name,
  message_rate,
  consumer_rate,
  ack_rate,
  redeliver_rate
FROM rabbitmq_queue_metrics 
WHERE timestamp >= NOW() - INTERVAL '1 hour';

-- Error Analysis
SELECT 
  queue_name,
  error_type,
  error_count,
  last_error_time
FROM rabbitmq_error_log 
WHERE timestamp >= NOW() - INTERVAL '24 hours'
ORDER BY error_count DESC;
```

## 🔒 Queue Security

### Security Measures

1. **Authentication**: Username/password authentication
2. **Authorization**: VHost và permission management
3. **Network Security**: TLS encryption
4. **Access Control**: IP whitelisting
5. **Audit Logging**: Message access logging

### Security Configuration

```conf
# RabbitMQ Security Configuration
default_user = admin
default_pass = your_strong_password
default_vhost = /

# SSL/TLS Configuration
listeners.ssl.default = 5671
ssl_options.cacertfile = /path/to/ca-cert.pem
ssl_options.certfile = /path/to/server-cert.pem
ssl_options.keyfile = /path/to/server-key.pem
ssl_options.verify = verify_peer
ssl_options.fail_if_no_peer_cert = true

# Access Control
management.load_definitions = /path/to/definitions.json

# Audit Logging
log.connection.level = info
log.channel.level = info
log.queue.level = info
```

## 🔄 Message Reliability

### Reliability Strategies

1. **Message Persistence**: Durable queues và persistent messages
2. **Publisher Confirms**: Confirm message delivery
3. **Consumer Acknowledgments**: Manual acknowledgment
4. **Dead Letter Queues**: Handle failed messages
5. **Retry Logic**: Exponential backoff retry

### Reliability Configuration

```javascript
// Message Reliability Configuration
const reliabilityConfig = {
  // Publisher Confirms
  publisherConfirms: true,
  publisherReturns: true,
  
  // Consumer Acknowledgments
  consumerAck: true,
  consumerPrefetch: 1,
  
  // Retry Logic
  retry: {
    maxAttempts: 3,
    initialDelay: 1000,
    maxDelay: 30000,
    backoffMultiplier: 2
  },
  
  // Dead Letter
  deadLetter: {
    exchange: 'dead.letter',
    routingKey: 'dead.letter.retry',
    ttl: 300000 // 5 minutes
  }
};
```

## 📈 Queue Optimization

### Optimization Strategies

1. **Queue Design**: Use appropriate exchange types
2. **Message Serialization**: Efficient serialization (JSON, MessagePack)
3. **Batch Processing**: Batch multiple messages
4. **Connection Pooling**: Reuse connections efficiently
5. **Load Balancing**: Distribute load across consumers

### Best Practices

```javascript
// Queue Best Practices
const queueBestPractices = {
  // Message Design
  messageDesign: {
    idempotent: true,
    serializable: true,
    versioned: true,
    backwardCompatible: true
  },
  
  // Routing Strategy
  routingStrategy: {
    specific: 'direct',
    pattern: 'topic',
    broadcast: 'fanout',
    priority: 'priority'
  },
  
  // Error Handling
  errorHandling: {
    retry: true,
    deadLetter: true,
    circuitBreaker: true,
    timeout: 30000
  },
  
  // Performance
  performance: {
    prefetch: 1,
    batchSize: 10,
    compression: true,
    connectionPool: true
  }
};
```

---

**Tài liệu này cung cấp thiết kế chi tiết cho queue RabbitMQ trong AI Camera Counting System, bao gồm các patterns, strategies, và best practices cho reliability và performance tối ưu.** 