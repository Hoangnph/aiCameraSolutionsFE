# Production Advanced Security Implementation - AI Camera Counting System

## 📊 Tổng quan

Tài liệu này trình bày chiến lược bảo mật nâng cao cho hệ thống AI Camera Counting trong môi trường production, bao gồm encryption, access control, threat detection và security monitoring.

## 🎯 Mục tiêu Security

- **Data Protection**: Bảo vệ dữ liệu ở mọi trạng thái (at rest, in transit, in use)
- **Access Control**: Kiểm soát truy cập chặt chẽ với least privilege principle
- **Threat Detection**: Phát hiện và ngăn chặn các mối đe dọa bảo mật
- **Compliance**: Tuân thủ các tiêu chuẩn bảo mật (SOC2, ISO27001, PCI DSS)
- **Incident Response**: Xử lý sự cố bảo mật nhanh chóng và hiệu quả

## 🏗️ Security Architecture

### Multi-Layer Security Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              SECURITY ARCHITECTURE                              │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              NETWORK SECURITY LAYER                         │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   WAF       │  │   DDoS      │  │   VPN       │  │   Firewall  │        │ │
│  │  │   (Web      │  │   Protection│  │   Gateway   │  │   Rules     │        │ │
│  │  │   Application│  │             │  │             │  │             │        │ │
│  │  │   Firewall) │  │ • Rate      │  │ • Site-to-  │  │ • Network   │        │ │
│  │  │             │  │   Limiting  │  │   Site      │  │   Access    │        │ │
│  │  │ • SQL       │  │ • Traffic   │  │ • Client-to-│  │   Control   │        │ │
│  │  │   Injection │  │   Filtering │  │   Site      │  │ • Port      │        │ │
│  │  │ • XSS       │  │ • Bot       │  │ • Encryption│  │   Filtering │        │ │
│  │  │   Protection│  │   Detection │  │ • Authentication│ • Protocol  │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                             │
│                                    ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              APPLICATION SECURITY LAYER                     │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   API       │  │   Session   │  │   Input     │  │   Output    │        │ │
│  │  │   Security  │  │   Management│  │   Validation│  │   Encoding  │        │ │
│  │  │             │  │             │  │             │  │             │        │ │
│  │  │ • Rate      │  │ • JWT       │  │ • Schema    │  │ • HTML      │        │ │
│  │  │   Limiting  │  │   Tokens    │  │   Validation│  │   Encoding  │        │ │
│  │  │ • API       │  │ • Session   │  │ • SQL       │  │ • URL       │        │ │
│  │  │   Keys      │  │   Timeout   │  │   Injection │  │   Encoding  │        │ │
│  │  │ • OAuth 2.0 │  │ • Secure    │  │ • XSS       │  │ • JSON      │        │ │
│  │  │ • OIDC      │  │   Cookies   │  │   Prevention│  │   Sanitization│       │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                             │
│                                    ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              DATABASE SECURITY LAYER                        │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Encryption│  │   Access    │  │   Audit     │  │   Backup    │        │ │
│  │  │             │  │   Control   │  │   Logging   │  │   Security  │        │ │
│  │  │ • At Rest   │  │ • Row-Level │  │ • Data      │  │             │        │ │
│  │  │ • In Transit│  │   Security  │  │   Access    │  │ • Encrypted │        │ │
│  │  │ • Column    │  │ • Column-   │  │ • Schema    │  │   Backups   │        │ │
│  │  │   Level     │  │   Level     │  │   Changes   │  │ • Access    │        │ │
│  │  │ • Key       │  │   Security  │  │ • User      │  │   Control   │        │ │
│  │  │   Management│  │ • Database  │  │   Actions   │  │ • Integrity │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                             │
│                                    ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              INFRASTRUCTURE SECURITY LAYER                 │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Container │  │   Secrets   │  │   Network   │  │   Monitoring│        │ │
│  │  │   Security  │  │   Management│  │   Security  │  │   & Alerting│        │ │
│  │  │             │  │             │  │             │  │             │        │ │
│  │  │ • Image     │  │ • AWS KMS   │  │ • VPC       │  │ • SIEM      │        │ │
│  │  │   Scanning  │  │ • HashiCorp │  │   Isolation │  │ • IDS/IPS   │        │ │
│  │  │ • Runtime   │  │   Vault     │  │ • Security  │  │ • Threat    │        │ │
│  │  │   Protection│  │ • Azure Key │  │   Groups    │  │   Detection │        │ │
│  │  │ • Pod       │  │   Vault     │  │ • Network   │  │ • Security  │        │ │
│  │  │   Security  │  │ • Rotation  │  │   ACLs      │  │   Analytics │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 🔐 Database Security Implementation

### Encryption at Rest

```sql
-- Enable database encryption
ALTER SYSTEM SET ssl = on;
ALTER SYSTEM SET ssl_cert_file = '/etc/ssl/certs/server.crt';
ALTER SYSTEM SET ssl_key_file = '/etc/ssl/private/server.key';

-- Create encrypted tablespace
CREATE TABLESPACE encrypted_tablespace
LOCATION '/var/lib/postgresql/encrypted_data'
WITH (encryption_key_id = 'your-encryption-key-id');

-- Move sensitive tables to encrypted tablespace
ALTER TABLE user_profiles SET TABLESPACE encrypted_tablespace;
ALTER TABLE camera_streams SET TABLESPACE encrypted_tablespace;
ALTER TABLE audit_logs SET TABLESPACE encrypted_tablespace;

-- Column-level encryption for sensitive data
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Encrypt sensitive columns
CREATE OR REPLACE FUNCTION encrypt_sensitive_data(data TEXT, key_id VARCHAR(100))
RETURNS TEXT AS $$
BEGIN
    -- Use AWS KMS or similar for key management
    RETURN encode(encrypt_iv(
        data::bytea, 
        get_encryption_key(key_id)::bytea, 
        '0123456789012345', 
        'aes-cbc'
    ), 'base64');
END;
$$ LANGUAGE plpgsql;

-- Apply encryption to sensitive columns
ALTER TABLE users ADD COLUMN encrypted_email TEXT;
ALTER TABLE users ADD COLUMN encrypted_phone TEXT;

UPDATE users SET 
    encrypted_email = encrypt_sensitive_data(email, 'email-key'),
    encrypted_phone = encrypt_sensitive_data(phone, 'phone-key');
```

### Row-Level Security (RLS)

```sql
-- Enable RLS on all sensitive tables
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE cameras ENABLE ROW LEVEL SECURITY;
ALTER TABLE counting_results ENABLE ROW LEVEL SECURITY;

-- User access policy
CREATE POLICY user_self_access ON users
    FOR ALL
    USING (id = current_setting('app.current_user_id')::integer)
    WITH CHECK (id = current_setting('app.current_user_id')::integer);

-- Admin access policy
CREATE POLICY admin_access ON users
    FOR ALL
    USING (current_setting('app.user_role') = 'admin')
    WITH CHECK (current_setting('app.user_role') = 'admin');

-- Camera access policy
CREATE POLICY camera_access ON cameras
    FOR SELECT
    USING (
        current_setting('app.user_role') = 'admin'
        OR
        camera_id IN (
            SELECT camera_id 
            FROM user_camera_permissions 
            WHERE user_id = current_setting('app.current_user_id')::integer
            AND permissions @> '["read"]'
        )
    );

-- Time-based access policy
CREATE POLICY time_based_access ON counting_results
    FOR SELECT
    USING (
        created_at > NOW() - INTERVAL '24 hours'
        OR
        current_setting('app.user_role') = 'admin'
    );
```

### Column-Level Security

```sql
-- Create security labels
CREATE TABLE security_labels (
    id SERIAL PRIMARY KEY,
    label_name VARCHAR(50) UNIQUE NOT NULL,
    security_level INTEGER NOT NULL,
    description TEXT
);

INSERT INTO security_labels VALUES
(1, 'public', 1, 'Public data'),
(2, 'internal', 2, 'Internal data'),
(3, 'confidential', 3, 'Confidential data'),
(4, 'restricted', 4, 'Restricted data');

-- Add security labels to columns
ALTER TABLE users ADD COLUMN security_label_id INTEGER REFERENCES security_labels(id);
ALTER TABLE cameras ADD COLUMN security_label_id INTEGER REFERENCES security_labels(id);

-- Update security labels
UPDATE users SET security_label_id = 3; -- confidential
UPDATE cameras SET security_label_id = 4; -- restricted

-- Column access control function
CREATE OR REPLACE FUNCTION check_column_access(
    required_level INTEGER,
    user_level INTEGER
)
RETURNS BOOLEAN AS $$
BEGIN
    RETURN user_level >= required_level;
END;
$$ LANGUAGE plpgsql;

-- Secure view with column-level access control
CREATE VIEW secure_user_view AS
SELECT 
    id,
    username,
    CASE 
        WHEN check_column_access(3, current_setting('app.user_security_level')::integer)
        THEN email 
        ELSE '***@***.***' 
    END as email,
    CASE 
        WHEN check_column_access(4, current_setting('app.user_security_level')::integer)
        THEN phone 
        ELSE '***-***-****' 
    END as phone,
    created_at
FROM users;
```

## 🛡️ Access Control Matrix

### Role-Based Access Control (RBAC)

```sql
-- Create roles table
CREATE TABLE security_roles (
    id SERIAL PRIMARY KEY,
    role_name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    security_level INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Define roles
INSERT INTO security_roles VALUES
(1, 'viewer', 'Read-only access to public data', 1),
(2, 'user', 'Standard user access', 2),
(3, 'analyst', 'Analytics and reporting access', 3),
(4, 'admin', 'Administrative access', 4),
(5, 'system_admin', 'System administration access', 5);

-- User roles mapping
CREATE TABLE user_roles (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    role_id INTEGER REFERENCES security_roles(id),
    granted_by INTEGER REFERENCES users(id),
    granted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Permission matrix
CREATE TABLE role_permissions (
    id SERIAL PRIMARY KEY,
    role_id INTEGER REFERENCES security_roles(id),
    resource_type VARCHAR(50) NOT NULL, -- table, view, function
    resource_name VARCHAR(100) NOT NULL,
    permissions JSONB NOT NULL, -- ["read", "write", "delete"]
    conditions JSONB -- additional conditions
);

-- Define permissions
INSERT INTO role_permissions VALUES
(1, 'viewer', 'table', 'public_analytics', '["read"]', '{}'),
(2, 'user', 'table', 'counting_results', '["read"]', '{"user_id": "current_user"}'),
(3, 'analyst', 'table', 'counting_results', '["read", "write"]', '{}'),
(4, 'admin', 'table', 'users', '["read", "write", "delete"]', '{}'),
(5, 'system_admin', 'table', '*', '["read", "write", "delete", "create"]', '{}');
```

### Attribute-Based Access Control (ABAC)

```sql
-- ABAC attributes table
CREATE TABLE access_attributes (
    id SERIAL PRIMARY KEY,
    attribute_name VARCHAR(50) NOT NULL,
    attribute_value TEXT NOT NULL,
    user_id INTEGER REFERENCES users(id),
    resource_id INTEGER,
    resource_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Define attributes
INSERT INTO access_attributes VALUES
(1, 'location', 'US-East-1', 1, NULL, 'user'),
(2, 'department', 'IT', 1, NULL, 'user'),
(3, 'security_clearance', 'secret', 1, NULL, 'user'),
(4, 'time_window', 'business_hours', 1, NULL, 'user');

-- ABAC policy function
CREATE OR REPLACE FUNCTION check_abac_access(
    user_id INTEGER,
    resource_type VARCHAR(50),
    resource_id INTEGER,
    required_attributes JSONB
)
RETURNS BOOLEAN AS $$
DECLARE
    user_attributes JSONB;
    has_access BOOLEAN := TRUE;
    attr_record RECORD;
BEGIN
    -- Get user attributes
    SELECT jsonb_object_agg(attribute_name, attribute_value) INTO user_attributes
    FROM access_attributes 
    WHERE user_id = $1;
    
    -- Check each required attribute
    FOR attr_record IN SELECT * FROM jsonb_each(required_attributes)
    LOOP
        IF NOT (user_attributes ? attr_record.key 
                AND user_attributes->>attr_record.key = attr_record.value::text) THEN
            has_access := FALSE;
            EXIT;
        END IF;
    END LOOP;
    
    RETURN has_access;
END;
$$ LANGUAGE plpgsql;
```

## 🔍 Security Monitoring & Detection

### Database Activity Monitoring

```sql
-- Enhanced audit logging
CREATE TABLE security_audit_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    session_id VARCHAR(100),
    action VARCHAR(100) NOT NULL,
    resource_type VARCHAR(50),
    resource_name VARCHAR(100),
    old_values JSONB,
    new_values JSONB,
    ip_address INET,
    user_agent TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    risk_score INTEGER DEFAULT 0,
    threat_indicators JSONB,
    is_suspicious BOOLEAN DEFAULT FALSE
);

-- Create indexes for efficient querying
CREATE INDEX idx_security_audit_user_id ON security_audit_logs(user_id);
CREATE INDEX idx_security_audit_action ON security_audit_logs(action);
CREATE INDEX idx_security_audit_timestamp ON security_audit_logs(timestamp);
CREATE INDEX idx_security_audit_risk_score ON security_audit_logs(risk_score);

-- Function to log security events
CREATE OR REPLACE FUNCTION log_security_event(
    p_user_id INTEGER,
    p_action VARCHAR(100),
    p_resource_type VARCHAR(50),
    p_resource_name VARCHAR(100),
    p_risk_score INTEGER DEFAULT 0
)
RETURNS VOID AS $$
BEGIN
    INSERT INTO security_audit_logs (
        user_id, 
        action, 
        resource_type, 
        resource_name,
        ip_address,
        user_agent,
        risk_score,
        timestamp
    ) VALUES (
        p_user_id,
        p_action,
        p_resource_type,
        p_resource_name,
        inet_client_addr(),
        current_setting('application_name'),
        p_risk_score,
        CURRENT_TIMESTAMP
    );
    
    -- Check for suspicious activity
    IF p_risk_score > 7 THEN
        UPDATE security_audit_logs 
        SET is_suspicious = TRUE 
        WHERE id = currval('security_audit_logs_id_seq');
        
        -- Trigger alert
        PERFORM pg_notify('security_alert', json_build_object(
            'user_id', p_user_id,
            'action', p_action,
            'risk_score', p_risk_score,
            'timestamp', CURRENT_TIMESTAMP
        )::text);
    END IF;
END;
$$ LANGUAGE plpgsql;
```

### Threat Detection Rules

```sql
-- Threat detection function
CREATE OR REPLACE FUNCTION detect_threats()
RETURNS TABLE(threat_type VARCHAR(100), description TEXT, severity VARCHAR(20)) AS $$
BEGIN
    -- Detect brute force attacks
    RETURN QUERY
    SELECT 
        'Brute Force Attack'::VARCHAR(100),
        'Multiple failed login attempts detected'::TEXT,
        'HIGH'::VARCHAR(20)
    WHERE EXISTS (
        SELECT 1 FROM security_audit_logs 
        WHERE action = 'LOGIN_FAILED' 
        AND timestamp > NOW() - INTERVAL '5 minutes'
        GROUP BY user_id 
        HAVING COUNT(*) > 5
    );
    
    -- Detect data exfiltration
    RETURN QUERY
    SELECT 
        'Data Exfiltration'::VARCHAR(100),
        'Large data export detected'::TEXT,
        'CRITICAL'::VARCHAR(20)
    WHERE EXISTS (
        SELECT 1 FROM security_audit_logs 
        WHERE action = 'DATA_EXPORT' 
        AND timestamp > NOW() - INTERVAL '1 hour'
        GROUP BY user_id 
        HAVING COUNT(*) > 10
    );
    
    -- Detect privilege escalation
    RETURN QUERY
    SELECT 
        'Privilege Escalation'::VARCHAR(100),
        'Unauthorized privilege change detected'::TEXT,
        'CRITICAL'::VARCHAR(20)
    WHERE EXISTS (
        SELECT 1 FROM security_audit_logs 
        WHERE action = 'ROLE_CHANGE' 
        AND timestamp > NOW() - INTERVAL '1 hour'
        AND new_values->>'role' IN ('admin', 'system_admin')
    );
    
    -- Detect unusual access patterns
    RETURN QUERY
    SELECT 
        'Unusual Access Pattern'::VARCHAR(100),
        'Access outside normal hours detected'::TEXT,
        'MEDIUM'::VARCHAR(20)
    WHERE EXISTS (
        SELECT 1 FROM security_audit_logs 
        WHERE timestamp > NOW() - INTERVAL '1 hour'
        AND EXTRACT(HOUR FROM timestamp) NOT BETWEEN 8 AND 18
        AND action IN ('DATA_ACCESS', 'DATA_MODIFY')
    );
END;
$$ LANGUAGE plpgsql;
```

## 🚨 Incident Response

### Security Incident Management

```sql
-- Security incidents table
CREATE TABLE security_incidents (
    id SERIAL PRIMARY KEY,
    incident_type VARCHAR(100) NOT NULL,
    severity VARCHAR(20) NOT NULL, -- low, medium, high, critical
    description TEXT NOT NULL,
    affected_users INTEGER[],
    affected_resources TEXT[],
    detection_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    response_time TIMESTAMP,
    resolution_time TIMESTAMP,
    status VARCHAR(20) DEFAULT 'open', -- open, investigating, resolved, closed
    assigned_to INTEGER REFERENCES users(id),
    mitigation_steps JSONB,
    lessons_learned TEXT
);

-- Incident response workflow
CREATE OR REPLACE FUNCTION handle_security_incident(
    p_incident_type VARCHAR(100),
    p_severity VARCHAR(20),
    p_description TEXT,
    p_affected_users INTEGER[] DEFAULT NULL
)
RETURNS INTEGER AS $$
DECLARE
    incident_id INTEGER;
BEGIN
    -- Create incident record
    INSERT INTO security_incidents (
        incident_type, 
        severity, 
        description, 
        affected_users
    ) VALUES (
        p_incident_type,
        p_severity,
        p_description,
        p_affected_users
    ) RETURNING id INTO incident_id;
    
    -- Apply immediate mitigation based on severity
    CASE p_severity
        WHEN 'critical' THEN
            -- Block affected users
            UPDATE users SET is_active = FALSE 
            WHERE id = ANY(p_affected_users);
            
            -- Log incident
            PERFORM log_security_event(
                NULL, 
                'INCIDENT_CREATED', 
                'security_incident', 
                incident_id::text, 
                10
            );
            
        WHEN 'high' THEN
            -- Increase monitoring
            UPDATE users SET security_level = security_level + 1 
            WHERE id = ANY(p_affected_users);
            
        WHEN 'medium' THEN
            -- Log for investigation
            PERFORM log_security_event(
                NULL, 
                'INCIDENT_CREATED', 
                'security_incident', 
                incident_id::text, 
                5
            );
            
        ELSE
            -- Just log the incident
            PERFORM log_security_event(
                NULL, 
                'INCIDENT_CREATED', 
                'security_incident', 
                incident_id::text, 
                1
            );
    END CASE;
    
    RETURN incident_id;
END;
$$ LANGUAGE plpgsql;
```

## 🔧 Implementation Guidelines

### Security Configuration

#### PostgreSQL Security Settings
```sql
-- Security configuration
ALTER SYSTEM SET ssl = on;
ALTER SYSTEM SET ssl_cert_file = '/etc/ssl/certs/server.crt';
ALTER SYSTEM SET ssl_key_file = '/etc/ssl/private/server.key';
ALTER SYSTEM SET ssl_ca_file = '/etc/ssl/certs/ca.crt';

-- Connection security
ALTER SYSTEM SET max_connections = 100;
ALTER SYSTEM SET shared_preload_libraries = 'pg_stat_statements,pgcrypto';
ALTER SYSTEM SET log_connections = on;
ALTER SYSTEM SET log_disconnections = on;
ALTER SYSTEM SET log_statement = 'all';
ALTER SYSTEM SET log_min_duration_statement = 1000;

-- Password security
ALTER SYSTEM SET password_encryption = 'scram-sha-256';
ALTER SYSTEM SET password_min_length = 12;
ALTER SYSTEM SET password_require_uppercase = on;
ALTER SYSTEM SET password_require_lowercase = on;
ALTER SYSTEM SET password_require_digits = on;
ALTER SYSTEM SET password_require_special = on;

-- Session security
ALTER SYSTEM SET session_timeout = '15min';
ALTER SYSTEM SET idle_in_transaction_session_timeout = '10min';
```

#### Network Security
```bash
# PostgreSQL network security
# pg_hba.conf configuration
# TYPE  DATABASE        USER            ADDRESS                 METHOD
local   all             postgres                                peer
host    all             all             127.0.0.1/32            md5
host    all             all             ::1/128                 md5
host    all             all             10.0.0.0/8              md5
host    all             all             172.16.0.0/12           md5
host    all             all             192.168.0.0/16          md5
host    all             all             0.0.0.0/0               reject
```

### Security Monitoring Script

```python
# Security monitoring script
import psycopg2
import json
from datetime import datetime, timedelta

class SecurityMonitor:
    def __init__(self, db_connection):
        self.conn = db_connection
        self.cursor = self.conn.cursor()
    
    def check_failed_logins(self):
        """Check for brute force attacks"""
        self.cursor.execute("""
            SELECT user_id, COUNT(*) as failed_attempts
            FROM security_audit_logs 
            WHERE action = 'LOGIN_FAILED' 
            AND timestamp > NOW() - INTERVAL '5 minutes'
            GROUP BY user_id 
            HAVING COUNT(*) > 5
        """)
        
        return self.cursor.fetchall()
    
    def check_data_access_patterns(self):
        """Check for unusual data access patterns"""
        self.cursor.execute("""
            SELECT user_id, COUNT(*) as access_count
            FROM security_audit_logs 
            WHERE action IN ('DATA_ACCESS', 'DATA_EXPORT')
            AND timestamp > NOW() - INTERVAL '1 hour'
            GROUP BY user_id 
            HAVING COUNT(*) > 100
        """)
        
        return self.cursor.fetchall()
    
    def check_privilege_changes(self):
        """Check for unauthorized privilege changes"""
        self.cursor.execute("""
            SELECT user_id, action, new_values
            FROM security_audit_logs 
            WHERE action = 'ROLE_CHANGE'
            AND timestamp > NOW() - INTERVAL '1 hour'
            AND new_values->>'role' IN ('admin', 'system_admin')
        """)
        
        return self.cursor.fetchall()
    
    def generate_security_report(self):
        """Generate comprehensive security report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'failed_logins': self.check_failed_logins(),
            'unusual_access': self.check_data_access_patterns(),
            'privilege_changes': self.check_privilege_changes(),
            'active_threats': self.detect_threats()
        }
        
        return report
    
    def detect_threats(self):
        """Detect active threats"""
        self.cursor.execute("SELECT * FROM detect_threats()")
        return self.cursor.fetchall()

# Usage
monitor = SecurityMonitor(db_connection)
report = monitor.generate_security_report()
print(json.dumps(report, indent=2))
```

## 📊 Security Metrics & KPIs

### Security Performance Indicators

| Metric | Target | Measurement | Alert Threshold |
|--------|--------|-------------|-----------------|
| **Failed Login Attempts** | < 5/hour | Count per hour | > 10/hour |
| **Data Access Violations** | 0 | Count per day | > 0 |
| **Privilege Escalation** | 0 | Count per day | > 0 |
| **Security Incidents** | < 1/month | Count per month | > 2/month |
| **Mean Time to Detection** | < 5 minutes | Average time | > 15 minutes |
| **Mean Time to Resolution** | < 2 hours | Average time | > 8 hours |

### Security Dashboard Queries

```sql
-- Security metrics dashboard
SELECT 
    'Failed Logins' as metric,
    COUNT(*) as value,
    'per hour' as unit
FROM security_audit_logs 
WHERE action = 'LOGIN_FAILED' 
AND timestamp > NOW() - INTERVAL '1 hour'

UNION ALL

SELECT 
    'Data Access Violations' as metric,
    COUNT(*) as value,
    'per day' as unit
FROM security_audit_logs 
WHERE action = 'ACCESS_VIOLATION' 
AND timestamp > NOW() - INTERVAL '1 day'

UNION ALL

SELECT 
    'Active Incidents' as metric,
    COUNT(*) as value,
    'total' as unit
FROM security_incidents 
WHERE status IN ('open', 'investigating')

UNION ALL

SELECT 
    'High Risk Users' as metric,
    COUNT(*) as value,
    'total' as unit
FROM users 
WHERE security_level > 3;
```

---

**Tài liệu này cung cấp framework hoàn chỉnh cho Advanced Security Implementation trong môi trường production, đảm bảo bảo vệ dữ liệu và hệ thống khỏi các mối đe dọa bảo mật.** 