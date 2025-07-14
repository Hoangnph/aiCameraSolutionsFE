# Production Data Lifecycle Management - AI Camera Counting System

## 📊 Tổng quan

Tài liệu này trình bày chiến lược quản lý vòng đời dữ liệu cho hệ thống AI Camera Counting trong môi trường production, bao gồm data retention, archiving, purging và compliance.

## 🎯 Data Lifecycle Objectives

- **Compliance**: Tuân thủ GDPR, CCPA, và các quy định bảo mật dữ liệu
- **Performance**: Tối ưu hiệu suất database thông qua data management
- **Cost Optimization**: Giảm chi phí lưu trữ thông qua tiered storage
- **Data Quality**: Đảm bảo chất lượng và tính toàn vẹn dữ liệu
- **Accessibility**: Duy trì khả năng truy cập dữ liệu theo yêu cầu

## 🏗️ Data Lifecycle Architecture

### Multi-Tier Data Storage Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              DATA LIFECYCLE ARCHITECTURE                        │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              HOT STORAGE TIER                              │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Current   │  │   Recent    │  │   Active    │  │   Working   │        │ │
│  │  │   Data      │  │   Data      │  │   Sessions  │  │   Data      │        │ │
│  │  │             │  │             │  │             │  │             │        │ │
│  │  │ • Last 7    │  │ • Last 30   │  │ • User      │  │ • Temporary │        │ │
│  │  │   days      │  │   days      │  │   Sessions  │  │   Data      │        │ │
│  │  │ • Real-time │  │ • Recent    │  │ • Cache     │  │ • Staging   │        │ │
│  │  │   counts    │  │   analytics │  │   Data      │  │   Data      │        │ │
│  │  │ • Active    │  │ • Recent    │  │ • Session   │  │ • Process   │        │ │
│  │  │   cameras   │  │   reports   │  │   State     │  │   Data      │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                             │
│                                    ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              WARM STORAGE TIER                              │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Historical│  │   Archived  │  │   Compressed│  │   Indexed   │        │ │
│  │  │   Data      │  │   Data      │  │   Data      │  │   Data      │        │ │
│  │  │             │  │             │  │             │  │             │        │ │
│  │  │ • 1-12      │  │ • 1-5 years │  │ • Compressed│  │ • Searchable│        │ │
│  │  │   months    │  │ • Archived  │  │   archives  │  │   archives  │        │ │
│  │  │ • Monthly   │  │ • Backup    │  │ • Reduced   │  │ • Metadata  │        │ │
│  │  │   reports   │  │   copies    │  │   storage   │  │   indexed   │        │ │
│  │  │ • Quarterly │  │ • Compliance│  │ • Fast      │  │ • Full-text │        │ │
│  │  │   analytics │  │   data      │  │   retrieval │  │   search    │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                             │
│                                    ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              COLD STORAGE TIER                              │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Long-term │  │   Compliance│  │   Disaster  │  │   Analytics │        │ │
│  │  │   Archive   │  │   Archive   │  │   Recovery  │  │   Archive   │        │ │
│  │  │             │  │             │  │             │  │             │        │ │
│  │  │ • 5+ years  │  │ • Legal     │  │ • Off-site  │  │ • ML/AI     │        │ │
│  │  │ • Rarely    │  │   retention │  │   backup    │  │   training  │        │ │
│  │  │   accessed  │  │ • Audit     │  │ • Geo-      │  │   data      │        │ │
│  │  │ • Low cost  │  │   trails    │  │   redundant │  │ • Historical│        │ │
│  │  │   storage   │  │ • Regulatory│  │ • Long-term │  │   patterns  │        │ │
│  │  │ • Batch     │  │   compliance│  │   retention │  │ • Trend     │        │ │
│  │  │   access    │  │             │  │             │  │   analysis  │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 📅 Data Retention Policy

### Retention Schedule

```sql
-- Data retention configuration table
CREATE TABLE data_retention_policy (
    id SERIAL PRIMARY KEY,
    table_name VARCHAR(100) NOT NULL,
    retention_period INTERVAL NOT NULL,
    retention_type VARCHAR(50) NOT NULL, -- 'delete', 'archive', 'anonymize'
    archive_location VARCHAR(255),
    compliance_requirements TEXT[],
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Define retention policies
INSERT INTO data_retention_policy VALUES
(1, 'counting_results', INTERVAL '2 years', 'archive', 's3://archive/counting-results', 
 ARRAY['GDPR', 'CCPA'], NOW(), NOW()),

(2, 'user_sessions', INTERVAL '90 days', 'delete', NULL, 
 ARRAY['GDPR'], NOW(), NOW()),

(3, 'audit_logs', INTERVAL '7 years', 'archive', 's3://archive/audit-logs', 
 ARRAY['SOX', 'PCI-DSS'], NOW(), NOW()),

(4, 'camera_streams', INTERVAL '1 year', 'archive', 's3://archive/camera-streams', 
 ARRAY['GDPR'], NOW(), NOW()),

(5, 'user_profiles', INTERVAL '5 years', 'anonymize', NULL, 
 ARRAY['GDPR', 'CCPA'], NOW(), NOW()),

(6, 'system_logs', INTERVAL '1 year', 'delete', NULL, 
 ARRAY['internal'], NOW(), NOW()),

(7, 'performance_metrics', INTERVAL '3 years', 'archive', 's3://archive/metrics', 
 ARRAY['internal'], NOW(), NOW()),

(8, 'error_logs', INTERVAL '6 months', 'delete', NULL, 
 ARRAY['internal'], NOW(), NOW());
```

### Data Lifecycle Stages

```sql
-- Data lifecycle stages table
CREATE TABLE data_lifecycle_stages (
    id SERIAL PRIMARY KEY,
    stage_name VARCHAR(50) NOT NULL,
    stage_order INTEGER NOT NULL,
    description TEXT,
    retention_action VARCHAR(50),
    storage_tier VARCHAR(20),
    access_frequency VARCHAR(20),
    cost_factor DECIMAL(5,2)
);

-- Define lifecycle stages
INSERT INTO data_lifecycle_stages VALUES
(1, 'Active', 1, 'Currently active data in production', 'none', 'hot', 'high', 1.00),
(2, 'Recent', 2, 'Recently accessed data', 'none', 'hot', 'medium', 0.80),
(3, 'Historical', 3, 'Historical data for analysis', 'compress', 'warm', 'low', 0.50),
(4, 'Archived', 4, 'Archived data for compliance', 'archive', 'warm', 'rare', 0.30),
(5, 'Long-term', 5, 'Long-term storage for legal requirements', 'archive', 'cold', 'very_rare', 0.10),
(6, 'Purged', 6, 'Data permanently deleted', 'delete', 'none', 'none', 0.00);
```

## 🔄 Data Archiving Strategy

### Automated Archiving System

```sql
-- Archive configuration table
CREATE TABLE archive_config (
    id SERIAL PRIMARY KEY,
    source_table VARCHAR(100) NOT NULL,
    archive_table VARCHAR(100) NOT NULL,
    archive_condition TEXT NOT NULL,
    compression_type VARCHAR(20) DEFAULT 'gzip',
    storage_location VARCHAR(255),
    schedule_cron VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    last_archive_run TIMESTAMP,
    next_archive_run TIMESTAMP
);

-- Archive tables structure
CREATE TABLE counting_results_archive (
    id INTEGER,
    camera_id INTEGER,
    count_type VARCHAR(50),
    count_value INTEGER,
    confidence_score DECIMAL(5,4),
    metadata JSONB,
    created_at TIMESTAMP,
    archived_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    archive_batch_id VARCHAR(50)
) PARTITION BY RANGE (archived_at);

-- Archive function
CREATE OR REPLACE FUNCTION archive_old_data(
    p_table_name VARCHAR(100),
    p_retention_days INTEGER
)
RETURNS INTEGER AS $$
DECLARE
    archive_count INTEGER;
    archive_table_name VARCHAR(100);
    archive_condition TEXT;
    batch_id VARCHAR(50);
BEGIN
    -- Generate batch ID
    batch_id := 'batch_' || TO_CHAR(NOW(), 'YYYYMMDD_HH24MISS');
    
    -- Get archive configuration
    SELECT 
        archive_table,
        archive_condition
    INTO 
        archive_table_name,
        archive_condition
    FROM archive_config 
    WHERE source_table = p_table_name;
    
    -- Archive data
    EXECUTE format(
        'INSERT INTO %I (
            id, camera_id, count_type, count_value, 
            confidence_score, metadata, created_at, 
            archived_at, archive_batch_id
        )
        SELECT 
            id, camera_id, count_type, count_value,
            confidence_score, metadata, created_at,
            NOW(), %L
        FROM %I 
        WHERE created_at < NOW() - INTERVAL ''%s days''
        AND %s',
        archive_table_name,
        batch_id,
        p_table_name,
        p_retention_days,
        archive_condition
    );
    
    GET DIAGNOSTICS archive_count = ROW_COUNT;
    
    -- Delete archived data from source
    IF archive_count > 0 THEN
        EXECUTE format(
            'DELETE FROM %I 
             WHERE created_at < NOW() - INTERVAL ''%s days''
             AND %s',
            p_table_name,
            p_retention_days,
            archive_condition
        );
    END IF;
    
    -- Update archive config
    UPDATE archive_config 
    SET last_archive_run = NOW(),
        next_archive_run = NOW() + INTERVAL '1 day'
    WHERE source_table = p_table_name;
    
    RETURN archive_count;
END;
$$ LANGUAGE plpgsql;
```

### Compression and Storage Optimization

```sql
-- Compression function for archived data
CREATE OR REPLACE FUNCTION compress_archived_data(
    p_archive_table VARCHAR(100)
)
RETURNS VOID AS $$
BEGIN
    -- Enable compression on archive table
    EXECUTE format('ALTER TABLE %I SET (compression = lz4)', p_archive_table);
    
    -- Compress existing data
    EXECUTE format('VACUUM ANALYZE %I', p_archive_table);
    
    RAISE NOTICE 'Compressed archive table: %', p_archive_table;
END;
$$ LANGUAGE plpgsql;

-- Storage optimization function
CREATE OR REPLACE FUNCTION optimize_storage()
RETURNS TABLE(table_name VARCHAR(100), original_size TEXT, optimized_size TEXT, savings_percent NUMERIC) AS $$
DECLARE
    table_record RECORD;
    original_size BIGINT;
    optimized_size BIGINT;
BEGIN
    FOR table_record IN 
        SELECT tablename 
        FROM pg_tables 
        WHERE schemaname = 'public'
        AND tablename LIKE '%archive%'
    LOOP
        -- Get original size
        SELECT pg_total_relation_size(table_record.tablename) INTO original_size;
        
        -- Optimize table
        EXECUTE format('VACUUM FULL ANALYZE %I', table_record.tablename);
        
        -- Get optimized size
        SELECT pg_total_relation_size(table_record.tablename) INTO optimized_size;
        
        RETURN QUERY SELECT 
            table_record.tablename::VARCHAR(100),
            pg_size_pretty(original_size),
            pg_size_pretty(optimized_size),
            ROUND(((original_size - optimized_size) * 100.0) / original_size, 2);
    END LOOP;
END;
$$ LANGUAGE plpgsql;
```

## 🗑️ Data Purging Strategy

### Automated Data Purging

```sql
-- Purge configuration table
CREATE TABLE purge_config (
    id SERIAL PRIMARY KEY,
    table_name VARCHAR(100) NOT NULL,
    purge_condition TEXT NOT NULL,
    purge_frequency VARCHAR(50) DEFAULT 'daily',
    batch_size INTEGER DEFAULT 10000,
    is_active BOOLEAN DEFAULT TRUE,
    last_purge_run TIMESTAMP,
    next_purge_run TIMESTAMP,
    total_purged_count BIGINT DEFAULT 0
);

-- Define purge configurations
INSERT INTO purge_config VALUES
(1, 'user_sessions', 'last_activity < NOW() - INTERVAL ''90 days''', 'daily', 5000, TRUE, NULL, NOW() + INTERVAL '1 day', 0),
(2, 'system_logs', 'created_at < NOW() - INTERVAL ''1 year''', 'weekly', 10000, TRUE, NULL, NOW() + INTERVAL '1 week', 0),
(3, 'error_logs', 'created_at < NOW() - INTERVAL ''6 months''', 'daily', 5000, TRUE, NULL, NOW() + INTERVAL '1 day', 0),
(4, 'temp_data', 'created_at < NOW() - INTERVAL ''7 days''', 'daily', 1000, TRUE, NULL, NOW() + INTERVAL '1 day', 0);

-- Purge function
CREATE OR REPLACE FUNCTION purge_expired_data(
    p_table_name VARCHAR(100)
)
RETURNS INTEGER AS $$
DECLARE
    purge_count INTEGER := 0;
    batch_count INTEGER;
    total_purged INTEGER := 0;
    purge_condition TEXT;
    batch_size INTEGER;
BEGIN
    -- Get purge configuration
    SELECT 
        purge_condition,
        batch_size
    INTO 
        purge_condition,
        batch_size
    FROM purge_config 
    WHERE table_name = p_table_name;
    
    -- Purge in batches
    LOOP
        EXECUTE format(
            'DELETE FROM %I 
             WHERE %s 
             LIMIT %s',
            p_table_name,
            purge_condition,
            batch_size
        );
        
        GET DIAGNOSTICS batch_count = ROW_COUNT;
        total_purged := total_purged + batch_count;
        
        -- Exit if no more rows to purge
        EXIT WHEN batch_count = 0;
        
        -- Commit batch
        COMMIT;
        
        -- Small delay to prevent blocking
        PERFORM pg_sleep(0.1);
    END LOOP;
    
    -- Update purge config
    UPDATE purge_config 
    SET last_purge_run = NOW(),
        next_purge_run = NOW() + INTERVAL '1 day',
        total_purged_count = total_purged_count + total_purged
    WHERE table_name = p_table_name;
    
    RETURN total_purged;
END;
$$ LANGUAGE plpgsql;
```

### Data Anonymization

```sql
-- Anonymization function
CREATE OR REPLACE FUNCTION anonymize_user_data(
    p_user_id INTEGER
)
RETURNS VOID AS $$
BEGIN
    -- Anonymize user profile
    UPDATE user_profiles 
    SET 
        first_name = 'ANONYMIZED',
        last_name = 'USER',
        email = 'anonymized_' || id || '@example.com',
        phone = '000-000-0000',
        address = 'ANONYMIZED',
        preferences = '{}'::jsonb,
        updated_at = NOW()
    WHERE user_id = p_user_id;
    
    -- Anonymize user sessions
    UPDATE user_sessions 
    SET 
        session_data = '{}'::jsonb,
        user_agent = 'ANONYMIZED',
        ip_address = '0.0.0.0'::inet
    WHERE user_id = p_user_id;
    
    -- Log anonymization
    INSERT INTO audit_logs (
        user_id, action, resource_type, resource_name, 
        old_values, new_values, ip_address
    ) VALUES (
        p_user_id, 'ANONYMIZE_USER', 'user', p_user_id::text,
        '{"action": "anonymization"}', '{"status": "completed"}',
        '0.0.0.0'::inet
    );
    
    RAISE NOTICE 'Anonymized user data for user ID: %', p_user_id;
END;
$$ LANGUAGE plpgsql;
```

## 📊 Data Lifecycle Monitoring

### Lifecycle Metrics Dashboard

```sql
-- Data lifecycle metrics view
CREATE VIEW data_lifecycle_metrics AS
SELECT 
    'Data Volume' as category,
    'Total Database Size' as metric,
    pg_size_pretty(pg_database_size(current_database())) as value,
    'size' as unit

UNION ALL

SELECT 
    'Data Volume' as category,
    'Active Data Size' as metric,
    pg_size_pretty(
        COALESCE(SUM(pg_total_relation_size(tablename)), 0)
    ) as value,
    'size' as unit
FROM pg_tables 
WHERE schemaname = 'public' 
AND tablename NOT LIKE '%archive%'

UNION ALL

SELECT 
    'Data Volume' as category,
    'Archive Data Size' as metric,
    pg_size_pretty(
        COALESCE(SUM(pg_total_relation_size(tablename)), 0)
    ) as value,
    'size' as unit
FROM pg_tables 
WHERE schemaname = 'public' 
AND tablename LIKE '%archive%'

UNION ALL

SELECT 
    'Retention' as category,
    'Records Pending Archive' as metric,
    COUNT(*)::text as value,
    'records' as unit
FROM counting_results 
WHERE created_at < NOW() - INTERVAL '2 years'

UNION ALL

SELECT 
    'Retention' as category,
    'Records Pending Purge' as metric,
    COUNT(*)::text as value,
    'records' as unit
FROM user_sessions 
WHERE last_activity < NOW() - INTERVAL '90 days'

UNION ALL

SELECT 
    'Compliance' as category,
    'GDPR Compliance Status' as metric,
    CASE 
        WHEN EXISTS (
            SELECT 1 FROM user_profiles 
            WHERE updated_at < NOW() - INTERVAL '5 years'
        ) THEN 'Non-Compliant'
        ELSE 'Compliant'
    END as value,
    'status' as unit;
```

### Lifecycle Alerting

```sql
-- Lifecycle alert function
CREATE OR REPLACE FUNCTION check_lifecycle_alerts()
RETURNS TABLE(alert_type VARCHAR(100), message TEXT, severity VARCHAR(20)) AS $$
BEGIN
    -- Check for data volume alerts
    RETURN QUERY
    SELECT 
        'High Data Volume'::VARCHAR(100),
        'Database size exceeds 80% of capacity'::TEXT,
        'HIGH'::VARCHAR(20)
    WHERE pg_database_size(current_database()) > 
          (SELECT setting::bigint * 0.8 FROM pg_settings WHERE name = 'max_database_size');
    
    -- Check for retention compliance
    RETURN QUERY
    SELECT 
        'Retention Compliance'::VARCHAR(100),
        'Data retention policy violations detected'::TEXT,
        'MEDIUM'::VARCHAR(20)
    WHERE EXISTS (
        SELECT 1 FROM counting_results 
        WHERE created_at < NOW() - INTERVAL '2 years'
        LIMIT 1000
    );
    
    -- Check for archive failures
    RETURN QUERY
    SELECT 
        'Archive Failure'::VARCHAR(100),
        'Data archiving process failed'::TEXT,
        'HIGH'::VARCHAR(20)
    WHERE EXISTS (
        SELECT 1 FROM archive_config 
        WHERE last_archive_run < NOW() - INTERVAL '2 days'
        AND is_active = TRUE
    );
    
    -- Check for purge failures
    RETURN QUERY
    SELECT 
        'Purge Failure'::VARCHAR(100),
        'Data purging process failed'::TEXT,
        'MEDIUM'::VARCHAR(20)
    WHERE EXISTS (
        SELECT 1 FROM purge_config 
        WHERE last_purge_run < NOW() - INTERVAL '2 days'
        AND is_active = TRUE
    );
END;
$$ LANGUAGE plpgsql;
```

## 🔧 Implementation Guidelines

### Automated Lifecycle Management

```sql
-- Lifecycle management function
CREATE OR REPLACE FUNCTION manage_data_lifecycle()
RETURNS VOID AS $$
DECLARE
    policy_record RECORD;
    archive_count INTEGER;
    purge_count INTEGER;
BEGIN
    -- Process retention policies
    FOR policy_record IN 
        SELECT * FROM data_retention_policy 
        WHERE is_active = TRUE
    LOOP
        CASE policy_record.retention_type
            WHEN 'archive' THEN
                -- Archive data
                SELECT archive_old_data(
                    policy_record.table_name,
                    EXTRACT(EPOCH FROM policy_record.retention_period) / 86400
                ) INTO archive_count;
                
                RAISE NOTICE 'Archived % records from %', 
                            archive_count, policy_record.table_name;
                
            WHEN 'delete' THEN
                -- Purge data
                SELECT purge_expired_data(policy_record.table_name) 
                INTO purge_count;
                
                RAISE NOTICE 'Purged % records from %', 
                            purge_count, policy_record.table_name;
                
            WHEN 'anonymize' THEN
                -- Anonymize data
                -- Implementation depends on specific requirements
                RAISE NOTICE 'Anonymization scheduled for %', 
                            policy_record.table_name;
        END CASE;
    END LOOP;
    
    -- Optimize storage
    PERFORM optimize_storage();
    
    -- Update metrics
    REFRESH MATERIALIZED VIEW data_lifecycle_metrics;
END;
$$ LANGUAGE plpgsql;

-- Schedule lifecycle management
SELECT cron.schedule('data-lifecycle', '0 2 * * *', 
                    'SELECT manage_data_lifecycle();');
```

### Compliance Reporting

```sql
-- Compliance report function
CREATE OR REPLACE FUNCTION generate_compliance_report()
RETURNS TABLE(compliance_area VARCHAR(100), status VARCHAR(20), details TEXT) AS $$
BEGIN
    -- GDPR Compliance
    RETURN QUERY
    SELECT 
        'GDPR Data Retention'::VARCHAR(100),
        CASE 
            WHEN EXISTS (
                SELECT 1 FROM user_profiles 
                WHERE updated_at < NOW() - INTERVAL '5 years'
            ) THEN 'Non-Compliant'::VARCHAR(20)
            ELSE 'Compliant'::VARCHAR(20)
        END,
        'User data retention compliance check'::TEXT;
    
    -- Data Access Compliance
    RETURN QUERY
    SELECT 
        'Data Access Logging'::VARCHAR(100),
        CASE 
            WHEN EXISTS (
                SELECT 1 FROM audit_logs 
                WHERE created_at > NOW() - INTERVAL '1 day'
            ) THEN 'Compliant'::VARCHAR(20)
            ELSE 'Non-Compliant'::VARCHAR(20)
        END,
        'Audit logging compliance check'::TEXT;
    
    -- Data Deletion Compliance
    RETURN QUERY
    SELECT 
        'Data Deletion Requests'::VARCHAR(100),
        CASE 
            WHEN EXISTS (
                SELECT 1 FROM data_deletion_requests 
                WHERE status = 'pending'
                AND created_at < NOW() - INTERVAL '30 days'
            ) THEN 'Non-Compliant'::VARCHAR(20)
            ELSE 'Compliant'::VARCHAR(20)
        END,
        'Data deletion request compliance check'::TEXT;
END;
$$ LANGUAGE plpgsql;
```

---

**Tài liệu này cung cấp framework hoàn chỉnh cho Data Lifecycle Management trong môi trường production, đảm bảo tuân thủ quy định và tối ưu hiệu suất hệ thống.** 