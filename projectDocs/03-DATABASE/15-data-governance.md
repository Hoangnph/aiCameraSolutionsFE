# Production Data Governance & Compliance - AI Camera Counting System

## 📊 Tổng quan

Tài liệu này trình bày chiến lược Data Governance và Compliance toàn diện cho hệ thống AI Camera Counting trong môi trường production.

## 🎯 Mục tiêu Data Governance

- **GDPR Compliance**: Tuân thủ quy định bảo vệ dữ liệu cá nhân
- **Data Privacy**: Bảo vệ quyền riêng tư của người dùng
- **Data Retention**: Quản lý vòng đời dữ liệu theo quy định
- **Audit Trail**: Theo dõi toàn bộ hoạt động dữ liệu
- **Data Classification**: Phân loại dữ liệu theo mức độ nhạy cảm

## 🏗️ Data Classification

### Data Sensitivity Levels

| Level | Classification | Description | Examples | Protection |
|-------|----------------|-------------|----------|------------|
| **1** | Public | Dữ liệu công khai | Analytics, reports, trends | Basic access control |
| **2** | Internal | Dữ liệu nội bộ | Business metrics, logs | Role-based access |
| **3** | Confidential | Dữ liệu bảo mật | User profiles, sessions | Encryption + RLS |
| **4** | Restricted | Dữ liệu hạn chế | Raw video, AI models | Maximum protection |

### Data Classification Implementation

```sql
-- Add classification columns to tables
ALTER TABLE users ADD COLUMN data_classification VARCHAR(20) DEFAULT 'confidential';
ALTER TABLE cameras ADD COLUMN data_classification VARCHAR(20) DEFAULT 'restricted';
ALTER TABLE counting_results ADD COLUMN data_classification VARCHAR(20) DEFAULT 'internal';

-- Update classifications
UPDATE users SET data_classification = 'confidential';
UPDATE cameras SET data_classification = 'restricted';
UPDATE counting_results SET data_classification = 'internal';
```

## 🔒 Data Protection

### Encryption Strategy

```sql
-- Column-level encryption
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Encrypt sensitive data
CREATE OR REPLACE FUNCTION encrypt_data(data TEXT, key TEXT)
RETURNS TEXT AS $$
BEGIN
    RETURN encode(encrypt_iv(data::bytea, key::bytea, '0123456789012345', 'aes-cbc'), 'base64');
END;
$$ LANGUAGE plpgsql;

-- Apply to sensitive columns
ALTER TABLE user_profiles ADD COLUMN encrypted_data TEXT;
UPDATE user_profiles SET encrypted_data = encrypt_data(profile_data::text, 'secret-key');
```

### Row-Level Security (RLS)

```sql
-- Enable RLS
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;

-- Create access policies
CREATE POLICY user_access_policy ON user_profiles
    FOR ALL
    USING (user_id = current_setting('app.current_user_id')::integer);

CREATE POLICY camera_access_policy ON cameras
    FOR SELECT
    USING (camera_id IN (
        SELECT camera_id FROM user_camera_permissions 
        WHERE user_id = current_setting('app.current_user_id')::integer
    ));
```

## 📊 GDPR Compliance

### Data Subject Rights

#### Right to Access
```sql
-- Export user data
CREATE OR REPLACE FUNCTION export_user_data(user_id INTEGER)
RETURNS JSONB AS $$
DECLARE
    user_data JSONB;
BEGIN
    SELECT jsonb_build_object(
        'user_info', (SELECT row_to_json(u) FROM users u WHERE u.id = user_id),
        'profile_data', (SELECT profile_data FROM user_profiles WHERE user_id = user_id),
        'activity_log', (SELECT jsonb_agg(row_to_json(al)) FROM audit_logs al WHERE al.user_id = user_id)
    ) INTO user_data;
    
    RETURN user_data;
END;
$$ LANGUAGE plpgsql;
```

#### Right to Erasure
```sql
-- Delete user data
CREATE OR REPLACE FUNCTION delete_user_data(user_id INTEGER)
RETURNS BOOLEAN AS $$
BEGIN
    -- Anonymize instead of hard delete
    UPDATE users SET 
        username = 'deleted_user_' || user_id,
        email = 'deleted_' || user_id || '@deleted.com',
        is_active = FALSE,
        deleted_at = CURRENT_TIMESTAMP
    WHERE id = user_id;
    
    -- Log deletion
    INSERT INTO audit_logs (user_id, action, details)
    VALUES (user_id, 'DATA_DELETION', 'GDPR deletion request');
    
    RETURN TRUE;
END;
$$ LANGUAGE plpgsql;
```

### Data Retention Policies

```sql
-- Retention policy table
CREATE TABLE data_retention_policies (
    id SERIAL PRIMARY KEY,
    table_name VARCHAR(100) NOT NULL,
    retention_period INTERVAL NOT NULL,
    retention_type VARCHAR(20) DEFAULT 'delete',
    enabled BOOLEAN DEFAULT TRUE
);

-- Define policies
INSERT INTO data_retention_policies VALUES
(1, 'camera_streams', '30 days', 'delete', true),
(2, 'counting_results', '1 year', 'archive', true),
(3, 'user_sessions', '90 days', 'delete', true),
(4, 'audit_logs', '7 years', 'archive', true);

-- Apply retention
CREATE OR REPLACE FUNCTION apply_retention_policies()
RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER := 0;
BEGIN
    -- Delete expired camera streams
    DELETE FROM camera_streams 
    WHERE created_at < NOW() - INTERVAL '30 days';
    
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    RETURN deleted_count;
END;
$$ LANGUAGE plpgsql;
```

## 📋 Audit & Compliance

### Audit Logging

```sql
-- Enhanced audit log
CREATE TABLE audit_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    action VARCHAR(100) NOT NULL,
    table_name VARCHAR(100),
    record_id INTEGER,
    old_values JSONB,
    new_values JSONB,
    ip_address INET,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Log data access
CREATE OR REPLACE FUNCTION log_data_access(
    p_user_id INTEGER,
    p_action VARCHAR(100),
    p_table_name VARCHAR(100)
)
RETURNS VOID AS $$
BEGIN
    INSERT INTO audit_logs (user_id, action, table_name, ip_address)
    VALUES (p_user_id, p_action, p_table_name, inet_client_addr());
END;
$$ LANGUAGE plpgsql;
```

### Compliance Monitoring

```sql
-- Check GDPR compliance
CREATE OR REPLACE FUNCTION check_gdpr_compliance()
RETURNS TABLE(check_name VARCHAR(100), status VARCHAR(20)) AS $$
BEGIN
    -- Check retention policies
    RETURN QUERY
    SELECT 'Data Retention'::VARCHAR(100),
           CASE WHEN EXISTS (SELECT 1 FROM data_retention_policies WHERE enabled = TRUE) 
                THEN 'COMPLIANT'::VARCHAR(20) 
                ELSE 'NON_COMPLIANT'::VARCHAR(20) END;
    
    -- Check audit logging
    RETURN QUERY
    SELECT 'Audit Logging'::VARCHAR(100),
           CASE WHEN EXISTS (SELECT 1 FROM audit_logs WHERE timestamp > NOW() - INTERVAL '1 day') 
                THEN 'COMPLIANT'::VARCHAR(20) 
                ELSE 'NON_COMPLIANT'::VARCHAR(20) END;
    
    -- Check encryption
    RETURN QUERY
    SELECT 'Data Encryption'::VARCHAR(100),
           CASE WHEN EXISTS (SELECT 1 FROM user_profiles WHERE encrypted_data IS NOT NULL) 
                THEN 'COMPLIANT'::VARCHAR(20) 
                ELSE 'NON_COMPLIANT'::VARCHAR(20) END;
END;
$$ LANGUAGE plpgsql;
```

## 🔧 Implementation Guidelines

### Data Masking

```sql
-- Mask sensitive data
CREATE OR REPLACE FUNCTION mask_email(email TEXT)
RETURNS TEXT AS $$
BEGIN
    IF email IS NULL THEN RETURN NULL; END IF;
    RETURN substring(email, 1, 1) || '***.' || 
           substring(email, position('.' in email) + 1, 1) || '**@' ||
           substring(email, position('@' in email) + 1, 1) || '******.com';
END;
$$ LANGUAGE plpgsql;

-- Create masked view
CREATE VIEW masked_user_profiles AS
SELECT 
    id,
    user_id,
    mask_email(profile_data->>'email') as masked_email,
    substring(profile_data->>'name', 1, 1) || '***' as masked_name,
    created_at
FROM user_profiles;
```

### Privacy Impact Assessment

```sql
-- PIA table
CREATE TABLE privacy_impact_assessments (
    id SERIAL PRIMARY KEY,
    assessment_name VARCHAR(200) NOT NULL,
    data_purpose TEXT NOT NULL,
    risk_level VARCHAR(20),
    mitigation_measures JSONB,
    assessment_date DATE DEFAULT CURRENT_DATE,
    status VARCHAR(20) DEFAULT 'draft'
);

-- Insert PIA
INSERT INTO privacy_impact_assessments VALUES
(1, 'AI Camera Counting System PIA', 
 'Real-time people counting for security and analytics', 
 'medium',
 '["data_minimization", "encryption", "access_controls"]'::jsonb,
 CURRENT_DATE, 'approved');
```

### Automated Compliance Monitoring

```python
# Compliance monitoring script
import psycopg2
from datetime import datetime

class ComplianceMonitor:
    def __init__(self, db_connection):
        self.conn = db_connection
        self.cursor = self.conn.cursor()
    
    def check_retention_violations(self):
        """Check data retention policy violations"""
        self.cursor.execute("""
            SELECT table_name, retention_period 
            FROM data_retention_policies 
            WHERE enabled = TRUE
        """)
        
        violations = []
        for table_name, retention_period in self.cursor.fetchall():
            self.cursor.execute(f"""
                SELECT COUNT(*) FROM {table_name} 
                WHERE created_at < NOW() - %s
            """, (retention_period,))
            
            count = self.cursor.fetchone()[0]
            if count > 0:
                violations.append({
                    'table': table_name,
                    'violation_count': count,
                    'retention_period': retention_period
                })
        
        return violations
    
    def generate_report(self):
        """Generate compliance report"""
        return {
            'timestamp': datetime.now().isoformat(),
            'retention_violations': self.check_retention_violations(),
            'gdpr_status': self.check_gdpr_compliance()
        }

# Usage
monitor = ComplianceMonitor(db_connection)
report = monitor.generate_report()
print(report)
```

## 📊 Data Lifecycle Management

### Lifecycle Stages

1. **Data Creation**: Camera streams, user input, system logs
2. **Data Processing**: AI analysis, aggregation, reporting
3. **Data Storage**: Hot storage, warm storage, cold storage
4. **Data Archival**: Backup, archive, retention
5. **Data Disposal**: Secure deletion, audit trail

### Retention Schedule

| Data Type | Retention Period | Storage Type | Disposal Method |
|-----------|------------------|--------------|-----------------|
| Camera Streams | 30 days | Hot storage | Secure deletion |
| Counting Results | 1 year | Warm storage | Archive |
| User Sessions | 90 days | Hot storage | Secure deletion |
| Audit Logs | 7 years | Cold storage | Archive |
| System Logs | 1 year | Warm storage | Secure deletion |

---

**Tài liệu này cung cấp framework hoàn chỉnh cho Data Governance và Compliance trong môi trường production, đảm bảo tuân thủ GDPR và các quy định bảo mật khác.** 