# Backend Authentication Service Documentation

## Tổng quan

Backend Authentication Service là một microservice Node.js được xây dựng để xử lý xác thực và quản lý người dùng cho hệ thống People Counting Dashboard. Service này sử dụng PostgreSQL làm cơ sở dữ liệu và JWT cho xác thực.

## Kiến trúc hệ thống

### Technology Stack
- **Runtime**: Node.js 16+
- **Framework**: Express.js
- **Database**: PostgreSQL 12+
- **Authentication**: JWT (JSON Web Tokens)
- **Password Hashing**: bcrypt
- **Validation**: Joi
- **Logging**: Winston
- **Container**: Docker & Docker Compose

### Architecture Pattern
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │  Auth Service   │    │   PostgreSQL    │
│   (React)       │◄──►│   (Node.js)     │◄──►│   Database      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │              ┌─────────────────┐              │
         └──────────────►│   Redis Cache   │◄─────────────┘
                        │   (Optional)    │
                        └─────────────────┘
```

## Cấu trúc dự án

```
beAuth/
├── docs/                          # Tài liệu hệ thống
│   ├── README.md                  # Tài liệu tổng quan
│   ├── api-reference.md           # Tham khảo API
│   ├── database-schema.md         # Schema cơ sở dữ liệu
│   ├── deployment-guide.md        # Hướng dẫn triển khai
│   └── security-guide.md          # Hướng dẫn bảo mật
├── src/
│   ├── config/
│   │   └── database.js            # Database configuration
│   ├── middleware/
│   │   ├── auth.js                # Authentication middleware
│   │   ├── errorHandler.js        # Error handling
│   │   └── notFoundHandler.js     # 404 handler
│   ├── routes/
│   │   ├── auth.js                # Authentication routes
│   │   └── user.js                # User management routes
│   ├── utils/
│   │   ├── jwt.js                 # JWT utilities
│   │   ├── validation.js          # Validation schemas
│   │   └── logger.js              # Logging utility
│   ├── database/
│   │   ├── migrate.js             # Database migrations
│   │   └── seed.js                # Seed data
│   └── index.js                   # Main application
├── test/
│   └── api.test.js                # API tests
├── Dockerfile                     # Container configuration
├── docker-compose.yml             # Development environment
├── package.json                   # Dependencies
├── env.example                    # Environment template
├── init.sql                       # Database initialization
└── README.md                      # Quick start guide
```

## Tính năng chính

### 1. Authentication
- ✅ User registration với validation và mã đăng ký
- ✅ User login với username/email
- ✅ JWT Access Token và Refresh Token
- ✅ Password reset functionality
- ✅ User logout
- ✅ Token refresh mechanism

### 2. User Management
- ✅ User profile management
- ✅ Password change
- ✅ Role-based access control (admin, user, viewer)
- ✅ User listing và search (Admin)
- ✅ User status management
- ✅ Registration code management (Admin)

### 3. Security Features
- ✅ Password hashing với bcrypt
- ✅ JWT token security
- ✅ Rate limiting
- ✅ Input validation với Joi
- ✅ CORS protection
- ✅ Helmet security headers
- ✅ Audit logging

### 4. Database Features
- ✅ PostgreSQL connection pooling
- ✅ Database migrations
- ✅ Seed data
- ✅ Audit trail
- ✅ Indexes cho performance

## API Endpoints

### Authentication Endpoints
| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| POST | `/api/v1/auth/register` | Đăng ký người dùng mới | Public |
| POST | `/api/v1/auth/login` | Đăng nhập | Public |
| POST | `/api/v1/auth/refresh` | Refresh token | Public |
| POST | `/api/v1/auth/logout` | Đăng xuất | Private |
| POST | `/api/v1/auth/forgot-password` | Quên mật khẩu | Public |
| POST | `/api/v1/auth/reset-password` | Đặt lại mật khẩu | Public |
| GET | `/api/v1/auth/me` | Thông tin user hiện tại | Private |

### User Management Endpoints
| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/api/v1/users/profile` | Xem profile | Private |
| PUT | `/api/v1/users/profile` | Cập nhật profile | Private |
| PUT | `/api/v1/users/change-password` | Đổi mật khẩu | Private |
| GET | `/api/v1/users` | Danh sách users | Admin |
| GET | `/api/v1/users/:id` | Chi tiết user | Admin |
| PUT | `/api/v1/users/:id` | Cập nhật user | Admin |
| DELETE | `/api/v1/users/:id` | Xóa user | Admin |

### Registration Code Management Endpoints (Admin Only)
| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/api/v1/users/registration-codes` | Danh sách mã đăng ký | Admin |
| GET | `/api/v1/users/registration-codes/:id` | Chi tiết mã đăng ký | Admin |
| POST | `/api/v1/users/registration-codes` | Tạo mã đăng ký mới | Admin |
| PUT | `/api/v1/users/registration-codes/:id` | Cập nhật mã đăng ký | Admin |
| DELETE | `/api/v1/users/registration-codes/:id` | Xóa mã đăng ký | Admin |

### System Endpoints
| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/health` | Health check | Public |

## Database Schema

### Users Table
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
    registration_code_id INTEGER REFERENCES registration_codes(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Registration Codes Table
```sql
CREATE TABLE registration_codes (
    id SERIAL PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    type VARCHAR(20) DEFAULT 'organization' CHECK (type IN ('organization', 'department', 'general')),
    max_uses INTEGER DEFAULT NULL,
    used_count INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    expires_at TIMESTAMP DEFAULT NULL,
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### User Sessions Table
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

### Audit Log Table
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

## Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| NODE_ENV | Environment | development | No |
| PORT | Server port | 3001 | No |
| API_VERSION | API version | v1 | No |
| DB_HOST | Database host | localhost | Yes |
| DB_PORT | Database port | 5432 | No |
| DB_NAME | Database name | people_counting_db | Yes |
| DB_USER | Database user | postgres | Yes |
| DB_PASSWORD | Database password | - | Yes |
| DB_SSL | Database SSL | false | No |
| JWT_SECRET | JWT secret key | - | Yes |
| JWT_ACCESS_TOKEN_EXPIRY | Access token expiry | 15m | No |
| JWT_REFRESH_TOKEN_EXPIRY | Refresh token expiry | 7d | No |
| BCRYPT_ROUNDS | Password hashing rounds | 12 | No |
| RATE_LIMIT_WINDOW_MS | Rate limit window | 900000 | No |
| RATE_LIMIT_MAX_REQUESTS | Rate limit max requests | 100 | No |
| CORS_ORIGIN | Allowed CORS origin | http://localhost:3000 | No |
| LOG_LEVEL | Logging level | info | No |

## Security Considerations

### Password Requirements
- Tối thiểu 8 ký tự
- Ít nhất 1 chữ hoa
- Ít nhất 1 chữ thường
- Ít nhất 1 số
- Ít nhất 1 ký tự đặc biệt (@$!%*?&)

### Token Security
- Access token: 15 phút
- Refresh token: 7 ngày
- JWT được ký với secret key
- Rate limiting: 100 requests/15 phút

### Database Security
- Mật khẩu được hash với bcrypt
- Reset token được hash trước khi lưu
- Audit logging cho các thay đổi quan trọng
- Parameterized queries để tránh SQL injection

## Monitoring & Logging

### Log Levels
- `error`: Lỗi nghiêm trọng
- `warn`: Cảnh báo
- `info`: Thông tin chung
- `http`: HTTP requests
- `debug`: Debug information (chỉ trong development)

### Log Files
- `logs/error.log`: Error logs
- `logs/all.log`: All logs

## Performance Optimization

### Database
- Connection pooling
- Indexes trên các trường thường query
- Prepared statements
- Query optimization

### Application
- Rate limiting
- Response caching
- Efficient error handling
- Memory management

## Tài liệu liên quan

- [API Reference](./api-reference.md)
- [Database Schema](./database-schema.md)
- [Deployment Guide](./deployment-guide.md)
- [Security Guide](./security-guide.md)

## Phiên bản

- **Version**: 1.0.0
- **Last Updated**: 2024
- **Status**: Production Ready 