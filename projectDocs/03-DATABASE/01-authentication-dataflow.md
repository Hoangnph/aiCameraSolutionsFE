# Authentication Data Flow - AI Camera Counting System

## 📊 Tổng quan

Authentication Data Flow là luồng dữ liệu cốt lõi xử lý xác thực và quản lý phiên làm việc trong hệ thống AI Camera Counting. Luồng này đảm bảo bảo mật, kiểm soát truy cập và quản lý phiên làm việc cho tất cả người dùng.

## 🏗️ Kiến trúc Authentication Flow

### High-Level Authentication Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              AUTHENTICATION FLOW ARCHITECTURE                   │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              CLIENT LAYER                                   │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Web       │  │   Mobile    │  │   Desktop   │  │   External  │        │ │
│  │  │   Dashboard │  │   App       │  │   Client    │  │   API       │        │ │
│  │  │   (React)   │  │   (React)   │  │   (Electron)│  │   Client    │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                             │
│                                    ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              API GATEWAY LAYER                              │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Rate      │  │   Load      │  │   Auth      │  │   Request   │        │ │
│  │  │   Limiting  │  │   Balancer  │  │   Gateway   │  │   Routing   │        │ │
│  │  │   (Redis)   │  │   (NGINX)   │  │   (JWT)     │  │   (Proxy)   │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                             │
│                                    ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              AUTHENTICATION SERVICE                         │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   beAuth    │  │   Session   │  │   Token     │  │   Audit     │        │ │
│  │  │   Service   │  │   Manager   │  │   Manager   │  │   Logger    │        │ │
│  │  │   (Node.js) │  │   (Redis)   │  │   (JWT)     │  │   (Winston) │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                             │
│                                    ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              DATA LAYER                                     │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   User      │  │   Session   │  │   Audit     │  │   Cache     │        │ │
│  │  │   Database  │  │   Database  │  │   Database  │  │   (Redis)   │        │ │
│  │  │   (PostgreSQL)│ │   (PostgreSQL)│ │   (PostgreSQL)│ │             │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Authentication Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              AUTHENTICATION FLOW DIAGRAM                        │
│                                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐      │
│  │   Client    │    │   API       │    │   beAuth    │    │   Database  │      │
│  │   (Frontend)│    │   Gateway   │    │   Service   │    │   (PostgreSQL)│     │
│  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘      │
│         │                   │                   │                   │          │
│         │ 1. Login Request  │                   │                   │          │
│         │ (username/password)│                   │                   │          │
│         │──────────────────►│                   │                   │          │
│         │                   │                   │                   │          │
│         │                   │ 2. Forward Request│                   │          │
│         │                   │ (Rate Limiting)   │                   │          │
│         │                   │──────────────────►│                   │          │
│         │                   │                   │                   │          │
│         │                   │                   │ 3. Validate User  │          │
│         │                   │                   │ (Check Database)  │          │
│         │                   │                   │──────────────────►│          │
│         │                   │                   │                   │          │
│         │                   │                   │ 4. User Data      │          │
│         │                   │                   │ (User Info)       │          │
│         │                   │                   │◄──────────────────┤          │
│         │                   │                   │                   │          │
│         │                   │                   │ 5. Generate Tokens│          │
│         │                   │                   │ (JWT Access/Refresh)│        │
│         │                   │                   │                   │          │
│         │                   │                   │ 6. Store Session  │          │
│         │                   │                   │ (Redis Cache)     │          │
│         │                   │                   │                   │          │
│         │                   │                   │ 7. Audit Log      │          │
│         │                   │                   │ (Login Event)     │          │
│         │                   │                   │                   │          │
│         │                   │ 8. Return Tokens  │                   │          │
│         │                   │ (JWT + User Info) │                   │          │
│         │                   │◄──────────────────┤                   │          │
│         │                   │                   │                   │          │
│         │ 9. Access Token   │                   │                   │          │
│         │ (Store in Memory) │                   │                   │          │
│         │◄──────────────────┤                   │                   │          │
│         │                   │                   │                   │          │
│         │ 10. API Requests  │                   │                   │          │
│         │ (with JWT)        │                   │                   │          │
│         │──────────────────►│                   │                   │          │
│         │                   │                   │                   │          │
│         │                   │ 11. Validate Token│                   │          │
│         │                   │ (JWT Verification)│                   │          │
│         │                   │──────────────────►│                   │          │
│         │                   │                   │                   │          │
│         │                   │                   │ 12. Check Session │          │
│         │                   │                   │ (Redis Cache)     │          │
│         │                   │                   │──────────────────►│          │
│         │                   │                   │                   │          │
│         │                   │                   │ 13. Session Valid │          │
│         │                   │                   │ (User Active)     │          │
│         │                   │                   │◄──────────────────┤          │
│         │                   │                   │                   │          │
│         │                   │ 14. Forward Request│                   │          │
│         │                   │ (to Backend)      │                   │          │
│         │                   │◄──────────────────┤                   │          │
│         │                   │                   │                   │          │
│         │ 15. API Response  │                   │                   │          │
│         │ (Data/Error)      │                   │                   │          │
│         │◄──────────────────┤                   │                   │          │
│         │                   │                   │                   │          │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 🔧 Cấu hình Authentication

### JWT Configuration
```javascript
// JWT Configuration
const jwtConfig = {
  accessToken: {
    secret: process.env.JWT_ACCESS_SECRET,
    expiresIn: '15m',
    algorithm: 'HS256'
  },
  refreshToken: {
    secret: process.env.JWT_REFRESH_SECRET,
    expiresIn: '7d',
    algorithm: 'HS256'
  }
};
```

### Session Configuration
```javascript
// Session Configuration
const sessionConfig = {
  store: redisStore,
  secret: process.env.SESSION_SECRET,
  resave: false,
  saveUninitialized: false,
  cookie: {
    secure: process.env.NODE_ENV === 'production',
    httpOnly: true,
    maxAge: 7 * 24 * 60 * 60 * 1000 // 7 days
  }
};
```

### Rate Limiting Configuration
```javascript
// Rate Limiting Configuration
const rateLimitConfig = {
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
  message: 'Too many requests from this IP',
  standardHeaders: true,
  legacyHeaders: false
};
```

## 🔗 API Endpoints

### Authentication Endpoints
| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| POST | `/api/v1/auth/login` | User login | Public |
| POST | `/api/v1/auth/logout` | User logout | Private |
| POST | `/api/v1/auth/refresh` | Refresh token | Public |
| POST | `/api/v1/auth/forgot-password` | Forgot password | Public |
| POST | `/api/v1/auth/reset-password` | Reset password | Public |
| GET | `/api/v1/auth/me` | Get current user | Private |

### User Management Endpoints
| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/api/v1/users/profile` | Get user profile | Private |
| PUT | `/api/v1/users/profile` | Update user profile | Private |
| PUT | `/api/v1/users/change-password` | Change password | Private |

## 📊 Performance Optimization

### Caching Strategy
- **Session Cache**: Redis với TTL 7 ngày
- **User Profile Cache**: Redis với TTL 1 giờ
- **Rate Limiting Cache**: Redis với TTL 15 phút

### Database Optimization
- **Connection Pooling**: 20 connections
- **Query Optimization**: Indexes trên username, email
- **Read Replicas**: Cho user profile queries

### Security Optimization
- **Password Hashing**: bcrypt với 12 rounds
- **Token Rotation**: Refresh token rotation
- **Session Invalidation**: Automatic cleanup

## 🛡️ Security Implementation

### Authentication Security
```javascript
// Password Validation
const passwordValidation = {
  minLength: 8,
  requireUppercase: true,
  requireLowercase: true,
  requireNumbers: true,
  requireSpecialChars: true
};

// JWT Security
const jwtSecurity = {
  algorithm: 'HS256',
  issuer: 'ai-camera-counting',
  audience: 'ai-camera-counting-users',
  clockTolerance: 30
};
```

### Session Security
```javascript
// Session Security
const sessionSecurity = {
  secure: process.env.NODE_ENV === 'production',
  httpOnly: true,
  sameSite: 'strict',
  maxAge: 7 * 24 * 60 * 60 * 1000
};
```

## 📈 Monitoring & Alerting

### Authentication Metrics
- **Login Success Rate**: ≥ 99%
- **Login Latency**: < 300ms
- **Token Refresh Rate**: < 5%
- **Session Invalidation Rate**: < 1%

### Security Monitoring
- **Failed Login Attempts**: Alert if > 5 per minute
- **Suspicious IP Activity**: Alert if > 10 requests per minute
- **Token Tampering**: Immediate alert
- **Session Hijacking**: Alert on multiple sessions

### Performance Monitoring
- **Database Connection Pool**: Monitor usage
- **Redis Cache Hit Rate**: ≥ 95%
- **API Response Time**: < 500ms
- **Error Rate**: < 0.1%

## ⚠️ Error Handling

### Authentication Errors
```javascript
// Error Handling
const authErrors = {
  INVALID_CREDENTIALS: {
    code: 'AUTH_001',
    message: 'Invalid username or password',
    status: 401
  },
  TOKEN_EXPIRED: {
    code: 'AUTH_002',
    message: 'Access token has expired',
    status: 401
  },
  INVALID_TOKEN: {
    code: 'AUTH_003',
    message: 'Invalid or malformed token',
    status: 401
  },
  RATE_LIMIT_EXCEEDED: {
    code: 'AUTH_004',
    message: 'Too many requests',
    status: 429
  }
};
```

### Recovery Procedures
- **Token Refresh**: Automatic refresh before expiry
- **Session Recovery**: Graceful session restoration
- **Rate Limit Recovery**: Exponential backoff
- **Database Recovery**: Connection retry logic

## ✅ Success Criteria

### Technical Success
- **Performance**: Login response time < 300ms
- **Reliability**: 99.9% uptime
- **Security**: Zero authentication vulnerabilities
- **Scalability**: Support 1000+ concurrent users

### Business Success
- **User Experience**: Seamless authentication flow
- **Security**: Zero unauthorized access
- **Compliance**: GDPR/CCPA compliant
- **Cost Efficiency**: Optimized resource usage

---

## 🔗 Traceability & Compliance

### Related Documents
- **Theory**: `01-02-data-flow-comprehensive-theory.md`
- **Security**: `01-03-security-architecture.md`
- **API Spec**: `beAuth/docs/api-reference.md`
- **Database**: `beAuth/docs/database-schema.md`

### Business Metrics
- **Latency**: < 300ms
- **Uptime**: ≥ 99.9%
- **Security Incidents**: 0
- **User Satisfaction**: ≥ 95%

### Compliance Checklist
- [x] GDPR compliance (data retention, user consent)
- [x] CCPA compliance (data access, deletion)
- [x] Audit logging (all authentication events)
- [x] Role-based access control (RBAC)
- [x] Session management (secure, timeout)

### Data Lineage
- User Input → Validation → Authentication → Session Creation → Token Generation → API Access
- All steps logged, audited, and monitored

### User/Role Matrix
| Role | Permissions | Data Access |
|------|-------------|-------------|
| User | Login, Profile Management | Own data only |
| Admin | User Management, System Config | All user data |
| Auditor | Read-only access | Audit logs, user activity |

### Incident Response Checklist
- [x] Real-time alerting for failed logins
- [x] Automatic session invalidation on suspicious activity
- [x] Rate limiting and IP blocking
- [x] Audit trail for all authentication events
- [x] Rollback procedures for security incidents
