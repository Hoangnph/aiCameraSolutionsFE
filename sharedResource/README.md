# 🏗️ **SHARED RESOURCES - AI Camera Counting System**

## 📊 **INFRASTRUCTURE STATUS: PRODUCTION READY ✅**

### 🎯 **Overview**
Tài liệu này hướng dẫn team development và testing sử dụng tất cả tài nguyên dùng chung trong môi trường development và production của hệ thống AI Camera Counting.

---

## 🏗️ **SYSTEM ARCHITECTURE**

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              AI CAMERA COUNTING SYSTEM                          │
│                                                                                 │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐              │
│  │   PostgreSQL    │    │     Redis       │    │   WebSocket     │              │
│  │   (Port 5432)   │    │   (Port 6379)   │    │   (Port 3003)   │              │
│  │   [Database]    │    │   [Cache]       │    │   [Real-time]   │              │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘              │
│           │                       │                       │                     │
│           └───────────┬───────────┼───────────────────────┘                     │
│                       │           │                                             │
│  ┌─────────────────┐  │  ┌─────────────────┐  ┌─────────────────┐              │
│  │   beAuth API    │  │  │  beCamera API   │  │   Frontend      │              │
│  │  (Port 3001)    │  │  │  (Port 3002)    │  │  (Port 3000)    │              │
│  │  [Auth Service] │  │  │  [AI Service]   │  │  [React App]    │              │
│  └─────────────────┘  │  └─────────────────┘  └─────────────────┘              │
│                       │                                                         │
│  ┌─────────────────┐  │  ┌─────────────────┐  ┌─────────────────┐              │
│  │   Monitoring    │  │  │   Security      │  │   Performance   │              │
│  │   [Grafana]     │  │  │   [Nginx]       │  │   [Load Test]   │              │
│  └─────────────────┘  │  └─────────────────┘  └─────────────────┘              │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🚀 **QUICK START GUIDE (NEW DOCKER-COMPOSE)**

### **1. Khởi động toàn bộ hệ thống (Development)**
```bash
# Khởi động tất cả service (database, redis, backend, websocket, frontend)
docker-compose up -d
```

### **2. Khởi động từng stack riêng lẻ (nếu cần debug độc lập)**
```bash
# Chỉ khởi động beAuth stack (auth + db)
docker-compose -f docker-compose.beauth.yml up -d

# Chỉ khởi động beCamera stack (camera + websocket + db + redis)
docker-compose -f docker-compose.becamera.yml up -d
```

### **3. Khởi động production stack**
```bash
# Khởi động production (cần build image production trước)
docker-compose -f docker-compose.prod.yml up -d
```

### **4. Kiểm tra trạng thái services**
```bash
docker ps
curl http://localhost:3001/health  # beAuth
curl http://localhost:3002/health  # beCamera
curl http://localhost:3000         # Frontend
```

### **5. Dừng toàn bộ hệ thống**
```bash
docker-compose down
```

### **6. Lưu ý**
- **KHÔNG sử dụng các file docker-compose cũ** (docker-compose.dev.yml, beAuth/docker-compose.yml, beCamera/docker-compose.yml) — đã bị xóa, chỉ dùng file hợp nhất mới.
- **Cấu hình biến môi trường**: copy file `env.example` thành `.env` và chỉnh sửa giá trị phù hợp.
- **Backup/restore**: backup đã lưu ở thư mục `backup/` nếu cần rollback.

---

## 📋 **SERVICE ENDPOINTS & STATUS**

### **🟢 ACTIVE SERVICES**

| Service | URL | Port | Status | Health Check | Description |
|---------|-----|------|--------|--------------|-------------|
| **Frontend** | http://localhost:3000 | 3000 | ✅ Running | http://localhost:3000 | React Application |
| **beAuth API** | http://localhost:3001 | 3001 | ✅ Running | http://localhost:3001/health | Authentication Service |
| **beCamera API** | http://localhost:3002 | 3002 | ✅ Running | http://localhost:3002/health | AI Camera Service |
| **WebSocket** | ws://localhost:3003 | 3003 | ✅ Running | - | Real-time Communication |
| **PostgreSQL** | localhost:5432 | 5432 | ✅ Running | `docker exec becamera_postgres pg_isready` | Main Database |
| **Redis** | localhost:6379 | 6379 | ✅ Running | `docker exec becamera_redis redis-cli ping` | Cache & Real-time Communication |

### **🔴 INACTIVE SERVICES**

| Service | URL | Port | Status | Description |
|---------|-----|------|--------|-------------|
| **N8N Workflow** | http://localhost:5678 | 5678 | ❌ Stopped | Workflow Automation |
| **Strapi CMS** | http://localhost:1337 | 1337 | ❌ Stopped | Content Management |

---

## 🗄️ **DATABASE INFORMATION**

### **📊 PostgreSQL Database**
- **Container**: `becamera_postgres`
- **Database**: `people_counting_db`
- **User**: `postgres`
- **Password**: `dev_password`
- **Port**: `5432`
- **Version**: PostgreSQL 13

### **📋 Database Schema**

#### **Tables Overview**
```sql
-- Core Tables
users                    -- User authentication & management
cameras                  -- Camera configuration & status
count_data              -- People counting data
refresh_tokens          -- JWT refresh tokens
user_sessions           -- User session management
registration_codes      -- Registration code management
audit_log               -- System audit trail
```

#### **Detailed Schema**
```sql
-- Users Table
users (
  id, username, email, password_hash, first_name, last_name,
  role, is_active, last_login, reset_password_token,
  reset_password_expires, email_verification_token,
  email_verified, created_at, updated_at, registration_code_id
)

-- Cameras Table  
cameras (
  id, name, location, stream_url, status, created_at, updated_at
)

-- Count Data Table
count_data (
  id, camera_id, people_in, people_out, current_count,
  confidence, timestamp
)

-- Refresh Tokens Table
refresh_tokens (
  id, user_id, token, expires_at, created_at
)

-- User Sessions Table
user_sessions (
  id, user_id, session_token, refresh_token, ip_address,
  user_agent, is_active, expires_at, created_at
)

-- Registration Codes Table
registration_codes (
  id, code, name, description, type, max_uses, used_count,
  is_active, expires_at, created_by, created_at, updated_at
)

-- Audit Log Table
audit_log (
  id, table_name, action, record_id, old_values, new_values,
  user_id, ip_address, timestamp
)
```

### **📊 Sample Data**
```sql
-- Cameras
INSERT INTO cameras (name, location, stream_url, status) VALUES
('Main Entrance Camera', 'Building A - Main Entrance', 'rtsp://camera1.example.com/stream1', 'active'),
('Parking Lot Camera', 'Building A - Parking Lot', 'rtsp://camera2.example.com/stream2', 'maintenance'),
('Lobby Camera', 'Building A - Lobby', 'rtsp://camera3.example.com/stream3', 'offline');

-- Count Data
INSERT INTO count_data (camera_id, people_in, people_out, current_count, confidence) VALUES
(1, 25, 18, 7, 0.92),
(1, 30, 22, 15, 0.88),
(2, 15, 12, 3, 0.95),
(2, 20, 18, 5, 0.91);
```

---

## 🔌 **API ENDPOINTS**

### **🔐 Authentication API (beAuth - Port 3001)**

#### **Base URL**: `http://localhost:3001/api/v1`

| Endpoint | Method | Description | Authentication |
|----------|--------|-------------|----------------|
| `/auth/login` | POST | User login | ❌ |
| `/auth/logout` | POST | User logout | ✅ |
| `/auth/refresh` | POST | Token refresh | ❌ |
| `/auth/me` | GET | Get current user | ✅ |
| `/users` | GET | List users | ✅ |
| `/users/{id}` | GET | Get user by ID | ✅ |
| `/users` | POST | Create user | ✅ |
| `/users/{id}` | PUT | Update user | ✅ |
| `/users/{id}` | DELETE | Delete user | ✅ |

#### **Authentication Headers**
```http
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

### **📹 Camera API (beCamera - Port 3002)**

#### **Base URL**: `http://localhost:3002/api/v1`

| Endpoint | Method | Description | Authentication |
|----------|--------|-------------|----------------|
| `/cameras` | GET | List all cameras | ✅ |
| `/cameras` | POST | Create new camera | ✅ |
| `/cameras/{id}` | GET | Get camera by ID | ✅ |
| `/cameras/{id}` | PUT | Update camera | ✅ |
| `/cameras/{id}` | DELETE | Delete camera | ✅ |
| `/cameras/{id}/status` | PATCH | Update camera status | ✅ |
| `/cameras/{id}/start` | POST | Start camera processing | ✅ |
| `/cameras/{id}/stop` | POST | Stop camera processing | ✅ |
| `/cameras/{id}/status` | GET | Get processing status | ✅ |
| `/counts` | GET | Get count data | ✅ |
| `/analytics/summary` | GET | Analytics summary | ✅ |
| `/workers/status` | GET | Worker pool status | ✅ |

### **🔌 WebSocket API (Port 3003)**

#### **Connection**: `ws://localhost:3003`

| Event | Direction | Description |
|-------|-----------|-------------|
| `connect` | Client → Server | Establish connection |
| `camera_update` | Server → Client | Real-time camera data |
| `count_update` | Server → Client | Real-time count data |
| `alert` | Server → Client | System alerts |

---

## 🔧 **DEVELOPMENT ENVIRONMENT**

### **🌐 Frontend Configuration**
```javascript
// Environment Variables (.env)
REACT_APP_API_URL=http://localhost:3001/api/v1
REACT_APP_CAMERA_API_URL=http://localhost:3002/api/v1
REACT_APP_WS_URL=ws://localhost:3003
REACT_APP_AUTH_SERVICE_URL=http://localhost:3001
```

### **🔐 beAuth Configuration**
```javascript
// Environment Variables
NODE_ENV=development
PORT=3001
DB_HOST=becamera_postgres
DB_PORT=5432
DB_NAME=people_counting_db
DB_USER=postgres
DB_PASSWORD=dev_password
JWT_SECRET=dev_jwt_secret_key_2024_ai_camera_system
JWT_ACCESS_TOKEN_EXPIRY=15m
JWT_REFRESH_TOKEN_EXPIRY=7d
BCRYPT_ROUNDS=12
CORS_ORIGIN=http://localhost:3000
// Note: beAuth uses database for session management, no Redis required
```

### **📹 beCamera Configuration**
```python
# Environment Variables
PYTHON_ENV=development
PORT=3002
DB_HOST=becamera_postgres
DB_PORT=5432
DB_NAME=people_counting_db
DB_USER=postgres
DB_PASSWORD=dev_password
REDIS_HOST=becamera_redis
REDIS_PORT=6379
JWT_SECRET=dev_jwt_secret_key_2024_ai_camera_system
CORS_ORIGIN=http://localhost:3000
# Note: beCamera uses Redis for caching, WebSocket pub/sub, and alert service
```

### **🗄️ Database Connection**
```javascript
// Frontend (src/services/authAPI.js, cameraAPI.js)
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:3001/api/v1';
const CAMERA_API_BASE_URL = process.env.REACT_APP_CAMERA_API_URL || 'http://localhost:3002/api/v1';
```

```python
# beCamera (main.py)
DB_HOST = os.getenv("DB_HOST", "becamera_postgres")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "people_counting_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "dev_password")
```

```javascript
// beAuth (config/database.js)
DB_HOST: process.env.DB_HOST || 'becamera_postgres',
DB_PORT: process.env.DB_PORT || 5432,
DB_NAME: process.env.DB_NAME || 'people_counting_db',
DB_USER: process.env.DB_USER || 'postgres',
DB_PASSWORD: process.env.DB_PASSWORD || 'dev_password'
```

### **🔴 Redis Connection**
```python
# beCamera (only service using Redis)
REDIS_HOST = os.getenv("REDIS_HOST", "becamera_redis")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")

# beAuth does not use Redis (uses database for session management)
```

---

## 🧪 **TESTING GUIDE**

### **1. API Testing**
```bash
# Test beAuth API
curl -X POST http://localhost:3001/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"admin123"}'

# Test beCamera API (requires authentication)
curl -H "Authorization: Bearer <token>" \
  http://localhost:3002/api/v1/cameras

# Test health endpoints
curl http://localhost:3001/health
curl http://localhost:3002/health
```

### **2. Database Testing**
```bash
# Connect to PostgreSQL
docker exec -it becamera_postgres psql -U postgres -d people_counting_db

# List tables
\dt

# Query data
SELECT * FROM cameras;
SELECT * FROM count_data LIMIT 10;

# Test Redis
docker exec -it becamera_redis redis-cli ping
```

### **3. Frontend Testing**
```bash
# Open browser
http://localhost:3000

# Test authentication flow
# Test camera management
# Test real-time counting
# Test analytics dashboard
```

### **4. WebSocket Testing**
```javascript
// Browser console
const ws = new WebSocket('ws://localhost:3003');
ws.onmessage = (event) => console.log('Received:', event.data);
ws.onopen = () => console.log('Connected to WebSocket');
```

---

## 🔍 **TROUBLESHOOTING**

### **Common Issues**

#### **1. Port Conflicts**
```bash
# Check port usage
lsof -i :3000  # Frontend
lsof -i :3001  # beAuth
lsof -i :3002  # beCamera
lsof -i :3003  # WebSocket
lsof -i :5432  # PostgreSQL
lsof -i :6379  # Redis
```

#### **2. Database Connection Issues**
```bash
# Check PostgreSQL status
docker exec becamera_postgres pg_isready -U postgres -d people_counting_db

# Check Redis status
docker exec becamera_redis redis-cli ping

# Restart database
docker-compose -f docker-compose.becamera.yml restart postgres redis
```

#### **3. Service Health Issues**
```bash
# Check service logs
docker logs auth_service
docker logs ai-camera-service

# Restart services
docker-compose restart  # In respective service directories

# Check container status
docker ps -a
```

#### **4. Authentication Issues**
```bash
# Check JWT token
curl -H "Authorization: Bearer <token>" http://localhost:3001/api/v1/auth/me

# Clear Redis cache
docker exec becamera_redis redis-cli FLUSHALL

# Clear Redis cache (beCamera)
docker exec becamera_redis redis-cli FLUSHALL
```

### **Environment Variables**
```bash
# Frontend (.env)
REACT_APP_API_URL=http://localhost:3001/api/v1
REACT_APP_CAMERA_API_URL=http://localhost:3002/api/v1
REACT_APP_WS_URL=ws://localhost:3003
REACT_APP_AUTH_SERVICE_URL=http://localhost:3001

# beAuth (.env)
NODE_ENV=development
PORT=3001
DB_HOST=becamera_postgres
DB_PORT=5432
DB_NAME=people_counting_db
DB_USER=postgres
DB_PASSWORD=dev_password
JWT_SECRET=dev_jwt_secret_key_2024_ai_camera_system

# beCamera (.env)
PYTHON_ENV=development
PORT=3002
DB_HOST=becamera_postgres
DB_PORT=5432
DB_NAME=people_counting_db
DB_USER=postgres
DB_PASSWORD=dev_password
REDIS_HOST=becamera_redis
REDIS_PORT=6379
```

---

## 📊 **MONITORING & LOGS**

### **Service Logs**
```bash
# beAuth logs
docker logs beauth_service

# beCamera logs
docker logs becamera_service

# Database logs
docker logs becamera_postgres

# Redis logs
docker logs becamera_redis

# Redis logs (beCamera)
docker logs becamera_redis
```

### **Health Monitoring**
```bash
# Service health checks
curl http://localhost:3001/health
curl http://localhost:3002/health

# Database health
docker exec becamera_postgres pg_isready -U postgres

# Redis health
docker exec becamera_redis redis-cli ping

# Redis health (beCamera)
docker exec becamera_redis redis-cli ping
```

---

## 📚 **ADDITIONAL RESOURCES**

### **Documentation**
- **Project Docs**: `projectDocs/` - Complete project documentation
- **API Reference**: `projectDocs/02-API-DOCUMENTATION/`
- **Database Schema**: `projectDocs/03-DATABASE/`
- **Deployment Guide**: `projectDocs/06-DEPLOYMENT/`

### **Development Tools**
- **Docker Compose**: `docker-compose.dev.yml` - Development environment
- **Docker Compose**: `docker-compose.prod.yml` - Production environment
- **Service Configs**: Individual `docker-compose.yml` in each service directory

### **Testing Resources**
- **Test Cases**: `projectDocs/07-TESTING/test-cases/`
- **API Testing**: Postman collections available
- **Load Testing**: `performance-tests/` directory

---

## 🎯 **NEXT STEPS**

### **For Developers**
1. Review API documentation in `projectDocs/02-API-DOCUMENTATION/`
2. Check database schema in `projectDocs/03-DATABASE/`
3. Follow testing guidelines in `projectDocs/07-TESTING/`
4. Use templates in `projectDocs/templates/`

### **For DevOps**
1. Review deployment guides in `projectDocs/06-DEPLOYMENT/`
2. Check monitoring setup in `projectDocs/08-MONITORING/`
3. Review security configurations in `projectDocs/09-SECURITY/`

### **For QA**
1. Review test cases in `projectDocs/07-TESTING/test-cases/`
2. Check quality gates in `projectDocs/08-MONITORING/`
3. Follow testing workflow in `projectDocs/07-TESTING/`

---

**📅 Last Updated**: [Ngày cập nhật]  
**👥 Maintainer**: Product Owner  
**📧 Contact**: [Email liên hệ]  
**🔄 Version**: 2.0 - Complete Infrastructure Documentation 

---

## HƯỚNG DẪN KHỞI ĐỘNG LẠI TOÀN BỘ DỊCH VỤ DOCKER

### 1. Tắt toàn bộ dịch vụ cũ:
```bash
docker-compose -f docker-compose.dev.yml down
```

### 2. Kiểm tra và dừng các container chiếm port:
```bash
docker ps -a
docker stop <container_name>
docker rm <container_name>
```
- Đặc biệt kiểm tra các port: 5432 (Postgres), 6379 (Redis), 3001 (beAuth), 3002 (beCamera), 3003 (WebSocket).

### 3. Khởi động lại toàn bộ stack:
```bash
docker-compose -f docker-compose.dev.yml up -d
```

### 4. Nếu gặp lỗi port, kiểm tra và dừng các container cũ như hướng dẫn trên.

### 5. Kiểm tra trạng thái dịch vụ:
```bash
docker ps
```

### 6. Truy cập frontend tại:
http://localhost:3000

---

**Lưu ý:**
- Nếu có thay đổi cấu trúc thư mục frontend, hãy đảm bảo đã cập nhật docker-compose, Dockerfile, CI/CD pipeline và các tài liệu liên quan.
- Nếu cần kiểm tra log của từng dịch vụ:
```bash
docker logs <container_name>
```
- Nếu cần dọn dẹp toàn bộ container, volume, network cũ:
```bash
docker system prune -a
```

--- 
