# Database Schema - Authentication Service

## Tổng quan

Database schema được thiết kế để hỗ trợ authentication và user management cho hệ thống People Counting Dashboard. Sử dụng PostgreSQL với các tính năng bảo mật và performance optimization.

## Database Architecture

### Entity Relationship Diagram

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     users       │    │ user_sessions   │    │   audit_log     │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│ id (PK)         │    │ id (PK)         │    │ id (PK)         │
│ username        │    │ user_id (FK)    │    │ table_name      │
│ email           │    │ session_token   │    │ action          │
│ password_hash   │    │ refresh_token   │    │ record_id       │
│ first_name      │    │ ip_address      │    │ old_values      │
│ last_name       │    │ user_agent      │    │ new_values      │
│ role            │    │ is_active       │    │ user_id (FK)    │
│ is_active       │    │ expires_at      │    │ ip_address      │
│ last_login      │    │ created_at      │    │ timestamp       │
│ reset_token     │    └─────────────────┘    └─────────────────┘
│ reset_expires   │              │                       │
│ email_token     │              │                       │
│ email_verified  │              │                       │
│ created_at      │              │                       │
│ updated_at      │              │                       │
└─────────────────┘              │                       │
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │   Custom Types  │
                        ├─────────────────┤
                        │ user_role       │
                        │ camera_status   │
                        │ alert_type      │
                        │ alert_severity  │
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
```

**Column Descriptions:**
- `id`: Primary key, auto-increment
- `username`: Unique username, 3-50 characters
- `email`: Unique email address
- `password_hash`: bcrypt hashed password
- `first_name`: User's first name (optional)
- `last_name`: User's last name (optional)
- `role`: User role (admin, user, viewer)
- `is_active`: Account status
- `last_login`: Last login timestamp
- `reset_password_token`: Hashed reset token
- `reset_password_expires`: Reset token expiry
- `email_verification_token`: Email verification token
- `email_verified`: Email verification status
- `created_at`: Account creation timestamp
- `updated_at`: Last update timestamp

### 2. User Sessions Table

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
```

**Column Descriptions:**
- `id`: Primary key, auto-increment
- `user_id`: Foreign key to users table
- `session_token`: JWT session token
- `refresh_token`: JWT refresh token
- `ip_address`: Client IP address
- `user_agent`: Client user agent
- `is_active`: Session status
- `expires_at`: Session expiry timestamp
- `created_at`: Session creation timestamp

### 3. Audit Log Table

```sql
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
```

**Column Descriptions:**
- `id`: Primary key, auto-increment
- `table_name`: Name of the table being audited
- `action`: Type of action (INSERT, UPDATE, DELETE)
- `record_id`: ID of the affected record
- `old_values`: Previous values (JSONB)
- `new_values`: New values (JSONB)
- `user_id`: User who performed the action
- `ip_address`: IP address of the user
- `timestamp`: When the action occurred

## Custom Types

### User Role Enum

```sql
CREATE TYPE user_role AS ENUM ('admin', 'user', 'viewer');
```

**Role Descriptions:**
- `admin`: Full system access, user management
- `user`: Standard user access
- `viewer`: Read-only access

### Camera Status Enum

```sql
CREATE TYPE camera_status AS ENUM ('online', 'offline', 'maintenance', 'error');
```

### Alert Type Enum

```sql
CREATE TYPE alert_type AS ENUM ('camera_offline', 'system_error', 'high_traffic', 'maintenance', 'detection_error');
```

### Alert Severity Enum

```sql
CREATE TYPE alert_severity AS ENUM ('low', 'medium', 'high', 'critical');
```

## Indexes

### Primary Indexes

```sql
-- Users table indexes
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_created_at ON users(created_at);
CREATE INDEX idx_users_reset_token ON users(reset_password_token);

-- User sessions table indexes
CREATE INDEX idx_user_sessions_user_id ON user_sessions(user_id);
CREATE INDEX idx_user_sessions_token ON user_sessions(session_token);
CREATE INDEX idx_user_sessions_refresh_token ON user_sessions(refresh_token);
CREATE INDEX idx_user_sessions_expires_at ON user_sessions(expires_at);

-- Audit log table indexes
CREATE INDEX idx_audit_log_table_name ON audit_log(table_name);
CREATE INDEX idx_audit_log_user_id ON audit_log(user_id);
CREATE INDEX idx_audit_log_timestamp ON audit_log(timestamp);
```

### Composite Indexes

```sql
-- For common queries
CREATE INDEX idx_users_role_active ON users(role, is_active);
CREATE INDEX idx_user_sessions_user_active ON user_sessions(user_id, is_active);
CREATE INDEX idx_audit_log_table_action ON audit_log(table_name, action);
```

### Partial Indexes

```sql
-- For active sessions only
CREATE INDEX idx_user_sessions_active ON user_sessions(expires_at) 
WHERE is_active = true;

-- For unread audit logs
CREATE INDEX idx_audit_log_recent ON audit_log(timestamp) 
WHERE timestamp > CURRENT_DATE - INTERVAL '30 days';
```

## Constraints

### Check Constraints

```sql
-- Username format
ALTER TABLE users ADD CONSTRAINT chk_username_format 
CHECK (username ~ '^[a-zA-Z0-9_]{3,50}$');

-- Email format
ALTER TABLE users ADD CONSTRAINT chk_email_format 
CHECK (email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$');

-- Password hash format (bcrypt)
ALTER TABLE users ADD CONSTRAINT chk_password_hash_format 
CHECK (password_hash ~ '^\$2[aby]\$\d{1,2}\$[./A-Za-z0-9]{53}$');
```

### Foreign Key Constraints

```sql
-- User sessions reference users
ALTER TABLE user_sessions 
ADD CONSTRAINT fk_user_sessions_user_id 
FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;

-- Audit log reference users
ALTER TABLE audit_log 
ADD CONSTRAINT fk_audit_log_user_id 
FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL;
```

## Triggers

### Updated At Trigger

```sql
-- Function to update updated_at column
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger for users table
CREATE TRIGGER update_users_updated_at 
    BEFORE UPDATE ON users 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();
```

### Audit Trigger

```sql
-- Function to log changes
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
CREATE TRIGGER audit_users_trigger
    AFTER INSERT OR UPDATE OR DELETE ON users
    FOR EACH ROW EXECUTE FUNCTION audit_trigger_function();
```

## Views

### User Statistics View

```sql
CREATE VIEW user_statistics AS
SELECT 
    role,
    COUNT(*) as total_users,
    COUNT(*) FILTER (WHERE is_active = true) as active_users,
    COUNT(*) FILTER (WHERE is_active = false) as inactive_users,
    COUNT(*) FILTER (WHERE email_verified = true) as verified_users,
    AVG(EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - created_at))/86400) as avg_account_age_days,
    MAX(last_login) as last_user_login
FROM users
GROUP BY role
ORDER BY role;
```

### Session Statistics View

```sql
CREATE VIEW session_statistics AS
SELECT 
    u.username,
    u.role,
    COUNT(s.id) as total_sessions,
    COUNT(s.id) FILTER (WHERE s.is_active = true) as active_sessions,
    MAX(s.created_at) as last_session_created,
    MAX(s.expires_at) as latest_session_expiry
FROM users u
LEFT JOIN user_sessions s ON u.id = s.user_id
GROUP BY u.id, u.username, u.role
ORDER BY u.username;
```

## Data Types and Storage

### JSONB Fields

#### Audit Log Values
```json
{
  "old_values": {
    "username": "olduser",
    "email": "old@example.com",
    "is_active": true
  },
  "new_values": {
    "username": "newuser",
    "email": "new@example.com",
    "is_active": false
  }
}
```

### Timestamp Fields
- All timestamp fields use `TIMESTAMP` type
- Default to `CURRENT_TIMESTAMP`
- Timezone: UTC

### Network Address Fields
- `ip_address` uses `INET` type for IPv4/IPv6 support
- Automatic validation and formatting

## Security Considerations

### Row Level Security (RLS)

```sql
-- Enable RLS on sensitive tables
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE audit_log ENABLE ROW LEVEL SECURITY;

-- Create policies
CREATE POLICY users_access ON users
    FOR SELECT USING (
        current_setting('app.current_user_id')::integer = id
        OR EXISTS (
            SELECT 1 FROM users 
            WHERE users.id = current_setting('app.current_user_id')::integer 
            AND users.role = 'admin'
        )
    );

CREATE POLICY sessions_access ON user_sessions
    FOR SELECT USING (
        user_id = current_setting('app.current_user_id')::integer
    );
```

### Data Encryption

```sql
-- Enable pgcrypto extension
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Encrypt sensitive fields (if needed)
-- Example: Encrypt email verification tokens
UPDATE users 
SET email_verification_token = crypt(email_verification_token, gen_salt('bf'))
WHERE email_verification_token IS NOT NULL;
```

## Backup and Maintenance

### Backup Strategy

```sql
-- Create backup tables for historical data
CREATE TABLE users_archive (
    LIKE users INCLUDING ALL
) PARTITION BY RANGE (created_at);

-- Archive old data
INSERT INTO users_archive 
SELECT * FROM users 
WHERE created_at < CURRENT_DATE - INTERVAL '1 year';

-- Clean up archived data
DELETE FROM users 
WHERE created_at < CURRENT_DATE - INTERVAL '1 year';
```

### Maintenance Procedures

```sql
-- Vacuum and analyze tables
VACUUM ANALYZE users;
VACUUM ANALYZE user_sessions;
VACUUM ANALYZE audit_log;

-- Update statistics
ANALYZE users;
ANALYZE user_sessions;
ANALYZE audit_log;

-- Clean up old sessions
DELETE FROM user_sessions 
WHERE expires_at < CURRENT_TIMESTAMP;

-- Clean up old audit logs
DELETE FROM audit_log 
WHERE timestamp < CURRENT_DATE - INTERVAL '90 days';
```

## Performance Optimization

### Query Optimization

```sql
-- Use prepared statements
PREPARE get_user_by_username(text) AS
SELECT * FROM users WHERE username = $1;

-- Use indexes effectively
EXPLAIN ANALYZE SELECT * FROM users WHERE role = 'admin' AND is_active = true;

-- Monitor slow queries
SELECT query, mean_time, calls 
FROM pg_stat_statements 
ORDER BY mean_time DESC 
LIMIT 10;
```

### Connection Pooling

```sql
-- Configure connection pool settings
ALTER SYSTEM SET max_connections = 200;
ALTER SYSTEM SET shared_buffers = '256MB';
ALTER SYSTEM SET effective_cache_size = '1GB';
```

## Monitoring and Alerting

### Database Metrics

```sql
-- Monitor table sizes
SELECT 
    schemaname,
    tablename,
    attname,
    n_distinct,
    correlation
FROM pg_stats 
WHERE tablename IN ('users', 'user_sessions', 'audit_log');

-- Monitor index usage
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes 
WHERE tablename IN ('users', 'user_sessions', 'audit_log');
```

### Health Checks

```sql
-- Database health check
SELECT 
    'Database is healthy' as status,
    current_timestamp as checked_at,
    version() as postgres_version;

-- Table health check
SELECT 
    tablename,
    n_tup_ins as inserts,
    n_tup_upd as updates,
    n_tup_del as deletes,
    n_live_tup as live_rows,
    n_dead_tup as dead_rows
FROM pg_stat_user_tables 
WHERE tablename IN ('users', 'user_sessions', 'audit_log');
``` 