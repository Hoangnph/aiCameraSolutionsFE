# Advanced Analytics Patterns - AI Camera Counting System

## 📊 Tổng quan

Tài liệu này trình bày advanced analytics patterns cho AI Camera Counting System, bao gồm machine learning data preparation, predictive analytics patterns, data warehouse integration và business intelligence patterns.

## 🎯 Analytics Objectives

- **Predictive Analytics**: Dự báo traffic patterns và anomalies
- **Real-time Analytics**: Real-time insights từ camera data
- **Business Intelligence**: Business metrics và reporting
- **Machine Learning**: Data preparation cho ML models
- **Performance Analytics**: System performance insights

## 🤖 Machine Learning Data Preparation

### 1. Feature Engineering for Camera Analytics

**Mục đích**: Chuẩn bị data cho machine learning models.

```sql
-- Feature Engineering Tables
CREATE TABLE ml_features (
    id SERIAL PRIMARY KEY,
    camera_id VARCHAR(100) REFERENCES camera_configurations(camera_id),
    feature_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Time-based Features
    hour_of_day INTEGER,
    day_of_week INTEGER,
    month INTEGER,
    is_weekend BOOLEAN,
    is_holiday BOOLEAN,
    
    -- Traffic Features
    people_count INTEGER,
    vehicle_count INTEGER,
    object_count INTEGER,
    traffic_density DECIMAL(5,2),
    
    -- Environmental Features
    weather_condition VARCHAR(50),
    temperature_celsius DECIMAL(4,1),
    humidity_percent DECIMAL(5,2),
    lighting_condition VARCHAR(20),
    
    -- Camera Features
    camera_angle_degrees INTEGER,
    camera_height_meters DECIMAL(4,2),
    field_of_view_degrees INTEGER,
    
    -- Performance Features
    detection_confidence DECIMAL(3,2),
    processing_latency_ms INTEGER,
    stream_quality_score DECIMAL(3,2),
    
    -- Derived Features
    traffic_intensity_level VARCHAR(20), -- low, medium, high
    anomaly_score DECIMAL(3,2),
    trend_direction VARCHAR(10), -- increasing, decreasing, stable
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Feature Engineering Function
CREATE OR REPLACE FUNCTION generate_ml_features(p_camera_id VARCHAR(100))
RETURNS VOID AS $$
DECLARE
    detection_record RECORD;
    hour_val INTEGER;
    day_val INTEGER;
    month_val INTEGER;
    is_weekend_val BOOLEAN;
    people_count_val INTEGER;
    vehicle_count_val INTEGER;
    traffic_density_val DECIMAL(5,2);
    anomaly_score_val DECIMAL(3,2);
BEGIN
    -- Get detection data for the last hour
    FOR detection_record IN 
        SELECT detection_timestamp, detection_type, detection_confidence
        FROM detection_data
        WHERE camera_id = p_camera_id
          AND detection_timestamp > NOW() - INTERVAL '1 hour'
    LOOP
        -- Extract time-based features
        hour_val := EXTRACT(HOUR FROM detection_record.detection_timestamp);
        day_val := EXTRACT(DOW FROM detection_record.detection_timestamp);
        month_val := EXTRACT(MONTH FROM detection_record.detection_timestamp);
        is_weekend_val := day_val IN (0, 6);
        
        -- Calculate traffic features
        SELECT 
            COUNT(*) FILTER (WHERE detection_type = 'person'),
            COUNT(*) FILTER (WHERE detection_type = 'vehicle')
        INTO people_count_val, vehicle_count_val
        FROM detection_data
        WHERE camera_id = p_camera_id
          AND detection_timestamp BETWEEN 
              detection_record.detection_timestamp - INTERVAL '5 minutes'
              AND detection_record.detection_timestamp;
        
        -- Calculate traffic density
        traffic_density_val := (people_count_val + vehicle_count_val) / 100.0;
        
        -- Calculate anomaly score
        anomaly_score_val := CASE 
            WHEN traffic_density_val > 2.0 THEN 0.9
            WHEN traffic_density_val > 1.0 THEN 0.5
            ELSE 0.1
        END;
        
        -- Insert features
        INSERT INTO ml_features (
            camera_id, feature_timestamp, hour_of_day, day_of_week, month,
            is_weekend, people_count, vehicle_count, traffic_density,
            detection_confidence, anomaly_score
        ) VALUES (
            p_camera_id, detection_record.detection_timestamp, hour_val, day_val, month_val,
            is_weekend_val, people_count_val, vehicle_count_val, traffic_density_val,
            detection_record.detection_confidence, anomaly_score_val
        );
    END LOOP;
END;
$$ LANGUAGE plpgsql;
```

### 2. Data Preprocessing for ML Models

```sql
-- Data Preprocessing Tables
CREATE TABLE ml_preprocessed_data (
    id SERIAL PRIMARY KEY,
    camera_id VARCHAR(100) REFERENCES camera_configurations(camera_id),
    preprocessing_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Normalized Features
    normalized_traffic_density DECIMAL(5,2),
    normalized_detection_confidence DECIMAL(5,2),
    normalized_anomaly_score DECIMAL(5,2),
    
    -- Encoded Features
    time_period_encoded INTEGER, -- 0-23 for hours
    day_type_encoded INTEGER, -- 0=weekday, 1=weekend
    season_encoded INTEGER, -- 0=spring, 1=summer, 2=fall, 3=winter
    
    -- Aggregated Features
    hourly_traffic_avg DECIMAL(5,2),
    daily_traffic_avg DECIMAL(5,2),
    weekly_traffic_avg DECIMAL(5,2),
    
    -- Target Variables
    next_hour_traffic INTEGER,
    traffic_prediction DECIMAL(5,2),
    anomaly_prediction BOOLEAN,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Data Preprocessing Function
CREATE OR REPLACE FUNCTION preprocess_ml_data(p_camera_id VARCHAR(100))
RETURNS VOID AS $$
DECLARE
    feature_record RECORD;
    min_traffic DECIMAL(5,2);
    max_traffic DECIMAL(5,2);
    avg_traffic DECIMAL(5,2);
    normalized_traffic DECIMAL(5,2);
    normalized_confidence DECIMAL(5,2);
    normalized_anomaly DECIMAL(5,2);
    time_period_encoded_val INTEGER;
    day_type_encoded_val INTEGER;
    season_encoded_val INTEGER;
BEGIN
    -- Get normalization parameters
    SELECT 
        MIN(traffic_density),
        MAX(traffic_density),
        AVG(traffic_density)
    INTO min_traffic, max_traffic, avg_traffic
    FROM ml_features
    WHERE camera_id = p_camera_id
      AND feature_timestamp > NOW() - INTERVAL '30 days';
    
    -- Process each feature record
    FOR feature_record IN 
        SELECT * FROM ml_features
        WHERE camera_id = p_camera_id
          AND feature_timestamp > NOW() - INTERVAL '24 hours'
        ORDER BY feature_timestamp
    LOOP
        -- Normalize features
        normalized_traffic := CASE 
            WHEN max_traffic > min_traffic THEN 
                (feature_record.traffic_density - min_traffic) / (max_traffic - min_traffic)
            ELSE 0.5
        END;
        
        normalized_confidence := feature_record.detection_confidence;
        normalized_anomaly := feature_record.anomaly_score;
        
        -- Encode categorical features
        time_period_encoded_val := feature_record.hour_of_day;
        day_type_encoded_val := CASE WHEN feature_record.is_weekend THEN 1 ELSE 0 END;
        season_encoded_val := CASE 
            WHEN feature_record.month IN (3, 4, 5) THEN 0  -- Spring
            WHEN feature_record.month IN (6, 7, 8) THEN 1  -- Summer
            WHEN feature_record.month IN (9, 10, 11) THEN 2 -- Fall
            ELSE 3  -- Winter
        END;
        
        -- Insert preprocessed data
        INSERT INTO ml_preprocessed_data (
            camera_id, preprocessing_timestamp,
            normalized_traffic_density, normalized_detection_confidence, normalized_anomaly_score,
            time_period_encoded, day_type_encoded, season_encoded
        ) VALUES (
            p_camera_id, feature_record.feature_timestamp,
            normalized_traffic, normalized_confidence, normalized_anomaly,
            time_period_encoded_val, day_type_encoded_val, season_encoded_val
        );
    END LOOP;
END;
$$ LANGUAGE plpgsql;
```

## 📈 Predictive Analytics Patterns

### 1. Traffic Prediction Models

**Mục đích**: Dự báo traffic patterns cho planning và optimization.

```sql
-- Traffic Prediction Tables
CREATE TABLE traffic_predictions (
    id SERIAL PRIMARY KEY,
    camera_id VARCHAR(100) REFERENCES camera_configurations(camera_id),
    prediction_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Prediction Timeframe
    prediction_horizon_hours INTEGER, -- 1, 6, 12, 24 hours
    prediction_start_time TIMESTAMP,
    prediction_end_time TIMESTAMP,
    
    -- Predicted Values
    predicted_people_count INTEGER,
    predicted_vehicle_count INTEGER,
    predicted_traffic_density DECIMAL(5,2),
    prediction_confidence DECIMAL(3,2),
    
    -- Model Information
    model_version VARCHAR(50),
    model_accuracy DECIMAL(5,2),
    features_used JSONB,
    
    -- Actual Values (for validation)
    actual_people_count INTEGER,
    actual_vehicle_count INTEGER,
    actual_traffic_density DECIMAL(5,2),
    prediction_error DECIMAL(5,2),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Traffic Prediction Function
CREATE OR REPLACE FUNCTION predict_traffic(
    p_camera_id VARCHAR(100),
    p_horizon_hours INTEGER DEFAULT 1
)
RETURNS TABLE(
    prediction_horizon_hours INTEGER,
    predicted_people_count INTEGER,
    predicted_vehicle_count INTEGER,
    predicted_traffic_density DECIMAL(5,2),
    prediction_confidence DECIMAL(3,2)
) AS $$
DECLARE
    historical_avg_people INTEGER;
    historical_avg_vehicles INTEGER;
    historical_avg_density DECIMAL(5,2);
    current_hour INTEGER;
    current_day INTEGER;
    seasonal_factor DECIMAL(3,2);
    time_factor DECIMAL(3,2);
    predicted_people INTEGER;
    predicted_vehicles INTEGER;
    predicted_density DECIMAL(5,2);
    confidence DECIMAL(3,2);
BEGIN
    -- Get current time features
    current_hour := EXTRACT(HOUR FROM NOW());
    current_day := EXTRACT(DOW FROM NOW());
    
    -- Get historical averages for the same time period
    SELECT 
        AVG(people_count),
        AVG(vehicle_count),
        AVG(traffic_density)
    INTO historical_avg_people, historical_avg_vehicles, historical_avg_density
    FROM ml_features
    WHERE camera_id = p_camera_id
      AND hour_of_day = current_hour
      AND day_of_week = current_day
      AND feature_timestamp > NOW() - INTERVAL '30 days';
    
    -- Calculate seasonal and time factors
    seasonal_factor := CASE 
        WHEN EXTRACT(MONTH FROM NOW()) IN (6, 7, 8) THEN 1.2  -- Summer peak
        WHEN EXTRACT(MONTH FROM NOW()) IN (12, 1, 2) THEN 0.8  -- Winter low
        ELSE 1.0
    END;
    
    time_factor := CASE 
        WHEN current_hour BETWEEN 7 AND 9 THEN 1.5   -- Morning rush
        WHEN current_hour BETWEEN 17 AND 19 THEN 1.5 -- Evening rush
        WHEN current_hour BETWEEN 22 AND 6 THEN 0.5  -- Night low
        ELSE 1.0
    END;
    
    -- Calculate predictions
    predicted_people := ROUND(COALESCE(historical_avg_people, 10) * seasonal_factor * time_factor);
    predicted_vehicles := ROUND(COALESCE(historical_avg_vehicles, 5) * seasonal_factor * time_factor);
    predicted_density := (predicted_people + predicted_vehicles) / 100.0;
    
    -- Calculate confidence based on data availability
    confidence := CASE 
        WHEN historical_avg_people IS NOT NULL THEN 0.85
        ELSE 0.60
    END;
    
    -- Store prediction
    INSERT INTO traffic_predictions (
        camera_id, prediction_horizon_hours, prediction_start_time, prediction_end_time,
        predicted_people_count, predicted_vehicle_count, predicted_traffic_density,
        prediction_confidence, model_version
    ) VALUES (
        p_camera_id, p_horizon_hours, NOW(), NOW() + (p_horizon_hours || ' hours')::INTERVAL,
        predicted_people, predicted_vehicles, predicted_density,
        confidence, 'v1.0'
    );
    
    -- Return predictions
    RETURN QUERY SELECT 
        p_horizon_hours,
        predicted_people,
        predicted_vehicles,
        predicted_density,
        confidence;
END;
$$ LANGUAGE plpgsql;
```

### 2. Anomaly Detection Patterns

```sql
-- Anomaly Detection Tables
CREATE TABLE anomaly_detections (
    id SERIAL PRIMARY KEY,
    camera_id VARCHAR(100) REFERENCES camera_configurations(camera_id),
    detection_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Anomaly Information
    anomaly_type VARCHAR(50), -- traffic_spike, traffic_drop, system_failure, security_breach
    anomaly_severity VARCHAR(20), -- low, medium, high, critical
    anomaly_score DECIMAL(3,2), -- 0.0 to 1.0
    
    -- Anomaly Details
    baseline_value DECIMAL(8,2),
    actual_value DECIMAL(8,2),
    deviation_percent DECIMAL(5,2),
    
    -- Context Information
    time_period VARCHAR(20), -- hour, day, week
    contributing_factors JSONB,
    
    -- Resolution
    is_resolved BOOLEAN DEFAULT FALSE,
    resolution_notes TEXT,
    resolved_at TIMESTAMP,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Anomaly Detection Function
CREATE OR REPLACE FUNCTION detect_anomalies(p_camera_id VARCHAR(100))
RETURNS TABLE(
    anomaly_type VARCHAR(50),
    anomaly_severity VARCHAR(20),
    anomaly_score DECIMAL(3,2),
    baseline_value DECIMAL(8,2),
    actual_value DECIMAL(8,2),
    deviation_percent DECIMAL(5,2)
) AS $$
DECLARE
    current_traffic INTEGER;
    baseline_traffic INTEGER;
    deviation_percent_val DECIMAL(5,2);
    anomaly_score_val DECIMAL(3,2);
    anomaly_severity_val VARCHAR(20);
    anomaly_type_val VARCHAR(50);
BEGIN
    -- Get current traffic
    SELECT COALESCE(SUM(people_count), 0)
    INTO current_traffic
    FROM ml_features
    WHERE camera_id = p_camera_id
      AND feature_timestamp > NOW() - INTERVAL '1 hour';
    
    -- Get baseline traffic (same hour, last 4 weeks)
    SELECT AVG(people_count)
    INTO baseline_traffic
    FROM ml_features
    WHERE camera_id = p_camera_id
      AND hour_of_day = EXTRACT(HOUR FROM NOW())
      AND day_of_week = EXTRACT(DOW FROM NOW())
      AND feature_timestamp > NOW() - INTERVAL '4 weeks'
      AND feature_timestamp < NOW() - INTERVAL '1 week';
    
    baseline_traffic := COALESCE(baseline_traffic, 10);
    
    -- Calculate deviation
    deviation_percent_val := CASE 
        WHEN baseline_traffic > 0 THEN 
            ((current_traffic - baseline_traffic) * 100.0) / baseline_traffic
        ELSE 0
    END;
    
    -- Calculate anomaly score
    anomaly_score_val := CASE 
        WHEN ABS(deviation_percent_val) > 200 THEN 1.0
        WHEN ABS(deviation_percent_val) > 100 THEN 0.8
        WHEN ABS(deviation_percent_val) > 50 THEN 0.6
        WHEN ABS(deviation_percent_val) > 25 THEN 0.4
        ELSE 0.2
    END;
    
    -- Determine severity and type
    anomaly_severity_val := CASE 
        WHEN anomaly_score_val > 0.8 THEN 'critical'
        WHEN anomaly_score_val > 0.6 THEN 'high'
        WHEN anomaly_score_val > 0.4 THEN 'medium'
        ELSE 'low'
    END;
    
    anomaly_type_val := CASE 
        WHEN deviation_percent_val > 50 THEN 'traffic_spike'
        WHEN deviation_percent_val < -50 THEN 'traffic_drop'
        ELSE 'unusual_pattern'
    END;
    
    -- Store anomaly if significant
    IF anomaly_score_val > 0.4 THEN
        INSERT INTO anomaly_detections (
            camera_id, anomaly_type, anomaly_severity, anomaly_score,
            baseline_value, actual_value, deviation_percent
        ) VALUES (
            p_camera_id, anomaly_type_val, anomaly_severity_val, anomaly_score_val,
            baseline_traffic, current_traffic, deviation_percent_val
        );
    END IF;
    
    -- Return anomaly details
    RETURN QUERY SELECT 
        anomaly_type_val,
        anomaly_severity_val,
        anomaly_score_val,
        baseline_traffic,
        current_traffic,
        deviation_percent_val;
END;
$$ LANGUAGE plpgsql;
```

## 📊 Real-time Analytics Patterns

### 1. Real-time Dashboard Queries

```sql
-- Real-time Analytics Dashboard
WITH real_time_metrics AS (
    SELECT 
        'Active Cameras' as metric_name,
        COUNT(*) as current_value,
        COUNT(*) FILTER (WHERE camera_status = 'online') as target_value,
        'count' as unit
    FROM camera_configurations
    
    UNION ALL
    
    SELECT 
        'Total Detections (Last Hour)' as metric_name,
        COUNT(*) as current_value,
        1000 as target_value,
        'count' as unit
    FROM detection_data
    WHERE detection_timestamp > NOW() - INTERVAL '1 hour'
    
    UNION ALL
    
    SELECT 
        'Average Processing Latency' as metric_name,
        ROUND(AVG(total_latency_ms)) as current_value,
        200 as target_value,
        'ms' as unit
    FROM realtime_processing_monitoring
    WHERE metric_timestamp > NOW() - INTERVAL '1 hour'
    
    UNION ALL
    
    SELECT 
        'AI Model Accuracy' as metric_name,
        ROUND(AVG(accuracy_score) * 100) as current_value,
        85 as target_value,
        'percent' as unit
    FROM ai_model_performance_monitoring
    WHERE metric_timestamp > NOW() - INTERVAL '1 hour'
    
    UNION ALL
    
    SELECT 
        'Stream Quality Score' as metric_name,
        ROUND(AVG(quality_score) * 100) as current_value,
        80 as target_value,
        'percent' as unit
    FROM stream_quality_monitoring
    WHERE metric_timestamp > NOW() - INTERVAL '1 hour'
),
anomaly_summary AS (
    SELECT 
        COUNT(*) as total_anomalies,
        COUNT(*) FILTER (WHERE anomaly_severity = 'critical') as critical_anomalies,
        COUNT(*) FILTER (WHERE anomaly_severity = 'high') as high_anomalies
    FROM anomaly_detections
    WHERE detection_timestamp > NOW() - INTERVAL '24 hours'
      AND is_resolved = FALSE
)
SELECT 
    rtm.metric_name,
    rtm.current_value,
    rtm.target_value,
    rtm.unit,
    CASE 
        WHEN rtm.current_value >= rtm.target_value THEN '🟢'
        WHEN rtm.current_value >= rtm.target_value * 0.8 THEN '🟡'
        ELSE '🔴'
    END as status_icon,
    ROUND((rtm.current_value * 100.0) / rtm.target_value, 1) as performance_percent,
    COALESCE(ams.total_anomalies, 0) as active_anomalies
FROM real_time_metrics rtm
CROSS JOIN anomaly_summary ams
ORDER BY rtm.metric_name;
```

### 2. Real-time Trend Analysis

```sql
-- Real-time Trend Analysis
WITH hourly_trends AS (
    SELECT 
        DATE_TRUNC('hour', detection_timestamp) as hour_bucket,
        COUNT(*) as detection_count,
        COUNT(*) FILTER (WHERE detection_type = 'person') as people_count,
        COUNT(*) FILTER (WHERE detection_type = 'vehicle') as vehicle_count
    FROM detection_data
    WHERE detection_timestamp > NOW() - INTERVAL '24 hours'
    GROUP BY DATE_TRUNC('hour', detection_timestamp)
),
trend_analysis AS (
    SELECT 
        hour_bucket,
        detection_count,
        people_count,
        vehicle_count,
        LAG(detection_count) OVER (ORDER BY hour_bucket) as prev_hour_detections,
        LAG(people_count) OVER (ORDER BY hour_bucket) as prev_hour_people,
        LAG(vehicle_count) OVER (ORDER BY hour_bucket) as prev_hour_vehicles
    FROM hourly_trends
)
SELECT 
    hour_bucket::TIME as time_period,
    detection_count,
    people_count,
    vehicle_count,
    CASE 
        WHEN prev_hour_detections IS NOT NULL THEN
            ROUND(((detection_count - prev_hour_detections) * 100.0) / prev_hour_detections, 1)
        ELSE 0
    END as detection_change_percent,
    CASE 
        WHEN prev_hour_people IS NOT NULL THEN
            ROUND(((people_count - prev_hour_people) * 100.0) / prev_hour_people, 1)
        ELSE 0
    END as people_change_percent,
    CASE 
        WHEN prev_hour_vehicles IS NOT NULL THEN
            ROUND(((vehicle_count - prev_hour_vehicles) * 100.0) / prev_hour_vehicles, 1)
        ELSE 0
    END as vehicle_change_percent,
    CASE 
        WHEN detection_count > prev_hour_detections THEN '📈'
        WHEN detection_count < prev_hour_detections THEN '📉'
        ELSE '➡️'
    END as trend_icon
FROM trend_analysis
ORDER BY hour_bucket DESC
LIMIT 24;
```

## 📊 Business Intelligence Patterns

### 1. KPI Dashboard

```sql
-- Business KPI Dashboard
WITH daily_kpis AS (
    SELECT 
        DATE(detection_timestamp) as kpi_date,
        COUNT(*) as total_detections,
        COUNT(DISTINCT camera_id) as active_cameras,
        COUNT(*) FILTER (WHERE detection_type = 'person') as people_detections,
        COUNT(*) FILTER (WHERE detection_type = 'vehicle') as vehicle_detections,
        AVG(detection_confidence) as avg_confidence
    FROM detection_data
    WHERE detection_timestamp > NOW() - INTERVAL '30 days'
    GROUP BY DATE(detection_timestamp)
),
weekly_kpis AS (
    SELECT 
        DATE_TRUNC('week', kpi_date) as week_start,
        AVG(total_detections) as avg_daily_detections,
        AVG(active_cameras) as avg_active_cameras,
        AVG(people_detections) as avg_people_detections,
        AVG(vehicle_detections) as avg_vehicle_detections,
        AVG(avg_confidence) as avg_confidence
    FROM daily_kpis
    GROUP BY DATE_TRUNC('week', kpi_date)
),
monthly_trends AS (
    SELECT 
        DATE_TRUNC('month', kpi_date) as month_start,
        SUM(total_detections) as monthly_detections,
        AVG(active_cameras) as avg_cameras_per_day,
        SUM(people_detections) as monthly_people,
        SUM(vehicle_detections) as monthly_vehicles
    FROM daily_kpis
    GROUP BY DATE_TRUNC('month', kpi_date)
)
SELECT 
    'Daily Average' as metric_type,
    ROUND(AVG(total_detections)) as detections,
    ROUND(AVG(active_cameras)) as cameras,
    ROUND(AVG(people_detections)) as people,
    ROUND(AVG(vehicle_detections)) as vehicles,
    ROUND(AVG(avg_confidence) * 100, 1) as confidence_percent
FROM daily_kpis
WHERE kpi_date > NOW() - INTERVAL '7 days'

UNION ALL

SELECT 
    'Weekly Average' as metric_type,
    ROUND(AVG(avg_daily_detections)) as detections,
    ROUND(AVG(avg_active_cameras)) as cameras,
    ROUND(AVG(avg_people_detections)) as people,
    ROUND(AVG(avg_vehicle_detections)) as vehicles,
    ROUND(AVG(avg_confidence) * 100, 1) as confidence_percent
FROM weekly_kpis
WHERE week_start > NOW() - INTERVAL '4 weeks'

UNION ALL

SELECT 
    'Monthly Total' as metric_type,
    ROUND(AVG(monthly_detections)) as detections,
    ROUND(AVG(avg_cameras_per_day)) as cameras,
    ROUND(AVG(monthly_people)) as people,
    ROUND(AVG(monthly_vehicles)) as vehicles,
    0 as confidence_percent
FROM monthly_trends
WHERE month_start > NOW() - INTERVAL '3 months';
```

### 2. Performance Analytics

```sql
-- Performance Analytics Dashboard
WITH performance_metrics AS (
    SELECT 
        DATE_TRUNC('hour', metric_timestamp) as hour_bucket,
        AVG(processing_rate_fps) as avg_processing_rate,
        AVG(total_latency_ms) as avg_latency,
        AVG(processing_quality_score) as avg_quality,
        COUNT(*) as metric_count
    FROM realtime_processing_monitoring
    WHERE metric_timestamp > NOW() - INTERVAL '7 days'
    GROUP BY DATE_TRUNC('hour', metric_timestamp)
),
ai_performance AS (
    SELECT 
        DATE_TRUNC('hour', metric_timestamp) as hour_bucket,
        AVG(accuracy_score) as avg_accuracy,
        AVG(inference_latency_ms) as avg_inference_latency,
        AVG(throughput_fps) as avg_throughput,
        COUNT(*) as metric_count
    FROM ai_model_performance_monitoring
    WHERE metric_timestamp > NOW() - INTERVAL '7 days'
    GROUP BY DATE_TRUNC('hour', metric_timestamp)
)
SELECT 
    pm.hour_bucket::TIME as time_period,
    ROUND(pm.avg_processing_rate, 2) as processing_fps,
    ROUND(pm.avg_latency, 0) as latency_ms,
    ROUND(pm.avg_quality * 100, 1) as quality_percent,
    ROUND(ai.avg_accuracy * 100, 1) as accuracy_percent,
    ROUND(ai.avg_inference_latency, 0) as inference_latency_ms,
    ROUND(ai.avg_throughput, 2) as ai_throughput_fps,
    CASE 
        WHEN pm.avg_processing_rate >= 25 AND pm.avg_latency <= 200 THEN '🟢'
        WHEN pm.avg_processing_rate >= 20 AND pm.avg_latency <= 300 THEN '🟡'
        ELSE '🔴'
    END as performance_status
FROM performance_metrics pm
LEFT JOIN ai_performance ai ON pm.hour_bucket = ai.hour_bucket
ORDER BY pm.hour_bucket DESC
LIMIT 168; -- Last 7 days (24 * 7)
```

---

**Tài liệu này cung cấp advanced analytics patterns cho AI Camera Counting System với machine learning data preparation, predictive analytics, real-time analytics và business intelligence capabilities.** 