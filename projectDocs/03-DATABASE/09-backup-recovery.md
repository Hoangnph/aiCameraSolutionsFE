# Backup and Recovery Guide - AI Camera Counting System

## 📊 Tổng quan

Tài liệu này cung cấp hướng dẫn chi tiết về backup và recovery database cho hệ thống AI Camera Counting, bao gồm backup strategy, recovery procedures, disaster recovery, và testing procedures.

## 🎯 Mục tiêu backup & recovery

- **RTO (Recovery Time Objective)**: < 4 giờ
- **RPO (Recovery Point Objective)**: < 1 giờ
- **Data Retention**: 7 năm cho compliance
- **Backup Frequency**: Continuous + daily full backup
- **Recovery Testing**: Monthly testing procedures

## 🏗️ Backup Architecture

### Backup Strategy Overview

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              BACKUP ARCHITECTURE OVERVIEW                       │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              PRODUCTION DATABASE                            │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Primary   │  │   Read      │  │   WAL       │  │   Archive   │        │ │
│  │  │   Database  │  │   Replicas  │  │   Streaming │  │   Logs      │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                             │
│                                    ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              BACKUP LAYER                                   │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Full      │  │   Incremental│  │   Differential│  │   Continuous│        │ │
│  │  │   Backup    │  │   Backup    │  │   Backup    │  │   Backup    │        │ │
│  │  │             │  │             │  │             │  │             │        │ │
│  │  │ • Daily     │  │ • Hourly    │  │ • Weekly    │  │ • WAL       │        │ │
│  │  │ • Complete  │  │ • Changes   │  │ • Changes   │  │   Archiving │        │ │
│  │  │ • Compressed│  │ • Fast      │  │ • Medium    │  │ • Real-time │        │ │
│  │  │ • Encrypted │  │ • Small     │  │ • Balanced  │  │ • Point-in-time│        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                             │
│                                    ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              STORAGE LAYER                                  │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Local     │  │   Network   │  │   Cloud     │  │   Archive   │        │ │
│  │  │   Storage   │  │   Storage   │  │   Storage   │  │   Storage   │        │ │
│  │  │             │  │             │  │             │  │             │        │ │
│  │  │ • Fast      │  │ • Shared    │  │ • Scalable  │  │ • Long-term │        │ │
│  │  │ • Access    │  │ • Redundant │  │ • Reliable  │  │ • Compliance│        │ │
│  │  │ • Recovery  │  │ • Backup    │  │ • Disaster  │  │ • Retention │        │ │
│  │  │ • Testing   │  │ • Mirror    │  │ • Recovery  │  │ • Legal     │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Backup Data Flow

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              BACKUP DATA FLOW                                   │
│                                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐      │
│  │   Database  │    │   Backup    │    │   Storage   │    │   Monitoring│      │
│  │   Engine    │    │   Process   │    │   System    │    │   & Alerting│      │
│  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘      │
│         │                   │                   │                   │          │
│         │ 1. Trigger        │                   │                   │          │
│         │ Backup            │                   │                   │          │
│         │ (Scheduled/Manual)│                   │                   │          │
│         │──────────────────►│                   │                   │          │
│         │                   │                   │                   │          │
│         │                   │ 2. Create         │                   │          │
│         │                   │ Backup            │                   │          │
│         │                   │ (pg_dump/WAL)     │                   │          │
│         │                   │──────────────────►│                   │          │
│         │                   │                   │                   │          │
│         │                   │                   │ 3. Store          │          │
│         │                   │                   │ Backup            │          │
│         │                   │                   │ (Compressed/Encrypted)│          │
│         │                   │                   │──────────────────►│          │
│         │                   │                   │                   │          │
│         │                   │                   │ 4. Verify         │          │
│         │                   │                   │ Backup            │          │
│         │                   │                   │ Integrity         │          │
│         │                   │                   │◄──────────────────┤          │
│         │                   │                   │                   │          │
│         │                   │ 5. Update         │                   │          │
│         │                   │ Backup Catalog    │                   │          │
│         │                   │ (Metadata)        │                   │          │
│         │                   │──────────────────►│                   │          │
│         │                   │                   │                   │          │
│         │                   │ 6. Notify         │                   │          │
│         │                   │ Success/Failure   │                   │          │
│         │                   │ (Monitoring)      │                   │          │
│         │                   │──────────────────►│                   │          │
│         │                   │                   │                   │          │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 📋 Backup Types

### 1. Full Backup

**Mục đích**: Backup toàn bộ database với compression và encryption.

```sql
-- Full backup function
CREATE OR REPLACE FUNCTION create_full_backup()
RETURNS TEXT AS $$
DECLARE
    backup_file TEXT;
    timestamp TEXT;
    checksum TEXT;
BEGIN
    timestamp := to_char(NOW(), 'YYYYMMDD_HH24MISS');
    backup_file := '/backups/full_backup_' || timestamp || '.sql.gz';
    
    -- Create full backup with compression
    PERFORM pg_dump(
        'ai_camera_counting_db',
        '--format=custom',
        '--compress=9',
        '--file=' || backup_file,
        '--verbose',
        '--no-password'
    );
    
    -- Calculate checksum
    SELECT MD5(pg_read_file(backup_file)) INTO checksum;
    
    -- Record backup in catalog
    INSERT INTO backup_catalog (
        backup_type,
        backup_file,
        backup_size,
        checksum,
        compression_ratio,
        created_at,
        status
    ) VALUES (
        'full',
        backup_file,
        pg_stat_file(backup_file).size,
        checksum,
        0.3, -- Estimated compression ratio
        NOW(),
        'completed'
    );
    
    -- Log backup completion
    INSERT INTO backup_log (
        backup_type,
        backup_file,
        message,
        created_at
    ) VALUES (
        'full',
        backup_file,
        'Full backup completed successfully',
        NOW()
    );
    
    RETURN backup_file;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
```

### 2. Incremental Backup

**Mục đích**: Backup chỉ những thay đổi từ lần backup cuối.

```sql
-- Incremental backup function
CREATE OR REPLACE FUNCTION create_incremental_backup()
RETURNS TEXT AS $$
DECLARE
    backup_file TEXT;
    timestamp TEXT;
    last_backup_time TIMESTAMP;
    changes_count INTEGER;
BEGIN
    timestamp := to_char(NOW(), 'YYYYMMDD_HH24MISS');
    backup_file := '/backups/incremental_backup_' || timestamp || '.sql.gz';
    
    -- Get last backup time
    SELECT MAX(created_at) INTO last_backup_time
    FROM backup_catalog
    WHERE backup_type = 'full';
    
    -- Create incremental backup
    PERFORM pg_dump(
        'ai_camera_counting_db',
        '--format=custom',
        '--compress=9',
        '--file=' || backup_file,
        '--verbose',
        '--no-password',
        '--data-only',
        '--where=updated_at >= ''' || last_backup_time || ''''
    );
    
    -- Count changes
    SELECT COUNT(*) INTO changes_count
    FROM (
        SELECT 'counting_results' as table_name, COUNT(*) as changes
        FROM counting_results WHERE created_at >= last_backup_time
        UNION ALL
        SELECT 'camera_events' as table_name, COUNT(*) as changes
        FROM camera_events WHERE timestamp >= last_backup_time
        UNION ALL
        SELECT 'analytics' as table_name, COUNT(*) as changes
        FROM analytics WHERE created_at >= last_backup_time
    ) changes_summary;
    
    -- Record incremental backup
    INSERT INTO backup_catalog (
        backup_type,
        backup_file,
        backup_size,
        changes_count,
        created_at,
        status
    ) VALUES (
        'incremental',
        backup_file,
        pg_stat_file(backup_file).size,
        changes_count,
        NOW(),
        'completed'
    );
    
    RETURN backup_file;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
```

### 3. WAL Archiving (Continuous Backup)

**Mục đích**: Archive WAL files để point-in-time recovery.

```sql
-- WAL archiving configuration
ALTER SYSTEM SET archive_mode = on;
ALTER SYSTEM SET archive_command = 'cp %p /backups/wal/%f';
ALTER SYSTEM SET archive_timeout = 300; -- 5 minutes
ALTER SYSTEM SET wal_level = replica;

-- WAL archiving function
CREATE OR REPLACE FUNCTION archive_wal_files()
RETURNS void AS $$
DECLARE
    wal_file RECORD;
BEGIN
    -- Archive WAL files
    FOR wal_file IN
        SELECT pg_walfile_name(pg_current_wal_lsn()) as current_wal
    LOOP
        -- Copy WAL file to archive
        PERFORM pg_exec('cp ' || pg_walfile_name(pg_current_wal_lsn()) || ' /backups/wal/');
        
        -- Compress archived WAL
        PERFORM pg_exec('gzip /backups/wal/' || pg_walfile_name(pg_current_wal_lsn()));
        
        -- Update WAL catalog
        INSERT INTO wal_archive_catalog (
            wal_file,
            archive_path,
            file_size,
            archived_at
        ) VALUES (
            pg_walfile_name(pg_current_wal_lsn()),
            '/backups/wal/' || pg_walfile_name(pg_current_wal_lsn()) || '.gz',
            pg_stat_file('/backups/wal/' || pg_walfile_name(pg_current_wal_lsn()) || '.gz').size,
            NOW()
        );
    END LOOP;
END;
$$ LANGUAGE plpgsql;
```

## 🔄 Recovery Procedures

### 1. Full Database Recovery

```sql
-- Full recovery function
CREATE OR REPLACE FUNCTION recover_full_database(backup_file TEXT)
RETURNS BOOLEAN AS $$
DECLARE
    recovery_start TIMESTAMP;
    recovery_end TIMESTAMP;
    success BOOLEAN;
BEGIN
    recovery_start := NOW();
    
    -- Stop database connections
    PERFORM pg_terminate_backend(pid)
    FROM pg_stat_activity
    WHERE datname = 'ai_camera_counting_db'
    AND pid <> pg_backend_pid();
    
    -- Drop existing database
    DROP DATABASE IF EXISTS ai_camera_counting_db;
    
    -- Create new database
    CREATE DATABASE ai_camera_counting_db;
    
    -- Restore from backup
    BEGIN
        PERFORM pg_restore(
            'ai_camera_counting_db',
            backup_file,
            '--verbose',
            '--no-password',
            '--clean',
            '--if-exists'
        );
        
        success := TRUE;
        
    EXCEPTION WHEN OTHERS THEN
        success := FALSE;
        
        -- Log recovery failure
        INSERT INTO recovery_log (
            recovery_type,
            backup_file,
            error_message,
            started_at,
            completed_at,
            status
        ) VALUES (
            'full',
            backup_file,
            SQLERRM,
            recovery_start,
            NOW(),
            'failed'
        );
    END;
    
    recovery_end := NOW();
    
    -- Log recovery completion
    INSERT INTO recovery_log (
        recovery_type,
        backup_file,
        started_at,
        completed_at,
        duration,
        status
    ) VALUES (
        'full',
        backup_file,
        recovery_start,
        recovery_end,
        recovery_end - recovery_start,
        CASE WHEN success THEN 'completed' ELSE 'failed' END
    );
    
    RETURN success;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
```

### 2. Point-in-Time Recovery

```sql
-- Point-in-time recovery function
CREATE OR REPLACE FUNCTION point_in_time_recovery(
    target_time TIMESTAMP,
    backup_file TEXT
)
RETURNS BOOLEAN AS $$
DECLARE
    recovery_start TIMESTAMP;
    recovery_end TIMESTAMP;
    success BOOLEAN;
BEGIN
    recovery_start := NOW();
    
    -- Restore base backup
    PERFORM recover_full_database(backup_file);
    
    -- Apply WAL files up to target time
    BEGIN
        -- Create recovery.conf
        PERFORM pg_exec('echo "restore_command = ''cp /backups/wal/%f %p''" > /var/lib/postgresql/recovery.conf');
        PERFORM pg_exec('echo "recovery_target_time = ''' || target_time || '''" >> /var/lib/postgresql/recovery.conf');
        PERFORM pg_exec('echo "recovery_target_action = ''promote''" >> /var/lib/postgresql/recovery.conf');
        
        -- Restart database in recovery mode
        PERFORM pg_exec('pg_ctl restart -D /var/lib/postgresql/data');
        
        success := TRUE;
        
    EXCEPTION WHEN OTHERS THEN
        success := FALSE;
        
        -- Log recovery failure
        INSERT INTO recovery_log (
            recovery_type,
            backup_file,
            target_time,
            error_message,
            started_at,
            completed_at,
            status
        ) VALUES (
            'point_in_time',
            backup_file,
            target_time,
            SQLERRM,
            recovery_start,
            NOW(),
            'failed'
        );
    END;
    
    recovery_end := NOW();
    
    -- Log recovery completion
    INSERT INTO recovery_log (
        recovery_type,
        backup_file,
        target_time,
        started_at,
        completed_at,
        duration,
        status
    ) VALUES (
        'point_in_time',
        backup_file,
        target_time,
        recovery_start,
        recovery_end,
        recovery_end - recovery_start,
        CASE WHEN success THEN 'completed' ELSE 'failed' END
    );
    
    RETURN success;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
```

### 3. Table-level Recovery

```sql
-- Table-level recovery function
CREATE OR REPLACE FUNCTION recover_table(
    table_name TEXT,
    backup_file TEXT
)
RETURNS BOOLEAN AS $$
DECLARE
    recovery_start TIMESTAMP;
    recovery_end TIMESTAMP;
    success BOOLEAN;
BEGIN
    recovery_start := NOW();
    
    -- Create temporary database for extraction
    CREATE DATABASE temp_recovery_db;
    
    BEGIN
        -- Restore backup to temporary database
        PERFORM pg_restore(
            'temp_recovery_db',
            backup_file,
            '--verbose',
            '--no-password',
            '--table=' || table_name
        );
        
        -- Export table data
        PERFORM pg_dump(
            'temp_recovery_db',
            '--table=' || table_name,
            '--data-only',
            '--format=plain',
            '--file=/tmp/' || table_name || '_recovered.sql'
        );
        
        -- Import to production database
        PERFORM pg_exec('psql ai_camera_counting_db < /tmp/' || table_name || '_recovered.sql');
        
        success := TRUE;
        
    EXCEPTION WHEN OTHERS THEN
        success := FALSE;
        
        -- Log recovery failure
        INSERT INTO recovery_log (
            recovery_type,
            backup_file,
            table_name,
            error_message,
            started_at,
            completed_at,
            status
        ) VALUES (
            'table',
            backup_file,
            table_name,
            SQLERRM,
            recovery_start,
            NOW(),
            'failed'
        );
    END;
    
    -- Clean up temporary database
    DROP DATABASE temp_recovery_db;
    
    recovery_end := NOW();
    
    -- Log recovery completion
    INSERT INTO recovery_log (
        recovery_type,
        backup_file,
        table_name,
        started_at,
        completed_at,
        duration,
        status
    ) VALUES (
        'table',
        backup_file,
        table_name,
        recovery_start,
        recovery_end,
        recovery_end - recovery_start,
        CASE WHEN success THEN 'completed' ELSE 'failed' END
    );
    
    RETURN success;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
```

## 🛡️ Disaster Recovery

### 1. Disaster Recovery Plan

```sql
-- Disaster recovery procedures table
CREATE TABLE IF NOT EXISTS disaster_recovery_procedures (
    id SERIAL PRIMARY KEY,
    scenario disaster_scenario NOT NULL,
    priority INTEGER NOT NULL,
    rto_minutes INTEGER NOT NULL,
    rpo_minutes INTEGER NOT NULL,
    procedure_steps TEXT[] NOT NULL,
    required_resources TEXT[],
    contact_person VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Disaster scenario enum
DO $$ BEGIN
    CREATE TYPE disaster_scenario AS ENUM (
        'database_corruption',
        'hardware_failure',
        'network_outage',
        'data_center_disaster',
        'cyber_attack',
        'human_error'
    );
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- Insert disaster recovery procedures
INSERT INTO disaster_recovery_procedures (
    scenario,
    priority,
    rto_minutes,
    rpo_minutes,
    procedure_steps,
    required_resources,
    contact_person
) VALUES (
    'database_corruption',
    1,
    240, -- 4 hours
    60,  -- 1 hour
    ARRAY[
        '1. Assess corruption extent',
        '2. Stop all database connections',
        '3. Restore from latest backup',
        '4. Apply WAL files if needed',
        '5. Validate data integrity',
        '6. Restart application services',
        '7. Monitor system health'
    ],
    ARRAY['backup_server', 'recovery_team', 'database_admin'],
    'Database Administrator'
);
```

### 2. Automated Disaster Recovery

```sql
-- Automated disaster recovery function
CREATE OR REPLACE FUNCTION automated_disaster_recovery()
RETURNS BOOLEAN AS $$
DECLARE
    latest_backup TEXT;
    recovery_success BOOLEAN;
BEGIN
    -- Get latest backup
    SELECT backup_file INTO latest_backup
    FROM backup_catalog
    WHERE status = 'completed'
    ORDER BY created_at DESC
    LIMIT 1;
    
    IF latest_backup IS NULL THEN
        RAISE EXCEPTION 'No valid backup found for recovery';
    END IF;
    
    -- Log disaster recovery start
    INSERT INTO disaster_recovery_log (
        scenario,
        backup_file,
        started_at,
        status
    ) VALUES (
        'automated_recovery',
        latest_backup,
        NOW(),
        'started'
    );
    
    -- Execute recovery
    SELECT recover_full_database(latest_backup) INTO recovery_success;
    
    -- Update recovery log
    UPDATE disaster_recovery_log
    SET 
        completed_at = NOW(),
        status = CASE WHEN recovery_success THEN 'completed' ELSE 'failed' END
    WHERE scenario = 'automated_recovery'
    AND started_at = (
        SELECT MAX(started_at) 
        FROM disaster_recovery_log 
        WHERE scenario = 'automated_recovery'
    );
    
    RETURN recovery_success;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
```

## 📊 Backup Monitoring

### 1. Backup Health Monitoring

```sql
-- Backup health check function
CREATE OR REPLACE FUNCTION check_backup_health()
RETURNS TABLE(health_status TEXT, details JSONB) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        CASE 
            WHEN COUNT(*) = 0 THEN 'no_backups'
            WHEN MAX(created_at) < NOW() - INTERVAL '24 hours' THEN 'backup_old'
            WHEN COUNT(*) FILTER (WHERE status = 'failed') > 0 THEN 'backup_failed'
            ELSE 'healthy'
        END::TEXT as health_status,
        jsonb_build_object(
            'total_backups', COUNT(*),
            'latest_backup', MAX(created_at),
            'failed_backups', COUNT(*) FILTER (WHERE status = 'failed'),
            'backup_size_gb', ROUND(SUM(backup_size) / 1024.0 / 1024.0 / 1024.0, 2),
            'compression_ratio', AVG(compression_ratio)
        ) as details
    FROM backup_catalog
    WHERE created_at >= NOW() - INTERVAL '7 days';
END;
$$ LANGUAGE plpgsql;
```

### 2. Backup Performance Metrics

```sql
-- Backup performance monitoring
CREATE OR REPLACE FUNCTION monitor_backup_performance()
RETURNS TABLE(metric_name TEXT, metric_value NUMERIC, threshold NUMERIC, status TEXT) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        'backup_duration_minutes'::TEXT,
        AVG(EXTRACT(EPOCH FROM (completed_at - started_at)) / 60)::NUMERIC,
        60.0::NUMERIC, -- 1 hour threshold
        CASE 
            WHEN AVG(EXTRACT(EPOCH FROM (completed_at - started_at)) / 60) > 60 THEN 'warning'
            ELSE 'normal'
        END::TEXT
    FROM backup_log
    WHERE backup_type = 'full'
    AND created_at >= NOW() - INTERVAL '7 days'
    UNION ALL
    SELECT 
        'backup_success_rate'::TEXT,
        (100.0 * COUNT(*) FILTER (WHERE status = 'completed') / COUNT(*))::NUMERIC,
        95.0::NUMERIC, -- 95% threshold
        CASE 
            WHEN (100.0 * COUNT(*) FILTER (WHERE status = 'completed') / COUNT(*)) < 95 THEN 'critical'
            ELSE 'normal'
        END::TEXT
    FROM backup_catalog
    WHERE created_at >= NOW() - INTERVAL '30 days';
END;
$$ LANGUAGE plpgsql;
```

## 🧪 Backup Testing

### 1. Automated Backup Testing

```sql
-- Automated backup testing function
CREATE OR REPLACE FUNCTION test_backup_recovery(backup_file TEXT)
RETURNS BOOLEAN AS $$
DECLARE
    test_db_name TEXT;
    test_success BOOLEAN;
    data_integrity_check BOOLEAN;
BEGIN
    test_db_name := 'test_recovery_' || to_char(NOW(), 'YYYYMMDD_HH24MISS');
    
    -- Create test database
    CREATE DATABASE test_db_name;
    
    BEGIN
        -- Restore backup to test database
        PERFORM pg_restore(
            test_db_name,
            backup_file,
            '--verbose',
            '--no-password'
        );
        
        -- Test data integrity
        SELECT COUNT(*) > 0 INTO data_integrity_check
        FROM (
            SELECT COUNT(*) as user_count FROM users
            UNION ALL
            SELECT COUNT(*) as camera_count FROM cameras
            UNION ALL
            SELECT COUNT(*) as result_count FROM counting_results
        ) integrity_check;
        
        test_success := data_integrity_check;
        
    EXCEPTION WHEN OTHERS THEN
        test_success := FALSE;
    END;
    
    -- Clean up test database
    DROP DATABASE IF EXISTS test_db_name;
    
    -- Log test results
    INSERT INTO backup_test_log (
        backup_file,
        test_result,
        test_date,
        notes
    ) VALUES (
        backup_file,
        test_success,
        NOW(),
        CASE 
            WHEN test_success THEN 'Backup recovery test passed'
            ELSE 'Backup recovery test failed'
        END
    );
    
    RETURN test_success;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
```

### 2. Scheduled Testing

```javascript
// Backup testing schedule
const backupTestingSchedule = {
  daily: {
    time: '03:00', // 3 AM
    tests: [
      'verify_backup_integrity',
      'check_backup_size',
      'validate_checksums'
    ]
  },
  weekly: {
    day: 'sunday',
    time: '04:00', // 4 AM
    tests: [
      'full_recovery_test',
      'point_in_time_recovery_test',
      'performance_validation'
    ]
  },
  monthly: {
    day: 1,
    time: '05:00', // 5 AM
    tests: [
      'disaster_recovery_drill',
      'cross_region_recovery_test',
      'compliance_audit'
    ]
  }
};
```

---

**Tài liệu này cung cấp hướng dẫn chi tiết về backup và recovery database cho AI Camera Counting System, bao gồm backup strategy, recovery procedures, disaster recovery, và testing procedures.** 