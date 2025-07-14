# Camera-Specific Database Design - AI Camera Counting System

## 📊 Tổng quan

Tài liệu này trình bày chi tiết data models cho camera management, stream processing, và counting data trong hệ thống AI Camera Counting, bao gồm camera configuration, video stream metadata, people counting events, và real-time analytics.

## 🎯 Mục tiêu

- **Camera Configuration**: Quản lý cấu hình camera và stream settings
- **Stream Processing**: Xử lý video stream metadata và real-time data
- **People Counting**: Lưu trữ và quản lý counting events
- **Real-time Analytics**: Analytics data structures cho real-time processing
- **Camera Health**: Monitoring và health tracking cho camera system

## 🏗️ Camera Data Architecture

### Camera System Data Flow

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              CAMERA DATA ARCHITECTURE                           │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              CAMERA CONFIGURATION LAYER                     │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Camera    │  │   Stream    │  │   AI Model  │  │   Alert     │        │ │
│  │  │   Settings  │  │   Config    │  │   Config    │  │   Rules     │        │ │
│  │  │             │  │             │  │             │  │             │        │ │
│  │  │ • Resolution│  │ • Protocol  │  │ • Model     │  │ • Threshold │        │ │
│  │  │ • FPS       │  │ • URL       │  │   Version   │  │ • Conditions│        │ │
│  │  │ • Quality   │  │ • Auth      │  │ • Parameters│  │ • Actions   │        │ │
│  │  │ • Region    │  │ • Timeout   │  │ • Confidence│  │ • Recipients│        │ │
│  │  │ • Schedule  │  │ • Retry     │  │   Threshold │  │ • Escalation│        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                             │
│                                    ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              STREAM PROCESSING LAYER                        │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Video     │  │   Frame     │  │   Metadata  │  │   Quality   │        │ │
│  │  │   Stream    │  │   Buffer    │  │   Storage   │  │   Metrics   │        │ │
│  │  │             │  │             │  │             │  │             │        │ │
│  │  │ • Stream ID │  │ • Frame     │  │ • Timestamp │  │ • Bitrate   │        │ │
│  │  │ • Source    │  │   Data      │  │ • Location  │  │ • Resolution│        │ │
│  │  │ • Format    │  │ • Processing│  │ • Weather   │  │ • Frame Rate│        │ │
│  │  │ • Encoding  │  │   Status    │  │ • Lighting  │  │ • Latency   │        │ │
│  │  │ • Bitrate   │  │ • Queue     │  │ • Events    │  │ • Jitter    │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                             │
│                                    ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              PEOPLE COUNTING LAYER                          │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Detection │  │   Tracking  │  │   Counting  │  │   Events    │        │ │
│  │  │   Events    │  │   Data      │  │   Results   │  │   Log       │        │ │
│  │  │             │  │             │  │             │  │             │        │ │
│  │  │ • Person    │  │ • Track ID  │  │ • In Count  │  │ • Entry     │        │ │
│  │  │   Detection │  │ • Position  │  │ • Out Count │  │ • Exit      │        │ │
│  │  │ • Bounding  │  │ • Velocity  │  │ • Total     │  │ • Direction │        │ │
│  │  │   Box       │  │ • Trajectory│  │ • Density   │  │ • Duration  │        │ │
│  │  │ • Confidence│  │ • Status    │  │ • Occupancy │  │ • Anomaly   │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                             │
│                                    ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              ANALYTICS LAYER                                │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Real-time │  │   Historical│  │   Predictive│  │   Business  │        │ │
│  │  │   Metrics   │  │   Data      │  │   Analytics │  │   Intelligence│       │ │
│  │  │             │  │             │  │             │  │             │        │ │
│  │  │ • Current   │  │ • Daily     │  │ • Trends    │  │ • KPIs      │        │ │
│  │  │   Count     │  │   Counts    │  │ • Patterns  │  │ • Reports   │        │ │
│  │  │ • Peak      │  │ • Hourly    │  │ • Forecasts │  │ • Dashboards│        │ │
│  │  │   Hours     │  │   Data      │  │ • Anomalies │  │ • Alerts    │        │ │
│  │  │ • Density   │  │ • Monthly   │  │ • Insights  │  │ • Metrics   │        │ │
│  │  │   Maps      │  │   Trends    │  │ • ML Models │  │ • Analytics │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 📊 Camera Configuration Data Models

### Camera Management Tables

```sql
-- Camera configuration table
CREATE TABLE camera_configurations (
    id SERIAL PRIMARY KEY,
    camera_id VARCHAR(100) UNIQUE NOT NULL,
    camera_name VARCHAR(200) NOT NULL,
    camera_type VARCHAR(50) NOT NULL, -- IP, USB, RTSP, etc.
    location_id INTEGER REFERENCES locations(id),
    tenant_id INTEGER REFERENCES tenants(id),
    
    -- Camera settings
    resolution_width INTEGER DEFAULT 1920,
    resolution_height INTEGER DEFAULT 1080,
    frame_rate INTEGER DEFAULT 30,
    bitrate INTEGER DEFAULT 4000, -- kbps
    quality_level VARCHAR(20) DEFAULT 'high', -- low, medium, high, ultra
    
    -- Stream configuration
    stream_url VARCHAR(500),
    stream_protocol VARCHAR(20) DEFAULT 'rtsp', -- rtsp, http, rtmp
    stream_username VARCHAR(100),
    stream_password VARCHAR(255), -- encrypted
    stream_timeout INTEGER DEFAULT 30, -- seconds
    stream_retry_count INTEGER DEFAULT 3,
    stream_retry_interval INTEGER DEFAULT 5, -- seconds
    
    -- AI Model configuration
    ai_model_id INTEGER REFERENCES ai_models(id),
    confidence_threshold DECIMAL(3,2) DEFAULT 0.7,
    detection_region JSONB, -- polygon coordinates
    tracking_enabled BOOLEAN DEFAULT TRUE,
    counting_enabled BOOLEAN DEFAULT TRUE,
    
    -- Schedule configuration
    is_active BOOLEAN DEFAULT TRUE,
    schedule_enabled BOOLEAN DEFAULT FALSE,
    schedule_config JSONB, -- cron-like schedule
    timezone VARCHAR(50) DEFAULT 'UTC',
    
    -- Alert configuration
    alert_enabled BOOLEAN DEFAULT TRUE,
    alert_rules JSONB, -- threshold rules
    
    -- Metadata
    description TEXT,
    tags TEXT[],
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER REFERENCES users(id),
    updated_by INTEGER REFERENCES users(id)
);

-- Camera health monitoring
CREATE TABLE camera_health (
    id SERIAL PRIMARY KEY,
    camera_id VARCHAR(100) REFERENCES camera_configurations(camera_id),
    
    -- Health metrics
    status VARCHAR(20) DEFAULT 'online', -- online, offline, error, maintenance
    last_heartbeat TIMESTAMP,
    uptime_percentage DECIMAL(5,2),
    response_time_ms INTEGER,
    
    -- Stream quality metrics
    stream_quality_score DECIMAL(3,2), -- 0.0 to 1.0
    frame_drop_rate DECIMAL(5,2), -- percentage
    bitrate_variance DECIMAL(5,2),
    latency_ms INTEGER,
    
    -- Error tracking
    error_count INTEGER DEFAULT 0,
    last_error_message TEXT,
    last_error_timestamp TIMESTAMP,
    
    -- Performance metrics
    cpu_usage_percent DECIMAL(5,2),
    memory_usage_percent DECIMAL(5,2),
    disk_usage_percent DECIMAL(5,2),
    network_bandwidth_mbps DECIMAL(8,2),
    
    -- Maintenance
    last_maintenance_date DATE,
    next_maintenance_date DATE,
    maintenance_notes TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Camera locations
CREATE TABLE camera_locations (
    id SERIAL PRIMARY KEY,
    location_name VARCHAR(200) NOT NULL,
    location_type VARCHAR(50), -- indoor, outdoor, entrance, exit, etc.
    address TEXT,
    coordinates POINT, -- latitude, longitude
    floor_level INTEGER,
    building_name VARCHAR(200),
    room_number VARCHAR(50),
    
    -- Capacity and limits
    max_capacity INTEGER,
    area_sqm DECIMAL(8,2),
    
    -- Metadata
    description TEXT,
    tags TEXT[],
    tenant_id INTEGER REFERENCES tenants(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Camera groups for management
CREATE TABLE camera_groups (
    id SERIAL PRIMARY KEY,
    group_name VARCHAR(200) NOT NULL,
    group_type VARCHAR(50), -- zone, building, floor, etc.
    description TEXT,
    tenant_id INTEGER REFERENCES tenants(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Camera group assignments
CREATE TABLE camera_group_assignments (
    id SERIAL PRIMARY KEY,
    camera_id VARCHAR(100) REFERENCES camera_configurations(camera_id),
    group_id INTEGER REFERENCES camera_groups(id),
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(camera_id, group_id)
);
```

## 📹 Video Stream Data Models

### Stream Processing Tables

```sql
-- Video stream metadata
CREATE TABLE video_streams (
    id SERIAL PRIMARY KEY,
    stream_id VARCHAR(100) UNIQUE NOT NULL,
    camera_id VARCHAR(100) REFERENCES camera_configurations(camera_id),
    
    -- Stream information
    stream_url VARCHAR(500) NOT NULL,
    stream_protocol VARCHAR(20) NOT NULL,
    stream_format VARCHAR(20), -- h264, h265, mjpeg, etc.
    stream_encoding VARCHAR(20), -- avc, hevc, etc.
    
    -- Stream metrics
    current_bitrate INTEGER, -- kbps
    current_fps INTEGER,
    current_resolution_width INTEGER,
    current_resolution_height INTEGER,
    
    -- Stream status
    is_active BOOLEAN DEFAULT TRUE,
    is_processing BOOLEAN DEFAULT FALSE,
    last_frame_timestamp TIMESTAMP,
    frame_count BIGINT DEFAULT 0,
    
    -- Quality metrics
    quality_score DECIMAL(3,2),
    frame_drop_count INTEGER DEFAULT 0,
    error_count INTEGER DEFAULT 0,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Frame processing queue
CREATE TABLE frame_queue (
    id SERIAL PRIMARY KEY,
    stream_id VARCHAR(100) REFERENCES video_streams(stream_id),
    frame_timestamp TIMESTAMP NOT NULL,
    frame_number BIGINT NOT NULL,
    
    -- Frame data
    frame_data BYTEA, -- compressed frame data
    frame_size INTEGER,
    frame_format VARCHAR(20),
    
    -- Processing status
    processing_status VARCHAR(20) DEFAULT 'pending', -- pending, processing, completed, failed
    processing_priority INTEGER DEFAULT 0,
    assigned_worker_id VARCHAR(100),
    
    -- AI processing results
    detection_results JSONB,
    tracking_results JSONB,
    processing_time_ms INTEGER,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed_at TIMESTAMP
);

-- Stream quality metrics
CREATE TABLE stream_quality_metrics (
    id SERIAL PRIMARY KEY,
    stream_id VARCHAR(100) REFERENCES video_streams(stream_id),
    metric_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Quality metrics
    bitrate INTEGER, -- kbps
    frame_rate DECIMAL(5,2),
    resolution_width INTEGER,
    resolution_height INTEGER,
    quality_score DECIMAL(3,2),
    
    -- Performance metrics
    latency_ms INTEGER,
    jitter_ms INTEGER,
    packet_loss_percent DECIMAL(5,2),
    frame_drop_rate DECIMAL(5,2),
    
    -- Error metrics
    error_count INTEGER,
    error_types JSONB,
    
    -- Network metrics
    bandwidth_utilization_percent DECIMAL(5,2),
    network_latency_ms INTEGER,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Stream events and alerts
CREATE TABLE stream_events (
    id SERIAL PRIMARY KEY,
    stream_id VARCHAR(100) REFERENCES video_streams(stream_id),
    event_type VARCHAR(50) NOT NULL, -- connection_lost, quality_degraded, error, etc.
    event_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Event details
    event_severity VARCHAR(20) DEFAULT 'info', -- info, warning, error, critical
    event_message TEXT,
    event_data JSONB,
    
    -- Resolution
    is_resolved BOOLEAN DEFAULT FALSE,
    resolved_at TIMESTAMP,
    resolution_notes TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 👥 People Counting Data Models

### Detection and Tracking Tables

```sql
-- Person detection events
CREATE TABLE person_detections (
    id SERIAL PRIMARY KEY,
    camera_id VARCHAR(100) REFERENCES camera_configurations(camera_id),
    frame_timestamp TIMESTAMP NOT NULL,
    detection_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Detection details
    detection_id VARCHAR(100) UNIQUE NOT NULL,
    confidence_score DECIMAL(3,2) NOT NULL,
    
    -- Bounding box
    bbox_x INTEGER NOT NULL,
    bbox_y INTEGER NOT NULL,
    bbox_width INTEGER NOT NULL,
    bbox_height INTEGER NOT NULL,
    
    -- Person attributes
    person_attributes JSONB, -- age, gender, clothing, etc.
    pose_estimation JSONB, -- keypoints, pose data
    
    -- Processing metadata
    model_version VARCHAR(50),
    processing_time_ms INTEGER,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Person tracking data
CREATE TABLE person_tracking (
    id SERIAL PRIMARY KEY,
    camera_id VARCHAR(100) REFERENCES camera_configurations(camera_id),
    track_id VARCHAR(100) NOT NULL,
    
    -- Tracking details
    detection_id VARCHAR(100) REFERENCES person_detections(detection_id),
    frame_timestamp TIMESTAMP NOT NULL,
    tracking_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Position and movement
    position_x INTEGER NOT NULL,
    position_y INTEGER NOT NULL,
    velocity_x DECIMAL(8,2),
    velocity_y DECIMAL(8,2),
    speed DECIMAL(8,2), -- pixels per second
    
    -- Trajectory
    trajectory_points JSONB, -- array of {x, y, timestamp}
    trajectory_length INTEGER,
    
    -- Tracking status
    tracking_status VARCHAR(20) DEFAULT 'active', -- active, lost, completed
    tracking_confidence DECIMAL(3,2),
    
    -- Duration
    first_seen TIMESTAMP,
    last_seen TIMESTAMP,
    duration_seconds INTEGER,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Counting events
CREATE TABLE counting_events (
    id SERIAL PRIMARY KEY,
    camera_id VARCHAR(100) REFERENCES camera_configurations(camera_id),
    event_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Event details
    event_type VARCHAR(20) NOT NULL, -- entry, exit, cross_line
    direction VARCHAR(20), -- in, out, north, south, east, west
    
    -- Person information
    track_id VARCHAR(100),
    detection_id VARCHAR(100) REFERENCES person_detections(detection_id),
    
    -- Location
    entry_point JSONB, -- coordinates
    exit_point JSONB, -- coordinates
    path_trajectory JSONB, -- complete path
    
    -- Counting data
    current_count_in INTEGER,
    current_count_out INTEGER,
    current_total INTEGER,
    
    -- Event metadata
    confidence_score DECIMAL(3,2),
    processing_time_ms INTEGER,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Real-time counting results
CREATE TABLE counting_results (
    id SERIAL PRIMARY KEY,
    camera_id VARCHAR(100) REFERENCES camera_configurations(camera_id),
    result_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Count data
    count_in INTEGER DEFAULT 0,
    count_out INTEGER DEFAULT 0,
    count_total INTEGER DEFAULT 0,
    count_density DECIMAL(8,2), -- people per square meter
    
    -- Occupancy data
    current_occupancy INTEGER DEFAULT 0,
    max_occupancy INTEGER,
    occupancy_percentage DECIMAL(5,2),
    
    -- Time-based data
    time_period VARCHAR(20), -- minute, hour, day
    period_start TIMESTAMP,
    period_end TIMESTAMP,
    
    -- Aggregated metrics
    peak_count INTEGER,
    average_count DECIMAL(8,2),
    min_count INTEGER,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Counting zones and lines
CREATE TABLE counting_zones (
    id SERIAL PRIMARY KEY,
    camera_id VARCHAR(100) REFERENCES camera_configurations(camera_id),
    zone_name VARCHAR(200) NOT NULL,
    zone_type VARCHAR(50), -- counting_line, area, region
    
    -- Zone definition
    zone_coordinates JSONB, -- polygon or line coordinates
    zone_area_sqm DECIMAL(8,2),
    
    -- Counting configuration
    counting_direction VARCHAR(20), -- bidirectional, in_only, out_only
    counting_method VARCHAR(20), -- line_crossing, area_occupancy
    
    -- Thresholds
    max_capacity INTEGER,
    alert_threshold INTEGER,
    
    -- Metadata
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 📈 Real-time Analytics Data Models

### Analytics and Reporting Tables

```sql
-- Real-time analytics metrics
CREATE TABLE realtime_analytics (
    id SERIAL PRIMARY KEY,
    camera_id VARCHAR(100) REFERENCES camera_configurations(camera_id),
    metric_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Current metrics
    current_count INTEGER DEFAULT 0,
    current_density DECIMAL(8,2),
    current_occupancy_percent DECIMAL(5,2),
    
    -- Trend metrics
    count_trend VARCHAR(20), -- increasing, decreasing, stable
    density_trend VARCHAR(20),
    occupancy_trend VARCHAR(20),
    
    -- Peak metrics
    peak_count INTEGER,
    peak_timestamp TIMESTAMP,
    average_count DECIMAL(8,2),
    
    -- Time-based metrics
    hourly_count INTEGER,
    daily_count INTEGER,
    weekly_count INTEGER,
    
    -- Performance metrics
    processing_latency_ms INTEGER,
    detection_accuracy DECIMAL(5,2),
    tracking_accuracy DECIMAL(5,2),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Historical analytics data
CREATE TABLE historical_analytics (
    id SERIAL PRIMARY KEY,
    camera_id VARCHAR(100) REFERENCES camera_configurations(camera_id),
    data_date DATE NOT NULL,
    time_period VARCHAR(20) NOT NULL, -- hour, day, week, month
    
    -- Aggregated counts
    total_count_in INTEGER DEFAULT 0,
    total_count_out INTEGER DEFAULT 0,
    total_count INTEGER DEFAULT 0,
    
    -- Peak metrics
    peak_count INTEGER,
    peak_hour INTEGER, -- 0-23
    peak_timestamp TIMESTAMP,
    
    -- Average metrics
    average_count DECIMAL(8,2),
    average_density DECIMAL(8,2),
    average_occupancy_percent DECIMAL(5,2),
    
    -- Time distribution
    hourly_distribution JSONB, -- {0: count, 1: count, ...}
    daily_distribution JSONB, -- {monday: count, tuesday: count, ...}
    
    -- Performance metrics
    total_processing_time_ms BIGINT,
    average_processing_time_ms DECIMAL(8,2),
    detection_count INTEGER,
    tracking_count INTEGER,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Analytics alerts and notifications
CREATE TABLE analytics_alerts (
    id SERIAL PRIMARY KEY,
    camera_id VARCHAR(100) REFERENCES camera_configurations(camera_id),
    alert_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Alert details
    alert_type VARCHAR(50) NOT NULL, -- capacity_exceeded, unusual_activity, etc.
    alert_severity VARCHAR(20) DEFAULT 'warning', -- info, warning, error, critical
    alert_message TEXT,
    
    -- Alert data
    alert_data JSONB,
    threshold_value DECIMAL(10,2),
    current_value DECIMAL(10,2),
    
    -- Alert status
    is_acknowledged BOOLEAN DEFAULT FALSE,
    acknowledged_at TIMESTAMP,
    acknowledged_by INTEGER REFERENCES users(id),
    
    -- Resolution
    is_resolved BOOLEAN DEFAULT FALSE,
    resolved_at TIMESTAMP,
    resolution_notes TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Analytics dashboards and reports
CREATE TABLE analytics_dashboards (
    id SERIAL PRIMARY KEY,
    dashboard_name VARCHAR(200) NOT NULL,
    dashboard_type VARCHAR(50), -- realtime, historical, summary
    
    -- Dashboard configuration
    dashboard_config JSONB, -- widgets, layout, filters
    refresh_interval_seconds INTEGER DEFAULT 30,
    
    -- Access control
    is_public BOOLEAN DEFAULT FALSE,
    created_by INTEGER REFERENCES users(id),
    tenant_id INTEGER REFERENCES tenants(id),
    
    -- Metadata
    description TEXT,
    tags TEXT[],
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Dashboard widgets
CREATE TABLE dashboard_widgets (
    id SERIAL PRIMARY KEY,
    dashboard_id INTEGER REFERENCES analytics_dashboards(id),
    widget_name VARCHAR(200) NOT NULL,
    widget_type VARCHAR(50), -- chart, metric, table, map
    
    -- Widget configuration
    widget_config JSONB, -- data source, chart type, filters
    widget_position JSONB, -- x, y, width, height
    widget_order INTEGER,
    
    -- Data source
    data_source_type VARCHAR(50), -- query, api, file
    data_source_config JSONB,
    
    -- Refresh settings
    auto_refresh BOOLEAN DEFAULT TRUE,
    refresh_interval_seconds INTEGER DEFAULT 30,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🔧 Database Optimization for Camera Data

### Indexing Strategy

```sql
-- Performance indexes for camera data
CREATE INDEX idx_camera_configurations_tenant ON camera_configurations(tenant_id);
CREATE INDEX idx_camera_configurations_location ON camera_configurations(location_id);
CREATE INDEX idx_camera_configurations_active ON camera_configurations(is_active) WHERE is_active = TRUE;

-- Stream processing indexes
CREATE INDEX idx_video_streams_camera ON video_streams(camera_id);
CREATE INDEX idx_video_streams_active ON video_streams(is_active) WHERE is_active = TRUE;
CREATE INDEX idx_video_streams_timestamp ON video_streams(last_frame_timestamp);

-- Frame queue optimization
CREATE INDEX idx_frame_queue_stream_status ON frame_queue(stream_id, processing_status);
CREATE INDEX idx_frame_queue_timestamp ON frame_queue(frame_timestamp);
CREATE INDEX idx_frame_queue_priority ON frame_queue(processing_priority DESC, frame_timestamp);

-- Detection and tracking indexes
CREATE INDEX idx_person_detections_camera_timestamp ON person_detections(camera_id, frame_timestamp);
CREATE INDEX idx_person_detections_confidence ON person_detections(confidence_score) WHERE confidence_score > 0.5;
CREATE INDEX idx_person_tracking_track_id ON person_tracking(track_id);
CREATE INDEX idx_person_tracking_camera_timestamp ON person_tracking(camera_id, frame_timestamp);

-- Counting events indexes
CREATE INDEX idx_counting_events_camera_timestamp ON counting_events(camera_id, event_timestamp);
CREATE INDEX idx_counting_events_type ON counting_events(event_type);
CREATE INDEX idx_counting_results_camera_timestamp ON counting_results(camera_id, result_timestamp);

-- Analytics indexes
CREATE INDEX idx_realtime_analytics_camera_timestamp ON realtime_analytics(camera_id, metric_timestamp);
CREATE INDEX idx_historical_analytics_camera_date ON historical_analytics(camera_id, data_date);
CREATE INDEX idx_analytics_alerts_camera_timestamp ON analytics_alerts(camera_id, alert_timestamp);
```

### Partitioning Strategy

```sql
-- Partition counting events by date
CREATE TABLE counting_events_partitioned (
    LIKE counting_events INCLUDING ALL
) PARTITION BY RANGE (event_timestamp);

-- Create monthly partitions
CREATE TABLE counting_events_2024_01 PARTITION OF counting_events_partitioned
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');
CREATE TABLE counting_events_2024_02 PARTITION OF counting_events_partitioned
    FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');

-- Partition person detections by date
CREATE TABLE person_detections_partitioned (
    LIKE person_detections INCLUDING ALL
) PARTITION BY RANGE (frame_timestamp);

-- Partition historical analytics by date
CREATE TABLE historical_analytics_partitioned (
    LIKE historical_analytics INCLUDING ALL
) PARTITION BY RANGE (data_date);
```

### Data Retention and Archiving

```sql
-- Data retention policies
CREATE OR REPLACE FUNCTION cleanup_old_camera_data()
RETURNS VOID AS $$
BEGIN
    -- Clean up old frame queue data (keep 7 days)
    DELETE FROM frame_queue 
    WHERE frame_timestamp < NOW() - INTERVAL '7 days';
    
    -- Archive old counting events (keep 90 days, archive older)
    INSERT INTO counting_events_archive 
    SELECT * FROM counting_events 
    WHERE event_timestamp < NOW() - INTERVAL '90 days';
    
    DELETE FROM counting_events 
    WHERE event_timestamp < NOW() - INTERVAL '90 days';
    
    -- Archive old person detections (keep 30 days)
    INSERT INTO person_detections_archive 
    SELECT * FROM person_detections 
    WHERE frame_timestamp < NOW() - INTERVAL '30 days';
    
    DELETE FROM person_detections 
    WHERE frame_timestamp < NOW() - INTERVAL '30 days';
    
    -- Clean up old stream quality metrics (keep 30 days)
    DELETE FROM stream_quality_metrics 
    WHERE metric_timestamp < NOW() - INTERVAL '30 days';
END;
$$ LANGUAGE plpgsql;

-- Schedule cleanup job
SELECT cron.schedule('cleanup-camera-data', '0 2 * * *', 'SELECT cleanup_old_camera_data();');
```

## 📊 Monitoring and Health Checks

### Camera Health Monitoring

```sql
-- Camera health check function
CREATE OR REPLACE FUNCTION check_camera_health()
RETURNS TABLE(
    camera_id VARCHAR(100),
    status VARCHAR(20),
    last_heartbeat TIMESTAMP,
    uptime_percentage DECIMAL(5,2),
    stream_quality_score DECIMAL(3,2),
    error_count INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        ch.camera_id,
        ch.status,
        ch.last_heartbeat,
        ch.uptime_percentage,
        ch.stream_quality_score,
        ch.error_count
    FROM camera_health ch
    WHERE ch.last_heartbeat < NOW() - INTERVAL '5 minutes'
       OR ch.status != 'online'
       OR ch.stream_quality_score < 0.7;
END;
$$ LANGUAGE plpgsql;

-- Stream quality monitoring
CREATE OR REPLACE FUNCTION monitor_stream_quality()
RETURNS TABLE(
    stream_id VARCHAR(100),
    camera_id VARCHAR(100),
    quality_score DECIMAL(3,2),
    frame_drop_rate DECIMAL(5,2),
    latency_ms INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        vs.stream_id,
        vs.camera_id,
        sqm.quality_score,
        sqm.frame_drop_rate,
        sqm.latency_ms
    FROM video_streams vs
    JOIN stream_quality_metrics sqm ON vs.stream_id = sqm.stream_id
    WHERE sqm.metric_timestamp > NOW() - INTERVAL '1 hour'
      AND (sqm.quality_score < 0.8 OR sqm.frame_drop_rate > 5.0 OR sqm.latency_ms > 1000);
END;
$$ LANGUAGE plpgsql;
```

---

**Tài liệu này cung cấp data models hoàn chỉnh cho camera-specific features, bao gồm configuration, stream processing, people counting, và real-time analytics với optimization strategies cho production deployment.** 