# Cache Design (Redis) - AI Camera Counting System

## 📊 Tổng quan

Tài liệu này mô tả thiết kế cache Redis cho hệ thống AI Camera Counting, bao gồm các cấu trúc cache, key patterns, value formats, và các chiến lược tối ưu hóa hiệu năng.

## 🎯 Mục tiêu cache

- **Performance**: Giảm latency xuống < 50ms cho real-time data
- **Scalability**: Hỗ trợ hàng trăm camera streams đồng thời
- **Reliability**: 99.9% cache hit rate
- **Consistency**: Đảm bảo data consistency giữa cache và database
- **Efficiency**: Tối ưu memory usage và network bandwidth

## 🏗️ Cache Architecture Overview

### High-Level Cache Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              CACHE ARCHITECTURE OVERVIEW                        │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              APPLICATION LAYER                              │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Frontend  │  │   API       │  │   Worker    │  │   Analytics │        │ │
│  │  │   (React)   │  │   Gateway   │  │   Services  │  │   Services  │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                             │
│                                    ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              CACHE LAYER (REDIS)                            │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Session   │  │   Real-time │  │   Status    │  │   Analytics │        │ │
│  │  │   Cache     │  │   Data      │  │   Cache     │  │   Cache     │        │ │
│  │  │             │  │   Cache     │  │             │  │             │        │ │
│  │  │ • User      │  │ • Counting  │  │ • Camera    │  │ • Reports   │        │ │
│  │  │   Sessions  │  │   Results   │  │   Status    │  │ • Trends    │        │ │
│  │  │ • Camera    │  │ • Live      │  │ • System    │  │ • KPIs      │        │ │
│  │  │   Sessions  │  │   Updates   │  │   Status    │  │ • Metrics   │        │ │
│  │  │ • Tokens    │  │ • Events    │  │ • Health    │  │ • Forecasts │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                             │
│                                    ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              UTILITY CACHE                                  │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Lock      │  │   Rate      │  │   Query     │  │   Config    │        │ │
│  │  │   Cache     │  │   Limiting  │  │   Cache     │  │   Cache     │        │ │
│  │  │             │  │   Cache     │  │             │  │             │        │ │
│  │  │ • Distributed│  │ • API       │  │ • Query     │  │ • System    │        │ │
│  │  │   Locks     │  │   Limits    │  │   Results   │  │   Config    │        │ │
│  │  │ • Processing│  │ • User      │  │ • Aggregated│  │ • Feature    │        │ │
│  │  │   Flags     │  │   Limits    │  │   Data      │  │   Flags      │        │ │
│  │  │ • Mutex     │  │ • IP        │  │ • Cached    │  │ • Settings   │        │ │
│  │  │   Locks     │  │   Limits    │  │   Queries   │  │ • Parameters │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Cache Data Flow

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              CACHE DATA FLOW                                    │
│                                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐      │
│  │   Database  │    │   Cache     │    │   Application│   │   Client    │      │
│  │   (Write)   │    │   (Redis)   │    │   (Read)     │   │   (Request) │      │
│  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘      │
│         │                   │                   │                   │          │
│         │ 1. Data Update    │                   │                   │          │
│         │ (INSERT/UPDATE)   │                   │                   │          │
│         │──────────────────►│                   │                   │          │
│         │                   │                   │                   │          │
│         │                   │ 2. Cache Update   │                   │          │
│         │                   │ (SET/HSET)        │                   │          │
│         │                   │──────────────────►│                   │          │
│         │                   │                   │                   │          │
│         │                   │                   │ 3. Cache Read     │          │
│         │                   │                   │ (GET/HGET)        │          │
│         │                   │                   │◄──────────────────┤          │
│         │                   │                   │                   │          │
│         │                   │                   │ 4. Data Response  │          │
│         │                   │                   │ (JSON)            │          │
│         │                   │                   │──────────────────►│          │
│         │                   │                   │                   │          │
│         │                   │ 5. Cache Miss     │                   │          │
│         │                   │ (Fallback)        │                   │          │
│         │                   │◄──────────────────┤                   │          │
│         │                   │                   │                   │          │
│         │ 6. Database Read  │                   │                   │          │
│         │ (SELECT)          │                   │                   │          │
│         │◄──────────────────┤                   │                   │          │
│         │                   │                   │                   │          │
│         │ 7. Cache Store    │                   │                   │          │
│         │ (SET with TTL)    │                   │                   │          │
│         │──────────────────►│                   │                   │          │
│         │                   │                   │                   │          │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 📋 Cache Categories

### 1. Session Cache

**Mục đích**: Lưu trữ thông tin session người dùng và camera.

**Key Patterns**:
```
session:user:{user_id} -> User session data
session:camera:{camera_id} -> Camera session data
session:token:{token} -> Token validation
```

**Value Structure**:
```json
{
  "user_id": 123,
  "username": "admin",
  "role": "admin",
  "permissions": ["read", "write", "admin"],
  "last_activity": "2024-01-15T10:30:00Z",
  "ip_address": "192.168.1.100",
  "user_agent": "Mozilla/5.0...",
  "expires_at": "2024-01-15T18:30:00Z"
}
```

**TTL**: 8 hours (28800 seconds)
**Eviction Policy**: LRU
**Use Cases**:
- User authentication
- Permission checking
- Session management
- Token validation

### 2. Real-time Data Cache

**Mục đích**: Lưu trữ dữ liệu real-time từ camera streams.

**Key Patterns**:
```
realtime:counting:{camera_id}:{zone_id} -> Latest counting result
realtime:status:{camera_id} -> Camera status
realtime:events:{camera_id} -> Recent events
realtime:frame:{camera_id} -> Latest frame data
```

**Value Structure**:
```json
{
  "camera_id": 1,
  "zone_id": 2,
  "timestamp": "2024-01-15T10:30:00Z",
  "count_in": 15,
  "count_out": 8,
  "total_count": 7,
  "confidence": 0.95,
  "frame_data": {
    "detections": 3,
    "bounding_boxes": [...],
    "processing_time": 45
  }
}
```

**TTL**: 5 minutes (300 seconds)
**Eviction Policy**: LRU
**Use Cases**:
- Real-time dashboard
- Live counting display
- WebSocket updates
- Performance monitoring

### 3. Status Cache

**Mục đích**: Lưu trữ trạng thái hệ thống và camera.

**Key Patterns**:
```
status:camera:{camera_id} -> Camera status
status:system:health -> System health
status:ai_model:{model_id} -> AI model status
status:zone:{zone_id} -> Zone status
```

**Value Structure**:
```json
{
  "camera_id": 1,
  "status": "online",
  "last_heartbeat": "2024-01-15T10:30:00Z",
  "error_count": 0,
  "last_error": null,
  "ai_model_status": "active",
  "processing_fps": 25,
  "memory_usage": 0.75,
  "cpu_usage": 0.60
}
```

**TTL**: 2 minutes (120 seconds)
**Eviction Policy**: LRU
**Use Cases**:
- System monitoring
- Health checks
- Status dashboard
- Alert generation

### 4. Analytics Cache

**Mục đích**: Lưu trữ dữ liệu analytics đã được tính toán.

**Key Patterns**:
```
analytics:hourly:{camera_id}:{date}:{hour} -> Hourly analytics
analytics:daily:{camera_id}:{date} -> Daily analytics
analytics:weekly:{camera_id}:{week} -> Weekly analytics
analytics:monthly:{camera_id}:{month} -> Monthly analytics
```

**Value Structure**:
```json
{
  "camera_id": 1,
  "period_type": "hourly",
  "period_start": "2024-01-15T10:00:00Z",
  "period_end": "2024-01-15T11:00:00Z",
  "total_count_in": 150,
  "total_count_out": 120,
  "peak_count": 25,
  "peak_time": "2024-01-15T10:30:00Z",
  "avg_count": 12.5,
  "data_points": 60
}
```

**TTL**: 1 hour (3600 seconds)
**Eviction Policy**: LRU
**Use Cases**:
- Dashboard reports
- Trend analysis
- Performance metrics
- Historical data

### 5. Lock Cache

**Mục đích**: Quản lý distributed locks và processing flags.

**Key Patterns**:
```
lock:camera:{camera_id}:processing -> Camera processing lock
lock:analytics:calculation -> Analytics calculation lock
lock:user:{user_id}:session -> User session lock
flag:camera:{camera_id}:maintenance -> Maintenance flag
```

**Value Structure**:
```json
{
  "lock_id": "uuid-12345",
  "owner": "worker-1",
  "acquired_at": "2024-01-15T10:30:00Z",
  "expires_at": "2024-01-15T10:35:00Z",
  "metadata": {
    "process_id": 12345,
    "host": "worker-1.example.com"
  }
}
```

**TTL**: 5 minutes (300 seconds)
**Eviction Policy**: None (manual cleanup)
**Use Cases**:
- Distributed processing
- Resource coordination
- Race condition prevention
- Maintenance mode

### 6. Rate Limiting Cache

**Mục đích**: Quản lý rate limiting cho API và user requests.

**Key Patterns**:
```
ratelimit:api:{user_id}:{endpoint} -> API rate limit
ratelimit:user:{user_id}:requests -> User request limit
ratelimit:ip:{ip_address}:requests -> IP request limit
```

**Value Structure**:
```json
{
  "user_id": 123,
  "endpoint": "/api/cameras/1/stream",
  "requests": 45,
  "limit": 100,
  "window_start": "2024-01-15T10:00:00Z",
  "window_end": "2024-01-15T11:00:00Z",
  "reset_at": "2024-01-15T11:00:00Z"
}
```

**TTL**: 1 hour (3600 seconds)
**Eviction Policy**: TTL
**Use Cases**:
- API rate limiting
- User quota management
- DDoS protection
- Resource protection

### 7. Query Cache

**Mục đích**: Cache kết quả queries phức tạp.

**Key Patterns**:
```
query:cameras:active -> Active cameras list
query:analytics:summary:{date} -> Analytics summary
query:alerts:unresolved -> Unresolved alerts
query:users:online -> Online users
```

**Value Structure**:
```json
{
  "query_hash": "abc123def456",
  "result": [...],
  "execution_time": 150,
  "row_count": 25,
  "cached_at": "2024-01-15T10:30:00Z",
  "expires_at": "2024-01-15T11:30:00Z"
}
```

**TTL**: 1 hour (3600 seconds)
**Eviction Policy**: LRU
**Use Cases**:
- Complex queries
- Dashboard data
- Report generation
- Performance optimization

### 8. Config Cache

**Mục đích**: Cache cấu hình hệ thống và feature flags.

**Key Patterns**:
```
config:system:general -> General system config
config:camera:{camera_id}:settings -> Camera settings
config:ai_model:{model_id}:params -> AI model parameters
config:feature:flags -> Feature flags
```

**Value Structure**:
```json
{
  "config_id": "system_general",
  "version": "1.0.0",
  "data": {
    "max_cameras": 100,
    "session_timeout": 28800,
    "maintenance_mode": false,
    "debug_mode": false
  },
  "updated_at": "2024-01-15T10:30:00Z",
  "updated_by": "admin"
}
```

**TTL**: 1 hour (3600 seconds)
**Eviction Policy**: LRU
**Use Cases**:
- System configuration
- Feature toggles
- Runtime settings
- Parameter management

## 🔧 Cache Configuration

### Redis Configuration

```conf
# Redis Configuration for AI Camera Counting System

# Memory Management
maxmemory 2gb
maxmemory-policy allkeys-lru

# Persistence
save 900 1
save 300 10
save 60 10000
rdbcompression yes
rdbchecksum yes

# Network
timeout 300
tcp-keepalive 60
tcp-backlog 511

# Security
requirepass your_redis_password
rename-command FLUSHDB ""
rename-command FLUSHALL ""

# Performance
tcp-nodelay yes
tcp-nopush yes
```

### Connection Pool Configuration

```javascript
// Redis Connection Pool Configuration
const redisConfig = {
  host: process.env.REDIS_HOST || 'localhost',
  port: process.env.REDIS_PORT || 6379,
  password: process.env.REDIS_PASSWORD,
  db: process.env.REDIS_DB || 0,
  
  // Connection Pool
  maxRetriesPerRequest: 3,
  retryDelayOnFailover: 100,
  enableReadyCheck: true,
  maxLoadingTimeout: 10000,
  
  // Performance
  lazyConnect: true,
  keepAlive: 30000,
  family: 4,
  
  // Security
  tls: process.env.REDIS_TLS === 'true' ? {} : undefined,
  
  // Monitoring
  enableOfflineQueue: false,
  enableAutoPipelining: true
};
```

## 📊 Cache Performance Metrics

### Key Performance Indicators (KPIs)

```javascript
// Cache Performance Metrics
const cacheMetrics = {
  // Hit Rate
  hitRate: {
    target: 0.95, // 95% hit rate
    current: 0.92,
    threshold: 0.90
  },
  
  // Response Time
  responseTime: {
    target: 50, // 50ms
    current: 45,
    threshold: 100
  },
  
  // Memory Usage
  memoryUsage: {
    target: 0.80, // 80% of max memory
    current: 0.75,
    threshold: 0.90
  },
  
  // Connection Count
  connections: {
    target: 100,
    current: 85,
    threshold: 150
  }
};
```

### Monitoring Queries

```sql
-- Cache Hit Rate
SELECT 
  SUM(hits) / (SUM(hits) + SUM(misses)) as hit_rate
FROM redis_stats 
WHERE timestamp >= NOW() - INTERVAL '1 hour';

-- Memory Usage
SELECT 
  used_memory_human,
  used_memory_peak_human,
  used_memory_rss_human
FROM redis_info;

-- Slow Queries
SELECT 
  command,
  duration,
  timestamp
FROM redis_slow_log 
WHERE duration > 10
ORDER BY duration DESC;
```

## 🔒 Cache Security

### Security Measures

1. **Authentication**: Redis password protection
2. **Network Security**: TLS encryption
3. **Access Control**: IP whitelisting
4. **Data Encryption**: Sensitive data encryption
5. **Audit Logging**: Cache access logging

### Security Configuration

```conf
# Redis Security Configuration
requirepass your_strong_password
rename-command FLUSHDB ""
rename-command FLUSHALL ""
rename-command CONFIG ""
rename-command SHUTDOWN ""

# Network Security
bind 127.0.0.1
protected-mode yes
tcp-backlog 511
timeout 300

# TLS Configuration
tls-port 6380
tls-cert-file /path/to/redis.crt
tls-key-file /path/to/redis.key
tls-ca-cert-file /path/to/ca.crt
```

## 🔄 Cache Consistency

### Consistency Strategies

1. **Write-Through**: Write to cache and database simultaneously
2. **Write-Behind**: Write to cache first, then database asynchronously
3. **Cache-Aside**: Application manages cache manually
4. **Read-Through**: Cache automatically loads from database on miss

### Invalidation Strategies

```javascript
// Cache Invalidation Patterns
const cacheInvalidation = {
  // Time-based invalidation
  timeBased: {
    session: 28800, // 8 hours
    realtime: 300,  // 5 minutes
    analytics: 3600, // 1 hour
    config: 3600    // 1 hour
  },
  
  // Event-based invalidation
  eventBased: {
    'camera:updated': ['status:camera:*', 'config:camera:*'],
    'user:logged_out': ['session:user:*', 'session:token:*'],
    'analytics:calculated': ['analytics:*', 'query:analytics:*']
  },
  
  // Manual invalidation
  manual: {
    flushAll: 'FLUSHALL',
    flushDb: 'FLUSHDB',
    deletePattern: 'DEL pattern:*'
  }
};
```

## 📈 Cache Optimization

### Optimization Strategies

1. **Key Design**: Use descriptive, hierarchical keys
2. **Value Serialization**: Use efficient serialization (JSON, MessagePack)
3. **Compression**: Compress large values
4. **Pipelining**: Batch multiple operations
5. **Connection Pooling**: Reuse connections efficiently

### Best Practices

```javascript
// Cache Best Practices
const cacheBestPractices = {
  // Key Naming
  keyNaming: {
    pattern: '{category}:{subcategory}:{identifier}',
    examples: [
      'session:user:123',
      'realtime:counting:1:2',
      'analytics:daily:1:2024-01-15'
    ]
  },
  
  // Value Optimization
  valueOptimization: {
    compression: true,
    serialization: 'json',
    maxSize: '1mb'
  },
  
  // TTL Strategy
  ttlStrategy: {
    short: 300,    // 5 minutes
    medium: 3600,  // 1 hour
    long: 86400,   // 1 day
    session: 28800 // 8 hours
  },
  
  // Error Handling
  errorHandling: {
    fallback: 'database',
    retry: 3,
    circuitBreaker: true
  }
};
```

---

**Tài liệu này cung cấp thiết kế chi tiết cho cache Redis trong AI Camera Counting System, bao gồm các patterns, strategies, và best practices cho hiệu năng tối ưu.** 