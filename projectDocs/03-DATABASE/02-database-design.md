# Database Design - AI Camera Counting System

## 📊 Tổng quan

Tài liệu này trình bày thiết kế tổng thể cho hệ thống lưu trữ dữ liệu của AI Camera Counting System, bao gồm Database (PostgreSQL), Cache (Redis), và Queue (RabbitMQ). Hệ thống được thiết kế để xử lý dữ liệu real-time từ hàng trăm camera streams đồng thời với khả năng mở rộng cao.

## 🎯 Mục tiêu thiết kế

- **Scalability**: Hỗ trợ xử lý hàng trăm camera streams đồng thời
- **Performance**: Đảm bảo response time < 100ms cho real-time data
- **Reliability**: 99.9% uptime với data consistency
- **Security**: Bảo mật dữ liệu người dùng và hệ thống
- **Maintainability**: Dễ dàng mở rộng và bảo trì

## 🏗️ Database Architecture Overview

### High-Level Database Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              DATABASE ARCHITECTURE OVERVIEW                     │
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
│  │                              DATA ACCESS LAYER                              │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Database  │  │   Cache     │  │   Queue     │  │   File      │        │ │
│  │  │   Connector │  │   Connector │  │   Connector │  │   Storage   │        │ │
│  │  │   (ORM)     │  │   (Redis)   │  │   (RabbitMQ)│  │   (S3/MinIO)│        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                             │
│                                    ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              STORAGE LAYER                                  │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Primary   │  │   Read      │  │   Cache     │  │   Message   │        │ │
│  │  │   Database  │  │   Replicas  │  │   (Redis)   │  │   Queue     │        │ │
│  │  │ (PostgreSQL)│  │ (PostgreSQL)│  │             │  │ (RabbitMQ)  │        │ │
│  │  │             │  │             │  │ • Session   │  │             │        │ │
│  │  │ • Users     │  │ • Analytics │  │ • Real-time │  │ • Events    │        │ │
│  │  │ • Cameras   │  │ • Reports   │  │ • Status    │  │ • Jobs      │        │ │
│  │  │ • Results   │  │ • History   │  │ • Cache     │  │ • Alerts    │        │ │
│  │  │ • Events    │  │ • Archive   │  │ • Locks     │  │ • Dead      │        │ │
│  │  │ • Analytics │  │ • Backup    │  │ • Flags     │  │   Letters   │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Data Flow Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              DATA FLOW ARCHITECTURE                             │
│                                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐      │
│  │   Camera    │    │   Worker    │    │   AI Model  │    │   Database  │      │
│  │   Stream    │    │   Pool      │    │   Engine    │    │   Layer     │      │
│  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘      │
│         │                   │                   │                   │          │
│         │ 1. RTSP Stream    │                   │                   │          │
│         │ (1920x1080, 25fps)│                   │                   │          │
│         │──────────────────►│                   │                   │          │
│         │                   │                   │                   │          │
│         │                   │ 2. Frame Capture  │                   │          │
│         │                   │ & Preprocessing   │                   │          │
│         │                   │ (Resize, Normalize)│                   │          │
│         │                   │──────────────────►│                   │          │
│         │                   │                   │                   │          │
│         │                   │                   │ 3. AI Detection   │          │
│         │                   │                   │ (YOLO/SSD Model)  │          │
│         │                   │                   │ (Person Detection)│          │
│         │                   │                   │──────────────────►│          │
│         │                   │                   │                   │          │
│         │                   │                   │ 4. Counting Logic │          │
│         │                   │                   │ (In/Out Tracking) │          │
│         │                   │                   │ (Zone Analysis)   │          │
│         │                   │                   │◄──────────────────┤          │
│         │                   │                   │                   │          │
│         │                   │ 5. Results        │                   │          │
│         │                   │ (Count, Confidence)│                   │          │
│         │                   │──────────────────►│                   │          │
│         │                   │                   │                   │          │
│         │                   │                   │ 6. Store & Cache  │          │
│         │                   │                   │ (PostgreSQL/Redis)│          │
│         │                   │                   │◄──────────────────┤          │
│         │                   │                   │                   │          │
│         │                   │ 7. Real-time      │                   │          │
│         │                   │ Broadcast         │                   │          │
│         │                   │ (WebSocket)       │                   │          │
│         │                   │◄──────────────────┤                   │          │
│         │                   │                   │                   │          │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Entity Relationship Diagram (ERD)

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              ENTITY RELATIONSHIP DIAGRAM                        │
│                                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │   users     │  │   cameras   │  │   zones     │  │   ai_models │            │
│  │             │  │             │  │             │  │             │            │
│  │ • id (PK)   │  │ • id (PK)   │  │ • id (PK)   │  │ • id (PK)   │            │
│  │ • username  │  │ • name      │  │ • name      │  │ • name      │            │
│  │ • email     │  │ • ip_address│  │ • camera_id │  │ • version   │            │
│  │ • role      │  │ • status    │  │ • coordinates│  │ • status    │            │
│  │ • is_active │  │ • config    │  │ • type      │  │ • config    │            │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘            │
│         │                   │                   │                   │            │
│         │ 1:N               │ 1:N               │ 1:N               │            │
│         │                   │                   │                   │            │
│         ▼                   ▼                   ▼                   ▼            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │user_sessions│  │camera_events│  │counting_results│  │model_logs  │            │
│  │             │  │             │  │             │  │             │            │
│  │ • id (PK)   │  │ • id (PK)   │  │ • id (PK)   │  │ • id (PK)   │            │
│  │ • user_id   │  │ • camera_id │  │ • camera_id │  │ • model_id  │            │
│  │ • token     │  │ • event_type│  │ • zone_id   │  │ • log_type  │            │
│  │ • expires   │  │ • timestamp │  │ • count_in  │  │ • message   │            │
│  │ • ip_address│  │ • data      │  │ • count_out │  │ • timestamp │            │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘            │
│         │                   │                   │                   │            │
│         │                   │                   │                   │            │
│         ▼                   ▼                   ▼                   ▼            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │audit_logs   │  │alerts       │  │analytics    │  │files        │            │
│  │             │  │             │  │             │  │             │            │
│  │ • id (PK)   │  │ • id (PK)   │  │ • id (PK)   │  │ • id (PK)   │            │
│  │ • table_name│  │ • type      │  │ • type      │  │ • filename  │            │
│  │ • action    │  │ • severity  │  │ • camera_id │  │ • path      │            │
│  │ • record_id │  │ • message   │  │ • data      │  │ • size      │            │
│  │ • user_id   │  │ • timestamp │  │ • timestamp │  │ • mime_type │            │
│  │ • timestamp │  │ • resolved  │  │ • period    │  │ • created_at│            │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘            │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Database Scaling Strategy

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              DATABASE SCALING STRATEGY                          │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              SCALING APPROACHES                             │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Read      │  │   Database  │  │   Data      │  │   Caching   │        │ │
│  │  │   Replicas  │  │   Partitioning│  │   Archiving │  │   Strategy  │        │ │
│  │  │             │  │             │  │             │  │             │        │ │
│  │  │ • Primary-  │  │ • Table     │  │ • Historical│  │ • Redis     │        │ │
│  │  │   Secondary │  │   Partitioning│  │   Data      │  │   Cache     │        │ │
│  │  │ • Load      │  │ • Index     │  │ • Cold      │  │ • Query     │        │ │
│  │  │   Distribution│  │   Partitioning│  │   Storage   │  │   Cache     │        │ │
│  │  │ • Analytics │  │ • Time-based│  │ • Compression│  │ • Result    │        │ │
│  │  │   Queries   │  │   Partitioning│  │ • Backup    │  │   Cache     │        │ │
│  │  │ • Reporting │  │ • Parallel  │  │ • Archive   │  │ • Session   │        │ │
│  │  │   Queries   │  │   Processing│  │   Policies  │  │   Cache     │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                             │
│                                    ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              IMPLEMENTATION PHASES                          │ │
│  │                                                                             │ │
│  │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │ │
│  │  │   Phase 1   │    │   Phase 2   │    │   Phase 3   │    │   Phase 4   │  │ │
│  │  │ Foundation  │    │ Read Replicas│    │ Partitioning│    │ Optimization│  │ │
│  │  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘  │ │
│  │         │                   │                   │                   │      │ │
│  │         │ • Single Database │ • Primary-Secondary│ • Table Partitioning│ • Advanced Caching│
│  │         │ • Basic Indexing  │ • Load Distribution│ • Time-based Archiving│ • Query Optimization│
│  │         │ • Simple Queries  │ • Analytics Queries│ • Data Compression│ • Performance Tuning│
│  │         │ • Basic Monitoring│ • Read Scaling    │ • Parallel Processing│ • Advanced Analytics│
│  │         │ • Backup Strategy │ • Failover Support│ • Cold Storage     │ • Real-time Analytics│
│  │         │                   │ • Health Monitoring│ • Archive Policies│ • Predictive Analytics│
│  │         │                   │                   │                   │      │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 📋 Database Design Principles

### 1. Normalization Strategy
- **3NF Compliance**: Đảm bảo database tuân thủ Third Normal Form
- **Selective Denormalization**: Denormalize cho các bảng analytics và reporting
- **Data Integrity**: Sử dụng foreign keys và constraints
- **Performance Balance**: Cân bằng giữa normalization và performance

### 2. Indexing Strategy
- **Primary Keys**: Auto-incrementing integers cho tất cả tables
- **Foreign Keys**: Index trên tất cả foreign key columns
- **Composite Indexes**: Cho các queries phức tạp
- **Partial Indexes**: Cho các điều kiện WHERE phổ biến
- **Time-based Indexes**: Cho các bảng có timestamp

### 3. Partitioning Strategy
- **Time-based Partitioning**: Cho các bảng events và analytics
- **Range Partitioning**: Theo ngày/tháng/năm
- **List Partitioning**: Theo camera_id hoặc zone_id
- **Hash Partitioning**: Cho các bảng lớn cần distribute

### 4. Data Retention Strategy
- **Hot Data**: 30 ngày gần nhất (PostgreSQL)
- **Warm Data**: 3-12 tháng (PostgreSQL với compression)
- **Cold Data**: 1-5 năm (Archive storage)
- **Historical Data**: 5+ năm (Long-term storage)

## 🔒 Security Considerations

### 1. Data Protection
- **Encryption at Rest**: Sử dụng PostgreSQL encryption
- **Encryption in Transit**: SSL/TLS cho tất cả connections
- **Column-level Encryption**: Cho sensitive data
- **Audit Logging**: Track tất cả data access và changes

### 2. Access Control
- **Role-based Access**: Database roles và permissions
- **Row-level Security**: Cho multi-tenant data
- **Connection Pooling**: Secure connection management
- **IP Whitelisting**: Restrict database access

### 3. Compliance
- **GDPR Compliance**: Data privacy và right to be forgotten
- **Data Retention**: Automated cleanup policies
- **Audit Trail**: Complete change history
- **Backup Encryption**: Encrypted backups

## 📊 Performance Optimization

### 1. Query Optimization
- **Query Planning**: Regular query analysis và optimization
- **Index Maintenance**: Regular index rebuilds và updates
- **Statistics Updates**: Keep table statistics current
- **Query Caching**: Application-level query caching

### 2. Connection Management
- **Connection Pooling**: Efficient connection reuse
- **Load Balancing**: Distribute read queries across replicas
- **Failover Handling**: Automatic failover to replicas
- **Health Monitoring**: Continuous database health checks

### 3. Monitoring and Alerting
- **Performance Metrics**: Query time, throughput, connections
- **Resource Monitoring**: CPU, memory, disk usage
- **Error Tracking**: Failed queries, connection errors
- **Capacity Planning**: Growth prediction và scaling

## 🔄 Migration and Backup Strategy

### 1. Migration Strategy
- **Zero-downtime Migrations**: Online schema changes
- **Rollback Plan**: Quick rollback procedures
- **Data Validation**: Post-migration data integrity checks
- **Performance Testing**: Pre-production migration testing

### 2. Backup Strategy
- **Full Backups**: Daily full database backups
- **Incremental Backups**: Hourly incremental backups
- **Point-in-time Recovery**: Continuous WAL archiving
- **Cross-region Backup**: Geographic redundancy

### 3. Disaster Recovery
- **RTO (Recovery Time Objective)**: < 4 hours
- **RPO (Recovery Point Objective)**: < 1 hour
- **Automated Recovery**: Scripted recovery procedures
- **Regular Testing**: Monthly disaster recovery drills

## 📈 Monitoring and Maintenance

### 1. Health Monitoring
- **Database Metrics**: Connection count, query performance
- **System Metrics**: CPU, memory, disk, network
- **Application Metrics**: Response time, error rates
- **Business Metrics**: Data volume, user activity

### 2. Maintenance Schedule
- **Daily**: Log rotation, connection cleanup
- **Weekly**: Statistics updates, index maintenance
- **Monthly**: Full backup verification, performance review
- **Quarterly**: Capacity planning, security audit

### 3. Alerting Rules
- **Critical**: Database down, disk full, connection limit
- **Warning**: High CPU usage, slow queries, disk space
- **Info**: Backup completion, maintenance tasks
- **Debug**: Query performance, index usage

---

**Tài liệu này cung cấp tổng quan về thiết kế database cho AI Camera Counting System, bao gồm kiến trúc, nguyên tắc thiết kế, và các chiến lược tối ưu hóa.** 