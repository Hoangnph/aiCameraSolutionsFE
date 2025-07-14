# AI Model Data Integration - AI Camera Counting System

## 📊 Tổng quan

Tài liệu này trình bày database patterns cho AI model integration và model management trong hệ thống AI Camera Counting, bao gồm model metadata storage, versioning, inference results, và performance tracking.

## 🎯 Mục tiêu

- **Model Metadata Storage**: Lưu trữ metadata cho AI models
- **Model Versioning**: Quản lý version và tracking cho models
- **Inference Results**: Lưu trữ kết quả inference
- **Model Performance**: Tracking performance metrics
- **A/B Testing**: Data structures cho A/B testing

## 🏗️ AI Model Data Architecture

### AI Model Management Flow

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              AI MODEL DATA ARCHITECTURE                         │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              MODEL MANAGEMENT LAYER                         │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Model     │  │   Version   │  │   Training  │  │   Deployment│        │ │
│  │  │   Registry  │  │   Control   │  │   History   │  │   Pipeline  │        │ │
│  │  │             │  │             │  │             │  │             │        │ │
│  │  │ • Model     │  │ • Version   │  │ • Training  │  │ • Deployment│        │ │
│  │  │   Metadata  │  │   Tracking  │  │   Runs      │  │   Status    │        │ │
│  │  │ • Model     │  │ • Model     │  │ • Metrics   │  │ • Rollback  │        │ │
│  │  │   Artifacts │  │   History   │  │ • Hyper-    │  │ • Canary    │        │ │
│  │  │ • Model     │  │ • Branching │  │   Parameters│  │   Testing   │        │ │
│  │  │   Config    │  │ • Merging   │  │ • Data      │  │ • Blue-     │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                             │
│                                    ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              INFERENCE LAYER                                │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Model     │  │   Inference │  │   Results   │  │   Performance│        │ │
│  │  │   Serving   │  │   Engine    │  │   Storage   │  │   Tracking  │        │ │
│  │  │             │  │             │  │             │  │             │        │ │
│  │  │ • Model     │  │ • Batch     │  │ • Detection │  │ • Accuracy  │        │ │
│  │  │   Loading   │  │   Inference │  │   Results   │  │ • Precision │        │ │
│  │  │ • Real-time │  │ • Stream    │  │ • Tracking  │  │ • Recall    │        │ │
│  │  │   Inference │  │   Processing│  │   Results   │  │ • F1 Score  │        │ │
│  │  │ • Model     │  │ • GPU       │  │ • Counting  │  │ • Latency   │        │ │
│  │  │   Caching   │  │   Acceleration│  │   Results   │  │ • Throughput│        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                             │
│                                    ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              ANALYTICS LAYER                                │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Model     │  │   A/B       │  │   Drift     │  │   Business  │        │ │
│  │  │   Analytics │  │   Testing   │  │   Detection │  │   Metrics   │        │ │
│  │  │             │  │             │  │             │  │             │        │ │
│  │  │ • Model     │  │ • A/B       │  │ • Data      │  │ • ROI       │        │ │
│  │  │   Performance│  │   Experiments│  │   Drift     │  │ • Cost      │        │ │
│  │  │ • Model     │  │ • Traffic   │  │ • Model     │  │ • Revenue   │        │ │
│  │  │   Monitoring│  │   Splitting │  │   Drift     │  │ • Efficiency│        │ │
│  │  │ • Model     │  │ • Results   │  │ • Alerting  │  │ • Impact    │        │ │
│  │  │   Insights  │  │   Analysis  │  │ • Retraining│  │ • KPIs      │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 🤖 AI Model Metadata Storage

### Model Registry Tables

```sql
-- AI Model registry
CREATE TABLE ai_models (
    id SERIAL PRIMARY KEY,
    model_id VARCHAR(100) UNIQUE NOT NULL,
    model_name VARCHAR(200) NOT NULL,
    model_type VARCHAR(50) NOT NULL, -- detection, tracking, counting, classification
    
    -- Model metadata
    model_description TEXT,
    model_version VARCHAR(50) DEFAULT '1.0.0',
    model_framework VARCHAR(50), -- tensorflow, pytorch, onnx, etc.
    model_format VARCHAR(50), -- saved_model, pb, pt, onnx, etc.
    
    -- Model configuration
    model_config JSONB, -- hyperparameters, architecture, etc.
    model_parameters INTEGER, -- number of parameters
    model_size_mb DECIMAL(8,2), -- model file size
    
    -- Model performance
    accuracy_score DECIMAL(5,2),
    precision_score DECIMAL(5,2),
    recall_score DECIMAL(5,2),
    f1_score DECIMAL(5,2),
    
    -- Model status
    is_active BOOLEAN DEFAULT TRUE,
    is_production BOOLEAN DEFAULT FALSE,
    deployment_status VARCHAR(20) DEFAULT 'development', -- development, testing, production, archived
    
    -- Model artifacts
    model_path VARCHAR(500), -- path to model file
    model_checksum VARCHAR(64), -- SHA256 checksum
    model_metadata_path VARCHAR(500), -- path to metadata file
    
    -- Creation and ownership
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Model versions
CREATE TABLE model_versions (
    id SERIAL PRIMARY KEY,
    model_id VARCHAR(100) REFERENCES ai_models(model_id),
    version_number VARCHAR(50) NOT NULL,
    
    -- Version details
    version_description TEXT,
    version_changes TEXT, -- changelog
    version_commit_hash VARCHAR(64), -- git commit hash
    
    -- Model files
    model_file_path VARCHAR(500),
    model_file_size_mb DECIMAL(8,2),
    model_file_checksum VARCHAR(64),
    
    -- Training information
    training_dataset VARCHAR(200),
    training_metrics JSONB,
    training_duration_hours DECIMAL(8,2),
    
    -- Performance metrics
    validation_accuracy DECIMAL(5,2),
    validation_precision DECIMAL(5,2),
    validation_recall DECIMAL(5,2),
    validation_f1 DECIMAL(5,2),
    
    -- Deployment information
    deployment_timestamp TIMESTAMP,
    deployment_environment VARCHAR(50), -- dev, staging, production
    deployment_status VARCHAR(20) DEFAULT 'not_deployed',
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(model_id, version_number)
);

-- Model training history
CREATE TABLE model_training_history (
    id SERIAL PRIMARY KEY,
    model_id VARCHAR(100) REFERENCES ai_models(model_id),
    training_run_id VARCHAR(100) UNIQUE NOT NULL,
    
    -- Training configuration
    training_config JSONB, -- hyperparameters, optimizer, etc.
    dataset_config JSONB, -- dataset paths, splits, etc.
    
    -- Training metrics
    training_accuracy DECIMAL(5,2),
    training_loss DECIMAL(8,4),
    validation_accuracy DECIMAL(5,2),
    validation_loss DECIMAL(8,4),
    
    -- Training progress
    epochs_completed INTEGER,
    total_epochs INTEGER,
    training_duration_hours DECIMAL(8,2),
    
    -- Training status
    training_status VARCHAR(20) DEFAULT 'running', -- running, completed, failed, cancelled
    error_message TEXT,
    
    -- Resource usage
    gpu_usage_percent DECIMAL(5,2),
    memory_usage_gb DECIMAL(8,2),
    cpu_usage_percent DECIMAL(5,2),
    
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🔄 Model Versioning and Tracking

### Version Control Tables

```sql
-- Model version control
CREATE TABLE model_version_control (
    id SERIAL PRIMARY KEY,
    model_id VARCHAR(100) REFERENCES ai_models(model_id),
    version_number VARCHAR(50) NOT NULL,
    
    -- Version control
    parent_version VARCHAR(50), -- parent version for branching
    branch_name VARCHAR(100), -- git branch name
    commit_hash VARCHAR(64), -- git commit hash
    commit_message TEXT,
    
    -- Changes tracking
    changes_summary TEXT,
    changes_details JSONB, -- detailed changes
    files_changed INTEGER,
    lines_added INTEGER,
    lines_deleted INTEGER,
    
    -- Author information
    author_name VARCHAR(200),
    author_email VARCHAR(200),
    commit_timestamp TIMESTAMP,
    
    -- Review and approval
    review_status VARCHAR(20) DEFAULT 'pending', -- pending, approved, rejected
    reviewed_by INTEGER REFERENCES users(id),
    reviewed_at TIMESTAMP,
    review_notes TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Model branching and merging
CREATE TABLE model_branches (
    id SERIAL PRIMARY KEY,
    branch_name VARCHAR(100) UNIQUE NOT NULL,
    base_version VARCHAR(50) NOT NULL,
    
    -- Branch information
    branch_description TEXT,
    branch_purpose VARCHAR(50), -- feature, bugfix, experiment, etc.
    branch_status VARCHAR(20) DEFAULT 'active', -- active, merged, abandoned
    
    -- Branch metadata
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    merged_at TIMESTAMP,
    merged_to VARCHAR(100) REFERENCES model_branches(branch_name)
);

-- Model deployment pipeline
CREATE TABLE model_deployment_pipeline (
    id SERIAL PRIMARY KEY,
    pipeline_id VARCHAR(100) UNIQUE NOT NULL,
    model_id VARCHAR(100) REFERENCES ai_models(model_id),
    version_number VARCHAR(50) NOT NULL,
    
    -- Pipeline stages
    pipeline_stages JSONB, -- array of pipeline stages
    current_stage VARCHAR(50),
    stage_status VARCHAR(20) DEFAULT 'pending', -- pending, running, completed, failed
    
    -- Deployment configuration
    deployment_config JSONB, -- deployment settings
    environment_config JSONB, -- environment-specific settings
    
    -- Pipeline status
    pipeline_status VARCHAR(20) DEFAULT 'pending', -- pending, running, completed, failed
    pipeline_started_at TIMESTAMP,
    pipeline_completed_at TIMESTAMP,
    
    -- Rollback information
    can_rollback BOOLEAN DEFAULT TRUE,
    rollback_version VARCHAR(50),
    rollback_reason TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 📊 Inference Results Storage

### Inference Data Tables

```sql
-- Model inference results
CREATE TABLE model_inference_results (
    id SERIAL PRIMARY KEY,
    inference_id VARCHAR(100) UNIQUE NOT NULL,
    model_id VARCHAR(100) REFERENCES ai_models(model_id),
    model_version VARCHAR(50) NOT NULL,
    
    -- Input data
    input_data_hash VARCHAR(64), -- hash of input data
    input_metadata JSONB, -- input metadata
    input_timestamp TIMESTAMP NOT NULL,
    
    -- Inference results
    inference_results JSONB NOT NULL, -- actual inference output
    confidence_scores JSONB, -- confidence scores for each detection
    processing_time_ms INTEGER, -- inference processing time
    
    -- Quality metrics
    result_quality_score DECIMAL(3,2), -- 0.0 to 1.0
    result_validation_status VARCHAR(20) DEFAULT 'valid', -- valid, invalid, uncertain
    
    -- Performance metrics
    gpu_utilization_percent DECIMAL(5,2),
    memory_usage_mb DECIMAL(8,2),
    batch_size INTEGER,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Detection results
CREATE TABLE detection_results (
    id SERIAL PRIMARY KEY,
    inference_id VARCHAR(100) REFERENCES model_inference_results(inference_id),
    detection_id VARCHAR(100) UNIQUE NOT NULL,
    
    -- Detection details
    object_class VARCHAR(50) NOT NULL, -- person, vehicle, etc.
    confidence_score DECIMAL(3,2) NOT NULL,
    
    -- Bounding box
    bbox_x INTEGER NOT NULL,
    bbox_y INTEGER NOT NULL,
    bbox_width INTEGER NOT NULL,
    bbox_height INTEGER NOT NULL,
    
    -- Additional attributes
    object_attributes JSONB, -- age, gender, clothing, etc.
    pose_estimation JSONB, -- keypoints, pose data
    
    -- Quality indicators
    detection_quality DECIMAL(3,2),
    occlusion_level DECIMAL(3,2), -- 0.0 = no occlusion, 1.0 = fully occluded
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tracking results
CREATE TABLE tracking_results (
    id SERIAL PRIMARY KEY,
    inference_id VARCHAR(100) REFERENCES model_inference_results(inference_id),
    track_id VARCHAR(100) NOT NULL,
    
    -- Tracking details
    detection_id VARCHAR(100) REFERENCES detection_results(detection_id),
    tracking_confidence DECIMAL(3,2),
    
    -- Position and movement
    position_x INTEGER NOT NULL,
    position_y INTEGER NOT NULL,
    velocity_x DECIMAL(8,2),
    velocity_y DECIMAL(8,2),
    speed DECIMAL(8,2),
    
    -- Tracking status
    tracking_status VARCHAR(20) DEFAULT 'active', -- active, lost, completed
    track_age_frames INTEGER, -- number of frames tracked
    
    -- Trajectory
    trajectory_points JSONB, -- array of {x, y, timestamp}
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Counting results
CREATE TABLE counting_results (
    id SERIAL PRIMARY KEY,
    inference_id VARCHAR(100) REFERENCES model_inference_results(inference_id),
    counting_event_id VARCHAR(100) UNIQUE NOT NULL,
    
    -- Counting details
    event_type VARCHAR(20) NOT NULL, -- entry, exit, cross_line
    direction VARCHAR(20), -- in, out, north, south, east, west
    
    -- Person information
    track_id VARCHAR(100),
    detection_id VARCHAR(100) REFERENCES detection_results(detection_id),
    
    -- Location
    entry_point JSONB, -- coordinates
    exit_point JSONB, -- coordinates
    path_trajectory JSONB, -- complete path
    
    -- Counting data
    current_count_in INTEGER,
    current_count_out INTEGER,
    current_total INTEGER,
    
    -- Event metadata
    event_confidence DECIMAL(3,2),
    processing_time_ms INTEGER,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 📈 Model Performance Tracking

### Performance Metrics Tables

```sql
-- Model performance metrics
CREATE TABLE model_performance_metrics (
    id SERIAL PRIMARY KEY,
    model_id VARCHAR(100) REFERENCES ai_models(model_id),
    model_version VARCHAR(50) NOT NULL,
    metric_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Accuracy metrics
    accuracy_score DECIMAL(5,2),
    precision_score DECIMAL(5,2),
    recall_score DECIMAL(5,2),
    f1_score DECIMAL(5,2),
    
    -- Performance metrics
    inference_latency_ms INTEGER,
    throughput_fps DECIMAL(8,2),
    gpu_utilization_percent DECIMAL(5,2),
    memory_usage_mb DECIMAL(8,2),
    
    -- Quality metrics
    false_positive_rate DECIMAL(5,2),
    false_negative_rate DECIMAL(5,2),
    detection_rate DECIMAL(5,2),
    
    -- Business metrics
    cost_per_inference DECIMAL(8,4), -- cost in dollars
    revenue_per_inference DECIMAL(8,4), -- revenue in dollars
    roi_percentage DECIMAL(8,2),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Model drift detection
CREATE TABLE model_drift_metrics (
    id SERIAL PRIMARY KEY,
    model_id VARCHAR(100) REFERENCES ai_models(model_id),
    drift_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Drift metrics
    data_drift_score DECIMAL(3,2), -- 0.0 to 1.0
    concept_drift_score DECIMAL(3,2), -- 0.0 to 1.0
    model_drift_score DECIMAL(3,2), -- 0.0 to 1.0
    
    -- Drift details
    drift_type VARCHAR(50), -- covariate, label, concept
    drift_severity VARCHAR(20), -- low, medium, high, critical
    drift_features JSONB, -- features with highest drift
    
    -- Alert status
    is_alerted BOOLEAN DEFAULT FALSE,
    alert_threshold DECIMAL(3,2) DEFAULT 0.8,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Model comparison metrics
CREATE TABLE model_comparison_metrics (
    id SERIAL PRIMARY KEY,
    comparison_id VARCHAR(100) UNIQUE NOT NULL,
    baseline_model_id VARCHAR(100) REFERENCES ai_models(model_id),
    challenger_model_id VARCHAR(100) REFERENCES ai_models(model_id),
    
    -- Comparison metrics
    accuracy_improvement DECIMAL(5,2),
    precision_improvement DECIMAL(5,2),
    recall_improvement DECIMAL(5,2),
    f1_improvement DECIMAL(5,2),
    
    -- Performance comparison
    latency_improvement_percent DECIMAL(5,2),
    throughput_improvement_percent DECIMAL(5,2),
    cost_improvement_percent DECIMAL(5,2),
    
    -- Statistical significance
    is_statistically_significant BOOLEAN,
    p_value DECIMAL(8,4),
    confidence_interval JSONB,
    
    -- Comparison status
    comparison_status VARCHAR(20) DEFAULT 'running', -- running, completed, failed
    winner_model_id VARCHAR(100) REFERENCES ai_models(model_id),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);
```

## 🧪 A/B Testing Data Structures

### A/B Testing Tables

```sql
-- A/B testing experiments
CREATE TABLE ab_testing_experiments (
    id SERIAL PRIMARY KEY,
    experiment_id VARCHAR(100) UNIQUE NOT NULL,
    experiment_name VARCHAR(200) NOT NULL,
    
    -- Experiment configuration
    baseline_model_id VARCHAR(100) REFERENCES ai_models(model_id),
    challenger_model_id VARCHAR(100) REFERENCES ai_models(model_id),
    
    -- Traffic splitting
    traffic_split_percent INTEGER DEFAULT 50, -- percentage to challenger
    traffic_split_method VARCHAR(50) DEFAULT 'random', -- random, user_id, session_id
    
    -- Experiment settings
    experiment_duration_days INTEGER DEFAULT 7,
    minimum_sample_size INTEGER DEFAULT 1000,
    confidence_level DECIMAL(3,2) DEFAULT 0.95,
    
    -- Experiment status
    experiment_status VARCHAR(20) DEFAULT 'draft', -- draft, running, completed, stopped
    start_date TIMESTAMP,
    end_date TIMESTAMP,
    
    -- Success criteria
    success_metrics JSONB, -- array of metrics to track
    success_thresholds JSONB, -- thresholds for each metric
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- A/B testing assignments
CREATE TABLE ab_testing_assignments (
    id SERIAL PRIMARY KEY,
    experiment_id VARCHAR(100) REFERENCES ab_testing_experiments(experiment_id),
    user_id INTEGER REFERENCES users(id),
    session_id VARCHAR(100),
    
    -- Assignment details
    assigned_model_id VARCHAR(100) REFERENCES ai_models(model_id),
    assigned_group VARCHAR(20) NOT NULL, -- baseline, challenger
    assignment_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Assignment metadata
    assignment_reason VARCHAR(50), -- random, user_id_hash, etc.
    assignment_confidence DECIMAL(3,2),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- A/B testing results
CREATE TABLE ab_testing_results (
    id SERIAL PRIMARY KEY,
    experiment_id VARCHAR(100) REFERENCES ab_testing_experiments(experiment_id),
    result_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Group metrics
    group_name VARCHAR(20) NOT NULL, -- baseline, challenger
    sample_size INTEGER,
    
    -- Performance metrics
    accuracy_score DECIMAL(5,2),
    precision_score DECIMAL(5,2),
    recall_score DECIMAL(5,2),
    f1_score DECIMAL(5,2),
    
    -- Business metrics
    conversion_rate DECIMAL(5,2),
    revenue_per_user DECIMAL(8,2),
    cost_per_user DECIMAL(8,2),
    
    -- Statistical significance
    is_statistically_significant BOOLEAN,
    p_value DECIMAL(8,4),
    confidence_interval JSONB,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- A/B testing conclusions
CREATE TABLE ab_testing_conclusions (
    id SERIAL PRIMARY KEY,
    experiment_id VARCHAR(100) REFERENCES ab_testing_experiments(experiment_id),
    
    -- Conclusion details
    winner_model_id VARCHAR(100) REFERENCES ai_models(model_id),
    conclusion_reason TEXT,
    recommendation VARCHAR(50), -- deploy_challenger, keep_baseline, run_longer
    
    -- Impact analysis
    expected_improvement_percent DECIMAL(5,2),
    confidence_level DECIMAL(3,2),
    risk_assessment VARCHAR(20), -- low, medium, high
    
    -- Deployment plan
    deployment_strategy VARCHAR(50), -- immediate, gradual, canary
    deployment_timeline_days INTEGER,
    
    -- Reviewer information
    reviewed_by INTEGER REFERENCES users(id),
    reviewed_at TIMESTAMP,
    review_notes TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🔧 Database Optimization for AI Models

### Performance Indexes

```sql
-- Performance indexes for AI model data
CREATE INDEX idx_ai_models_active ON ai_models(is_active) WHERE is_active = TRUE;
CREATE INDEX idx_ai_models_production ON ai_models(is_production) WHERE is_production = TRUE;
CREATE INDEX idx_ai_models_type ON ai_models(model_type);

CREATE INDEX idx_model_versions_model_version ON model_versions(model_id, version_number);
CREATE INDEX idx_model_versions_deployment ON model_versions(deployment_status, deployment_timestamp);

CREATE INDEX idx_inference_results_model_timestamp ON model_inference_results(model_id, input_timestamp DESC);
CREATE INDEX idx_inference_results_quality ON model_inference_results(result_quality_score) WHERE result_quality_score > 0.5;

CREATE INDEX idx_detection_results_inference ON detection_results(inference_id);
CREATE INDEX idx_detection_results_confidence ON detection_results(confidence_score) WHERE confidence_score > 0.7;

CREATE INDEX idx_tracking_results_track_id ON tracking_results(track_id);
CREATE INDEX idx_tracking_results_status ON tracking_results(tracking_status);

CREATE INDEX idx_performance_metrics_model_timestamp ON model_performance_metrics(model_id, metric_timestamp DESC);
CREATE INDEX idx_drift_metrics_model_timestamp ON model_drift_metrics(model_id, drift_timestamp DESC);

CREATE INDEX idx_ab_experiments_status ON ab_testing_experiments(experiment_status);
CREATE INDEX idx_ab_assignments_experiment_user ON ab_testing_assignments(experiment_id, user_id);
CREATE INDEX idx_ab_results_experiment_group ON ab_testing_results(experiment_id, group_name);
```

### Data Retention and Archiving

```sql
-- Data retention policies for AI models
CREATE OR REPLACE FUNCTION cleanup_old_ai_data()
RETURNS VOID AS $$
BEGIN
    -- Archive old inference results (keep 90 days, archive older)
    INSERT INTO inference_results_archive 
    SELECT * FROM model_inference_results 
    WHERE input_timestamp < NOW() - INTERVAL '90 days';
    
    DELETE FROM model_inference_results 
    WHERE input_timestamp < NOW() - INTERVAL '90 days';
    
    -- Archive old performance metrics (keep 1 year)
    INSERT INTO performance_metrics_archive 
    SELECT * FROM model_performance_metrics 
    WHERE metric_timestamp < NOW() - INTERVAL '1 year';
    
    DELETE FROM model_performance_metrics 
    WHERE metric_timestamp < NOW() - INTERVAL '1 year';
    
    -- Archive old A/B testing results (keep 2 years)
    INSERT INTO ab_results_archive 
    SELECT * FROM ab_testing_results 
    WHERE result_timestamp < NOW() - INTERVAL '2 years';
    
    DELETE FROM ab_testing_results 
    WHERE result_timestamp < NOW() - INTERVAL '2 years';
END;
$$ LANGUAGE plpgsql;

-- Schedule cleanup job
SELECT cron.schedule('cleanup-ai-data', '0 3 * * *', 'SELECT cleanup_old_ai_data();');
```

---

**Tài liệu này cung cấp patterns hoàn chỉnh cho AI model data integration, bao gồm model metadata storage, versioning, inference results, performance tracking, và A/B testing với optimization strategies cho production deployment.** 