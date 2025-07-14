# Worker Pool Architecture - Kiến trúc Worker Pool

## 📊 Tổng quan

Tài liệu này trình bày lý thuyết về kiến trúc Worker Pool trong hệ thống AI Camera Counting, tập trung vào việc quản lý và phân phối tài nguyên xử lý cho các camera streams.

## 🎯 Mục tiêu
- Tối ưu hóa việc sử dụng tài nguyên CPU/GPU cho AI processing
- Đảm bảo khả năng mở rộng và xử lý đồng thời nhiều camera
- Cung cấp fault tolerance và load balancing
- Giảm thiểu latency trong xử lý real-time

## 🏗️ Kiến trúc Worker Pool

### 1. Worker Pool Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              WORKER POOL ARCHITECTURE                          │
│                                                                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                  │
│  │   Camera        │  │   Task Queue    │  │   Worker        │                  │
│  │   Streams       │  │   (RabbitMQ)    │  │   Manager       │                  │
│  │                 │  │                 │  │                 │                  │
│  │ • RTSP Streams  │  │ • Task Buffer   │  │ • Lifecycle Mgmt│                  │
│  │ • HTTP Streams  │  │ • Priority Queue│  │ • Health Check  │                  │
│  │ • File Uploads  │  │ • Dead Letter   │  │ • Scaling Logic │                  │
│  │ • Batch Files   │  │ • Retry Logic   │  │ • Load Balancing│                  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘                  │
│           │                       │                       │                     │
│           │                       │                       │                     │
│           ▼                       ▼                       ▼                     │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                  │
│  │   Load          │  │   Resource      │  │   Worker        │                  │
│  │   Balancer      │  │   Monitor       │  │   Registry      │                  │
│  │                 │  │                 │  │                 │                  │
│  │ • Round Robin   │  │ • CPU Monitor   │  │ • Worker Info   │                  │
│  │ • Least Loaded  │  │ • Memory Monitor│  │ • Capabilities  │                  │
│  │ • Capability    │  │ • GPU Monitor   │  │ • Status Track  │                  │
│  │ • Geographic    │  │ • Network I/O   │  │ • Health Status │                  │
│  │ • Priority      │  │ • Disk I/O      │  │ • Performance   │                  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘                  │
│           │                       │                       │                     │
│           │                       │                       │                     │
│           └───────────────────────┼───────────────────────┘                     │
│                                   │                                             │
│                                   ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐│
│  │                              WORKER POOL                                   ││
│  │                                                                             ││
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        ││
│  │  │   Worker 1  │  │   Worker 2  │  │   Worker 3  │  │   Worker N  │        ││
│  │  │             │  │             │  │             │  │             │        ││
│  │  │ • AI Model  │  │ • AI Model  │  │ • AI Model  │  │ • AI Model  │        ││
│  │  │ • Processing│  │ • Processing│  │ • Processing│  │ • Processing│        ││
│  │  │ • GPU/CPU   │  │ • GPU/CPU   │  │ • GPU/CPU   │  │ • GPU/CPU   │        ││
│  │  │ • Memory    │  │ • Memory    │  │ • Memory    │  │ • Memory    │        ││
│  │  │ • Network   │  │ • Network   │  │ • Network   │  │ • Network   │        ││
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        ││
│  └─────────────────────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              OUTPUT PROCESSING                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                  │
│  │   Result        │  │   Analytics     │  │   Real-time     │                  │
│  │   Storage       │  │   Engine        │  │   Broadcasting  │                  │
│  │                 │  │                 │  │                 │                  │
│  │ • PostgreSQL    │  │ • Data Pipeline │  │ • WebSocket     │                  │
│  │ • Redis Cache   │  │ • Aggregation   │  │ • Event Stream  │                  │
│  │ • File Storage  │  │ • Reporting     │  │ • Live Updates  │                  │
│  │ • Backup        │  │ • Dashboards    │  │ • Notifications │                  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 2. Worker Lifecycle Management Flow

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Worker    │    │   Worker    │    │   Resource  │    │   Task      │
│   Startup   │    │   Manager   │    │   Monitor   │    │   Queue     │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
       │                   │                   │                   │
       │ 1. Initialize     │                   │                   │
       │    Worker        │                   │                   │
       │──────────────────►│                   │                   │
       │                   │                   │                   │
       │ 2. Register       │                   │                   │
       │    Worker        │                   │                   │
       │◄──────────────────│                   │                   │
       │                   │                   │                   │
       │ 3. Health Check   │                   │                   │
       │    Request        │                   │                   │
       │──────────────────────────────────────►│                   │
       │                   │                   │                   │
       │ 4. Resource       │                   │                   │
       │    Status         │                   │                   │
       │◄──────────────────────────────────────│                   │
       │                   │                   │                   │
       │ 5. Ready for      │                   │                   │
       │    Tasks          │                   │                   │
       │──────────────────────────────────────────────────────────►│
       │                   │                   │                   │
       │ 6. Task           │                   │                   │
       │    Assignment     │                   │                   │
       │◄──────────────────────────────────────────────────────────│
       │                   │                   │                   │
       │ 7. Process Task   │                   │                   │
       │    (AI Model)     │                   │                   │
       │                   │                   │                   │
       │ 8. Update Status  │                   │                   │
       │    & Metrics      │                   │                   │
       │──────────────────►│                   │                   │
       │                   │                   │                   │
       │ 9. Continue       │                   │                   │
       │    Processing     │                   │                   │
       │                   │                   │                   │
```

### 3. Load Balancing Strategy Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              LOAD BALANCING STRATEGIES                         │
│                                                                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                  │
│  │   Round Robin   │  │   Least Loaded  │  │   Capability    │                  │
│  │                 │  │                 │  │   Based         │                  │
│  │ Task 1 → W1     │  │ CPU: W1(80%)    │  │ GPU: W1(High)   │                  │
│  │ Task 2 → W2     │  │ CPU: W2(30%)    │  │ GPU: W2(Medium) │                  │
│  │ Task 3 → W3     │  │ CPU: W3(60%)    │  │ GPU: W3(Low)    │                  │
│  │ Task 4 → W1     │  │                 │  │                 │                  │
│  │ Task 5 → W2     │  │ Task → W2       │  │ AI Task → W1    │                  │
│  │ Task 6 → W3     │  │ (Lowest Load)   │  │ (Best GPU)      │                  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘                  │
│                                                                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                  │
│  │   Geographic    │  │   Priority      │  │   Hybrid        │                  │
│  │   Based         │  │   Based         │  │   Strategy      │                  │
│  │                 │  │                 │  │                 │                  │
│  │ Region A → W1   │  │ Critical → W1   │  │ 1. Priority     │                  │
│  │ Region B → W2   │  │ High → W2       │  │ 2. Capability   │                  │
│  │ Region C → W3   │  │ Normal → W3     │  │ 3. Load         │                  │
│  │                 │  │ Low → W4        │  │ 4. Geographic   │                  │
│  │ (Low Latency)   │  │                 │  │                 │                  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 4. Scaling Strategy Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              SCALING STRATEGIES                                │
│                                                                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                  │
│  │   Horizontal    │  │   Vertical      │  │   Auto-Scaling  │                  │
│  │   Scaling       │  │   Scaling       │  │                 │                  │
│  │                 │  │                 │  │                 │                  │
│  │ Add Workers:    │  │ Increase        │  │ Metrics:        │                  │
│  │ W1, W2, W3      │  │ Resources:      │  │ • CPU > 80%     │                  │
│  │ ↓               │  │ • CPU: 2→4 cores│  │ • Memory > 85%  │                  │
│  │ W4, W5, W6      │  │ • RAM: 8→16GB   │  │ • Queue > 100   │                  │
│  │ ↓               │  │ • GPU: 1→2 cards│  │ • Latency > 500ms│                  │
│  │ W7, W8, W9      │  │                 │  │                 │                  │
│  │                 │  │ (Same Worker)   │  │ Actions:        │                  │
│  │ (More Workers)  │  │                 │  │ • Scale Up      │                  │
│  └─────────────────┘  └─────────────────┘  │ • Scale Down    │                  │
│                                           │ • Alert          │                  │
│  ┌─────────────────┐  ┌─────────────────┐  └─────────────────┘                  │
│  │   Predictive    │  │   Reactive      │                                      │
│  │   Scaling       │  │   Scaling       │                                      │
│  │                 │  │                 │                                      │
│  │ • Time-based    │  │ • Load-based    │                                      │
│  │ • Pattern-based │  │ • Error-based   │                                      │
│  │ • Event-based   │  │ • Performance   │                                      │
│  │                 │  │ • Health-based  │                                      │
│  │ Scale before    │  │                 │                                      │
│  │ peak load       │  │ Scale after     │                                      │
│  │                 │  │ issues occur    │                                      │
│  └─────────────────┘  └─────────────────┘                                      │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 5. Fault Tolerance Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              FAULT TOLERANCE ARCHITECTURE                      │
│                                                                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                  │
│  │   Worker        │  │   Circuit       │  │   Task Retry    │                  │
│  │   Isolation     │  │   Breaker       │  │   Logic         │                  │
│  │                 │  │                 │  │                 │                  │
│  │ • Process       │  │ • Open State    │  │ • Max Retries: 3│                  │
│  │   Isolation     │  │ • Half-Open     │  │ • Backoff:      │                  │
│  │ • Memory        │  │ • Closed State  │  │   1s, 2s, 4s   │                  │
│  │   Isolation     │  │ • Failure Count │  │ • Dead Letter   │                  │
│  │ • Network       │  │ • Timeout       │  │   Queue         │                  │
│  │   Isolation     │  │ • Recovery      │  │ • Manual Review │                  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘                  │
│           │                       │                       │                     │
│           │                       │                       │                     │
│           ▼                       ▼                       ▼                     │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                  │
│  │   Backup        │  │   State         │  │   Health        │                  │
│  │   Workers       │  │   Recovery      │  │   Monitoring    │                  │
│  │                 │  │                 │  │                 │                  │
│  │ • Hot Standby   │  │ • Checkpointing │  │ • Heartbeat     │                  │
│  │ • Warm Standby  │  │ • State Sync    │  │ • Health Check  │                  │
│  │ • Cold Standby  │  │ • Data Recovery │  │ • Performance   │                  │
│  │ • Failover      │  │ • Restart Logic │  │ • Resource      │                  │
│  │ • Load Sharing  │  │ • Consistency   │  │ • Alerting      │                  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 6. Resource Monitoring Dashboard Mockup

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              WORKER POOL MONITORING DASHBOARD                  │
│                                                                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                  │
│  │   System        │  │   Worker        │  │   Performance   │                  │
│  │   Overview      │  │   Status        │  │   Metrics       │                  │
│  │                 │  │                 │  │                 │                  │
│  │ Total Workers: 8│  │ W1: ✅ Active   │  │ CPU Avg: 65%    │                  │
│  │ Active: 7       │  │ W2: ✅ Active   │  │ Memory Avg: 72% │                  │
│  │ Failed: 1       │  │ W3: ❌ Failed   │  │ GPU Avg: 45%    │                  │
│  │ Queue Size: 45  │  │ W4: ✅ Active   │  │ Network: 2.3MB/s│                  │
│  │ Throughput: 120 │  │ W5: ✅ Active   │  │ Latency: 180ms  │                  │
│  │ Tasks/min       │  │ W6: ✅ Active   │  │ Error Rate: 0.5%│                  │
│  └─────────────────┘  │ W7: ✅ Active   │  └─────────────────┘                  │
│                       │ W8: ✅ Active   │                                      │
│  ┌─────────────────┐  └─────────────────┘  ┌─────────────────┐                  │
│  │   Load          │                       │   Alerts        │                  │
│  │   Distribution  │                       │                 │                  │
│  │                 │                       │ • W3 Failed     │                  │
│  │ W1: 15%         │                       │ • High CPU W5   │                  │
│  │ W2: 12%         │                       │ • Queue > 50    │                  │
│  │ W3: 0% (Failed) │                       │ • Memory W7     │                  │
│  │ W4: 18%         │                       │ • Auto-scaling  │                  │
│  │ W5: 22%         │                       │   Triggered     │                  │
│  │ W6: 14%         │                       │                 │                  │
│  │ W7: 11%         │                       │                 │                  │
│  │ W8: 8%          │                       │                 │                  │
│  └─────────────────┘                       └─────────────────┘                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 🏗️ Kiến trúc Worker Pool Components

- **Worker Manager**: Quản lý lifecycle của workers, health check, scaling
- **Load Balancer**: Phân phối camera streams đến workers phù hợp
- **Task Queue**: Lưu trữ và quản lý các task xử lý
- **Resource Monitor**: Theo dõi tài nguyên CPU/GPU/memory
- **Worker Registry**: Đăng ký và quản lý thông tin workers

## 🔄 Worker Lifecycle Management
- **Registration**: Worker đăng ký với manager khi khởi động
- **Health Check**: Kiểm tra trạng thái worker định kỳ
- **Task Assignment**: Phân công task dựa trên load và capability
- **Failure Recovery**: Tự động restart worker khi có lỗi
- **Graceful Shutdown**: Dừng worker an toàn khi cần

## 📊 Load Balancing Strategies
- **Round Robin**: Phân phối task theo vòng tròn
- **Least Loaded**: Gán task cho worker có ít tải nhất
- **Capability-based**: Phân phối theo khả năng xử lý của worker
- **Geographic**: Phân phối theo vị trí địa lý
- **Priority-based**: Ưu tiên task quan trọng

## 🔒 Fault Tolerance & Recovery
- **Worker Isolation**: Cô lập lỗi giữa các workers
- **Task Retry**: Tự động thử lại task khi worker fail
- **Circuit Breaker**: Ngăn chặn cascade failure
- **Backup Workers**: Dự phòng workers cho critical tasks
- **State Recovery**: Khôi phục trạng thái sau restart

## 📈 Scaling Strategies
- **Horizontal Scaling**: Thêm/bớt workers theo demand
- **Vertical Scaling**: Tăng/giảm tài nguyên cho worker
- **Auto-scaling**: Tự động scale dựa trên metrics
- **Predictive Scaling**: Scale trước khi có peak load

## 🔍 Monitoring & Observability
- **Worker Metrics**: CPU, memory, GPU usage, task queue length
- **Performance Metrics**: Throughput, latency, error rate
- **Health Status**: Worker status, uptime, failure rate
- **Resource Utilization**: Tài nguyên sử dụng, efficiency

## 🚀 Best Practices
- Thiết kế worker stateless để dễ scale và recover
- Implement proper error handling và logging
- Sử dụng connection pooling cho database access
- Thiết lập monitoring và alerting cho worker health
- Định kỳ review và optimize worker configuration

---

**Tài liệu này là nền tảng lý thuyết cho việc thiết kế và triển khai Worker Pool trong dự án AI Camera Counting.** 