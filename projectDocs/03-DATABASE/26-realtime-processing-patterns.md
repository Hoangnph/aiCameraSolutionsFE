# Real-time Processing Patterns - AI Camera Counting System

## 📊 Tổng quan

Tài liệu này trình bày database patterns cho real-time video processing và analytics trong hệ thống AI Camera Counting, bao gồm real-time data ingestion, stream processing, time-series optimization, và event-driven patterns.

## 🎯 Mục tiêu

- **Real-time Data Ingestion**: Xử lý dữ liệu video stream real-time
- **Stream Processing**: Database patterns cho stream processing
- **Time-series Optimization**: Tối ưu cho time-series data
- **Real-time Aggregation**: Aggregation patterns cho real-time analytics
- **Event-driven Architecture**: Event-driven database patterns

## 🏗️ Real-time Processing Architecture

### Real-time Data Flow Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              REAL-TIME PROCESSING ARCHITECTURE                  │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              DATA INGESTION LAYER                           │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Video     │  │   Frame     │  │   Metadata  │  │   Quality   │        │ │
│  │  │   Stream    │  │   Buffer    │  │   Extractor │  │   Monitor   │        │ │
│  │  │             │  │             │  │             │  │             │        │ │
│  │  │ • RTSP      │  │ • Frame     │  │ • Timestamp │  │ • Bitrate   │        │ │
│  │  │   Stream    │  │   Queue     │  │ • Location  │  │ • FPS       │        │ │
│  │  │ • HTTP      │  │ • Priority  │  │ • Weather   │  │ • Latency   │        │ │
│  │  │   Stream    │  │   Queue     │  │ • Events    │  │ • Jitter    │        │ │
│  │  │ • WebRTC    │  │ • Batch     │  │ • Context   │  │ • Quality   │        │ │
│  │  │   Stream    │  │   Queue     │  │ • Metadata  │  │   Score     │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                             │
│                                    ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              PROCESSING LAYER                               │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   AI Model  │  │   Detection │  │   Tracking  │  │   Counting  │        │ │
│  │  │   Processor │  │   Engine    │  │   Engine    │  │   Engine    │        │ │
│  │  │             │  │             │  │             │  │             │        │ │
│  │  │ • Model     │  │ • Person    │  │ • Object    │  │ • Line      │        │ │
│  │  │   Inference │  │   Detection │  │   Tracking  │  │   Crossing  │        │ │
│  │  │ • Batch     │  │ • Bounding  │  │ • Trajectory│  │ • Zone      │        │ │
│  │  │   Processing│  │   Box       │  │ • Velocity  │  │   Counting  │        │ │
│  │  │ • GPU       │  │ • Confidence│  │ • Prediction│  │ • Density   │        │ │
│  │  │   Acceleration│  │ • Multi-    │  │ • Occlusion │  │   Mapping   │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                             │
│                                    ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              STORAGE LAYER                                  │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Real-time │  │   Time-     │  │   Event     │  │   Analytics │        │ │
│  │  │   Cache     │  │   Series    │  │   Store     │  │   Store     │        │ │
│  │  │             │  │   Database  │  │             │  │             │        │ │
│  │  │ • Redis     │  │ • InfluxDB  │  │ • Event     │  │ • Aggregated│        │ │
│  │  │   Cache     │  │ • Timescale │  │   Log       │  │   Data      │        │ │
│  │  │ • Memory    │  │   DB        │  │ • Stream    │  │ • Metrics   │        │ │
│  │  │   Cache     │  │ • PostgreSQL│  │   Processing│  │ • Reports   │        │ │
│  │  │ • LRU       │  │   Time-     │  │ • CQRS      │  │ • Dashboards│        │ │
│  │  │   Cache     │  │   Series    │  │   Pattern   │  │ • KPIs      │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 📥 Real-time Data Ingestion Patterns

### High-Speed Data Ingestion

```sql
-- Real-time data ingestion tables
CREATE TABLE realtime_data_ingestion (
    id SERIAL PRIMARY KEY,
    ingestion_id VARCHAR(100) UNIQUE NOT NULL,
    camera_id VARCHAR(100) NOT NULL,
    stream_id VARCHAR(100) NOT NULL,
    
    -- Ingestion metadata
    ingestion_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    frame_timestamp TIMESTAMP NOT NULL,
    frame_number BIGINT NOT NULL,
    
    -- Data payload
    data_type VARCHAR(50) NOT NULL, -- frame, detection, tracking, counting
    data_payload JSONB NOT NULL,
    data_size_bytes INTEGER,
    
    -- Processing status
    processing_status VARCHAR(20) DEFAULT 'pending', -- pending, processing, completed, failed
    processing_priority INTEGER DEFAULT 0,
    retry_count INTEGER DEFAULT 0,
    
    -- Performance metrics
    ingestion_latency_ms INTEGER,
    processing_latency_ms INTEGER,
    total_latency_ms INTEGER,
    
    -- Error handling
    error_message TEXT,
    error_code VARCHAR(50),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- High-performance ingestion queue
CREATE TABLE ingestion_queue (
    id SERIAL PRIMARY KEY,
    queue_id VARCHAR(100) UNIQUE NOT NULL,
    queue_type VARCHAR(50) NOT NULL, -- high_priority, normal, batch
    
    -- Queue configuration
    max_size INTEGER DEFAULT 10000,
    current_size INTEGER DEFAULT 0,
    processing_rate INTEGER DEFAULT 1000, -- items per second
    
    -- Queue status
    is_active BOOLEAN DEFAULT TRUE,
    is_paused BOOLEAN DEFAULT FALSE,
    last_processed_at TIMESTAMP,
    
    -- Performance metrics
    avg_processing_time_ms DECIMAL(8,2),
    error_rate DECIMAL(5,2),
    throughput_items_per_sec DECIMAL(8,2),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Queue items
CREATE TABLE queue_items (
    id SERIAL PRIMARY KEY,
    queue_id VARCHAR(100) REFERENCES ingestion_queue(queue_id),
    item_priority INTEGER DEFAULT 0,
    
    -- Item data
    item_type VARCHAR(50) NOT NULL,
    item_data JSONB NOT NULL,
    item_size_bytes INTEGER,
    
    -- Processing status
    status VARCHAR(20) DEFAULT 'queued', -- queued, processing, completed, failed
    attempts INTEGER DEFAULT 0,
    max_attempts INTEGER DEFAULT 3,
    
    -- Timestamps
    queued_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processing_started_at TIMESTAMP,
    completed_at TIMESTAMP,
    
    -- Error handling
    error_message TEXT,
    error_code VARCHAR(50),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Real-time ingestion monitoring
CREATE TABLE ingestion_monitoring (
    id SERIAL PRIMARY KEY,
    camera_id VARCHAR(100) NOT NULL,
    metric_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Ingestion metrics
    ingestion_rate_fps DECIMAL(8,2),
    ingestion_latency_ms INTEGER,
    ingestion_throughput_mbps DECIMAL(8,2),
    
    -- Queue metrics
    queue_size INTEGER,
    queue_processing_rate INTEGER,
    queue_wait_time_ms INTEGER,
    
    -- Error metrics
    error_count INTEGER,
    error_rate DECIMAL(5,2),
    retry_count INTEGER,
    
    -- Performance metrics
    cpu_usage_percent DECIMAL(5,2),
    memory_usage_percent DECIMAL(5,2),
    network_bandwidth_mbps DECIMAL(8,2),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Optimized Ingestion Functions

```sql
-- High-performance ingestion function
CREATE OR REPLACE FUNCTION ingest_realtime_data(
    p_camera_id VARCHAR(100),
    p_stream_id VARCHAR(100),
    p_frame_timestamp TIMESTAMP,
    p_frame_number BIGINT,
    p_data_type VARCHAR(50),
    p_data_payload JSONB
)
RETURNS VARCHAR(100) AS $$
DECLARE
    v_ingestion_id VARCHAR(100);
    v_start_time TIMESTAMP;
    v_ingestion_latency INTEGER;
BEGIN
    v_start_time := NOW();
    
    -- Generate unique ingestion ID
    v_ingestion_id := p_camera_id || '_' || p_frame_number || '_' || EXTRACT(EPOCH FROM p_frame_timestamp);
    
    -- Insert into real-time ingestion table
    INSERT INTO realtime_data_ingestion (
        ingestion_id, camera_id, stream_id, frame_timestamp, frame_number,
        data_type, data_payload, data_size_bytes, ingestion_latency_ms
    ) VALUES (
        v_ingestion_id, p_camera_id, p_stream_id, p_frame_timestamp, p_frame_number,
        p_data_type, p_data_payload, jsonb_array_length(p_data_payload),
        EXTRACT(EPOCH FROM (NOW() - v_start_time)) * 1000
    );
    
    -- Add to processing queue
    INSERT INTO queue_items (queue_id, item_type, item_data, item_priority)
    VALUES (
        'high_priority',
        'realtime_processing',
        jsonb_build_object(
            'ingestion_id', v_ingestion_id,
            'camera_id', p_camera_id,
            'data_type', p_data_type
        ),
        CASE 
            WHEN p_data_type = 'detection' THEN 10
            WHEN p_data_type = 'tracking' THEN 8
            WHEN p_data_type = 'counting' THEN 9
            ELSE 5
        END
    );
    
    RETURN v_ingestion_id;
END;
$$ LANGUAGE plpgsql;

-- Batch ingestion function for high throughput
CREATE OR REPLACE FUNCTION batch_ingest_data(
    p_data_batch JSONB
)
RETURNS INTEGER AS $$
DECLARE
    v_item JSONB;
    v_count INTEGER := 0;
BEGIN
    -- Process batch of data
    FOR v_item IN SELECT * FROM jsonb_array_elements(p_data_batch)
    LOOP
        PERFORM ingest_realtime_data(
            v_item->>'camera_id',
            v_item->>'stream_id',
            (v_item->>'frame_timestamp')::TIMESTAMP,
            (v_item->>'frame_number')::BIGINT,
            v_item->>'data_type',
            v_item->'data_payload'
        );
        v_count := v_count + 1;
    END LOOP;
    
    RETURN v_count;
END;
$$ LANGUAGE plpgsql;
```

## 🔄 Stream Processing Database Design

### Stream Processing Tables

```sql
-- Stream processing pipeline
CREATE TABLE stream_processing_pipeline (
    id SERIAL PRIMARY KEY,
    pipeline_id VARCHAR(100) UNIQUE NOT NULL,
    pipeline_name VARCHAR(200) NOT NULL,
    pipeline_type VARCHAR(50) NOT NULL, -- detection, tracking, counting, analytics
    
    -- Pipeline configuration
    pipeline_config JSONB NOT NULL,
    processing_steps JSONB, -- array of processing steps
    dependencies JSONB, -- step dependencies
    
    -- Pipeline status
    is_active BOOLEAN DEFAULT TRUE,
    is_running BOOLEAN DEFAULT FALSE,
    current_step VARCHAR(100),
    
    -- Performance metrics
    processing_rate_fps DECIMAL(8,2),
    avg_processing_time_ms DECIMAL(8,2),
    error_rate DECIMAL(5,2),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Processing steps
CREATE TABLE processing_steps (
    id SERIAL PRIMARY KEY,
    pipeline_id VARCHAR(100) REFERENCES stream_processing_pipeline(pipeline_id),
    step_name VARCHAR(100) NOT NULL,
    step_order INTEGER NOT NULL,
    
    -- Step configuration
    step_type VARCHAR(50) NOT NULL, -- filter, transform, aggregate, output
    step_config JSONB,
    step_conditions JSONB, -- conditions for step execution
    
    -- Step status
    is_active BOOLEAN DEFAULT TRUE,
    is_required BOOLEAN DEFAULT TRUE,
    
    -- Performance metrics
    avg_execution_time_ms DECIMAL(8,2),
    success_rate DECIMAL(5,2),
    error_count INTEGER DEFAULT 0,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Processing results
CREATE TABLE processing_results (
    id SERIAL PRIMARY KEY,
    pipeline_id VARCHAR(100) REFERENCES stream_processing_pipeline(pipeline_id),
    ingestion_id VARCHAR(100) REFERENCES realtime_data_ingestion(ingestion_id),
    
    -- Result data
    step_name VARCHAR(100) NOT NULL,
    result_data JSONB,
    result_metadata JSONB,
    
    -- Processing metrics
    processing_time_ms INTEGER,
    memory_usage_mb DECIMAL(8,2),
    cpu_usage_percent DECIMAL(5,2),
    
    -- Status
    status VARCHAR(20) DEFAULT 'completed', -- completed, failed, skipped
    error_message TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Stream processing monitoring
CREATE TABLE stream_processing_monitoring (
    id SERIAL PRIMARY KEY,
    pipeline_id VARCHAR(100) REFERENCES stream_processing_pipeline(pipeline_id),
    metric_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Processing metrics
    input_rate_fps DECIMAL(8,2),
    output_rate_fps DECIMAL(8,2),
    processing_latency_ms INTEGER,
    queue_size INTEGER,
    
    -- Resource usage
    cpu_usage_percent DECIMAL(5,2),
    memory_usage_percent DECIMAL(5,2),
    gpu_usage_percent DECIMAL(5,2),
    
    -- Quality metrics
    accuracy_percent DECIMAL(5,2),
    precision_percent DECIMAL(5,2),
    recall_percent DECIMAL(5,2),
    
    -- Error metrics
    error_count INTEGER,
    error_rate DECIMAL(5,2),
    retry_count INTEGER,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## ⏰ Time-series Data Optimization

### Time-series Database Design

```sql
-- Time-series data tables
CREATE TABLE timeseries_data (
    id SERIAL PRIMARY KEY,
    camera_id VARCHAR(100) NOT NULL,
    metric_name VARCHAR(100) NOT NULL,
    metric_timestamp TIMESTAMP NOT NULL,
    
    -- Metric values
    metric_value NUMERIC,
    metric_unit VARCHAR(20),
    metric_tags JSONB, -- additional metadata
    
    -- Quality indicators
    confidence_score DECIMAL(3,2),
    data_quality_score DECIMAL(3,2),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Time-series aggregation tables
CREATE TABLE timeseries_aggregations (
    id SERIAL PRIMARY KEY,
    camera_id VARCHAR(100) NOT NULL,
    metric_name VARCHAR(100) NOT NULL,
    aggregation_type VARCHAR(20) NOT NULL, -- minute, hour, day, week, month
    aggregation_timestamp TIMESTAMP NOT NULL,
    
    -- Aggregated values
    count_values INTEGER,
    sum_value NUMERIC,
    avg_value NUMERIC,
    min_value NUMERIC,
    max_value NUMERIC,
    std_dev_value NUMERIC,
    
    -- Additional metrics
    first_value NUMERIC,
    last_value NUMERIC,
    value_range NUMERIC,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Time-series indexes for performance
CREATE INDEX idx_timeseries_data_camera_metric_timestamp 
ON timeseries_data(camera_id, metric_name, metric_timestamp DESC);

CREATE INDEX idx_timeseries_data_timestamp 
ON timeseries_data(metric_timestamp DESC);

CREATE INDEX idx_timeseries_aggregations_camera_metric_type_timestamp 
ON timeseries_aggregations(camera_id, metric_name, aggregation_type, aggregation_timestamp DESC);

-- Time-series partitioning
CREATE TABLE timeseries_data_partitioned (
    LIKE timeseries_data INCLUDING ALL
) PARTITION BY RANGE (metric_timestamp);

-- Create monthly partitions
CREATE TABLE timeseries_data_2024_01 PARTITION OF timeseries_data_partitioned
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');
CREATE TABLE timeseries_data_2024_02 PARTITION OF timeseries_data_partitioned
    FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');
```

### Time-series Optimization Functions

```sql
-- Time-series aggregation function
CREATE OR REPLACE FUNCTION aggregate_timeseries_data(
    p_camera_id VARCHAR(100),
    p_metric_name VARCHAR(100),
    p_aggregation_type VARCHAR(20),
    p_start_timestamp TIMESTAMP,
    p_end_timestamp TIMESTAMP
)
RETURNS JSONB AS $$
DECLARE
    v_result JSONB;
BEGIN
    SELECT jsonb_build_object(
        'camera_id', p_camera_id,
        'metric_name', p_metric_name,
        'aggregation_type', p_aggregation_type,
        'start_timestamp', p_start_timestamp,
        'end_timestamp', p_end_timestamp,
        'count', COUNT(*),
        'sum', SUM(metric_value),
        'avg', AVG(metric_value),
        'min', MIN(metric_value),
        'max', MAX(metric_value),
        'std_dev', STDDEV(metric_value),
        'first_value', FIRST_VALUE(metric_value) OVER (ORDER BY metric_timestamp),
        'last_value', LAST_VALUE(metric_value) OVER (ORDER BY metric_timestamp)
    )
    INTO v_result
    FROM timeseries_data
    WHERE camera_id = p_camera_id
      AND metric_name = p_metric_name
      AND metric_timestamp BETWEEN p_start_timestamp AND p_end_timestamp;
    
    RETURN v_result;
END;
$$ LANGUAGE plpgsql;

-- Time-series data compression
CREATE OR REPLACE FUNCTION compress_timeseries_data(
    p_camera_id VARCHAR(100),
    p_metric_name VARCHAR(100),
    p_retention_days INTEGER DEFAULT 30
)
RETURNS INTEGER AS $$
DECLARE
    v_compressed_count INTEGER := 0;
    v_cutoff_date DATE;
BEGIN
    v_cutoff_date := CURRENT_DATE - INTERVAL '1 day' * p_retention_days;
    
    -- Aggregate old data by hour
    INSERT INTO timeseries_aggregations (
        camera_id, metric_name, aggregation_type, aggregation_timestamp,
        count_values, sum_value, avg_value, min_value, max_value, std_dev_value
    )
    SELECT 
        camera_id,
        metric_name,
        'hour' as aggregation_type,
        DATE_TRUNC('hour', metric_timestamp) as aggregation_timestamp,
        COUNT(*) as count_values,
        SUM(metric_value) as sum_value,
        AVG(metric_value) as avg_value,
        MIN(metric_value) as min_value,
        MAX(metric_value) as max_value,
        STDDEV(metric_value) as std_dev_value
    FROM timeseries_data
    WHERE camera_id = p_camera_id
      AND metric_name = p_metric_name
      AND metric_timestamp < v_cutoff_date
    GROUP BY camera_id, metric_name, DATE_TRUNC('hour', metric_timestamp)
    ON CONFLICT (camera_id, metric_name, aggregation_type, aggregation_timestamp)
    DO UPDATE SET
        count_values = EXCLUDED.count_values,
        sum_value = EXCLUDED.sum_value,
        avg_value = EXCLUDED.avg_value,
        min_value = EXCLUDED.min_value,
        max_value = EXCLUDED.max_value,
        std_dev_value = EXCLUDED.std_dev_value,
        updated_at = CURRENT_TIMESTAMP;
    
    -- Delete old detailed data
    DELETE FROM timeseries_data
    WHERE camera_id = p_camera_id
      AND metric_name = p_metric_name
      AND metric_timestamp < v_cutoff_date;
    
    GET DIAGNOSTICS v_compressed_count = ROW_COUNT;
    
    RETURN v_compressed_count;
END;
$$ LANGUAGE plpgsql;
```

## 📊 Real-time Aggregation Patterns

### Real-time Aggregation Tables

```sql
-- Real-time aggregation tables
CREATE TABLE realtime_aggregations (
    id SERIAL PRIMARY KEY,
    camera_id VARCHAR(100) NOT NULL,
    aggregation_key VARCHAR(200) NOT NULL, -- e.g., "count_in_1min", "density_5min"
    aggregation_timestamp TIMESTAMP NOT NULL,
    
    -- Aggregated values
    current_value NUMERIC,
    previous_value NUMERIC,
    change_value NUMERIC,
    change_percent DECIMAL(5,2),
    
    -- Trend indicators
    trend_direction VARCHAR(20), -- increasing, decreasing, stable
    trend_strength DECIMAL(3,2), -- 0.0 to 1.0
    
    -- Statistical values
    min_value NUMERIC,
    max_value NUMERIC,
    avg_value NUMERIC,
    count_values INTEGER,
    
    -- Metadata
    aggregation_config JSONB,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Real-time counters
CREATE TABLE realtime_counters (
    id SERIAL PRIMARY KEY,
    camera_id VARCHAR(100) NOT NULL,
    counter_name VARCHAR(100) NOT NULL,
    
    -- Counter values
    current_count INTEGER DEFAULT 0,
    total_count INTEGER DEFAULT 0,
    reset_count INTEGER DEFAULT 0,
    
    -- Time-based counters
    hourly_count INTEGER DEFAULT 0,
    daily_count INTEGER DEFAULT 0,
    weekly_count INTEGER DEFAULT 0,
    monthly_count INTEGER DEFAULT 0,
    
    -- Counter metadata
    last_increment_at TIMESTAMP,
    last_reset_at TIMESTAMP,
    counter_config JSONB,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(camera_id, counter_name)
);

-- Real-time metrics cache
CREATE TABLE realtime_metrics_cache (
    id SERIAL PRIMARY KEY,
    cache_key VARCHAR(200) UNIQUE NOT NULL,
    cache_value JSONB NOT NULL,
    
    -- Cache metadata
    cache_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ttl_seconds INTEGER DEFAULT 300, -- 5 minutes default
    cache_size_bytes INTEGER,
    
    -- Cache performance
    hit_count INTEGER DEFAULT 0,
    miss_count INTEGER DEFAULT 0,
    last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Real-time Aggregation Functions

```sql
-- Real-time aggregation function
CREATE OR REPLACE FUNCTION update_realtime_aggregation(
    p_camera_id VARCHAR(100),
    p_aggregation_key VARCHAR(200),
    p_new_value NUMERIC,
    p_aggregation_config JSONB DEFAULT '{}'::jsonb
)
RETURNS JSONB AS $$
DECLARE
    v_previous_value NUMERIC;
    v_change_value NUMERIC;
    v_change_percent DECIMAL(5,2);
    v_trend_direction VARCHAR(20);
    v_trend_strength DECIMAL(3,2);
    v_result JSONB;
BEGIN
    -- Get previous value
    SELECT current_value INTO v_previous_value
    FROM realtime_aggregations
    WHERE camera_id = p_camera_id AND aggregation_key = p_aggregation_key
    ORDER BY aggregation_timestamp DESC
    LIMIT 1;
    
    -- Calculate changes
    v_change_value := p_new_value - COALESCE(v_previous_value, 0);
    v_change_percent := CASE 
        WHEN COALESCE(v_previous_value, 0) > 0 
        THEN (v_change_value / v_previous_value) * 100
        ELSE 0
    END;
    
    -- Determine trend
    v_trend_direction := CASE 
        WHEN v_change_value > 0 THEN 'increasing'
        WHEN v_change_value < 0 THEN 'decreasing'
        ELSE 'stable'
    END;
    
    v_trend_strength := LEAST(ABS(v_change_percent) / 100, 1.0);
    
    -- Insert or update aggregation
    INSERT INTO realtime_aggregations (
        camera_id, aggregation_key, aggregation_timestamp,
        current_value, previous_value, change_value, change_percent,
        trend_direction, trend_strength, aggregation_config
    ) VALUES (
        p_camera_id, p_aggregation_key, CURRENT_TIMESTAMP,
        p_new_value, v_previous_value, v_change_value, v_change_percent,
        v_trend_direction, v_trend_strength, p_aggregation_config
    )
    ON CONFLICT (camera_id, aggregation_key, aggregation_timestamp)
    DO UPDATE SET
        current_value = EXCLUDED.current_value,
        previous_value = EXCLUDED.previous_value,
        change_value = EXCLUDED.change_value,
        change_percent = EXCLUDED.change_percent,
        trend_direction = EXCLUDED.trend_direction,
        trend_strength = EXCLUDED.trend_strength,
        updated_at = CURRENT_TIMESTAMP;
    
    -- Return result
    v_result := jsonb_build_object(
        'camera_id', p_camera_id,
        'aggregation_key', p_aggregation_key,
        'current_value', p_new_value,
        'previous_value', v_previous_value,
        'change_value', v_change_value,
        'change_percent', v_change_percent,
        'trend_direction', v_trend_direction,
        'trend_strength', v_trend_strength
    );
    
    RETURN v_result;
END;
$$ LANGUAGE plpgsql;

-- Real-time counter increment function
CREATE OR REPLACE FUNCTION increment_realtime_counter(
    p_camera_id VARCHAR(100),
    p_counter_name VARCHAR(100),
    p_increment_value INTEGER DEFAULT 1
)
RETURNS INTEGER AS $$
DECLARE
    v_new_count INTEGER;
BEGIN
    INSERT INTO realtime_counters (
        camera_id, counter_name, current_count, total_count,
        hourly_count, daily_count, weekly_count, monthly_count,
        last_increment_at
    ) VALUES (
        p_camera_id, p_counter_name, p_increment_value, p_increment_value,
        p_increment_value, p_increment_value, p_increment_value, p_increment_value,
        CURRENT_TIMESTAMP
    )
    ON CONFLICT (camera_id, counter_name)
    DO UPDATE SET
        current_count = realtime_counters.current_count + p_increment_value,
        total_count = realtime_counters.total_count + p_increment_value,
        hourly_count = realtime_counters.hourly_count + p_increment_value,
        daily_count = realtime_counters.daily_count + p_increment_value,
        weekly_count = realtime_counters.weekly_count + p_increment_value,
        monthly_count = realtime_counters.monthly_count + p_increment_value,
        last_increment_at = CURRENT_TIMESTAMP,
        updated_at = CURRENT_TIMESTAMP;
    
    SELECT current_count INTO v_new_count
    FROM realtime_counters
    WHERE camera_id = p_camera_id AND counter_name = p_counter_name;
    
    RETURN v_new_count;
END;
$$ LANGUAGE plpgsql;
```

## 🔄 Event-driven Database Patterns

### Event Store and Event Sourcing

```sql
-- Event store for event sourcing
CREATE TABLE event_store (
    id SERIAL PRIMARY KEY,
    event_id VARCHAR(100) UNIQUE NOT NULL,
    aggregate_id VARCHAR(100) NOT NULL,
    aggregate_type VARCHAR(100) NOT NULL, -- camera, detection, counting, etc.
    
    -- Event details
    event_type VARCHAR(100) NOT NULL,
    event_version INTEGER NOT NULL,
    event_data JSONB NOT NULL,
    event_metadata JSONB,
    
    -- Event ordering
    event_timestamp TIMESTAMP NOT NULL,
    event_sequence BIGINT NOT NULL,
    
    -- Event source
    source_system VARCHAR(100),
    user_id INTEGER REFERENCES users(id),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Event projections for read models
CREATE TABLE event_projections (
    id SERIAL PRIMARY KEY,
    projection_name VARCHAR(100) NOT NULL,
    aggregate_id VARCHAR(100) NOT NULL,
    
    -- Projection data
    projection_data JSONB NOT NULL,
    projection_version INTEGER NOT NULL,
    
    -- Projection metadata
    last_event_id VARCHAR(100),
    last_event_timestamp TIMESTAMP,
    last_event_sequence BIGINT,
    
    -- Projection status
    is_current BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(projection_name, aggregate_id)
);

-- Event handlers for processing
CREATE TABLE event_handlers (
    id SERIAL PRIMARY KEY,
    handler_name VARCHAR(100) UNIQUE NOT NULL,
    handler_type VARCHAR(50) NOT NULL, -- processor, projector, notifier
    
    -- Handler configuration
    event_types TEXT[] NOT NULL, -- array of event types to handle
    handler_config JSONB,
    
    -- Handler status
    is_active BOOLEAN DEFAULT TRUE,
    is_running BOOLEAN DEFAULT FALSE,
    
    -- Processing metrics
    processed_events_count BIGINT DEFAULT 0,
    last_processed_event_id VARCHAR(100),
    last_processed_at TIMESTAMP,
    
    -- Error handling
    error_count INTEGER DEFAULT 0,
    last_error_message TEXT,
    last_error_at TIMESTAMP,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Event processing queue
CREATE TABLE event_processing_queue (
    id SERIAL PRIMARY KEY,
    event_id VARCHAR(100) REFERENCES event_store(event_id),
    handler_name VARCHAR(100) REFERENCES event_handlers(handler_name),
    
    -- Processing status
    processing_status VARCHAR(20) DEFAULT 'pending', -- pending, processing, completed, failed
    processing_priority INTEGER DEFAULT 0,
    attempts INTEGER DEFAULT 0,
    max_attempts INTEGER DEFAULT 3,
    
    -- Processing timestamps
    queued_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processing_started_at TIMESTAMP,
    completed_at TIMESTAMP,
    
    -- Error handling
    error_message TEXT,
    error_code VARCHAR(50),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Event-driven Functions

```sql
-- Event publishing function
CREATE OR REPLACE FUNCTION publish_event(
    p_aggregate_id VARCHAR(100),
    p_aggregate_type VARCHAR(100),
    p_event_type VARCHAR(100),
    p_event_data JSONB,
    p_event_metadata JSONB DEFAULT '{}'::jsonb,
    p_source_system VARCHAR(100) DEFAULT 'database',
    p_user_id INTEGER DEFAULT NULL
)
RETURNS VARCHAR(100) AS $$
DECLARE
    v_event_id VARCHAR(100);
    v_event_sequence BIGINT;
    v_event_version INTEGER;
BEGIN
    -- Generate event ID
    v_event_id := p_aggregate_type || '_' || p_aggregate_id || '_' || EXTRACT(EPOCH FROM NOW()) || '_' || FLOOR(RANDOM() * 1000);
    
    -- Get next sequence number
    SELECT COALESCE(MAX(event_sequence), 0) + 1 INTO v_event_sequence
    FROM event_store
    WHERE aggregate_id = p_aggregate_id;
    
    -- Get next version
    SELECT COALESCE(MAX(event_version), 0) + 1 INTO v_event_version
    FROM event_store
    WHERE aggregate_id = p_aggregate_id;
    
    -- Insert event
    INSERT INTO event_store (
        event_id, aggregate_id, aggregate_type, event_type, event_version,
        event_data, event_metadata, event_timestamp, event_sequence,
        source_system, user_id
    ) VALUES (
        v_event_id, p_aggregate_id, p_aggregate_type, p_event_type, v_event_version,
        p_event_data, p_event_metadata, CURRENT_TIMESTAMP, v_event_sequence,
        p_source_system, p_user_id
    );
    
    -- Queue event for processing
    INSERT INTO event_processing_queue (event_id, handler_name, processing_priority)
    SELECT v_event_id, handler_name, 
           CASE 
               WHEN handler_type = 'processor' THEN 10
               WHEN handler_type = 'projector' THEN 5
               ELSE 1
           END
    FROM event_handlers
    WHERE is_active = TRUE
      AND p_event_type = ANY(event_types);
    
    RETURN v_event_id;
END;
$$ LANGUAGE plpgsql;

-- Event processing function
CREATE OR REPLACE FUNCTION process_event_queue()
RETURNS INTEGER AS $$
DECLARE
    v_processed_count INTEGER := 0;
    v_queue_item RECORD;
BEGIN
    -- Process pending events
    FOR v_queue_item IN 
        SELECT eq.*, es.event_type, es.event_data, es.aggregate_id, es.aggregate_type
        FROM event_processing_queue eq
        JOIN event_store es ON eq.event_id = es.event_id
        WHERE eq.processing_status = 'pending'
          AND eq.attempts < eq.max_attempts
        ORDER BY eq.processing_priority DESC, eq.queued_at ASC
        LIMIT 100
    LOOP
        -- Mark as processing
        UPDATE event_processing_queue
        SET processing_status = 'processing',
            processing_started_at = CURRENT_TIMESTAMP,
            attempts = attempts + 1
        WHERE id = v_queue_item.id;
        
        -- Process based on handler type
        -- This would typically call external processing logic
        -- For now, we'll just mark as completed
        
        UPDATE event_processing_queue
        SET processing_status = 'completed',
            completed_at = CURRENT_TIMESTAMP
        WHERE id = v_queue_item.id;
        
        v_processed_count := v_processed_count + 1;
    END LOOP;
    
    RETURN v_processed_count;
END;
$$ LANGUAGE plpgsql;
```

## 📊 Performance Optimization

### Real-time Performance Indexes

```sql
-- Performance indexes for real-time processing
CREATE INDEX idx_realtime_data_ingestion_camera_timestamp 
ON realtime_data_ingestion(camera_id, ingestion_timestamp DESC);

CREATE INDEX idx_realtime_data_ingestion_status 
ON realtime_data_ingestion(processing_status, processing_priority DESC);

CREATE INDEX idx_queue_items_status_priority 
ON queue_items(status, item_priority DESC, queued_at ASC);

CREATE INDEX idx_timeseries_data_camera_metric_timestamp 
ON timeseries_data(camera_id, metric_name, metric_timestamp DESC);

CREATE INDEX idx_realtime_aggregations_camera_key_timestamp 
ON realtime_aggregations(camera_id, aggregation_key, aggregation_timestamp DESC);

CREATE INDEX idx_event_store_aggregate_sequence 
ON event_store(aggregate_id, event_sequence);

CREATE INDEX idx_event_processing_queue_status_priority 
ON event_processing_queue(processing_status, processing_priority DESC, queued_at ASC);
```

### Real-time Performance Monitoring

```sql
-- Real-time performance monitoring
CREATE TABLE realtime_performance_metrics (
    id SERIAL PRIMARY KEY,
    metric_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Ingestion performance
    ingestion_rate_fps DECIMAL(8,2),
    ingestion_latency_ms INTEGER,
    ingestion_throughput_mbps DECIMAL(8,2),
    
    -- Processing performance
    processing_rate_fps DECIMAL(8,2),
    processing_latency_ms INTEGER,
    queue_size INTEGER,
    queue_wait_time_ms INTEGER,
    
    -- Database performance
    query_response_time_ms INTEGER,
    connection_count INTEGER,
    cache_hit_ratio DECIMAL(5,2),
    
    -- System performance
    cpu_usage_percent DECIMAL(5,2),
    memory_usage_percent DECIMAL(5,2),
    disk_io_mbps DECIMAL(8,2),
    network_bandwidth_mbps DECIMAL(8,2),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Performance alerting
CREATE OR REPLACE FUNCTION check_realtime_performance()
RETURNS TABLE(
    alert_type VARCHAR(50),
    alert_message TEXT,
    alert_severity VARCHAR(20)
) AS $$
BEGIN
    -- Check ingestion performance
    IF EXISTS (
        SELECT 1 FROM realtime_performance_metrics 
        WHERE metric_timestamp > NOW() - INTERVAL '5 minutes'
          AND ingestion_latency_ms > 1000
    ) THEN
        RETURN QUERY SELECT 
            'high_ingestion_latency'::VARCHAR(50),
            'Ingestion latency is above 1000ms'::TEXT,
            'warning'::VARCHAR(20);
    END IF;
    
    -- Check processing performance
    IF EXISTS (
        SELECT 1 FROM realtime_performance_metrics 
        WHERE metric_timestamp > NOW() - INTERVAL '5 minutes'
          AND processing_latency_ms > 5000
    ) THEN
        RETURN QUERY SELECT 
            'high_processing_latency'::VARCHAR(50),
            'Processing latency is above 5000ms'::TEXT,
            'error'::VARCHAR(20);
    END IF;
    
    -- Check queue size
    IF EXISTS (
        SELECT 1 FROM realtime_performance_metrics 
        WHERE metric_timestamp > NOW() - INTERVAL '5 minutes'
          AND queue_size > 10000
    ) THEN
        RETURN QUERY SELECT 
            'large_queue_size'::VARCHAR(50),
            'Queue size is above 10000 items'::TEXT,
            'warning'::VARCHAR(20);
    END IF;
END;
$$ LANGUAGE plpgsql;
```

---

**Tài liệu này cung cấp patterns hoàn chỉnh cho real-time processing trong database, bao gồm data ingestion, stream processing, time-series optimization, real-time aggregation, và event-driven patterns với performance optimization cho production deployment.** 