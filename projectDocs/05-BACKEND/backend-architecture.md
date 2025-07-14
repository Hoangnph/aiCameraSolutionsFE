# Backend Architecture Patterns - Patterns kiến trúc backend

## 📊 Tổng quan

Tài liệu này mô tả các patterns kiến trúc backend được sử dụng trong hệ thống AI Camera Counting, bao gồm microservices patterns, data patterns, và integration patterns.

## 🎯 Mục tiêu

### Mục tiêu chính
- **Scalability**: Khả năng mở rộng theo chiều ngang và dọc
- **Maintainability**: Code dễ bảo trì và mở rộng
- **Performance**: Hiệu suất cao với tải lớn
- **Reliability**: Độ tin cậy và fault tolerance
- **Security**: Bảo mật end-to-end
- **Testability**: Dễ dàng test và validate

### Yêu cầu kỹ thuật
- **Microservices Architecture**: Tách biệt các service
- **Event-Driven Architecture**: Xử lý bất đồng bộ
- **CQRS Pattern**: Tách biệt read/write operations
- **Repository Pattern**: Abstraction cho data access
- **Dependency Injection**: Loose coupling
- **Circuit Breaker**: Fault tolerance

## 🏗️ Microservices Architecture Patterns

### 1. Service Decomposition Pattern

#### Backend Architecture Overview Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              BACKEND ARCHITECTURE OVERVIEW                      │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                  │
│  │   API Gateway   │  │   Load Balancer │  │   Service Mesh  │                  │
│  │   (NGINX)       │  │   (HAProxy)     │  │   (Istio)       │                  │
│  │                 │  │                 │  │                 │                  │
│  │ • Route Requests│  │ • Traffic Dist  │  │ • Service Disc  │                  │
│  │ • Auth/Authorize│  │ • Health Check  │  │ • Circuit Breaker│                  │
│  │ • Rate Limiting │  │ • Failover      │  │ • Retry Logic   │                  │
│  │ • SSL/TLS       │  │ • Load Balancing│  │ • Observability │                  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘                  │
└─────────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              MICROSERVICES LAYER                               │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                  │
│  │   Auth Service  │  │  Camera Service │  │ Analytics Service│                  │
│  │   (Node.js)     │  │   (Python)      │  │   (Python)      │                  │
│  │                 │  │                 │  │                 │                  │
│  │ • User Auth     │  │ • Camera Mgmt   │  │ • Data Analytics│                  │
│  │ • JWT Tokens    │  │ • AI Processing │  │ • Report Gen    │                  │
│  │ • User Mgmt     │  │ • Worker Pool   │  │ • Metrics       │                  │
│  │ • Permissions   │  │ • Stream Mgmt   │  │ • Dashboards    │                  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘                  │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                  │
│  │ Notification    │  │   Worker Pool   │  │   WebSocket     │                  │
│  │   Service       │  │   Service       │  │   Service       │                  │
│  │                 │  │                 │  │                 │                  │
│  │ • Email/SMS     │  │ • Task Queue    │  │ • Real-time     │                  │
│  │ • Push Notif    │  │ • Worker Mgmt   │  │ • Broadcasting  │                  │
│  │ • Alert Mgmt    │  │ • Load Balance  │  │ • Connection    │                  │
│  │ • Templates     │  │ • Scaling       │  │ • Event Routing │                  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘                  │
└─────────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              DATA LAYER                                        │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                  │
│  │   PostgreSQL    │  │   Redis Cache   │  │   Message Queue │                  │
│  │   (Primary DB)  │  │   (L2 Cache)    │  │   (RabbitMQ)    │                  │
│  │                 │  │                 │  │                 │                  │
│  │ • User Data     │  │ • Session Data  │  │ • Event Queue   │                  │
│  │ • Camera Data   │  │ • Real-time     │  │ • Task Queue    │                  │
│  │ • Analytics     │  │ • Analytics     │  │ • Dead Letter   │                  │
│  │ • Audit Logs    │  │ • Rate Limiting │  │ • Retry Logic   │                  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

#### Microservices Decomposition Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              MICROSERVICES DECOMPOSITION                        │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              BOUNDED CONTEXTS                               │ │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐              │ │
│  │  │   User Mgmt     │  │   Camera Mgmt   │  │   Analytics     │              │ │
│  │  │   Context       │  │   Context       │  │   Context       │              │ │
│  │  │                 │  │                 │  │                 │              │ │
│  │  │ • Authentication│  │ • Camera CRUD   │  │ • Data Analysis │              │ │
│  │  │ • Authorization │  │ • Stream Mgmt   │  │ • Report Gen    │              │ │
│  │  │ • User Profile  │  │ • AI Processing │  │ • Metrics       │              │ │
│  │  │ • Role Mgmt     │  │ • Worker Pool   │  │ • Dashboards    │              │ │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘              │ │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐              │ │
│  │  │   Notification  │  │   Monitoring    │  │   Integration   │              │ │
│  │  │   Context       │  │   Context       │  │   Context       │              │ │
│  │  │                 │  │                 │  │                 │              │ │
│  │  │ • Email/SMS     │  │ • Health Check  │  │ • External APIs │              │ │
│  │  │ • Push Notif    │  │ • Metrics       │  │ • Webhooks      │              │ │
│  │  │ • Alert Mgmt    │  │ • Logging       │  │ • Data Sync     │              │ │
│  │  │ • Templates     │  │ • Alerting      │  │ • ETL Process   │              │ │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘              │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              SERVICE BOUNDARIES                             │ │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐              │ │
│  │  │   Auth Service  │  │  Camera Service │  │ Analytics Service│              │ │
│  │  │   (Port: 3001)  │  │   (Port: 8000)  │  │   (Port: 8001)  │              │ │
│  │  │                 │  │                 │  │                 │              │ │
│  │  │ • /auth/*       │  │ • /cameras/*    │  │ • /analytics/*  │              │ │
│  │  │ • /users/*      │  │ • /workers/*    │  │ • /reports/*    │              │ │
│  │  │ • /roles/*      │  │ • /streams/*    │  │ • /metrics/*    │              │ │
│  │  │ • /permissions/*│  │ • /ai-models/*  │  │ • /dashboards/* │              │ │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘              │ │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐              │ │
│  │  │ Notification    │  │   Worker Pool   │  │   WebSocket     │              │ │
│  │  │   Service       │  │   Service       │  │   Service       │              │ │
│  │  │   (Port: 8002)  │  │   (Port: 8003)  │  │   (Port: 8004)  │              │ │
│  │  │                 │  │                 │  │                 │              │ │
│  │  │ • /notifications│  │ • /workers/*    │  │ • /ws/*         │              │ │
│  │  │ • /templates/*  │  │ • /tasks/*      │  │ • /events/*     │              │ │
│  │  │ • /alerts/*     │  │ • /queue/*      │  │ • /broadcast/*  │              │ │
│  │  │ • /channels/*   │  │ • /scaling/*    │  │ • /connections/*│              │ │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘              │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

#### Service Communication Patterns Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              SERVICE COMMUNICATION PATTERNS                     │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              SYNCHRONOUS COMMUNICATION                      │ │
│  │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │ │
│  │  │   Frontend  │    │   API       │    │   Camera    │    │   Auth      │  │ │
│  │  │   (React)   │    │   Gateway   │    │   Service   │    │   Service   │  │ │
│  │  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘  │ │
│  │         │                   │                   │                   │      │ │
│  │         │ 1. HTTP Request   │                   │                   │      │ │
│  │         │──────────────────►│                   │                   │      │ │
│  │         │                   │ 2. Route Request │                   │      │ │
│  │         │                   │──────────────────►│                   │      │ │
│  │         │                   │                   │ 3. Auth Check    │      │ │
│  │         │                   │                   │──────────────────►│      │ │
│  │         │                   │                   │                   │      │ │
│  │         │                   │                   │ 4. Auth Response │      │ │
│  │         │                   │                   │◄──────────────────│      │ │
│  │         │                   │                   │                   │      │ │
│  │         │                   │ 5. Process Request│                   │      │ │
│  │         │                   │                   │                   │      │ │
│  │         │ 6. HTTP Response  │                   │                   │      │ │
│  │         │◄──────────────────│                   │                   │      │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              ASYNCHRONOUS COMMUNICATION                     │ │
│  │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │ │
│  │  │   Camera    │    │   Message   │    │   Worker    │    │ Analytics   │  │ │
│  │  │   Service   │    │   Queue     │    │   Pool      │    │ Service     │  │ │
│  │  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘  │ │
│  │         │                   │                   │                   │      │ │
│  │         │ 1. Publish Event  │                   │                   │      │ │
│  │         │──────────────────►│                   │                   │      │ │
│  │         │                   │                   │                   │      │ │
│  │         │                   │ 2. Consume Event  │                   │      │ │
│  │         │                   │──────────────────►│                   │      │ │
│  │         │                   │                   │                   │      │ │
│  │         │                   │                   │ 3. Process Task   │      │ │
│  │         │                   │                   │                   │      │ │
│  │         │                   │                   │ 4. Publish Result │      │ │
│  │         │                   │                   │──────────────────►│      │ │
│  │         │                   │                   │                   │      │ │
│  │         │                   │ 5. Consume Result │                   │      │ │
│  │         │                   │──────────────────────────────────────►│      │ │
│  │         │                   │                   │                   │      │ │
│  │         │                   │                   │ 6. Update Analytics│     │ │
│  │         │                   │                   │                   │      │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

#### Data Architecture Patterns Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              DATA ARCHITECTURE PATTERNS                         │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              DATABASE PER SERVICE                           │ │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐              │ │
│  │  │   Auth DB       │  │   Camera DB     │  │ Analytics DB    │              │ │
│  │  │   (PostgreSQL)  │  │   (PostgreSQL)  │  │   (TimescaleDB) │              │ │
│  │  │                 │  │                 │  │                 │              │ │
│  │  │ • users         │  │ • cameras       │  │ • hourly_analytics            │ │
│  │  │ • user_sessions │  │ • counting_results│ │ • daily_analytics             │ │
│  │  │ • permissions   │  │ • camera_events │  │ • monthly_analytics           │ │
│  │  │ • roles         │  │ • ai_models     │  │ • performance_metrics         │ │
│  │  │ • audit_logs    │  │ • worker_assignments│ │ • trend_analysis            │ │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘              │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              CACHING STRATEGY                               │ │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐              │ │
│  │  │   L1 Cache      │  │   L2 Cache      │  │   L3 Cache      │              │ │
│  │  │   (In-Memory)   │  │   (Redis)       │  │   (CDN)         │              │ │
│  │  │                 │  │                 │  │                 │              │ │
│  │  │ • Session Data  │  │ • User Data     │  │ • Static Assets │              │ │
│  │  │ • Temp Results  │  │ • Camera Data   │  │ • Images        │              │ │
│  │  │ • Query Cache   │  │ • Analytics     │  │ • Videos        │              │ │
│  │  │ • Rate Limiting │  │ • Real-time     │  │ • Documents     │              │ │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘              │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              DATA CONSISTENCY PATTERNS                      │ │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐              │ │
│  │  │   Strong        │  │   Eventual      │  │   Causal        │              │ │
│  │  │   Consistency   │  │   Consistency   │  │   Consistency   │              │ │
│  │  │                 │  │                 │  │                 │              │ │
│  │  │ • User Auth     │  │ • Analytics     │  │ • Notifications │              │ │
│  │  │ • Permissions   │  │ • Reports       │  │ • Alerts        │              │ │
│  │  │ • Critical Data │  │ • Metrics       │  │ • Events        │              │ │
│  │  │ • Transactions  │  │ • Aggregations  │  │ • Messages      │              │ │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘              │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

#### API Gateway Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              API GATEWAY ARCHITECTURE                           │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              GATEWAY LAYERS                                 │ │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐              │ │
│  │  │   Security      │  │   Routing       │  │   Monitoring    │              │ │
│  │  │   Layer         │  │   Layer         │  │   Layer         │              │ │
│  │  │                 │  │                 │  │                 │              │ │
│  │  │ • Authentication│  │ • Load Balancing│  │ • Metrics       │              │ │
│  │  │ • Authorization │  │ • Service Disc  │  │ • Logging       │              │ │
│  │  │ • Rate Limiting │  │ • Circuit Breaker│ │ • Alerting      │              │ │
│  │  │ • SSL/TLS       │  │ • Retry Logic   │  │ • Tracing       │              │ │
│  │  │ • CORS          │  │ • Timeout Mgmt  │  │ • Health Check  │              │ │
│  │  │ • Input Valid   │  │ • Version Mgmt  │  │ • Performance   │              │ │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘              │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              ROUTING RULES                                  │ │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐              │ │
│  │  │   Auth Routes   │  │   Camera Routes │  │ Analytics Routes│              │ │
│  │  │                 │  │                 │  │                 │              │ │
│  │  │ • /api/v1/auth/*│  │ • /api/v1/cameras/*│ • /api/v1/analytics/*        │ │
│  │  │ • /api/v1/users/*│ │ • /api/v1/workers/*│ • /api/v1/reports/*          │ │
│  │  │ • /api/v1/roles/*│ │ • /api/v1/streams/*│ • /api/v1/metrics/*          │ │
│  │  │ • /api/v1/permissions/*│ • /api/v1/ai-models/*│ • /api/v1/dashboards/* │ │
│  │  │                 │  │                 │  │                 │              │ │
│  │  │ Target: Auth    │  │ Target: Camera  │  │ Target: Analytics│            │ │
│  │  │ Service         │  │ Service         │  │ Service         │              │ │
│  │  │ Port: 3001      │  │ Port: 8000      │  │ Port: 8001      │              │ │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘              │ │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐              │ │
│  │  │ Notification    │  │   Worker Pool   │  │   WebSocket     │              │ │
│  │  │   Routes        │  │   Routes        │  │   Routes        │              │ │
│  │  │                 │  │                 │  │                 │              │ │
│  │  │ • /api/v1/notifications/*│ • /api/v1/workers/*│ • /ws/*                 │ │
│  │  │ • /api/v1/templates/*│ • /api/v1/tasks/*│ • /api/v1/events/*           │ │
│  │  │ • /api/v1/alerts/*│ • /api/v1/queue/*│ • /api/v1/broadcast/*          │ │
│  │  │ • /api/v1/channels/*│ • /api/v1/scaling/*│ • /api/v1/connections/*     │ │
│  │  │                 │  │                 │  │                 │              │ │
│  │  │ Target: Notification│ Target: Worker │  │ Target: WebSocket│            │ │
│  │  │ Service         │  │ Pool Service    │  │ Service         │              │ │
│  │  │ Port: 8002      │  │ Port: 8003      │  │ Port: 8004      │              │ │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘              │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

#### Backend Security Patterns Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              BACKEND SECURITY PATTERNS                          │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              SECURITY LAYERS                                │ │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐              │ │
│  │  │   Network       │  │   Application   │  │   Data          │              │ │
│  │  │   Security      │  │   Security      │  │   Security      │              │ │
│  │  │                 │  │                 │  │                 │              │ │
│  │  │ • Firewall      │  │ • Authentication│  │ • Encryption    │              │ │
│  │  │ • DDoS Protect  │  │ • Authorization │  │ • Access Control│              │ │
│  │  │ • VPN           │  │ • Input Valid   │  │ • Audit Logging │              │ │
│  │  │ • IDS/IPS       │  │ • Session Mgmt  │  │ • Backup        │              │ │
│  │  │ • Load Balancer │  │ • Rate Limiting │  │ • Compliance    │              │ │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘              │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              AUTHENTICATION FLOW                            │ │
│  │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │ │
│  │  │   Client    │    │   API       │    │   Auth      │    │   Database  │  │ │
│  │  │   (Frontend)│    │   Gateway   │    │   Service   │    │             │  │ │
│  │  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘  │ │
│  │         │                   │                   │                   │      │ │
│  │         │ 1. Login Request  │                   │                   │      │ │
│  │         │──────────────────►│                   │                   │      │ │
│  │         │                   │ 2. Route to Auth  │                   │      │ │
│  │         │                   │──────────────────►│                   │      │ │
│  │         │                   │                   │ 3. Validate User  │      │ │
│  │         │                   │                   │──────────────────►│      │ │
│  │         │                   │                   │                   │      │ │
│  │         │                   │                   │ 4. User Data      │      │ │
│  │         │                   │                   │◄──────────────────│      │ │
│  │         │                   │                   │                   │      │ │
│  │         │                   │ 5. Generate JWT   │                   │      │ │
│  │         │                   │                   │                   │      │ │
│  │         │ 6. JWT Response   │                   │                   │      │ │
│  │         │◄──────────────────│                   │                   │      │ │
│  │         │                   │                   │                   │      │ │
│  │         │ 7. Store Token    │                   │                   │      │ │
│  │         │ (localStorage)    │                   │                   │      │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              AUTHORIZATION MATRIX                           │ │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐              │ │
│  │  │   Roles         │  │   Permissions   │  │   Resources     │              │ │
│  │  │                 │  │                 │  │                 │              │ │
│  │  │ • Super Admin   │  │ • camera:read   │  │ • /cameras/*    │              │ │
│  │  │ • Admin         │  │ • camera:write  │  │ • /users/*      │              │ │
│  │  │ • Operator      │  │ • camera:delete │  │ • /analytics/*  │              │ │
│  │  │ • Viewer        │  │ • user:read     │  │ • /reports/*    │              │ │
│  │  │ • Guest         │  │ • user:write    │  │ • /settings/*   │              │ │
│  │  │                 │  │ • analytics:read│  │ • /logs/*       │              │ │
│  │  │                 │  │ • analytics:write│ │ • /admin/*      │              │ │
│  │  │                 │  │ • system:admin  │  │ • /api/*        │              │ │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘              │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

#### Service Boundaries
```yaml
# Service Decomposition
services:
  auth_service:
    responsibility: "Authentication & Authorization"
    bounded_context: "User Management"
    data_ownership: "User data, sessions, permissions"
    api_endpoints:
      - "/auth/login"
      - "/auth/register"
      - "/auth/refresh"
      - "/auth/logout"
  
  camera_service:
    responsibility: "Camera Management & Processing"
    bounded_context: "Camera Operations"
    data_ownership: "Camera data, streams, configurations"
    api_endpoints:
      - "/cameras"
      - "/cameras/{id}/stream"
      - "/cameras/{id}/config"
      - "/cameras/{id}/status"
  
  analytics_service:
    responsibility: "Analytics & Reporting"
    bounded_context: "Data Analytics"
    data_ownership: "Analytics data, reports, metrics"
    api_endpoints:
      - "/analytics/reports"
      - "/analytics/metrics"
      - "/analytics/export"
      - "/analytics/dashboard"
  
  notification_service:
    responsibility: "Notifications & Alerts"
    bounded_context: "Communication"
    data_ownership: "Notification templates, delivery logs"
    api_endpoints:
      - "/notifications/send"
      - "/notifications/templates"
      - "/notifications/history"
```

#### Service Communication
```yaml
# Service Communication Patterns
communication:
  synchronous:
    - http_rest: "Direct API calls"
    - grpc: "High-performance RPC"
    - graphql: "Flexible data querying"
  
  asynchronous:
    - message_queue: "Event-driven communication"
    - pub_sub: "Broadcast events"
    - event_sourcing: "Event store"
  
  patterns:
    - saga_pattern: "Distributed transactions"
    - circuit_breaker: "Fault tolerance"
    - bulkhead: "Isolation"
    - retry: "Resilience"
```

### 2. API Gateway Pattern

#### Gateway Architecture
```yaml
# API Gateway Configuration
api_gateway:
  responsibilities:
    - routing: "Route requests to appropriate services"
    - authentication: "Centralized authentication"
    - rate_limiting: "API throttling"
    - caching: "Response caching"
    - monitoring: "Request/response logging"
    - transformation: "Request/response transformation"
  
  routing_rules:
    - pattern: "/api/v1/auth/*"
      service: "auth_service"
      timeout: "5s"
      retries: 3
    
    - pattern: "/api/v1/cameras/*"
      service: "camera_service"
      timeout: "10s"
      retries: 2
    
    - pattern: "/api/v1/analytics/*"
      service: "analytics_service"
      timeout: "15s"
      retries: 1
```

#### Gateway Implementation
```javascript
// API Gateway Implementation
const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');

const app = express();

// Authentication middleware
app.use('/api/v1/*', authenticateToken);

// Rate limiting middleware
app.use('/api/v1/*', rateLimiter);

// Service routing
app.use('/api/v1/auth', createProxyMiddleware({
  target: 'http://auth-service:3001',
  changeOrigin: true,
  timeout: 5000,
  retries: 3
}));

app.use('/api/v1/cameras', createProxyMiddleware({
  target: 'http://camera-service:3002',
  changeOrigin: true,
  timeout: 10000,
  retries: 2
}));

app.use('/api/v1/analytics', createProxyMiddleware({
  target: 'http://analytics-service:3003',
  changeOrigin: true,
  timeout: 15000,
  retries: 1
}));
```

## 📊 Data Architecture Patterns

### 1. Database per Service Pattern

#### Database Design
```yaml
# Database per Service
databases:
  auth_db:
    service: "auth_service"
    type: "PostgreSQL"
    schema:
      - users
      - user_sessions
      - permissions
      - roles
      - audit_logs
  
  camera_db:
    service: "camera_service"
    type: "PostgreSQL"
    schema:
      - cameras
      - camera_configs
      - counting_results
      - camera_events
      - ai_models
  
  analytics_db:
    service: "analytics_service"
    type: "PostgreSQL + TimescaleDB"
    schema:
      - hourly_analytics
      - daily_analytics
      - monthly_analytics
      - performance_metrics
      - trend_analysis
```

#### Data Consistency
```yaml
# Data Consistency Patterns
consistency_patterns:
  eventual_consistency:
    - saga_pattern: "Distributed transactions"
    - event_sourcing: "Event-driven consistency"
    - cqrs: "Command/Query separation"
  
  strong_consistency:
    - distributed_transactions: "2PC/3PC"
    - consensus_algorithms: "Raft/Paxos"
    - database_sharding: "Horizontal partitioning"
```

### 2. CQRS Pattern (Command Query Responsibility Segregation)

#### CQRS Implementation
```javascript
// Command Handler
class CreateCameraCommandHandler {
  async handle(command) {
    const camera = new Camera({
      name: command.name,
      location: command.location,
      stream_url: command.stream_url
    });
    
    await this.cameraRepository.save(camera);
    
    // Publish event
    await this.eventBus.publish(new CameraCreatedEvent(camera.id));
    
    return camera.id;
  }
}

// Query Handler
class GetCameraQueryHandler {
  async handle(query) {
    return await this.cameraReadRepository.findById(query.cameraId);
  }
}

// Command
class CreateCameraCommand {
  constructor(name, location, stream_url) {
    this.name = name;
    this.location = location;
    this.stream_url = stream_url;
  }
}

// Query
class GetCameraQuery {
  constructor(cameraId) {
    this.cameraId = cameraId;
  }
}
```

#### Event Sourcing
```javascript
// Event Store
class EventStore {
  async saveEvents(aggregateId, events, expectedVersion) {
    const eventStream = await this.getEventStream(aggregateId);
    
    if (eventStream.version !== expectedVersion) {
      throw new ConcurrencyError();
    }
    
    for (const event of events) {
      await this.saveEvent(aggregateId, event);
    }
  }
  
  async getEvents(aggregateId) {
    return await this.eventRepository.findByAggregateId(aggregateId);
  }
}

// Aggregate
class CameraAggregate {
  constructor(id) {
    this.id = id;
    this.name = null;
    this.location = null;
    this.status = 'inactive';
    this.uncommittedEvents = [];
  }
  
  create(name, location, stream_url) {
    this.apply(new CameraCreatedEvent(this.id, name, location, stream_url));
  }
  
  activate() {
    this.apply(new CameraActivatedEvent(this.id));
  }
  
  apply(event) {
    this.handle(event);
    this.uncommittedEvents.push(event);
  }
  
  handle(event) {
    if (event instanceof CameraCreatedEvent) {
      this.name = event.name;
      this.location = event.location;
      this.status = 'active';
    } else if (event instanceof CameraActivatedEvent) {
      this.status = 'active';
    }
  }
}
```

## 🔄 Event-Driven Architecture Patterns

### 1. Event Sourcing Pattern

#### Event Structure
```javascript
// Event Base Class
class DomainEvent {
  constructor(aggregateId, version, timestamp = new Date()) {
    this.aggregateId = aggregateId;
    this.version = version;
    this.timestamp = timestamp;
    this.eventType = this.constructor.name;
  }
}

// Camera Events
class CameraCreatedEvent extends DomainEvent {
  constructor(aggregateId, name, location, stream_url) {
    super(aggregateId, 1);
    this.name = name;
    this.location = location;
    this.stream_url = stream_url;
  }
}

class CameraActivatedEvent extends DomainEvent {
  constructor(aggregateId) {
    super(aggregateId, 2);
  }
}

class CameraDeactivatedEvent extends DomainEvent {
  constructor(aggregateId) {
    super(aggregateId, 3);
  }
}

class CountingResultEvent extends DomainEvent {
  constructor(aggregateId, count, timestamp) {
    super(aggregateId, 4);
    this.count = count;
    this.timestamp = timestamp;
  }
}
```

#### Event Handler
```javascript
// Event Handler
class CameraEventHandler {
  async handle(event) {
    switch (event.eventType) {
      case 'CameraCreatedEvent':
        await this.handleCameraCreated(event);
        break;
      case 'CameraActivatedEvent':
        await this.handleCameraActivated(event);
        break;
      case 'CountingResultEvent':
        await this.handleCountingResult(event);
        break;
    }
  }
  
  async handleCameraCreated(event) {
    // Update read model
    await this.cameraReadRepository.save({
      id: event.aggregateId,
      name: event.name,
      location: event.location,
      status: 'active',
      created_at: event.timestamp
    });
    
    // Send notifications
    await this.notificationService.sendCameraCreatedNotification(event);
  }
  
  async handleCountingResult(event) {
    // Update analytics
    await this.analyticsService.updateCount(event.aggregateId, event.count, event.timestamp);
    
    // Check thresholds
    await this.alertService.checkThresholds(event.aggregateId, event.count);
  }
}
```

### 2. Saga Pattern

#### Saga Implementation
```javascript
// Saga Coordinator
class CameraCreationSaga {
  constructor(cameraService, workerService, notificationService) {
    this.cameraService = cameraService;
    this.workerService = workerService;
    this.notificationService = notificationService;
  }
  
  async execute(command) {
    const sagaId = this.generateSagaId();
    
    try {
      // Step 1: Create camera
      const camera = await this.cameraService.createCamera(command);
      
      // Step 2: Assign worker
      await this.workerService.assignCameraToWorker(camera.id);
      
      // Step 3: Send notification
      await this.notificationService.sendCameraCreatedNotification(camera);
      
      return camera;
    } catch (error) {
      // Compensating actions
      await this.compensate(sagaId, error);
      throw error;
    }
  }
  
  async compensate(sagaId, error) {
    // Rollback actions in reverse order
    try {
      await this.notificationService.rollbackNotification(sagaId);
      await this.workerService.unassignCamera(sagaId);
      await this.cameraService.deleteCamera(sagaId);
    } catch (compensationError) {
      // Log compensation error
      console.error('Compensation failed:', compensationError);
    }
  }
}
```

## 🛡️ Resilience Patterns

### 1. Circuit Breaker Pattern

#### Circuit Breaker Implementation
```javascript
// Circuit Breaker
class CircuitBreaker {
  constructor(failureThreshold = 5, timeout = 60000) {
    this.failureThreshold = failureThreshold;
    this.timeout = timeout;
    this.failureCount = 0;
    this.lastFailureTime = null;
    this.state = 'CLOSED'; // CLOSED, OPEN, HALF_OPEN
  }
  
  async execute(operation) {
    if (this.state === 'OPEN') {
      if (this.shouldAttemptReset()) {
        this.state = 'HALF_OPEN';
      } else {
        throw new CircuitBreakerOpenError();
      }
    }
    
    try {
      const result = await operation();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }
  
  onSuccess() {
    this.failureCount = 0;
    this.state = 'CLOSED';
  }
  
  onFailure() {
    this.failureCount++;
    this.lastFailureTime = Date.now();
    
    this.state = 'OPEN';
  }
  
  shouldAttemptReset() {
    return Date.now() - this.lastFailureTime > this.timeout;
  }
}

// Usage
const circuitBreaker = new CircuitBreaker(5, 60000);

const cameraService = {
  async getCamera(id) {
    return await circuitBreaker.execute(async () => {
      return await this.httpClient.get(`/cameras/${id}`);
    });
  }
};
```

### 2. Retry Pattern

#### Retry Implementation
```javascript
// Retry Pattern
class RetryPattern {
  constructor(maxRetries = 3, backoffStrategy = 'exponential') {
    this.maxRetries = maxRetries;
    this.backoffStrategy = backoffStrategy;
  }
  
  async execute(operation) {
    let lastError;
    
    for (let attempt = 0; attempt <= this.maxRetries; attempt++) {
      try {
        return await operation();
      } catch (error) {
        lastError = error;
        
        if (attempt === this.maxRetries) {
          throw lastError;
        }
        
        if (!this.isRetryable(error)) {
          throw error;
        }
        
        await this.delay(this.getBackoffDelay(attempt));
      }
    }
  }
  
  isRetryable(error) {
    const retryableErrors = [
      'ECONNRESET',
      'ETIMEDOUT',
      'ENOTFOUND',
      'ECONNREFUSED'
    ];
    
    return retryableErrors.includes(error.code) || 
           (error.status >= 500 && error.status < 600);
  }
  
  getBackoffDelay(attempt) {
    switch (this.backoffStrategy) {
      case 'exponential':
        return Math.pow(2, attempt) * 1000;
      case 'linear':
        return (attempt + 1) * 1000;
      case 'fixed':
        return 1000;
      default:
        return 1000;
    }
  }
  
  delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}
```

## 📊 Repository Pattern

### 1. Repository Implementation

#### Base Repository
```javascript
// Base Repository
class BaseRepository {
  constructor(model) {
    this.model = model;
  }
  
  async findById(id) {
    return await this.model.findByPk(id);
  }
  
  async findAll(options = {}) {
    return await this.model.findAll(options);
  }
  
  async create(data) {
    return await this.model.create(data);
  }
  
  async update(id, data) {
    const entity = await this.findById(id);
    if (!entity) {
      throw new EntityNotFoundError();
    }
    return await entity.update(data);
  }
  
  async delete(id) {
    const entity = await this.findById(id);
    if (!entity) {
      throw new EntityNotFoundError();
    }
    await entity.destroy();
  }
  
  async findOne(where) {
    return await this.model.findOne({ where });
  }
  
  async count(where = {}) {
    return await this.model.count({ where });
  }
}
```

#### Camera Repository
```javascript
// Camera Repository
class CameraRepository extends BaseRepository {
  constructor(cameraModel) {
    super(cameraModel);
  }
  
  async findByStatus(status) {
    return await this.findAll({
      where: { status },
      include: ['worker', 'ai_model']
    });
  }
  
  async findByLocation(location) {
    return await this.findAll({
      where: { location },
      include: ['worker', 'ai_model']
    });
  }
  
  async findActiveCameras() {
    return await this.findByStatus('active');
  }
  
  async updateStatus(id, status) {
    return await this.update(id, { status });
  }
  
  async assignWorker(cameraId, workerId) {
    return await this.update(cameraId, { worker_id: workerId });
  }
  
  async getCameraWithAnalytics(id) {
    return await this.model.findByPk(id, {
      include: [
        'worker',
        'ai_model',
        'counting_results',
        'camera_events'
      ]
    });
  }
}
```

## 🔧 Dependency Injection Pattern

### 1. DI Container

#### Container Implementation
```javascript
// Dependency Injection Container
class Container {
  constructor() {
    this.services = new Map();
    this.singletons = new Map();
  }
  
  register(name, factory, options = {}) {
    this.services.set(name, { factory, options });
  }
  
  resolve(name) {
    const service = this.services.get(name);
    if (!service) {
      throw new Error(`Service ${name} not registered`);
    }
    
    if (service.options.singleton) {
      if (!this.singletons.has(name)) {
        this.singletons.set(name, service.factory(this));
      }
      return this.singletons.get(name);
    }
    
    return service.factory(this);
  }
}

// Service Registration
const container = new Container();

// Register services
container.register('database', (container) => {
  return new Database(config.database);
}, { singleton: true });

container.register('cameraRepository', (container) => {
  const database = container.resolve('database');
  return new CameraRepository(database.models.Camera);
}, { singleton: true });

container.register('cameraService', (container) => {
  const cameraRepository = container.resolve('cameraRepository');
  const eventBus = container.resolve('eventBus');
  return new CameraService(cameraRepository, eventBus);
}, { singleton: true });

container.register('cameraController', (container) => {
  const cameraService = container.resolve('cameraService');
  return new CameraController(cameraService);
}, { singleton: true });
```

## 🧪 Testing Patterns

### 1. Unit Testing Patterns

#### Service Testing
```javascript
// Camera Service Test
describe('CameraService', () => {
  let cameraService;
  let mockCameraRepository;
  let mockEventBus;
  
  beforeEach(() => {
    mockCameraRepository = {
      create: jest.fn(),
      findById: jest.fn(),
      update: jest.fn(),
      delete: jest.fn()
    };
    
    mockEventBus = {
      publish: jest.fn()
    };
    
    cameraService = new CameraService(mockCameraRepository, mockEventBus);
  });
  
  describe('createCamera', () => {
    it('should create camera successfully', async () => {
      const cameraData = {
        name: 'Test Camera',
        location: 'Test Location',
        stream_url: 'rtsp://test.com/stream'
      };
      
      const expectedCamera = { id: 1, ...cameraData, status: 'active' };
      mockCameraRepository.create.mockResolvedValue(expectedCamera);
      
      const result = await cameraService.createCamera(cameraData);
      
      expect(mockCameraRepository.create).toHaveBeenCalledWith(cameraData);
      expect(mockEventBus.publish).toHaveBeenCalledWith(
        expect.objectContaining({
          eventType: 'CameraCreatedEvent',
          aggregateId: 1
        })
      );
      expect(result).toEqual(expectedCamera);
    });
    
    it('should throw error when camera creation fails', async () => {
      const cameraData = { name: 'Test Camera' };
      const error = new Error('Database error');
      mockCameraRepository.create.mockRejectedValue(error);
      
      await expect(cameraService.createCamera(cameraData)).rejects.toThrow('Database error');
    });
  });
});
```

### 2. Integration Testing Patterns

#### API Integration Test
```javascript
// API Integration Test
describe('Camera API Integration', () => {
  let app;
  let server;
  
  beforeAll(async () => {
    app = express();
    setupRoutes(app);
    server = app.listen(0);
  });
  
  afterAll(async () => {
    await server.close();
  });
  
  describe('POST /api/v1/cameras', () => {
    it('should create camera successfully', async () => {
      const cameraData = {
        name: 'Integration Test Camera',
        location: 'Test Location',
        stream_url: 'rtsp://test.com/stream'
      };
      
      const response = await request(app)
        .post('/api/v1/cameras')
        .set('Authorization', `Bearer ${validToken}`)
        .send(cameraData)
        .expect(201);
      
      expect(response.body.success).toBe(true);
      expect(response.body.data.name).toBe(cameraData.name);
      expect(response.body.data.status).toBe('active');
    });
    
    it('should return 400 for invalid data', async () => {
      const invalidData = { name: '' };
      
      const response = await request(app)
        .post('/api/v1/cameras')
        .set('Authorization', `Bearer ${validToken}`)
        .send(invalidData)
        .expect(400);
      
      expect(response.body.success).toBe(false);
      expect(response.body.errors).toBeDefined();
    });
  });
});
```

## 🚀 Implementation Roadmap

### Phase 1: Foundation (Weeks 1-2)
- [ ] Setup microservices architecture
- [ ] Implement API Gateway
- [ ] Setup database per service
- [ ] Implement basic repository pattern

### Phase 2: Advanced Patterns (Weeks 3-4)
- [ ] Implement CQRS pattern
- [ ] Setup event sourcing
- [ ] Implement saga pattern
- [ ] Add circuit breaker pattern

### Phase 3: Testing & Optimization (Weeks 5-6)
- [ ] Implement comprehensive testing
- [ ] Add monitoring and logging
- [ ] Performance optimization
- [ ] Documentation review

---

**Tài liệu này cung cấp các patterns kiến trúc backend toàn diện cho hệ thống AI Camera Counting, đảm bảo tính scalable, maintainable và reliable.**
