# Production Deployment & CI/CD - AI Camera Counting System

## 📊 Tổng quan

Tài liệu này trình bày chiến lược deployment và CI/CD cho database trong môi trường production, bao gồm automation, blue-green deployment, rollback procedures và environment management.

## 🎯 Deployment Objectives

- **Automation**: Tự động hóa toàn bộ quá trình deployment
- **Reliability**: Đảm bảo deployment an toàn và ổn định
- **Speed**: Giảm thời gian deployment và time-to-market
- **Rollback**: Khả năng rollback nhanh chóng khi có vấn đề
- **Monitoring**: Theo dõi quá trình deployment và health checks

## 🏗️ CI/CD Architecture

### Multi-Stage CI/CD Pipeline

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              CI/CD PIPELINE ARCHITECTURE                        │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              DEVELOPMENT STAGE                              │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Code      │  │   Unit      │  │   Integration│  │   Code      │        │ │
│  │  │   Commit    │  │   Tests     │  │   Tests     │  │   Review    │        │ │
│  │  │             │  │             │  │             │  │             │        │ │
│  │  │ • Git       │  │ • Database  │  │ • API       │  │ • Peer      │        │ │
│  │  │   Push      │  │   Functions │  │   Tests     │  │   Review    │        │ │
│  │  │ • Branch    │  │ • Stored    │  │ • Cache     │  │ • Security  │        │ │
│  │  │   Creation  │  │   Procedures│  │   Tests     │  │   Scan      │        │ │
│  │  │ • Trigger   │  │ • Trigger   │  │ • Queue     │  │ • Quality   │        │ │
│  │  │   Pipeline  │  │   Tests     │  │   Tests     │  │   Gates     │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                             │
│                                    ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              STAGING STAGE                                  │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Build     │  │   Deploy    │  │   Test      │  │   Validate  │        │ │
│  │  │   Database  │  │   to        │  │   Staging   │  │   Staging   │        │ │
│  │  │   Schema    │  │   Staging   │  │   Environment│  │   Environment│       │ │
│  │  │             │  │             │  │             │  │             │        │ │
│  │  │ • Schema    │  │ • Database  │  │ • End-to-   │  │ • Performance│        │ │
│  │  │   Migration │  │   Provision │  │   End Tests │  │   Tests     │        │ │
│  │  │ • Data      │  │ • Schema    │  │ • Load      │  │ • Security  │        │ │
│  │  │   Seeding   │  │   Update    │  │   Tests     │  │   Tests     │        │ │
│  │  │ • Index     │  │ • Data      │  │ • User      │  │ • Compliance│        │ │
│  │  │   Creation  │  │   Migration │  │   Acceptance│  │   Checks    │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                             │
│                                    ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              PRODUCTION STAGE                               │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Blue-Green│  │   Health    │  │   Traffic   │  │   Rollback  │        │ │
│  │  │   Deployment│  │   Checks    │  │   Switch    │  │   Procedures│        │ │
│  │  │             │  │             │  │             │  │             │        │ │
│  │  │ • Database  │  │ • Database  │  │ • Load      │  │ • Automatic │        │ │
│  │  │   Copy      │  │   Health    │  │   Balancer  │  │   Rollback  │        │ │
│  │  │ • Schema    │  │   Monitoring│  │   Switch    │  │ • Manual    │        │ │
│  │  │   Migration │  │ • Performance│  │ • DNS       │  │   Rollback  │        │ │
│  │  │ • Data      │  │   Monitoring│  │   Update    │  │ • Data      │        │ │
│  │  │   Sync      │  │ • Alerting  │  │ • Cache     │  │   Recovery  │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 🔧 Database Deployment Automation

### Schema Migration Management

```sql
-- Migration management tables
CREATE TABLE deployment_migrations (
    id SERIAL PRIMARY KEY,
    migration_name VARCHAR(200) NOT NULL,
    migration_version VARCHAR(50) NOT NULL,
    migration_type VARCHAR(20) NOT NULL, -- schema, data, index, function
    migration_sql TEXT NOT NULL,
    rollback_sql TEXT,
    dependencies TEXT[],
    is_applied BOOLEAN DEFAULT FALSE,
    applied_at TIMESTAMP,
    applied_by VARCHAR(100),
    execution_time_ms INTEGER,
    status VARCHAR(20) DEFAULT 'pending', -- pending, running, completed, failed, rolled_back
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Migration execution log
CREATE TABLE deployment_execution_logs (
    id SERIAL PRIMARY KEY,
    deployment_id VARCHAR(100) NOT NULL,
    migration_id INTEGER REFERENCES deployment_migrations(id),
    execution_step VARCHAR(50) NOT NULL,
    step_status VARCHAR(20) NOT NULL, -- started, completed, failed
    step_duration_ms INTEGER,
    step_output TEXT,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Define migration templates
INSERT INTO deployment_migrations VALUES
(1, 'create_initial_schema', '1.0.0', 'schema',
 'CREATE TABLE IF NOT EXISTS cameras (
    id SERIAL PRIMARY KEY,
    camera_name VARCHAR(100) NOT NULL,
    location VARCHAR(255),
    status VARCHAR(20) DEFAULT ''active'',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);',
 'DROP TABLE IF EXISTS cameras;',
 ARRAY[]::TEXT[],
 FALSE, NULL, NULL, 'pending', NULL, NOW()),

(2, 'add_camera_metadata', '1.1.0', 'schema',
 'ALTER TABLE cameras ADD COLUMN IF NOT EXISTS metadata JSONB DEFAULT ''{}''::jsonb;',
 'ALTER TABLE cameras DROP COLUMN IF EXISTS metadata;',
 ARRAY['create_initial_schema'],
 FALSE, NULL, NULL, 'pending', NULL, NOW()),

(3, 'create_counting_results_table', '1.2.0', 'schema',
 'CREATE TABLE IF NOT EXISTS counting_results (
    id SERIAL PRIMARY KEY,
    camera_id INTEGER REFERENCES cameras(id),
    count_type VARCHAR(50) NOT NULL,
    count_value INTEGER NOT NULL,
    confidence_score DECIMAL(5,4),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);',
 'DROP TABLE IF EXISTS counting_results;',
 ARRAY['create_initial_schema'],
 FALSE, NULL, NULL, 'pending', NULL, NOW()),

(4, 'add_performance_indexes', '1.3.0', 'index',
 'CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_counting_results_camera_time 
  ON counting_results(camera_id, created_at DESC);',
 'DROP INDEX IF EXISTS idx_counting_results_camera_time;',
 ARRAY['create_counting_results_table'],
 FALSE, NULL, NULL, 'pending', NULL, NOW());

-- Migration execution function
CREATE OR REPLACE FUNCTION execute_migration(
    p_migration_id INTEGER,
    p_deployment_id VARCHAR(100)
)
RETURNS BOOLEAN AS $$
DECLARE
    migration_record RECORD;
    start_time TIMESTAMP;
    end_time TIMESTAMP;
    execution_time INTEGER;
BEGIN
    -- Get migration details
    SELECT * INTO migration_record
    FROM deployment_migrations
    WHERE id = p_migration_id AND is_applied = FALSE;
    
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Migration not found or already applied: %', p_migration_id;
    END IF;
    
    -- Check dependencies
    IF migration_record.dependencies IS NOT NULL THEN
        FOR i IN 1..array_length(migration_record.dependencies, 1) LOOP
            IF NOT EXISTS (
                SELECT 1 FROM deployment_migrations 
                WHERE migration_name = migration_record.dependencies[i] 
                AND is_applied = TRUE
            ) THEN
                RAISE EXCEPTION 'Dependency not met: %', migration_record.dependencies[i];
            END IF;
        END LOOP;
    END IF;
    
    -- Log execution start
    INSERT INTO deployment_execution_logs (deployment_id, migration_id, execution_step, step_status)
    VALUES (p_deployment_id, p_migration_id, 'migration_start', 'started');
    
    -- Update migration status
    UPDATE deployment_migrations 
    SET status = 'running', applied_at = NOW()
    WHERE id = p_migration_id;
    
    start_time := clock_timestamp();
    
    -- Execute migration
    BEGIN
        EXECUTE migration_record.migration_sql;
        
        end_time := clock_timestamp();
        execution_time := EXTRACT(EPOCH FROM (end_time - start_time)) * 1000;
        
        -- Update migration as completed
        UPDATE deployment_migrations 
        SET is_applied = TRUE,
            status = 'completed',
            execution_time_ms = execution_time,
            applied_by = current_user
        WHERE id = p_migration_id;
        
        -- Log successful execution
        INSERT INTO deployment_execution_logs (
            deployment_id, migration_id, execution_step, step_status, step_duration_ms
        ) VALUES (
            p_deployment_id, p_migration_id, 'migration_complete', 'completed', execution_time
        );
        
        RETURN TRUE;
        
    EXCEPTION
        WHEN OTHERS THEN
            end_time := clock_timestamp();
            execution_time := EXTRACT(EPOCH FROM (end_time - start_time)) * 1000;
            
            -- Update migration as failed
            UPDATE deployment_migrations 
            SET status = 'failed',
                error_message = SQLERRM,
                execution_time_ms = execution_time
            WHERE id = p_migration_id;
            
            -- Log failed execution
            INSERT INTO deployment_execution_logs (
                deployment_id, migration_id, execution_step, step_status, 
                step_duration_ms, error_message
            ) VALUES (
                p_deployment_id, p_migration_id, 'migration_failed', 'failed', 
                execution_time, SQLERRM
            );
            
            RETURN FALSE;
    END;
END;
$$ LANGUAGE plpgsql;
```

### Automated Deployment Pipeline

```sql
-- Deployment pipeline management
CREATE TABLE deployment_pipelines (
    id SERIAL PRIMARY KEY,
    pipeline_name VARCHAR(100) NOT NULL,
    pipeline_version VARCHAR(50) NOT NULL,
    environment VARCHAR(20) NOT NULL, -- dev, staging, production
    status VARCHAR(20) DEFAULT 'pending', -- pending, running, completed, failed, rolled_back
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    triggered_by VARCHAR(100),
    git_commit_hash VARCHAR(50),
    git_branch VARCHAR(100),
    deployment_config JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Pipeline stages
CREATE TABLE deployment_stages (
    id SERIAL PRIMARY KEY,
    pipeline_id INTEGER REFERENCES deployment_pipelines(id),
    stage_name VARCHAR(100) NOT NULL,
    stage_order INTEGER NOT NULL,
    stage_type VARCHAR(50) NOT NULL, -- build, test, deploy, validate, rollback
    status VARCHAR(20) DEFAULT 'pending', -- pending, running, completed, failed, skipped
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    duration_ms INTEGER,
    stage_config JSONB,
    stage_output TEXT,
    error_message TEXT
);

-- Pipeline execution function
CREATE OR REPLACE FUNCTION execute_deployment_pipeline(
    p_pipeline_name VARCHAR(100),
    p_environment VARCHAR(20),
    p_git_commit_hash VARCHAR(50),
    p_git_branch VARCHAR(100)
)
RETURNS INTEGER AS $$
DECLARE
    pipeline_id INTEGER;
    stage_record RECORD;
    stage_start TIMESTAMP;
    stage_end TIMESTAMP;
    stage_duration INTEGER;
BEGIN
    -- Create pipeline record
    INSERT INTO deployment_pipelines (
        pipeline_name, pipeline_version, environment, status, 
        started_at, triggered_by, git_commit_hash, git_branch
    ) VALUES (
        p_pipeline_name, '1.0.0', p_environment, 'running',
        NOW(), current_user, p_git_commit_hash, p_git_branch
    ) RETURNING id INTO pipeline_id;
    
    -- Define pipeline stages
    INSERT INTO deployment_stages (pipeline_id, stage_name, stage_order, stage_type, stage_config)
    VALUES 
        (pipeline_id, 'Build Database Schema', 1, 'build', 
         '{"migrations": ["create_initial_schema", "add_camera_metadata", "create_counting_results_table"]}'),
        (pipeline_id, 'Run Unit Tests', 2, 'test', 
         '{"test_suites": ["user_management", "camera_management", "counting_results"]}'),
        (pipeline_id, 'Deploy to Environment', 3, 'deploy', 
         '{"target_environment": "' || p_environment || '", "deployment_strategy": "blue_green"}'),
        (pipeline_id, 'Health Checks', 4, 'validate', 
         '{"health_checks": ["database_connectivity", "api_endpoints", "performance_metrics"]}'),
        (pipeline_id, 'Integration Tests', 5, 'test', 
         '{"test_suites": ["api_integration", "cache_integration", "queue_integration"]}');
    
    -- Execute stages sequentially
    FOR stage_record IN 
        SELECT * FROM deployment_stages 
        WHERE pipeline_id = pipeline_id 
        ORDER BY stage_order
    LOOP
        -- Update stage status
        UPDATE deployment_stages 
        SET status = 'running', started_at = NOW()
        WHERE id = stage_record.id;
        
        stage_start := clock_timestamp();
        
        -- Execute stage based on type
        CASE stage_record.stage_type
            WHEN 'build' THEN
                PERFORM execute_build_stage(stage_record.id, stage_record.stage_config);
            WHEN 'test' THEN
                PERFORM execute_test_stage(stage_record.id, stage_record.stage_config);
            WHEN 'deploy' THEN
                PERFORM execute_deploy_stage(stage_record.id, stage_record.stage_config);
            WHEN 'validate' THEN
                PERFORM execute_validate_stage(stage_record.id, stage_record.stage_config);
            ELSE
                RAISE EXCEPTION 'Unknown stage type: %', stage_record.stage_type;
        END CASE;
        
        stage_end := clock_timestamp();
        stage_duration := EXTRACT(EPOCH FROM (stage_end - stage_start)) * 1000;
        
        -- Update stage completion
        UPDATE deployment_stages 
        SET status = 'completed', 
            completed_at = stage_end,
            duration_ms = stage_duration
        WHERE id = stage_record.id;
        
        -- Check if stage failed and handle accordingly
        IF EXISTS (
            SELECT 1 FROM deployment_stages 
            WHERE pipeline_id = pipeline_id AND status = 'failed'
        ) THEN
            -- Update pipeline status
            UPDATE deployment_pipelines 
            SET status = 'failed', completed_at = NOW()
            WHERE id = pipeline_id;
            
            -- Trigger rollback
            PERFORM trigger_pipeline_rollback(pipeline_id);
            
            RETURN pipeline_id;
        END IF;
    END LOOP;
    
    -- Update pipeline as completed
    UPDATE deployment_pipelines 
    SET status = 'completed', completed_at = NOW()
    WHERE id = pipeline_id;
    
    RETURN pipeline_id;
END;
$$ LANGUAGE plpgsql;
```

## 🔄 Blue-Green Deployment

### Blue-Green Deployment Strategy

```sql
-- Blue-green deployment management
CREATE TABLE blue_green_deployments (
    id SERIAL PRIMARY KEY,
    deployment_name VARCHAR(100) NOT NULL,
    blue_environment VARCHAR(100) NOT NULL,
    green_environment VARCHAR(100) NOT NULL,
    current_active VARCHAR(10) DEFAULT 'blue', -- blue, green
    deployment_status VARCHAR(20) DEFAULT 'idle', -- idle, deploying, switching, completed, failed
    blue_database_url VARCHAR(500),
    green_database_url VARCHAR(500),
    switch_started_at TIMESTAMP,
    switch_completed_at TIMESTAMP,
    health_check_results JSONB,
    rollback_triggered BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Blue-green deployment function
CREATE OR REPLACE FUNCTION execute_blue_green_deployment(
    p_deployment_name VARCHAR(100),
    p_new_version VARCHAR(50)
)
RETURNS BOOLEAN AS $$
DECLARE
    deployment_record RECORD;
    inactive_environment VARCHAR(10);
    health_check_result BOOLEAN;
BEGIN
    -- Get current deployment configuration
    SELECT * INTO deployment_record
    FROM blue_green_deployments
    WHERE deployment_name = p_deployment_name;
    
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Blue-green deployment not found: %', p_deployment_name;
    END IF;
    
    -- Determine inactive environment
    inactive_environment := CASE deployment_record.current_active
        WHEN 'blue' THEN 'green'
        WHEN 'green' THEN 'blue'
        ELSE 'blue'
    END;
    
    -- Update deployment status
    UPDATE blue_green_deployments 
    SET deployment_status = 'deploying',
        updated_at = NOW()
    WHERE id = deployment_record.id;
    
    -- Deploy to inactive environment
    PERFORM deploy_to_environment(inactive_environment, p_new_version);
    
    -- Run health checks on new deployment
    health_check_result := perform_health_checks(inactive_environment);
    
    IF NOT health_check_result THEN
        -- Health checks failed, rollback
        UPDATE blue_green_deployments 
        SET deployment_status = 'failed',
            rollback_triggered = TRUE,
            updated_at = NOW()
        WHERE id = deployment_record.id;
        
        RETURN FALSE;
    END IF;
    
    -- Switch traffic to new environment
    UPDATE blue_green_deployments 
    SET deployment_status = 'switching',
        switch_started_at = NOW(),
        updated_at = NOW()
    WHERE id = deployment_record.id;
    
    -- Perform traffic switch
    PERFORM switch_traffic_to_environment(inactive_environment);
    
    -- Update active environment
    UPDATE blue_green_deployments 
    SET current_active = inactive_environment,
        deployment_status = 'completed',
        switch_completed_at = NOW(),
        updated_at = NOW()
    WHERE id = deployment_record.id;
    
    RETURN TRUE;
END;
$$ LANGUAGE plpgsql;

-- Health check function
CREATE OR REPLACE FUNCTION perform_health_checks(p_environment VARCHAR(10))
RETURNS BOOLEAN AS $$
DECLARE
    health_checks JSONB := '[]'::jsonb;
    check_result BOOLEAN;
BEGIN
    -- Database connectivity check
    BEGIN
        PERFORM 1;
        health_checks := health_checks || jsonb_build_object('database_connectivity', 'PASS');
    EXCEPTION
        WHEN OTHERS THEN
            health_checks := health_checks || jsonb_build_object('database_connectivity', 'FAIL');
            RETURN FALSE;
    END;
    
    -- API endpoint check
    BEGIN
        -- Simulate API health check
        PERFORM COUNT(*) FROM cameras WHERE status = 'active';
        health_checks := health_checks || jsonb_build_object('api_endpoints', 'PASS');
    EXCEPTION
        WHEN OTHERS THEN
            health_checks := health_checks || jsonb_build_object('api_endpoints', 'FAIL');
            RETURN FALSE;
    END;
    
    -- Performance check
    BEGIN
        -- Check query performance
        IF EXISTS (
            SELECT 1 FROM pg_stat_statements 
            WHERE mean_time > 5000
            AND query_start > NOW() - INTERVAL '5 minutes'
        ) THEN
            health_checks := health_checks || jsonb_build_object('performance', 'WARNING');
        ELSE
            health_checks := health_checks || jsonb_build_object('performance', 'PASS');
        END IF;
    EXCEPTION
        WHEN OTHERS THEN
            health_checks := health_checks || jsonb_build_object('performance', 'FAIL');
            RETURN FALSE;
    END;
    
    -- Update health check results
    UPDATE blue_green_deployments 
    SET health_check_results = health_checks
    WHERE current_active = p_environment;
    
    -- Return overall health status
    RETURN NOT (health_checks @> '[{"database_connectivity": "FAIL"}, {"api_endpoints": "FAIL"}, {"performance": "FAIL"}]');
END;
$$ LANGUAGE plpgsql;
```

## 🔙 Rollback Procedures

### Automated Rollback System

```sql
-- Rollback management
CREATE TABLE deployment_rollbacks (
    id SERIAL PRIMARY KEY,
    pipeline_id INTEGER REFERENCES deployment_pipelines(id),
    rollback_reason VARCHAR(200) NOT NULL,
    rollback_type VARCHAR(20) NOT NULL, -- automatic, manual, health_check_failure
    previous_version VARCHAR(50),
    target_version VARCHAR(50),
    rollback_status VARCHAR(20) DEFAULT 'pending', -- pending, running, completed, failed
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    rollback_steps JSONB,
    error_message TEXT
);

-- Rollback execution function
CREATE OR REPLACE FUNCTION execute_rollback(
    p_pipeline_id INTEGER,
    p_rollback_reason VARCHAR(200)
)
RETURNS BOOLEAN AS $$
DECLARE
    pipeline_record RECORD;
    rollback_id INTEGER;
    migration_record RECORD;
    rollback_success BOOLEAN := TRUE;
BEGIN
    -- Get pipeline details
    SELECT * INTO pipeline_record
    FROM deployment_pipelines
    WHERE id = p_pipeline_id;
    
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Pipeline not found: %', p_pipeline_id;
    END IF;
    
    -- Create rollback record
    INSERT INTO deployment_rollbacks (
        pipeline_id, rollback_reason, rollback_type, 
        previous_version, target_version, rollback_status
    ) VALUES (
        p_pipeline_id, p_rollback_reason, 'automatic',
        pipeline_record.pipeline_version, 'previous_version', 'running'
    ) RETURNING id INTO rollback_id;
    
    -- Execute rollback migrations in reverse order
    FOR migration_record IN 
        SELECT * FROM deployment_migrations
        WHERE is_applied = TRUE
        AND applied_at >= pipeline_record.started_at
        ORDER BY applied_at DESC
    LOOP
        -- Check if rollback SQL exists
        IF migration_record.rollback_sql IS NOT NULL THEN
            BEGIN
                EXECUTE migration_record.rollback_sql;
                
                -- Update migration status
                UPDATE deployment_migrations 
                SET is_applied = FALSE,
                    status = 'rolled_back',
                    applied_at = NULL
                WHERE id = migration_record.id;
                
            EXCEPTION
                WHEN OTHERS THEN
                    rollback_success := FALSE;
                    
                    -- Log rollback error
                    UPDATE deployment_rollbacks 
                    SET rollback_status = 'failed',
                        error_message = SQLERRM,
                        completed_at = NOW()
                    WHERE id = rollback_id;
                    
                    RETURN FALSE;
            END;
        END IF;
    END LOOP;
    
    -- Update rollback status
    UPDATE deployment_rollbacks 
    SET rollback_status = 'completed',
        completed_at = NOW()
    WHERE id = rollback_id;
    
    -- Update pipeline status
    UPDATE deployment_pipelines 
    SET status = 'rolled_back',
        completed_at = NOW()
    WHERE id = p_pipeline_id;
    
    RETURN rollback_success;
END;
$$ LANGUAGE plpgsql;

-- Automatic rollback trigger
CREATE OR REPLACE FUNCTION trigger_automatic_rollback()
RETURNS TRIGGER AS $$
BEGIN
    -- Check if deployment failed and trigger rollback
    IF NEW.status = 'failed' AND OLD.status = 'running' THEN
        PERFORM execute_rollback(NEW.id, 'Deployment failed - automatic rollback');
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger for automatic rollback
CREATE TRIGGER deployment_failure_rollback
    AFTER UPDATE ON deployment_pipelines
    FOR EACH ROW
    EXECUTE FUNCTION trigger_automatic_rollback();
```

## 🔧 Environment Management

### Environment Configuration

```sql
-- Environment configuration management
CREATE TABLE environment_configs (
    id SERIAL PRIMARY KEY,
    environment_name VARCHAR(50) NOT NULL,
    environment_type VARCHAR(20) NOT NULL, -- development, staging, production
    database_url VARCHAR(500),
    database_name VARCHAR(100),
    database_user VARCHAR(100),
    connection_pool_size INTEGER DEFAULT 10,
    max_connections INTEGER DEFAULT 100,
    backup_schedule VARCHAR(100),
    monitoring_enabled BOOLEAN DEFAULT TRUE,
    alerting_enabled BOOLEAN DEFAULT TRUE,
    config_data JSONB DEFAULT '{}'::jsonb,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Environment-specific configurations
INSERT INTO environment_configs VALUES
(1, 'development', 'development', 
 'postgresql://dev_user:dev_pass@localhost:5432/ai_camera_dev',
 'ai_camera_dev', 'dev_user', 5, 20, 'daily', FALSE, FALSE,
 '{"log_level": "debug", "debug_mode": true}', TRUE),

(2, 'staging', 'staging',
 'postgresql://staging_user:staging_pass@staging-db:5432/ai_camera_staging',
 'ai_camera_staging', 'staging_user', 10, 50, 'daily', TRUE, TRUE,
 '{"log_level": "info", "debug_mode": false}', TRUE),

(3, 'production', 'production',
 'postgresql://prod_user:prod_pass@prod-db:5432/ai_camera_prod',
 'ai_camera_prod', 'prod_user', 20, 200, 'hourly', TRUE, TRUE,
 '{"log_level": "warn", "debug_mode": false, "ssl_mode": "require"}', TRUE);

-- Environment deployment function
CREATE OR REPLACE FUNCTION deploy_to_environment(
    p_environment_name VARCHAR(50),
    p_version VARCHAR(50)
)
RETURNS BOOLEAN AS $$
DECLARE
    env_config RECORD;
    deployment_success BOOLEAN := TRUE;
BEGIN
    -- Get environment configuration
    SELECT * INTO env_config
    FROM environment_configs
    WHERE environment_name = p_environment_name AND is_active = TRUE;
    
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Environment not found or inactive: %', p_environment_name;
    END IF;
    
    -- Log deployment start
    INSERT INTO deployment_execution_logs (
        deployment_id, execution_step, step_status, step_output
    ) VALUES (
        'env_deploy_' || p_environment_name,
        'deploy_start',
        'started',
        'Deploying version ' || p_version || ' to ' || p_environment_name
    );
    
    -- Execute environment-specific deployment steps
    CASE env_config.environment_type
        WHEN 'development' THEN
            -- Development deployment (minimal steps)
            PERFORM deploy_development_environment(env_config, p_version);
            
        WHEN 'staging' THEN
            -- Staging deployment (full testing)
            PERFORM deploy_staging_environment(env_config, p_version);
            
        WHEN 'production' THEN
            -- Production deployment (blue-green)
            PERFORM deploy_production_environment(env_config, p_version);
            
        ELSE
            RAISE EXCEPTION 'Unknown environment type: %', env_config.environment_type;
    END CASE;
    
    -- Log deployment completion
    INSERT INTO deployment_execution_logs (
        deployment_id, execution_step, step_status, step_output
    ) VALUES (
        'env_deploy_' || p_environment_name,
        'deploy_complete',
        'completed',
        'Successfully deployed version ' || p_version || ' to ' || p_environment_name
    );
    
    RETURN deployment_success;
END;
$$ LANGUAGE plpgsql;
```

## 📊 Deployment Monitoring

### Deployment Metrics and Reporting

```sql
-- Deployment metrics view
CREATE VIEW deployment_metrics AS
SELECT 
    environment,
    COUNT(*) as total_deployments,
    COUNT(CASE WHEN status = 'completed' THEN 1 END) as successful_deployments,
    COUNT(CASE WHEN status = 'failed' THEN 1 END) as failed_deployments,
    COUNT(CASE WHEN status = 'rolled_back' THEN 1 END) as rollback_deployments,
    ROUND(
        (COUNT(CASE WHEN status = 'completed' THEN 1 END) * 100.0) / COUNT(*), 2
    ) as success_rate,
    AVG(EXTRACT(EPOCH FROM (completed_at - started_at))) as avg_deployment_time_seconds,
    MAX(EXTRACT(EPOCH FROM (completed_at - started_at))) as max_deployment_time_seconds
FROM deployment_pipelines
WHERE created_at > NOW() - INTERVAL '30 days'
GROUP BY environment
ORDER BY environment;

-- Deployment performance analysis
CREATE VIEW deployment_performance AS
SELECT 
    pipeline_name,
    environment,
    status,
    EXTRACT(EPOCH FROM (completed_at - started_at)) as deployment_duration_seconds,
    CASE 
        WHEN EXTRACT(EPOCH FROM (completed_at - started_at)) < 300 THEN 'FAST'
        WHEN EXTRACT(EPOCH FROM (completed_at - started_at)) < 900 THEN 'NORMAL'
        ELSE 'SLOW'
    END as performance_category,
    triggered_by,
    git_commit_hash,
    git_branch
FROM deployment_pipelines
WHERE completed_at IS NOT NULL
ORDER BY completed_at DESC;

-- Deployment health dashboard
CREATE OR REPLACE FUNCTION get_deployment_health()
RETURNS JSONB AS $$
DECLARE
    health_data JSONB;
BEGIN
    SELECT jsonb_build_object(
        'deployment_health', jsonb_build_object(
            'total_deployments_today', (
                SELECT COUNT(*) FROM deployment_pipelines 
                WHERE created_at > CURRENT_DATE
            ),
            'successful_deployments_today', (
                SELECT COUNT(*) FROM deployment_pipelines 
                WHERE created_at > CURRENT_DATE AND status = 'completed'
            ),
            'failed_deployments_today', (
                SELECT COUNT(*) FROM deployment_pipelines 
                WHERE created_at > CURRENT_DATE AND status = 'failed'
            ),
            'active_deployments', (
                SELECT COUNT(*) FROM deployment_pipelines 
                WHERE status = 'running'
            ),
            'avg_deployment_time_minutes', (
                SELECT ROUND(AVG(EXTRACT(EPOCH FROM (completed_at - started_at))) / 60, 2)
                FROM deployment_pipelines
                WHERE status = 'completed'
                AND completed_at > NOW() - INTERVAL '7 days'
            )
        ),
        'environment_status', (
            SELECT jsonb_agg(
                jsonb_build_object(
                    'environment', environment,
                    'last_deployment', MAX(completed_at),
                    'last_status', status,
                    'is_healthy', CASE WHEN status = 'completed' THEN TRUE ELSE FALSE END
                )
            )
            FROM (
                SELECT DISTINCT ON (environment) 
                    environment, completed_at, status
                FROM deployment_pipelines
                ORDER BY environment, completed_at DESC
            ) env_status
        ),
        'recent_rollbacks', (
            SELECT jsonb_agg(
                jsonb_build_object(
                    'pipeline_id', pipeline_id,
                    'rollback_reason', rollback_reason,
                    'rollback_type', rollback_type,
                    'started_at', started_at
                )
            )
            FROM deployment_rollbacks
            WHERE started_at > NOW() - INTERVAL '7 days'
            ORDER BY started_at DESC
            LIMIT 10
        )
    ) INTO health_data;
    
    RETURN health_data;
END;
$$ LANGUAGE plpgsql;
```

---

**Tài liệu này cung cấp framework hoàn chỉnh cho Deployment & CI/CD trong môi trường production, đảm bảo automation, reliability và monitoring cho quá trình deployment database.** 