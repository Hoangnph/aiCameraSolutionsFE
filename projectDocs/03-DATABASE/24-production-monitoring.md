# Production-Ready Monitoring & Alerting - AI Camera Counting System

## 📊 Tổng quan

Tài liệu này trình bày hệ thống monitoring và alerting production-ready cho database AI Camera Counting, bao gồm real-time monitoring, alerting, logging và observability với focus đặc biệt vào camera system monitoring.

## 🎯 Monitoring Objectives

- **Real-time Visibility**: Hiển thị trạng thái hệ thống real-time
- **Proactive Alerting**: Cảnh báo sớm trước khi có sự cố
- **Performance Tracking**: Theo dõi hiệu suất và bottlenecks
- **Capacity Planning**: Dự báo nhu cầu tài nguyên
- **Incident Response**: Hỗ trợ xử lý sự cố nhanh chóng
- **Camera Health Monitoring**: Monitoring camera system health
- **Stream Quality Metrics**: Theo dõi chất lượng video stream
- **AI Model Performance**: Monitoring AI model performance
- **Real-time Processing**: Monitoring real-time processing metrics

## 🏗️ Monitoring Architecture

### Multi-Layer Monitoring Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              MONITORING ARCHITECTURE                            │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              DATA COLLECTION LAYER                          │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Database  │  │   Camera    │  │   AI Model  │  │   Business  │        │ │
│  │  │   Metrics   │  │   Metrics   │  │   Metrics   │  │   Metrics   │        │ │
│  │  │             │  │             │  │             │  │             │        │ │
│  │  │ • Query     │  │ • Camera    │  │ • Model     │  │ • User      │        │ │
│  │  │   Performance│  │   Health    │  │   Accuracy  │  │   Activity  │        │ │
│  │  │ • Connection│  │ • Stream    │  │ • Inference │  │ • Revenue   │        │ │
│  │  │   Pool      │  │   Quality   │  │   Latency   │  │ • Conversion│        │ │
│  │  │ • Lock      │  │ • Frame     │  │ • Model     │  │   Rates     │        │ │
│  │  │   Contention│  │   Processing│  │   Drift     │  │ • SLA       │        │ │
│  │  │ • Cache     │  │ • Detection │  │ • A/B Test  │  │   Metrics   │        │ │
│  │  │   Hit Rate  │  │   Accuracy  │  │   Results   │  │             │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                             │
│                                    ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              PROCESSING LAYER                               │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Data      │  │   Aggregation│  │   Correlation│  │   Anomaly   │        │ │
│  │  │   Validation│  │   & Storage │  │   Engine    │  │   Detection │        │ │
│  │  │             │  │             │  │             │  │             │        │ │
│  │  │ • Schema    │  │ • Time-     │  │ • Cross-    │  │ • Machine   │        │ │
│  │  │   Validation│  │   Series    │  │   Service   │  │   Learning  │        │ │
│  │  │ • Data      │  │   Database  │  │   Correlation│  │   Models    │        │ │
│  │  │   Quality   │  │ • Metrics   │  │ • Root      │  │ • Statistical│       │ │
│  │  │ • Outlier   │  │   Aggregation│  │   Cause     │  │   Analysis  │        │ │
│  │  │   Detection │  │ • Data      │  │   Analysis  │  │ • Pattern   │        │ │
│  │  │ • Duplicate │  │   Retention │  │ • Impact    │  │   Recognition│       │ │
│  │  │   Detection │  │   Policies  │  │   Assessment│  │ • Predictive│        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                             │
│                                    ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              ALERTING LAYER                                 │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Alert     │  │   Escalation│  │   Notification│  │   Incident  │        │ │
│  │  │   Rules     │  │   Engine    │  │   System    │  │   Management│        │ │
│  │  │             │  │             │  │             │  │             │        │ │
│  │  │ • Threshold │  │ • Time-     │  │ • Email     │  │ • Incident  │        │ │
│  │  │   Based     │  │   Based     │  │   Alerts    │  │   Creation  │        │ │
│  │  │ • Trend     │  │   Escalation│  │ • SMS       │  │ • Assignment│        │ │
│  │  │   Based     │  │ • Role-     │  │   Alerts    │  │ • Tracking  │        │ │
│  │  │ • Anomaly   │  │   Based     │  │ • Slack     │  │ • Resolution│        │ │
│  │  │   Based     │  │   Escalation│  │   Integration│  │ • Post-     │        │ │
│  │  │ • Composite │  │ • Auto-     │  │ • Webhook   │  │   Incident  │        │ │
│  │  │   Rules     │  │   Recovery  │  │   Alerts    │  │   Analysis  │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 📹 Camera System Monitoring

### 1. Camera Health Monitoring

**Mục đích**: Monitoring sức khỏe của camera system và phát hiện sự cố sớm.

```sql
-- Camera Health Monitoring Table
CREATE TABLE camera_health_monitoring (
    id SERIAL PRIMARY KEY,
    camera_id VARCHAR(100) REFERENCES camera_configurations(camera_id),
    metric_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Camera Status
    camera_status VARCHAR(20), -- online, offline, error, maintenance
    last_heartbeat TIMESTAMP,
    uptime_percentage DECIMAL(5,2),
    response_time_ms INTEGER,
    
    -- Stream Health
    stream_status VARCHAR(20), -- active, inactive, error
    stream_quality_score DECIMAL(3,2), -- 0.0 to 1.0
    frame_drop_rate DECIMAL(5,2), -- percentage
    bitrate_variance DECIMAL(5,2),
    latency_ms INTEGER,
    
    -- Processing Health
    detection_processing_rate_fps DECIMAL(8,2),
    tracking_processing_rate_fps DECIMAL(8,2),
    counting_processing_rate_fps DECIMAL(8,2),
    
    -- Error Tracking
    error_count INTEGER DEFAULT 0,
    last_error_message TEXT,
    last_error_timestamp TIMESTAMP,
    error_severity VARCHAR(20), -- low, medium, high, critical
    
    -- Performance Metrics
    cpu_usage_percent DECIMAL(5,2),
    memory_usage_percent DECIMAL(5,2),
    disk_usage_percent DECIMAL(5,2),
    network_bandwidth_mbps DECIMAL(8,2),
    
    -- Maintenance
    last_maintenance_date DATE,
    next_maintenance_date DATE,
    maintenance_notes TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Camera Health Alert Function
CREATE OR REPLACE FUNCTION check_camera_health_alerts()
RETURNS TABLE(
    camera_id VARCHAR(100),
    alert_type VARCHAR(50),
    alert_message TEXT,
    alert_severity VARCHAR(20)
) AS $$
BEGIN
    -- Check offline cameras
    RETURN QUERY
    SELECT 
        chm.camera_id,
        'camera_offline'::VARCHAR(50) as alert_type,
        'Camera is offline for more than 5 minutes'::TEXT as alert_message,
        'critical'::VARCHAR(20) as alert_severity
    FROM camera_health_monitoring chm
    WHERE chm.last_heartbeat < NOW() - INTERVAL '5 minutes'
      AND chm.camera_status != 'offline'
    
    UNION ALL
    
    -- Check poor stream quality
    SELECT 
        chm.camera_id,
        'poor_stream_quality'::VARCHAR(50),
        'Stream quality score is below 0.7'::TEXT,
        'warning'::VARCHAR(20)
    FROM camera_health_monitoring chm
    WHERE chm.stream_quality_score < 0.7
      AND chm.metric_timestamp > NOW() - INTERVAL '10 minutes'
    
    UNION ALL
    
    -- Check high error rates
    SELECT 
        chm.camera_id,
        'high_error_rate'::VARCHAR(50),
        'High error rate detected'::TEXT,
        'error'::VARCHAR(20)
    FROM camera_health_monitoring chm
    WHERE chm.error_count > 10
      AND chm.metric_timestamp > NOW() - INTERVAL '1 hour'
    
    UNION ALL
    
    -- Check performance issues
    SELECT 
        chm.camera_id,
        'performance_degradation'::VARCHAR(50),
        'Camera performance is degraded'::TEXT,
        'warning'::VARCHAR(20)
    FROM camera_health_monitoring chm
    WHERE chm.cpu_usage_percent > 80
       OR chm.memory_usage_percent > 80
       OR chm.disk_usage_percent > 90;
END;
$$ LANGUAGE plpgsql;
```

### 2. Stream Quality Metrics

**Mục đích**: Monitoring chất lượng video stream và phát hiện degradation.

```sql
-- Stream Quality Monitoring Table
CREATE TABLE stream_quality_monitoring (
    id SERIAL PRIMARY KEY,
    stream_id VARCHAR(100) REFERENCES video_streams(stream_id),
    camera_id VARCHAR(100) REFERENCES camera_configurations(camera_id),
    metric_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Quality Metrics
    quality_score DECIMAL(3,2), -- 0.0 to 1.0
    bitrate INTEGER, -- kbps
    frame_rate DECIMAL(5,2),
    resolution_width INTEGER,
    resolution_height INTEGER,
    
    -- Performance Metrics
    latency_ms INTEGER,
    jitter_ms INTEGER,
    packet_loss_percent DECIMAL(5,2),
    frame_drop_rate DECIMAL(5,2),
    
    -- Error Metrics
    error_count INTEGER,
    error_types JSONB,
    connection_drops INTEGER,
    
    -- Network Metrics
    bandwidth_utilization_percent DECIMAL(5,2),
    network_latency_ms INTEGER,
    network_jitter_ms INTEGER,
    
    -- Quality Indicators
    blur_detection_score DECIMAL(3,2),
    noise_level DECIMAL(3,2),
    compression_artifacts DECIMAL(3,2),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Stream Quality Alert Function
CREATE OR REPLACE FUNCTION check_stream_quality_alerts()
RETURNS TABLE(
    stream_id VARCHAR(100),
    camera_id VARCHAR(100),
    alert_type VARCHAR(50),
    alert_message TEXT,
    alert_severity VARCHAR(20)
) AS $$
BEGIN
    -- Check poor quality streams
    RETURN QUERY
    SELECT 
        sqm.stream_id,
        sqm.camera_id,
        'poor_stream_quality'::VARCHAR(50) as alert_type,
        'Stream quality score is below threshold'::TEXT as alert_message,
        'warning'::VARCHAR(20) as alert_severity
    FROM stream_quality_monitoring sqm
    WHERE sqm.quality_score < 0.6
      AND sqm.metric_timestamp > NOW() - INTERVAL '5 minutes'
    
    UNION ALL
    
    -- Check high latency
    SELECT 
        sqm.stream_id,
        sqm.camera_id,
        'high_latency'::VARCHAR(50),
        'Stream latency is above 1000ms'::TEXT,
        'error'::VARCHAR(20)
    FROM stream_quality_monitoring sqm
    WHERE sqm.latency_ms > 1000
      AND sqm.metric_timestamp > NOW() - INTERVAL '5 minutes'
    
    UNION ALL
    
    -- Check high frame drop rate
    SELECT 
        sqm.stream_id,
        sqm.camera_id,
        'high_frame_drops'::VARCHAR(50),
        'Frame drop rate is above 10%'::TEXT,
        'warning'::VARCHAR(20)
    FROM stream_quality_monitoring sqm
    WHERE sqm.frame_drop_rate > 10.0
      AND sqm.metric_timestamp > NOW() - INTERVAL '5 minutes'
    
    UNION ALL
    
    -- Check connection issues
    SELECT 
        sqm.stream_id,
        sqm.camera_id,
        'connection_issues'::VARCHAR(50),
        'Multiple connection drops detected'::TEXT,
        'critical'::VARCHAR(20)
    FROM stream_quality_monitoring sqm
    WHERE sqm.connection_drops > 5
      AND sqm.metric_timestamp > NOW() - INTERVAL '1 hour';
END;
$$ LANGUAGE plpgsql;
```

### 3. AI Model Performance Monitoring

**Mục đích**: Monitoring performance của AI models và phát hiện degradation.

```sql
-- AI Model Performance Monitoring Table
CREATE TABLE ai_model_performance_monitoring (
    id SERIAL PRIMARY KEY,
    model_id VARCHAR(100) REFERENCES ai_models(model_id),
    model_version VARCHAR(50),
    metric_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Performance Metrics
    inference_latency_ms INTEGER,
    throughput_fps DECIMAL(8,2),
    gpu_utilization_percent DECIMAL(5,2),
    memory_usage_mb DECIMAL(8,2),
    
    -- Accuracy Metrics
    accuracy_score DECIMAL(5,2),
    precision_score DECIMAL(5,2),
    recall_score DECIMAL(5,2),
    f1_score DECIMAL(5,2),
    
    -- Quality Metrics
    false_positive_rate DECIMAL(5,2),
    false_negative_rate DECIMAL(5,2),
    detection_rate DECIMAL(5,2),
    
    -- Drift Detection
    data_drift_score DECIMAL(3,2), -- 0.0 to 1.0
    concept_drift_score DECIMAL(3,2),
    model_drift_score DECIMAL(3,2),
    
    -- Business Metrics
    cost_per_inference DECIMAL(8,4),
    revenue_per_inference DECIMAL(8,4),
    roi_percentage DECIMAL(8,2),
    
    -- Error Tracking
    inference_errors INTEGER,
    model_loading_time_ms INTEGER,
    model_availability_percent DECIMAL(5,2),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- AI Model Performance Alert Function
CREATE OR REPLACE FUNCTION check_ai_model_alerts()
RETURNS TABLE(
    model_id VARCHAR(100),
    alert_type VARCHAR(50),
    alert_message TEXT,
    alert_severity VARCHAR(20)
) AS $$
BEGIN
    -- Check model drift
    RETURN QUERY
    SELECT 
        ampm.model_id,
        'model_drift'::VARCHAR(50) as alert_type,
        'Model drift detected'::TEXT as alert_message,
        'warning'::VARCHAR(20) as alert_severity
    FROM ai_model_performance_monitoring ampm
    WHERE ampm.model_drift_score > 0.8
      AND ampm.metric_timestamp > NOW() - INTERVAL '1 hour'
    
    UNION ALL
    
    -- Check accuracy degradation
    SELECT 
        ampm.model_id,
        'accuracy_degradation'::VARCHAR(50),
        'Model accuracy has degraded significantly'::TEXT,
        'error'::VARCHAR(20)
    FROM ai_model_performance_monitoring ampm
    WHERE ampm.accuracy_score < 0.7
      AND ampm.metric_timestamp > NOW() - INTERVAL '1 hour'
    
    UNION ALL
    
    -- Check high latency
    SELECT 
        ampm.model_id,
        'high_inference_latency'::VARCHAR(50),
        'Inference latency is above 200ms'::TEXT,
        'warning'::VARCHAR(20)
    FROM ai_model_performance_monitoring ampm
    WHERE ampm.inference_latency_ms > 200
      AND ampm.metric_timestamp > NOW() - INTERVAL '5 minutes'
    
    UNION ALL
    
    -- Check low throughput
    SELECT 
        ampm.model_id,
        'low_throughput'::VARCHAR(50),
        'Model throughput is below 25 FPS'::TEXT,
        'warning'::VARCHAR(20)
    FROM ai_model_performance_monitoring ampm
    WHERE ampm.throughput_fps < 25
      AND ampm.metric_timestamp > NOW() - INTERVAL '5 minutes';
END;
$$ LANGUAGE plpgsql;
```

### 4. Real-time Processing Metrics

**Mục đích**: Monitoring real-time processing performance và bottlenecks.

```sql
-- Real-time Processing Monitoring Table
CREATE TABLE realtime_processing_monitoring (
    id SERIAL PRIMARY KEY,
    camera_id VARCHAR(100) REFERENCES camera_configurations(camera_id),
    metric_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Processing Performance
    ingestion_rate_fps DECIMAL(8,2),
    processing_rate_fps DECIMAL(8,2),
    output_rate_fps DECIMAL(8,2),
    
    -- Latency Metrics
    ingestion_latency_ms INTEGER,
    processing_latency_ms INTEGER,
    total_latency_ms INTEGER,
    
    -- Queue Metrics
    input_queue_size INTEGER,
    processing_queue_size INTEGER,
    output_queue_size INTEGER,
    queue_wait_time_ms INTEGER,
    
    -- Resource Usage
    cpu_usage_percent DECIMAL(5,2),
    memory_usage_percent DECIMAL(5,2),
    gpu_usage_percent DECIMAL(5,2),
    network_bandwidth_mbps DECIMAL(8,2),
    
    -- Error Metrics
    processing_errors INTEGER,
    dropped_frames INTEGER,
    retry_count INTEGER,
    
    -- Quality Metrics
    processing_quality_score DECIMAL(3,2),
    data_loss_percent DECIMAL(5,2),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Real-time Processing Alert Function
CREATE OR REPLACE FUNCTION check_realtime_processing_alerts()
RETURNS TABLE(
    camera_id VARCHAR(100),
    alert_type VARCHAR(50),
    alert_message TEXT,
    alert_severity VARCHAR(20)
) AS $$
BEGIN
    -- Check processing bottlenecks
    RETURN QUERY
    SELECT 
        rpm.camera_id,
        'processing_bottleneck'::VARCHAR(50) as alert_type,
        'Processing rate is below ingestion rate'::TEXT as alert_message,
        'warning'::VARCHAR(20) as alert_severity
    FROM realtime_processing_monitoring rpm
    WHERE rpm.processing_rate_fps < rpm.ingestion_rate_fps * 0.8
      AND rpm.metric_timestamp > NOW() - INTERVAL '5 minutes'
    
    UNION ALL
    
    -- Check high latency
    SELECT 
        rpm.camera_id,
        'high_processing_latency'::VARCHAR(50),
        'Processing latency is above 500ms'::TEXT,
        'error'::VARCHAR(20)
    FROM realtime_processing_monitoring rpm
    WHERE rpm.total_latency_ms > 500
      AND rpm.metric_timestamp > NOW() - INTERVAL '5 minutes'
    
    UNION ALL
    
    -- Check queue overflow
    SELECT 
        rpm.camera_id,
        'queue_overflow'::VARCHAR(50),
        'Processing queue is overflowing'::TEXT,
        'critical'::VARCHAR(20)
    FROM realtime_processing_monitoring rpm
    WHERE rpm.processing_queue_size > 1000
      AND rpm.metric_timestamp > NOW() - INTERVAL '5 minutes'
    
    UNION ALL
    
    -- Check high error rate
    SELECT 
        rpm.camera_id,
        'high_error_rate'::VARCHAR(50),
        'High processing error rate detected'::TEXT,
        'error'::VARCHAR(20)
    FROM realtime_processing_monitoring rpm
    WHERE rpm.processing_errors > 10
      AND rpm.metric_timestamp > NOW() - INTERVAL '1 hour';
END;
$$ LANGUAGE plpgsql;
```

## 📊 Database Monitoring System

### Database Metrics Collection

```sql
-- Database monitoring tables
CREATE TABLE monitoring_metrics (
    id SERIAL PRIMARY KEY,
    metric_name VARCHAR(100) NOT NULL,
    metric_value NUMERIC NOT NULL,
    metric_unit VARCHAR(20),
    metric_category VARCHAR(50) NOT NULL, -- performance, availability, capacity, security
    metric_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metric_labels JSONB DEFAULT '{}'::jsonb,
    source_system VARCHAR(50) DEFAULT 'database'
);

-- Database performance metrics
CREATE TABLE database_performance_metrics (
    id SERIAL PRIMARY KEY,
    collection_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    active_connections INTEGER,
    idle_connections INTEGER,
    total_connections INTEGER,
    max_connections INTEGER,
    connection_utilization_percent DECIMAL(5,2),
    queries_per_second NUMERIC,
    slow_queries_count INTEGER,
    avg_query_time_ms NUMERIC,
    max_query_time_ms NUMERIC,
    cache_hit_ratio DECIMAL(5,2),
    buffer_hit_ratio DECIMAL(5,2),
    index_hit_ratio DECIMAL(5,2),
    deadlocks_count INTEGER,
    locks_count INTEGER,
    checkpoint_writes INTEGER,
    wal_generated_bytes BIGINT,
    vacuum_count INTEGER,
    autovacuum_count INTEGER
);

-- Database capacity metrics
CREATE TABLE database_capacity_metrics (
    id SERIAL PRIMARY KEY,
    collection_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    database_size_bytes BIGINT,
    table_sizes JSONB,
    index_sizes JSONB,
    free_space_bytes BIGINT,
    disk_usage_percent DECIMAL(5,2),
    table_bloat_percent DECIMAL(5,2),
    index_bloat_percent DECIMAL(5,2),
    transaction_log_size_bytes BIGINT,
    backup_size_bytes BIGINT,
    replication_lag_seconds INTEGER
);

-- Database availability metrics
CREATE TABLE database_availability_metrics (
    id SERIAL PRIMARY KEY,
    collection_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    uptime_seconds BIGINT,
    downtime_seconds BIGINT,
    availability_percent DECIMAL(5,2),
    last_restart_time TIMESTAMP,
    planned_maintenance_count INTEGER,
    unplanned_outage_count INTEGER,
    mttr_minutes INTEGER, -- Mean Time To Recovery
    mtbf_hours INTEGER,   -- Mean Time Between Failures
    replication_status VARCHAR(20),
    backup_status VARCHAR(20),
    recovery_point_objective_seconds INTEGER,
    recovery_time_objective_minutes INTEGER
);

-- Database security metrics
CREATE TABLE database_security_metrics (
    id SERIAL PRIMARY KEY,
    collection_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    failed_login_attempts INTEGER,
    successful_logins INTEGER,
    suspicious_activities INTEGER,
    privilege_escalation_attempts INTEGER,
    data_access_violations INTEGER,
    encryption_status VARCHAR(20),
    ssl_connections_count INTEGER,
    non_ssl_connections_count INTEGER,
    audit_log_entries_count INTEGER,
    security_incidents_count INTEGER
);

-- Metrics collection functions
CREATE OR REPLACE FUNCTION collect_database_metrics()
RETURNS VOID AS $$
DECLARE
    active_conns INTEGER;
    idle_conns INTEGER;
    total_conns INTEGER;
    max_conns INTEGER;
    cache_hit_ratio DECIMAL(5,2);
    buffer_hit_ratio DECIMAL(5,2);
    slow_queries INTEGER;
    avg_query_time NUMERIC;
BEGIN
    -- Collect connection metrics
    SELECT 
        COUNT(*) FILTER (WHERE state = 'active'),
        COUNT(*) FILTER (WHERE state = 'idle'),
        COUNT(*),
        setting::integer
    INTO active_conns, idle_conns, total_conns, max_conns
    FROM pg_stat_activity, pg_settings 
    WHERE name = 'max_connections';
    
    -- Collect cache hit ratios
    SELECT 
        ROUND((SUM(heap_blks_hit) * 100.0) / (SUM(heap_blks_hit) + SUM(heap_blks_read)), 2),
        ROUND((SUM(idx_blks_hit) * 100.0) / (SUM(idx_blks_hit) + SUM(idx_blks_read)), 2)
    INTO buffer_hit_ratio, cache_hit_ratio
    FROM pg_statio_user_tables, pg_statio_user_indexes;
    
    -- Collect query performance metrics
    SELECT 
        COUNT(*) FILTER (WHERE mean_time > 1000),
        AVG(mean_time)
    INTO slow_queries, avg_query_time
    FROM pg_stat_statements;
    
    -- Insert performance metrics
    INSERT INTO database_performance_metrics (
        active_connections, idle_connections, total_connections, max_connections,
        connection_utilization_percent, cache_hit_ratio, buffer_hit_ratio,
        slow_queries_count, avg_query_time_ms
    ) VALUES (
        active_conns, idle_conns, total_conns, max_conns,
        ROUND((total_conns * 100.0) / max_conns, 2),
        cache_hit_ratio, buffer_hit_ratio,
        slow_queries, avg_query_time
    );
    
    -- Insert into general metrics table
    INSERT INTO monitoring_metrics (metric_name, metric_value, metric_unit, metric_category, metric_labels)
    VALUES 
        ('active_connections', active_conns, 'connections', 'performance', '{"component": "database"}'),
        ('connection_utilization', ROUND((total_conns * 100.0) / max_conns, 2), 'percent', 'performance', '{"component": "database"}'),
        ('cache_hit_ratio', cache_hit_ratio, 'percent', 'performance', '{"component": "database"}'),
        ('slow_queries', slow_queries, 'queries', 'performance', '{"component": "database"}');
END;
$$ LANGUAGE plpgsql;

-- Capacity metrics collection
CREATE OR REPLACE FUNCTION collect_capacity_metrics()
RETURNS VOID AS $$
DECLARE
    db_size BIGINT;
    free_space BIGINT;
    table_sizes JSONB;
    index_sizes JSONB;
BEGIN
    -- Get database size
    SELECT pg_database_size(current_database()) INTO db_size;
    
    -- Get table sizes
    SELECT jsonb_object_agg(tablename, pg_total_relation_size(tablename::regclass))
    INTO table_sizes
    FROM pg_tables 
    WHERE schemaname = 'public';
    
    -- Get index sizes
    SELECT jsonb_object_agg(indexname, pg_relation_size(indexname::regclass))
    INTO index_sizes
    FROM pg_indexes 
    WHERE schemaname = 'public';
    
    -- Insert capacity metrics
    INSERT INTO database_capacity_metrics (
        database_size_bytes, table_sizes, index_sizes
    ) VALUES (
        db_size, table_sizes, index_sizes
    );
    
    -- Insert into general metrics table
    INSERT INTO monitoring_metrics (metric_name, metric_value, metric_unit, metric_category, metric_labels)
    VALUES 
        ('database_size', db_size, 'bytes', 'capacity', '{"component": "database"}'),
        ('table_count', jsonb_array_length(table_sizes), 'tables', 'capacity', '{"component": "database"}'),
        ('index_count', jsonb_array_length(index_sizes), 'indexes', 'capacity', '{"component": "database"}');
END;
$$ LANGUAGE plpgsql;
```

## 🚨 Alerting System

### 1. Alert Rules Configuration

```sql
-- Alert Rules Table
CREATE TABLE alert_rules (
    id SERIAL PRIMARY KEY,
    rule_name VARCHAR(100) UNIQUE NOT NULL,
    rule_description TEXT,
    
    -- Rule Configuration
    metric_name VARCHAR(100) NOT NULL,
    threshold_value NUMERIC NOT NULL,
    comparison_operator VARCHAR(10) NOT NULL, -- >, <, >=, <=, =, !=
    time_window_minutes INTEGER DEFAULT 5,
    evaluation_frequency_minutes INTEGER DEFAULT 1,
    
    -- Alert Configuration
    alert_severity VARCHAR(20) DEFAULT 'warning', -- info, warning, error, critical
    alert_message_template TEXT,
    alert_channels JSONB, -- email, sms, slack, webhook
    
    -- Escalation
    escalation_enabled BOOLEAN DEFAULT TRUE,
    escalation_delay_minutes INTEGER DEFAULT 15,
    escalation_channels JSONB,
    
    -- Status
    is_active BOOLEAN DEFAULT TRUE,
    last_evaluated TIMESTAMP,
    last_triggered TIMESTAMP,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Camera-specific Alert Rules
INSERT INTO alert_rules (rule_name, rule_description, metric_name, threshold_value, comparison_operator, alert_severity, alert_message_template) VALUES
('camera_offline', 'Camera offline for more than 5 minutes', 'camera_uptime_percentage', 0, '=', 'critical', 'Camera {camera_id} is offline'),
('poor_stream_quality', 'Stream quality below 0.7', 'stream_quality_score', 0.7, '<', 'warning', 'Stream quality for camera {camera_id} is poor'),
('high_processing_latency', 'Processing latency above 500ms', 'processing_latency_ms', 500, '>', 'error', 'High processing latency for camera {camera_id}'),
('ai_model_drift', 'AI model drift detected', 'model_drift_score', 0.8, '>', 'warning', 'Model drift detected for model {model_id}'),
('database_high_connections', 'Database connections above 80%', 'connection_utilization_percent', 80, '>', 'warning', 'High database connection utilization');
```

### 2. Alert Management

```sql
-- Alerts Table
CREATE TABLE alerts (
    id SERIAL PRIMARY KEY,
    alert_rule_id INTEGER REFERENCES alert_rules(id),
    
    -- Alert Details
    alert_type VARCHAR(50) NOT NULL,
    alert_severity VARCHAR(20) NOT NULL,
    alert_message TEXT NOT NULL,
    alert_data JSONB,
    
    -- Context
    camera_id VARCHAR(100),
    model_id VARCHAR(100),
    metric_value NUMERIC,
    threshold_value NUMERIC,
    
    -- Status
    status VARCHAR(20) DEFAULT 'active', -- active, acknowledged, resolved, closed
    acknowledged_at TIMESTAMP,
    acknowledged_by INTEGER REFERENCES users(id),
    resolved_at TIMESTAMP,
    resolved_by INTEGER REFERENCES users(id),
    
    -- Timestamps
    triggered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Alert Resolution Function
CREATE OR REPLACE FUNCTION resolve_alert(
    p_alert_id INTEGER,
    p_resolved_by INTEGER,
    p_resolution_notes TEXT DEFAULT NULL
)
RETURNS BOOLEAN AS $$
BEGIN
    UPDATE alerts
    SET 
        status = 'resolved',
        resolved_at = CURRENT_TIMESTAMP,
        resolved_by = p_resolved_by,
        last_updated = CURRENT_TIMESTAMP
    WHERE id = p_alert_id;
    
    -- Log resolution
    INSERT INTO alert_resolution_log (
        alert_id, resolved_by, resolution_notes, resolution_time
    ) VALUES (
        p_alert_id, p_resolved_by, p_resolution_notes, CURRENT_TIMESTAMP
    );
    
    RETURN FOUND;
END;
$$ LANGUAGE plpgsql;
```

## 📈 Monitoring Dashboard

### 1. Camera System Dashboard Query

```sql
-- Camera System Health Dashboard
WITH camera_health_summary AS (
    SELECT 
        COUNT(*) as total_cameras,
        COUNT(*) FILTER (WHERE camera_status = 'online') as online_cameras,
        COUNT(*) FILTER (WHERE camera_status = 'offline') as offline_cameras,
        COUNT(*) FILTER (WHERE camera_status = 'error') as error_cameras,
        AVG(stream_quality_score) as avg_stream_quality,
        AVG(uptime_percentage) as avg_uptime
    FROM camera_health_monitoring
    WHERE metric_timestamp > NOW() - INTERVAL '1 hour'
),
ai_model_summary AS (
    SELECT 
        COUNT(DISTINCT model_id) as total_models,
        AVG(accuracy_score) as avg_accuracy,
        AVG(inference_latency_ms) as avg_latency,
        COUNT(*) FILTER (WHERE model_drift_score > 0.8) as models_with_drift
    FROM ai_model_performance_monitoring
    WHERE metric_timestamp > NOW() - INTERVAL '1 hour'
),
processing_summary AS (
    SELECT 
        COUNT(DISTINCT camera_id) as active_cameras,
        AVG(processing_rate_fps) as avg_processing_rate,
        AVG(total_latency_ms) as avg_latency,
        SUM(processing_errors) as total_errors
    FROM realtime_processing_monitoring
    WHERE metric_timestamp > NOW() - INTERVAL '1 hour'
)
SELECT 
    chs.total_cameras,
    chs.online_cameras,
    chs.offline_cameras,
    chs.error_cameras,
    ROUND(chs.avg_stream_quality, 3) as avg_stream_quality,
    ROUND(chs.avg_uptime, 2) as avg_uptime_percent,
    ams.total_models,
    ROUND(ams.avg_accuracy, 3) as avg_model_accuracy,
    ROUND(ams.avg_latency, 0) as avg_model_latency_ms,
    ams.models_with_drift,
    ps.active_cameras,
    ROUND(ps.avg_processing_rate, 2) as avg_processing_fps,
    ROUND(ps.avg_latency, 0) as avg_processing_latency_ms,
    ps.total_errors
FROM camera_health_summary chs
CROSS JOIN ai_model_summary ams
CROSS JOIN processing_summary ps;
```

### 2. Real-time Alert Dashboard

```sql
-- Real-time Alert Dashboard
WITH active_alerts AS (
    SELECT 
        alert_type,
        alert_severity,
        COUNT(*) as alert_count,
        MIN(triggered_at) as first_alert,
        MAX(triggered_at) as last_alert
    FROM alerts
    WHERE status = 'active'
      AND triggered_at > NOW() - INTERVAL '24 hours'
    GROUP BY alert_type, alert_severity
),
alert_trends AS (
    SELECT 
        alert_type,
        DATE_TRUNC('hour', triggered_at) as hour,
        COUNT(*) as alert_count
    FROM alerts
    WHERE triggered_at > NOW() - INTERVAL '24 hours'
    GROUP BY alert_type, DATE_TRUNC('hour', triggered_at)
)
SELECT 
    aa.alert_type,
    aa.alert_severity,
    aa.alert_count,
    aa.first_alert,
    aa.last_alert,
    CASE 
        WHEN aa.alert_severity = 'critical' THEN '🔴'
        WHEN aa.alert_severity = 'error' THEN '🟠'
        WHEN aa.alert_severity = 'warning' THEN '🟡'
        ELSE '🟢'
    END as severity_icon
FROM active_alerts aa
ORDER BY 
    CASE aa.alert_severity
        WHEN 'critical' THEN 1
        WHEN 'error' THEN 2
        WHEN 'warning' THEN 3
        ELSE 4
    END,
    aa.alert_count DESC;
```

---

**Tài liệu này cung cấp hệ thống monitoring và alerting hoàn chỉnh cho AI Camera Counting System, bao gồm camera health monitoring, stream quality metrics, AI model performance monitoring, real-time processing metrics, và comprehensive alerting system với enterprise-grade monitoring capabilities.** 