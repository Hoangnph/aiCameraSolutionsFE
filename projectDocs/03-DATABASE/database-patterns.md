# Database Patterns - Patterns Database

## 📊 Tổng quan

Tài liệu này trình bày các patterns lý thuyết về database design và management cho hệ thống AI Camera Counting, bao gồm relational và NoSQL databases.

## 🎯 Mục tiêu
- Đảm bảo database scalable, performant và reliable
- Tối ưu hóa data access patterns và query performance
- Đảm bảo data integrity và consistency
- Cung cấp efficient data storage và retrieval

## 🏗️ Database Architecture Patterns

### 1. Database Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              DATABASE ARCHITECTURE OVERVIEW                    │
│                                                                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                  │
│  │   Application   │  │   Database      │  │   Storage       │                  │
│  │   Layer         │  │   Layer         │  │   Layer         │                  │
│  │                 │  │                 │  │                 │                  │
│  │ • Web App       │  │ • Primary DB    │  │ • SSD Storage   │                  │
│  │ • Mobile App    │  │ • Read Replicas │  │ • HDD Storage   │                  │
│  │ • API Services  │  │ • Cache Layer   │  │ • Cloud Storage │                  │
│  │ • Worker        │  │ • Search Index  │  │ • Backup        │                  │
│  │   Services      │  │ • Analytics DB  │  │   Storage       │                  │
│  │ • Analytics     │  │ • Archive DB    │  │ • Archive       │                  │
│  │   Services      │  │ • Time Series   │  │   Storage       │                  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘                  │
│           │                       │                       │                     │
│           │                       │                       │                     │
│           ▼                       ▼                       ▼                     │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                  │
│  │   Connection    │  │   Query         │  │   Data          │                  │
│  │   Layer         │  │   Processing    │  │   Management    │                  │
│  │                 │  │                 │  │                 │                  │
│  │ • Connection    │  │ • Query         │  │ • Data          │                  │
│  │   Pooling       │  │   Optimization  │  │   Validation    │                  │
│  │ • Load          │  │ • Query         │  │ • Data          │                  │
│  │   Balancing     │  │   Caching       │  │   Transformation│                  │
│  │ • Failover      │  │ • Query         │  │ • Data          │                  │
│  │   Handling      │  │   Routing       │  │   Migration     │                  │
│  │ • Health        │  │ • Query         │  │ • Data          │                  │
│  │   Monitoring    │  │   Monitoring    │  │   Backup        │                  │
│  │ • Connection    │  │ • Query         │  │ • Data          │                  │
│  │   Encryption    │  │   Logging       │  │   Recovery      │                  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘                  │
└─────────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              DATABASE PATTERNS                                 │
│                                                                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                  │
│  │   Single        │  │   Database per  │  │   Shared        │                  │
│  │   Database      │  │   Service       │  │   Database      │                  │
│  │                 │  │                 │  │                 │                  │
│  │ • Centralized   │  │ • Microservice  │  │ • Multiple      │                  │
│  │   Database      │  │   Isolation     │  │   Services      │                  │
│  │ • Simple        │  │ • Independent   │  │ • Shared        │                  │
│  │   Architecture  │  │   Schemas       │  │   Schema        │                  │
│  │ • Easy          │  │ • Service       │  │ • Data          │                  │
│  │   Management    │  │   Autonomy      │  │   Consistency   │                  │
│  │ • ACID          │  │ • Technology    │  │ • Transaction   │                  │
│  │   Compliance    │  │   Flexibility   │  │   Management    │                  │
│  │ • Single Point  │  │ • Scalability   │  │ • Complex       │                  │
│  │   of Failure    │  │ • Data          │  │   Coordination  │                  │
│  │ • Limited       │  │   Ownership     │  │ • Coupling      │                  │
│  │   Scalability   │  │ • Independent   │  │ • Performance   │                  │
│  │ • Technology    │  │   Deployment    │  │   Bottlenecks   │                  │
│  │   Lock-in       │  │ • Data          │  │ • Schema        │                  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 2. Data Modeling Patterns Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              DATA MODELING PATTERNS                            │
│                                                                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                  │
│  │   Normalized    │  │   Denormalized  │  │   Document      │                  │
│  │   Model         │  │   Model         │  │   Model         │                  │
│  │                 │  │                 │  │                 │                  │
│  │ • 3NF/BCNF      │  │ • Read          │  │ • Flexible      │                  │
│  │   Compliance    │  │   Optimized     │  │   Schema        │                  │
│  │ • Data          │  │ • Write         │  │ • JSON/BSON     │                  │
│  │   Integrity     │  │   Performance   │  │   Structure     │                  │
│  │ • Minimal       │  │ • Query         │  │ • Nested        │                  │
│  │   Redundancy    │  │   Simplicity    │  │   Documents     │                  │
│  │ • Complex       │  │ • Storage       │  │ • Schema-less   │                  │
│  │   Joins         │  │   Overhead      │  │ • Easy          │                  │
│  │ • Write         │  │ • Data          │  │   Scaling       │                  │
│  │   Performance   │  │   Consistency   │  │ • Query         │                  │
│  │ • Storage       │  │   Challenges    │  │   Flexibility   │                  │
│  │   Efficiency    │  │ • Update        │  │ • No Joins      │                  │
│  │ • ACID          │  │   Complexity    │  │ • Horizontal    │                  │
│  │   Transactions  │  │ • Data          │  │   Scaling       │                  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘                  │
│           │                       │                       │                     │
│           │                       │                       │                     │
│           ▼                       ▼                       ▼                     │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                  │
│  │   Entity-       │  │   Time-Series   │  │   Event         │                  │
│  │   Relationship  │  │   Model         │  │   Sourcing      │                  │
│  │   Model         │  │                 │  │                 │                  │
│  │                 │  │                 │  │                 │                  │
│  │ • Entity        │  │ • Time-based    │  │ • Event Store   │                  │
│  │   Definition    │  │   Partitioning  │  │ • Event         │                  │
│  │ • Relationship  │  │ • Time          │  │   Stream        │                  │
│  │   Mapping       │  │   Indexing      │  │ • State         │                  │
│  │ • Foreign Key   │  │ • Aggregation   │  │   Rebuilding    │                  │
│  │   Constraints   │  │   Functions     │  │ • Event         │                  │
│  │ • Referential   │  │ • Retention     │  │   Versioning    │                  │
│  │   Integrity     │  │   Policies      │  │ • Event         │                  │
│  │ • Cardinality   │  │ • Compression   │  │   Replay        │                  │
│  │   Rules         │  │ • Downsampling  │  │ • Audit Trail   │                  │
│  │ • Normalization │  │ • Real-time     │  │ • Temporal      │                  │
│  │   Rules         │  │   Queries       │  │   Queries       │                  │
│  │ • Schema        │  │ • Analytics     │  │ • CQRS          │                  │
│  │   Evolution     │  │   Optimization  │  │   Integration   │                  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 3. Scaling Strategy Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              SCALING STRATEGIES                                │
│                                                                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                  │
│  │   Read          │  │   Database      │  │   Horizontal    │                  │
│  │   Replicas      │  │   Partitioning  │  │   Scaling       │                  │
│  │                 │  │                 │  │                 │                  │
│  │ • Primary-      │  │ • Table         │  │ • Database      │                  │
│  │   Secondary     │  │   Partitioning  │  │   Sharding      │                  │
│  │ • Load          │  │ • Index         │  │ • Distributed   │                  │
│  │   Distribution  │  │   Partitioning  │  │   Databases     │                  │
│  │ • Read          │  │ • Data          │  │ • Consistent    │                  │
│  │   Scaling       │  │   Archiving     │  │   Hashing       │                  │
│  │ • Failover      │  │ • Partition     │  │ • Shard Key     │                  │
│  │   Support       │  │   Pruning       │  │   Strategy      │                  │
│  │ • Data          │  │ • Parallel      │  │ • Cross-Shard   │                  │
│  │   Synchronization│  │   Processing   │  │   Queries       │                  │
│  │ • Consistency   │  │ • Partition     │  │ • Shard         │                  │
│  │   Models        │  │   Maintenance   │  │   Rebalancing   │                  │
│  │ • Replication   │  │ • Partition     │  │ • Shard         │                  │
│  │   Lag           │  │   Monitoring    │  │   Monitoring    │                  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘                  │
│           │                       │                       │                     │
│           │                       │                       │                     │
│           ▼                       ▼                       ▼                     │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                  │
│  │   Vertical      │  │   Caching       │  │   Connection    │                  │
│  │   Scaling       │  │   Strategy      │  │   Pooling       │                  │
│  │                 │  │                 │  │                 │                  │
│  │ • CPU           │  │ • Application   │  │ • Connection    │                  │
│  │   Upgrades      │  │   Cache         │  │   Reuse         │                  │
│  │ • Memory        │  │ • Database      │  │ • Resource      │                  │
│  │   Upgrades      │  │   Cache         │  │   Management    │                  │
│  │ • Storage       │  │ • Query Cache   │  │ • Load          │                  │
│  │   Upgrades      │  │ • Result Cache  │  │   Distribution  │                  │
│  │ • Network       │  │ • Distributed   │  │ • Connection    │                  │
│  │   Upgrades      │  │   Cache         │  │   Monitoring    │                  │
│  │ • Hardware      │  │ • Cache         │  │ • Connection    │                  │
│  │   Optimization  │  │   Invalidation  │  │   Pooling       │                  │
│  │ • Resource      │  │ • Cache         │  │ • Connection    │                  │
│  │   Monitoring    │  │   Warming       │  │   Failover      │                  │
│  │ • Performance   │  │ • Cache         │  │ • Connection    │                  │
│  │   Tuning        │  │   Statistics    │  │   Encryption    │                  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 4. Migration Strategy Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              MIGRATION STRATEGIES                              │
│                                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐      │
│  │   Source    │    │   Migration │    │   Target    │    │   Validation │      │
│  │   Database  │    │   Engine    │    │   Database  │    │   & Testing  │      │
│  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘      │
│         │                   │                   │                   │          │
│         │ 1. Schema         │                   │                   │          │
│         │    Analysis       │                   │                   │          │
│         │──────────────────►│                   │                   │          │
│         │                   │                   │                   │          │
│         │ 2. Data           │                   │                   │          │
│         │    Extraction     │                   │                   │          │
│         │◄──────────────────│                   │                   │          │
│         │                   │                   │                   │          │
│         │ 3. Schema         │                   │                   │          │
│         │    Migration      │                   │                   │          │
│         │──────────────────────────────────────►│                   │          │
│         │                   │                   │                   │          │
│         │ 4. Data           │                   │                   │          │
│         │    Migration      │                   │                   │          │
│         │──────────────────────────────────────►│                   │          │
│         │                   │                   │                   │          │
│         │ 5. Data           │                   │                   │          │
│         │    Validation     │                   │                   │          │
│         │──────────────────────────────────────────────────────────►│          │
│         │                   │                   │                   │          │
│         │ 6. Rollback       │                   │                   │          │
│         │    (if needed)    │                   │                   │          │
│         │◄──────────────────────────────────────────────────────────│          │
│         │                   │                   │                   │          │
│                                                                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                  │
│  │   Migration     │  │   Zero-         │  │   Rollback      │                  │
│  │   Types         │  │   Downtime      │  │   Strategy      │                  │
│  │                 │  │   Migration     │  │                 │                  │
│  │                 │  │                 │  │                 │                  │
│  │ • Schema        │  │ • Blue-Green    │  │ • Point-in-time │                  │
│  │   Migration     │  │   Deployment    │  │   Recovery      │                  │
│  │ • Data          │  │ • Canary        │  │ • Backup        │                  │
│  │   Migration     │  │   Deployment    │  │   Restoration   │                  │
│  │ • Version       │  │ • Feature       │  │ • Schema        │                  │
│  │   Migration     │  │   Flags         │  │   Rollback      │                  │
│  │ • Incremental   │  │ • Database      │  │ • Data          │                  │
│  │   Migration     │  │   Mirroring     │  │   Rollback      │                  │
│  │ • Full          │  │ • Read/Write    │  │ • Application   │                  │
│  │   Migration     │  │   Splitting     │  │   Rollback      │                  │
│  │ • Partial       │  │ • Traffic       │  │ • Configuration │                  │
│  │   Migration     │  │   Routing       │  │   Rollback      │                  │
│  │ • Parallel      │  │ • Health        │  │ • Monitoring    │                  │
│  │   Migration     │  │   Checks        │  │   Rollback      │                  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 5. Backup and Recovery Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              BACKUP & RECOVERY ARCHITECTURE                    │
│                                                                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                  │
│  │   Backup        │  │   Recovery      │  │   Disaster      │                  │
│  │   Strategy      │  │   Strategy      │  │   Recovery      │                  │
│  │                 │  │                 │  │                 │                  │
│  │ • Full Backup   │  │ • Point-in-time │  │ • RTO: 4 hours  │                  │
│  │ • Incremental   │  │   Recovery      │  │ • RPO: 1 hour   │                  │
│  │   Backup        │  │ • Full          │  │ • Multi-region  │                  │
│  │ • Differential  │  │   Recovery      │  │   Backup        │                  │
│  │   Backup        │  │ • Incremental   │  │ • Cross-cloud   │                  │
│  │ • Transaction   │  │   Recovery      │  │   Backup        │                  │
│  │   Log Backup    │  │ • Selective     │  │ • Automated     │                  │
│  │ • Snapshot      │  │   Recovery      │  │   Failover      │                  │
│  │   Backup        │  │ • Schema        │  │ • Manual        │                  │
│  │ • Continuous    │  │   Recovery      │  │   Failover      │                  │
│  │   Backup        │  │ • Data          │  │ • Backup        │                  │
│  │ • Automated     │  │   Validation    │  │   Verification  │                  │
│  │   Backup        │  │ • Recovery      │  │ • Recovery      │                  │
│  │ • Backup        │  │   Testing       │  │   Testing       │                  │
│  │   Encryption    │  │ • Recovery      │  │ • Monitoring    │                  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘                  │
│           │                       │                       │                     │
│           │                       │                       │                     │
│           ▼                       ▼                       ▼                     │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                  │
│  │   Backup        │  │   Backup        │  │   Recovery      │                  │
│  │   Storage       │  │   Monitoring    │  │   Procedures    │                  │
│  │                 │  │                 │  │                 │                  │
│  │ • Local Storage │  │ • Backup        │  │ • Recovery      │                  │
│  │ • Cloud Storage │  │   Success Rate  │  │   Runbooks      │                  │
│  │ • Tape Storage  │  │ • Backup Size   │  │ • Recovery      │                  │
│  │ • Hybrid        │  │ • Backup        │  │   Checklists    │                  │
│  │   Storage       │  │   Duration      │  │ • Recovery      │                  │
│  │ • Offsite       │  │ • Backup        │  │   Scripts       │                  │
│  │   Storage       │  │   Verification  │  │ • Recovery      │                  │
│  │ • Redundant     │  │ • Backup        │  │   Automation    │                  │
│  │   Storage       │  │   Retention     │  │ • Recovery      │                  │
│  │ • Encrypted     │  │ • Backup        │  │   Validation    │                  │
│  │   Storage       │  │   Performance   │  │ • Recovery      │                  │
│  │ • Compressed    │  │ • Backup        │  │   Documentation │                  │
│  │   Storage       │  │   Alerts        │  │ • Recovery      │                  │
│  │ • Tiered        │  │ • Backup        │  │   Training      │                  │
│  │   Storage       │  │   Reporting     │  │ • Recovery      │                  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 6. Performance Optimization Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              PERFORMANCE OPTIMIZATION                          │
│                                                                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                  │
│  │   Indexing      │  │   Query         │  │   Connection    │                  │
│  │   Strategy      │  │   Optimization  │  │   Management    │                  │
│  │                 │  │                 │  │                 │                  │
│  │ • Primary       │  │ • Query         │  │ • Connection    │                  │
│  │   Indexes       │  │   Analysis      │  │   Pooling       │                  │
│  │ • Secondary     │  │ • Query         │  │ • Connection    │                  │
│  │   Indexes       │  │   Rewriting     │  │   Limits        │                  │
│  │ • Composite     │  │ • Query         │  │ • Connection    │                  │
│  │   Indexes       │  │   Hints         │  │   Timeout       │                  │
│  │ • Partial       │  │ • Query         │  │ • Connection    │                  │
│  │   Indexes       │  │   Caching       │  │   Monitoring    │                  │
│  │ • Covering      │  │ • Query         │  │ • Connection    │                  │
│  │   Indexes       │  │   Partitioning  │  │   Encryption    │                  │
│  │ • Unique        │  │ • Query         │  │ • Connection    │                  │
│  │   Indexes       │  │   Parallelization│  │   Load          │                  │
│  │ • Spatial       │  │ • Query         │  │   Balancing     │                  │
│  │   Indexes       │  │   Batching      │  │ • Connection    │                  │
│  │ • Full-text     │  │ • Query         │  │   Failover      │                  │
│  │   Indexes       │  │   Monitoring    │  │ • Connection    │                  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘                  │
│           │                       │                       │                     │
│           │                       │                       │                     │
│           ▼                       ▼                       ▼                     │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                  │
│  │   Caching       │  │   Partitioning  │  │   Monitoring    │                  │
│  │   Strategy      │  │   Strategy      │  │   & Tuning      │                  │
│  │                 │  │                 │  │                 │                  │
│  │ • Application   │  │ • Table         │  │ • Performance   │                  │
│  │   Cache         │  │   Partitioning  │  │   Monitoring    │                  │
│  │ • Database      │  │ • Index         │  │ • Query         │                  │
│  │   Cache         │  │   Partitioning  │  │   Monitoring    │                  │
│  │ • Query Cache   │  │ • Data          │  │ • Resource      │                  │
│  │ • Result Cache  │  │   Partitioning  │  │   Monitoring    │                  │
│  │ • Distributed   │  │ • Hash          │  │ • Bottleneck    │                  │
│  │   Cache         │  │   Partitioning  │  │   Detection     │                  │
│  │ • Cache         │  │ • Range         │  │ • Performance   │                  │
│  │   Invalidation  │  │   Partitioning  │  │   Tuning        │                  │
│  │ • Cache         │  │ • List          │  │ • Auto-tuning   │                  │
│  │   Warming       │  │   Partitioning  │  │ • Performance   │                  │
│  │ • Cache         │  │ • Composite     │  │   Alerts        │                  │
│  │   Statistics    │  │   Partitioning  │  │ • Performance   │                  │
│  │ • Cache         │  │ • Partition     │  │   Reporting     │                  │
│  │   Monitoring    │  │   Maintenance   │  │ • Performance   │                  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 🏗️ Database Architecture Patterns

- **Single Database**: Centralized database cho simple applications
- **Database per Service**: Separate database cho từng microservice
- **Shared Database**: Multiple services share single database
- **Read Replicas**: Separate read-only databases cho scaling
- **Database Sharding**: Horizontal partitioning across multiple databases

## 🔄 Data Modeling Patterns
- **Normalization**: Reduce data redundancy và improve integrity
- **Denormalization**: Optimize read performance cho specific use cases
- **Entity-Relationship**: Model relationships between entities
- **Document Modeling**: Flexible schema cho document databases
- **Time-Series Modeling**: Optimize cho time-based data

## 📊 Query Optimization Patterns
- **Indexing Strategy**: Proper indexes cho frequently queried fields
- **Query Optimization**: Optimize SQL queries cho performance
- **Connection Pooling**: Efficient database connection management
- **Caching Strategy**: Application và database-level caching
- **Query Partitioning**: Split large queries thành smaller chunks

## 🔒 Data Security Patterns
- **Encryption**: Encrypt data at rest và in transit
- **Access Control**: Role-based access control cho database
- **Audit Logging**: Log all database access và changes
- **Data Masking**: Mask sensitive data trong non-production environments
- **Backup Encryption**: Encrypt database backups

## 📈 Performance Patterns
- **Read/Write Splitting**: Separate read và write operations
- **Database Partitioning**: Partition large tables cho performance
- **Connection Pooling**: Reuse database connections
- **Query Caching**: Cache frequently executed queries
- **Batch Operations**: Group multiple operations cho efficiency

## 🔍 Data Migration Patterns
- **Schema Evolution**: Handle database schema changes
- **Data Migration**: Migrate data between different formats
- **Versioning**: Version database schema changes
- **Rollback Strategy**: Rollback database changes khi cần
- **Zero-Downtime Migration**: Migrate without service interruption

## 📱 Real-time Data Patterns
- **Change Data Capture**: Capture database changes in real-time
- **Event Sourcing**: Store events thay vì current state
- **CQRS**: Separate read và write models
- **Stream Processing**: Process data streams in real-time
- **Materialized Views**: Pre-computed views cho performance

## 🚀 Best Practices
- Design database schema cho scalability và performance
- Implement proper indexing strategy
- Sử dụng connection pooling cho efficient resource usage
- Regular database maintenance và optimization
- Monitor database performance và health

---

**Tài liệu này là nền tảng lý thuyết cho việc thiết kế và quản lý database trong dự án AI Camera Counting.** 