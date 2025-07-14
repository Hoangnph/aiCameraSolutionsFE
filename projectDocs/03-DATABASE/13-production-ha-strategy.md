# Production High Availability Strategy - AI Camera Counting System

## 📊 Tổng quan

Tài liệu này trình bày chiến lược High Availability (HA) và Disaster Recovery (DR) cho hệ thống AI Camera Counting trong môi trường production, đảm bảo 99.99% uptime và khả năng phục hồi nhanh chóng khi có sự cố.

## 🎯 Mục tiêu HA/DR

- **Uptime**: 99.99% (4.32 phút downtime/tháng)
- **RTO (Recovery Time Objective)**: < 15 phút
- **RPO (Recovery Point Objective)**: < 5 phút
- **Geographic Distribution**: Multi-region deployment
- **Data Consistency**: Strong consistency với eventual consistency cho analytics

## 🏗️ High Availability Architecture

### Multi-Region HA Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              MULTI-REGION HA ARCHITECTURE                       │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              PRIMARY REGION (US-EAST-1)                     │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Load      │  │   Primary   │  │   Cache     │  │   Queue     │        │ │
│  │  │   Balancer  │  │   Database  │  │   Cluster   │  │   Cluster   │        │ │
│  │  │   (ALB)     │  │ (PostgreSQL)│  │   (Redis)   │  │ (RabbitMQ)  │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  │         │                   │                   │                   │        │ │
│  │         │                   │                   │                   │        │ │
│  │         ▼                   ▼                   ▼                   ▼        │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Auto      │  │   Read      │  │   Cache     │  │   Queue     │        │ │
│  │  │   Scaling   │  │   Replicas  │  │   Sentinel  │  │   Mirroring │        │ │
│  │  │   Group     │  │   (3x)      │  │   (3x)      │  │   (2x)      │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                             │
│                                    │ Cross-Region Replication                    │
│                                    │ (Synchronous + Asynchronous)               │
│                                    │                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              SECONDARY REGION (US-WEST-2)                   │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Standby   │  │   Standby   │  │   Cache     │  │   Queue     │        │ │
│  │  │   Load      │  │   Database  │  │   Replica   │  │   Replica   │        │ │
│  │  │   Balancer  │  │ (PostgreSQL)│  │   (Redis)   │  │ (RabbitMQ)  │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  │         │                   │                   │                   │        │ │
│  │         │                   │                   │                   │        │ │
│  │         ▼                   ▼                   ▼                   ▼        │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Warm      │  │   Read      │  │   Cache     │  │   Queue     │        │ │
│  │  │   Standby   │  │   Replicas  │  │   Sentinel  │  │   Mirroring │        │ │
│  │  │   Services  │  │   (2x)      │  │   (2x)      │  │   (1x)      │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              DISASTER RECOVERY REGION (EU-WEST-1)           │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Cold      │  │   Backup    │  │   Archive   │  │   Log       │        │ │
│  │  │   Standby   │  │   Storage   │  │   Storage   │  │   Storage   │        │ │
│  │  │   Services  │  │   (S3)      │  │   (Glacier) │  │   (S3)      │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Database HA Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              DATABASE HIGH AVAILABILITY                         │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              PRIMARY DATABASE CLUSTER                       │ │
│  │                                                                             │ │
│  │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │ │
│  │  │   Primary   │    │   Standby   │    │   Standby   │    │   Standby   │  │ │
│  │  │   Master    │    │   Replica   │    │   Replica   │    │   Replica   │  │ │
│  │  │ (PostgreSQL)│    │ (PostgreSQL)│    │ (PostgreSQL)│    │ (PostgreSQL)│  │ │
│  │  │             │    │             │    │             │    │             │  │ │
│  │  │ • Write     │    │ • Read      │    │ • Read      │    │ • Read      │  │ │
│  │  │ • WAL       │    │ • Analytics │    │ • Reporting │    │ • Backup    │  │ │
│  │  │ • Sync      │    │ • Sync      │    │ • Async     │    │ • Async     │  │ │
│  │  │ • Failover  │    │ • Failover  │    │ • Failover  │    │ • Failover  │  │ │
│  │  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘  │ │
│  │         │                   │                   │                   │      │ │
│  │         │                   │                   │                   │      │ │
│  │         ▼                   ▼                   ▼                   ▼      │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   WAL       │  │   Health    │  │   Load      │  │   Backup    │        │ │
│  │  │   Shipping  │  │   Monitor   │  │   Balancer  │  │   Manager   │        │ │
│  │  │   (Sync)    │  │   (pgpool)  │  │   (pgpool)  │  │   (pg_basebackup)│   │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                             │
│                                    │ Cross-Region Replication                   │
│                                    │ (Asynchronous WAL Shipping)               │
│                                    │                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              STANDBY DATABASE CLUSTER                       │ │
│  │                                                                             │ │
│  │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │ │
│  │  │   Standby   │    │   Standby   │    │   Standby   │    │   Standby   │  │ │
│  │  │   Master    │    │   Replica   │    │   Replica   │    │   Replica   │  │ │
│  │  │ (PostgreSQL)│    │ (PostgreSQL)│    │ (PostgreSQL)│    │ (PostgreSQL)│  │ │
│  │  │             │    │             │    │             │    │             │  │ │
│  │  │ • Read      │    │ • Read      │    │ • Read      │    │ • Read      │  │ │
│  │  │ • WAL       │    │ • Analytics │    │ • Reporting │    │ • Backup    │  │ │
│  │  │ • Sync      │    │ • Sync      │    │ • Async     │    │ • Async     │  │ │
│  │  │ • Failover  │    │ • Failover  │    │ • Failover  │    │ • Failover  │  │ │
│  │  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘  │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Cache HA Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              CACHE HIGH AVAILABILITY                           │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              REDIS SENTINEL CLUSTER                         │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Sentinel  │  │   Sentinel  │  │   Sentinel  │  │   Sentinel  │        │ │
│  │  │   Node 1    │  │   Node 2    │  │   Node 3    │  │   Node 4    │        │ │
│  │  │             │  │             │  │             │  │             │        │ │
│  │  │ • Monitor   │  │ • Monitor   │  │ • Monitor   │  │ • Monitor   │        │ │
│  │  │ • Failover  │  │ • Failover  │  │ • Failover  │  │ • Failover  │        │ │
│  │  │ • Config    │  │ • Config    │  │ • Config    │  │ • Config    │        │ │
│  │  │ • Quorum    │  │ • Quorum    │  │ • Quorum    │  │ • Quorum    │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  │         │                   │                   │                   │        │ │
│  │         │                   │                   │                   │        │ │
│  │         ▼                   ▼                   ▼                   ▼        │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Master    │  │   Slave 1   │  │   Slave 2   │  │   Slave 3   │        │ │
│  │  │   Redis     │  │   Redis     │  │   Redis     │  │   Redis     │        │ │
│  │  │             │  │             │  │             │  │             │        │ │
│  │  │ • Write     │  │ • Read      │  │ • Read      │  │ • Read      │        │ │
│  │  │ • Replication│  │ • Replication│  │ • Replication│  │ • Replication│        │ │
│  │  │ • Persistence│  │ • Persistence│  │ • Persistence│  │ • Persistence│        │ │
│  │  │ • Failover  │  │ • Failover  │  │ • Failover  │  │ • Failover  │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                             │
│                                    │ Cross-Region Replication                   │
│                                    │ (Redis Cluster)                            │ │
│                                    │                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              STANDBY REDIS CLUSTER                          │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Sentinel  │  │   Sentinel  │  │   Sentinel  │  │   Sentinel  │        │ │
│  │  │   Node 1    │  │   Node 2    │  │   Node 3    │  │   Node 4    │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  │         │                   │                   │                   │        │ │
│  │         ▼                   ▼                   ▼                   ▼        │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Standby   │  │   Standby   │  │   Standby   │  │   Standby   │        │ │
│  │  │   Master    │  │   Slave 1   │  │   Slave 2   │  │   Slave 3   │        │ │
│  │  │   Redis     │  │   Redis     │  │   Redis     │  │   Redis     │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 🔄 Failover Strategy

### Database Failover Process

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              DATABASE FAILOVER PROCESS                          │
│                                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐      │
│  │   Primary   │    │   Health    │    │   Standby   │    │   Load      │      │
│  │   Database  │    │   Monitor   │    │   Database  │    │   Balancer  │      │
│  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘      │
│         │                   │                   │                   │          │
│         │ 1. Primary        │                   │                   │          │
│         │    Failure        │                   │                   │          │
│         │──────────────────►│                   │                   │          │
│         │                   │                   │                   │          │
│         │                   │ 2. Health Check   │                   │          │
│         │                   │    Failed         │                   │          │
│         │                   │──────────────────►│                   │          │
│         │                   │                   │                   │          │
│         │                   │                   │ 3. Promote        │          │
│         │                   │                   │    Standby        │          │
│         │                   │                   │──────────────────►│          │
│         │                   │                   │                   │          │
│         │                   │                   │ 4. Update DNS     │          │
│         │                   │                   │    & Config       │          │
│         │                   │                   │──────────────────►│          │
│         │                   │                   │                   │          │
│         │                   │                   │ 5. Route Traffic  │          │
│         │                   │                   │    to New Primary │          │
│         │                   │                   │◄──────────────────┤          │
│         │                   │                   │                   │          │
│         │                   │ 6. Notify         │                   │          │
│         │                   │    Operations     │                   │          │
│         │                   │◄──────────────────┤                   │          │
│         │                   │                   │                   │          │
│         │ 7. Alert          │                   │                   │          │
│         │    Sent           │                   │                   │          │
│         │◄──────────────────┤                   │                   │          │
│         │                   │                   │                   │          │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Cache Failover Process

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              CACHE FAILOVER PROCESS                             │
│                                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐      │
│  │   Redis     │    │   Sentinel  │    │   Slave     │    │   Application│      │
│  │   Master    │    │   Cluster   │    │   Redis     │    │   Layer      │      │
│  │  └────────────┘    └────────────┘    └────────────┘    └────────────┘      │
│         │                   │                   │                   │          │
│         │ 1. Master         │                   │                   │          │
│         │    Failure        │                   │                   │          │
│         │──────────────────►│                   │                   │          │
│         │                   │                   │                   │          │
│         │                   │ 2. Sentinel       │                   │          │
│         │                   │    Detection      │                   │          │
│         │                   │──────────────────►│                   │          │
│         │                   │                   │                   │          │
│         │                   │                   │ 3. Promote        │          │
│         │                   │                   │    Slave          │          │
│         │                   │──────────────────►│                   │          │
│         │                   │                   │                   │          │
│         │                   │ 4. Update         │                   │          │
│         │                   │    Configuration  │                   │          │
│         │                   │──────────────────►│                   │          │
│         │                   │                   │                   │          │
│         │                   │                   │ 5. Reconnect      │          │
│         │                   │                   │    Applications   │          │
│         │                   │                   │◄──────────────────┤          │
│         │                   │                   │                   │          │
│         │                   │ 6. Cache          │                   │          │
│         │                   │    Warming        │                   │          │
│         │                   │◄──────────────────┤                   │          │
│         │                   │                   │                   │          │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 📊 RTO/RPO Requirements

### Recovery Objectives by Service

| Service | RTO | RPO | Strategy |
|---------|-----|-----|----------|
| **Database** | 5 phút | 1 phút | Synchronous replication + WAL shipping |
| **Cache** | 2 phút | 0 phút | Redis Sentinel + AOF persistence |
| **Queue** | 3 phút | 0 phút | RabbitMQ mirroring + persistent messages |
| **Application** | 10 phút | 5 phút | Auto-scaling + health checks |
| **Storage** | 15 phút | 5 phút | Cross-region replication + S3 |

### Geographic Distribution

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              GEOGRAPHIC DISTRIBUTION                            │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              NORTH AMERICA                                  │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   US-East-1 │  │   US-West-2 │  │   US-Central│  │   Canada    │        │ │
│  │  │   (Primary) │  │   (Secondary)│  │   (Tertiary)│  │   (DR)      │        │ │
│  │  │             │  │             │  │             │  │             │        │ │
│  │  │ • 99.99%    │  │ • 99.95%    │  │ • 99.9%     │  │ • 99.5%     │        │ │
│  │  │ • < 50ms    │  │ • < 100ms   │  │ • < 150ms   │  │ • < 200ms   │        │ │
│  │  │ • Sync      │  │ • Async     │  │ • Async     │  │ • Backup    │        │ │
│  │  │ • Active    │  │ • Standby   │  │ • Standby   │  │ • Cold      │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                             │
│                                    │ Global Load Balancer                        │
│                                    │ (Route 53 + CloudFront)                    │
│                                    │                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              EUROPE                                          │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   EU-West-1 │  │   EU-Central│  │   EU-North  │  │   UK        │        │ │
│  │  │   (Primary) │  │   (Secondary)│  │   (Tertiary)│  │   (DR)      │        │ │
│  │  │             │  │             │  │             │  │             │        │ │
│  │  │ • 99.99%    │  │ • 99.95%    │  │ • 99.9%     │  │ • 99.5%     │        │ │
│  │  │ • < 50ms    │  │ • < 100ms   │  │ • < 150ms   │  │ • < 200ms   │        │ │
│  │  │ • Sync      │  │ • Async     │  │ • Async     │  │ • Backup    │        │ │
│  │  │ • Active    │  │ • Standby   │  │ • Standby   │  │ • Cold      │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                             │
│                                    │ Cross-Region Replication                   │
│                                    │ (Asynchronous)                             │ │
│                                    │                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              ASIA PACIFIC                                   │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   AP-South-1│  │   AP-East-1 │  │   AP-Northeast│  │   Australia │        │ │
│  │  │   (Primary) │  │   (Secondary)│  │   (Tertiary)│  │   (DR)      │        │ │
│  │  │             │  │             │  │             │  │             │        │ │
│  │  │ • 99.99%    │  │ • 99.95%    │  │ • 99.9%     │  │ • 99.5%     │        │ │
│  │  │ • < 50ms    │  │ • < 100ms   │  │ • < 150ms   │  │ • < 200ms   │        │ │
│  │  │ • Sync      │  │ • Async     │  │ • Async     │  │ • Backup    │        │ │
│  │  │ • Active    │  │ • Standby   │  │ • Standby   │  │ • Cold      │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 🔧 Implementation Guidelines

### Database HA Implementation

#### PostgreSQL Configuration
```sql
-- Primary Database Configuration
max_connections = 200
shared_buffers = 4GB
effective_cache_size = 12GB
wal_level = replica
max_wal_senders = 10
max_replication_slots = 10
hot_standby = on
wal_keep_segments = 64
archive_mode = on
archive_command = 'aws s3 cp %p s3://backup-bucket/wal/%f'

-- Standby Database Configuration
hot_standby = on
max_standby_streaming_delay = 30s
max_standby_archive_delay = 30s
wal_receiver_status_interval = 10s
hot_standby_feedback = on
```

#### Replication Setup
```bash
# Primary Database
pg_basebackup -h primary-host -D /var/lib/postgresql/standby -U replicator -v -P -W

# Standby Database
echo "standby_mode = 'on'" >> postgresql.conf
echo "primary_conninfo = 'host=primary-host port=5432 user=replicator password=password'" >> postgresql.conf
echo "restore_command = 'aws s3 cp s3://backup-bucket/wal/%f %p'" >> postgresql.conf
```

### Cache HA Implementation

#### Redis Sentinel Configuration
```conf
# sentinel.conf
port 26379
sentinel monitor mymaster primary-redis 6379 2
sentinel down-after-milliseconds mymaster 5000
sentinel parallel-syncs mymaster 1
sentinel failover-timeout mymaster 10000
sentinel auth-pass mymaster password
```

#### Redis Cluster Configuration
```conf
# redis.conf
cluster-enabled yes
cluster-config-file nodes.conf
cluster-node-timeout 5000
appendonly yes
appendfsync everysec
save 900 1
save 300 10
save 60 10000
```

### Queue HA Implementation

#### RabbitMQ Mirroring
```bash
# Enable mirroring
rabbitmqctl set_policy ha-all "^" '{"ha-mode":"all","ha-sync-mode":"automatic"}'

# Configure cluster
rabbitmqctl join_cluster rabbit@node1
rabbitmqctl start_app
```

## 📈 Monitoring & Alerting

### HA Health Monitoring

#### Database Monitoring
- **Primary/Standby Status**: Continuous monitoring of replication lag
- **Connection Pool**: Monitor connection usage and availability
- **Query Performance**: Track slow queries and performance degradation
- **Disk Space**: Monitor storage usage and growth trends
- **Backup Status**: Verify backup completion and restore testing

#### Cache Monitoring
- **Sentinel Status**: Monitor sentinel cluster health
- **Master/Slave Status**: Track replication status and lag
- **Memory Usage**: Monitor Redis memory consumption
- **Hit/Miss Ratio**: Track cache performance metrics
- **Connection Count**: Monitor client connections

#### Queue Monitoring
- **Queue Depth**: Monitor message queue lengths
- **Consumer Status**: Track consumer health and performance
- **Message Throughput**: Monitor message processing rates
- **Error Rates**: Track failed message processing
- **Cluster Health**: Monitor RabbitMQ cluster status

### Alert Thresholds

| Metric | Warning | Critical | Action |
|--------|---------|----------|--------|
| **Replication Lag** | > 30s | > 60s | Check network, promote standby |
| **Cache Hit Ratio** | < 80% | < 60% | Scale cache, optimize queries |
| **Queue Depth** | > 1000 | > 5000 | Scale consumers, check processing |
| **Response Time** | > 200ms | > 500ms | Check performance, scale resources |
| **Error Rate** | > 1% | > 5% | Investigate errors, rollback if needed |

## 🚨 Disaster Recovery Procedures

### Automated Failover

#### Database Failover
1. **Detection**: Health check fails for primary database
2. **Verification**: Confirm failure with multiple health checks
3. **Promotion**: Automatically promote standby to primary
4. **DNS Update**: Update DNS records to point to new primary
5. **Application Update**: Update application configuration
6. **Monitoring**: Verify all services are healthy
7. **Notification**: Alert operations team

#### Cache Failover
1. **Detection**: Sentinel detects master failure
2. **Election**: Sentinel cluster elects new master
3. **Promotion**: Promote slave to master
4. **Reconfiguration**: Update client configurations
5. **Cache Warming**: Warm up cache with frequently accessed data
6. **Verification**: Confirm cache is serving requests
7. **Notification**: Alert operations team

### Manual Recovery Procedures

#### Complete Region Failure
1. **Assessment**: Evaluate scope and impact of failure
2. **Communication**: Notify stakeholders and customers
3. **Failover**: Manually initiate failover to secondary region
4. **Verification**: Confirm all services are operational
5. **Monitoring**: Closely monitor system health
6. **Recovery**: Plan and execute primary region recovery
7. **Failback**: Return to primary region when safe

#### Data Corruption Recovery
1. **Isolation**: Isolate affected systems
2. **Assessment**: Determine scope of corruption
3. **Backup Verification**: Verify backup integrity
4. **Point-in-Time Recovery**: Restore to last known good state
5. **Data Validation**: Verify data integrity
6. **Service Restoration**: Gradually restore services
7. **Post-Mortem**: Document lessons learned

## 📋 Testing & Validation

### HA Testing Schedule

| Test Type | Frequency | Description |
|-----------|-----------|-------------|
| **Failover Test** | Monthly | Simulate primary failure and verify failover |
| **Performance Test** | Weekly | Test system performance under load |
| **Recovery Test** | Quarterly | Test complete disaster recovery procedures |
| **Backup Test** | Monthly | Verify backup integrity and restore capability |
| **Load Test** | Bi-weekly | Test system behavior under high load |

### Test Scenarios

#### Database Failover Test
```bash
# Simulate primary database failure
sudo systemctl stop postgresql@primary

# Verify automatic failover
curl -f http://health-check-endpoint

# Verify data consistency
psql -h standby-host -c "SELECT COUNT(*) FROM counting_results;"

# Restore primary and verify failback
sudo systemctl start postgresql@primary
```

#### Cache Failover Test
```bash
# Simulate Redis master failure
redis-cli -h master-redis DEBUG SEGFAULT

# Verify sentinel failover
redis-cli -p 26379 sentinel master mymaster

# Verify application connectivity
curl -f http://cache-health-endpoint

# Restore master and verify failback
redis-server /etc/redis/redis.conf
```

## 🔒 Security Considerations

### HA Security Measures

#### Network Security
- **VPC Isolation**: Separate VPCs for primary and standby regions
- **Security Groups**: Restrict access to database and cache ports
- **VPN Tunnels**: Encrypted communication between regions
- **DDoS Protection**: CloudFront and WAF protection

#### Data Security
- **Encryption at Rest**: All data encrypted using AES-256
- **Encryption in Transit**: TLS 1.3 for all communications
- **Key Management**: AWS KMS for encryption key management
- **Access Control**: IAM roles and policies for access control

#### Monitoring Security
- **Audit Logging**: Comprehensive audit trails for all operations
- **Access Monitoring**: Monitor all database and cache access
- **Anomaly Detection**: Detect unusual access patterns
- **Incident Response**: Automated incident response procedures

---

**Tài liệu này cung cấp framework hoàn chỉnh cho High Availability và Disaster Recovery trong môi trường production, đảm bảo 99.99% uptime và khả năng phục hồi nhanh chóng.** 