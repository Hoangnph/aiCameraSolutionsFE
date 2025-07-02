# Authentication Service - People Counting Dashboard

## Tổng quan

Authentication Service là một microservice Node.js được xây dựng để xử lý xác thực và quản lý người dùng cho hệ thống People Counting Dashboard. Service này sử dụng PostgreSQL làm cơ sở dữ liệu và JWT cho xác thực.

## Tính năng

### Authentication
- ✅ Đăng ký người dùng mới
- ✅ Đăng nhập với username/email
- ✅ JWT Access Token và Refresh Token
- ✅ Đăng xuất
- ✅ Quên mật khẩu
- ✅ Đặt lại mật khẩu
- ✅ Xác thực token

### User Management
- ✅ Xem thông tin profile
- ✅ Cập nhật thông tin profile
- ✅ Thay đổi mật khẩu
- ✅ Quản lý người dùng (Admin)
- ✅ Phân quyền theo role (admin, user, viewer)

### Security
- ✅ Mã hóa mật khẩu với bcrypt
- ✅ Rate limiting
- ✅ Input validation với Joi
- ✅ CORS protection
- ✅ Helmet security headers
- ✅ Audit logging

## Cấu trúc dự án

```
beAuth/
├── src/
│   ├── config/
│   │   └── database.js          # Database configuration
│   ├── middleware/
│   │   ├── auth.js              # Authentication middleware
│   │   ├── errorHandler.js      # Error handling middleware
│   │   └── notFoundHandler.js   # 404 handler
│   ├── routes/
│   │   ├── auth.js              # Authentication routes
│   │   └── user.js              # User management routes
│   ├── utils/
│   │   ├── jwt.js               # JWT utilities
│   │   ├── validation.js        # Validation schemas
│   │   └── logger.js            # Logging utility
│   ├── database/
│   │   ├── migrate.js           # Database migrations
│   │   └── seed.js              # Seed data
│   └── index.js                 # Main application file
├── package.json                 # Dependencies
├── env.example                  # Environment variables example
└── README.md                    # This file
```

## Cài đặt

### Yêu cầu hệ thống
- Node.js >= 16.0.0
- PostgreSQL >= 12.0
- npm hoặc yarn

### Bước 1: Clone và cài đặt dependencies
```bash
cd beAuth
npm install
```

### Bước 2: Cấu hình môi trường
```bash
cp env.example .env
```

Chỉnh sửa file `.env` với thông tin database và các cấu hình khác:
```env
# Server Configuration
NODE_ENV=development
PORT=3001
API_VERSION=v1

# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=people_counting_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_SSL=false

# JWT Configuration
JWT_SECRET=your_super_secret_jwt_key_here
JWT_ACCESS_TOKEN_EXPIRY=15m
JWT_REFRESH_TOKEN_EXPIRY=7d

# Security
BCRYPT_ROUNDS=12
RATE_LIMIT_WINDOW_MS=900000
RATE_LIMIT_MAX_REQUESTS=100

# CORS
CORS_ORIGIN=http://localhost:3000
```

### Bước 3: Tạo database
```sql
CREATE DATABASE people_counting_db;
```

### Bước 4: Chạy migrations
```bash
npm run migrate
```

### Bước 5: Seed dữ liệu mẫu (tùy chọn)
```bash
npm run seed
```

### Bước 6: Khởi chạy server
```bash
# Development mode
npm run dev

# Production mode
npm start
```

## API Endpoints

### Authentication

#### Đăng ký
```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "username": "newuser",
  "email": "user@example.com",
  "password": "Password123!",
  "confirmPassword": "Password123!",
  "firstName": "John",
  "lastName": "Doe"
}
```

#### Đăng nhập
```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "username": "newuser",
  "password": "Password123!"
}
```

#### Refresh Token
```http
POST /api/v1/auth/refresh
Content-Type: application/json

{
  "refreshToken": "your_refresh_token"
}
```

#### Đăng xuất
```http
POST /api/v1/auth/logout
Authorization: Bearer your_access_token
```

#### Quên mật khẩu
```http
POST /api/v1/auth/forgot-password
Content-Type: application/json

{
  "email": "user@example.com"
}
```

#### Đặt lại mật khẩu
```http
POST /api/v1/auth/reset-password
Content-Type: application/json

{
  "token": "reset_token",
  "password": "NewPassword123!",
  "confirmPassword": "NewPassword123!"
}
```

### User Management

#### Xem profile
```http
GET /api/v1/auth/me
Authorization: Bearer your_access_token
```

#### Cập nhật profile
```http
PUT /api/v1/users/profile
Authorization: Bearer your_access_token
Content-Type: application/json

{
  "firstName": "John",
  "lastName": "Smith",
  "email": "newemail@example.com"
}
```

#### Thay đổi mật khẩu
```http
PUT /api/v1/users/change-password
Authorization: Bearer your_access_token
Content-Type: application/json

{
  "currentPassword": "OldPassword123!",
  "newPassword": "NewPassword123!",
  "confirmNewPassword": "NewPassword123!"
}
```

#### Quản lý người dùng (Admin)
```http
GET /api/v1/users?page=1&limit=10&search=john&role=user
Authorization: Bearer your_access_token
```

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
  role VARCHAR(20) DEFAULT 'user' CHECK (role IN ('admin', 'user', 'viewer')),
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

## Tài khoản mặc định

Sau khi chạy seed, các tài khoản mặc định sẽ được tạo:

- **Admin**: `admin` / `Admin123!`
- **Test User**: `testuser` / `Test123!`
- **Viewer**: `viewer` / `Viewer123!`

## Development

### Scripts
```bash
npm start          # Start production server
npm run dev        # Start development server with nodemon
npm test           # Run tests
npm run lint       # Run ESLint
npm run migrate    # Run database migrations
npm run seed       # Seed sample data
```

### Environment Variables
- `NODE_ENV`: Environment (development/production)
- `PORT`: Server port (default: 3001)
- `DB_HOST`: Database host
- `DB_PORT`: Database port
- `DB_NAME`: Database name
- `DB_USER`: Database user
- `DB_PASSWORD`: Database password
- `JWT_SECRET`: JWT secret key
- `JWT_ACCESS_TOKEN_EXPIRY`: Access token expiry (default: 15m)
- `JWT_REFRESH_TOKEN_EXPIRY`: Refresh token expiry (default: 7d)
- `BCRYPT_ROUNDS`: Password hashing rounds (default: 12)
- `CORS_ORIGIN`: Allowed CORS origin

## Security

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

## Monitoring & Logging

Service sử dụng Winston logger với các level:
- `error`: Lỗi nghiêm trọng
- `warn`: Cảnh báo
- `info`: Thông tin chung
- `http`: HTTP requests
- `debug`: Debug information (chỉ trong development)

## Deployment

### Docker (Recommended)
```dockerfile
FROM node:16-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
EXPOSE 3001
CMD ["npm", "start"]
```

### Environment Variables for Production
```env
NODE_ENV=production
PORT=3001
DB_HOST=your_db_host
DB_NAME=people_counting_db
DB_USER=your_db_user
DB_PASSWORD=your_secure_password
JWT_SECRET=your_very_secure_jwt_secret
CORS_ORIGIN=https://your-frontend-domain.com
```

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Kiểm tra thông tin database trong `.env`
   - Đảm bảo PostgreSQL đang chạy
   - Kiểm tra quyền truy cập database

2. **JWT Token Error**
   - Kiểm tra `JWT_SECRET` trong `.env`
   - Đảm bảo token chưa hết hạn
   - Kiểm tra format token trong header

3. **Validation Error**
   - Kiểm tra format dữ liệu gửi lên
   - Đảm bảo password đáp ứng yêu cầu
   - Kiểm tra email format

## Contributing

1. Fork repository
2. Tạo feature branch
3. Commit changes
4. Push to branch
5. Tạo Pull Request

## License

MIT License 