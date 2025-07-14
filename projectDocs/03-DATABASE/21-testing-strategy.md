# Production Database Testing Strategy - AI Camera Counting System

## 📊 Tổng quan

Tài liệu này trình bày chiến lược testing cho database trong môi trường production, bao gồm unit testing, integration testing, performance testing và data migration testing.

## 🎯 Testing Objectives

- **Data Integrity**: Đảm bảo tính toàn vẹn dữ liệu trong mọi scenario
- **Performance**: Kiểm tra hiệu suất database dưới tải cao
- **Reliability**: Đảm bảo độ tin cậy của database operations
- **Security**: Kiểm tra bảo mật database và access control
- **Compliance**: Đảm bảo tuân thủ các quy định về dữ liệu

## 🏗️ Testing Architecture

### Multi-Layer Testing Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              TESTING ARCHITECTURE                               │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              UNIT TESTING LAYER                             │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Function  │  │   Stored    │  │   Trigger   │  │   Constraint│        │ │
│  │  │   Tests     │  │   Procedure │  │   Tests     │  │   Tests     │        │ │
│  │  │             │  │   Tests     │  │             │  │             │        │ │
│  │  │ • Data      │  │ • Business  │  │ • Data      │  │ • Foreign   │        │ │
│  │  │   Validation│  │   Logic     │  │   Integrity │  │   Key       │        │ │
│  │  │ • Input     │  │ • Complex   │  │ • Audit     │  │   Constraints│       │ │
│  │  │   Sanitization│   Queries   │  │   Logging   │  │ • Check      │        │ │
│  │  │ • Output    │  │ • Error     │  │ • Business  │  │   Constraints│       │ │
│  │  │   Formatting│  │   Handling  │  │   Rules     │  │ • Unique    │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                             │
│                                    ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                            INTEGRATION TESTING LAYER                        │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   API       │  │   Cache     │  │   Queue     │  │   External  │        │ │
│  │  │   Integration│  │   Integration│  │   Integration│  │   Service   │        │ │
│  │  │             │  │             │  │             │  │   Integration│        │ │
│  │  │ • REST API  │  │ • Redis     │  │ • RabbitMQ  │  │ • Third-    │        │ │
│  │  │   Endpoints │  │   Cache     │  │   Queues    │  │   Party APIs│        │ │
│  │  │ • GraphQL   │  │ • Cache     │  │ • Message   │  │ • Webhooks  │        │ │
│  │  │   Queries   │  │   Invalidation│   Processing │  │ • File      │        │ │
│  │  │ • Data      │  │ • Cache     │  │ • Dead      │  │   Storage   │        │ │
│  │  │   Flow      │  │   Consistency│   Letter      │  │ • Analytics │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                             │
│                                    ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                            PERFORMANCE TESTING LAYER                        │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Load      │  │   Stress    │  │   Endurance │  │   Scalability│       │ │
│  │  │   Testing   │  │   Testing   │  │   Testing   │  │   Testing   │        │ │
│  │  │             │  │             │  │             │  │             │        │ │
│  │  │ • Normal    │  │ • Peak      │  │ • Long-term │  │ • Horizontal│        │ │
│  │  │   Load      │  │   Load      │  │   Stability │  │   Scaling   │        │ │
│  │  │ • Concurrent│  │ • Resource  │  │ • Memory    │  │ • Vertical  │        │ │
│  │  │   Users     │  │   Limits    │  │   Leaks     │  │   Scaling   │        │ │
│  │  │ • Response  │  │ • Failure   │  │ • Connection│  │ • Database  │        │ │
│  │  │   Times     │  │   Scenarios │  │   Pooling   │  │   Sharding  │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 🧪 Unit Testing Framework

### Database Function Testing

```sql
-- Test framework setup
CREATE SCHEMA IF NOT EXISTS test_framework;

-- Test results table
CREATE TABLE test_framework.test_results (
    id SERIAL PRIMARY KEY,
    test_name VARCHAR(200) NOT NULL,
    test_category VARCHAR(50) NOT NULL,
    test_status VARCHAR(20) NOT NULL, -- PASS, FAIL, ERROR
    test_duration_ms INTEGER,
    error_message TEXT,
    test_data JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Test assertion functions
CREATE OR REPLACE FUNCTION test_framework.assert_equals(
    p_expected ANYELEMENT,
    p_actual ANYELEMENT,
    p_test_name VARCHAR(200)
)
RETURNS BOOLEAN AS $$
BEGIN
    IF p_expected = p_actual THEN
        INSERT INTO test_framework.test_results (test_name, test_category, test_status, test_duration_ms)
        VALUES (p_test_name, 'assertion', 'PASS', 0);
        RETURN TRUE;
    ELSE
        INSERT INTO test_framework.test_results (test_name, test_category, test_status, error_message, test_data)
        VALUES (p_test_name, 'assertion', 'FAIL', 
                'Expected: ' || p_expected || ', Actual: ' || p_actual,
                jsonb_build_object('expected', p_expected, 'actual', p_actual));
        RETURN FALSE;
    END IF;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION test_framework.assert_not_null(
    p_value ANYELEMENT,
    p_test_name VARCHAR(200)
)
RETURNS BOOLEAN AS $$
BEGIN
    IF p_value IS NOT NULL THEN
        INSERT INTO test_framework.test_results (test_name, test_category, test_status, test_duration_ms)
        VALUES (p_test_name, 'assertion', 'PASS', 0);
        RETURN TRUE;
    ELSE
        INSERT INTO test_framework.test_results (test_name, test_category, test_status, error_message)
        VALUES (p_test_name, 'assertion', 'FAIL', 'Value is NULL');
        RETURN FALSE;
    END IF;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION test_framework.assert_exists(
    p_query TEXT,
    p_test_name VARCHAR(200)
)
RETURNS BOOLEAN AS $$
DECLARE
    result_count INTEGER;
BEGIN
    EXECUTE 'SELECT COUNT(*) FROM (' || p_query || ') t' INTO result_count;
    
    IF result_count > 0 THEN
        INSERT INTO test_framework.test_results (test_name, test_category, test_status, test_duration_ms)
        VALUES (p_test_name, 'assertion', 'PASS', 0);
        RETURN TRUE;
    ELSE
        INSERT INTO test_framework.test_results (test_name, test_category, test_status, error_message)
        VALUES (p_test_name, 'assertion', 'FAIL', 'Query returned no results');
        RETURN FALSE;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Test data setup functions
CREATE OR REPLACE FUNCTION test_framework.setup_test_data()
RETURNS VOID AS $$
BEGIN
    -- Create test users
    INSERT INTO users (username, email, password_hash, role, status)
    VALUES 
        ('test_user1', 'test1@example.com', 'hash1', 'user', 'active'),
        ('test_user2', 'test2@example.com', 'hash2', 'admin', 'active'),
        ('test_user3', 'test3@example.com', 'hash3', 'user', 'inactive');
    
    -- Create test cameras
    INSERT INTO cameras (camera_name, location, status, ip_address, model)
    VALUES 
        ('Test Camera 1', 'Test Location 1', 'active', '192.168.1.100', 'Test Model 1'),
        ('Test Camera 2', 'Test Location 2', 'active', '192.168.1.101', 'Test Model 2'),
        ('Test Camera 3', 'Test Location 3', 'inactive', '192.168.1.102', 'Test Model 3');
    
    -- Create test counting results
    INSERT INTO counting_results (camera_id, count_type, count_value, confidence_score)
    VALUES 
        (1, 'people', 5, 0.95),
        (1, 'people', 3, 0.87),
        (2, 'vehicles', 2, 0.92),
        (2, 'vehicles', 1, 0.78);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION test_framework.cleanup_test_data()
RETURNS VOID AS $$
BEGIN
    -- Clean up test data
    DELETE FROM counting_results WHERE camera_id IN (SELECT id FROM cameras WHERE camera_name LIKE 'Test Camera%');
    DELETE FROM cameras WHERE camera_name LIKE 'Test Camera%';
    DELETE FROM users WHERE username LIKE 'test_user%';
END;
$$ LANGUAGE plpgsql;
```

### Unit Test Examples

```sql
-- Test user management functions
CREATE OR REPLACE FUNCTION test_framework.test_user_management()
RETURNS BOOLEAN AS $$
DECLARE
    test_user_id INTEGER;
    test_result BOOLEAN := TRUE;
BEGIN
    -- Setup test data
    PERFORM test_framework.setup_test_data();
    
    -- Test 1: Create user
    INSERT INTO users (username, email, password_hash, role, status)
    VALUES ('test_create_user', 'create@example.com', 'hash', 'user', 'active')
    RETURNING id INTO test_user_id;
    
    test_result := test_result AND test_framework.assert_not_null(test_user_id, 'User creation should return ID');
    test_result := test_result AND test_framework.assert_exists(
        'SELECT 1 FROM users WHERE id = ' || test_user_id,
        'Created user should exist in database'
    );
    
    -- Test 2: Update user
    UPDATE users SET status = 'inactive' WHERE id = test_user_id;
    
    test_result := test_result AND test_framework.assert_equals(
        'inactive',
        (SELECT status FROM users WHERE id = test_user_id),
        'User status should be updated to inactive'
    );
    
    -- Test 3: Delete user
    DELETE FROM users WHERE id = test_user_id;
    
    test_result := test_result AND test_framework.assert_equals(
        0,
        (SELECT COUNT(*) FROM users WHERE id = test_user_id),
        'User should be deleted from database'
    );
    
    -- Cleanup
    PERFORM test_framework.cleanup_test_data();
    
    RETURN test_result;
END;
$$ LANGUAGE plpgsql;

-- Test camera management functions
CREATE OR REPLACE FUNCTION test_framework.test_camera_management()
RETURNS BOOLEAN AS $$
DECLARE
    test_camera_id INTEGER;
    test_result BOOLEAN := TRUE;
BEGIN
    -- Setup test data
    PERFORM test_framework.setup_test_data();
    
    -- Test 1: Create camera
    INSERT INTO cameras (camera_name, location, status, ip_address, model)
    VALUES ('Test Camera Create', 'Test Location', 'active', '192.168.1.200', 'Test Model')
    RETURNING id INTO test_camera_id;
    
    test_result := test_result AND test_framework.assert_not_null(test_camera_id, 'Camera creation should return ID');
    test_result := test_result AND test_framework.assert_exists(
        'SELECT 1 FROM cameras WHERE id = ' || test_camera_id,
        'Created camera should exist in database'
    );
    
    -- Test 2: Update camera status
    UPDATE cameras SET status = 'maintenance' WHERE id = test_camera_id;
    
    test_result := test_result AND test_framework.assert_equals(
        'maintenance',
        (SELECT status FROM cameras WHERE id = test_camera_id),
        'Camera status should be updated to maintenance'
    );
    
    -- Test 3: Camera with counting results
    INSERT INTO counting_results (camera_id, count_type, count_value, confidence_score)
    VALUES (test_camera_id, 'people', 10, 0.95);
    
    test_result := test_result AND test_framework.assert_exists(
        'SELECT 1 FROM counting_results WHERE camera_id = ' || test_camera_id,
        'Camera should have associated counting results'
    );
    
    -- Cleanup
    PERFORM test_framework.cleanup_test_data();
    
    RETURN test_result;
END;
$$ LANGUAGE plpgsql;

-- Test counting results functions
CREATE OR REPLACE FUNCTION test_framework.test_counting_results()
RETURNS BOOLEAN AS $$
DECLARE
    test_result BOOLEAN := TRUE;
    avg_count NUMERIC;
BEGIN
    -- Setup test data
    PERFORM test_framework.setup_test_data();
    
    -- Test 1: Insert counting result
    INSERT INTO counting_results (camera_id, count_type, count_value, confidence_score)
    VALUES (1, 'people', 15, 0.98);
    
    test_result := test_result AND test_framework.assert_exists(
        'SELECT 1 FROM counting_results WHERE camera_id = 1 AND count_value = 15',
        'Counting result should be inserted correctly'
    );
    
    -- Test 2: Calculate average count
    SELECT AVG(count_value) INTO avg_count
    FROM counting_results 
    WHERE camera_id = 1 AND count_type = 'people';
    
    test_result := test_result AND test_framework.assert_equals(
        7.67, -- (5 + 3 + 15) / 3
        ROUND(avg_count, 2),
        'Average count should be calculated correctly'
    );
    
    -- Test 3: High confidence results
    test_result := test_result AND test_framework.assert_equals(
        2,
        (SELECT COUNT(*) FROM counting_results WHERE confidence_score > 0.9),
        'Should have 2 high confidence results'
    );
    
    -- Cleanup
    PERFORM test_framework.cleanup_test_data();
    
    RETURN test_result;
END;
$$ LANGUAGE plpgsql;
```

## 🔗 Integration Testing

### API Integration Tests

```sql
-- API integration test functions
CREATE OR REPLACE FUNCTION test_framework.test_api_integration()
RETURNS BOOLEAN AS $$
DECLARE
    test_result BOOLEAN := TRUE;
    api_response JSONB;
BEGIN
    -- Setup test data
    PERFORM test_framework.setup_test_data();
    
    -- Test 1: REST API - Get cameras
    SELECT build_api_response('success_list', 
        (SELECT jsonb_agg(jsonb_build_object('id', id, 'name', camera_name))
         FROM cameras WHERE status = 'active'),
        'Cameras retrieved successfully'
    ) INTO api_response;
    
    test_result := test_result AND test_framework.assert_equals(
        'success',
        api_response->>'status',
        'API response should have success status'
    );
    
    -- Test 2: GraphQL - Get counting results
    SELECT resolve_get_counting_results(1, NULL, NULL) INTO api_response;
    
    test_result := test_result AND test_framework.assert_not_null(
        api_response,
        'GraphQL resolver should return data'
    );
    
    -- Test 3: Webhook integration
    SELECT deliver_webhook_event(1, 'camera.created', 
        '{"camera_id": 1, "camera_name": "Test Camera"}') INTO api_response;
    
    test_result := test_result AND test_framework.assert_exists(
        'SELECT 1 FROM webhook_events WHERE event_type = ''camera.created''',
        'Webhook event should be created'
    );
    
    -- Cleanup
    PERFORM test_framework.cleanup_test_data();
    
    RETURN test_result;
END;
$$ LANGUAGE plpgsql;

-- Cache integration tests
CREATE OR REPLACE FUNCTION test_framework.test_cache_integration()
RETURNS BOOLEAN AS $$
DECLARE
    test_result BOOLEAN := TRUE;
    cache_key VARCHAR(200);
    cache_value JSONB;
BEGIN
    -- Setup test data
    PERFORM test_framework.setup_test_data();
    
    -- Test 1: Cache key generation
    SELECT get_tenant_cache_key(1, 'cameras') INTO cache_key;
    
    test_result := test_result AND test_framework.assert_equals(
        'tenant_1:cameras',
        cache_key,
        'Cache key should be generated correctly'
    );
    
    -- Test 2: Cache data storage
    SELECT set_cached_result('test_key', '{"data": "test_value"}'::jsonb, 3600) INTO cache_value;
    
    test_result := test_result AND test_framework.assert_exists(
        'SELECT 1 FROM query_cache WHERE cache_key = ''test_key''',
        'Cache data should be stored'
    );
    
    -- Test 3: Cache data retrieval
    SELECT get_cached_result('test_key') INTO cache_value;
    
    test_result := test_result AND test_framework.assert_equals(
        'test_value',
        cache_value->'data',
        'Cache data should be retrieved correctly'
    );
    
    -- Cleanup
    PERFORM test_framework.cleanup_test_data();
    
    RETURN test_result;
END;
$$ LANGUAGE plpgsql;
```

## ⚡ Performance Testing

### Load Testing Framework

```sql
-- Performance test functions
CREATE OR REPLACE FUNCTION test_framework.performance_load_test(
    p_concurrent_users INTEGER DEFAULT 10,
    p_test_duration_seconds INTEGER DEFAULT 60
)
RETURNS TABLE(
    test_name VARCHAR(200),
    avg_response_time NUMERIC,
    max_response_time NUMERIC,
    min_response_time NUMERIC,
    total_requests INTEGER,
    success_rate NUMERIC
) AS $$
DECLARE
    start_time TIMESTAMP;
    end_time TIMESTAMP;
    test_start TIMESTAMP;
    test_end TIMESTAMP;
    response_time INTEGER;
    success_count INTEGER := 0;
    total_count INTEGER := 0;
BEGIN
    start_time := NOW();
    end_time := start_time + (p_test_duration_seconds || ' seconds')::INTERVAL;
    
    -- Simulate concurrent user load
    WHILE NOW() < end_time LOOP
        test_start := clock_timestamp();
        
        -- Simulate database operations
        PERFORM COUNT(*) FROM cameras WHERE status = 'active';
        PERFORM COUNT(*) FROM counting_results WHERE created_at > NOW() - INTERVAL '1 hour';
        PERFORM AVG(count_value) FROM counting_results WHERE camera_id = 1;
        
        test_end := clock_timestamp();
        response_time := EXTRACT(EPOCH FROM (test_end - test_start)) * 1000;
        
        -- Record performance metrics
        INSERT INTO test_framework.test_results (
            test_name, test_category, test_status, test_duration_ms, test_data
        ) VALUES (
            'load_test_query',
            'performance',
            CASE WHEN response_time < 1000 THEN 'PASS' ELSE 'FAIL' END,
            response_time,
            jsonb_build_object('concurrent_users', p_concurrent_users)
        );
        
        total_count := total_count + 1;
        IF response_time < 1000 THEN
            success_count := success_count + 1;
        END IF;
        
        -- Small delay to simulate realistic load
        PERFORM pg_sleep(0.1);
    END LOOP;
    
    -- Return performance summary
    RETURN QUERY
    SELECT 
        'Load Test Summary'::VARCHAR(200),
        ROUND(AVG(test_duration_ms), 2),
        MAX(test_duration_ms),
        MIN(test_duration_ms),
        total_count,
        ROUND((success_count * 100.0) / total_count, 2)
    FROM test_framework.test_results
    WHERE test_name = 'load_test_query'
    AND created_at >= start_time;
END;
$$ LANGUAGE plpgsql;

-- Stress testing function
CREATE OR REPLACE FUNCTION test_framework.performance_stress_test()
RETURNS TABLE(
    test_name VARCHAR(200),
    stress_level VARCHAR(20),
    system_status VARCHAR(20),
    error_count INTEGER
) AS $$
DECLARE
    stress_levels INTEGER[] := ARRAY[10, 50, 100, 200, 500];
    current_level INTEGER;
    error_count INTEGER;
    system_status VARCHAR(20);
BEGIN
    FOREACH current_level IN ARRAY stress_levels
    LOOP
        -- Simulate stress at current level
        error_count := 0;
        
        -- Try to create many concurrent connections/operations
        FOR i IN 1..current_level LOOP
            BEGIN
                -- Simulate heavy database operation
                PERFORM COUNT(*) FROM counting_results;
                PERFORM AVG(count_value) FROM counting_results GROUP BY camera_id;
                PERFORM COUNT(*) FROM cameras WHERE status = 'active';
            EXCEPTION
                WHEN OTHERS THEN
                    error_count := error_count + 1;
            END;
        END LOOP;
        
        -- Determine system status
        system_status := CASE 
            WHEN error_count = 0 THEN 'STABLE'
            WHEN error_count < current_level * 0.1 THEN 'DEGRADED'
            ELSE 'FAILED'
        END;
        
        RETURN QUERY SELECT 
            'Stress Test Level ' || current_level::VARCHAR(200),
            current_level::VARCHAR(20),
            system_status,
            error_count;
    END LOOP;
END;
$$ LANGUAGE plpgsql;
```

## 🔄 Data Migration Testing

### Migration Test Framework

```sql
-- Migration test functions
CREATE OR REPLACE FUNCTION test_framework.test_data_migration()
RETURNS BOOLEAN AS $$
DECLARE
    test_result BOOLEAN := TRUE;
    original_count INTEGER;
    migrated_count INTEGER;
BEGIN
    -- Setup test data
    PERFORM test_framework.setup_test_data();
    
    -- Test 1: Schema migration
    -- Simulate adding a new column
    ALTER TABLE cameras ADD COLUMN IF NOT EXISTS test_migration_column VARCHAR(50);
    
    test_result := test_result AND test_framework.assert_exists(
        'SELECT 1 FROM information_schema.columns WHERE table_name = ''cameras'' AND column_name = ''test_migration_column''',
        'New column should be added to schema'
    );
    
    -- Test 2: Data migration
    -- Simulate data transformation
    UPDATE cameras SET test_migration_column = 'migrated_' || camera_name;
    
    test_result := test_result AND test_framework.assert_exists(
        'SELECT 1 FROM cameras WHERE test_migration_column LIKE ''migrated_%''',
        'Data should be migrated correctly'
    );
    
    -- Test 3: Rollback capability
    -- Simulate rollback
    ALTER TABLE cameras DROP COLUMN IF EXISTS test_migration_column;
    
    test_result := test_result AND test_framework.assert_equals(
        0,
        (SELECT COUNT(*) FROM information_schema.columns WHERE table_name = 'cameras' AND column_name = 'test_migration_column'),
        'Column should be removed during rollback'
    );
    
    -- Cleanup
    PERFORM test_framework.cleanup_test_data();
    
    RETURN test_result;
END;
$$ LANGUAGE plpgsql;

-- Backup and restore testing
CREATE OR REPLACE FUNCTION test_framework.test_backup_restore()
RETURNS BOOLEAN AS $$
DECLARE
    test_result BOOLEAN := TRUE;
    backup_data JSONB;
    restored_count INTEGER;
BEGIN
    -- Setup test data
    PERFORM test_framework.setup_test_data();
    
    -- Test 1: Data backup
    SELECT jsonb_agg(
        jsonb_build_object(
            'id', id,
            'camera_name', camera_name,
            'location', location,
            'status', status
        )
    ) INTO backup_data
    FROM cameras WHERE camera_name LIKE 'Test Camera%';
    
    test_result := test_result AND test_framework.assert_not_null(
        backup_data,
        'Backup data should be created'
    );
    
    -- Test 2: Data restore simulation
    -- Simulate restoring data to a temporary table
    CREATE TEMP TABLE temp_cameras_restore AS
    SELECT * FROM jsonb_populate_recordset(null::cameras, backup_data);
    
    SELECT COUNT(*) INTO restored_count FROM temp_cameras_restore;
    
    test_result := test_result AND test_framework.assert_equals(
        (SELECT COUNT(*) FROM cameras WHERE camera_name LIKE 'Test Camera%'),
        restored_count,
        'Restored data count should match original'
    );
    
    -- Test 3: Data integrity after restore
    test_result := test_result AND test_framework.assert_exists(
        'SELECT 1 FROM temp_cameras_restore WHERE camera_name = ''Test Camera 1''',
        'Restored data should maintain integrity'
    );
    
    -- Cleanup
    DROP TABLE temp_cameras_restore;
    PERFORM test_framework.cleanup_test_data();
    
    RETURN test_result;
END;
$$ LANGUAGE plpgsql;
```

## 📊 Test Execution and Reporting

### Test Runner

```sql
-- Test execution function
CREATE OR REPLACE FUNCTION test_framework.run_all_tests()
RETURNS TABLE(
    test_category VARCHAR(50),
    total_tests INTEGER,
    passed_tests INTEGER,
    failed_tests INTEGER,
    success_rate NUMERIC
) AS $$
DECLARE
    test_functions TEXT[] := ARRAY[
        'test_framework.test_user_management',
        'test_framework.test_camera_management',
        'test_framework.test_counting_results',
        'test_framework.test_api_integration',
        'test_framework.test_cache_integration',
        'test_framework.test_data_migration',
        'test_framework.test_backup_restore'
    ];
    test_function TEXT;
    test_result BOOLEAN;
BEGIN
    -- Clear previous test results
    DELETE FROM test_framework.test_results WHERE created_at < NOW() - INTERVAL '1 hour';
    
    -- Run all test functions
    FOREACH test_function IN ARRAY test_functions
    LOOP
        BEGIN
            EXECUTE 'SELECT ' || test_function || '()' INTO test_result;
            
            -- Record test result
            INSERT INTO test_framework.test_results (test_name, test_category, test_status, test_duration_ms)
            VALUES (test_function, 'integration', 
                    CASE WHEN test_result THEN 'PASS' ELSE 'FAIL' END, 0);
        EXCEPTION
            WHEN OTHERS THEN
                INSERT INTO test_framework.test_results (test_name, test_category, test_status, error_message)
                VALUES (test_function, 'integration', 'ERROR', SQLERRM);
        END;
    END LOOP;
    
    -- Return test summary
    RETURN QUERY
    SELECT 
        test_category,
        COUNT(*) as total_tests,
        COUNT(CASE WHEN test_status = 'PASS' THEN 1 END) as passed_tests,
        COUNT(CASE WHEN test_status IN ('FAIL', 'ERROR') THEN 1 END) as failed_tests,
        ROUND(
            (COUNT(CASE WHEN test_status = 'PASS' THEN 1 END) * 100.0) / COUNT(*), 2
        ) as success_rate
    FROM test_framework.test_results
    WHERE created_at > NOW() - INTERVAL '1 hour'
    GROUP BY test_category
    ORDER BY test_category;
END;
$$ LANGUAGE plpgsql;

-- Test report generation
CREATE OR REPLACE FUNCTION test_framework.generate_test_report()
RETURNS JSONB AS $$
DECLARE
    report JSONB;
BEGIN
    SELECT jsonb_build_object(
        'report_generated_at', NOW(),
        'test_summary', (
            SELECT jsonb_agg(
                jsonb_build_object(
                    'category', test_category,
                    'total_tests', total_tests,
                    'passed_tests', passed_tests,
                    'failed_tests', failed_tests,
                    'success_rate', success_rate
                )
            )
            FROM test_framework.run_all_tests()
        ),
        'recent_failures', (
            SELECT jsonb_agg(
                jsonb_build_object(
                    'test_name', test_name,
                    'error_message', error_message,
                    'created_at', created_at
                )
            )
            FROM test_framework.test_results
            WHERE test_status IN ('FAIL', 'ERROR')
            AND created_at > NOW() - INTERVAL '1 hour'
        ),
        'performance_metrics', (
            SELECT jsonb_build_object(
                'avg_response_time', ROUND(AVG(test_duration_ms), 2),
                'max_response_time', MAX(test_duration_ms),
                'min_response_time', MIN(test_duration_ms)
            )
            FROM test_framework.test_results
            WHERE test_category = 'performance'
            AND created_at > NOW() - INTERVAL '1 hour'
        )
    ) INTO report;
    
    RETURN report;
END;
$$ LANGUAGE plpgsql;
```

---

**Tài liệu này cung cấp framework hoàn chỉnh cho Database Testing Strategy trong môi trường production, đảm bảo chất lượng, độ tin cậy và hiệu suất của hệ thống database.** 