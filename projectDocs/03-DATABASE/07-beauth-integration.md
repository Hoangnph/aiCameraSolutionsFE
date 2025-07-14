# beAuth Integration Guide - AI Camera Counting System

## 📊 Tổng quan

Tài liệu này cung cấp hướng dẫn chi tiết về tích hợp database beCamera với hệ thống beAuth, bao gồm user synchronization, session management, permission handling, và audit logging.

## 🎯 Mục tiêu tích hợp

- **User Synchronization**: Đồng bộ user data giữa beAuth và beCamera
- **Session Management**: Quản lý session thống nhất
- **Permission Control**: Kiểm soát quyền truy cập camera và data
- **Audit Trail**: Ghi nhận đầy đủ các hoạt động user
- **Security**: Đảm bảo bảo mật thông tin user

## 🏗️ Integration Architecture

### beAuth Integration Overview

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              BEAUTH INTEGRATION OVERVIEW                        │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              BEAUTH SYSTEM                                  │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   User      │  │   Session   │  │   Permission│  │   Audit     │        │ │
│  │  │   Management│  │   Management│  │   Management│  │   Logging   │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                             │
│                                    │ API Calls                                   │
│                                    │ (REST/GraphQL)                              │
│                                    ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              BECAMERA SYSTEM                                │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   User      │  │   Session   │  │   Camera    │  │   Audit     │        │ │
│  │  │   Sync      │  │   Cache     │  │   Permission│  │   Sync      │        │ │
│  │  │   Service   │  │   Service   │  │   Service   │  │   Service   │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                             │
│                                    ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              BECAMERA DATABASE                              │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Users     │  │   Sessions  │  │   Permissions│  │   Audit     │        │ │
│  │  │   Table     │  │   Table     │  │   Table     │  │   Logs      │        │ │
│  │  │             │  │             │  │             │  │             │        │ │
│  │  │ • Synced    │  │ • Local     │  │ • Camera    │  │ • User      │        │ │
│  │  │   from      │  │   cache     │  │   access    │  │   actions   │        │ │
│  │  │   beAuth    │  │ • Token     │  │ • Zone      │  │ • Data      │        │ │
│  │  │ • Read-only │  │   validation│  │   access    │  │   access    │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Data Synchronization Flow

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              DATA SYNCHRONIZATION FLOW                          │
│                                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐      │
│  │   beAuth    │    │   Sync      │    │   beCamera  │    │   Cache     │      │
│  │   Database  │    │   Service   │    │   Database  │    │   (Redis)   │      │
│  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘      │
│         │                   │                   │                   │          │
│         │ 1. User Created   │                   │                   │          │
│         │ (beAuth)          │                   │                   │          │
│         │──────────────────►│                   │                   │          │
│         │                   │                   │                   │          │
│         │                   │ 2. Sync User      │                   │          │
│         │                   │ Data              │                   │          │
│         │                   │──────────────────►│                   │          │
│         │                   │                   │                   │          │
│         │                   │                   │ 3. Store User     │          │
│         │                   │                   │ (beCamera DB)     │          │
│         │                   │                   │──────────────────►│          │
│         │                   │                   │                   │          │
│         │                   │                   │ 4. Update Cache   │          │
│         │                   │                   │ (User Session)    │          │
│         │                   │                   │──────────────────►│          │
│         │                   │                   │                   │          │
│         │                   │ 5. Confirm Sync   │                   │          │
│         │                   │ Success           │                   │          │
│         │                   │◄──────────────────┤                   │          │
│         │                   │                   │                   │          │
│         │ 6. Log Sync       │                   │                   │          │
│         │ Event             │                   │                   │          │
│         │◄──────────────────┤                   │                   │          │
│         │                   │                   │                   │          │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 📋 User Synchronization

### 1. User Data Structure

**Mục đích**: Đồng bộ user data từ beAuth sang beCamera với read-only access.

```sql
-- User table structure (synced from beAuth)
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
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Sync metadata
    sync_id UUID DEFAULT gen_random_uuid(),
    last_sync_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sync_status sync_status DEFAULT 'synced'
);

-- Sync status enum
DO $$ BEGIN
    CREATE TYPE sync_status AS ENUM ('pending', 'synced', 'failed', 'out_of_sync');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;
```

### 2. User Synchronization Service

```sql
-- User synchronization function
CREATE OR REPLACE FUNCTION sync_user_from_beauth(user_data JSONB)
RETURNS BOOLEAN AS $$
DECLARE
    user_id INTEGER;
    sync_success BOOLEAN;
BEGIN
    BEGIN
        -- Extract user data
        user_id := (user_data->>'id')::INTEGER;
        
        -- Insert or update user
        INSERT INTO users (
            id, username, email, password_hash, first_name, last_name,
            role, is_active, last_login, email_verified, created_at, updated_at,
            sync_id, last_sync_at, sync_status
        ) VALUES (
            user_id,
            user_data->>'username',
            user_data->>'email',
            user_data->>'password_hash',
            user_data->>'first_name',
            user_data->>'last_name',
            (user_data->>'role')::user_role,
            (user_data->>'is_active')::BOOLEAN,
            (user_data->>'last_login')::TIMESTAMP,
            (user_data->>'email_verified')::BOOLEAN,
            (user_data->>'created_at')::TIMESTAMP,
            (user_data->>'updated_at')::TIMESTAMP,
            gen_random_uuid(),
            NOW(),
            'synced'
        )
        ON CONFLICT (id) DO UPDATE SET
            username = EXCLUDED.username,
            email = EXCLUDED.email,
            password_hash = EXCLUDED.password_hash,
            first_name = EXCLUDED.first_name,
            last_name = EXCLUDED.last_name,
            role = EXCLUDED.role,
            is_active = EXCLUDED.is_active,
            last_login = EXCLUDED.last_login,
            email_verified = EXCLUDED.email_verified,
            updated_at = EXCLUDED.updated_at,
            last_sync_at = NOW(),
            sync_status = 'synced';
        
        sync_success := TRUE;
        
    EXCEPTION WHEN OTHERS THEN
        sync_success := FALSE;
        
        -- Log sync failure
        INSERT INTO sync_error_log (
            sync_type,
            user_id,
            error_message,
            sync_data,
            created_at
        ) VALUES (
            'user_sync',
            user_id,
            SQLERRM,
            user_data,
            NOW()
        );
    END;
    
    -- Log sync event
    INSERT INTO sync_log (
        sync_type,
        user_id,
        success,
        created_at
    ) VALUES (
        'user_sync',
        user_id,
        sync_success,
        NOW()
    );
    
    RETURN sync_success;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
```

### 3. Batch User Synchronization

```sql
-- Batch user synchronization function
CREATE OR REPLACE FUNCTION sync_users_batch(users_data JSONB[])
RETURNS TABLE(user_id INTEGER, sync_status TEXT, error_message TEXT) AS $$
DECLARE
    user_data JSONB;
    sync_result BOOLEAN;
    user_id_val INTEGER;
BEGIN
    FOREACH user_data IN ARRAY users_data
    LOOP
        user_id_val := (user_data->>'id')::INTEGER;
        
        SELECT sync_user_from_beauth(user_data) INTO sync_result;
        
        RETURN QUERY
        SELECT 
            user_id_val,
            CASE WHEN sync_result THEN 'success' ELSE 'failed' END::TEXT,
            CASE WHEN NOT sync_result THEN 'Sync failed' ELSE NULL END::TEXT;
    END LOOP;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
```

## 🔐 Session Management

### 1. Session Data Structure

**Mục đích**: Quản lý session local với validation từ beAuth.

```sql
-- Session table structure
CREATE TABLE IF NOT EXISTS user_sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    session_token VARCHAR(255) UNIQUE NOT NULL,
    refresh_token VARCHAR(255) UNIQUE NOT NULL,
    ip_address INET,
    user_agent TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Session metadata
    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    login_method VARCHAR(50) DEFAULT 'password',
    device_info JSONB DEFAULT '{}'
);

-- Session validation function
CREATE OR REPLACE FUNCTION validate_session(session_token_param VARCHAR(255))
RETURNS TABLE(user_id INTEGER, username VARCHAR(50), role user_role, is_valid BOOLEAN) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        us.user_id,
        u.username,
        u.role,
        (us.is_active AND us.expires_at > NOW())::BOOLEAN as is_valid
    FROM user_sessions us
    JOIN users u ON us.user_id = u.id
    WHERE us.session_token = session_token_param
    AND us.is_active = TRUE
    AND us.expires_at > NOW();
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
```

### 2. Session Cache Integration

```sql
-- Session cache management
CREATE OR REPLACE FUNCTION update_session_cache(session_token_param VARCHAR(255))
RETURNS void AS $$
DECLARE
    session_data JSONB;
BEGIN
    -- Get session data
    SELECT jsonb_build_object(
        'user_id', us.user_id,
        'username', u.username,
        'role', u.role,
        'permissions', get_user_permissions(us.user_id),
        'expires_at', us.expires_at,
        'last_activity', us.last_activity
    ) INTO session_data
    FROM user_sessions us
    JOIN users u ON us.user_id = u.id
    WHERE us.session_token = session_token_param
    AND us.is_active = TRUE;
    
    -- Update Redis cache (via application layer)
    -- This would be handled by the application service
    PERFORM set_session_cache(session_token_param, session_data);
    
    -- Update last activity
    UPDATE user_sessions
    SET last_activity = NOW()
    WHERE session_token = session_token_param;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
```

## 🔒 Permission Management

### 1. Camera Permission Structure

**Mục đích**: Quản lý quyền truy cập camera và data cho từng user.

```sql
-- Camera permissions table
CREATE TABLE IF NOT EXISTS camera_permissions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    camera_id INTEGER NOT NULL REFERENCES cameras(id) ON DELETE CASCADE,
    permission_type permission_type NOT NULL,
    granted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    granted_by INTEGER REFERENCES users(id),
    expires_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    
    UNIQUE(user_id, camera_id, permission_type)
);

-- Permission types
DO $$ BEGIN
    CREATE TYPE permission_type AS ENUM ('read', 'write', 'admin', 'view_live', 'view_history', 'export_data');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- Zone permissions table
CREATE TABLE IF NOT EXISTS zone_permissions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    zone_id INTEGER NOT NULL REFERENCES zones(id) ON DELETE CASCADE,
    permission_type permission_type NOT NULL,
    granted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    granted_by INTEGER REFERENCES users(id),
    expires_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    
    UNIQUE(user_id, zone_id, permission_type)
);
```

### 2. Permission Checking Functions

```sql
-- Check camera permission function
CREATE OR REPLACE FUNCTION check_camera_permission(
    user_id_param INTEGER,
    camera_id_param INTEGER,
    permission_type_param permission_type
)
RETURNS BOOLEAN AS $$
DECLARE
    has_permission BOOLEAN;
    user_role_val user_role;
BEGIN
    -- Get user role
    SELECT role INTO user_role_val
    FROM users
    WHERE id = user_id_param;
    
    -- Admin has all permissions
    IF user_role_val = 'admin' THEN
        RETURN TRUE;
    END IF;
    
    -- Check specific permission
    SELECT EXISTS(
        SELECT 1 FROM camera_permissions
        WHERE user_id = user_id_param
        AND camera_id = camera_id_param
        AND permission_type = permission_type_param
        AND is_active = TRUE
        AND (expires_at IS NULL OR expires_at > NOW())
    ) INTO has_permission;
    
    RETURN has_permission;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Check zone permission function
CREATE OR REPLACE FUNCTION check_zone_permission(
    user_id_param INTEGER,
    zone_id_param INTEGER,
    permission_type_param permission_type
)
RETURNS BOOLEAN AS $$
DECLARE
    has_permission BOOLEAN;
    user_role_val user_role;
BEGIN
    -- Get user role
    SELECT role INTO user_role_val
    FROM users
    WHERE id = user_id_param;
    
    -- Admin has all permissions
    IF user_role_val = 'admin' THEN
        RETURN TRUE;
    END IF;
    
    -- Check specific permission
    SELECT EXISTS(
        SELECT 1 FROM zone_permissions
        WHERE user_id = user_id_param
        AND zone_id = zone_id_param
        AND permission_type = permission_type_param
        AND is_active = TRUE
        AND (expires_at IS NULL OR expires_at > NOW())
    ) INTO has_permission;
    
    RETURN has_permission;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
```

### 3. Row-Level Security with beAuth

```sql
-- Enable RLS on sensitive tables
ALTER TABLE counting_results ENABLE ROW LEVEL SECURITY;
ALTER TABLE camera_events ENABLE ROW LEVEL SECURITY;
ALTER TABLE analytics ENABLE ROW LEVEL SECURITY;

-- RLS policies for counting_results
CREATE POLICY counting_results_access_policy ON counting_results
    FOR ALL
    TO authenticated_users
    USING (
        check_camera_permission(
            current_setting('app.current_user_id')::integer,
            camera_id,
            'read'
        )
    );

-- RLS policies for camera_events
CREATE POLICY camera_events_access_policy ON camera_events
    FOR ALL
    TO authenticated_users
    USING (
        check_camera_permission(
            current_setting('app.current_user_id')::integer,
            camera_id,
            'read'
        )
    );

-- RLS policies for analytics
CREATE POLICY analytics_access_policy ON analytics
    FOR ALL
    TO authenticated_users
    USING (
        check_camera_permission(
            current_setting('app.current_user_id')::integer,
            camera_id,
            'read'
        )
    );
```

## 📊 Audit Logging

### 1. User Activity Audit

**Mục đích**: Ghi nhận tất cả hoạt động của user từ beAuth.

```sql
-- User activity audit table
CREATE TABLE IF NOT EXISTS user_activity_audit (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    session_id INTEGER REFERENCES user_sessions(id),
    activity_type activity_type NOT NULL,
    resource_type resource_type,
    resource_id INTEGER,
    action_details JSONB DEFAULT '{}',
    ip_address INET,
    user_agent TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Activity types
DO $$ BEGIN
    CREATE TYPE activity_type AS ENUM (
        'login', 'logout', 'data_access', 'data_modification',
        'permission_grant', 'permission_revoke', 'camera_access',
        'report_generation', 'export_data', 'system_config'
    );
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- Resource types
DO $$ BEGIN
    CREATE TYPE resource_type AS ENUM (
        'camera', 'zone', 'counting_result', 'analytics',
        'user', 'permission', 'system_config'
    );
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;
```

### 2. Audit Logging Functions

```sql
-- Log user activity function
CREATE OR REPLACE FUNCTION log_user_activity(
    user_id_param INTEGER,
    activity_type_param activity_type,
    resource_type_param resource_type DEFAULT NULL,
    resource_id_param INTEGER DEFAULT NULL,
    action_details_param JSONB DEFAULT '{}'
)
RETURNS void AS $$
BEGIN
    INSERT INTO user_activity_audit (
        user_id,
        session_id,
        activity_type,
        resource_type,
        resource_id,
        action_details,
        ip_address,
        user_agent,
        timestamp
    ) VALUES (
        user_id_param,
        current_setting('app.current_session_id', true)::integer,
        activity_type_param,
        resource_type_param,
        resource_id_param,
        action_details_param,
        inet_client_addr(),
        current_setting('app.user_agent', true),
        NOW()
    );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Get user activity summary
CREATE OR REPLACE FUNCTION get_user_activity_summary(
    user_id_param INTEGER,
    days_back INTEGER DEFAULT 30
)
RETURNS TABLE(activity_type activity_type, count BIGINT, last_activity TIMESTAMP) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        uaa.activity_type,
        COUNT(*)::BIGINT,
        MAX(aa.timestamp) as last_activity
    FROM user_activity_audit uaa
    WHERE uaa.user_id = user_id_param
    AND uaa.timestamp >= NOW() - (days_back || ' days')::INTERVAL
    GROUP BY uaa.activity_type
    ORDER BY count DESC;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
```

## 🔄 API Integration

### 1. beAuth API Integration

```javascript
// beAuth API integration configuration
const beAuthIntegrationConfig = {
  baseUrl: process.env.BEAUTH_API_URL || 'http://beauth:3000',
  apiKey: process.env.BEAUTH_API_KEY,
  
  endpoints: {
    user: {
      get: '/api/users/:id',
      list: '/api/users',
      create: '/api/users',
      update: '/api/users/:id',
      delete: '/api/users/:id'
    },
    session: {
      validate: '/api/sessions/validate',
      refresh: '/api/sessions/refresh',
      revoke: '/api/sessions/revoke'
    },
    permission: {
      get: '/api/permissions/user/:userId',
      grant: '/api/permissions/grant',
      revoke: '/api/permissions/revoke'
    }
  },
  
  sync: {
    interval: 300000, // 5 minutes
    batchSize: 100,
    retryAttempts: 3,
    retryDelay: 5000
  }
};

// User synchronization service
class UserSyncService {
  constructor(config) {
    this.config = config;
    this.lastSyncTime = null;
  }
  
  async syncUsers() {
    try {
      const response = await fetch(`${this.config.baseUrl}/api/users/sync`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${this.config.apiKey}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          lastSyncTime: this.lastSyncTime,
          batchSize: this.config.sync.batchSize
        })
      });
      
      if (response.ok) {
        const users = await response.json();
        await this.processUsers(users);
        this.lastSyncTime = new Date().toISOString();
      }
    } catch (error) {
      console.error('User sync failed:', error);
      throw error;
    }
  }
  
  async processUsers(users) {
    for (const user of users) {
      await this.syncUser(user);
    }
  }
  
  async syncUser(userData) {
    // Call database function to sync user
    const result = await db.query(
      'SELECT sync_user_from_beauth($1)',
      [JSON.stringify(userData)]
    );
    return result.rows[0].sync_user_from_beauth;
  }
}
```

### 2. Session Validation Service

```javascript
// Session validation service
class SessionValidationService {
  constructor(config) {
    this.config = config;
  }
  
  async validateSession(sessionToken) {
    try {
      const response = await fetch(`${this.config.baseUrl}/api/sessions/validate`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${this.config.apiKey}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ sessionToken })
      });
      
      if (response.ok) {
        const sessionData = await response.json();
        await this.updateLocalSession(sessionData);
        return sessionData;
      } else {
        await this.invalidateLocalSession(sessionToken);
        return null;
      }
    } catch (error) {
      console.error('Session validation failed:', error);
      return null;
    }
  }
  
  async updateLocalSession(sessionData) {
    // Update local session cache and database
    await db.query(
      'SELECT update_session_cache($1)',
      [sessionData.sessionToken]
    );
  }
  
  async invalidateLocalSession(sessionToken) {
    // Invalidate local session
    await db.query(
      'UPDATE user_sessions SET is_active = false WHERE session_token = $1',
      [sessionToken]
    );
  }
}
```

## 📈 Monitoring & Health Checks

### 1. Integration Health Monitoring

```sql
-- Integration health check function
CREATE OR REPLACE FUNCTION check_beauth_integration_health()
RETURNS TABLE(component TEXT, status TEXT, last_check TIMESTAMP, details JSONB) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        'user_sync'::TEXT as component,
        CASE 
            WHEN MAX(last_sync_at) > NOW() - INTERVAL '10 minutes' THEN 'healthy'
            WHEN MAX(last_sync_at) > NOW() - INTERVAL '1 hour' THEN 'warning'
            ELSE 'critical'
        END::TEXT as status,
        MAX(last_sync_at) as last_check,
        jsonb_build_object(
            'total_users', COUNT(*),
            'synced_users', COUNT(*) FILTER (WHERE sync_status = 'synced'),
            'failed_syncs', COUNT(*) FILTER (WHERE sync_status = 'failed')
        ) as details
    FROM users
    UNION ALL
    SELECT 
        'session_validation'::TEXT,
        CASE 
            WHEN COUNT(*) FILTER (WHERE expires_at > NOW()) > 0 THEN 'healthy'
            ELSE 'warning'
        END::TEXT,
        MAX(last_activity) as last_check,
        jsonb_build_object(
            'active_sessions', COUNT(*) FILTER (WHERE expires_at > NOW()),
            'expired_sessions', COUNT(*) FILTER (WHERE expires_at <= NOW())
        ) as details
    FROM user_sessions;
END;
$$ LANGUAGE plpgsql;
```

### 2. Integration Metrics

```sql
-- Integration metrics function
CREATE OR REPLACE FUNCTION get_integration_metrics()
RETURNS TABLE(metric_name TEXT, metric_value NUMERIC, timestamp TIMESTAMP) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        'user_sync_success_rate'::TEXT,
        (100.0 * COUNT(*) FILTER (WHERE success = true) / COUNT(*))::NUMERIC,
        NOW()
    FROM sync_log
    WHERE sync_type = 'user_sync'
    AND created_at >= NOW() - INTERVAL '24 hours'
    UNION ALL
    SELECT 
        'active_sessions_count'::TEXT,
        COUNT(*)::NUMERIC,
        NOW()
    FROM user_sessions
    WHERE is_active = TRUE
    AND expires_at > NOW()
    UNION ALL
    SELECT 
        'permission_checks_per_hour'::TEXT,
        COUNT(*)::NUMERIC,
        NOW()
    FROM user_activity_audit
    WHERE activity_type = 'data_access'
    AND timestamp >= NOW() - INTERVAL '1 hour';
END;
$$ LANGUAGE plpgsql;
```

---

**Tài liệu này cung cấp hướng dẫn chi tiết về tích hợp database beCamera với hệ thống beAuth, bao gồm user synchronization, session management, permission handling, và audit logging.** 