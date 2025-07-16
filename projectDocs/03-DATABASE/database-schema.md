# Database Schema - People Counting Dashboard

## Tổng quan Database

Hệ thống sử dụng PostgreSQL làm cơ sở dữ liệu chính với cấu trúc được thiết kế để hỗ trợ real-time people counting, analytics và reporting.

## Database Architecture

### 1. Database Diagram

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     users       │    │    cameras      │    │   count_data    │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│ id (PK)         │    │ id (PK)         │    │ id (PK)         │
│ username        │    │ name            │    │ camera_id (FK)  │
│ email           │    │ location        │    │ timestamp       │
│ password_hash   │    │ stream_url      │    │ people_in       │
│ role            │    │ status          │    │ people_out      │
│ created_at      │    │ settings        │    │ current_count   │
│ updated_at      │    │ created_at      │    │ confidence      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         │              ┌─────────────────┐              │
         └──────────────►│     alerts      │◄─────────────┘
                        ├─────────────────┤
                        │ id (PK)         │
                        │ type            │
                        │ severity        │
                        │ title           │
                        │ message         │
                        │ camera_id (FK)  │
                        │ user_id (FK)    │
                        │ is_read         │
                        │ created_at      │
                        └─────────────────┘
```

## Table Definitions

### 1. Users Table

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    role VARCHAR(20) DEFAULT 'user' CHECK (role IN ('admin', 'user', 'viewer')),
    is_active BOOLEAN DEFAULT TRUE,
    last_login TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_created_at ON users(created_at);

-- Trigger for updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_updated_at 
    BEFORE UPDATE ON users 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();
```

### 2. Cameras Table

```sql
CREATE TABLE cameras (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    ip_address VARCHAR(200),
    description TEXT,
    rtsp_url VARCHAR(500) NOT NULL,
    status VARCHAR(20) DEFAULT 'offline' CHECK (status IN ('online', 'offline', 'maintenance', 'error')),
    settings JSONB DEFAULT '{}',
    ai_model_version VARCHAR(50),
    detection_sensitivity DECIMAL(3,2) DEFAULT 0.8,
    counting_zones JSONB DEFAULT '[]',
    max_occupancy INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_cameras_name ON cameras(name);
CREATE INDEX idx_cameras_status ON cameras(status);
CREATE INDEX idx_cameras_ip_address ON cameras(ip_address);
CREATE INDEX idx_cameras_created_at ON cameras(created_at);
CREATE INDEX idx_cameras_settings ON cameras USING GIN(settings);

-- Trigger for updated_at
CREATE TRIGGER update_cameras_updated_at 
    BEFORE UPDATE ON cameras 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();
```

### 3. Count Data Table

```sql
CREATE TABLE count_data (
    id SERIAL PRIMARY KEY,
    camera_id INTEGER NOT NULL REFERENCES cameras(id) ON DELETE CASCADE,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    people_in INTEGER DEFAULT 0,
    people_out INTEGER DEFAULT 0,
    current_count INTEGER DEFAULT 0,
    occupancy DECIMAL(5,2),
    confidence DECIMAL(3,2),
    frame_data JSONB,
    detection_metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_count_data_camera_id ON count_data(camera_id);
CREATE INDEX idx_count_data_timestamp ON count_data(timestamp);
CREATE INDEX idx_count_data_camera_timestamp ON count_data(camera_id, timestamp);
CREATE INDEX idx_count_data_created_at ON count_data(created_at);

-- Partitioning for large datasets
CREATE TABLE count_data_y2024m01 PARTITION OF count_data
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

CREATE TABLE count_data_y2024m02 PARTITION OF count_data
    FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');
```

### 4. Alerts Table

```sql
CREATE TABLE alerts (
    id SERIAL PRIMARY KEY,
    type VARCHAR(50) NOT NULL CHECK (type IN ('camera_offline', 'system_error', 'high_traffic', 'maintenance', 'detection_error')),
    severity VARCHAR(20) NOT NULL CHECK (severity IN ('low', 'medium', 'high', 'critical')),
    title VARCHAR(200) NOT NULL,
    message TEXT,
    camera_id INTEGER REFERENCES cameras(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    is_read BOOLEAN DEFAULT FALSE,
    is_resolved BOOLEAN DEFAULT FALSE,
    resolved_at TIMESTAMP,
    resolved_by INTEGER REFERENCES users(id),
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_alerts_type ON alerts(type);
CREATE INDEX idx_alerts_severity ON alerts(severity);
CREATE INDEX idx_alerts_camera_id ON alerts(camera_id);
CREATE INDEX idx_alerts_user_id ON alerts(user_id);
CREATE INDEX idx_alerts_is_read ON alerts(is_read);
CREATE INDEX idx_alerts_created_at ON alerts(created_at);
CREATE INDEX idx_alerts_metadata ON alerts USING GIN(metadata);

-- Trigger for updated_at
CREATE TRIGGER update_alerts_updated_at 
    BEFORE UPDATE ON alerts 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();
```

### 5. Reports Table

```sql
CREATE TABLE reports (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    type VARCHAR(50) NOT NULL CHECK (type IN ('people-count', 'peak-hours', 'custom')),
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    parameters JSONB NOT NULL,
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    file_path VARCHAR(500),
    file_size INTEGER,
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'generating', 'completed', 'failed')),
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_reports_type ON reports(type);
CREATE INDEX idx_reports_user_id ON reports(user_id);
CREATE INDEX idx_reports_status ON reports(status);
CREATE INDEX idx_reports_generated_at ON reports(generated_at);
CREATE INDEX idx_reports_parameters ON reports USING GIN(parameters);
```

### 6. System Settings Table

```sql
CREATE TABLE system_settings (
    id SERIAL PRIMARY KEY,
    key VARCHAR(100) UNIQUE NOT NULL,
    value JSONB NOT NULL,
    description TEXT,
    is_public BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_system_settings_key ON system_settings(key);
CREATE INDEX idx_system_settings_is_public ON system_settings(is_public);

-- Trigger for updated_at
CREATE TRIGGER update_system_settings_updated_at 
    BEFORE UPDATE ON system_settings 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();
```

### 7. User Sessions Table

```sql
CREATE TABLE user_sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    session_token VARCHAR(255) UNIQUE NOT NULL,
    refresh_token VARCHAR(255) UNIQUE NOT NULL,
    ip_address INET,
    user_agent TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_user_sessions_user_id ON user_sessions(user_id);
CREATE INDEX idx_user_sessions_token ON user_sessions(session_token);
CREATE INDEX idx_user_sessions_refresh_token ON user_sessions(refresh_token);
CREATE INDEX idx_user_sessions_expires_at ON user_sessions(expires_at);
```

## Data Types and Constraints

### 1. JSONB Fields

#### Camera Settings
```json
{
  "detection_sensitivity": 0.8,
  "counting_zones": [
    {
      "id": "zone1",
      "name": "Entry Zone",
      "coordinates": [[x1, y1], [x2, y2], [x3, y3], [x4, y4]],
      "direction": "in"
    }
  ],
  "alert_thresholds": {
    "max_occupancy": 100,
    "min_occupancy": 5
  },
  "recording": {
    "enabled": true,
    "quality": "720p",
    "retention_days": 30
  }
}
```

#### Alert Metadata
```json
{
  "detection_confidence": 0.95,
  "frame_count": 150,
  "processing_time_ms": 45,
  "ai_model_version": "v1.2.0",
  "error_details": {
    "code": "CAMERA_TIMEOUT",
    "message": "Camera stream timeout"
  }
}
```

#### Report Parameters
```json
{
  "time_range": {
    "start": "2024-01-01T00:00:00Z",
    "end": "2024-01-31T23:59:59Z"
  },
  "cameras": [1, 2, 3],
  "filters": {
    "min_confidence": 0.8,
    "include_metadata": true
  },
  "format": "pdf",
  "include_charts": true
}
```

### 2. Enums and Constraints

```sql
-- Create custom types
CREATE TYPE user_role AS ENUM ('admin', 'user', 'viewer');
CREATE TYPE camera_status AS ENUM ('online', 'offline', 'maintenance', 'error');
CREATE TYPE alert_type AS ENUM ('camera_offline', 'system_error', 'high_traffic', 'maintenance', 'detection_error');
CREATE TYPE alert_severity AS ENUM ('low', 'medium', 'high', 'critical');
CREATE TYPE report_type AS ENUM ('people-count', 'peak-hours', 'custom');
CREATE TYPE report_status AS ENUM ('pending', 'generating', 'completed', 'failed');

-- Add constraints
ALTER TABLE users ADD CONSTRAINT chk_user_role CHECK (role IN ('admin', 'user', 'viewer'));
ALTER TABLE cameras ADD CONSTRAINT chk_camera_status CHECK (status IN ('online', 'offline', 'maintenance', 'error'));
ALTER TABLE alerts ADD CONSTRAINT chk_alert_type CHECK (type IN ('camera_offline', 'system_error', 'high_traffic', 'maintenance', 'detection_error'));
ALTER TABLE alerts ADD CONSTRAINT chk_alert_severity CHECK (severity IN ('low', 'medium', 'high', 'critical'));
```

## Views and Materialized Views

### 1. Camera Statistics View

```sql
CREATE VIEW camera_statistics AS
SELECT 
    c.id,
    c.name,
    c.location,
    c.status,
    COUNT(cd.id) as total_records,
    MAX(cd.timestamp) as last_update,
    SUM(cd.people_in) as total_people_in,
    SUM(cd.people_out) as total_people_out,
    AVG(cd.current_count) as avg_occupancy,
    MAX(cd.current_count) as peak_occupancy,
    AVG(cd.confidence) as avg_confidence
FROM cameras c
LEFT JOIN count_data cd ON c.id = cd.camera_id
GROUP BY c.id, c.name, c.location, c.status;
```

### 2. Daily Analytics View

```sql
CREATE VIEW daily_analytics AS
SELECT 
    DATE(timestamp) as date,
    camera_id,
    SUM(people_in) as daily_people_in,
    SUM(people_out) as daily_people_out,
    AVG(current_count) as avg_occupancy,
    MAX(current_count) as peak_occupancy,
    COUNT(*) as record_count
FROM count_data
GROUP BY DATE(timestamp), camera_id
ORDER BY date DESC, camera_id;
```

### 3. Alert Summary View

```sql
CREATE VIEW alert_summary AS
SELECT 
    type,
    severity,
    COUNT(*) as count,
    COUNT(*) FILTER (WHERE is_read = false) as unread_count,
    MIN(created_at) as first_occurrence,
    MAX(created_at) as last_occurrence
FROM alerts
GROUP BY type, severity
ORDER BY severity DESC, count DESC;
```

## Indexes and Performance

### 1. Primary Indexes

```sql
-- Composite indexes for common queries
CREATE INDEX idx_count_data_camera_timestamp ON count_data(camera_id, timestamp DESC);
CREATE INDEX idx_alerts_camera_created ON alerts(camera_id, created_at DESC);
CREATE INDEX idx_alerts_user_read ON alerts(user_id, is_read, created_at DESC);

-- Partial indexes for active data
CREATE INDEX idx_count_data_recent ON count_data(timestamp) 
WHERE timestamp > CURRENT_DATE - INTERVAL '30 days';

CREATE INDEX idx_alerts_unread ON alerts(created_at) 
WHERE is_read = false;
```

### 2. Full-Text Search Indexes

```sql
-- For searching camera names and locations
CREATE INDEX idx_cameras_search ON cameras 
USING gin(to_tsvector('english', name || ' ' || COALESCE(location, '')));

-- For searching alert messages
CREATE INDEX idx_alerts_search ON alerts 
USING gin(to_tsvector('english', title || ' ' || COALESCE(message, '')));
```

## Backup and Maintenance

### 1. Backup Strategy

```sql
-- Create backup tables for historical data
CREATE TABLE count_data_archive (
    LIKE count_data INCLUDING ALL
) PARTITION BY RANGE (timestamp);

-- Archive old data
INSERT INTO count_data_archive 
SELECT * FROM count_data 
WHERE timestamp < CURRENT_DATE - INTERVAL '1 year';

-- Clean up archived data
DELETE FROM count_data 
WHERE timestamp < CURRENT_DATE - INTERVAL '1 year';
```

### 2. Maintenance Procedures

```sql
-- Vacuum and analyze tables
VACUUM ANALYZE count_data;
VACUUM ANALYZE alerts;
VACUUM ANALYZE cameras;

-- Update statistics
ANALYZE count_data;
ANALYZE alerts;
ANALYZE cameras;

-- Clean up old sessions
DELETE FROM user_sessions 
WHERE expires_at < CURRENT_TIMESTAMP;

-- Clean up old reports
DELETE FROM reports 
WHERE created_at < CURRENT_DATE - INTERVAL '90 days';
```

## Security Considerations

### 1. Row Level Security (RLS)

```sql
-- Enable RLS on sensitive tables
ALTER TABLE count_data ENABLE ROW LEVEL SECURITY;
ALTER TABLE alerts ENABLE ROW LEVEL SECURITY;
ALTER TABLE cameras ENABLE ROW LEVEL SECURITY;

-- Create policies
CREATE POLICY count_data_access ON count_data
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM users 
            WHERE users.id = current_setting('app.current_user_id')::integer
        )
    );

CREATE POLICY alerts_access ON alerts
    FOR SELECT USING (
        user_id = current_setting('app.current_user_id')::integer
        OR EXISTS (
            SELECT 1 FROM users 
            WHERE users.id = current_setting('app.current_user_id')::integer 
            AND users.role = 'admin'
        )
    );
```

### 2. Data Encryption

```sql
-- Encrypt sensitive fields
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Update password hashing
UPDATE users 
SET password_hash = crypt(password_hash, gen_salt('bf'))
WHERE password_hash NOT LIKE '$2a$%';
```

## Monitoring and Logging

### 1. Audit Trail

```sql
-- Create audit log table
CREATE TABLE audit_log (
    id SERIAL PRIMARY KEY,
    table_name VARCHAR(50) NOT NULL,
    action VARCHAR(20) NOT NULL,
    record_id INTEGER,
    old_values JSONB,
    new_values JSONB,
    user_id INTEGER REFERENCES users(id),
    ip_address INET,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create audit triggers
CREATE OR REPLACE FUNCTION audit_trigger_function()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO audit_log (table_name, action, record_id, new_values, user_id)
        VALUES (TG_TABLE_NAME, 'INSERT', NEW.id, to_jsonb(NEW), current_setting('app.current_user_id')::integer);
        RETURN NEW;
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO audit_log (table_name, action, record_id, old_values, new_values, user_id)
        VALUES (TG_TABLE_NAME, 'UPDATE', NEW.id, to_jsonb(OLD), to_jsonb(NEW), current_setting('app.current_user_id')::integer);
        RETURN NEW;
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO audit_log (table_name, action, record_id, old_values, user_id)
        VALUES (TG_TABLE_NAME, 'DELETE', OLD.id, to_jsonb(OLD), current_setting('app.current_user_id')::integer);
        RETURN OLD;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- Apply audit triggers
CREATE TRIGGER audit_cameras_trigger
    AFTER INSERT OR UPDATE OR DELETE ON cameras
    FOR EACH ROW EXECUTE FUNCTION audit_trigger_function();

CREATE TRIGGER audit_alerts_trigger
    AFTER INSERT OR UPDATE OR DELETE ON alerts
    FOR EACH ROW EXECUTE FUNCTION audit_trigger_function();
``` 