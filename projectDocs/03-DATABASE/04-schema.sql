-- Database Schema for AI Camera Counting System (beCamera)
-- PostgreSQL Database Schema
-- Version: 1.0
-- Created: 2024
-- Description: Complete database schema for AI Camera Counting System

-- =============================================================================
-- DATABASE INITIALIZATION
-- =============================================================================

-- Create database if not exists (this will be handled by docker-compose)
-- CREATE DATABASE ai_camera_counting_db;

-- Connect to the database
\c ai_camera_counting_db;

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "pg_stat_statements";

-- =============================================================================
-- CUSTOM TYPES
-- =============================================================================

-- User role enumeration
DO $$ BEGIN
    CREATE TYPE user_role AS ENUM ('admin', 'user', 'viewer');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- Camera status enumeration
DO $$ BEGIN
    CREATE TYPE camera_status AS ENUM ('online', 'offline', 'maintenance', 'error');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- Event type enumeration
DO $$ BEGIN
    CREATE TYPE event_type AS ENUM ('connection', 'detection', 'error', 'maintenance', 'system');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- Event severity enumeration
DO $$ BEGIN
    CREATE TYPE event_severity AS ENUM ('info', 'warning', 'error', 'critical');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- Alert type enumeration
DO $$ BEGIN
    CREATE TYPE alert_type AS ENUM ('camera_offline', 'system_error', 'high_traffic', 'maintenance', 'detection_error');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- Alert severity enumeration
DO $$ BEGIN
    CREATE TYPE alert_severity AS ENUM ('low', 'medium', 'high', 'critical');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- Model type enumeration
DO $$ BEGIN
    CREATE TYPE model_type AS ENUM ('detection', 'classification', 'tracking', 'segmentation');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- Model status enumeration
DO $$ BEGIN
    CREATE TYPE model_status AS ENUM ('active', 'inactive', 'training', 'error');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- Zone type enumeration
DO $$ BEGIN
    CREATE TYPE zone_type AS ENUM ('entrance', 'exit', 'area', 'line');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- Zone direction enumeration
DO $$ BEGIN
    CREATE TYPE zone_direction AS ENUM ('in', 'out', 'bidirectional');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- Period type enumeration
DO $$ BEGIN
    CREATE TYPE period_type AS ENUM ('hour', 'day', 'week', 'month', 'year');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- File type enumeration
DO $$ BEGIN
    CREATE TYPE file_type AS ENUM ('media', 'document', 'log', 'backup', 'config');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- =============================================================================
-- CORE TABLES
-- =============================================================================

-- Users table (synchronized with beAuth)
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    role user_role DEFAULT 'user',
    is_active BOOLEAN DEFAULT TRUE,
    last_login TIMESTAMP,
    reset_password_token VARCHAR(255),
    reset_password_expires TIMESTAMP,
    email_verification_token VARCHAR(255),
    email_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- AI Models table
CREATE TABLE IF NOT EXISTS ai_models (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    version VARCHAR(50) NOT NULL,
    description TEXT,
    model_type model_type DEFAULT 'detection',
    file_path VARCHAR(500),
    file_size BIGINT,
    checksum VARCHAR(64),
    status model_status DEFAULT 'inactive',
    accuracy DECIMAL(5,4),
    inference_time_ms INTEGER,
    config JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(name, version)
);

-- Cameras table
CREATE TABLE IF NOT EXISTS cameras (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    ip_address INET NOT NULL,
    port INTEGER DEFAULT 554,
    rtsp_url VARCHAR(500) NOT NULL,
    username VARCHAR(50),
    password VARCHAR(255),
    model VARCHAR(100),
    manufacturer VARCHAR(100),
    resolution_width INTEGER,
    resolution_height INTEGER,
    fps INTEGER DEFAULT 25,
    status camera_status DEFAULT 'offline',
    is_active BOOLEAN DEFAULT TRUE,
    ai_model_id INTEGER REFERENCES ai_models(id),
    config JSONB DEFAULT '{}',
    last_heartbeat TIMESTAMP,
    last_error TEXT,
    error_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Zones table
CREATE TABLE IF NOT EXISTS zones (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    camera_id INTEGER NOT NULL REFERENCES cameras(id) ON DELETE CASCADE,
    zone_type zone_type DEFAULT 'entrance',
    coordinates JSONB NOT NULL,
    direction zone_direction DEFAULT 'bidirectional',
    is_active BOOLEAN DEFAULT TRUE,
    config JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================================================================
-- EVENT TABLES
-- =============================================================================

-- Camera Events table
CREATE TABLE IF NOT EXISTS camera_events (
    id SERIAL PRIMARY KEY,
    camera_id INTEGER NOT NULL REFERENCES cameras(id) ON DELETE CASCADE,
    event_type event_type NOT NULL,
    severity event_severity DEFAULT 'info',
    message TEXT,
    data JSONB DEFAULT '{}',
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Model Logs table
CREATE TABLE IF NOT EXISTS model_logs (
    id SERIAL PRIMARY KEY,
    model_id INTEGER NOT NULL REFERENCES ai_models(id) ON DELETE CASCADE,
    log_type event_type NOT NULL,
    severity event_severity DEFAULT 'info',
    message TEXT,
    data JSONB DEFAULT '{}',
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User Sessions table
CREATE TABLE IF NOT EXISTS user_sessions (
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

-- =============================================================================
-- DATA TABLES
-- =============================================================================

-- Counting Results table
CREATE TABLE IF NOT EXISTS counting_results (
    id SERIAL PRIMARY KEY,
    camera_id INTEGER NOT NULL REFERENCES cameras(id) ON DELETE CASCADE,
    zone_id INTEGER NOT NULL REFERENCES zones(id) ON DELETE CASCADE,
    timestamp TIMESTAMP NOT NULL,
    count_in INTEGER DEFAULT 0,
    count_out INTEGER DEFAULT 0,
    total_count INTEGER DEFAULT 0,
    confidence DECIMAL(5,4),
    frame_data JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Analytics table
CREATE TABLE IF NOT EXISTS analytics (
    id SERIAL PRIMARY KEY,
    camera_id INTEGER NOT NULL REFERENCES cameras(id) ON DELETE CASCADE,
    zone_id INTEGER REFERENCES zones(id) ON DELETE CASCADE,
    period_type period_type NOT NULL,
    period_start TIMESTAMP NOT NULL,
    period_end TIMESTAMP NOT NULL,
    total_count_in INTEGER DEFAULT 0,
    total_count_out INTEGER DEFAULT 0,
    peak_count INTEGER DEFAULT 0,
    peak_time TIMESTAMP,
    avg_count DECIMAL(10,2) DEFAULT 0,
    data_points INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================================================================
-- SYSTEM TABLES
-- =============================================================================

-- Alerts table
CREATE TABLE IF NOT EXISTS alerts (
    id SERIAL PRIMARY KEY,
    alert_type alert_type NOT NULL,
    severity alert_severity DEFAULT 'medium',
    title VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    camera_id INTEGER REFERENCES cameras(id) ON DELETE CASCADE,
    zone_id INTEGER REFERENCES zones(id) ON DELETE CASCADE,
    data JSONB DEFAULT '{}',
    is_resolved BOOLEAN DEFAULT FALSE,
    resolved_at TIMESTAMP,
    resolved_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Audit Logs table
CREATE TABLE IF NOT EXISTS audit_logs (
    id SERIAL PRIMARY KEY,
    table_name VARCHAR(50) NOT NULL,
    action VARCHAR(20) NOT NULL,
    record_id INTEGER,
    old_values JSONB,
    new_values JSONB,
    user_id INTEGER REFERENCES users(id),
    ip_address INET,
    user_agent TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Files table
CREATE TABLE IF NOT EXISTS files (
    id SERIAL PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    original_filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_size BIGINT NOT NULL,
    mime_type VARCHAR(100),
    file_type file_type DEFAULT 'media',
    camera_id INTEGER REFERENCES cameras(id) ON DELETE CASCADE,
    zone_id INTEGER REFERENCES zones(id) ON DELETE CASCADE,
    metadata JSONB DEFAULT '{}',
    is_public BOOLEAN DEFAULT FALSE,
    expires_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- System Logs table
CREATE TABLE IF NOT EXISTS system_logs (
    id SERIAL PRIMARY KEY,
    log_level event_severity NOT NULL,
    component VARCHAR(100) NOT NULL,
    message TEXT NOT NULL,
    data JSONB DEFAULT '{}',
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================================================================
-- INDEXES
-- =============================================================================

-- Users indexes
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);
CREATE INDEX IF NOT EXISTS idx_users_created_at ON users(created_at);
CREATE INDEX IF NOT EXISTS idx_users_reset_token ON users(reset_password_token);

-- AI Models indexes
CREATE INDEX IF NOT EXISTS idx_ai_models_name_version ON ai_models(name, version);
CREATE INDEX IF NOT EXISTS idx_ai_models_status ON ai_models(status);
CREATE INDEX IF NOT EXISTS idx_ai_models_model_type ON ai_models(model_type);

-- Cameras indexes
CREATE INDEX IF NOT EXISTS idx_cameras_ip_address ON cameras(ip_address);
CREATE INDEX IF NOT EXISTS idx_cameras_status ON cameras(status);
CREATE INDEX IF NOT EXISTS idx_cameras_is_active ON cameras(is_active);
CREATE INDEX IF NOT EXISTS idx_cameras_ai_model_id ON cameras(ai_model_id);
CREATE INDEX IF NOT EXISTS idx_cameras_last_heartbeat ON cameras(last_heartbeat);

-- Zones indexes
CREATE INDEX IF NOT EXISTS idx_zones_camera_id ON zones(camera_id);
CREATE INDEX IF NOT EXISTS idx_zones_zone_type ON zones(zone_type);
CREATE INDEX IF NOT EXISTS idx_zones_is_active ON zones(is_active);

-- Camera Events indexes
CREATE INDEX IF NOT EXISTS idx_camera_events_camera_id ON camera_events(camera_id);
CREATE INDEX IF NOT EXISTS idx_camera_events_event_type ON camera_events(event_type);
CREATE INDEX IF NOT EXISTS idx_camera_events_severity ON camera_events(severity);
CREATE INDEX IF NOT EXISTS idx_camera_events_timestamp ON camera_events(timestamp);

-- Model Logs indexes
CREATE INDEX IF NOT EXISTS idx_model_logs_model_id ON model_logs(model_id);
CREATE INDEX IF NOT EXISTS idx_model_logs_log_type ON model_logs(log_type);
CREATE INDEX IF NOT EXISTS idx_model_logs_timestamp ON model_logs(timestamp);

-- User Sessions indexes
CREATE INDEX IF NOT EXISTS idx_user_sessions_user_id ON user_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_user_sessions_token ON user_sessions(session_token);
CREATE INDEX IF NOT EXISTS idx_user_sessions_refresh_token ON user_sessions(refresh_token);
CREATE INDEX IF NOT EXISTS idx_user_sessions_expires_at ON user_sessions(expires_at);

-- Counting Results indexes
CREATE INDEX IF NOT EXISTS idx_counting_results_camera_id ON counting_results(camera_id);
CREATE INDEX IF NOT EXISTS idx_counting_results_zone_id ON counting_results(zone_id);
CREATE INDEX IF NOT EXISTS idx_counting_results_timestamp ON counting_results(timestamp);
CREATE INDEX IF NOT EXISTS idx_counting_results_camera_timestamp ON counting_results(camera_id, timestamp);

-- Analytics indexes
CREATE INDEX IF NOT EXISTS idx_analytics_camera_id ON analytics(camera_id);
CREATE INDEX IF NOT EXISTS idx_analytics_zone_id ON analytics(zone_id);
CREATE INDEX IF NOT EXISTS idx_analytics_period_type ON analytics(period_type);
CREATE INDEX IF NOT EXISTS idx_analytics_period_start ON analytics(period_start);
CREATE INDEX IF NOT EXISTS idx_analytics_camera_period ON analytics(camera_id, period_type, period_start);

-- Alerts indexes
CREATE INDEX IF NOT EXISTS idx_alerts_alert_type ON alerts(alert_type);
CREATE INDEX IF NOT EXISTS idx_alerts_severity ON alerts(severity);
CREATE INDEX IF NOT EXISTS idx_alerts_camera_id ON alerts(camera_id);
CREATE INDEX IF NOT EXISTS idx_alerts_is_resolved ON alerts(is_resolved);
CREATE INDEX IF NOT EXISTS idx_alerts_created_at ON alerts(created_at);

-- Audit Logs indexes
CREATE INDEX IF NOT EXISTS idx_audit_logs_table_name ON audit_logs(table_name);
CREATE INDEX IF NOT EXISTS idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_timestamp ON audit_logs(timestamp);
CREATE INDEX IF NOT EXISTS idx_audit_logs_action ON audit_logs(action);

-- Files indexes
CREATE INDEX IF NOT EXISTS idx_files_camera_id ON files(camera_id);
CREATE INDEX IF NOT EXISTS idx_files_file_type ON files(file_type);
CREATE INDEX IF NOT EXISTS idx_files_created_at ON files(created_at);
CREATE INDEX IF NOT EXISTS idx_files_expires_at ON files(expires_at);

-- System Logs indexes
CREATE INDEX IF NOT EXISTS idx_system_logs_log_level ON system_logs(log_level);
CREATE INDEX IF NOT EXISTS idx_system_logs_component ON system_logs(component);
CREATE INDEX IF NOT EXISTS idx_system_logs_timestamp ON system_logs(timestamp);

-- =============================================================================
-- TRIGGERS AND FUNCTIONS
-- =============================================================================

-- Function to update updated_at column
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Function to create audit log entry
CREATE OR REPLACE FUNCTION create_audit_log()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO audit_logs (table_name, action, record_id, new_values, user_id, ip_address, user_agent)
        VALUES (TG_TABLE_NAME, 'INSERT', NEW.id, to_jsonb(NEW), current_setting('app.current_user_id', true)::integer, inet_client_addr(), current_setting('app.user_agent', true));
        RETURN NEW;
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO audit_logs (table_name, action, record_id, old_values, new_values, user_id, ip_address, user_agent)
        VALUES (TG_TABLE_NAME, 'UPDATE', NEW.id, to_jsonb(OLD), to_jsonb(NEW), current_setting('app.current_user_id', true)::integer, inet_client_addr(), current_setting('app.user_agent', true));
        RETURN NEW;
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO audit_logs (table_name, action, record_id, old_values, user_id, ip_address, user_agent)
        VALUES (TG_TABLE_NAME, 'DELETE', OLD.id, to_jsonb(OLD), current_setting('app.current_user_id', true)::integer, inet_client_addr(), current_setting('app.user_agent', true));
        RETURN OLD;
    END IF;
    RETURN NULL;
END;
$$ language 'plpgsql';

-- Create triggers for updated_at
DROP TRIGGER IF EXISTS update_users_updated_at ON users;
CREATE TRIGGER update_users_updated_at 
    BEFORE UPDATE ON users 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_ai_models_updated_at ON ai_models;
CREATE TRIGGER update_ai_models_updated_at 
    BEFORE UPDATE ON ai_models 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_cameras_updated_at ON cameras;
CREATE TRIGGER update_cameras_updated_at 
    BEFORE UPDATE ON cameras 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_zones_updated_at ON zones;
CREATE TRIGGER update_zones_updated_at 
    BEFORE UPDATE ON zones 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_analytics_updated_at ON analytics;
CREATE TRIGGER update_analytics_updated_at 
    BEFORE UPDATE ON analytics 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_alerts_updated_at ON alerts;
CREATE TRIGGER update_alerts_updated_at 
    BEFORE UPDATE ON alerts 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Create triggers for audit logging
DROP TRIGGER IF EXISTS audit_users ON users;
CREATE TRIGGER audit_users
    AFTER INSERT OR UPDATE OR DELETE ON users
    FOR EACH ROW EXECUTE FUNCTION create_audit_log();

DROP TRIGGER IF EXISTS audit_cameras ON cameras;
CREATE TRIGGER audit_cameras
    AFTER INSERT OR UPDATE OR DELETE ON cameras
    FOR EACH ROW EXECUTE FUNCTION create_audit_log();

DROP TRIGGER IF EXISTS audit_zones ON zones;
CREATE TRIGGER audit_zones
    AFTER INSERT OR UPDATE OR DELETE ON zones
    FOR EACH ROW EXECUTE FUNCTION create_audit_log();

DROP TRIGGER IF EXISTS audit_ai_models ON ai_models;
CREATE TRIGGER audit_ai_models
    AFTER INSERT OR UPDATE OR DELETE ON ai_models
    FOR EACH ROW EXECUTE FUNCTION create_audit_log();

-- =============================================================================
-- PARTITIONING
-- =============================================================================

-- Partition counting_results by month
CREATE TABLE IF NOT EXISTS counting_results_y2024m01 PARTITION OF counting_results
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

CREATE TABLE IF NOT EXISTS counting_results_y2024m02 PARTITION OF counting_results
    FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');

-- Partition camera_events by month
CREATE TABLE IF NOT EXISTS camera_events_y2024m01 PARTITION OF camera_events
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

CREATE TABLE IF NOT EXISTS camera_events_y2024m02 PARTITION OF camera_events
    FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');

-- =============================================================================
-- SAMPLE DATA
-- =============================================================================

-- Insert default admin user (password: Admin123!)
INSERT INTO users (username, email, password_hash, first_name, last_name, role, is_active, email_verified)
VALUES (
    'admin',
    'admin@aicamera.com',
    '$2a$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HS.iK8O', -- Admin123!
    'System',
    'Administrator',
    'admin',
    true,
    true
) ON CONFLICT (username) DO NOTHING;

-- Insert default AI model
INSERT INTO ai_models (name, version, description, model_type, status, accuracy, inference_time_ms)
VALUES (
    'YOLO-v8',
    '1.0.0',
    'YOLO v8 for person detection',
    'detection',
    'active',
    0.95,
    50
) ON CONFLICT (name, version) DO NOTHING;

-- =============================================================================
-- PERMISSIONS
-- =============================================================================

-- Grant permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO postgres;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO postgres;

-- =============================================================================
-- COMPLETION
-- =============================================================================

-- Log completion
SELECT 'Database schema initialization completed successfully!' as status; 