# Migration Strategy Document - AI Camera Counting System

## 📊 Tổng quan

Tài liệu này cung cấp chiến lược migration database chi tiết cho hệ thống AI Camera Counting, bao gồm schema migration, data migration, zero-downtime deployment, rollback strategy, và testing procedures.

## 🎯 Mục tiêu migration

- **Zero Downtime**: Không gián đoạn service trong quá trình migration
- **Data Integrity**: Đảm bảo tính toàn vẹn dữ liệu 100%
- **Rollback Capability**: Có thể rollback nhanh chóng nếu có vấn đề
- **Performance**: Không ảnh hưởng đến hiệu năng hệ thống
- **Testing**: Validation đầy đủ trước và sau migration

## 🏗️ Migration Architecture

### Migration Strategy Overview

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              MIGRATION STRATEGY OVERVIEW                        │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              PREPARATION PHASE                              │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Schema    │  │   Data      │  │   Backup    │  │   Testing   │        │ │
│  │  │   Analysis  │  │   Analysis  │  │   Strategy  │  │   Environment│        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                             │
│                                    ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              EXECUTION PHASE                                │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Schema    │  │   Data      │  │   Index     │  │   Validation│        │ │
│  │  │   Migration │  │   Migration │  │   Creation  │  │   & Testing │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                             │
│                                    ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              VERIFICATION PHASE                             │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Data      │  │   Performance│  │   Application│  │   Rollback  │        │ │
│  │  │   Integrity │  │   Testing   │  │   Testing   │  │   Preparation│        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Zero-Downtime Migration Flow

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              ZERO-DOWNTIME MIGRATION FLOW                       │
│                                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐      │
│  │   Primary   │    │   Migration │    │   Validation│    │   Switch    │      │
│  │   Database  │    │   Database  │    │   & Testing │    │   Traffic   │      │
│  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘      │
│         │                   │                   │                   │          │
│         │ 1. Create         │                   │                   │          │
│         │ Migration DB      │                   │                   │          │
│         │──────────────────►│                   │                   │          │
│         │                   │                   │                   │          │
│         │                   │ 2. Apply Schema   │                   │          │
│         │                   │ Changes           │                   │          │
│         │                   │──────────────────►│                   │          │
│         │                   │                   │                   │          │
│         │                   │                   │ 3. Sync Data      │          │
│         │                   │                   │ (Replication)     │          │
│         │                   │                   │──────────────────►│          │
│         │                   │                   │                   │          │
│         │                   │                   │ 4. Validate       │          │
│         │                   │                   │ Data Integrity    │          │
│         │                   │                   │◄──────────────────┤          │
│         │                   │                   │                   │          │
│         │                   │                   │ 5. Performance    │          │
│         │                   │                   │ Testing           │          │
│         │                   │                   │◄──────────────────┤          │
│         │                   │                   │                   │          │
│         │                   │                   │ 6. Switch         │          │
│         │                   │                   │ Traffic           │          │
│         │                   │                   │◄──────────────────┤          │
│         │                   │                   │                   │          │
│         │ 7. Monitor        │                   │                   │          │
│         │ & Validate        │                   │                   │          │
│         │◄──────────────────┤                   │                   │          │
│         │                   │                   │                   │          │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 📋 Migration Types

### 1. Schema Migration

**Mục đích**: Thay đổi cấu trúc database mà không ảnh hưởng đến dữ liệu.

#### Safe Schema Changes

```sql
-- Safe operations (can be done online)
-- Adding columns with default values
ALTER TABLE cameras ADD COLUMN new_feature BOOLEAN DEFAULT false;

-- Adding indexes
CREATE INDEX CONCURRENTLY idx_cameras_new_feature ON cameras(new_feature);

-- Adding constraints (if data is valid)
ALTER TABLE counting_results ADD CONSTRAINT check_positive_count 
CHECK (count_in >= 0 AND count_out >= 0);

-- Renaming columns
ALTER TABLE users RENAME COLUMN old_column TO new_column;

-- Adding foreign keys (if data is valid)
ALTER TABLE zones ADD CONSTRAINT fk_zones_camera 
FOREIGN KEY (camera_id) REFERENCES cameras(id);
```

#### Breaking Schema Changes

```sql
-- Breaking changes (require careful planning)
-- Removing columns
ALTER TABLE cameras DROP COLUMN deprecated_column;

-- Changing column types
ALTER TABLE counting_results ALTER COLUMN confidence TYPE DECIMAL(6,5);

-- Removing constraints
ALTER TABLE counting_results DROP CONSTRAINT old_constraint;

-- Changing table structure
ALTER TABLE analytics DROP COLUMN old_metric;
ALTER TABLE analytics ADD COLUMN new_metric JSONB;
```

### 2. Data Migration

**Mục đích**: Di chuyển hoặc transform dữ liệu giữa các bảng hoặc databases.

#### Batch Data Migration

```sql
-- Batch migration function
CREATE OR REPLACE FUNCTION migrate_camera_data_batch(
    batch_size INTEGER DEFAULT 1000,
    offset_val INTEGER DEFAULT 0
)
RETURNS INTEGER AS $$
DECLARE
    migrated_count INTEGER;
    total_count INTEGER;
BEGIN
    -- Get total count
    SELECT COUNT(*) INTO total_count FROM cameras_old;
    
    -- Migrate batch
    INSERT INTO cameras (
        name, description, ip_address, port, rtsp_url,
        username, password, model, manufacturer,
        resolution_width, resolution_height, fps,
        status, is_active, config, created_at, updated_at
    )
    SELECT 
        name, description, ip_address, port, rtsp_url,
        username, password, model, manufacturer,
        resolution_width, resolution_height, fps,
        status, is_active, config, created_at, updated_at
    FROM cameras_old
    ORDER BY id
    LIMIT batch_size OFFSET offset_val;
    
    GET DIAGNOSTICS migrated_count = ROW_COUNT;
    
    -- Log migration progress
    INSERT INTO migration_log (
        migration_type,
        batch_number,
        records_migrated,
        total_records,
        status,
        started_at,
        completed_at
    ) VALUES (
        'camera_data_migration',
        (offset_val / batch_size) + 1,
        migrated_count,
        total_count,
        'completed',
        NOW(),
        NOW()
    );
    
    RETURN migrated_count;
END;
$$ LANGUAGE plpgsql;
```

#### Real-time Data Migration

```sql
-- Real-time migration using triggers
CREATE OR REPLACE FUNCTION sync_camera_changes()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO cameras_new (
            id, name, description, ip_address, port, rtsp_url,
            username, password, model, manufacturer,
            resolution_width, resolution_height, fps,
            status, is_active, config, created_at, updated_at
        ) VALUES (
            NEW.id, NEW.name, NEW.description, NEW.ip_address, NEW.port, NEW.rtsp_url,
            NEW.username, NEW.password, NEW.model, NEW.manufacturer,
            NEW.resolution_width, NEW.resolution_height, NEW.fps,
            NEW.status, NEW.is_active, NEW.config, NEW.created_at, NEW.updated_at
        );
        RETURN NEW;
    ELSIF TG_OP = 'UPDATE' THEN
        UPDATE cameras_new SET
            name = NEW.name,
            description = NEW.description,
            ip_address = NEW.ip_address,
            port = NEW.port,
            rtsp_url = NEW.rtsp_url,
            username = NEW.username,
            password = NEW.password,
            model = NEW.model,
            manufacturer = NEW.manufacturer,
            resolution_width = NEW.resolution_width,
            resolution_height = NEW.resolution_height,
            fps = NEW.fps,
            status = NEW.status,
            is_active = NEW.is_active,
            config = NEW.config,
            updated_at = NEW.updated_at
        WHERE id = NEW.id;
        RETURN NEW;
    ELSIF TG_OP = 'DELETE' THEN
        DELETE FROM cameras_new WHERE id = OLD.id;
        RETURN OLD;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- Create trigger for real-time sync
CREATE TRIGGER sync_cameras_trigger
    AFTER INSERT OR UPDATE OR DELETE ON cameras
    FOR EACH ROW
    EXECUTE FUNCTION sync_camera_changes();
```

## 🔄 Migration Tools & Scripts

### 1. Migration Management System

```sql
-- Migration tracking table
CREATE TABLE IF NOT EXISTS migrations (
    id SERIAL PRIMARY KEY,
    migration_name VARCHAR(255) NOT NULL UNIQUE,
    version VARCHAR(50) NOT NULL,
    description TEXT,
    sql_file VARCHAR(255),
    checksum VARCHAR(64),
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    applied_by VARCHAR(100),
    execution_time INTERVAL,
    status migration_status DEFAULT 'pending',
    rollback_sql TEXT,
    dependencies INTEGER[]
);

-- Migration status enum
DO $$ BEGIN
    CREATE TYPE migration_status AS ENUM ('pending', 'running', 'completed', 'failed', 'rolled_back');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- Migration log table
CREATE TABLE IF NOT EXISTS migration_log (
    id SERIAL PRIMARY KEY,
    migration_id INTEGER REFERENCES migrations(id),
    log_level log_level DEFAULT 'info',
    message TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    execution_time INTERVAL,
    error_details JSONB
);

-- Log level enum
DO $$ BEGIN
    CREATE TYPE log_level AS ENUM ('debug', 'info', 'warning', 'error', 'critical');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;
```

### 2. Migration Scripts

```javascript
// Migration runner script
class DatabaseMigration {
  constructor(config) {
    this.config = config;
    this.connection = null;
  }

  async connect() {
    this.connection = await pg.connect(this.config);
  }

  async runMigration(migrationName, sqlFile) {
    try {
      console.log(`Starting migration: ${migrationName}`);
      
      // Record migration start
      await this.recordMigrationStart(migrationName);
      
      // Read and execute SQL file
      const sql = fs.readFileSync(sqlFile, 'utf8');
      const startTime = Date.now();
      
      await this.connection.query('BEGIN');
      await this.connection.query(sql);
      await this.connection.query('COMMIT');
      
      const executionTime = Date.now() - startTime;
      
      // Record migration completion
      await this.recordMigrationComplete(migrationName, executionTime);
      
      console.log(`Migration completed: ${migrationName} in ${executionTime}ms`);
      
    } catch (error) {
      await this.connection.query('ROLLBACK');
      await this.recordMigrationError(migrationName, error);
      throw error;
    }
  }

  async recordMigrationStart(migrationName) {
    await this.connection.query(`
      INSERT INTO migrations (migration_name, status, applied_at)
      VALUES ($1, 'running', NOW())
      ON CONFLICT (migration_name) 
      DO UPDATE SET status = 'running', applied_at = NOW()
    `, [migrationName]);
  }

  async recordMigrationComplete(migrationName, executionTime) {
    await this.connection.query(`
      UPDATE migrations 
      SET status = 'completed', execution_time = $2
      WHERE migration_name = $1
    `, [migrationName, `${executionTime}ms`]);
  }

  async recordMigrationError(migrationName, error) {
    await this.connection.query(`
      UPDATE migrations 
      SET status = 'failed'
      WHERE migration_name = $1
    `, [migrationName]);
    
    await this.connection.query(`
      INSERT INTO migration_log (migration_id, log_level, message, error_details)
      SELECT id, 'error', $2, $3
      FROM migrations WHERE migration_name = $1
    `, [migrationName, error.message, JSON.stringify(error)]);
  }
}
```

## 🔍 Testing & Validation

### 1. Pre-Migration Testing

```sql
-- Data integrity validation
CREATE OR REPLACE FUNCTION validate_data_integrity()
RETURNS TABLE(table_name TEXT, record_count BIGINT, checksum TEXT) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        'users'::TEXT as table_name,
        COUNT(*)::BIGINT as record_count,
        MD5(string_agg(id::text || username || email, '')) as checksum
    FROM users
    UNION ALL
    SELECT 
        'cameras'::TEXT,
        COUNT(*)::BIGINT,
        MD5(string_agg(id::text || name || ip_address, ''))
    FROM cameras
    UNION ALL
    SELECT 
        'counting_results'::TEXT,
        COUNT(*)::BIGINT,
        MD5(string_agg(id::text || camera_id::text || timestamp::text, ''))
    FROM counting_results;
END;
$$ LANGUAGE plpgsql;

-- Performance baseline
CREATE OR REPLACE FUNCTION measure_performance_baseline()
RETURNS TABLE(metric_name TEXT, metric_value NUMERIC) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        'avg_query_time'::TEXT,
        AVG(total_time)::NUMERIC
    FROM pg_stat_statements
    WHERE query LIKE '%counting_results%'
    UNION ALL
    SELECT 
        'cache_hit_ratio'::TEXT,
        (100.0 * sum(heap_blks_hit) / (sum(heap_blks_hit) + sum(heap_blks_read)))::NUMERIC
    FROM pg_statio_user_tables
    WHERE relname = 'counting_results';
END;
$$ LANGUAGE plpgsql;
```

### 2. Post-Migration Validation

```sql
-- Post-migration validation function
CREATE OR REPLACE FUNCTION validate_migration_success()
RETURNS BOOLEAN AS $$
DECLARE
    data_matches BOOLEAN;
    performance_ok BOOLEAN;
    constraints_valid BOOLEAN;
BEGIN
    -- Check data integrity
    SELECT COUNT(*) = 0 INTO data_matches
    FROM (
        SELECT COUNT(*) as old_count FROM cameras_old
        UNION ALL
        SELECT COUNT(*) as new_count FROM cameras_new
    ) counts
    WHERE old_count != new_count;
    
    -- Check performance
    SELECT AVG(total_time) < 1000 INTO performance_ok
    FROM pg_stat_statements
    WHERE query LIKE '%counting_results%'
    AND calls > 10;
    
    -- Check constraints
    SELECT COUNT(*) = 0 INTO constraints_valid
    FROM information_schema.table_constraints tc
    WHERE tc.table_name = 'cameras_new'
    AND tc.constraint_type = 'FOREIGN KEY'
    AND NOT EXISTS (
        SELECT 1 FROM information_schema.table_constraints 
        WHERE table_name = 'cameras_old' 
        AND constraint_name = tc.constraint_name
    );
    
    RETURN data_matches AND performance_ok AND constraints_valid;
END;
$$ LANGUAGE plpgsql;
```

## 🔄 Rollback Strategy

### 1. Rollback Preparation

```sql
-- Rollback preparation function
CREATE OR REPLACE FUNCTION prepare_rollback()
RETURNS void AS $$
BEGIN
    -- Create backup of current state
    PERFORM pg_dump(
        'ai_camera_counting_db',
        '--format=custom',
        '--file=/backups/pre_migration_backup_' || to_char(NOW(), 'YYYYMMDD_HH24MISS') || '.sql'
    );
    
    -- Create rollback scripts
    INSERT INTO migration_rollback_scripts (
        migration_name,
        rollback_sql,
        created_at
    ) VALUES (
        'camera_schema_migration',
        'ALTER TABLE cameras DROP COLUMN new_feature;',
        NOW()
    );
    
    -- Log rollback preparation
    INSERT INTO migration_log (
        migration_id,
        log_level,
        message
    ) VALUES (
        (SELECT id FROM migrations WHERE migration_name = 'camera_schema_migration'),
        'info',
        'Rollback preparation completed'
    );
END;
$$ LANGUAGE plpgsql;
```

### 2. Automated Rollback

```sql
-- Automated rollback function
CREATE OR REPLACE FUNCTION execute_rollback(migration_name_param TEXT)
RETURNS BOOLEAN AS $$
DECLARE
    rollback_sql TEXT;
    migration_record RECORD;
BEGIN
    -- Get migration details
    SELECT * INTO migration_record
    FROM migrations
    WHERE migration_name = migration_name_param;
    
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Migration % not found', migration_name_param;
    END IF;
    
    -- Get rollback SQL
    SELECT rollback_sql INTO rollback_sql
    FROM migration_rollback_scripts
    WHERE migration_name = migration_name_param
    ORDER BY created_at DESC
    LIMIT 1;
    
    IF rollback_sql IS NULL THEN
        RAISE EXCEPTION 'No rollback script found for migration %', migration_name_param;
    END IF;
    
    -- Execute rollback
    BEGIN
        EXECUTE rollback_sql;
        
        -- Update migration status
        UPDATE migrations
        SET status = 'rolled_back'
        WHERE migration_name = migration_name_param;
        
        -- Log rollback
        INSERT INTO migration_log (
            migration_id,
            log_level,
            message
        ) VALUES (
            migration_record.id,
            'info',
            'Rollback executed successfully'
        );
        
        RETURN TRUE;
        
    EXCEPTION WHEN OTHERS THEN
        -- Log rollback failure
        INSERT INTO migration_log (
            migration_id,
            log_level,
            message,
            error_details
        ) VALUES (
            migration_record.id,
            'error',
            'Rollback failed: ' || SQLERRM,
            jsonb_build_object('error', SQLERRM, 'sql_state', SQLSTATE)
        );
        
        RETURN FALSE;
    END;
END;
$$ LANGUAGE plpgsql;
```

## 📊 Migration Monitoring

### 1. Migration Progress Tracking

```sql
-- Migration progress view
CREATE VIEW migration_progress AS
SELECT 
    m.migration_name,
    m.version,
    m.status,
    m.applied_at,
    m.execution_time,
    COUNT(ml.id) as log_entries,
    MAX(ml.timestamp) as last_activity
FROM migrations m
LEFT JOIN migration_log ml ON m.id = ml.migration_id
GROUP BY m.id, m.migration_name, m.version, m.status, m.applied_at, m.execution_time
ORDER BY m.applied_at DESC;

-- Migration health check
CREATE OR REPLACE FUNCTION check_migration_health()
RETURNS TABLE(health_status TEXT, details JSONB) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        CASE 
            WHEN COUNT(*) = 0 THEN 'healthy'
            WHEN COUNT(*) FILTER (WHERE status = 'failed') > 0 THEN 'failed'
            WHEN COUNT(*) FILTER (WHERE status = 'running') > 0 THEN 'running'
            ELSE 'completed'
        END::TEXT as health_status,
        jsonb_build_object(
            'total_migrations', COUNT(*),
            'completed', COUNT(*) FILTER (WHERE status = 'completed'),
            'failed', COUNT(*) FILTER (WHERE status = 'failed'),
            'running', COUNT(*) FILTER (WHERE status = 'running'),
            'pending', COUNT(*) FILTER (WHERE status = 'pending')
        ) as details
    FROM migrations;
END;
$$ LANGUAGE plpgsql;
```

### 2. Performance Monitoring

```sql
-- Migration performance monitoring
CREATE OR REPLACE FUNCTION monitor_migration_performance()
RETURNS TABLE(metric_name TEXT, metric_value NUMERIC, threshold NUMERIC, status TEXT) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        'migration_duration'::TEXT,
        AVG(EXTRACT(EPOCH FROM execution_time))::NUMERIC,
        300.0::NUMERIC, -- 5 minutes threshold
        CASE 
            WHEN AVG(EXTRACT(EPOCH FROM execution_time)) > 300 THEN 'warning'
            ELSE 'normal'
        END::TEXT
    FROM migrations
    WHERE status = 'completed'
    AND applied_at >= NOW() - INTERVAL '24 hours'
    UNION ALL
    SELECT 
        'failed_migrations'::TEXT,
        COUNT(*)::NUMERIC,
        0.0::NUMERIC,
        CASE 
            WHEN COUNT(*) > 0 THEN 'critical'
            ELSE 'normal'
        END::TEXT
    FROM migrations
    WHERE status = 'failed'
    AND applied_at >= NOW() - INTERVAL '24 hours';
END;
$$ LANGUAGE plpgsql;
```

## 🚀 Deployment Strategy

### 1. Blue-Green Deployment

```javascript
// Blue-Green deployment configuration
const blueGreenConfig = {
  blue: {
    database: 'ai_camera_counting_db_blue',
    application: 'ai-camera-api-blue',
    loadBalancer: 'blue-pool'
  },
  green: {
    database: 'ai_camera_counting_db_green',
    application: 'ai-camera-api-green',
    loadBalancer: 'green-pool'
  },
  
  migration: {
    steps: [
      'backup_blue_database',
      'create_green_database',
      'apply_migrations_to_green',
      'sync_data_to_green',
      'validate_green_database',
      'switch_traffic_to_green',
      'monitor_green_performance',
      'decommission_blue_database'
    ],
    
    rollback: {
      steps: [
        'switch_traffic_back_to_blue',
        'decommission_green_database'
      ]
    }
  }
};
```

### 2. Canary Deployment

```javascript
// Canary deployment configuration
const canaryConfig = {
  stages: [
    {
      name: 'internal_testing',
      traffic_percentage: 0,
      duration: '1 hour',
      metrics: ['error_rate', 'response_time', 'throughput']
    },
    {
      name: 'alpha_testing',
      traffic_percentage: 5,
      duration: '2 hours',
      metrics: ['error_rate', 'response_time', 'user_satisfaction']
    },
    {
      name: 'beta_testing',
      traffic_percentage: 20,
      duration: '4 hours',
      metrics: ['error_rate', 'response_time', 'business_metrics']
    },
    {
      name: 'production_rollout',
      traffic_percentage: 100,
      duration: '1 hour',
      metrics: ['error_rate', 'response_time', 'system_health']
    }
  ],
  
  rollback_triggers: {
    error_rate_threshold: 0.05, // 5%
    response_time_threshold: 1000, // 1 second
    user_complaints_threshold: 10
  }
};
```

---

**Tài liệu này cung cấp chiến lược migration database chi tiết cho AI Camera Counting System, bao gồm schema migration, data migration, zero-downtime deployment, rollback strategy, và testing procedures.** 