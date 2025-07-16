# beCamera Service Fix Summary

## Tổng quan
Tài liệu này mô tả các lỗi đã được sửa và trạng thái hiện tại của beCamera service trong hệ thống AI Camera Counting.

## Các lỗi đã được sửa

### 1. Database Schema Mismatch
**Vấn đề:** beCamera service đang sử dụng schema cũ không khớp với database thực tế.

**Lỗi cụ thể:**
- Sử dụng `ip_address` thay vì `location`
- Sử dụng `rtsp_url` thay vì `stream_url`
- Sử dụng `count_data` table thay vì `counting_results`
- Sử dụng `people_in/people_out` thay vì `count_in/count_out`

**Giải pháp:**
- Cập nhật tất cả SQL queries trong `beCamera/main.py`
- Thay đổi field names trong API responses
- Cập nhật cả authenticated và test endpoints

### 2. Docker Networking Issues
**Vấn đề:** beCamera service không thể kết nối với Redis và có port conflicts.

**Lỗi cụ thể:**
- `REDIS_HOST=beauth_redis` (sai container name - đã sửa thành becamera_redis)
- Port conflict giữa becamera service và websocket service (cùng port 3003)

**Giải pháp:**
- Thay đổi `REDIS_HOST=becamera_redis` trong `beCamera/env.camera`
- Thay đổi websocket port từ 3003 → 3004 trong `docker-compose.becamera.yml`
- Loại bỏ port 3003 không cần thiết từ becamera service

### 3. Environment Configuration
**Vấn đề:** Environment variables không đồng bộ giữa các services.

**Giải pháp:**
- Cập nhật `env.example` với các giá trị thực tế đang hoạt động
- Đồng bộ JWT_SECRET giữa beAuth và beCamera
- Cập nhật WebSocket URL trong frontend config

## 4. Environment Variable Issue (2025-07-15)
**Vấn đề:**
- beCamera không thể xác thực token với beAuth do thiếu biến môi trường `AUTH_SERVICE_URL` trong container (dù đã có trong docker-compose).
- Dẫn đến mọi request `/api/v1/cameras` trả về 503 (Service Unavailable) dù backend và database đều healthy.

**Giải pháp:**
- Thêm biến môi trường `AUTH_SERVICE_URL=http://ai_camera_beauth:3001` vào service `becamera` trong `docker-compose.yml`.
- Rebuild container bằng `docker-compose up -d --build becamera` để biến môi trường được áp dụng.
- Kiểm tra lại bằng `docker exec ai_camera_becamera env | grep AUTH_SERVICE_URL`.

**Kết quả:**
- beCamera xác thực token thành công với beAuth, API trả về đúng dữ liệu khi user đã đăng nhập.

## 5. Dataflow xác thực camera API (2025-07-15)
1. Frontend gửi request `/api/v1/cameras` kèm accessToken.
2. beCamera nhận request, gửi token sang beAuth (`/api/v1/auth/verify`) để xác thực.
3. Nếu token hợp lệ, truy vấn database và trả về dữ liệu camera.
4. Nếu token không hợp lệ, trả về 401.
5. Nếu không kết nối được beAuth, trả về 503.

## Trạng thái hiện tại

### ✅ Services đang hoạt động
1. **beAuth Service** (Port 3001)
   - Authentication endpoints hoạt động
   - User registration với registration codes
   - JWT token generation và validation
   - Database connection thành công

2. **beCamera Service** (Port 3002)
   - Health check: `{"status":"healthy","database":"connected","redis":"connected"}`
   - Camera CRUD operations hoạt động
   - Authentication integration thành công
   - Analytics endpoints hoạt động

3. **Database** (PostgreSQL)
   - Unified schema được áp dụng
   - Sample data có sẵn (3 cameras, users, registration codes)
   - All tables và relationships hoạt động

4. **Redis** (Port 6379)
   - Cache service hoạt động
   - Worker pool integration thành công

### ✅ API Endpoints đã test
1. **Authentication:**
   - `POST /api/v1/auth/register` ✅
   - `POST /api/v1/auth/login` ✅
   - `POST /api/v1/auth/verify` ✅

2. **Camera Management:**
   - `GET /api/v1/cameras` (authenticated) ✅
   - `GET /api/v1/test/cameras` (public) ✅
   - `POST /api/v1/cameras` (create) ✅
   - `GET /api/v1/analytics/summary` ✅

3. **Health Checks:**
   - `GET /health` (beCamera) ✅
   - `GET /health` (beAuth) ✅

## Cấu hình hiện tại

### Database Schema (cameras table)
```sql
CREATE TABLE cameras (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    ip_address VARCHAR(500),
    rtsp_url TEXT,
    status camera_status DEFAULT 'offline',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Environment Variables
```bash
# Database
DB_HOST=becamera_postgres
DB_PORT=5432
DB_NAME=people_counting_db
DB_USER=postgres
DB_PASSWORD=dev_password

# Redis
REDIS_HOST=becamera_redis
REDIS_PORT=6379

# JWT
JWT_SECRET=dev_jwt_secret_key_2024_ai_camera_system

# Auth Service
AUTH_SERVICE_URL=http://ai_camera_beauth:3001
```

### Port Configuration
- beAuth Service: 3001
- beCamera Service: 3002
- WebSocket Service: 3004
- PostgreSQL: 5432
- Redis: 6379

## Test Data Available

### Users
- admin (role: admin)
- testuser (role: user)
- viewer (role: viewer)
- testadmin (role: user) - newly created

### Registration Codes
- REG001 (max_uses: 100, used: 7)
- REG002 (max_uses: 50, used: 0)
- LIMITED (max_uses: 1, used: 0)

### Cameras
- Main Entrance Camera (active)
- Parking Lot Camera (active)
- Lobby Camera (offline)
- Test Camera (offline) - newly created

## Next Steps

1. **Frontend Integration**
   - Test frontend với beCamera API
   - Implement camera management UI
   - Add real-time updates via WebSocket

2. **AI Model Integration**
   - Implement camera processing với AI models
   - Add people counting logic
   - Real-time analytics

3. **Production Deployment**
   - Security hardening
   - Performance optimization
   - Monitoring và logging

## Troubleshooting

### Common Issues
1. **Port conflicts:** Kiểm tra `lsof -i :PORT` trước khi start services
2. **Database connection:** Đảm bảo PostgreSQL container healthy
3. **Redis connection:** Kiểm tra container name trong environment
4. **JWT validation:** Đảm bảo JWT_SECRET đồng bộ giữa services

### Useful Commands
```bash
# Check service health
curl http://localhost:3001/health
curl http://localhost:3002/health

# Test authentication
curl -X POST http://localhost:3001/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "testadmin", "password": "Test123!"}'

# Test camera API
curl -X GET http://localhost:3002/api/v1/test/cameras

# Check database
docker exec becamera_postgres psql -U postgres -d people_counting_db -c "\dt"
``` 