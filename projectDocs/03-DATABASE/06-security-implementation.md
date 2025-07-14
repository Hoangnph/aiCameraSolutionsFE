# Security Implementation Guide - AI Camera Counting System

## 📊 Tổng quan

Tài liệu này cung cấp hướng dẫn chi tiết về triển khai bảo mật database cho hệ thống AI Camera Counting, bao gồm authentication, authorization, encryption, audit logging, và compliance với các tiêu chuẩn bảo mật, với focus đặc biệt vào camera data security và video stream protection.

## 🎯 Mục tiêu bảo mật

- **Data Protection**: Bảo vệ dữ liệu nhạy cảm với encryption
- **Access Control**: Kiểm soát truy cập dựa trên role và permission
- **Audit Trail**: Ghi nhận đầy đủ các hoạt động truy cập
- **Compliance**: Tuân thủ GDPR, ISO 27001, SOC 2
- **Incident Response**: Phát hiện và xử lý sự cố bảo mật
- **Camera Data Security**: Bảo vệ camera feeds và video data
- **Video Stream Security**: Encryption cho video streams
- **Privacy Compliance**: GDPR compliance cho video data

## 🏗️ Security Architecture

### Database Security Layers

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              SECURITY ARCHITECTURE                              │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              APPLICATION LAYER                              │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Input     │  │   Session   │  │   API       │  │   Audit     │        │ │
│  │  │   Validation│  │   Management│  │   Security  │  │   Logging   │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                             │
│                                    ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              NETWORK LAYER                                  │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   TLS/SSL   │  │   VPN       │  │   Firewall  │  │   IDS/IPS   │        │ │
│  │  │   Encryption│  │   Tunnel    │  │   Rules     │  │   Detection │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                             │
│                                    ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              DATABASE LAYER                                 │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Authentication│  │   Authorization│  │   Encryption │  │   Audit     │        │ │
│  │  │   & Access   │  │   & Roles   │  │   & Keys   │  │   Logging   │        │ │
│  │  │   Control    │  │   Management│  │   Management│  │   & Monitoring│        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                             │
│                                    ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              STORAGE LAYER                                  │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Disk      │  │   Backup    │  │   Archive   │  │   Key       │        │ │
│  │  │   Encryption│  │   Encryption│  │   Encryption│  │   Management│        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 📹 Camera Data Security

### 1. Camera Data Encryption

**Mục đích**: Bảo vệ camera configuration và sensitive data.

```sql
-- Camera Configuration Encryption
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Encrypt camera stream credentials
ALTER TABLE camera_configurations 
ADD COLUMN stream_password_encrypted BYTEA;

-- Function to encrypt camera credentials
CREATE OR REPLACE FUNCTION encrypt_camera_credentials(
    p_username TEXT,
    p_password TEXT,
    p_camera_id VARCHAR(100)
)
RETURNS JSONB AS $$
DECLARE
    v_encrypted_username BYTEA;
    v_encrypted_password BYTEA;
    v_result JSONB;
BEGIN
    -- Encrypt username and password
    v_encrypted_username := pgp_sym_encrypt(p_username, current_setting('app.camera_encryption_key'));
    v_encrypted_password := pgp_sym_encrypt(p_password, current_setting('app.camera_encryption_key'));
    
    v_result := jsonb_build_object(
        'encrypted_username', encode(v_encrypted_username, 'base64'),
        'encrypted_password', encode(v_encrypted_password, 'base64'),
        'camera_id', p_camera_id,
        'encrypted_at', NOW()
    );
    
    RETURN v_result;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function to decrypt camera credentials
CREATE OR REPLACE FUNCTION decrypt_camera_credentials(
    p_encrypted_username TEXT,
    p_encrypted_password TEXT
)
RETURNS JSONB AS $$
DECLARE
    v_decrypted_username TEXT;
    v_decrypted_password TEXT;
    v_result JSONB;
BEGIN
    -- Decrypt username and password
    v_decrypted_username := pgp_sym_decrypt(decode(p_encrypted_username, 'base64'), current_setting('app.camera_encryption_key'));
    v_decrypted_password := pgp_sym_decrypt(decode(p_encrypted_password, 'base64'), current_setting('app.camera_encryption_key'));
    
    v_result := jsonb_build_object(
        'username', v_decrypted_username,
        'password', v_decrypted_password,
        'decrypted_at', NOW()
    );
    
    RETURN v_result;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Update existing camera configurations with encrypted passwords
UPDATE camera_configurations 
SET stream_password_encrypted = encode(
    pgp_sym_encrypt(stream_password, current_setting('app.camera_encryption_key')), 
    'base64'
)
WHERE stream_password IS NOT NULL;
```

### 2. Video Stream Security

**Mục đích**: Bảo vệ video stream data và metadata.

```sql
-- Video Stream Security Table
CREATE TABLE video_stream_security (
    id SERIAL PRIMARY KEY,
    stream_id VARCHAR(100) REFERENCES video_streams(stream_id),
    
    -- Stream Security Configuration
    encryption_enabled BOOLEAN DEFAULT TRUE,
    encryption_algorithm VARCHAR(50) DEFAULT 'AES-256',
    encryption_key_id VARCHAR(100),
    
    -- Access Control
    access_control_enabled BOOLEAN DEFAULT TRUE,
    allowed_ips INET[],
    allowed_users INTEGER[],
    access_token VARCHAR(255),
    
    -- Stream Protection
    watermark_enabled BOOLEAN DEFAULT TRUE,
    watermark_text TEXT,
    watermark_position VARCHAR(20) DEFAULT 'bottom-right',
    
    -- Privacy Protection
    face_blur_enabled BOOLEAN DEFAULT TRUE,
    license_plate_blur_enabled BOOLEAN DEFAULT TRUE,
    privacy_zones JSONB, -- areas to exclude from processing
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Stream Access Control Function
CREATE OR REPLACE FUNCTION check_stream_access(
    p_stream_id VARCHAR(100),
    p_user_id INTEGER,
    p_client_ip INET
)
RETURNS BOOLEAN AS $$
DECLARE
    v_access_allowed BOOLEAN := FALSE;
    v_stream_security RECORD;
BEGIN
    -- Get stream security configuration
    SELECT * INTO v_stream_security
    FROM video_stream_security
    WHERE stream_id = p_stream_id;
    
    -- Check if access control is enabled
    IF NOT v_stream_security.access_control_enabled THEN
        RETURN TRUE;
    END IF;
    
    -- Check IP address
    IF v_stream_security.allowed_ips IS NOT NULL AND 
       p_client_ip = ANY(v_stream_security.allowed_ips) THEN
        v_access_allowed := TRUE;
    END IF;
    
    -- Check user permissions
    IF v_stream_security.allowed_users IS NOT NULL AND 
       p_user_id = ANY(v_stream_security.allowed_users) THEN
        v_access_allowed := TRUE;
    END IF;
    
    RETURN v_access_allowed;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
```

### 3. Privacy Compliance (GDPR for Video Data)

**Mục đích**: Đảm bảo compliance với GDPR cho video data.

```sql
-- Privacy Compliance Table
CREATE TABLE privacy_compliance (
    id SERIAL PRIMARY KEY,
    camera_id VARCHAR(100) REFERENCES camera_configurations(camera_id),
    
    -- GDPR Compliance
    data_retention_days INTEGER DEFAULT 30,
    consent_required BOOLEAN DEFAULT TRUE,
    consent_collected BOOLEAN DEFAULT FALSE,
    consent_date TIMESTAMP,
    
    -- Data Subject Rights
    right_to_erasure_enabled BOOLEAN DEFAULT TRUE,
    right_to_portability_enabled BOOLEAN DEFAULT TRUE,
    right_to_rectification_enabled BOOLEAN DEFAULT TRUE,
    
    -- Privacy Settings
    face_detection_enabled BOOLEAN DEFAULT TRUE,
    personal_data_processing BOOLEAN DEFAULT FALSE,
    anonymization_enabled BOOLEAN DEFAULT TRUE,
    
    -- Legal Basis
    legal_basis VARCHAR(50), -- legitimate_interest, consent, contract
    purpose_of_processing TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- GDPR Data Erasure Function
CREATE OR REPLACE FUNCTION gdpr_data_erasure(
    p_camera_id VARCHAR(100),
    p_data_subject_id VARCHAR(100)
)
RETURNS JSONB AS $$
DECLARE
    v_erased_count INTEGER := 0;
    v_result JSONB;
BEGIN
    -- Erase person detection data
    DELETE FROM person_detections 
    WHERE camera_id = p_camera_id 
      AND object_attributes->>'data_subject_id' = p_data_subject_id;
    
    GET DIAGNOSTICS v_erased_count = ROW_COUNT;
    
    -- Erase tracking data
    DELETE FROM person_tracking 
    WHERE camera_id = p_camera_id 
      AND detection_id IN (
          SELECT detection_id FROM person_detections 
          WHERE object_attributes->>'data_subject_id' = p_data_subject_id
      );
    
    -- Erase counting events
    DELETE FROM counting_events 
    WHERE camera_id = p_camera_id 
      AND detection_id IN (
          SELECT detection_id FROM person_detections 
          WHERE object_attributes->>'data_subject_id' = p_data_subject_id
      );
    
    -- Log erasure
    INSERT INTO privacy_audit_log (
        camera_id, data_subject_id, action_type, details
    ) VALUES (
        p_camera_id, p_data_subject_id, 'data_erasure', 
        jsonb_build_object('erased_records', v_erased_count, 'erased_at', NOW())
    );
    
    v_result := jsonb_build_object(
        'camera_id', p_camera_id,
        'data_subject_id', p_data_subject_id,
        'erased_records', v_erased_count,
        'erased_at', NOW(),
        'status', 'completed'
    );
    
    RETURN v_result;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Privacy Audit Log
CREATE TABLE privacy_audit_log (
    id SERIAL PRIMARY KEY,
    camera_id VARCHAR(100),
    data_subject_id VARCHAR(100),
    action_type VARCHAR(50), -- data_erasure, consent_given, access_request
    details JSONB,
    user_id INTEGER REFERENCES users(id),
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🔐 Authentication & Access Control

### 1. Database User Management

**Mục đích**: Quản lý users và roles với least privilege principle.

```sql
-- Create Application Roles
CREATE ROLE ai_camera_app WITH LOGIN PASSWORD 'strong_password_here';
CREATE ROLE ai_camera_readonly WITH LOGIN PASSWORD 'readonly_password_here';
CREATE ROLE ai_camera_admin WITH LOGIN PASSWORD 'admin_password_here';

-- Create Service Roles
CREATE ROLE worker_service WITH LOGIN PASSWORD 'worker_password_here';
CREATE ROLE analytics_service WITH LOGIN PASSWORD 'analytics_password_here';
CREATE ROLE backup_service WITH LOGIN PASSWORD 'backup_password_here';

-- Set Connection Limits
ALTER ROLE ai_camera_app CONNECTION LIMIT 50;
ALTER ROLE ai_camera_readonly CONNECTION LIMIT 20;
ALTER ROLE worker_service CONNECTION LIMIT 100;
```

### 2. Role-based Access Control (RBAC)

```sql
-- Grant Permissions to Application Role
GRANT CONNECT ON DATABASE ai_camera_counting_db TO ai_camera_app;
GRANT USAGE ON SCHEMA public TO ai_camera_app;

-- Grant CRUD permissions
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO ai_camera_app;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO ai_camera_app;

-- Grant Read-only permissions
GRANT CONNECT ON DATABASE ai_camera_counting_db TO ai_camera_readonly;
GRANT USAGE ON SCHEMA public TO ai_camera_readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO ai_camera_readonly;

-- Grant Admin permissions
GRANT ALL PRIVILEGES ON DATABASE ai_camera_counting_db TO ai_camera_admin;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO ai_camera_admin;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO ai_camera_admin;
```

### 3. Row-Level Security (RLS)

```sql
-- Enable RLS on sensitive tables
ALTER TABLE counting_results ENABLE ROW LEVEL SECURITY;
ALTER TABLE camera_events ENABLE ROW LEVEL SECURITY;
ALTER TABLE analytics ENABLE ROW LEVEL SECURITY;
ALTER TABLE camera_configurations ENABLE ROW LEVEL SECURITY;
ALTER TABLE video_streams ENABLE ROW LEVEL SECURITY;

-- Create RLS Policies
CREATE POLICY camera_access_policy ON counting_results
    FOR ALL
    TO ai_camera_app
    USING (
        camera_id IN (
            SELECT camera_id FROM camera_permissions 
            WHERE user_id = current_setting('app.current_user_id')::integer
        )
    );

CREATE POLICY admin_access_policy ON counting_results
    FOR ALL
    TO ai_camera_admin
    USING (true);

-- Camera Events RLS
CREATE POLICY camera_events_policy ON camera_events
    FOR ALL
    TO ai_camera_app
    USING (
        camera_id IN (
            SELECT camera_id FROM camera_permissions 
            WHERE user_id = current_setting('app.current_user_id')::integer
        )
    );

-- Camera Configuration RLS
CREATE POLICY camera_config_policy ON camera_configurations
    FOR ALL
    TO ai_camera_app
    USING (
        tenant_id = current_setting('app.current_tenant_id')::integer
    );

-- Video Stream RLS
CREATE POLICY video_stream_policy ON video_streams
    FOR ALL
    TO ai_camera_app
    USING (
        camera_id IN (
            SELECT camera_id FROM camera_configurations 
            WHERE tenant_id = current_setting('app.current_tenant_id')::integer
        )
    );
```

## 🔒 Data Encryption

### 1. Column-level Encryption

```sql
-- Create encryption extension
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Encrypt sensitive columns
ALTER TABLE users 
ADD COLUMN password_hash_encrypted BYTEA;

-- Function to encrypt password
CREATE OR REPLACE FUNCTION encrypt_password(password_text TEXT)
RETURNS BYTEA AS $$
BEGIN
    RETURN pgp_sym_encrypt(password_text, current_setting('app.encryption_key'));
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function to decrypt password
CREATE OR REPLACE FUNCTION decrypt_password(password_encrypted BYTEA)
RETURNS TEXT AS $$
BEGIN
    RETURN pgp_sym_decrypt(password_encrypted, current_setting('app.encryption_key'));
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Encrypt camera passwords
UPDATE cameras 
SET password = encode(pgp_sym_encrypt(password, current_setting('app.encryption_key')), 'base64')
WHERE password IS NOT NULL;
```

### 2. Transparent Data Encryption (TDE)

```sql
-- Enable tablespace encryption
CREATE TABLESPACE encrypted_tablespace
LOCATION '/var/lib/postgresql/encrypted_data'
WITH (encryption = 'on');

-- Move sensitive tables to encrypted tablespace
ALTER TABLE users SET TABLESPACE encrypted_tablespace;
ALTER TABLE audit_logs SET TABLESPACE encrypted_tablespace;
ALTER TABLE user_sessions SET TABLESPACE encrypted_tablespace;
ALTER TABLE camera_configurations SET TABLESPACE encrypted_tablespace;
ALTER TABLE privacy_compliance SET TABLESPACE encrypted_tablespace;
```

### 3. Backup Encryption

```sql
-- Encrypted backup function
CREATE OR REPLACE FUNCTION create_encrypted_backup()
RETURNS TEXT AS $$
DECLARE
    v_backup_file TEXT;
    v_encrypted_file TEXT;
BEGIN
    -- Create backup file name
    v_backup_file := '/tmp/backup_' || to_char(NOW(), 'YYYYMMDD_HH24MISS') || '.sql';
    v_encrypted_file := v_backup_file || '.gpg';
    
    -- Create backup
    PERFORM pg_dump('ai_camera_counting_db', '--file=' || v_backup_file);
    
    -- Encrypt backup
    PERFORM system('gpg --encrypt --recipient backup-key ' || v_backup_file);
    
    -- Remove unencrypted backup
    PERFORM system('rm ' || v_backup_file);
    
    RETURN v_encrypted_file;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
```

## 📋 Audit Logging

### 1. Comprehensive Audit Trail

```sql
-- Enhanced Audit Log Table
CREATE TABLE audit_log (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER REFERENCES users(id),
    session_id VARCHAR(100),
    ip_address INET,
    user_agent TEXT,
    
    -- Action Details
    action_type VARCHAR(50), -- SELECT, INSERT, UPDATE, DELETE, LOGIN, LOGOUT
    table_name VARCHAR(100),
    record_id VARCHAR(100),
    column_name VARCHAR(100),
    
    -- Data Changes
    old_value TEXT,
    new_value TEXT,
    change_summary JSONB,
    
    -- Context
    application_name VARCHAR(100),
    module_name VARCHAR(100),
    operation_description TEXT,
    
    -- Security Context
    authentication_method VARCHAR(50),
    authorization_level VARCHAR(50),
    security_clearance VARCHAR(50)
);

-- Camera-specific Audit Triggers
CREATE OR REPLACE FUNCTION audit_camera_changes()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO audit_log (
            user_id, action_type, table_name, record_id, 
            new_value, change_summary, operation_description
        ) VALUES (
            current_setting('app.current_user_id')::integer,
            'INSERT',
            TG_TABLE_NAME,
            NEW.camera_id,
            to_json(NEW)::text,
            jsonb_build_object('operation', 'camera_created', 'camera_name', NEW.camera_name),
            'Camera configuration created'
        );
        RETURN NEW;
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO audit_log (
            user_id, action_type, table_name, record_id,
            old_value, new_value, change_summary, operation_description
        ) VALUES (
            current_setting('app.current_user_id')::integer,
            'UPDATE',
            TG_TABLE_NAME,
            NEW.camera_id,
            to_json(OLD)::text,
            to_json(NEW)::text,
            jsonb_build_object('operation', 'camera_updated', 'changes', 
                (SELECT jsonb_object_agg(key, value) FROM jsonb_each(to_json(NEW)) 
                 WHERE key NOT IN (SELECT key FROM jsonb_each(to_json(OLD))))),
            'Camera configuration updated'
        );
        RETURN NEW;
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO audit_log (
            user_id, action_type, table_name, record_id,
            old_value, change_summary, operation_description
        ) VALUES (
            current_setting('app.current_user_id')::integer,
            'DELETE',
            TG_TABLE_NAME,
            OLD.camera_id,
            to_json(OLD)::text,
            jsonb_build_object('operation', 'camera_deleted', 'camera_name', OLD.camera_name),
            'Camera configuration deleted'
        );
        RETURN OLD;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- Create audit triggers
CREATE TRIGGER audit_camera_configurations
    AFTER INSERT OR UPDATE OR DELETE ON camera_configurations
    FOR EACH ROW EXECUTE FUNCTION audit_camera_changes();

CREATE TRIGGER audit_video_streams
    AFTER INSERT OR UPDATE OR DELETE ON video_streams
    FOR EACH ROW EXECUTE FUNCTION audit_camera_changes();

CREATE TRIGGER audit_counting_results
    AFTER INSERT OR UPDATE OR DELETE ON counting_results
    FOR EACH ROW EXECUTE FUNCTION audit_camera_changes();
```

### 2. Security Event Monitoring

```sql
-- Security Events Table
CREATE TABLE security_events (
    id SERIAL PRIMARY KEY,
    event_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    event_type VARCHAR(50), -- failed_login, unauthorized_access, data_breach, etc.
    severity VARCHAR(20), -- low, medium, high, critical
    
    -- Event Details
    user_id INTEGER REFERENCES users(id),
    ip_address INET,
    user_agent TEXT,
    session_id VARCHAR(100),
    
    -- Event Context
    table_name VARCHAR(100),
    record_id VARCHAR(100),
    operation VARCHAR(50),
    
    -- Security Details
    threat_level VARCHAR(20),
    risk_score INTEGER,
    mitigation_action VARCHAR(100),
    
    -- Response
    is_responded BOOLEAN DEFAULT FALSE,
    response_action VARCHAR(100),
    response_timestamp TIMESTAMP,
    response_user_id INTEGER REFERENCES users(id)
);

-- Security Alert Function
CREATE OR REPLACE FUNCTION check_security_threats()
RETURNS TABLE(
    event_id INTEGER,
    threat_type VARCHAR(50),
    threat_level VARCHAR(20),
    recommended_action TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        se.id,
        se.event_type,
        se.severity,
        CASE 
            WHEN se.event_type = 'failed_login' AND se.risk_score > 80 THEN 'Block IP address and notify admin'
            WHEN se.event_type = 'unauthorized_access' THEN 'Immediate account suspension and investigation'
            WHEN se.event_type = 'data_breach' THEN 'Emergency response: isolate affected systems'
            ELSE 'Monitor and log for further analysis'
        END as recommended_action
    FROM security_events se
    WHERE se.event_timestamp > NOW() - INTERVAL '1 hour'
      AND se.severity IN ('high', 'critical')
      AND se.is_responded = FALSE
    ORDER BY se.event_timestamp DESC;
END;
$$ LANGUAGE plpgsql;
```

## 🛡️ Access Control for Camera Feeds

### 1. Camera Feed Access Control

```sql
-- Camera Feed Access Control Table
CREATE TABLE camera_feed_access (
    id SERIAL PRIMARY KEY,
    camera_id VARCHAR(100) REFERENCES camera_configurations(camera_id),
    user_id INTEGER REFERENCES users(id),
    
    -- Access Permissions
    can_view_live BOOLEAN DEFAULT FALSE,
    can_view_recorded BOOLEAN DEFAULT FALSE,
    can_control_camera BOOLEAN DEFAULT FALSE,
    can_configure_camera BOOLEAN DEFAULT FALSE,
    
    -- Time-based Access
    access_start_time TIME,
    access_end_time TIME,
    access_days_of_week INTEGER[], -- 0=Sunday, 1=Monday, etc.
    
    -- IP Restrictions
    allowed_ips INET[],
    allowed_networks CIDR[],
    
    -- Session Control
    max_concurrent_sessions INTEGER DEFAULT 1,
    session_timeout_minutes INTEGER DEFAULT 30,
    
    -- Audit Settings
    require_reason BOOLEAN DEFAULT TRUE,
    access_reason TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    created_by INTEGER REFERENCES users(id)
);

-- Camera Feed Access Check Function
CREATE OR REPLACE FUNCTION check_camera_feed_access(
    p_camera_id VARCHAR(100),
    p_user_id INTEGER,
    p_access_type VARCHAR(20), -- live, recorded, control, configure
    p_client_ip INET
)
RETURNS BOOLEAN AS $$
DECLARE
    v_access_record RECORD;
    v_current_time TIME := CURRENT_TIME;
    v_current_day INTEGER := EXTRACT(DOW FROM CURRENT_DATE);
    v_has_access BOOLEAN := FALSE;
BEGIN
    -- Get access record
    SELECT * INTO v_access_record
    FROM camera_feed_access
    WHERE camera_id = p_camera_id 
      AND user_id = p_user_id
      AND expires_at > NOW();
    
    -- Check if access record exists
    IF v_access_record IS NULL THEN
        RETURN FALSE;
    END IF;
    
    -- Check time-based access
    IF v_access_record.access_start_time IS NOT NULL AND 
       v_access_record.access_end_time IS NOT NULL THEN
        IF v_current_time < v_access_record.access_start_time OR 
           v_current_time > v_access_record.access_end_time THEN
            RETURN FALSE;
        END IF;
    END IF;
    
    -- Check day-based access
    IF v_access_record.access_days_of_week IS NOT NULL AND 
       v_current_day != ALL(v_access_record.access_days_of_week) THEN
        RETURN FALSE;
    END IF;
    
    -- Check IP restrictions
    IF v_access_record.allowed_ips IS NOT NULL AND 
       p_client_ip != ALL(v_access_record.allowed_ips) THEN
        RETURN FALSE;
    END IF;
    
    -- Check network restrictions
    IF v_access_record.allowed_networks IS NOT NULL THEN
        v_has_access := FALSE;
        FOR i IN 1..array_length(v_access_record.allowed_networks, 1) LOOP
            IF p_client_ip << v_access_record.allowed_networks[i] THEN
                v_has_access := TRUE;
                EXIT;
            END IF;
        END LOOP;
        IF NOT v_has_access THEN
            RETURN FALSE;
        END IF;
    END IF;
    
    -- Check specific permissions
    CASE p_access_type
        WHEN 'live' THEN
            RETURN v_access_record.can_view_live;
        WHEN 'recorded' THEN
            RETURN v_access_record.can_view_recorded;
        WHEN 'control' THEN
            RETURN v_access_record.can_control_camera;
        WHEN 'configure' THEN
            RETURN v_access_record.can_configure_camera;
        ELSE
            RETURN FALSE;
    END CASE;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
```

### 2. Real-time Access Monitoring

```sql
-- Camera Access Log
CREATE TABLE camera_access_log (
    id SERIAL PRIMARY KEY,
    camera_id VARCHAR(100) REFERENCES camera_configurations(camera_id),
    user_id INTEGER REFERENCES users(id),
    
    -- Access Details
    access_type VARCHAR(20), -- live, recorded, control, configure
    access_method VARCHAR(50), -- web, mobile, api
    client_ip INET,
    user_agent TEXT,
    session_id VARCHAR(100),
    
    -- Access Duration
    access_start TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    access_end TIMESTAMP,
    duration_seconds INTEGER,
    
    -- Access Result
    access_granted BOOLEAN,
    access_denied_reason TEXT,
    
    -- Security Context
    authentication_method VARCHAR(50),
    authorization_level VARCHAR(50),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Access Monitoring Function
CREATE OR REPLACE FUNCTION monitor_camera_access()
RETURNS TABLE(
    camera_id VARCHAR(100),
    user_id INTEGER,
    suspicious_activity TEXT,
    risk_score INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        cal.camera_id,
        cal.user_id,
        'Multiple failed access attempts'::TEXT as suspicious_activity,
        80 as risk_score
    FROM camera_access_log cal
    WHERE cal.access_start > NOW() - INTERVAL '1 hour'
      AND cal.access_granted = FALSE
    GROUP BY cal.camera_id, cal.user_id
    HAVING COUNT(*) > 5
    
    UNION ALL
    
    SELECT 
        cal.camera_id,
        cal.user_id,
        'Unusual access time'::TEXT as suspicious_activity,
        60 as risk_score
    FROM camera_access_log cal
    JOIN camera_feed_access cfa ON cal.camera_id = cfa.camera_id AND cal.user_id = cfa.user_id
    WHERE cal.access_start > NOW() - INTERVAL '1 hour'
      AND cal.access_granted = TRUE
      AND (EXTRACT(HOUR FROM cal.access_start) < 6 OR EXTRACT(HOUR FROM cal.access_start) > 22)
      AND cfa.access_start_time IS NOT NULL
      AND (EXTRACT(HOUR FROM cal.access_start) < cfa.access_start_time OR EXTRACT(HOUR FROM cal.access_start) > cfa.access_end_time);
END;
$$ LANGUAGE plpgsql;
```

## 📊 Security Monitoring Dashboard

### 1. Security Metrics Query

```sql
-- Security Dashboard Query
WITH security_summary AS (
    SELECT 
        'failed_logins' as metric_type,
        COUNT(*) as count,
        COUNT(*) FILTER (WHERE event_timestamp > NOW() - INTERVAL '1 hour') as recent_count
    FROM security_events
    WHERE event_type = 'failed_login'
    
    UNION ALL
    
    SELECT 
        'unauthorized_access' as metric_type,
        COUNT(*) as count,
        COUNT(*) FILTER (WHERE event_timestamp > NOW() - INTERVAL '1 hour') as recent_count
    FROM security_events
    WHERE event_type = 'unauthorized_access'
    
    UNION ALL
    
    SELECT 
        'camera_access_violations' as metric_type,
        COUNT(*) as count,
        COUNT(*) FILTER (WHERE access_start > NOW() - INTERVAL '1 hour') as recent_count
    FROM camera_access_log
    WHERE access_granted = FALSE
)
SELECT 
    metric_type,
    count as total_count,
    recent_count,
    CASE 
        WHEN recent_count > 10 THEN 'critical'
        WHEN recent_count > 5 THEN 'warning'
        ELSE 'normal'
    END as security_status
FROM security_summary
ORDER BY recent_count DESC;
```

---

**Tài liệu này cung cấp hướng dẫn bảo mật hoàn chỉnh cho hệ thống AI Camera Counting, bao gồm camera data security, video stream protection, privacy compliance (GDPR), access control cho camera feeds, và comprehensive security monitoring với enterprise-grade security measures.** 