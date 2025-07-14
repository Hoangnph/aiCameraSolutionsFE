# Production Performance Tuning - AI Camera Counting System

## 📊 Tổng quan

Tài liệu này trình bày chiến lược tối ưu hiệu suất database cho hệ thống AI Camera Counting trong môi trường production, bao gồm query optimization, indexing, caching và monitoring.

## 🎯 Performance Objectives

- **Response Time**: < 100ms cho 95% queries
- **Throughput**: > 10,000 queries/second
- **Concurrency**: Hỗ trợ > 1,000 concurrent connections
- **Availability**: 99.99% uptime
- **Scalability**: Linear scaling với workload tăng

## 🏗️ Performance Architecture

### Multi-Tier Performance Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              PERFORMANCE ARCHITECTURE                           │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              APPLICATION TIER                               │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Query     │  │   Connection│  │   Statement │  │   Result     │        │ │
│  │  │   Cache     │  │   Pooling   │  │   Cache     │  │   Cache      │        │ │
│  │  │             │  │             │  │             │  │             │        │ │
│  │  │ • Redis     │  │ • PgBouncer │  │ • Prepared  │  │ • JSON       │        │ │
│  │  │   Cache     │  │ • Connection│  │   Statements│  │   Response   │        │ │
│  │  │ • Query     │  │   Limits    │  │ • Query     │  │   Caching    │        │ │
│  │  │   Results   │  │ • Load      │  │   Plans     │  │ • Pagination │        │ │
│  │  │ • Session   │  │   Balancing │  │ • Parameter │  │ • Compression│        │ │
│  │  │   Data      │  │ • Failover  │  │   Binding   │  │ • Streaming  │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                             │
│                                    ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              DATABASE TIER                                  │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Query     │  │   Index     │  │   Partition │  │   Parallel   │        │ │
│  │  │   Optimizer │  │   Strategy  │  │   Strategy  │  │   Processing │        │ │
│  │  │             │  │             │  │             │  │             │        │ │
│  │  │ • Cost-     │  │ • B-tree    │  │ • Time-     │  │ • Parallel   │        │ │
│  │  │   Based     │  │   Indexes   │  │   Based     │  │   Queries    │        │ │
│  │  │   Planning  │  │ • Hash      │  │   Partition │  │ • Parallel   │        │ │
│  │  │ • Statistics│  │   Indexes   │  │ • Range     │  │   Scans      │        │ │
│  │  │ • Execution │  │ • GIN       │  │   Partition │  │ • Parallel   │        │ │
│  │  │   Plans     │  │   Indexes   │  │ • List      │  │   Joins      │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                             │
│                                    ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              STORAGE TIER                                   │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Buffer    │  │   WAL       │  │   Storage   │  │   I/O       │        │ │
│  │  │   Cache     │  │   Tuning    │  │   Layout    │  │   Optimization│       │ │
│  │  │             │  │             │  │             │  │             │        │ │
│  │  │ • Shared    │  │ • WAL       │  │ • SSD       │  │ • Async     │        │ │
│  │  │   Buffers   │  │   Buffers   │  │   Storage   │  │   I/O       │        │ │
│  │  │ • Work      │  │ • WAL       │  │ • RAID      │  │ • Direct    │        │ │
│  │  │   Memory    │  │   Segments  │  │   Arrays    │  │   I/O       │        │ │
│  │  │ • Temp      │  │ • Checkpoint│  │ • Storage   │  │ • I/O       │        │ │
│  │  │   Buffers   │  │   Tuning    │  │   Pools     │  │   Scheduler │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 🔍 Query Performance Analysis

### Performance Monitoring Queries

```sql
-- Slow query analysis
SELECT 
    query,
    calls,
    total_time,
    mean_time,
    stddev_time,
    rows,
    shared_blks_hit,
    shared_blks_read,
    shared_blks_written,
    shared_blks_dirtied,
    temp_blks_read,
    temp_blks_written,
    blk_read_time,
    blk_write_time
FROM pg_stat_statements 
WHERE mean_time > 1000  -- queries taking more than 1 second
ORDER BY mean_time DESC
LIMIT 20;

-- Table access patterns
SELECT 
    schemaname,
    tablename,
    seq_scan,
    seq_tup_read,
    idx_scan,
    idx_tup_fetch,
    n_tup_ins,
    n_tup_upd,
    n_tup_del,
    n_live_tup,
    n_dead_tup,
    last_vacuum,
    last_autovacuum,
    last_analyze,
    last_autoanalyze
FROM pg_stat_user_tables
ORDER BY seq_scan DESC;

-- Index usage analysis
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch,
    pg_size_pretty(pg_relation_size(indexrelid)) as index_size
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;

-- Connection analysis
SELECT 
    datname,
    numbackends,
    xact_commit,
    xact_rollback,
    blks_read,
    blks_hit,
    tup_returned,
    tup_fetched,
    tup_inserted,
    tup_updated,
    tup_deleted,
    temp_files,
    temp_bytes,
    deadlocks
FROM pg_stat_database;
```

### Query Execution Plan Analysis

```sql
-- Analyze query execution plan
EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) 
SELECT 
    c.camera_id,
    c.location,
    COUNT(cr.id) as total_count,
    AVG(cr.count_value) as avg_count,
    MAX(cr.created_at) as last_count
FROM cameras c
JOIN counting_results cr ON c.id = cr.camera_id
WHERE cr.created_at > NOW() - INTERVAL '24 hours'
GROUP BY c.camera_id, c.location
ORDER BY total_count DESC;

-- Check for missing indexes
SELECT 
    schemaname,
    tablename,
    attname,
    n_distinct,
    correlation
FROM pg_stats 
WHERE schemaname = 'public'
AND tablename IN ('cameras', 'counting_results', 'users')
ORDER BY tablename, attname;

-- Analyze table statistics
ANALYZE cameras;
ANALYZE counting_results;
ANALYZE users;
ANALYZE user_profiles;
```

## 📈 Indexing Strategy

### Strategic Index Design

```sql
-- Primary indexes for performance
CREATE INDEX CONCURRENTLY idx_counting_results_camera_time 
ON counting_results(camera_id, created_at DESC);

CREATE INDEX CONCURRENTLY idx_counting_results_time_range 
ON counting_results(created_at DESC) 
WHERE created_at > NOW() - INTERVAL '30 days';

CREATE INDEX CONCURRENTLY idx_users_email 
ON users(email) 
WHERE email IS NOT NULL;

CREATE INDEX CONCURRENTLY idx_cameras_location 
ON cameras(location) 
WHERE location IS NOT NULL;

-- Composite indexes for complex queries
CREATE INDEX CONCURRENTLY idx_counting_results_complex 
ON counting_results(camera_id, count_type, created_at DESC, count_value);

CREATE INDEX CONCURRENTLY idx_user_profiles_complex 
ON user_profiles(user_id, profile_type, updated_at DESC);

-- Partial indexes for filtered queries
CREATE INDEX CONCURRENTLY idx_active_cameras 
ON cameras(id, location) 
WHERE status = 'active';

CREATE INDEX CONCURRENTLY idx_recent_results 
ON counting_results(camera_id, created_at) 
WHERE created_at > NOW() - INTERVAL '7 days';

-- GIN indexes for JSON data
CREATE INDEX CONCURRENTLY idx_camera_metadata_gin 
ON cameras USING GIN (metadata);

CREATE INDEX CONCURRENTLY idx_user_preferences_gin 
ON user_profiles USING GIN (preferences);

-- Hash indexes for equality comparisons
CREATE INDEX CONCURRENTLY idx_users_username_hash 
ON users USING HASH (username);

CREATE INDEX CONCURRENTLY idx_cameras_serial_hash 
ON cameras USING HASH (serial_number);
```

### Index Maintenance

```sql
-- Index maintenance function
CREATE OR REPLACE FUNCTION maintain_indexes()
RETURNS VOID AS $$
DECLARE
    index_record RECORD;
BEGIN
    -- Reindex indexes with high bloat
    FOR index_record IN 
        SELECT 
            schemaname,
            tablename,
            indexname,
            pg_size_pretty(pg_relation_size(indexrelid)) as index_size
        FROM pg_stat_user_indexes 
        WHERE idx_scan > 1000  -- frequently used indexes
        AND schemaname = 'public'
    LOOP
        EXECUTE format('REINDEX INDEX CONCURRENTLY %I.%I', 
                      index_record.schemaname, 
                      index_record.indexname);
        
        RAISE NOTICE 'Reindexed: %.%', 
                    index_record.schemaname, 
                    index_record.indexname;
    END LOOP;
    
    -- Update table statistics
    ANALYZE;
END;
$$ LANGUAGE plpgsql;

-- Scheduled index maintenance
SELECT cron.schedule('index-maintenance', '0 2 * * 0', 'SELECT maintain_indexes();');
```

## 🗂️ Partitioning Strategy

### Time-Based Partitioning

```sql
-- Create partitioned table for counting results
CREATE TABLE counting_results_partitioned (
    id SERIAL,
    camera_id INTEGER NOT NULL,
    count_type VARCHAR(50) NOT NULL,
    count_value INTEGER NOT NULL,
    confidence_score DECIMAL(5,4),
    metadata JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) PARTITION BY RANGE (created_at);

-- Create monthly partitions
CREATE TABLE counting_results_2024_01 
PARTITION OF counting_results_partitioned 
FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

CREATE TABLE counting_results_2024_02 
PARTITION OF counting_results_partitioned 
FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');

CREATE TABLE counting_results_2024_03 
PARTITION OF counting_results_partitioned 
FOR VALUES FROM ('2024-03-01') TO ('2024-04-01');

-- Create indexes on partitions
CREATE INDEX idx_counting_results_2024_01_camera_time 
ON counting_results_2024_01(camera_id, created_at DESC);

CREATE INDEX idx_counting_results_2024_02_camera_time 
ON counting_results_2024_02(camera_id, created_at DESC);

CREATE INDEX idx_counting_results_2024_03_camera_time 
ON counting_results_2024_03(camera_id, created_at DESC);

-- Partition management function
CREATE OR REPLACE FUNCTION create_monthly_partition(year_month DATE)
RETURNS VOID AS $$
DECLARE
    partition_name TEXT;
    start_date DATE;
    end_date DATE;
BEGIN
    partition_name := 'counting_results_' || 
                     TO_CHAR(year_month, 'YYYY_MM');
    start_date := DATE_TRUNC('month', year_month);
    end_date := start_date + INTERVAL '1 month';
    
    EXECUTE format(
        'CREATE TABLE %I PARTITION OF counting_results_partitioned 
         FOR VALUES FROM (%L) TO (%L)',
        partition_name, start_date, end_date
    );
    
    EXECUTE format(
        'CREATE INDEX %I ON %I(camera_id, created_at DESC)',
        'idx_' || partition_name || '_camera_time',
        partition_name
    );
    
    RAISE NOTICE 'Created partition: %', partition_name;
END;
$$ LANGUAGE plpgsql;

-- Auto-create partitions
CREATE OR REPLACE FUNCTION auto_create_partitions()
RETURNS VOID AS $$
DECLARE
    next_month DATE;
BEGIN
    next_month := DATE_TRUNC('month', NOW()) + INTERVAL '1 month';
    
    -- Create next 3 months of partitions
    FOR i IN 0..2 LOOP
        PERFORM create_monthly_partition(next_month + (i || ' months')::INTERVAL);
    END LOOP;
END;
$$ LANGUAGE plpgsql;
```

## ⚡ Caching Strategy

### Application-Level Caching

```sql
-- Materialized views for complex aggregations
CREATE MATERIALIZED VIEW mv_daily_counts AS
SELECT 
    camera_id,
    DATE(created_at) as count_date,
    count_type,
    COUNT(*) as total_records,
    SUM(count_value) as total_count,
    AVG(count_value) as avg_count,
    MIN(count_value) as min_count,
    MAX(count_value) as max_count,
    AVG(confidence_score) as avg_confidence
FROM counting_results
WHERE created_at > NOW() - INTERVAL '30 days'
GROUP BY camera_id, DATE(created_at), count_type
ORDER BY camera_id, count_date DESC, count_type;

-- Create index on materialized view
CREATE INDEX idx_mv_daily_counts_camera_date 
ON mv_daily_counts(camera_id, count_date DESC);

-- Refresh materialized view function
CREATE OR REPLACE FUNCTION refresh_daily_counts()
RETURNS VOID AS $$
BEGIN
    REFRESH MATERIALIZED VIEW CONCURRENTLY mv_daily_counts;
    RAISE NOTICE 'Refreshed daily counts materialized view';
END;
$$ LANGUAGE plpgsql;

-- Scheduled refresh
SELECT cron.schedule('refresh-daily-counts', '0 */4 * * *', 
                    'SELECT refresh_daily_counts();');
```

### Query Result Caching

```sql
-- Cache table for frequently accessed data
CREATE TABLE query_cache (
    cache_key VARCHAR(255) PRIMARY KEY,
    cache_value JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    access_count INTEGER DEFAULT 0,
    last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for cache management
CREATE INDEX idx_query_cache_expires ON query_cache(expires_at);
CREATE INDEX idx_query_cache_access ON query_cache(last_accessed);

-- Cache management functions
CREATE OR REPLACE FUNCTION get_cached_result(cache_key VARCHAR(255))
RETURNS JSONB AS $$
DECLARE
    result JSONB;
BEGIN
    SELECT cache_value INTO result
    FROM query_cache
    WHERE cache_key = $1
    AND expires_at > NOW();
    
    IF result IS NOT NULL THEN
        UPDATE query_cache 
        SET access_count = access_count + 1,
            last_accessed = CURRENT_TIMESTAMP
        WHERE cache_key = $1;
    END IF;
    
    RETURN result;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION set_cached_result(
    cache_key VARCHAR(255),
    cache_value JSONB,
    ttl_seconds INTEGER DEFAULT 3600
)
RETURNS VOID AS $$
BEGIN
    INSERT INTO query_cache (cache_key, cache_value, expires_at)
    VALUES ($1, $2, NOW() + ($3 || ' seconds')::INTERVAL)
    ON CONFLICT (cache_key) 
    DO UPDATE SET 
        cache_value = EXCLUDED.cache_value,
        expires_at = EXCLUDED.expires_at,
        access_count = 0,
        last_accessed = CURRENT_TIMESTAMP;
END;
$$ LANGUAGE plpgsql;

-- Cache cleanup function
CREATE OR REPLACE FUNCTION cleanup_expired_cache()
RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    DELETE FROM query_cache 
    WHERE expires_at < NOW();
    
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    
    -- Also remove least accessed items if cache is too large
    DELETE FROM query_cache 
    WHERE cache_key IN (
        SELECT cache_key 
        FROM query_cache 
        ORDER BY access_count ASC, last_accessed ASC 
        LIMIT 100
    );
    
    RETURN deleted_count;
END;
$$ LANGUAGE plpgsql;
```

## 🔧 Database Configuration Tuning

### PostgreSQL Performance Settings

```sql
-- Memory configuration
ALTER SYSTEM SET shared_buffers = '2GB';  -- 25% of RAM
ALTER SYSTEM SET effective_cache_size = '6GB';  -- 75% of RAM
ALTER SYSTEM SET work_mem = '64MB';  -- Per operation memory
ALTER SYSTEM SET maintenance_work_mem = '256MB';  -- Maintenance operations

-- Connection settings
ALTER SYSTEM SET max_connections = 200;
ALTER SYSTEM SET shared_preload_libraries = 'pg_stat_statements,pgcrypto';

-- WAL settings
ALTER SYSTEM SET wal_buffers = '16MB';
ALTER SYSTEM SET checkpoint_completion_target = 0.9;
ALTER SYSTEM SET wal_writer_delay = '200ms';
ALTER SYSTEM SET max_wal_size = '2GB';
ALTER SYSTEM SET min_wal_size = '1GB';

-- Query planner settings
ALTER SYSTEM SET random_page_cost = 1.1;  -- For SSD
ALTER SYSTEM SET effective_io_concurrency = 200;  -- For SSD
ALTER SYSTEM SET default_statistics_target = 100;

-- Logging for performance analysis
ALTER SYSTEM SET log_statement = 'all';
ALTER SYSTEM SET log_min_duration_statement = 1000;  -- Log queries > 1s
ALTER SYSTEM SET log_checkpoints = on;
ALTER SYSTEM SET log_connections = on;
ALTER SYSTEM SET log_disconnections = on;
```

### Connection Pooling Configuration

```ini
# PgBouncer configuration (pgbouncer.ini)
[databases]
* = host=localhost port=5432

[pgbouncer]
listen_addr = *
listen_port = 6432
auth_type = md5
auth_file = /etc/pgbouncer/userlist.txt
pool_mode = transaction
max_client_conn = 1000
default_pool_size = 20
max_db_connections = 100
max_user_connections = 100
server_reset_query = DISCARD ALL
server_check_query = select 1
server_check_delay = 30
max_server_lifetime = 3600
```

## 📊 Performance Monitoring

### Performance Metrics Dashboard

```sql
-- Performance metrics view
CREATE VIEW performance_metrics AS
SELECT 
    'Query Performance' as category,
    'Average Query Time' as metric,
    ROUND(AVG(mean_time), 2) as value,
    'ms' as unit
FROM pg_stat_statements
WHERE calls > 10

UNION ALL

SELECT 
    'Query Performance' as category,
    'Slow Queries (>1s)' as metric,
    COUNT(*) as value,
    'queries' as unit
FROM pg_stat_statements
WHERE mean_time > 1000

UNION ALL

SELECT 
    'Cache Performance' as category,
    'Buffer Hit Ratio' as metric,
    ROUND(
        (SUM(heap_blks_hit) * 100.0) / 
        (SUM(heap_blks_hit) + SUM(heap_blks_read)), 2
    ) as value,
    '%' as unit
FROM pg_statio_user_tables

UNION ALL

SELECT 
    'Connection Performance' as category,
    'Active Connections' as metric,
    COUNT(*) as value,
    'connections' as unit
FROM pg_stat_activity
WHERE state = 'active'

UNION ALL

SELECT 
    'Storage Performance' as category,
    'Database Size' as metric,
    pg_size_pretty(pg_database_size(current_database())) as value,
    'size' as unit

UNION ALL

SELECT 
    'Index Performance' as category,
    'Index Hit Ratio' as metric,
    ROUND(
        (SUM(idx_blks_hit) * 100.0) / 
        (SUM(idx_blks_hit) + SUM(idx_blks_read)), 2
    ) as value,
    '%' as unit
FROM pg_statio_user_indexes;
```

### Performance Alerting

```sql
-- Performance alert function
CREATE OR REPLACE FUNCTION check_performance_alerts()
RETURNS TABLE(alert_type VARCHAR(100), message TEXT, severity VARCHAR(20)) AS $$
BEGIN
    -- Check for slow queries
    RETURN QUERY
    SELECT 
        'Slow Queries'::VARCHAR(100),
        'Queries taking longer than 5 seconds detected'::TEXT,
        'HIGH'::VARCHAR(20)
    WHERE EXISTS (
        SELECT 1 FROM pg_stat_statements 
        WHERE mean_time > 5000
    );
    
    -- Check buffer hit ratio
    RETURN QUERY
    SELECT 
        'Low Buffer Hit Ratio'::VARCHAR(100),
        'Buffer hit ratio below 90%'::TEXT,
        'MEDIUM'::VARCHAR(20)
    WHERE (
        SELECT (SUM(heap_blks_hit) * 100.0) / 
               (SUM(heap_blks_hit) + SUM(heap_blks_read))
        FROM pg_statio_user_tables
    ) < 90;
    
    -- Check connection count
    RETURN QUERY
    SELECT 
        'High Connection Count'::VARCHAR(100),
        'More than 80% of max connections in use'::TEXT,
        'HIGH'::VARCHAR(20)
    WHERE (
        SELECT COUNT(*) FROM pg_stat_activity
    ) > (
        SELECT setting::integer * 0.8 
        FROM pg_settings 
        WHERE name = 'max_connections'
    );
    
    -- Check for long-running transactions
    RETURN QUERY
    SELECT 
        'Long Running Transactions'::VARCHAR(100),
        'Transactions running longer than 10 minutes'::TEXT,
        'CRITICAL'::VARCHAR(20)
    WHERE EXISTS (
        SELECT 1 FROM pg_stat_activity 
        WHERE state = 'active' 
        AND query_start < NOW() - INTERVAL '10 minutes'
    );
END;
$$ LANGUAGE plpgsql;
```

## 🚀 Optimization Best Practices

### Query Optimization Guidelines

1. **Use EXPLAIN ANALYZE** để phân tích execution plan
2. **Avoid SELECT *** - chỉ select columns cần thiết
3. **Use LIMIT** cho large result sets
4. **Use appropriate indexes** cho WHERE, JOIN, ORDER BY clauses
5. **Use prepared statements** để tránh query parsing overhead
6. **Use connection pooling** để giảm connection overhead
7. **Use materialized views** cho complex aggregations
8. **Use partitioning** cho large tables
9. **Monitor and tune** regularly

### Performance Testing

```sql
-- Performance testing function
CREATE OR REPLACE FUNCTION performance_test()
RETURNS TABLE(test_name VARCHAR(100), duration_ms NUMERIC, rows_affected INTEGER) AS $$
DECLARE
    start_time TIMESTAMP;
    end_time TIMESTAMP;
    row_count INTEGER;
BEGIN
    -- Test 1: Simple SELECT
    start_time := clock_timestamp();
    SELECT COUNT(*) INTO row_count FROM counting_results WHERE created_at > NOW() - INTERVAL '1 hour';
    end_time := clock_timestamp();
    
    RETURN QUERY SELECT 
        'Hourly Count Query'::VARCHAR(100),
        EXTRACT(EPOCH FROM (end_time - start_time)) * 1000,
        row_count;
    
    -- Test 2: Complex JOIN
    start_time := clock_timestamp();
    SELECT COUNT(*) INTO row_count 
    FROM cameras c 
    JOIN counting_results cr ON c.id = cr.camera_id 
    WHERE cr.created_at > NOW() - INTERVAL '24 hours';
    end_time := clock_timestamp();
    
    RETURN QUERY SELECT 
        'Daily Camera Count Query'::VARCHAR(100),
        EXTRACT(EPOCH FROM (end_time - start_time)) * 1000,
        row_count;
    
    -- Test 3: Aggregation
    start_time := clock_timestamp();
    SELECT COUNT(*) INTO row_count 
    FROM (
        SELECT camera_id, COUNT(*) 
        FROM counting_results 
        WHERE created_at > NOW() - INTERVAL '7 days'
        GROUP BY camera_id
    ) subq;
    end_time := clock_timestamp();
    
    RETURN QUERY SELECT 
        'Weekly Aggregation Query'::VARCHAR(100),
        EXTRACT(EPOCH FROM (end_time - start_time)) * 1000,
        row_count;
END;
$$ LANGUAGE plpgsql;
```

---

**Tài liệu này cung cấp framework hoàn chỉnh cho Performance Tuning trong môi trường production, đảm bảo hiệu suất tối ưu cho hệ thống AI Camera Counting.** 