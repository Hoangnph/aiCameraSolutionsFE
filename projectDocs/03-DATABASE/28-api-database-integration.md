# API Database Integration Guide - AI Camera Counting System

## 📊 Tổng quan

Tài liệu này trình bày hướng dẫn chi tiết về API integration với database trong hệ thống AI Camera Counting, bao gồm API endpoint database mappings, data validation patterns, error handling, và performance optimization.

## 🎯 Mục tiêu

- **API Endpoint Mappings**: Mapping giữa API endpoints và database operations
- **Data Validation**: Patterns cho data validation và sanitization
- **Error Handling**: Database error handling patterns
- **Performance Optimization**: API performance optimization với database
- **Connection Management**: Database connection management cho APIs

## 🏗️ API Database Architecture

### API Database Integration Flow

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              API DATABASE INTEGRATION ARCHITECTURE              │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              API GATEWAY LAYER                             │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Request   │  │   Rate      │  │   Auth      │  │   Request   │        │ │
│  │  │   Router    │  │   Limiting  │  │   Middleware│  │   Validation│        │ │
│  │  │             │  │             │  │             │  │             │        │ │
│  │  │ • Route     │  │ • Rate      │  │ • JWT       │  │ • Schema    │        │ │
│  │  │   Matching  │  │   Limits    │  │   Validation│  │   Validation│        │ │
│  │  │ • Load      │  │ • Throttling│  │ • Role      │  │ • Data      │        │ │
│  │  │   Balancing │  │ • Quotas    │  │   Checking  │  │   Sanitization│       │ │
│  │  │ • Service   │  │ • Burst     │  │ • Permission│  │ • Input     │        │ │
│  │  │   Discovery │  │   Control   │  │   Validation│  │   Filtering │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                             │
│                                    ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              API SERVICE LAYER                              │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Camera    │  │   Detection │  │   Analytics │  │   User      │        │ │
│  │  │   Service   │  │   Service   │  │   Service   │  │   Service   │        │ │
│  │  │             │  │             │  │             │  │             │        │ │
│  │  │ • Camera    │  │ • Detection │  │ • Analytics │  │ • User      │        │ │
│  │  │   CRUD      │  │   Results   │  │   Data      │  │   Management│        │ │
│  │  │ • Stream    │  │ • Tracking  │  │ • Reports   │  │ • Auth      │        │ │
│  │  │   Management│  │   Data      │  │ • Metrics   │  │ • Permissions│       │ │
│  │  │ • Health    │  │ • Counting  │  │ • Dashboards│  │ • Profiles  │        │ │
│  │  │   Monitoring│  │   Events    │  │ • KPIs      │  │ • Settings  │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                             │
│                                    ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              DATA ACCESS LAYER                              │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Repository│  │   Query     │  │   Cache     │  │   Connection│        │ │
│  │  │   Pattern   │  │   Builder   │  │   Layer     │  │   Pool      │        │ │
│  │  │             │  │             │  │             │  │             │        │ │
│  │  │ • Data      │  │ • Dynamic   │  │ • Redis     │  │ • Connection│        │ │
│  │  │   Access    │  │   Queries   │  │   Cache     │  │   Pooling   │        │ │
│  │  │ • CRUD      │  │ • Query     │  │ • Memory    │  │ • Connection│        │ │
│  │  │   Operations│  │   Optimization│  │   Cache     │  │   Monitoring│        │ │
│  │  │ • Data      │  │ • Parameter │  │ • Cache     │  │ • Failover  │        │ │
│  │  │   Mapping   │  │   Binding   │  │   Invalidation│  │ • Load      │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                             │
│                                    ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              DATABASE LAYER                                 │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Primary   │  │   Read      │  │   Cache     │  │   Analytics │        │ │
│  │  │   Database  │  │   Replica   │  │   Database  │  │   Database  │        │ │
│  │  │             │  │             │  │             │  │             │        │ │
│  │  │ • Write     │  │ • Read      │  │ • Session   │  │ • Analytics │        │ │
│  │  │   Operations│  │   Operations│  │   Data      │  │   Data      │        │ │
│  │  │ • ACID      │  │ • Reporting │  │ • Temporary │  │ • Aggregated│        │ │
│  │  │   Compliance│  │ • Analytics │  │   Data      │  │   Data      │        │ │
│  │  │ • Data      │  │ • Backup    │  │ • Cache     │  │ • Historical│        │ │
│  │  │   Integrity │  │ • Recovery  │  │   Tables    │  │   Data      │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 🔗 API Endpoint Database Mappings

### Camera Management API Mappings

```sql
-- API endpoint to database mapping table
CREATE TABLE api_endpoint_mappings (
    id SERIAL PRIMARY KEY,
    endpoint_path VARCHAR(200) NOT NULL,
    http_method VARCHAR(10) NOT NULL, -- GET, POST, PUT, DELETE
    service_name VARCHAR(100) NOT NULL,
    
    -- Database mapping
    database_operation VARCHAR(50) NOT NULL, -- SELECT, INSERT, UPDATE, DELETE
    target_table VARCHAR(100),
    target_schema VARCHAR(100),
    
    -- Query configuration
    query_template TEXT,
    query_parameters JSONB,
    result_mapping JSONB,
    
    -- Performance settings
    cache_enabled BOOLEAN DEFAULT TRUE,
    cache_ttl_seconds INTEGER DEFAULT 300,
    rate_limit_per_minute INTEGER DEFAULT 100,
    
    -- Security settings
    requires_auth BOOLEAN DEFAULT TRUE,
    required_roles TEXT[],
    required_permissions TEXT[],
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(endpoint_path, http_method)
);

-- Insert API endpoint mappings
INSERT INTO api_endpoint_mappings (endpoint_path, http_method, service_name, database_operation, target_table, query_template) VALUES
-- Camera Management
('/api/v1/cameras', 'GET', 'camera_service', 'SELECT', 'camera_configurations', 'SELECT * FROM camera_configurations WHERE tenant_id = $1 AND is_active = true'),
('/api/v1/cameras/{id}', 'GET', 'camera_service', 'SELECT', 'camera_configurations', 'SELECT * FROM camera_configurations WHERE camera_id = $1 AND tenant_id = $2'),
('/api/v1/cameras', 'POST', 'camera_service', 'INSERT', 'camera_configurations', 'INSERT INTO camera_configurations (camera_id, camera_name, ...) VALUES ($1, $2, ...)'),
('/api/v1/cameras/{id}', 'PUT', 'camera_service', 'UPDATE', 'camera_configurations', 'UPDATE camera_configurations SET ... WHERE camera_id = $1'),
('/api/v1/cameras/{id}', 'DELETE', 'camera_service', 'UPDATE', 'camera_configurations', 'UPDATE camera_configurations SET is_active = false WHERE camera_id = $1'),

-- Camera Health
('/api/v1/cameras/{id}/health', 'GET', 'camera_service', 'SELECT', 'camera_health', 'SELECT * FROM camera_health WHERE camera_id = $1'),
('/api/v1/cameras/{id}/health', 'POST', 'camera_service', 'INSERT', 'camera_health', 'INSERT INTO camera_health (camera_id, status, ...) VALUES ($1, $2, ...)'),

-- Stream Management
('/api/v1/cameras/{id}/streams', 'GET', 'camera_service', 'SELECT', 'video_streams', 'SELECT * FROM video_streams WHERE camera_id = $1'),
('/api/v1/cameras/{id}/streams', 'POST', 'camera_service', 'INSERT', 'video_streams', 'INSERT INTO video_streams (stream_id, camera_id, ...) VALUES ($1, $2, ...)'),

-- Detection Results
('/api/v1/cameras/{id}/detections', 'GET', 'detection_service', 'SELECT', 'person_detections', 'SELECT * FROM person_detections WHERE camera_id = $1 AND frame_timestamp > $2'),
('/api/v1/cameras/{id}/detections', 'POST', 'detection_service', 'INSERT', 'person_detections', 'INSERT INTO person_detections (camera_id, detection_id, ...) VALUES ($1, $2, ...)'),

-- Counting Results
('/api/v1/cameras/{id}/counting', 'GET', 'counting_service', 'SELECT', 'counting_results', 'SELECT * FROM counting_results WHERE camera_id = $1 ORDER BY result_timestamp DESC LIMIT $2'),
('/api/v1/cameras/{id}/counting', 'POST', 'counting_service', 'INSERT', 'counting_events', 'INSERT INTO counting_events (camera_id, event_type, ...) VALUES ($1, $2, ...)'),

-- Analytics
('/api/v1/cameras/{id}/analytics', 'GET', 'analytics_service', 'SELECT', 'realtime_analytics', 'SELECT * FROM realtime_analytics WHERE camera_id = $1 ORDER BY metric_timestamp DESC LIMIT $2'),
('/api/v1/cameras/{id}/analytics/historical', 'GET', 'analytics_service', 'SELECT', 'historical_analytics', 'SELECT * FROM historical_analytics WHERE camera_id = $1 AND data_date BETWEEN $2 AND $3');
```

### API Response Data Models

```sql
-- API response templates
CREATE TABLE api_response_templates (
    id SERIAL PRIMARY KEY,
    endpoint_mapping_id INTEGER REFERENCES api_endpoint_mappings(id),
    response_type VARCHAR(50) NOT NULL, -- success, error, paginated
    
    -- Response structure
    response_schema JSONB NOT NULL,
    response_example JSONB,
    response_headers JSONB,
    
    -- Response configuration
    include_metadata BOOLEAN DEFAULT TRUE,
    include_pagination BOOLEAN DEFAULT FALSE,
    include_timestamps BOOLEAN DEFAULT TRUE,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- API error codes and messages
CREATE TABLE api_error_codes (
    id SERIAL PRIMARY KEY,
    error_code VARCHAR(20) UNIQUE NOT NULL,
    error_message TEXT NOT NULL,
    error_category VARCHAR(50) NOT NULL, -- validation, database, auth, business
    
    -- Error details
    http_status_code INTEGER NOT NULL,
    error_details JSONB,
    suggested_action TEXT,
    
    -- Localization
    localized_messages JSONB, -- translations
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert common error codes
INSERT INTO api_error_codes (error_code, error_message, error_category, http_status_code) VALUES
('CAMERA_NOT_FOUND', 'Camera with specified ID not found', 'business', 404),
('CAMERA_INACTIVE', 'Camera is currently inactive', 'business', 400),
('INVALID_CAMERA_CONFIG', 'Invalid camera configuration provided', 'validation', 400),
('STREAM_CONNECTION_FAILED', 'Failed to connect to camera stream', 'business', 503),
('DETECTION_FAILED', 'Person detection failed', 'business', 500),
('COUNTING_ERROR', 'People counting error occurred', 'business', 500),
('INSUFFICIENT_PERMISSIONS', 'Insufficient permissions to access resource', 'auth', 403),
('RATE_LIMIT_EXCEEDED', 'Rate limit exceeded', 'business', 429),
('DATABASE_CONNECTION_ERROR', 'Database connection error', 'database', 503),
('VALIDATION_ERROR', 'Request validation failed', 'validation', 400);
```

## ✅ Data Validation Patterns

### Input Validation Tables

```sql
-- API input validation schemas
CREATE TABLE api_validation_schemas (
    id SERIAL PRIMARY KEY,
    endpoint_mapping_id INTEGER REFERENCES api_endpoint_mappings(id),
    schema_name VARCHAR(100) NOT NULL,
    
    -- Validation schema
    validation_schema JSONB NOT NULL, -- JSON Schema format
    validation_rules JSONB, -- custom validation rules
    
    -- Validation configuration
    strict_mode BOOLEAN DEFAULT TRUE,
    allow_unknown_fields BOOLEAN DEFAULT FALSE,
    sanitize_input BOOLEAN DEFAULT TRUE,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Validation rules for camera data
INSERT INTO api_validation_schemas (endpoint_mapping_id, schema_name, validation_schema) VALUES
(3, 'camera_create', '{
  "type": "object",
  "required": ["camera_name", "camera_type", "stream_url"],
  "properties": {
    "camera_name": {
      "type": "string",
      "minLength": 1,
      "maxLength": 200,
      "pattern": "^[a-zA-Z0-9\\s\\-_]+$"
    },
    "camera_type": {
      "type": "string",
      "enum": ["IP", "USB", "RTSP", "HTTP", "WebRTC"]
    },
    "stream_url": {
      "type": "string",
      "format": "uri",
      "maxLength": 500
    },
    "resolution_width": {
      "type": "integer",
      "minimum": 320,
      "maximum": 7680
    },
    "resolution_height": {
      "type": "integer",
      "minimum": 240,
      "maximum": 4320
    },
    "frame_rate": {
      "type": "integer",
      "minimum": 1,
      "maximum": 120
    },
    "confidence_threshold": {
      "type": "number",
      "minimum": 0.1,
      "maximum": 1.0
    }
  }
}'),

(4, 'camera_update', '{
  "type": "object",
  "properties": {
    "camera_name": {
      "type": "string",
      "minLength": 1,
      "maxLength": 200
    },
    "stream_url": {
      "type": "string",
      "format": "uri"
    },
    "is_active": {
      "type": "boolean"
    },
    "ai_model_id": {
      "type": "integer",
      "minimum": 1
    }
  }
}'),

(9, 'detection_create', '{
  "type": "object",
  "required": ["detection_id", "confidence_score", "bbox_x", "bbox_y", "bbox_width", "bbox_height"],
  "properties": {
    "detection_id": {
      "type": "string",
      "pattern": "^[a-zA-Z0-9\\-_]+$"
    },
    "confidence_score": {
      "type": "number",
      "minimum": 0.0,
      "maximum": 1.0
    },
    "bbox_x": {
      "type": "integer",
      "minimum": 0
    },
    "bbox_y": {
      "type": "integer",
      "minimum": 0
    },
    "bbox_width": {
      "type": "integer",
      "minimum": 1
    },
    "bbox_height": {
      "type": "integer",
      "minimum": 1
    },
    "object_attributes": {
      "type": "object"
    }
  }
}');

-- Data sanitization rules
CREATE TABLE data_sanitization_rules (
    id SERIAL PRIMARY KEY,
    field_name VARCHAR(100) NOT NULL,
    field_type VARCHAR(50) NOT NULL, -- string, integer, float, boolean, json
    
    -- Sanitization rules
    sanitization_type VARCHAR(50) NOT NULL, -- trim, escape, validate, transform
    sanitization_config JSONB,
    
    -- Validation rules
    validation_pattern VARCHAR(200),
    min_length INTEGER,
    max_length INTEGER,
    min_value NUMERIC,
    max_value NUMERIC,
    
    -- Error handling
    error_message TEXT,
    default_value TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sanitization rules
INSERT INTO data_sanitization_rules (field_name, field_type, sanitization_type, sanitization_config) VALUES
('camera_name', 'string', 'trim', '{"remove_extra_spaces": true, "to_lowercase": false}'),
('stream_url', 'string', 'validate', '{"check_url_format": true, "allowed_protocols": ["rtsp", "http", "https"]}'),
('confidence_score', 'float', 'validate', '{"min": 0.0, "max": 1.0, "precision": 2}'),
('bbox_coordinates', 'json', 'validate', '{"required_fields": ["x", "y", "width", "height"], "non_negative": true}'),
('user_input', 'string', 'escape', '{"escape_html": true, "escape_sql": true}');
```

## ❌ Error Handling Database Patterns

### Error Handling Tables

```sql
-- API error logging
CREATE TABLE api_error_logs (
    id SERIAL PRIMARY KEY,
    request_id VARCHAR(100) NOT NULL,
    endpoint_path VARCHAR(200) NOT NULL,
    http_method VARCHAR(10) NOT NULL,
    
    -- Error details
    error_code VARCHAR(20) REFERENCES api_error_codes(error_code),
    error_message TEXT,
    error_stack_trace TEXT,
    error_category VARCHAR(50),
    
    -- Request details
    request_headers JSONB,
    request_body TEXT,
    request_params JSONB,
    user_id INTEGER REFERENCES users(id),
    
    -- Response details
    response_status_code INTEGER,
    response_body TEXT,
    response_time_ms INTEGER,
    
    -- Database context
    database_operation VARCHAR(50),
    database_error TEXT,
    affected_tables TEXT[],
    
    -- Timestamp
    error_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Database error patterns
CREATE TABLE database_error_patterns (
    id SERIAL PRIMARY KEY,
    error_pattern VARCHAR(200) NOT NULL,
    error_type VARCHAR(50) NOT NULL, -- constraint_violation, connection_error, timeout, etc.
    
    -- Pattern matching
    pattern_regex VARCHAR(500),
    pattern_description TEXT,
    
    -- Error handling
    suggested_action TEXT,
    retry_strategy VARCHAR(50), -- immediate, exponential_backoff, none
    max_retries INTEGER DEFAULT 3,
    
    -- Monitoring
    alert_threshold INTEGER DEFAULT 10, -- alert after N occurrences
    alert_severity VARCHAR(20) DEFAULT 'warning', -- info, warning, error, critical
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert common database error patterns
INSERT INTO database_error_patterns (error_pattern, error_type, pattern_regex, suggested_action) VALUES
('duplicate key value violates unique constraint', 'constraint_violation', 'duplicate key value violates unique constraint', 'Check for existing record before insert'),
('foreign key constraint violation', 'constraint_violation', 'foreign key constraint violation', 'Verify referenced record exists'),
('connection to server at .* failed', 'connection_error', 'connection to server at .* failed', 'Check database connectivity'),
('query execution timeout', 'timeout', 'query execution timeout', 'Optimize query or increase timeout'),
('insufficient memory', 'resource_error', 'insufficient memory', 'Check database memory usage'),
('table .* does not exist', 'schema_error', 'table .* does not exist', 'Verify database schema');

-- Error recovery strategies
CREATE TABLE error_recovery_strategies (
    id SERIAL PRIMARY KEY,
    error_pattern_id INTEGER REFERENCES database_error_patterns(id),
    strategy_name VARCHAR(100) NOT NULL,
    
    -- Recovery configuration
    recovery_action VARCHAR(50) NOT NULL, -- retry, fallback, circuit_breaker, manual_intervention
    recovery_config JSONB,
    
    -- Timing
    retry_delay_ms INTEGER DEFAULT 1000,
    max_retry_attempts INTEGER DEFAULT 3,
    circuit_breaker_threshold INTEGER DEFAULT 5,
    
    -- Fallback options
    fallback_endpoint VARCHAR(200),
    fallback_data JSONB,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Error Handling Functions

```sql
-- Error logging function
CREATE OR REPLACE FUNCTION log_api_error(
    p_request_id VARCHAR(100),
    p_endpoint_path VARCHAR(200),
    p_http_method VARCHAR(10),
    p_error_code VARCHAR(20),
    p_error_message TEXT,
    p_error_stack_trace TEXT DEFAULT NULL,
    p_request_body TEXT DEFAULT NULL,
    p_user_id INTEGER DEFAULT NULL,
    p_database_operation VARCHAR(50) DEFAULT NULL,
    p_database_error TEXT DEFAULT NULL
)
RETURNS INTEGER AS $$
DECLARE
    v_error_log_id INTEGER;
BEGIN
    INSERT INTO api_error_logs (
        request_id, endpoint_path, http_method, error_code, error_message,
        error_stack_trace, request_body, user_id, database_operation, database_error
    ) VALUES (
        p_request_id, p_endpoint_path, p_http_method, p_error_code, p_error_message,
        p_error_stack_trace, p_request_body, p_user_id, p_database_operation, p_database_error
    ) RETURNING id INTO v_error_log_id;
    
    -- Check if error pattern matches and trigger alerts
    PERFORM check_error_patterns(p_error_message);
    
    RETURN v_error_log_id;
END;
$$ LANGUAGE plpgsql;

-- Error pattern checking function
CREATE OR REPLACE FUNCTION check_error_patterns(p_error_message TEXT)
RETURNS VOID AS $$
DECLARE
    v_pattern RECORD;
    v_error_count INTEGER;
BEGIN
    FOR v_pattern IN 
        SELECT * FROM database_error_patterns 
        WHERE p_error_message ~ pattern_regex
    LOOP
        -- Count recent occurrences
        SELECT COUNT(*) INTO v_error_count
        FROM api_error_logs
        WHERE error_message ~ v_pattern.error_pattern
          AND error_timestamp > NOW() - INTERVAL '1 hour';
        
        -- Trigger alert if threshold exceeded
        IF v_error_count >= v_pattern.alert_threshold THEN
            INSERT INTO system_alerts (
                alert_type, alert_message, alert_severity, alert_data
            ) VALUES (
                'database_error_pattern',
                'Database error pattern detected: ' || v_pattern.error_pattern,
                v_pattern.alert_severity,
                jsonb_build_object(
                    'pattern_id', v_pattern.id,
                    'error_count', v_error_count,
                    'suggested_action', v_pattern.suggested_action
                )
            );
        END IF;
    END LOOP;
END;
$$ LANGUAGE plpgsql;
```

## ⚡ API Performance Optimization

### Performance Optimization Tables

```sql
-- API performance monitoring
CREATE TABLE api_performance_metrics (
    id SERIAL PRIMARY KEY,
    endpoint_path VARCHAR(200) NOT NULL,
    http_method VARCHAR(10) NOT NULL,
    metric_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Response time metrics
    avg_response_time_ms INTEGER,
    min_response_time_ms INTEGER,
    max_response_time_ms INTEGER,
    p95_response_time_ms INTEGER,
    p99_response_time_ms INTEGER,
    
    -- Throughput metrics
    request_count INTEGER,
    success_count INTEGER,
    error_count INTEGER,
    requests_per_second DECIMAL(8,2),
    
    -- Database metrics
    database_query_count INTEGER,
    database_query_time_ms INTEGER,
    database_connection_count INTEGER,
    cache_hit_ratio DECIMAL(5,2),
    
    -- Resource usage
    cpu_usage_percent DECIMAL(5,2),
    memory_usage_mb DECIMAL(8,2),
    network_bandwidth_mbps DECIMAL(8,2),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- API caching configuration
CREATE TABLE api_cache_config (
    id SERIAL PRIMARY KEY,
    endpoint_mapping_id INTEGER REFERENCES api_endpoint_mappings(id),
    
    -- Cache settings
    cache_enabled BOOLEAN DEFAULT TRUE,
    cache_ttl_seconds INTEGER DEFAULT 300,
    cache_key_template VARCHAR(500),
    cache_invalidation_rules JSONB,
    
    -- Cache performance
    cache_hit_ratio DECIMAL(5,2),
    cache_size_mb DECIMAL(8,2),
    cache_eviction_count INTEGER,
    
    -- Cache strategy
    cache_strategy VARCHAR(50) DEFAULT 'lru', -- lru, lfu, ttl
    cache_distribution BOOLEAN DEFAULT FALSE, -- distributed caching
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Query optimization tracking
CREATE TABLE query_optimization_tracking (
    id SERIAL PRIMARY KEY,
    endpoint_mapping_id INTEGER REFERENCES api_endpoint_mappings(id),
    query_hash VARCHAR(64) NOT NULL,
    
    -- Query details
    original_query TEXT,
    optimized_query TEXT,
    query_plan JSONB,
    
    -- Performance metrics
    original_execution_time_ms INTEGER,
    optimized_execution_time_ms INTEGER,
    performance_improvement_percent DECIMAL(5,2),
    
    -- Optimization details
    optimization_type VARCHAR(50), -- indexing, query_rewrite, caching
    optimization_reason TEXT,
    optimization_applied_at TIMESTAMP,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Performance Optimization Functions

```sql
-- Query performance monitoring function
CREATE OR REPLACE FUNCTION monitor_query_performance(
    p_endpoint_mapping_id INTEGER,
    p_query_hash VARCHAR(64),
    p_execution_time_ms INTEGER,
    p_query_plan JSONB DEFAULT NULL
)
RETURNS VOID AS $$
DECLARE
    v_avg_execution_time INTEGER;
    v_performance_threshold INTEGER := 1000; -- 1 second threshold
BEGIN
    -- Calculate average execution time
    SELECT AVG(original_execution_time_ms) INTO v_avg_execution_time
    FROM query_optimization_tracking
    WHERE endpoint_mapping_id = p_endpoint_mapping_id
      AND query_hash = p_query_hash;
    
    -- If query is slow, suggest optimization
    IF p_execution_time_ms > v_performance_threshold THEN
        INSERT INTO query_optimization_tracking (
            endpoint_mapping_id, query_hash, original_execution_time_ms, query_plan
        ) VALUES (
            p_endpoint_mapping_id, p_query_hash, p_execution_time_ms, p_query_plan
        );
        
        -- Trigger optimization alert
        INSERT INTO system_alerts (
            alert_type, alert_message, alert_severity, alert_data
        ) VALUES (
            'slow_query_detected',
            'Slow query detected for endpoint mapping ID: ' || p_endpoint_mapping_id,
            'warning',
            jsonb_build_object(
                'endpoint_mapping_id', p_endpoint_mapping_id,
                'query_hash', p_query_hash,
                'execution_time_ms', p_execution_time_ms,
                'threshold_ms', v_performance_threshold
            )
        );
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Cache hit ratio calculation function
CREATE OR REPLACE FUNCTION calculate_cache_hit_ratio(
    p_endpoint_mapping_id INTEGER,
    p_time_window_minutes INTEGER DEFAULT 60
)
RETURNS DECIMAL(5,2) AS $$
DECLARE
    v_total_requests INTEGER;
    v_cache_hits INTEGER;
    v_hit_ratio DECIMAL(5,2);
BEGIN
    -- Count total requests
    SELECT COUNT(*) INTO v_total_requests
    FROM api_performance_metrics
    WHERE endpoint_mapping_id = p_endpoint_mapping_id
      AND metric_timestamp > NOW() - INTERVAL '1 minute' * p_time_window_minutes;
    
    -- Count cache hits (this would need to be implemented based on your caching strategy)
    SELECT COUNT(*) INTO v_cache_hits
    FROM api_performance_metrics
    WHERE endpoint_mapping_id = p_endpoint_mapping_id
      AND metric_timestamp > NOW() - INTERVAL '1 minute' * p_time_window_minutes
      AND cache_hit = TRUE;
    
    -- Calculate hit ratio
    IF v_total_requests > 0 THEN
        v_hit_ratio := (v_cache_hits::DECIMAL / v_total_requests::DECIMAL) * 100;
    ELSE
        v_hit_ratio := 0;
    END IF;
    
    -- Update cache configuration
    UPDATE api_cache_config
    SET cache_hit_ratio = v_hit_ratio,
        updated_at = CURRENT_TIMESTAMP
    WHERE endpoint_mapping_id = p_endpoint_mapping_id;
    
    RETURN v_hit_ratio;
END;
$$ LANGUAGE plpgsql;
```

## 🔌 Database Connection Management

### Connection Management Tables

```sql
-- Database connection pool monitoring
CREATE TABLE database_connection_pool (
    id SERIAL PRIMARY KEY,
    pool_name VARCHAR(100) NOT NULL,
    metric_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Pool metrics
    total_connections INTEGER,
    active_connections INTEGER,
    idle_connections INTEGER,
    waiting_connections INTEGER,
    
    -- Connection performance
    avg_connection_time_ms INTEGER,
    avg_query_time_ms INTEGER,
    connection_errors INTEGER,
    
    -- Pool configuration
    max_connections INTEGER,
    min_connections INTEGER,
    connection_timeout_seconds INTEGER,
    idle_timeout_seconds INTEGER,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Connection health monitoring
CREATE TABLE database_connection_health (
    id SERIAL PRIMARY KEY,
    connection_id VARCHAR(100) UNIQUE NOT NULL,
    pool_name VARCHAR(100) NOT NULL,
    
    -- Connection status
    connection_status VARCHAR(20) DEFAULT 'active', -- active, idle, error, closed
    connection_start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_activity_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Connection metrics
    query_count INTEGER DEFAULT 0,
    total_query_time_ms BIGINT DEFAULT 0,
    error_count INTEGER DEFAULT 0,
    
    -- Connection details
    client_host VARCHAR(100),
    client_port INTEGER,
    database_name VARCHAR(100),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Connection failover configuration
CREATE TABLE database_failover_config (
    id SERIAL PRIMARY KEY,
    primary_database VARCHAR(100) NOT NULL,
    replica_database VARCHAR(100) NOT NULL,
    
    -- Failover settings
    failover_enabled BOOLEAN DEFAULT TRUE,
    health_check_interval_seconds INTEGER DEFAULT 30,
    failover_threshold INTEGER DEFAULT 3,
    
    -- Connection settings
    connection_timeout_seconds INTEGER DEFAULT 10,
    read_timeout_seconds INTEGER DEFAULT 30,
    write_timeout_seconds INTEGER DEFAULT 30,
    
    -- Load balancing
    read_distribution_percent INTEGER DEFAULT 80, -- percentage of reads to replica
    write_distribution_percent INTEGER DEFAULT 100, -- percentage of writes to primary
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Connection Management Functions

```sql
-- Database connection health check function
CREATE OR REPLACE FUNCTION check_database_health()
RETURNS TABLE(
    pool_name VARCHAR(100),
    health_status VARCHAR(20),
    active_connections INTEGER,
    total_connections INTEGER,
    connection_utilization_percent DECIMAL(5,2)
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        dcp.pool_name,
        CASE 
            WHEN dcp.active_connections::DECIMAL / dcp.total_connections::DECIMAL > 0.8 THEN 'critical'
            WHEN dcp.active_connections::DECIMAL / dcp.total_connections::DECIMAL > 0.6 THEN 'warning'
            ELSE 'healthy'
        END as health_status,
        dcp.active_connections,
        dcp.total_connections,
        (dcp.active_connections::DECIMAL / dcp.total_connections::DECIMAL) * 100 as connection_utilization_percent
    FROM database_connection_pool dcp
    WHERE dcp.metric_timestamp > NOW() - INTERVAL '5 minutes'
    ORDER BY connection_utilization_percent DESC;
END;
$$ LANGUAGE plpgsql;

-- Connection pool optimization function
CREATE OR REPLACE FUNCTION optimize_connection_pool(
    p_pool_name VARCHAR(100)
)
RETURNS JSONB AS $$
DECLARE
    v_current_utilization DECIMAL(5,2);
    v_recommended_max_connections INTEGER;
    v_recommended_min_connections INTEGER;
    v_result JSONB;
BEGIN
    -- Get current utilization
    SELECT (active_connections::DECIMAL / total_connections::DECIMAL) * 100
    INTO v_current_utilization
    FROM database_connection_pool
    WHERE pool_name = p_pool_name
    ORDER BY metric_timestamp DESC
    LIMIT 1;
    
    -- Calculate recommendations
    IF v_current_utilization > 80 THEN
        v_recommended_max_connections := total_connections * 1.5;
        v_recommended_min_connections := total_connections * 0.3;
    ELSIF v_current_utilization < 30 THEN
        v_recommended_max_connections := total_connections * 0.8;
        v_recommended_min_connections := total_connections * 0.2;
    ELSE
        v_recommended_max_connections := total_connections;
        v_recommended_min_connections := total_connections * 0.25;
    END IF;
    
    v_result := jsonb_build_object(
        'pool_name', p_pool_name,
        'current_utilization_percent', v_current_utilization,
        'recommended_max_connections', v_recommended_max_connections,
        'recommended_min_connections', v_recommended_min_connections,
        'optimization_reason', CASE 
            WHEN v_current_utilization > 80 THEN 'High utilization detected'
            WHEN v_current_utilization < 30 THEN 'Low utilization detected'
            ELSE 'Optimal utilization'
        END
    );
    
    RETURN v_result;
END;
$$ LANGUAGE plpgsql;
```

## 📊 Performance Indexes

```sql
-- Performance indexes for API database integration
CREATE INDEX idx_api_endpoint_mappings_path_method ON api_endpoint_mappings(endpoint_path, http_method);
CREATE INDEX idx_api_error_logs_timestamp ON api_error_logs(error_timestamp DESC);
CREATE INDEX idx_api_error_logs_error_code ON api_error_logs(error_code);
CREATE INDEX idx_api_error_logs_user_id ON api_error_logs(user_id);

CREATE INDEX idx_api_performance_metrics_endpoint_timestamp ON api_performance_metrics(endpoint_path, metric_timestamp DESC);
CREATE INDEX idx_api_performance_metrics_response_time ON api_performance_metrics(avg_response_time_ms DESC);

CREATE INDEX idx_query_optimization_tracking_endpoint ON query_optimization_tracking(endpoint_mapping_id);
CREATE INDEX idx_query_optimization_tracking_hash ON query_optimization_tracking(query_hash);

CREATE INDEX idx_database_connection_pool_timestamp ON database_connection_pool(metric_timestamp DESC);
CREATE INDEX idx_database_connection_health_status ON database_connection_health(connection_status);
CREATE INDEX idx_database_connection_health_last_activity ON database_connection_health(last_activity_time DESC);
```

---

**Tài liệu này cung cấp hướng dẫn hoàn chỉnh cho API database integration, bao gồm endpoint mappings, data validation, error handling, performance optimization, và connection management với best practices cho production deployment.** 