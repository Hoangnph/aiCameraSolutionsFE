# Production Multi-tenancy Architecture - AI Camera Counting System

## 📊 Tổng quan

Tài liệu này trình bày kiến trúc multi-tenancy cho hệ thống AI Camera Counting trong môi trường production, bao gồm tenant isolation, data segregation, resource allocation và scalability.

## 🎯 Multi-tenancy Objectives

- **Tenant Isolation**: Đảm bảo dữ liệu và tài nguyên được tách biệt hoàn toàn giữa các tenant
- **Scalability**: Hỗ trợ hàng nghìn tenant với hiệu suất tối ưu
- **Resource Efficiency**: Chia sẻ tài nguyên một cách hiệu quả
- **Security**: Bảo mật dữ liệu tenant ở mức cao nhất
- **Flexibility**: Hỗ trợ các cấu hình khác nhau cho từng tenant

## 🏗️ Multi-tenancy Architecture

### Multi-Tenant Database Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              MULTI-TENANCY ARCHITECTURE                         │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              TENANT MANAGEMENT LAYER                        │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Tenant    │  │   Tenant    │  │   Tenant    │  │   Tenant    │        │ │
│  │  │   Registry  │  │   Provisioning│  │   Billing   │  │   Limits    │        │ │
│  │  │             │  │             │  │             │  │             │        │ │
│  │  │ • Tenant    │  │ • Auto      │  │ • Usage     │  │ • Storage   │        │ │
│  │  │   Metadata  │  │   Provision │  │   Tracking  │  │   Limits    │        │ │
│  │  │ • Tenant    │  │ • Resource  │  │ • Billing   │  │ • API       │        │ │
│  │  │   Status    │  │   Allocation│  │   Cycles    │  │   Limits    │        │ │
│  │  │ • Tenant    │  │ • Schema    │  │ • Cost      │  │ • User      │        │ │
│  │  │   Config    │  │   Creation  │  │   Allocation│  │   Limits    │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                             │
│                                    ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              DATA ISOLATION LAYER                           │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Shared    │  │   Schema    │  │   Row-Level │  │   Database  │        │ │
│  │  │   Database  │  │   Per       │  │   Security  │  │   Per       │        │ │
│  │  │             │  │   Tenant    │  │   (RLS)     │  │   Tenant    │        │ │
│  │  │ • Single    │  │             │  │             │  │             │        │ │
│  │  │   Database  │  │ • Separate  │  │ • Tenant    │  │ • Complete  │        │ │
│  │  │ • Tenant    │  │   Schemas   │  │   Filtering │  │   Isolation │        │ │
│  │  │   Filtering │  │ • Tenant    │  │ • Data      │  │ • Maximum   │        │ │
│  │  │ • Resource  │  │   Prefix    │  │   Segregation│  │   Security  │        │ │
│  │  │   Sharing   │  │ • Schema    │  │ • Access    │  │ • Resource  │        │ │
│  │  │ • Cost      │  │   Isolation │  │   Control   │  │   Dedication│        │ │
│  │  │   Efficiency│  │             │  │             │  │             │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                             │
│                                    ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              APPLICATION LAYER                              │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Tenant    │  │   Request   │  │   Data      │  │   Response  │        │ │
│  │  │   Context   │  │   Routing   │  │   Access    │  │   Filtering │        │ │
│  │  │             │  │             │  │   Layer     │  │             │        │ │
│  │  │ • Tenant    │  │ • URL       │  │ • Query     │  │ • Tenant    │        │ │
│  │  │   Detection │  │   Based     │  │   Filtering │  │   Data      │        │ │
│  │  │ • Tenant    │  │ • Subdomain │  │ • Schema    │  │   Isolation │        │ │
│  │  │   Validation│  │ • Header    │  │   Selection │  │ • Response  │        │ │
│  │  │ • Tenant    │  │   Based     │  │ • Connection│  │   Sanitization│       │ │
│  │  │   Limits    │  │ • Token     │  │   Pooling   │  │ • Error     │        │ │
│  │  │   Check     │  │   Based     │  │ • Caching   │  │   Handling  │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 🏢 Tenant Management System

### Tenant Registry

```sql
-- Tenant management tables
CREATE TABLE tenants (
    id SERIAL PRIMARY KEY,
    tenant_id VARCHAR(50) UNIQUE NOT NULL,
    tenant_name VARCHAR(100) NOT NULL,
    tenant_domain VARCHAR(100) UNIQUE,
    tenant_subdomain VARCHAR(50) UNIQUE,
    status VARCHAR(20) DEFAULT 'active', -- active, suspended, inactive
    plan_type VARCHAR(20) DEFAULT 'standard', -- basic, standard, premium, enterprise
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB DEFAULT '{}'::jsonb
);

-- Tenant configuration
CREATE TABLE tenant_configs (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER REFERENCES tenants(id),
    config_key VARCHAR(100) NOT NULL,
    config_value TEXT,
    config_type VARCHAR(20) DEFAULT 'string', -- string, integer, boolean, json
    is_encrypted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(tenant_id, config_key)
);

-- Tenant resource limits
CREATE TABLE tenant_limits (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER REFERENCES tenants(id),
    resource_type VARCHAR(50) NOT NULL, -- storage, api_calls, users, cameras
    limit_value BIGINT NOT NULL,
    current_usage BIGINT DEFAULT 0,
    reset_period VARCHAR(20) DEFAULT 'monthly', -- daily, weekly, monthly, yearly
    reset_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(tenant_id, resource_type)
);

-- Tenant billing
CREATE TABLE tenant_billing (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER REFERENCES tenants(id),
    billing_cycle VARCHAR(20) NOT NULL, -- monthly, quarterly, yearly
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    base_amount DECIMAL(10,2) NOT NULL,
    usage_amount DECIMAL(10,2) DEFAULT 0,
    total_amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending', -- pending, paid, overdue, cancelled
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert default tenant configurations
INSERT INTO tenant_configs (tenant_id, config_key, config_value, config_type) VALUES
(1, 'max_cameras', '10', 'integer'),
(1, 'max_users', '50', 'integer'),
(1, 'storage_limit_gb', '100', 'integer'),
(1, 'api_rate_limit', '1000', 'integer'),
(1, 'retention_days', '365', 'integer'),
(1, 'backup_frequency', 'daily', 'string'),
(1, 'support_level', 'standard', 'string');
```

### Tenant Provisioning

```sql
-- Tenant provisioning function
CREATE OR REPLACE FUNCTION provision_tenant(
    p_tenant_id VARCHAR(50),
    p_tenant_name VARCHAR(100),
    p_plan_type VARCHAR(20) DEFAULT 'standard'
)
RETURNS INTEGER AS $$
DECLARE
    new_tenant_id INTEGER;
    schema_name VARCHAR(100);
BEGIN
    -- Create tenant record
    INSERT INTO tenants (tenant_id, tenant_name, plan_type)
    VALUES (p_tenant_id, p_tenant_name, p_plan_type)
    RETURNING id INTO new_tenant_id;
    
    -- Create tenant schema
    schema_name := 'tenant_' || new_tenant_id;
    EXECUTE format('CREATE SCHEMA %I', schema_name);
    
    -- Create tenant tables in schema
    EXECUTE format('
        CREATE TABLE %I.cameras (
            id SERIAL PRIMARY KEY,
            camera_name VARCHAR(100) NOT NULL,
            location VARCHAR(255),
            status VARCHAR(20) DEFAULT ''active'',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )', schema_name);
    
    EXECUTE format('
        CREATE TABLE %I.counting_results (
            id SERIAL PRIMARY KEY,
            camera_id INTEGER REFERENCES %I.cameras(id),
            count_type VARCHAR(50) NOT NULL,
            count_value INTEGER NOT NULL,
            confidence_score DECIMAL(5,4),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )', schema_name, schema_name);
    
    EXECUTE format('
        CREATE TABLE %I.users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            role VARCHAR(20) DEFAULT ''user'',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )', schema_name);
    
    -- Create indexes
    EXECUTE format('
        CREATE INDEX idx_%s_counting_results_camera_time 
        ON %I.counting_results(camera_id, created_at DESC)', 
        new_tenant_id, schema_name);
    
    -- Set default limits based on plan
    INSERT INTO tenant_limits (tenant_id, resource_type, limit_value)
    SELECT 
        new_tenant_id,
        resource_type,
        CASE p_plan_type
            WHEN 'basic' THEN basic_limit
            WHEN 'standard' THEN standard_limit
            WHEN 'premium' THEN premium_limit
            WHEN 'enterprise' THEN enterprise_limit
        END
    FROM (
        VALUES 
            ('cameras', 5, 10, 50, 200),
            ('users', 10, 50, 200, 1000),
            ('storage_gb', 50, 100, 500, 2000),
            ('api_calls_per_day', 1000, 10000, 50000, 200000)
        ) AS limits(resource_type, basic_limit, standard_limit, premium_limit, enterprise_limit);
    
    -- Set default configurations
    INSERT INTO tenant_configs (tenant_id, config_key, config_value, config_type)
    VALUES
        (new_tenant_id, 'schema_name', schema_name, 'string'),
        (new_tenant_id, 'timezone', 'UTC', 'string'),
        (new_tenant_id, 'language', 'en', 'string'),
        (new_tenant_id, 'date_format', 'YYYY-MM-DD', 'string');
    
    RAISE NOTICE 'Provisioned tenant: % (ID: %, Schema: %)', 
                p_tenant_name, new_tenant_id, schema_name;
    
    RETURN new_tenant_id;
END;
$$ LANGUAGE plpgsql;
```

## 🔒 Data Isolation Strategies

### Row-Level Security (RLS) Implementation

```sql
-- Enable RLS on shared tables
ALTER TABLE cameras ENABLE ROW LEVEL SECURITY;
ALTER TABLE counting_results ENABLE ROW LEVEL SECURITY;
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;

-- Tenant-based RLS policies
CREATE POLICY tenant_cameras_policy ON cameras
    FOR ALL
    USING (tenant_id = current_setting('app.current_tenant_id')::integer)
    WITH CHECK (tenant_id = current_setting('app.current_tenant_id')::integer);

CREATE POLICY tenant_counting_results_policy ON counting_results
    FOR ALL
    USING (tenant_id = current_setting('app.current_tenant_id')::integer)
    WITH CHECK (tenant_id = current_setting('app.current_tenant_id')::integer);

CREATE POLICY tenant_users_policy ON users
    FOR ALL
    USING (tenant_id = current_setting('app.current_tenant_id')::integer)
    WITH CHECK (tenant_id = current_setting('app.current_tenant_id')::integer);

-- Tenant context function
CREATE OR REPLACE FUNCTION set_tenant_context(tenant_id INTEGER)
RETURNS VOID AS $$
BEGIN
    PERFORM set_config('app.current_tenant_id', tenant_id::text, FALSE);
    PERFORM set_config('app.current_tenant_schema', 
                      'tenant_' || tenant_id::text, FALSE);
END;
$$ LANGUAGE plpgsql;
```

### Schema-Based Isolation

```sql
-- Schema-based data access function
CREATE OR REPLACE FUNCTION get_tenant_data(
    p_table_name VARCHAR(100),
    p_tenant_id INTEGER
)
RETURNS TABLE(data JSONB) AS $$
DECLARE
    schema_name VARCHAR(100);
    query_text TEXT;
BEGIN
    schema_name := 'tenant_' || p_tenant_id;
    
    query_text := format('
        SELECT to_jsonb(t.*) as data
        FROM %I.%I t
        LIMIT 1000
    ', schema_name, p_table_name);
    
    RETURN QUERY EXECUTE query_text;
END;
$$ LANGUAGE plpgsql;

-- Cross-tenant data access (admin only)
CREATE OR REPLACE FUNCTION get_all_tenant_data(
    p_table_name VARCHAR(100)
)
RETURNS TABLE(tenant_id INTEGER, data JSONB) AS $$
DECLARE
    tenant_record RECORD;
    schema_name VARCHAR(100);
    query_text TEXT;
BEGIN
    FOR tenant_record IN 
        SELECT id FROM tenants WHERE status = 'active'
    LOOP
        schema_name := 'tenant_' || tenant_record.id;
        
        query_text := format('
            SELECT %L::integer as tenant_id, to_jsonb(t.*) as data
            FROM %I.%I t
            LIMIT 100
        ', tenant_record.id, schema_name, p_table_name);
        
        RETURN QUERY EXECUTE query_text;
    END LOOP;
END;
$$ LANGUAGE plpgsql;
```

## 📊 Resource Management

### Resource Usage Tracking

```sql
-- Resource usage tracking
CREATE TABLE tenant_resource_usage (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER REFERENCES tenants(id),
    resource_type VARCHAR(50) NOT NULL,
    usage_value BIGINT NOT NULL,
    usage_date DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Resource usage tracking function
CREATE OR REPLACE FUNCTION track_resource_usage(
    p_tenant_id INTEGER,
    p_resource_type VARCHAR(50),
    p_usage_value BIGINT DEFAULT 1
)
RETURNS VOID AS $$
BEGIN
    -- Insert usage record
    INSERT INTO tenant_resource_usage (tenant_id, resource_type, usage_value)
    VALUES (p_tenant_id, p_resource_type, p_usage_value);
    
    -- Update current usage in limits table
    UPDATE tenant_limits 
    SET current_usage = current_usage + p_usage_value,
        updated_at = CURRENT_TIMESTAMP
    WHERE tenant_id = p_tenant_id 
    AND resource_type = p_resource_type;
END;
$$ LANGUAGE plpgsql;

-- Resource limit check function
CREATE OR REPLACE FUNCTION check_resource_limit(
    p_tenant_id INTEGER,
    p_resource_type VARCHAR(50),
    p_required_amount BIGINT DEFAULT 1
)
RETURNS BOOLEAN AS $$
DECLARE
    current_usage BIGINT;
    limit_value BIGINT;
BEGIN
    SELECT current_usage, limit_value 
    INTO current_usage, limit_value
    FROM tenant_limits 
    WHERE tenant_id = p_tenant_id 
    AND resource_type = p_resource_type;
    
    RETURN (current_usage + p_required_amount) <= limit_value;
END;
$$ LANGUAGE plpgsql;
```

### Billing and Usage Analytics

```sql
-- Usage analytics view
CREATE VIEW tenant_usage_analytics AS
SELECT 
    t.tenant_id,
    t.tenant_name,
    t.plan_type,
    tl.resource_type,
    tl.limit_value,
    tl.current_usage,
    ROUND((tl.current_usage * 100.0) / tl.limit_value, 2) as usage_percentage,
    CASE 
        WHEN tl.current_usage >= tl.limit_value THEN 'LIMIT_REACHED'
        WHEN tl.current_usage >= (tl.limit_value * 0.8) THEN 'HIGH_USAGE'
        WHEN tl.current_usage >= (tl.limit_value * 0.5) THEN 'MEDIUM_USAGE'
        ELSE 'LOW_USAGE'
    END as usage_status
FROM tenants t
JOIN tenant_limits tl ON t.id = tl.tenant_id
WHERE t.status = 'active'
ORDER BY t.tenant_id, tl.resource_type;

-- Billing calculation function
CREATE OR REPLACE FUNCTION calculate_tenant_billing(
    p_tenant_id INTEGER,
    p_billing_cycle VARCHAR(20) DEFAULT 'monthly'
)
RETURNS TABLE(
    tenant_id INTEGER,
    base_amount DECIMAL(10,2),
    usage_amount DECIMAL(10,2),
    total_amount DECIMAL(10,2)
) AS $$
DECLARE
    plan_type VARCHAR(20);
    base_cost DECIMAL(10,2);
    usage_cost DECIMAL(10,2);
BEGIN
    -- Get tenant plan
    SELECT t.plan_type INTO plan_type
    FROM tenants t
    WHERE t.id = p_tenant_id;
    
    -- Calculate base cost
    base_cost := CASE plan_type
        WHEN 'basic' THEN 29.99
        WHEN 'standard' THEN 99.99
        WHEN 'premium' THEN 299.99
        WHEN 'enterprise' THEN 999.99
        ELSE 0
    END;
    
    -- Calculate usage cost
    SELECT COALESCE(SUM(
        CASE resource_type
            WHEN 'storage_gb' THEN current_usage * 0.10
            WHEN 'api_calls_per_day' THEN current_usage * 0.001
            WHEN 'cameras' THEN current_usage * 5.00
            WHEN 'users' THEN current_usage * 2.00
            ELSE 0
        END
    ), 0) INTO usage_cost
    FROM tenant_limits
    WHERE tenant_id = p_tenant_id;
    
    RETURN QUERY SELECT 
        p_tenant_id,
        base_cost,
        usage_cost,
        base_cost + usage_cost;
END;
$$ LANGUAGE plpgsql;
```

## 🔧 Application Integration

### Tenant Context Management

```sql
-- Tenant context middleware function
CREATE OR REPLACE FUNCTION resolve_tenant_context(
    p_tenant_identifier VARCHAR(100)
)
RETURNS INTEGER AS $$
DECLARE
    tenant_id INTEGER;
BEGIN
    -- Try to resolve tenant by different methods
    SELECT id INTO tenant_id
    FROM tenants
    WHERE tenant_id = p_tenant_identifier
       OR tenant_domain = p_tenant_identifier
       OR tenant_subdomain = p_tenant_identifier
       OR tenant_name = p_tenant_identifier;
    
    IF tenant_id IS NULL THEN
        RAISE EXCEPTION 'Tenant not found: %', p_tenant_identifier;
    END IF;
    
    -- Set tenant context
    PERFORM set_tenant_context(tenant_id);
    
    RETURN tenant_id;
END;
$$ LANGUAGE plpgsql;

-- Tenant-aware data access functions
CREATE OR REPLACE FUNCTION get_tenant_cameras(p_tenant_id INTEGER)
RETURNS TABLE(
    id INTEGER,
    camera_name VARCHAR(100),
    location VARCHAR(255),
    status VARCHAR(20),
    created_at TIMESTAMP
) AS $$
DECLARE
    schema_name VARCHAR(100);
BEGIN
    schema_name := 'tenant_' || p_tenant_id;
    
    RETURN QUERY EXECUTE format('
        SELECT id, camera_name, location, status, created_at
        FROM %I.cameras
        ORDER BY created_at DESC
    ', schema_name);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_tenant_counting_results(
    p_tenant_id INTEGER,
    p_camera_id INTEGER DEFAULT NULL,
    p_start_date TIMESTAMP DEFAULT NULL,
    p_end_date TIMESTAMP DEFAULT NULL
)
RETURNS TABLE(
    id INTEGER,
    camera_id INTEGER,
    count_type VARCHAR(50),
    count_value INTEGER,
    confidence_score DECIMAL(5,4),
    created_at TIMESTAMP
) AS $$
DECLARE
    schema_name VARCHAR(100);
    where_clause TEXT := '';
BEGIN
    schema_name := 'tenant_' || p_tenant_id;
    
    IF p_camera_id IS NOT NULL THEN
        where_clause := where_clause || ' AND camera_id = ' || p_camera_id;
    END IF;
    
    IF p_start_date IS NOT NULL THEN
        where_clause := where_clause || ' AND created_at >= ''' || p_start_date || '''';
    END IF;
    
    IF p_end_date IS NOT NULL THEN
        where_clause := where_clause || ' AND created_at <= ''' || p_end_date || '''';
    END IF;
    
    RETURN QUERY EXECUTE format('
        SELECT id, camera_id, count_type, count_value, confidence_score, created_at
        FROM %I.counting_results
        WHERE 1=1 %s
        ORDER BY created_at DESC
        LIMIT 1000
    ', schema_name, where_clause);
END;
$$ LANGUAGE plpgsql;
```

## 📈 Performance Optimization

### Multi-Tenant Performance Strategies

```sql
-- Tenant-specific connection pooling
CREATE OR REPLACE FUNCTION get_tenant_connection_pool(
    p_tenant_id INTEGER
)
RETURNS VARCHAR(100) AS $$
BEGIN
    -- Return tenant-specific connection pool name
    RETURN 'tenant_pool_' || p_tenant_id;
END;
$$ LANGUAGE plpgsql;

-- Tenant-specific caching
CREATE OR REPLACE FUNCTION get_tenant_cache_key(
    p_tenant_id INTEGER,
    p_cache_key VARCHAR(100)
)
RETURNS VARCHAR(200) AS $$
BEGIN
    -- Prefix cache keys with tenant ID
    RETURN 'tenant_' || p_tenant_id || ':' || p_cache_key;
END;
$$ LANGUAGE plpgsql;

-- Tenant data partitioning
CREATE OR REPLACE FUNCTION create_tenant_partitions(
    p_tenant_id INTEGER
)
RETURNS VOID AS $$
DECLARE
    schema_name VARCHAR(100);
BEGIN
    schema_name := 'tenant_' || p_tenant_id;
    
    -- Create partitioned counting results table
    EXECUTE format('
        CREATE TABLE %I.counting_results_partitioned (
            id SERIAL,
            camera_id INTEGER,
            count_type VARCHAR(50),
            count_value INTEGER,
            confidence_score DECIMAL(5,4),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) PARTITION BY RANGE (created_at)
    ', schema_name);
    
    -- Create monthly partitions for the next 12 months
    FOR i IN 0..11 LOOP
        EXECUTE format('
            CREATE TABLE %I.counting_results_%s 
            PARTITION OF %I.counting_results_partitioned
            FOR VALUES FROM (''%s-01-01'') TO (''%s-01-01'')
        ', 
        schema_name,
        TO_CHAR(NOW() + (i || ' months')::INTERVAL, 'YYYY_MM'),
        schema_name,
        TO_CHAR(NOW() + (i || ' months')::INTERVAL, 'YYYY-MM'),
        TO_CHAR(NOW() + ((i+1) || ' months')::INTERVAL, 'YYYY-MM')
        );
    END LOOP;
END;
$$ LANGUAGE plpgsql;
```

## 🔍 Monitoring and Analytics

### Multi-Tenant Monitoring

```sql
-- Tenant performance metrics
CREATE VIEW tenant_performance_metrics AS
SELECT 
    t.tenant_id,
    t.tenant_name,
    t.plan_type,
    COUNT(DISTINCT c.id) as camera_count,
    COUNT(cr.id) as total_counts,
    AVG(cr.confidence_score) as avg_confidence,
    MAX(cr.created_at) as last_activity,
    pg_size_pretty(pg_database_size(current_database())) as db_size
FROM tenants t
LEFT JOIN LATERAL get_tenant_cameras(t.id) c ON TRUE
LEFT JOIN LATERAL get_tenant_counting_results(t.id) cr ON TRUE
WHERE t.status = 'active'
GROUP BY t.id, t.tenant_id, t.tenant_name, t.plan_type
ORDER BY total_counts DESC;

-- Tenant health monitoring
CREATE OR REPLACE FUNCTION check_tenant_health()
RETURNS TABLE(
    tenant_id VARCHAR(50),
    health_status VARCHAR(20),
    issues TEXT[]
) AS $$
DECLARE
    tenant_record RECORD;
    issues TEXT[];
BEGIN
    FOR tenant_record IN 
        SELECT t.tenant_id, t.tenant_name, t.id
        FROM tenants t
        WHERE t.status = 'active'
    LOOP
        issues := ARRAY[]::TEXT[];
        
        -- Check resource limits
        IF EXISTS (
            SELECT 1 FROM tenant_limits 
            WHERE tenant_id = tenant_record.id 
            AND current_usage >= limit_value
        ) THEN
            issues := array_append(issues, 'Resource limit exceeded');
        END IF;
        
        -- Check recent activity
        IF NOT EXISTS (
            SELECT 1 FROM tenant_resource_usage 
            WHERE tenant_id = tenant_record.id 
            AND usage_date >= CURRENT_DATE - INTERVAL '7 days'
        ) THEN
            issues := array_append(issues, 'No recent activity');
        END IF;
        
        -- Determine health status
        RETURN QUERY SELECT 
            tenant_record.tenant_id,
            CASE 
                WHEN array_length(issues, 1) = 0 THEN 'HEALTHY'
                WHEN array_length(issues, 1) <= 2 THEN 'WARNING'
                ELSE 'CRITICAL'
            END,
            issues;
    END LOOP;
END;
$$ LANGUAGE plpgsql;
```

---

**Tài liệu này cung cấp framework hoàn chỉnh cho Multi-tenancy Architecture trong môi trường production, đảm bảo isolation, scalability và hiệu suất tối ưu cho hệ thống multi-tenant.** 