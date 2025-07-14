# Scaling Strategy Document - AI Camera Counting System

## 📊 Tổng quan

Tài liệu này cung cấp chiến lược scaling database chi tiết cho hệ thống AI Camera Counting, bao gồm horizontal scaling, vertical scaling, read replicas, sharding, và performance optimization.

## 🎯 Mục tiêu scaling

- **Horizontal Scaling**: Hỗ trợ > 1000 camera streams đồng thời
- **Vertical Scaling**: Tối ưu hiệu năng cho single instance
- **Read Scaling**: > 10,000 read operations/second
- **Write Scaling**: > 1,000 write operations/second
- **Data Growth**: Hỗ trợ > 10TB data với growth 1TB/month

## 🏗️ Scaling Architecture

### Scaling Strategy Overview

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              SCALING STRATEGY OVERVIEW                          │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              APPLICATION LAYER                              │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Load      │  │   Connection│  │   Query     │  │   Cache     │        │ │
│  │  │   Balancer  │  │   Pooling   │  │   Router    │  │   Layer     │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                             │
│                                    ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              DATABASE LAYER                                 │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Primary   │  │   Read      │  │   Analytics │  │   Archive   │        │ │
│  │  │   Database  │  │   Replicas  │  │   Database  │  │   Database  │        │ │
│  │  │             │  │             │  │             │  │             │        │ │
│  │  │ • Write     │  │ • Read      │  │ • Reports   │  │ • Historical│        │ │
│  │  │   Operations│  │   Operations│  │ • Analytics │  │   Data      │        │ │
│  │  │ • ACID      │  │ • Load      │  │ • Aggregated│  │ • Long-term │        │ │
│  │  │   Compliance│  │   Distribution│  │   Data      │  │   Storage   │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                             │
│                                    ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              SHARDING LAYER                                 │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Shard 1   │  │   Shard 2   │  │   Shard 3   │  │   Shard N   │        │ │
│  │  │             │  │             │  │             │  │             │        │ │
│  │  │ • Cameras   │  │ • Cameras   │  │ • Cameras   │  │ • Cameras   │        │ │
│  │  │   1-100     │  │   101-200   │  │   201-300   │  │   N*100+    │        │ │
│  │  │ • Events    │  │ • Events    │  │ • Events    │  │ • Events    │        │ │
│  │  │ • Results   │  │ • Results   │  │ • Results   │  │ • Results   │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Scaling Phases

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              SCALING PHASES                                     │
│                                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐      │
│  │   Phase 1   │    │   Phase 2   │    │   Phase 3   │    │   Phase 4   │      │
│  │ Foundation  │    │ Read Scaling│    │ Horizontal  │    │ Advanced    │      │
│  │             │    │             │    │ Scaling     │    │ Optimization│      │
│  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘      │
│         │                   │                   │                   │          │
│         │ • Single Database │ • Read Replicas   │ • Database Sharding│ • Multi-Region│
│         │ • Basic Indexing  │ • Load Balancing  │ • Partitioning    │ • Global     │
│         │ • Simple Queries  │ • Query Routing   │ • Data Distribution│   Distribution│
│         │ • Basic Monitoring│ • Failover Support│ • Parallel Processing│ • Geo-Replication│
│         │ • Backup Strategy │ • Health Monitoring│ • Cross-Shard Queries│ • Disaster Recovery│
│         │                   │ • Performance Tuning│ • Shard Management│ • Advanced Analytics│
│         │                   │                   │                   │          │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 📈 Vertical Scaling

### 1. Hardware Optimization

**Mục đích**: Tối ưu hóa hardware resources cho single database instance.

```sql
-- Hardware configuration recommendations
CREATE OR REPLACE FUNCTION get_hardware_recommendations()
RETURNS TABLE(component TEXT, current_value TEXT, recommended_value TEXT, priority TEXT) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        'CPU Cores'::TEXT,
        (SELECT setting FROM pg_settings WHERE name = 'max_connections')::TEXT,
        '32 cores'::TEXT,
        'high'::TEXT
    UNION ALL
    SELECT 
        'Memory (RAM)'::TEXT,
        (SELECT setting FROM pg_settings WHERE name = 'shared_buffers')::TEXT,
        '64GB'::TEXT,
        'high'::TEXT
    UNION ALL
    SELECT 
        'Storage Type'::TEXT,
        'HDD'::TEXT,
        'SSD/NVMe'::TEXT,
        'critical'::TEXT
    UNION ALL
    SELECT 
        'Storage Capacity'::TEXT,
        '1TB'::TEXT,
        '10TB'::TEXT,
        'medium'::TEXT
    UNION ALL
    SELECT 
        'Network Bandwidth'::TEXT,
        '1Gbps'::TEXT,
        '10Gbps'::TEXT,
        'high'::TEXT;
END;
$$ LANGUAGE plpgsql;
```

### 2. Database Configuration Optimization

```sql
-- Performance tuning configuration
ALTER SYSTEM SET shared_buffers = '16GB';  -- 25% of RAM
ALTER SYSTEM SET effective_cache_size = '48GB';  -- 75% of RAM
ALTER SYSTEM SET maintenance_work_mem = '2GB';
ALTER SYSTEM SET checkpoint_completion_target = 0.9;
ALTER SYSTEM SET wal_buffers = '16MB';
ALTER SYSTEM SET default_statistics_target = 100;
ALTER SYSTEM SET random_page_cost = 1.1;  -- For SSD
ALTER SYSTEM SET effective_io_concurrency = 200;  -- For SSD
ALTER SYSTEM SET work_mem = '256MB';
ALTER SYSTEM SET max_connections = 200;
ALTER SYSTEM SET max_worker_processes = 8;
ALTER SYSTEM SET max_parallel_workers_per_gather = 4;
ALTER SYSTEM SET max_parallel_workers = 8;

-- Reload configuration
SELECT pg_reload_conf();
```

### 3. Query Optimization

```sql
-- Query performance analysis
CREATE OR REPLACE FUNCTION analyze_query_performance()
RETURNS TABLE(query_pattern TEXT, avg_time NUMERIC, total_calls BIGINT, improvement_potential TEXT) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        CASE 
            WHEN query LIKE '%counting_results%' THEN 'counting_results_queries'
            WHEN query LIKE '%camera_events%' THEN 'camera_events_queries'
            WHEN query LIKE '%analytics%' THEN 'analytics_queries'
            ELSE 'other_queries'
        END::TEXT as query_pattern,
        ROUND(AVG(total_time), 2)::NUMERIC as avg_time,
        SUM(calls)::BIGINT as total_calls,
        CASE 
            WHEN AVG(total_time) > 1000 THEN 'Add indexes or optimize query'
            WHEN AVG(total_time) > 500 THEN 'Consider query optimization'
            ELSE 'Performance is good'
        END::TEXT as improvement_potential
    FROM pg_stat_statements
    WHERE calls > 10
    GROUP BY query_pattern
    ORDER BY avg_time DESC;
END;
$$ LANGUAGE plpgsql;
```

## 🔄 Horizontal Scaling

### 1. Read Replicas

**Mục đích**: Distribute read load across multiple database instances.

```sql
-- Read replica configuration
-- Primary Database (Write Operations)
-- beCamera_db_primary

-- Read Replicas (Read Operations)
-- beCamera_db_replica_1
-- beCamera_db_replica_2
-- beCamera_db_replica_3

-- Replication lag monitoring
CREATE OR REPLACE FUNCTION monitor_replication_lag()
RETURNS TABLE(replica_name TEXT, lag_seconds INTEGER, status TEXT) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        'replica_1'::TEXT as replica_name,
        EXTRACT(EPOCH FROM (NOW() - pg_last_xact_replay_timestamp()))::INTEGER as lag_seconds,
        CASE 
            WHEN pg_last_xact_replay_timestamp() IS NULL THEN 'disconnected'
            WHEN EXTRACT(EPOCH FROM (NOW() - pg_last_xact_replay_timestamp())) > 300 THEN 'lagging'
            ELSE 'healthy'
        END::TEXT as status
    UNION ALL
    SELECT 
        'replica_2'::TEXT,
        EXTRACT(EPOCH FROM (NOW() - pg_last_xact_replay_timestamp()))::INTEGER,
        CASE 
            WHEN pg_last_xact_replay_timestamp() IS NULL THEN 'disconnected'
            WHEN EXTRACT(EPOCH FROM (NOW() - pg_last_xact_replay_timestamp())) > 300 THEN 'lagging'
            ELSE 'healthy'
        END::TEXT
    UNION ALL
    SELECT 
        'replica_3'::TEXT,
        EXTRACT(EPOCH FROM (NOW() - pg_last_xact_replay_timestamp()))::INTEGER,
        CASE 
            WHEN pg_last_xact_replay_timestamp() IS NULL THEN 'disconnected'
            WHEN EXTRACT(EPOCH FROM (NOW() - pg_last_xact_replay_timestamp())) > 300 THEN 'lagging'
            ELSE 'healthy'
        END::TEXT;
END;
$$ LANGUAGE plpgsql;
```

### 2. Load Balancing Configuration

```javascript
// Load balancer configuration
const loadBalancerConfig = {
  primary: {
    host: 'primary-db.example.com',
    port: 5432,
    role: 'primary',
    weight: 0 // No read traffic
  },
  replicas: [
    {
      host: 'replica-1.example.com',
      port: 5432,
      role: 'replica',
      weight: 1,
      health_check: '/health',
      max_connections: 100
    },
    {
      host: 'replica-2.example.com',
      port: 5432,
      role: 'replica',
      weight: 1,
      health_check: '/health',
      max_connections: 100
    },
    {
      host: 'replica-3.example.com',
      port: 5432,
      role: 'replica',
      weight: 1,
      health_check: '/health',
      max_connections: 100
    }
  ],
  
  routing: {
    read_queries: ['SELECT'],
    write_queries: ['INSERT', 'UPDATE', 'DELETE', 'CREATE', 'ALTER', 'DROP'],
    analytics_queries: ['SELECT * FROM analytics'],
    failover: true,
    connection_timeout: 5000,
    query_timeout: 30000
  }
};
```

## 🔀 Database Sharding

### 1. Sharding Strategy

**Mục đích**: Distribute data across multiple database instances based on camera_id.

```sql
-- Sharding configuration
CREATE OR REPLACE FUNCTION get_shard_for_camera(camera_id INTEGER)
RETURNS INTEGER AS $$
BEGIN
    -- Hash-based sharding
    RETURN (camera_id % 4) + 1;
    
    -- Range-based sharding (alternative)
    -- RETURN CASE 
    --     WHEN camera_id BETWEEN 1 AND 100 THEN 1
    --     WHEN camera_id BETWEEN 101 AND 200 THEN 2
    --     WHEN camera_id BETWEEN 201 AND 300 THEN 3
    --     ELSE 4
    -- END;
END;
$$ LANGUAGE plpgsql;

-- Shard routing table
CREATE TABLE IF NOT EXISTS shard_routing (
    shard_id INTEGER PRIMARY KEY,
    shard_name VARCHAR(100) NOT NULL,
    host VARCHAR(100) NOT NULL,
    port INTEGER DEFAULT 5432,
    database_name VARCHAR(100) NOT NULL,
    camera_range_start INTEGER,
    camera_range_end INTEGER,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert shard configurations
INSERT INTO shard_routing (shard_id, shard_name, host, database_name, camera_range_start, camera_range_end) VALUES
(1, 'shard_1', 'shard-1.example.com', 'ai_camera_shard_1', 1, 100),
(2, 'shard_2', 'shard-2.example.com', 'ai_camera_shard_2', 101, 200),
(3, 'shard_3', 'shard-3.example.com', 'ai_camera_shard_3', 201, 300),
(4, 'shard_4', 'shard-4.example.com', 'ai_camera_shard_4', 301, 400);
```

### 2. Cross-Shard Queries

```sql
-- Cross-shard query function
CREATE OR REPLACE FUNCTION execute_cross_shard_query(query_template TEXT, params JSONB)
RETURNS TABLE(shard_id INTEGER, result_count INTEGER, execution_time NUMERIC) AS $$
DECLARE
    shard_record RECORD;
    start_time TIMESTAMP;
    end_time TIMESTAMP;
    result_count INTEGER;
BEGIN
    FOR shard_record IN
        SELECT * FROM shard_routing WHERE is_active = TRUE
    LOOP
        start_time := NOW();
        
        -- Execute query on each shard
        EXECUTE format('SELECT COUNT(*) FROM %I.%I WHERE %s', 
                      shard_record.database_name, 
                      'counting_results', 
                      query_template)
        INTO result_count
        USING params;
        
        end_time := NOW();
        
        RETURN QUERY
        SELECT 
            shard_record.shard_id,
            result_count,
            EXTRACT(EPOCH FROM (end_time - start_time))::NUMERIC;
    END LOOP;
END;
$$ LANGUAGE plpgsql;
```

### 3. Shard Management

```sql
-- Shard health monitoring
CREATE OR REPLACE FUNCTION monitor_shard_health()
RETURNS TABLE(shard_id INTEGER, shard_name TEXT, status TEXT, record_count BIGINT, last_update TIMESTAMP) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        sr.shard_id,
        sr.shard_name,
        CASE 
            WHEN sr.is_active THEN 'healthy'
            ELSE 'inactive'
        END::TEXT as status,
        COALESCE(stats.record_count, 0)::BIGINT,
        COALESCE(stats.last_update, NOW()) as last_update
    FROM shard_routing sr
    LEFT JOIN (
        SELECT 
            get_shard_for_camera(camera_id) as shard_id,
            COUNT(*) as record_count,
            MAX(created_at) as last_update
        FROM counting_results
        GROUP BY get_shard_for_camera(camera_id)
    ) stats ON sr.shard_id = stats.shard_id
    ORDER BY sr.shard_id;
END;
$$ LANGUAGE plpgsql;
```

## 📊 Data Partitioning

### 1. Time-based Partitioning

```sql
-- Time-based partitioning for counting_results
CREATE TABLE counting_results (
    id SERIAL,
    camera_id INTEGER NOT NULL,
    zone_id INTEGER NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    count_in INTEGER DEFAULT 0,
    count_out INTEGER DEFAULT 0,
    total_count INTEGER DEFAULT 0,
    confidence DECIMAL(5,4),
    frame_data JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) PARTITION BY RANGE (timestamp);

-- Monthly partitions
CREATE TABLE counting_results_y2024m01 
PARTITION OF counting_results
FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

CREATE TABLE counting_results_y2024m02 
PARTITION OF counting_results
FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');

-- Auto-create partitions function
CREATE OR REPLACE FUNCTION create_monthly_partition(table_name TEXT, start_date date)
RETURNS void AS $$
DECLARE
    partition_name text;
    end_date date;
BEGIN
    partition_name := table_name || '_y' || to_char(start_date, 'YYYY') || 'm' || to_char(start_date, 'MM');
    end_date := start_date + INTERVAL '1 month';
    
    EXECUTE format('CREATE TABLE IF NOT EXISTS %I PARTITION OF %I FOR VALUES FROM (%L) TO (%L)',
                   partition_name, table_name, start_date, end_date);
    
    -- Create indexes on new partition
    EXECUTE format('CREATE INDEX IF NOT EXISTS %I ON %I (camera_id, timestamp)',
                   partition_name || '_idx_camera_timestamp', partition_name);
    
    -- Log partition creation
    INSERT INTO partition_log (
        table_name,
        partition_name,
        start_date,
        end_date,
        created_at
    ) VALUES (
        table_name,
        partition_name,
        start_date,
        end_date,
        NOW()
    );
END;
$$ LANGUAGE plpgsql;
```

### 2. Hash Partitioning

```sql
-- Hash partitioning for camera_events
CREATE TABLE camera_events (
    id SERIAL,
    camera_id INTEGER NOT NULL,
    event_type event_type NOT NULL,
    severity event_severity DEFAULT 'info',
    message TEXT,
    data JSONB DEFAULT '{}',
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) PARTITION BY HASH (camera_id);

-- Hash partitions
CREATE TABLE camera_events_p0 PARTITION OF camera_events FOR VALUES WITH (modulus 4, remainder 0);
CREATE TABLE camera_events_p1 PARTITION OF camera_events FOR VALUES WITH (modulus 4, remainder 1);
CREATE TABLE camera_events_p2 PARTITION OF camera_events FOR VALUES WITH (modulus 4, remainder 2);
CREATE TABLE camera_events_p3 PARTITION OF camera_events FOR VALUES WITH (modulus 4, remainder 3);
```

## 🔧 Connection Pooling

### 1. Advanced Connection Pooling

```javascript
// Advanced connection pool configuration
const advancedPoolConfig = {
  primary: {
    host: process.env.DB_PRIMARY_HOST,
    port: process.env.DB_PRIMARY_PORT,
    database: process.env.DB_NAME,
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    
    // Connection pool settings
    max: 50,
    min: 10,
    idle: 30000,
    acquire: 60000,
    evict: 60000,
    
    // SSL configuration
    ssl: {
      rejectUnauthorized: false
    },
    
    // Application name for monitoring
    application_name: 'ai-camera-primary-pool'
  },
  
  replicas: [
    {
      host: process.env.DB_REPLICA_1_HOST,
      port: process.env.DB_REPLICA_1_PORT,
      database: process.env.DB_NAME,
      user: process.env.DB_READONLY_USER,
      password: process.env.DB_READONLY_PASSWORD,
      
      // Read-only pool settings
      max: 30,
      min: 5,
      idle: 30000,
      acquire: 60000,
      evict: 60000,
      
      // Load balancing weight
      weight: 1,
      
      application_name: 'ai-camera-replica-1-pool'
    },
    {
      host: process.env.DB_REPLICA_2_HOST,
      port: process.env.DB_REPLICA_2_PORT,
      database: process.env.DB_NAME,
      user: process.env.DB_READONLY_USER,
      password: process.env.DB_READONLY_PASSWORD,
      
      max: 30,
      min: 5,
      idle: 30000,
      acquire: 60000,
      evict: 60000,
      
      weight: 1,
      
      application_name: 'ai-camera-replica-2-pool'
    }
  ],
  
  // Pool management
  management: {
    health_check_interval: 30000,
    max_retries: 3,
    retry_delay: 1000,
    circuit_breaker: {
      failure_threshold: 5,
      recovery_timeout: 60000
    }
  }
};
```

### 2. Connection Pool Monitoring

```sql
-- Connection pool monitoring
CREATE OR REPLACE FUNCTION monitor_connection_pools()
RETURNS TABLE(pool_name TEXT, total_connections INTEGER, active_connections INTEGER, idle_connections INTEGER, waiting_connections INTEGER) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        'primary_pool'::TEXT as pool_name,
        COUNT(*)::INTEGER as total_connections,
        COUNT(*) FILTER (WHERE state = 'active')::INTEGER as active_connections,
        COUNT(*) FILTER (WHERE state = 'idle')::INTEGER as idle_connections,
        COUNT(*) FILTER (WHERE state = 'waiting')::INTEGER as waiting_connections
    FROM pg_stat_activity
    WHERE application_name = 'ai-camera-primary-pool'
    UNION ALL
    SELECT 
        'replica_pool'::TEXT,
        COUNT(*)::INTEGER,
        COUNT(*) FILTER (WHERE state = 'active')::INTEGER,
        COUNT(*) FILTER (WHERE state = 'idle')::INTEGER,
        COUNT(*) FILTER (WHERE state = 'waiting')::INTEGER
    FROM pg_stat_activity
    WHERE application_name LIKE 'ai-camera-replica-%';
END;
$$ LANGUAGE plpgsql;
```

## 📈 Performance Monitoring

### 1. Scaling Metrics

```sql
-- Scaling performance metrics
CREATE OR REPLACE FUNCTION get_scaling_metrics()
RETURNS TABLE(metric_name TEXT, current_value NUMERIC, target_value NUMERIC, status TEXT) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        'read_operations_per_second'::TEXT,
        (SELECT COUNT(*) FROM pg_stat_statements WHERE query LIKE 'SELECT%')::NUMERIC,
        10000.0::NUMERIC,
        CASE 
            WHEN (SELECT COUNT(*) FROM pg_stat_statements WHERE query LIKE 'SELECT%') > 10000 THEN 'scaling_needed'
            ELSE 'within_limits'
        END::TEXT
    UNION ALL
    SELECT 
        'write_operations_per_second'::TEXT,
        (SELECT COUNT(*) FROM pg_stat_statements WHERE query LIKE 'INSERT%' OR query LIKE 'UPDATE%' OR query LIKE 'DELETE%')::NUMERIC,
        1000.0::NUMERIC,
        CASE 
            WHEN (SELECT COUNT(*) FROM pg_stat_statements WHERE query LIKE 'INSERT%' OR query LIKE 'UPDATE%' OR query LIKE 'DELETE%') > 1000 THEN 'scaling_needed'
            ELSE 'within_limits'
        END::TEXT
    UNION ALL
    SELECT 
        'active_connections'::TEXT,
        COUNT(*)::NUMERIC,
        200.0::NUMERIC,
        CASE 
            WHEN COUNT(*) > 200 THEN 'scaling_needed'
            ELSE 'within_limits'
        END::TEXT
    FROM pg_stat_activity
    WHERE state = 'active';
END;
$$ LANGUAGE plpgsql;
```

### 2. Auto-scaling Triggers

```sql
-- Auto-scaling trigger function
CREATE OR REPLACE FUNCTION check_scaling_triggers()
RETURNS void AS $$
DECLARE
    current_load NUMERIC;
    max_load NUMERIC;
    scaling_action TEXT;
BEGIN
    -- Check current load
    SELECT AVG(total_time) INTO current_load
    FROM pg_stat_statements
    WHERE calls > 10;
    
    -- Get max acceptable load
    max_load := 1000; -- 1 second average query time
    
    -- Determine scaling action
    IF current_load > max_load THEN
        scaling_action := 'scale_up';
        
        -- Log scaling trigger
        INSERT INTO scaling_log (
            trigger_type,
            current_value,
            threshold_value,
            action,
            created_at
        ) VALUES (
            'performance',
            current_load,
            max_load,
            scaling_action,
            NOW()
        );
        
        -- Send alert
        INSERT INTO alerts (
            alert_type,
            severity,
            title,
            message
        ) VALUES (
            'scaling_trigger',
            'medium',
            'Database Scaling Required',
            'Current load (' || current_load || ') exceeds threshold (' || max_load || ')'
        );
    END IF;
END;
$$ LANGUAGE plpgsql;
```

## 🚀 Implementation Roadmap

### 1. Phase 1: Foundation (Months 1-2)

```sql
-- Phase 1 implementation checklist
CREATE TABLE IF NOT EXISTS scaling_implementation (
    phase INTEGER PRIMARY KEY,
    phase_name VARCHAR(100) NOT NULL,
    description TEXT,
    tasks TEXT[],
    estimated_duration INTERVAL,
    dependencies INTEGER[],
    status implementation_status DEFAULT 'pending',
    started_at TIMESTAMP,
    completed_at TIMESTAMP
);

-- Implementation status enum
DO $$ BEGIN
    CREATE TYPE implementation_status AS ENUM ('pending', 'in_progress', 'completed', 'blocked');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- Insert Phase 1 tasks
INSERT INTO scaling_implementation (
    phase,
    phase_name,
    description,
    tasks,
    estimated_duration,
    dependencies
) VALUES (
    1,
    'Foundation',
    'Basic database optimization and monitoring setup',
    ARRAY[
        'Optimize database configuration',
        'Implement basic indexing strategy',
        'Set up monitoring and alerting',
        'Create backup and recovery procedures',
        'Performance baseline establishment'
    ],
    INTERVAL '2 months',
    ARRAY[]::INTEGER[]
);
```

### 2. Phase 2: Read Scaling (Months 3-4)

```sql
-- Insert Phase 2 tasks
INSERT INTO scaling_implementation (
    phase,
    phase_name,
    description,
    tasks,
    estimated_duration,
    dependencies
) VALUES (
    2,
    'Read Scaling',
    'Implement read replicas and load balancing',
    ARRAY[
        'Set up read replicas',
        'Configure replication',
        'Implement load balancing',
        'Add failover mechanisms',
        'Monitor replication lag'
    ],
    INTERVAL '2 months',
    ARRAY[1]
);
```

### 3. Phase 3: Horizontal Scaling (Months 5-7)

```sql
-- Insert Phase 3 tasks
INSERT INTO scaling_implementation (
    phase,
    phase_name,
    description,
    tasks,
    estimated_duration,
    dependencies
) VALUES (
    3,
    'Horizontal Scaling',
    'Implement database sharding and partitioning',
    ARRAY[
        'Design sharding strategy',
        'Implement database sharding',
        'Set up cross-shard queries',
        'Add data partitioning',
        'Implement shard management'
    ],
    INTERVAL '3 months',
    ARRAY[2]
);
```

### 4. Phase 4: Advanced Optimization (Months 8-10)

```sql
-- Insert Phase 4 tasks
INSERT INTO scaling_implementation (
    phase,
    phase_name,
    description,
    tasks,
    estimated_duration,
    dependencies
) VALUES (
    4,
    'Advanced Optimization',
    'Multi-region deployment and advanced features',
    ARRAY[
        'Implement multi-region deployment',
        'Add geo-replication',
        'Advanced caching strategies',
        'Performance optimization',
        'Disaster recovery setup'
    ],
    INTERVAL '3 months',
    ARRAY[3]
);
```

---

**Tài liệu này cung cấp chiến lược scaling database chi tiết cho AI Camera Counting System, bao gồm horizontal scaling, vertical scaling, read replicas, sharding, và performance optimization.** 