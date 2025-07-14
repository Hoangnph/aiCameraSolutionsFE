# Production API Integration Patterns - AI Camera Counting System

## 📊 Tổng quan

Tài liệu này trình bày các patterns tích hợp API cho hệ thống AI Camera Counting trong môi trường production, bao gồm REST API, GraphQL, webhooks và third-party integrations.

## 🎯 API Integration Objectives

- **Standardization**: Chuẩn hóa API design patterns và response formats
- **Scalability**: Hỗ trợ high-throughput API requests
- **Security**: Bảo mật API endpoints và data transmission
- **Monitoring**: Theo dõi API performance và usage
- **Versioning**: Quản lý API versions và backward compatibility

## 🏗️ API Architecture

### Multi-Layer API Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              API INTEGRATION ARCHITECTURE                       │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              API GATEWAY LAYER                              │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Rate      │  │   Auth      │  │   Request   │  │   Response  │        │ │
│  │  │   Limiting  │  │   & Auth    │  │   Routing   │  │   Caching   │        │ │
│  │  │             │  │             │  │             │  │             │        │ │
│  │  │ • Per-user  │  │ • JWT       │  │ • Path      │  │ • ETag      │        │ │
│  │  │   limits    │  │   Tokens    │  │   matching  │  │   Caching   │        │ │
│  │  │ • Per-API   │  │ • API Keys  │  │ • Method    │  │ • Response  │        │ │
│  │  │   limits    │  │ • OAuth 2.0 │  │   routing   │  │   Compression│       │ │
│  │  │ • Burst     │  │ • Role-based│  │ • Load      │  │ • CORS      │        │ │
│  │  │   control   │  │   access    │  │   balancing │  │   Headers   │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                             │
│                                    ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              API SERVICE LAYER                              │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   REST API  │  │   GraphQL   │  │   WebSocket │  │   Webhook   │        │ │
│  │  │   Services  │  │   Services  │  │   Services  │  │   Services  │        │ │
│  │  │             │  │             │  │             │  │             │        │ │
│  │  │ • CRUD      │  │ • Query     │  │ • Real-time │  │ • Event     │        │ │
│  │  │   Operations│  │   Language  │  │   Updates   │  │   Delivery  │        │ │
│  │  │ • Resource  │  │ • Schema    │  │ • Live      │  │ • HTTP      │        │ │
│  │  │   Endpoints │  │   Introspection│   Streaming │  │   Callbacks │        │ │
│  │  │ • HTTP      │  │ • Resolvers │  │ • Bi-       │  │ • Retry     │        │ │
│  │  │   Methods   │  │ • Mutations │  │   directional│  │   Logic     │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                             │
│                                    ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              DATA ACCESS LAYER                              │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Query     │  │   Cache     │  │   Validation│  │   Response  │        │ │
│  │  │   Builder   │  │   Layer     │  │   Layer     │  │   Builder   │        │ │
│  │  │             │  │             │  │             │  │             │        │ │
│  │  │ • Dynamic   │  │ • Redis     │  │ • Input     │  │ • JSON      │        │ │
│  │  │   Queries   │  │   Cache     │  │   Validation│  │   Response  │        │ │
│  │  │ • Query     │  │ • Response  │  │ • Schema    │  │ • XML       │        │ │
│  │  │   Optimization│   Caching   │  │   Validation│  │   Response  │        │ │
│  │  │ • Parameter │  │ • Cache     │  │ • Business  │  │ • Error     │        │ │
│  │  │   Binding   │  │   Invalidation│   Rules     │  │   Handling  │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 🔌 REST API Design

### REST API Endpoints Structure

```sql
-- API endpoints registry
CREATE TABLE api_endpoints (
    id SERIAL PRIMARY KEY,
    endpoint_path VARCHAR(255) NOT NULL,
    http_method VARCHAR(10) NOT NULL, -- GET, POST, PUT, DELETE, PATCH
    api_version VARCHAR(10) NOT NULL, -- v1, v2, v3
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    rate_limit_per_minute INTEGER DEFAULT 100,
    requires_auth BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(endpoint_path, http_method, api_version)
);

-- Define API endpoints
INSERT INTO api_endpoints VALUES
-- Camera Management
(1, '/api/v1/cameras', 'GET', 'v1', 'List all cameras', TRUE, 100, TRUE),
(2, '/api/v1/cameras', 'POST', 'v1', 'Create new camera', TRUE, 50, TRUE),
(3, '/api/v1/cameras/{id}', 'GET', 'v1', 'Get camera details', TRUE, 200, TRUE),
(4, '/api/v1/cameras/{id}', 'PUT', 'v1', 'Update camera', TRUE, 50, TRUE),
(5, '/api/v1/cameras/{id}', 'DELETE', 'v1', 'Delete camera', TRUE, 20, TRUE),

-- Counting Results
(6, '/api/v1/counting-results', 'GET', 'v1', 'List counting results', TRUE, 200, TRUE),
(7, '/api/v1/counting-results', 'POST', 'v1', 'Create counting result', TRUE, 100, TRUE),
(8, '/api/v1/counting-results/{id}', 'GET', 'v1', 'Get counting result', TRUE, 300, TRUE),
(9, '/api/v1/counting-results/analytics', 'GET', 'v1', 'Get analytics data', TRUE, 50, TRUE),

-- Real-time Data
(10, '/api/v1/streams/{camera_id}/live', 'GET', 'v1', 'Live camera stream', TRUE, 1000, TRUE),
(11, '/api/v1/streams/{camera_id}/counts', 'GET', 'v1', 'Real-time counts', TRUE, 500, TRUE),

-- User Management
(12, '/api/v1/users', 'GET', 'v1', 'List users', TRUE, 50, TRUE),
(13, '/api/v1/users', 'POST', 'v1', 'Create user', TRUE, 20, TRUE),
(14, '/api/v1/users/{id}', 'GET', 'v1', 'Get user details', TRUE, 100, TRUE),
(15, '/api/v1/users/{id}', 'PUT', 'v1', 'Update user', TRUE, 20, TRUE),
(16, '/api/v1/users/{id}', 'DELETE', 'v1', 'Delete user', TRUE, 10, TRUE);

-- API response templates
CREATE TABLE api_response_templates (
    id SERIAL PRIMARY KEY,
    template_name VARCHAR(100) NOT NULL,
    template_type VARCHAR(20) NOT NULL, -- success, error, pagination
    response_structure JSONB NOT NULL,
    status_code INTEGER NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Define response templates
INSERT INTO api_response_templates VALUES
(1, 'success_single', 'success', 
 '{"status": "success", "data": {}, "message": "string", "timestamp": "string"}', 
 200, 'Single resource success response'),

(2, 'success_list', 'success', 
 '{"status": "success", "data": [], "pagination": {"page": 1, "limit": 10, "total": 100}, "message": "string", "timestamp": "string"}', 
 200, 'List resource success response'),

(3, 'error_validation', 'error', 
 '{"status": "error", "error": {"code": "VALIDATION_ERROR", "message": "string", "details": []}, "timestamp": "string"}', 
 400, 'Validation error response'),

(4, 'error_not_found', 'error', 
 '{"status": "error", "error": {"code": "NOT_FOUND", "message": "string"}, "timestamp": "string"}', 
 404, 'Resource not found error response'),

(5, 'error_unauthorized', 'error', 
 '{"status": "error", "error": {"code": "UNAUTHORIZED", "message": "string"}, "timestamp": "string"}', 
 401, 'Unauthorized error response');
```

### REST API Implementation

```sql
-- API request logging
CREATE TABLE api_requests (
    id SERIAL PRIMARY KEY,
    endpoint_id INTEGER REFERENCES api_endpoints(id),
    user_id INTEGER REFERENCES users(id),
    tenant_id INTEGER,
    request_method VARCHAR(10) NOT NULL,
    request_path VARCHAR(255) NOT NULL,
    request_headers JSONB,
    request_body TEXT,
    response_status INTEGER,
    response_time_ms INTEGER,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- API rate limiting
CREATE TABLE api_rate_limits (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    endpoint_id INTEGER REFERENCES api_endpoints(id),
    request_count INTEGER DEFAULT 1,
    window_start TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- API response builder function
CREATE OR REPLACE FUNCTION build_api_response(
    p_template_name VARCHAR(100),
    p_data JSONB DEFAULT NULL,
    p_message TEXT DEFAULT NULL,
    p_error_code VARCHAR(50) DEFAULT NULL,
    p_error_message TEXT DEFAULT NULL,
    p_error_details JSONB DEFAULT NULL
)
RETURNS JSONB AS $$
DECLARE
    template_record RECORD;
    response JSONB;
BEGIN
    -- Get response template
    SELECT * INTO template_record
    FROM api_response_templates
    WHERE template_name = p_template_name;
    
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Response template not found: %', p_template_name;
    END IF;
    
    -- Build response based on template type
    CASE template_record.template_type
        WHEN 'success' THEN
            response := template_record.response_structure;
            response := jsonb_set(response, '{data}', COALESCE(p_data, '{}'::jsonb));
            response := jsonb_set(response, '{message}', to_jsonb(COALESCE(p_message, '')));
            response := jsonb_set(response, '{timestamp}', to_jsonb(NOW()::text));
            
        WHEN 'error' THEN
            response := template_record.response_structure;
            response := jsonb_set(response, '{error,code}', to_jsonb(COALESCE(p_error_code, 'UNKNOWN_ERROR')));
            response := jsonb_set(response, '{error,message}', to_jsonb(COALESCE(p_error_message, 'An error occurred')));
            IF p_error_details IS NOT NULL THEN
                response := jsonb_set(response, '{error,details}', p_error_details);
            END IF;
            response := jsonb_set(response, '{timestamp}', to_jsonb(NOW()::text));
            
        ELSE
            RAISE EXCEPTION 'Unknown template type: %', template_record.template_type;
    END CASE;
    
    RETURN response;
END;
$$ LANGUAGE plpgsql;
```

## 🔍 GraphQL Implementation

### GraphQL Schema Design

```sql
-- GraphQL schema registry
CREATE TABLE graphql_schemas (
    id SERIAL PRIMARY KEY,
    schema_name VARCHAR(100) NOT NULL,
    schema_version VARCHAR(10) NOT NULL,
    schema_definition TEXT NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- GraphQL queries registry
CREATE TABLE graphql_queries (
    id SERIAL PRIMARY KEY,
    query_name VARCHAR(100) NOT NULL,
    query_type VARCHAR(20) NOT NULL, -- query, mutation, subscription
    query_definition TEXT NOT NULL,
    resolver_function VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    rate_limit_per_minute INTEGER DEFAULT 100,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Define GraphQL queries
INSERT INTO graphql_queries VALUES
(1, 'getCameras', 'query', 
 'query GetCameras($limit: Int, $offset: Int) {
    cameras(limit: $limit, offset: $offset) {
      id
      name
      location
      status
      lastActivity
      countingResults {
        id
        countValue
        confidenceScore
        createdAt
      }
    }
  }', 
 'resolve_get_cameras', TRUE, 100),

(2, 'getCountingResults', 'query',
 'query GetCountingResults($cameraId: ID, $startDate: DateTime, $endDate: DateTime) {
    countingResults(cameraId: $cameraId, startDate: $startDate, endDate: $endDate) {
      id
      cameraId
      countType
      countValue
      confidenceScore
      createdAt
      camera {
        name
        location
      }
    }
  }',
 'resolve_get_counting_results', TRUE, 200),

(3, 'createCamera', 'mutation',
 'mutation CreateCamera($input: CameraInput!) {
    createCamera(input: $input) {
      id
      name
      location
      status
      createdAt
    }
  }',
 'resolve_create_camera', TRUE, 50),

(4, 'updateCountingResult', 'mutation',
 'mutation UpdateCountingResult($id: ID!, $input: CountingResultInput!) {
    updateCountingResult(id: $id, input: $input) {
      id
      countValue
      confidenceScore
      updatedAt
    }
  }',
 'resolve_update_counting_result', TRUE, 100);

-- GraphQL resolver functions
CREATE OR REPLACE FUNCTION resolve_get_cameras(
    p_limit INTEGER DEFAULT 10,
    p_offset INTEGER DEFAULT 0
)
RETURNS JSONB AS $$
DECLARE
    result JSONB;
BEGIN
    SELECT jsonb_agg(
        jsonb_build_object(
            'id', c.id,
            'name', c.camera_name,
            'location', c.location,
            'status', c.status,
            'lastActivity', c.updated_at,
            'countingResults', (
                SELECT jsonb_agg(
                    jsonb_build_object(
                        'id', cr.id,
                        'countValue', cr.count_value,
                        'confidenceScore', cr.confidence_score,
                        'createdAt', cr.created_at
                    )
                )
                FROM counting_results cr
                WHERE cr.camera_id = c.id
                AND cr.created_at > NOW() - INTERVAL '24 hours'
                LIMIT 10
            )
        )
    ) INTO result
    FROM cameras c
    WHERE c.status = 'active'
    LIMIT p_limit
    OFFSET p_offset;
    
    RETURN COALESCE(result, '[]'::jsonb);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION resolve_get_counting_results(
    p_camera_id INTEGER DEFAULT NULL,
    p_start_date TIMESTAMP DEFAULT NULL,
    p_end_date TIMESTAMP DEFAULT NULL
)
RETURNS JSONB AS $$
DECLARE
    result JSONB;
    where_clause TEXT := 'WHERE 1=1';
BEGIN
    IF p_camera_id IS NOT NULL THEN
        where_clause := where_clause || ' AND cr.camera_id = ' || p_camera_id;
    END IF;
    
    IF p_start_date IS NOT NULL THEN
        where_clause := where_clause || ' AND cr.created_at >= ''' || p_start_date || '''';
    END IF;
    
    IF p_end_date IS NOT NULL THEN
        where_clause := where_clause || ' AND cr.created_at <= ''' || p_end_date || '''';
    END IF;
    
    EXECUTE format('
        SELECT jsonb_agg(
            jsonb_build_object(
                ''id'', cr.id,
                ''cameraId'', cr.camera_id,
                ''countType'', cr.count_type,
                ''countValue'', cr.count_value,
                ''confidenceScore'', cr.confidence_score,
                ''createdAt'', cr.created_at,
                ''camera'', jsonb_build_object(
                    ''name'', c.camera_name,
                    ''location'', c.location
                )
            )
        )
        FROM counting_results cr
        JOIN cameras c ON cr.camera_id = c.id
        %s
        ORDER BY cr.created_at DESC
        LIMIT 1000
    ', where_clause) INTO result;
    
    RETURN COALESCE(result, '[]'::jsonb);
END;
$$ LANGUAGE plpgsql;
```

## 🔗 Webhook Integration

### Webhook Management System

```sql
-- Webhook endpoints
CREATE TABLE webhook_endpoints (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER REFERENCES tenants(id),
    endpoint_name VARCHAR(100) NOT NULL,
    endpoint_url VARCHAR(500) NOT NULL,
    event_types TEXT[] NOT NULL, -- ['camera.created', 'counting_result.created', 'alert.triggered']
    http_method VARCHAR(10) DEFAULT 'POST',
    headers JSONB DEFAULT '{}'::jsonb,
    is_active BOOLEAN DEFAULT TRUE,
    retry_count INTEGER DEFAULT 3,
    timeout_seconds INTEGER DEFAULT 30,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Webhook events
CREATE TABLE webhook_events (
    id SERIAL PRIMARY KEY,
    endpoint_id INTEGER REFERENCES webhook_endpoints(id),
    event_type VARCHAR(100) NOT NULL,
    event_data JSONB NOT NULL,
    status VARCHAR(20) DEFAULT 'pending', -- pending, sent, failed, retrying
    response_status INTEGER,
    response_body TEXT,
    retry_count INTEGER DEFAULT 0,
    next_retry_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sent_at TIMESTAMP
);

-- Webhook delivery function
CREATE OR REPLACE FUNCTION deliver_webhook_event(
    p_endpoint_id INTEGER,
    p_event_type VARCHAR(100),
    p_event_data JSONB
)
RETURNS INTEGER AS $$
DECLARE
    event_id INTEGER;
    endpoint_record RECORD;
BEGIN
    -- Get endpoint details
    SELECT * INTO endpoint_record
    FROM webhook_endpoints
    WHERE id = p_endpoint_id AND is_active = TRUE;
    
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Webhook endpoint not found or inactive: %', p_endpoint_id;
    END IF;
    
    -- Check if event type is supported
    IF NOT (p_event_type = ANY(endpoint_record.event_types)) THEN
        RAISE EXCEPTION 'Event type not supported: %', p_event_type;
    END IF;
    
    -- Create webhook event
    INSERT INTO webhook_events (endpoint_id, event_type, event_data)
    VALUES (p_endpoint_id, p_event_type, p_event_data)
    RETURNING id INTO event_id;
    
    -- Schedule immediate delivery
    PERFORM pg_notify('webhook_delivery', json_build_object(
        'event_id', event_id,
        'endpoint_url', endpoint_record.endpoint_url,
        'event_type', p_event_type,
        'event_data', p_event_data
    )::text);
    
    RETURN event_id;
END;
$$ LANGUAGE plpgsql;

-- Webhook retry function
CREATE OR REPLACE FUNCTION retry_failed_webhooks()
RETURNS INTEGER AS $$
DECLARE
    retry_count INTEGER := 0;
    event_record RECORD;
BEGIN
    FOR event_record IN 
        SELECT we.*, wep.endpoint_url, wep.retry_count as max_retries
        FROM webhook_events we
        JOIN webhook_endpoints wep ON we.endpoint_id = wep.id
        WHERE we.status = 'failed'
        AND we.retry_count < wep.retry_count
        AND (we.next_retry_at IS NULL OR we.next_retry_at <= NOW())
        AND wep.is_active = TRUE
    LOOP
        -- Update retry count and status
        UPDATE webhook_events 
        SET retry_count = retry_count + 1,
            status = 'retrying',
            next_retry_at = NOW() + (retry_count * INTERVAL '5 minutes')
        WHERE id = event_record.id;
        
        -- Schedule retry delivery
        PERFORM pg_notify('webhook_delivery', json_build_object(
            'event_id', event_record.id,
            'endpoint_url', event_record.endpoint_url,
            'event_type', event_record.event_type,
            'event_data', event_record.event_data,
            'retry_count', event_record.retry_count + 1
        )::text);
        
        retry_count := retry_count + 1;
    END LOOP;
    
    RETURN retry_count;
END;
$$ LANGUAGE plpgsql;
```

## 🔄 Third-Party Integrations

### Integration Management

```sql
-- Third-party integrations
CREATE TABLE third_party_integrations (
    id SERIAL PRIMARY KEY,
    integration_name VARCHAR(100) NOT NULL,
    integration_type VARCHAR(50) NOT NULL, -- 'analytics', 'notification', 'storage', 'ai_service'
    provider_name VARCHAR(100) NOT NULL,
    api_endpoint VARCHAR(500),
    api_key VARCHAR(255),
    api_secret VARCHAR(255),
    config JSONB DEFAULT '{}'::jsonb,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Integration events
CREATE TABLE integration_events (
    id SERIAL PRIMARY KEY,
    integration_id INTEGER REFERENCES third_party_integrations(id),
    event_type VARCHAR(100) NOT NULL,
    event_data JSONB NOT NULL,
    status VARCHAR(20) DEFAULT 'pending', -- pending, sent, failed, completed
    response_data JSONB,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed_at TIMESTAMP
);

-- Define common integrations
INSERT INTO third_party_integrations VALUES
(1, 'google_analytics', 'analytics', 'Google', 
 'https://analytics.google.com/analytics/web/', 
 'your-api-key', 'your-api-secret',
 '{"tracking_id": "GA-XXXXXXXXX", "custom_dimensions": {}}', TRUE),

(2, 'slack_notifications', 'notification', 'Slack',
 'https://hooks.slack.com/services/XXX/YYY/ZZZ',
 'your-webhook-url', NULL,
 '{"channel": "#alerts", "username": "AI Camera Bot"}', TRUE),

(3, 'aws_s3_storage', 'storage', 'Amazon Web Services',
 'https://s3.amazonaws.com',
 'your-access-key', 'your-secret-key',
 '{"bucket_name": "camera-data", "region": "us-east-1"}', TRUE),

(4, 'openai_ai_service', 'ai_service', 'OpenAI',
 'https://api.openai.com/v1',
 'your-api-key', NULL,
 '{"model": "gpt-4", "max_tokens": 1000}', TRUE);

-- Integration event handler
CREATE OR REPLACE FUNCTION handle_integration_event(
    p_integration_name VARCHAR(100),
    p_event_type VARCHAR(100),
    p_event_data JSONB
)
RETURNS INTEGER AS $$
DECLARE
    integration_record RECORD;
    event_id INTEGER;
BEGIN
    -- Get integration details
    SELECT * INTO integration_record
    FROM third_party_integrations
    WHERE integration_name = p_integration_name AND is_active = TRUE;
    
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Integration not found or inactive: %', p_integration_name;
    END IF;
    
    -- Create integration event
    INSERT INTO integration_events (integration_id, event_type, event_data)
    VALUES (integration_record.id, p_event_type, p_event_data)
    RETURNING id INTO event_id;
    
    -- Process based on integration type
    CASE integration_record.integration_type
        WHEN 'analytics' THEN
            PERFORM process_analytics_integration(integration_record, p_event_data);
        WHEN 'notification' THEN
            PERFORM process_notification_integration(integration_record, p_event_data);
        WHEN 'storage' THEN
            PERFORM process_storage_integration(integration_record, p_event_data);
        WHEN 'ai_service' THEN
            PERFORM process_ai_service_integration(integration_record, p_event_data);
        ELSE
            RAISE EXCEPTION 'Unknown integration type: %', integration_record.integration_type;
    END CASE;
    
    -- Update event status
    UPDATE integration_events 
    SET status = 'completed', processed_at = NOW()
    WHERE id = event_id;
    
    RETURN event_id;
END;
$$ LANGUAGE plpgsql;
```

## 📊 API Monitoring and Analytics

### API Performance Monitoring

```sql
-- API performance metrics
CREATE VIEW api_performance_metrics AS
SELECT 
    endpoint_path,
    http_method,
    api_version,
    COUNT(*) as total_requests,
    AVG(response_time_ms) as avg_response_time,
    MAX(response_time_ms) as max_response_time,
    MIN(response_time_ms) as min_response_time,
    COUNT(CASE WHEN response_status >= 400 THEN 1 END) as error_count,
    ROUND(
        (COUNT(CASE WHEN response_status >= 400 THEN 1 END) * 100.0) / COUNT(*), 2
    ) as error_rate,
    COUNT(DISTINCT user_id) as unique_users,
    COUNT(DISTINCT ip_address) as unique_ips
FROM api_requests ar
JOIN api_endpoints ae ON ar.endpoint_id = ae.id
WHERE ar.created_at > NOW() - INTERVAL '24 hours'
GROUP BY endpoint_path, http_method, api_version
ORDER BY total_requests DESC;

-- API usage analytics
CREATE VIEW api_usage_analytics AS
SELECT 
    DATE_TRUNC('hour', created_at) as hour_bucket,
    endpoint_path,
    COUNT(*) as request_count,
    AVG(response_time_ms) as avg_response_time,
    COUNT(CASE WHEN response_status >= 400 THEN 1 END) as error_count
FROM api_requests ar
JOIN api_endpoints ae ON ar.endpoint_id = ae.id
WHERE ar.created_at > NOW() - INTERVAL '7 days'
GROUP BY DATE_TRUNC('hour', created_at), endpoint_path
ORDER BY hour_bucket DESC, request_count DESC;

-- API rate limiting monitoring
CREATE VIEW api_rate_limit_violations AS
SELECT 
    ar.user_id,
    u.username,
    ae.endpoint_path,
    COUNT(*) as request_count,
    ae.rate_limit_per_minute as limit_per_minute,
    arl.window_start,
    arl.window_start + INTERVAL '1 minute' as window_end
FROM api_rate_limits arl
JOIN api_endpoints ae ON arl.endpoint_id = ae.id
JOIN api_requests ar ON arl.user_id = ar.user_id AND arl.endpoint_id = ar.endpoint_id
JOIN users u ON ar.user_id = u.id
WHERE arl.request_count > ae.rate_limit_per_minute
AND arl.window_start > NOW() - INTERVAL '1 hour'
GROUP BY ar.user_id, u.username, ae.endpoint_path, ae.rate_limit_per_minute, arl.window_start
ORDER BY request_count DESC;
```

### API Health Monitoring

```sql
-- API health check function
CREATE OR REPLACE FUNCTION check_api_health()
RETURNS TABLE(
    endpoint_path VARCHAR(255),
    health_status VARCHAR(20),
    avg_response_time NUMERIC,
    error_rate NUMERIC,
    last_request TIMESTAMP
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        ae.endpoint_path,
        CASE 
            WHEN ar.avg_response_time > 5000 THEN 'CRITICAL'
            WHEN ar.avg_response_time > 2000 THEN 'WARNING'
            WHEN ar.error_rate > 10 THEN 'ERROR'
            ELSE 'HEALTHY'
        END as health_status,
        ROUND(ar.avg_response_time, 2) as avg_response_time,
        ROUND(ar.error_rate, 2) as error_rate,
        ar.last_request
    FROM api_endpoints ae
    LEFT JOIN (
        SELECT 
            endpoint_id,
            AVG(response_time_ms) as avg_response_time,
            ROUND(
                (COUNT(CASE WHEN response_status >= 400 THEN 1 END) * 100.0) / COUNT(*), 2
            ) as error_rate,
            MAX(created_at) as last_request
        FROM api_requests
        WHERE created_at > NOW() - INTERVAL '1 hour'
        GROUP BY endpoint_id
    ) ar ON ae.id = ar.endpoint_id
    WHERE ae.is_active = TRUE
    ORDER BY health_status DESC, avg_response_time DESC;
END;
$$ LANGUAGE plpgsql;
```

---

**Tài liệu này cung cấp framework hoàn chỉnh cho API Integration Patterns trong môi trường production, đảm bảo scalability, security và monitoring cho hệ thống API.** 