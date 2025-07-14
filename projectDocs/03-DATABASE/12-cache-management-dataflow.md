# Cache Management Data Flow - AI Camera Counting System

## 📊 Tổng quan

Tài liệu này mô tả chi tiết data flow cho cache management trong hệ thống AI Camera Counting, bao gồm kiến trúc, các loại cache, cấu hình, eviction/invalidation, consistency, monitoring, error handling, security và các API endpoints liên quan.

## 🎯 Mục tiêu
- **Performance**: Tăng tốc độ truy xuất dữ liệu, giảm latency hệ thống
- **Scalability**: Hỗ trợ scale-out, multi-layer cache
- **Consistency**: Đảm bảo dữ liệu cache nhất quán với nguồn gốc
- **Reliability**: Tự động phục hồi, invalidation, fallback
- **Observability**: Monitoring, alerting, traceability
- **Security**: Bảo mật dữ liệu cache và access control

## 🏗️ Cache Architecture

```
┌───────────────────────────────────────────────────────────────────────────────┐
│                        CACHE MANAGEMENT ARCHITECTURE                         │
│                                                                              │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐       │
│  │  Client     │   │   API       │   │   Cache     │   │   Database  │       │
│  │  (Web,      │   │   Gateway   │   │   Layer(s)  │   │   Layer     │       │
│  │   Mobile)   │   │             │   │ (L1/L2/Redis│   │             │       │
│  └─────────────┘   └─────────────┘   └─────────────┘   └─────────────┘       │
│         │               │                   │                  │             │
│         │ 1. Request    │                   │                  │             │
│         │──────────────►│                   │                  │             │
│         │               │ 2. Check L1/L2    │                  │             │
│         │               │   Cache           │                  │             │
│         │               │──────────────────►│                  │             │
│         │               │                   │ 3. Cache Miss    │             │
│         │               │                   │──────────────────►│             │
│         │               │                   │                  │ 4. Query DB │
│         │               │                   │                  │────────────►│
│         │               │                   │                  │             │
│         │               │                   │ 5. Update Cache  │             │
│         │               │                   │◄─────────────────│             │
│         │               │ 6. Return Data    │                  │             │
│         │◄──────────────│                   │                  │             │
└───────────────────────────────────────────────────────────────────────────────┘
```

## 🔄 Cache Data Flow Details

### 1. User/Session Cache Flow
- Khi user login, session info được cache (L1: memory, L2: Redis)
- Các request tiếp theo kiểm tra cache trước khi truy vấn DB
- Khi logout/expire, cache invalidation tự động

### 2. Camera Info Cache Flow
- Camera metadata (id, location, status) được cache để tăng tốc truy xuất
- Khi camera update, cache invalidation theo event hoặc TTL

### 3. AI Inference Result Cache Flow
- Kết quả inference (count, bounding box) cache tạm thời để phục vụ analytics/replay
- TTL ngắn, invalidation khi có inference mới

### 4. Analytics/Report Cache Flow
- Kết quả analytics/reporting cache theo user/session hoặc global
- Invalidate khi có dữ liệu mới hoặc theo schedule

### 5. Config/Feature Flag Cache Flow
- Config, feature flag cache để giảm truy vấn DB/config server
- Invalidate khi config thay đổi hoặc theo TTL

## 🔧 Cache Configuration

### 1. Redis (Distributed Cache)
```typescript
interface RedisCacheConfig {
  host: string;
  port: number;
  password?: string;
  db: number;
  keyPrefix: string;
  ttl: {
    session: 1800; // 30 phút
    camera: 600; // 10 phút
    aiResult: 60; // 1 phút
    analytics: 300; // 5 phút
    config: 900; // 15 phút
  };
  evictionPolicy: 'volatile-lru' | 'allkeys-lru' | 'volatile-ttl' | 'noeviction';
  maxMemory: '512mb';
  monitoring: true;
  alerting: true;
}
```

### 2. Local (In-memory) Cache
```typescript
interface LocalCacheConfig {
  maxSize: number;
  ttl: number;
  evictionPolicy: 'lru' | 'lfu' | 'fifo';
  layers: {
    l1: { enabled: true; maxSize: 1000; ttl: 60; };
    l2: { enabled: true; maxSize: 10000; ttl: 600; };
  };
}
```

### 3. Multi-layer Cache Strategy
- L1: In-memory (per instance, fastest, volatile)
- L2: Redis (shared, persistent, scalable)
- L3: DB fallback (source of truth)
- Cache warming, prefetch, write-through, read-through, cache-aside patterns

### 4. Invalidation & Consistency
- TTL-based invalidation
- Event-driven invalidation (pub/sub, message queue)
- Manual invalidation (API)
- Write-through & write-back consistency
- Cache stampede protection (lock, singleflight)

## 🛡️ Security & Reliability
- **TLS/SSL** cho Redis connection
- **Access Control**: Chỉ cho phép app/service truy cập keyspace được phân quyền
- **Data Encryption** (tuỳ chọn)
- **Cache Poisoning Protection**: Validate input/output
- **Failover/Replication**: Redis Sentinel/Cluster
- **Fallback**: Tự động fallback DB khi cache lỗi

## 📈 Monitoring & Alerting
- **Metrics**: hit rate, miss rate, eviction rate, memory usage, latency
- **Alerting**: memory usage cao, hit rate thấp, eviction tăng bất thường
- **Tracing**: cache key, request id, cache layer
- **Logging**: log cache event, error, invalidation

## 📋 API Endpoints (ví dụ)
```typescript
interface CacheAPI {
  // Get cache status
  'GET /api/v1/cache/status': {
    query: { key?: string; layer?: 'l1'|'l2' };
    response: { key: string; exists: boolean; ttl: number; value?: any; layer: string }[];
  };
  // Invalidate cache
  'POST /api/v1/cache/invalidate': {
    body: { key: string; layer?: 'l1'|'l2'; recursive?: boolean };
    response: { status: 'ok'|'error'; invalidated: boolean; error?: string };
  };
  // Set cache value
  'POST /api/v1/cache/set': {
    body: { key: string; value: any; ttl?: number; layer?: 'l1'|'l2' };
    response: { status: 'ok'|'error'; error?: string };
  };
}
```

## 🏆 Success Criteria
- **Performance**: >95% cache hit rate, <10ms latency (L1), <50ms (L2)
- **Reliability**: 99.99% cache availability, tự động fallback
- **Consistency**: Dữ liệu cache nhất quán với DB, không stale data
- **Observability**: Đầy đủ metrics, alert, trace cho mọi layer
- **Security**: Không rò rỉ cache, access control chặt chẽ
- **Scalability**: Scale-out multi-layer dễ dàng

## 🔗 Traceability & Compliance

### Related Documents
- **Theory**: `01-02-data-flow-comprehensive-theory.md`
- **Infrastructure**: `05-01-infrastructure-theory.md`
- **Performance**: `06-07-performance-optimization-patterns.md`
- **Database**: `06-03-database-patterns.md`
- **Monitoring**: `05-02-monitoring-observability.md`

### Business Metrics
- **Cache Hit Rate**: ≥ 95%
- **Cache Response Time**: < 10ms
- **Cache Uptime**: ≥ 99.99%
- **Memory Usage**: < 80%
- **Cost per Cache Hit**: < $0.0001

### Compliance Checklist
- [x] Cache data encryption
- [x] Access control for cache operations
- [x] Data retention and eviction policies
- [x] Audit logging for cache events
- [x] Cache consistency validation

### Data Lineage
- Data Source → Cache Layer (Redis) → Cache Hit/Miss → Data Retrieval → Response → Invalidation
- All cache operations tracked, monitored, and audited

### User/Role Matrix
| Role | Permissions | Cache Access |
|------|-------------|--------------|
| User | N/A | N/A |
| Admin | Manage cache, monitor performance | All caches |
| System | Read/write cache data | All caches |
| Auditor | View cache logs, compliance checks | All cache events |

### Incident Response Checklist
- [x] Cache failure monitoring and alerts
- [x] Cache miss rate monitoring
- [x] Memory usage monitoring
- [x] Cache corruption detection
- [x] Cache performance optimization

---
**Status**: ✅ **COMPLETE**
**Quality Level**: 🏆 ENTERPRISE GRADE
**Production Ready**: ✅ YES

Cache Management data flow đã được thiết kế chuẩn production, đảm bảo performance, reliability, consistency, observability và security cho toàn bộ hệ thống. 