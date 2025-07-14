# Data Governance Framework - AI Camera Counting System

## 📊 Tổng quan

Tài liệu này trình bày data governance framework cho AI Camera Counting System, bao gồm data classification, data lineage tracking, compliance reporting và data quality management.

## 🎯 Governance Objectives

- **Data Classification**: Phân loại data theo sensitivity và importance
- **Data Lineage**: Track data flow và transformations
- **Compliance**: Đảm bảo compliance với regulations
- **Data Quality**: Maintain data quality standards
- **Access Control**: Control data access và usage

## 📋 Data Classification Framework

### 1. Data Classification Levels

**Mục đích**: Phân loại data theo sensitivity và business value.

```sql
-- Data Classification Tables
CREATE TABLE data_classification (
    id SERIAL PRIMARY KEY,
    classification_level VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    sensitivity_score INTEGER CHECK (sensitivity_score >= 1 AND sensitivity_score <= 5),
    retention_period_days INTEGER,
    encryption_required BOOLEAN DEFAULT TRUE,
    access_control_level VARCHAR(20), -- public, internal, confidential, restricted
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Data Classification Levels
INSERT INTO data_classification (classification_level, description, sensitivity_score, retention_period_days, encryption_required, access_control_level) VALUES
('Public', 'Public information, no restrictions', 1, 365, FALSE, 'public'),
('Internal', 'Internal business data', 2, 730, TRUE, 'internal'),
('Confidential', 'Sensitive business data', 3, 1095, TRUE, 'confidential'),
('Restricted', 'Highly sensitive data', 4, 1825, TRUE, 'restricted'),
('Critical', 'Critical system data', 5, 2555, TRUE, 'restricted');

-- Data Classification Mapping
CREATE TABLE data_classification_mapping (
    id SERIAL PRIMARY KEY,
    table_name VARCHAR(100) NOT NULL,
    column_name VARCHAR(100),
    classification_level VARCHAR(50) REFERENCES data_classification(classification_level),
    classification_reason TEXT,
    pii_flag BOOLEAN DEFAULT FALSE,
    encryption_method VARCHAR(50),
    masking_required BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Camera System Data Classification
INSERT INTO data_classification_mapping (table_name, column_name, classification_level, classification_reason, pii_flag, encryption_method, masking_required) VALUES
-- Camera Configuration Data
('camera_configurations', 'camera_id', 'Internal', 'System identifier', FALSE, 'AES-256', FALSE),
('camera_configurations', 'camera_name', 'Internal', 'Business identifier', FALSE, 'AES-256', FALSE),
('camera_configurations', 'location_address', 'Confidential', 'Location information', FALSE, 'AES-256', TRUE),
('camera_configurations', 'ip_address', 'Restricted', 'Network security', FALSE, 'AES-256', TRUE),

-- Detection Data
('detection_data', 'detection_id', 'Internal', 'System identifier', FALSE, 'AES-256', FALSE),
('detection_data', 'camera_id', 'Internal', 'System reference', FALSE, 'AES-256', FALSE),
('detection_data', 'detection_type', 'Internal', 'Business data', FALSE, 'AES-256', FALSE),
('detection_data', 'detection_confidence', 'Internal', 'Business data', FALSE, 'AES-256', FALSE),
('detection_data', 'detection_timestamp', 'Internal', 'Business data', FALSE, 'AES-256', FALSE),

-- User Data
('users', 'user_id', 'Internal', 'System identifier', FALSE, 'AES-256', FALSE),
('users', 'username', 'Internal', 'Business identifier', FALSE, 'AES-256', FALSE),
('users', 'email', 'Confidential', 'Personal information', TRUE, 'AES-256', TRUE),
('users', 'phone_number', 'Confidential', 'Personal information', TRUE, 'AES-256', TRUE),
('users', 'password_hash', 'Restricted', 'Security credential', FALSE, 'AES-256', TRUE),

-- AI Model Data
('ai_models', 'model_id', 'Internal', 'System identifier', FALSE, 'AES-256', FALSE),
('ai_models', 'model_name', 'Internal', 'Business identifier', FALSE, 'AES-256', FALSE),
('ai_models', 'model_path', 'Restricted', 'System security', FALSE, 'AES-256', TRUE),
('ai_models', 'model_parameters', 'Confidential', 'Business intelligence', FALSE, 'AES-256', TRUE);
```

### 2. Data Classification Functions

```sql
-- Data Classification Function
CREATE OR REPLACE FUNCTION classify_data(
    p_table_name VARCHAR(100),
    p_column_name VARCHAR(100)
)
RETURNS TABLE(
    classification_level VARCHAR(50),
    sensitivity_score INTEGER,
    encryption_required BOOLEAN,
    access_control_level VARCHAR(20),
    pii_flag BOOLEAN
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        dcm.classification_level,
        dc.sensitivity_score,
        dc.encryption_required,
        dc.access_control_level,
        dcm.pii_flag
    FROM data_classification_mapping dcm
    JOIN data_classification dc ON dcm.classification_level = dc.classification_level
    WHERE dcm.table_name = p_table_name
      AND dcm.column_name = p_column_name;
END;
$$ LANGUAGE plpgsql;

-- Data Sensitivity Report
CREATE OR REPLACE FUNCTION generate_sensitivity_report()
RETURNS TABLE(
    table_name VARCHAR(100),
    column_name VARCHAR(100),
    classification_level VARCHAR(50),
    sensitivity_score INTEGER,
    pii_flag BOOLEAN,
    encryption_status VARCHAR(20)
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        dcm.table_name,
        dcm.column_name,
        dcm.classification_level,
        dc.sensitivity_score,
        dcm.pii_flag,
        CASE 
            WHEN dcm.encryption_method IS NOT NULL THEN 'Encrypted'
            WHEN dc.encryption_required THEN 'Required'
            ELSE 'Not Required'
        END as encryption_status
    FROM data_classification_mapping dcm
    JOIN data_classification dc ON dcm.classification_level = dc.classification_level
    ORDER BY dc.sensitivity_score DESC, dcm.table_name, dcm.column_name;
END;
$$ LANGUAGE plpgsql;
```

## 🔄 Data Lineage Tracking

### 1. Data Lineage Framework

**Mục đích**: Track data flow và transformations across the system.

```sql
-- Data Lineage Tables
CREATE TABLE data_lineage (
    id SERIAL PRIMARY KEY,
    source_table VARCHAR(100),
    source_column VARCHAR(100),
    target_table VARCHAR(100),
    target_column VARCHAR(100),
    transformation_type VARCHAR(50), -- copy, aggregate, transform, derive
    transformation_logic TEXT,
    lineage_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE
);

-- Data Lineage Tracking
CREATE TABLE data_lineage_execution (
    id SERIAL PRIMARY KEY,
    lineage_id INTEGER REFERENCES data_lineage(id),
    execution_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source_record_count INTEGER,
    target_record_count INTEGER,
    processing_time_ms INTEGER,
    success_status BOOLEAN,
    error_message TEXT
);

-- Camera System Data Lineage
INSERT INTO data_lineage (source_table, source_column, target_table, target_column, transformation_type, transformation_logic, created_by) VALUES
-- Detection Data Flow
('detection_data', 'detection_timestamp', 'ml_features', 'feature_timestamp', 'copy', 'Direct copy of timestamp', 'system'),
('detection_data', 'camera_id', 'ml_features', 'camera_id', 'copy', 'Direct copy of camera_id', 'system'),
('detection_data', 'detection_type', 'ml_features', 'people_count', 'aggregate', 'COUNT WHERE detection_type = person', 'system'),
('detection_data', 'detection_type', 'ml_features', 'vehicle_count', 'aggregate', 'COUNT WHERE detection_type = vehicle', 'system'),

-- ML Features to Predictions
('ml_features', 'traffic_density', 'traffic_predictions', 'predicted_traffic_density', 'transform', 'ML model prediction', 'system'),
('ml_features', 'people_count', 'traffic_predictions', 'predicted_people_count', 'transform', 'ML model prediction', 'system'),

-- Camera Health to Monitoring
('camera_health_monitoring', 'camera_status', 'anomaly_detections', 'anomaly_type', 'derive', 'Derive anomaly type from status', 'system'),
('camera_health_monitoring', 'error_count', 'anomaly_detections', 'anomaly_score', 'transform', 'Calculate anomaly score from errors', 'system');

-- Data Lineage Tracking Function
CREATE OR REPLACE FUNCTION track_data_lineage(
    p_source_table VARCHAR(100),
    p_target_table VARCHAR(100),
    p_transformation_type VARCHAR(50),
    p_source_count INTEGER,
    p_target_count INTEGER,
    p_processing_time INTEGER
)
RETURNS INTEGER AS $$
DECLARE
    lineage_record_id INTEGER;
BEGIN
    -- Get lineage record
    SELECT id INTO lineage_record_id
    FROM data_lineage
    WHERE source_table = p_source_table
      AND target_table = p_target_table
      AND transformation_type = p_transformation_type
      AND is_active = TRUE
    LIMIT 1;
    
    IF lineage_record_id IS NOT NULL THEN
        -- Record execution
        INSERT INTO data_lineage_execution (
            lineage_id, source_record_count, target_record_count,
            processing_time_ms, success_status
        ) VALUES (
            lineage_record_id, p_source_count, p_target_count,
            p_processing_time, TRUE
        );
    END IF;
    
    RETURN lineage_record_id;
END;
$$ LANGUAGE plpgsql;
```

### 2. Data Lineage Visualization

```sql
-- Data Lineage Report
CREATE OR REPLACE FUNCTION generate_lineage_report()
RETURNS TABLE(
    source_table VARCHAR(100),
    source_column VARCHAR(100),
    target_table VARCHAR(100),
    target_column VARCHAR(100),
    transformation_type VARCHAR(50),
    last_execution TIMESTAMP,
    avg_processing_time_ms INTEGER,
    success_rate DECIMAL(5,2)
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        dl.source_table,
        dl.source_column,
        dl.target_table,
        dl.target_column,
        dl.transformation_type,
        MAX(dle.execution_timestamp) as last_execution,
        ROUND(AVG(dle.processing_time_ms)) as avg_processing_time_ms,
        ROUND((COUNT(*) FILTER (WHERE dle.success_status = TRUE) * 100.0) / COUNT(*), 2) as success_rate
    FROM data_lineage dl
    LEFT JOIN data_lineage_execution dle ON dl.id = dle.lineage_id
    WHERE dl.is_active = TRUE
    GROUP BY dl.id, dl.source_table, dl.source_column, dl.target_table, dl.target_column, dl.transformation_type
    ORDER BY dl.source_table, dl.target_table;
END;
$$ LANGUAGE plpgsql;
```

## 📋 Compliance Reporting

### 1. GDPR Compliance Framework

**Mục đích**: Đảm bảo compliance với GDPR và other privacy regulations.

```sql
-- GDPR Compliance Tables
CREATE TABLE gdpr_compliance (
    id SERIAL PRIMARY KEY,
    compliance_type VARCHAR(50), -- data_processing, data_retention, data_deletion, consent_management
    table_name VARCHAR(100),
    column_name VARCHAR(100),
    pii_category VARCHAR(50), -- personal_data, sensitive_data, special_category
    legal_basis VARCHAR(100), -- consent, legitimate_interest, contract, legal_obligation
    retention_period_days INTEGER,
    deletion_required BOOLEAN DEFAULT TRUE,
    consent_required BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- GDPR Compliance Mapping
INSERT INTO gdpr_compliance (compliance_type, table_name, column_name, pii_category, legal_basis, retention_period_days, consent_required) VALUES
-- User Data
('data_processing', 'users', 'email', 'personal_data', 'consent', 2555, TRUE),
('data_processing', 'users', 'phone_number', 'personal_data', 'consent', 2555, TRUE),
('data_processing', 'users', 'username', 'personal_data', 'legitimate_interest', 2555, FALSE),

-- Camera Data
('data_processing', 'camera_configurations', 'location_address', 'personal_data', 'legitimate_interest', 1825, FALSE),
('data_processing', 'detection_data', 'detection_timestamp', 'personal_data', 'legitimate_interest', 1095, FALSE),

-- AI Model Data
('data_processing', 'ai_models', 'model_parameters', 'sensitive_data', 'legitimate_interest', 3650, FALSE);

-- GDPR Compliance Report
CREATE OR REPLACE FUNCTION generate_gdpr_report()
RETURNS TABLE(
    table_name VARCHAR(100),
    column_name VARCHAR(100),
    pii_category VARCHAR(50),
    legal_basis VARCHAR(100),
    retention_period_days INTEGER,
    consent_required BOOLEAN,
    compliance_status VARCHAR(20)
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        gc.table_name,
        gc.column_name,
        gc.pii_category,
        gc.legal_basis,
        gc.retention_period_days,
        gc.consent_required,
        CASE 
            WHEN gc.consent_required AND gc.legal_basis = 'consent' THEN 'Compliant'
            WHEN NOT gc.consent_required AND gc.legal_basis != 'consent' THEN 'Compliant'
            ELSE 'Review Required'
        END as compliance_status
    FROM gdpr_compliance gc
    ORDER BY gc.table_name, gc.column_name;
END;
$$ LANGUAGE plpgsql;
```

### 2. Data Retention Management

```sql
-- Data Retention Management
CREATE TABLE data_retention_policies (
    id SERIAL PRIMARY KEY,
    table_name VARCHAR(100) NOT NULL,
    retention_period_days INTEGER NOT NULL,
    retention_type VARCHAR(50), -- archive, delete, anonymize
    archive_location VARCHAR(200),
    last_cleanup_date DATE,
    next_cleanup_date DATE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Data Retention Policies
INSERT INTO data_retention_policies (table_name, retention_period_days, retention_type, archive_location) VALUES
('detection_data', 1095, 'archive', '/archive/detection_data'),
('camera_health_monitoring', 730, 'delete', NULL),
('stream_quality_monitoring', 365, 'delete', NULL),
('ai_model_performance_monitoring', 1825, 'archive', '/archive/ai_models'),
('traffic_predictions', 730, 'delete', NULL),
('anomaly_detections', 1095, 'archive', '/archive/anomalies');

-- Data Cleanup Function
CREATE OR REPLACE FUNCTION cleanup_expired_data()
RETURNS TABLE(
    table_name VARCHAR(100),
    records_deleted INTEGER,
    cleanup_status VARCHAR(20)
) AS $$
DECLARE
    policy_record RECORD;
    deleted_count INTEGER;
BEGIN
    FOR policy_record IN 
        SELECT * FROM data_retention_policies 
        WHERE is_active = TRUE 
          AND next_cleanup_date <= CURRENT_DATE
    LOOP
        -- Delete expired records
        EXECUTE format('DELETE FROM %I WHERE created_at < NOW() - INTERVAL ''%s days''', 
                      policy_record.table_name, policy_record.retention_period_days);
        
        GET DIAGNOSTICS deleted_count = ROW_COUNT;
        
        -- Update cleanup dates
        UPDATE data_retention_policies
        SET 
            last_cleanup_date = CURRENT_DATE,
            next_cleanup_date = CURRENT_DATE + INTERVAL '30 days'
        WHERE id = policy_record.id;
        
        -- Return results
        RETURN QUERY SELECT 
            policy_record.table_name,
            deleted_count,
            CASE 
                WHEN deleted_count > 0 THEN 'Cleaned'
                ELSE 'No Data'
            END::VARCHAR(20);
    END LOOP;
END;
$$ LANGUAGE plpgsql;
```

## 📊 Data Quality Management

### 1. Data Quality Framework

**Mục đích**: Monitor và maintain data quality standards.

```sql
-- Data Quality Rules
CREATE TABLE data_quality_rules (
    id SERIAL PRIMARY KEY,
    rule_name VARCHAR(200) UNIQUE NOT NULL,
    table_name VARCHAR(100) NOT NULL,
    column_name VARCHAR(100),
    rule_type VARCHAR(50), -- completeness, accuracy, consistency, timeliness
    rule_condition TEXT,
    severity VARCHAR(20), -- low, medium, high, critical
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Data Quality Rules for Camera System
INSERT INTO data_quality_rules (rule_name, table_name, column_name, rule_type, rule_condition, severity) VALUES
-- Completeness Rules
('Camera ID Not Null', 'camera_configurations', 'camera_id', 'completeness', 'camera_id IS NOT NULL', 'critical'),
('Detection Timestamp Not Null', 'detection_data', 'detection_timestamp', 'completeness', 'detection_timestamp IS NOT NULL', 'critical'),
('User Email Not Null', 'users', 'email', 'completeness', 'email IS NOT NULL', 'high'),

-- Accuracy Rules
('Detection Confidence Range', 'detection_data', 'detection_confidence', 'accuracy', 'detection_confidence BETWEEN 0 AND 1', 'high'),
('Camera Status Valid', 'camera_configurations', 'camera_status', 'accuracy', 'camera_status IN (''online'', ''offline'', ''maintenance'', ''error'')', 'high'),
('Stream Quality Range', 'stream_quality_monitoring', 'quality_score', 'accuracy', 'quality_score BETWEEN 0 AND 1', 'medium'),

-- Consistency Rules
('Camera Reference Integrity', 'detection_data', 'camera_id', 'consistency', 'EXISTS (SELECT 1 FROM camera_configurations WHERE camera_id = detection_data.camera_id)', 'critical'),
('User Reference Integrity', 'camera_configurations', 'created_by', 'consistency', 'EXISTS (SELECT 1 FROM users WHERE id = camera_configurations.created_by)', 'high'),

-- Timeliness Rules
('Recent Detection Data', 'detection_data', 'detection_timestamp', 'timeliness', 'detection_timestamp > NOW() - INTERVAL ''1 day''', 'medium'),
('Recent Camera Health', 'camera_health_monitoring', 'metric_timestamp', 'timeliness', 'metric_timestamp > NOW() - INTERVAL ''1 hour''', 'high');

-- Data Quality Monitoring
CREATE TABLE data_quality_results (
    id SERIAL PRIMARY KEY,
    rule_id INTEGER REFERENCES data_quality_rules(id),
    check_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    records_checked INTEGER,
    records_failed INTEGER,
    failure_rate DECIMAL(5,2),
    quality_score DECIMAL(5,2),
    error_details JSONB,
    is_resolved BOOLEAN DEFAULT FALSE
);

-- Data Quality Check Function
CREATE OR REPLACE FUNCTION check_data_quality()
RETURNS TABLE(
    rule_name VARCHAR(200),
    table_name VARCHAR(100),
    rule_type VARCHAR(50),
    records_checked INTEGER,
    records_failed INTEGER,
    failure_rate DECIMAL(5,2),
    quality_score DECIMAL(5,2),
    status VARCHAR(20)
) AS $$
DECLARE
    rule_record RECORD;
    total_records INTEGER;
    failed_records INTEGER;
    failure_rate_val DECIMAL(5,2);
    quality_score_val DECIMAL(5,2);
BEGIN
    FOR rule_record IN 
        SELECT * FROM data_quality_rules WHERE is_active = TRUE
    LOOP
        -- Execute rule check
        EXECUTE format('SELECT COUNT(*) FROM %I', rule_record.table_name) INTO total_records;
        
        EXECUTE format('SELECT COUNT(*) FROM %I WHERE NOT (%s)', 
                      rule_record.table_name, rule_record.rule_condition) INTO failed_records;
        
        -- Calculate metrics
        failure_rate_val := CASE 
            WHEN total_records > 0 THEN (failed_records * 100.0) / total_records
            ELSE 0
        END;
        
        quality_score_val := 100.0 - failure_rate_val;
        
        -- Store results
        INSERT INTO data_quality_results (
            rule_id, records_checked, records_failed, failure_rate, quality_score
        ) VALUES (
            rule_record.id, total_records, failed_records, failure_rate_val, quality_score_val
        );
        
        -- Return results
        RETURN QUERY SELECT 
            rule_record.rule_name,
            rule_record.table_name,
            rule_record.rule_type,
            total_records,
            failed_records,
            failure_rate_val,
            quality_score_val,
            CASE 
                WHEN failure_rate_val = 0 THEN 'PASS'
                WHEN failure_rate_val < 5 THEN 'WARNING'
                ELSE 'FAIL'
            END::VARCHAR(20);
    END LOOP;
END;
$$ LANGUAGE plpgsql;
```

### 2. Data Quality Dashboard

```sql
-- Data Quality Dashboard
WITH quality_summary AS (
    SELECT 
        dqr.rule_type,
        COUNT(*) as total_rules,
        COUNT(*) FILTER (WHERE dqr.severity = 'critical') as critical_rules,
        COUNT(*) FILTER (WHERE dqr.severity = 'high') as high_rules,
        AVG(dqr2.quality_score) as avg_quality_score,
        COUNT(*) FILTER (WHERE dqr2.quality_score < 95) as rules_below_threshold
    FROM data_quality_rules dqr
    LEFT JOIN data_quality_results dqr2 ON dqr.id = dqr2.rule_id
    WHERE dqr.is_active = TRUE
      AND dqr2.check_timestamp > NOW() - INTERVAL '24 hours'
    GROUP BY dqr.rule_type
),
recent_failures AS (
    SELECT 
        dqr.rule_name,
        dqr.table_name,
        dqr.severity,
        dqr2.failure_rate,
        dqr2.check_timestamp
    FROM data_quality_results dqr2
    JOIN data_quality_rules dqr ON dqr2.rule_id = dqr.id
    WHERE dqr2.failure_rate > 0
      AND dqr2.check_timestamp > NOW() - INTERVAL '24 hours'
    ORDER BY dqr2.failure_rate DESC
    LIMIT 10
)
SELECT 
    'Quality Summary' as report_type,
    qs.rule_type,
    qs.total_rules,
    qs.critical_rules,
    qs.high_rules,
    ROUND(qs.avg_quality_score, 2) as avg_quality_score,
    qs.rules_below_threshold,
    CASE 
        WHEN qs.avg_quality_score >= 95 THEN '🟢 Excellent'
        WHEN qs.avg_quality_score >= 85 THEN '🟡 Good'
        WHEN qs.avg_quality_score >= 70 THEN '🟠 Fair'
        ELSE '🔴 Poor'
    END as quality_status
FROM quality_summary qs

UNION ALL

SELECT 
    'Recent Failures' as report_type,
    rf.rule_name as rule_type,
    0 as total_rules,
    0 as critical_rules,
    0 as high_rules,
    rf.failure_rate as avg_quality_score,
    0 as rules_below_threshold,
    CASE rf.severity
        WHEN 'critical' THEN '🔴 Critical'
        WHEN 'high' THEN '🟠 High'
        WHEN 'medium' THEN '🟡 Medium'
        ELSE '🟢 Low'
    END as quality_status
FROM recent_failures rf;
```

---

**Tài liệu này cung cấp comprehensive data governance framework cho AI Camera Counting System với data classification, lineage tracking, compliance reporting và quality management capabilities.** 