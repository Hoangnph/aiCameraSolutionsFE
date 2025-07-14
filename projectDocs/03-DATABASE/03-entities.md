# Database Entities - AI Camera Counting System

## 📊 Tổng quan

Tài liệu này mô tả chi tiết từng bảng/entity trong database của hệ thống AI Camera Counting, bao gồm mục đích, cấu trúc, quan hệ và các chú ý quan trọng.

## 🏗️ Entity Overview

### Core Entities Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              CORE ENTITIES OVERVIEW                             │
│                                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │   Core      │  │   Event     │  │   Analytics │  │   System    │            │
│  │   Entities  │  │   Entities  │  │   Entities  │  │   Entities  │            │
│  │             │  │             │  │             │  │             │            │
│  │ • users     │  │ • camera_events│  │ • counting_results│  │ • audit_logs │            │
│  │ • cameras   │  │ • model_logs │  │ • analytics │  │ • alerts    │            │
│  │ • zones     │  │ • user_sessions│  │ • reports   │  │ • files     │            │
│  │ • ai_models │  │ • system_logs│  │ • trends    │  │ • configs   │            │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘            │
│         │                   │                   │                   │            │
│         │                   │                   │                   │            │
│         ▼                   ▼                   ▼                   ▼            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │   Primary   │  │   Time-     │  │   Aggregated│  │   Metadata  │            │
│  │   Data      │  │   Series    │  │   Data      │  │   & Logs    │            │
│  │             │  │   Data      │  │             │  │             │            │
│  │ • Master    │  │ • Events    │  │ • Analytics │  │ • Audit     │            │
│  │   Records   │  │ • Logs      │  │ • Reports   │  │   Trail     │            │
│  │ • Reference │  │ • Metrics   │  │ • Trends    │  │ • System    │            │
│  │   Data      │  │ • Alerts    │  │ • KPIs      │  │   Info      │            │
│  │ • Config    │  │ • Notifications│  │ • Forecasts │  │ • Files    │            │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘            │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 📋 Core Entities

### 1. users Table

**Mục đích**: Quản lý thông tin người dùng và phân quyền truy cập hệ thống.

**Mô tả**: Bảng này lưu trữ thông tin người dùng, bao gồm thông tin cá nhân, thông tin đăng nhập, và phân quyền. Được đồng bộ với hệ thống beAuth.

**Cấu trúc bảng**:
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

**Chi tiết các trường**:
- `id`: Primary key, auto-increment
- `username`: Tên đăng nhập, unique, không được trống
- `email`: Email người dùng, unique, không được trống
- `password_hash`: Hash của mật khẩu (bcrypt)
- `first_name`: Tên người dùng
- `last_name`: Họ người dùng
- `role`: Vai trò người dùng (admin, user, viewer)
- `is_active`: Trạng thái hoạt động
- `last_login`: Thời gian đăng nhập cuối
- `reset_password_token`: Token reset mật khẩu
- `reset_password_expires`: Thời gian hết hạn token reset
- `email_verification_token`: Token xác thực email
- `email_verified`: Trạng thái xác thực email
- `created_at`: Thời gian tạo
- `updated_at`: Thời gian cập nhật cuối

**Quan hệ**:
- 1:N với `user_sessions`
- 1:N với `audit_logs`
- 1:N với `camera_permissions` (nếu có)

**Indexes**:
```sql
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_created_at ON users(created_at);
CREATE INDEX idx_users_reset_token ON users(reset_password_token);
```

**Chú ý**:
- Đồng bộ với hệ thống beAuth
- Mật khẩu được hash bằng bcrypt
- Token có thời gian hết hạn
- Audit log cho tất cả thay đổi

### 2. cameras Table

**Mục đích**: Quản lý thông tin camera và cấu hình xử lý.

**Mô tả**: Bảng này lưu trữ thông tin chi tiết về các camera trong hệ thống, bao gồm thông tin kết nối, cấu hình xử lý, và trạng thái hoạt động.

**Cấu trúc bảng**:
```sql
CREATE TABLE cameras (
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
```

**Chi tiết các trường**:
- `id`: Primary key, auto-increment
- `name`: Tên camera, không được trống
- `description`: Mô tả camera
- `ip_address`: Địa chỉ IP camera
- `port`: Port kết nối (mặc định 554 cho RTSP)
- `rtsp_url`: URL stream RTSP
- `username`: Username kết nối camera
- `password`: Password kết nối camera (encrypted)
- `model`: Model camera
- `manufacturer`: Nhà sản xuất camera
- `resolution_width`: Độ phân giải chiều rộng
- `resolution_height`: Độ phân giải chiều cao
- `fps`: Frames per second
- `status`: Trạng thái camera (online, offline, maintenance, error)
- `is_active`: Trạng thái hoạt động
- `ai_model_id`: ID model AI được sử dụng
- `config`: Cấu hình JSON cho camera
- `last_heartbeat`: Thời gian heartbeat cuối
- `last_error`: Lỗi cuối cùng
- `error_count`: Số lần lỗi
- `created_at`: Thời gian tạo
- `updated_at`: Thời gian cập nhật cuối

**Quan hệ**:
- N:1 với `ai_models`
- 1:N với `zones`
- 1:N với `camera_events`
- 1:N với `counting_results`

**Indexes**:
```sql
CREATE INDEX idx_cameras_ip_address ON cameras(ip_address);
CREATE INDEX idx_cameras_status ON cameras(status);
CREATE INDEX idx_cameras_is_active ON cameras(is_active);
CREATE INDEX idx_cameras_ai_model_id ON cameras(ai_model_id);
CREATE INDEX idx_cameras_last_heartbeat ON cameras(last_heartbeat);
```

**Chú ý**:
- Password được encrypt
- Config lưu dưới dạng JSONB
- Heartbeat monitoring
- Error tracking và retry logic

### 3. zones Table

**Mục đích**: Định nghĩa các khu vực đếm người trong camera.

**Mô tả**: Bảng này định nghĩa các vùng/zones trong camera để đếm người ra/vào, bao gồm tọa độ và loại zone.

**Cấu trúc bảng**:
```sql
CREATE TABLE zones (
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
```

**Chi tiết các trường**:
- `id`: Primary key, auto-increment
- `name`: Tên zone, không được trống
- `description`: Mô tả zone
- `camera_id`: ID camera chứa zone
- `zone_type`: Loại zone (entrance, exit, area, line)
- `coordinates`: Tọa độ zone (JSON array of points)
- `direction`: Hướng đếm (in, out, bidirectional)
- `is_active`: Trạng thái hoạt động
- `config`: Cấu hình JSON cho zone
- `created_at`: Thời gian tạo
- `updated_at`: Thời gian cập nhật cuối

**Quan hệ**:
- N:1 với `cameras`
- 1:N với `counting_results`

**Indexes**:
```sql
CREATE INDEX idx_zones_camera_id ON zones(camera_id);
CREATE INDEX idx_zones_zone_type ON zones(zone_type);
CREATE INDEX idx_zones_is_active ON zones(is_active);
```

**Chú ý**:
- Coordinates lưu dưới dạng JSONB
- Cascade delete khi camera bị xóa
- Support nhiều loại zone khác nhau

### 4. ai_models Table

**Mục đích**: Quản lý các model AI và version.

**Mô tả**: Bảng này lưu trữ thông tin về các model AI được sử dụng trong hệ thống, bao gồm version, trạng thái, và cấu hình.

**Cấu trúc bảng**:
```sql
CREATE TABLE ai_models (
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
```

**Chi tiết các trường**:
- `id`: Primary key, auto-increment
- `name`: Tên model, không được trống
- `version`: Version model, không được trống
- `description`: Mô tả model
- `model_type`: Loại model (detection, classification, tracking)
- `file_path`: Đường dẫn file model
- `file_size`: Kích thước file (bytes)
- `checksum`: Checksum file để verify integrity
- `status`: Trạng thái model (active, inactive, training, error)
- `accuracy`: Độ chính xác model (0-1)
- `inference_time_ms`: Thời gian inference trung bình (ms)
- `config`: Cấu hình JSON cho model
- `created_at`: Thời gian tạo
- `updated_at`: Thời gian cập nhật cuối

**Quan hệ**:
- 1:N với `cameras`
- 1:N với `model_logs`

**Indexes**:
```sql
CREATE INDEX idx_ai_models_name_version ON ai_models(name, version);
CREATE INDEX idx_ai_models_status ON ai_models(status);
CREATE INDEX idx_ai_models_model_type ON ai_models(model_type);
```

**Chú ý**:
- Unique constraint trên name + version
- Checksum để verify file integrity
- Performance metrics tracking

## 📊 Event Entities

### 5. camera_events Table

**Mục đích**: Lưu trữ các sự kiện từ camera.

**Mô tả**: Bảng này lưu trữ tất cả các sự kiện từ camera, bao gồm sự kiện hệ thống, lỗi, và thông tin trạng thái.

**Cấu trúc bảng**:
```sql
CREATE TABLE camera_events (
    id SERIAL PRIMARY KEY,
    camera_id INTEGER NOT NULL REFERENCES cameras(id) ON DELETE CASCADE,
    event_type event_type NOT NULL,
    severity event_severity DEFAULT 'info',
    message TEXT,
    data JSONB DEFAULT '{}',
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Chi tiết các trường**:
- `id`: Primary key, auto-increment
- `camera_id`: ID camera
- `event_type`: Loại sự kiện (connection, detection, error, maintenance)
- `severity`: Mức độ nghiêm trọng (info, warning, error, critical)
- `message`: Nội dung sự kiện
- `data`: Dữ liệu bổ sung (JSON)
- `timestamp`: Thời gian sự kiện

**Quan hệ**:
- N:1 với `cameras`

**Indexes**:
```sql
CREATE INDEX idx_camera_events_camera_id ON camera_events(camera_id);
CREATE INDEX idx_camera_events_event_type ON camera_events(event_type);
CREATE INDEX idx_camera_events_severity ON camera_events(severity);
CREATE INDEX idx_camera_events_timestamp ON camera_events(timestamp);
```

**Chú ý**:
- Partitioning theo timestamp
- Data lưu dưới dạng JSONB
- Cascade delete với camera

### 6. counting_results Table

**Mục đích**: Lưu trữ kết quả đếm người từ camera.

**Mô tả**: Bảng này lưu trữ kết quả đếm người real-time từ các camera và zone, bao gồm số lượng người ra/vào theo thời gian.

**Cấu trúc bảng**:
```sql
CREATE TABLE counting_results (
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
```

**Chi tiết các trường**:
- `id`: Primary key, auto-increment
- `camera_id`: ID camera
- `zone_id`: ID zone
- `timestamp`: Thời gian đếm
- `count_in`: Số người đi vào
- `count_out`: Số người đi ra
- `total_count`: Tổng số người hiện tại
- `confidence`: Độ tin cậy của kết quả (0-1)
- `frame_data`: Dữ liệu frame (JSON)
- `created_at`: Thời gian tạo record

**Quan hệ**:
- N:1 với `cameras`
- N:1 với `zones`

**Indexes**:
```sql
CREATE INDEX idx_counting_results_camera_id ON counting_results(camera_id);
CREATE INDEX idx_counting_results_zone_id ON counting_results(zone_id);
CREATE INDEX idx_counting_results_timestamp ON counting_results(timestamp);
CREATE INDEX idx_counting_results_camera_timestamp ON counting_results(camera_id, timestamp);
```

**Chú ý**:
- Partitioning theo timestamp
- High-frequency writes
- Aggregation cho analytics

## 📈 Analytics Entities

### 7. analytics Table

**Mục đích**: Lưu trữ dữ liệu analytics đã được tổng hợp.

**Mô tả**: Bảng này lưu trữ các dữ liệu analytics đã được tính toán và tổng hợp từ counting_results, bao gồm thống kê theo giờ, ngày, tuần, tháng.

**Cấu trúc bảng**:
```sql
CREATE TABLE analytics (
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
```

**Chi tiết các trường**:
- `id`: Primary key, auto-increment
- `camera_id`: ID camera
- `zone_id`: ID zone (NULL cho tổng hợp toàn camera)
- `period_type`: Loại period (hour, day, week, month)
- `period_start`: Thời gian bắt đầu period
- `period_end`: Thời gian kết thúc period
- `total_count_in`: Tổng số người đi vào
- `total_count_out`: Tổng số người đi ra
- `peak_count`: Số người cao nhất trong period
- `peak_time`: Thời gian đạt peak
- `avg_count`: Số người trung bình
- `data_points`: Số điểm dữ liệu
- `created_at`: Thời gian tạo
- `updated_at`: Thời gian cập nhật cuối

**Quan hệ**:
- N:1 với `cameras`
- N:1 với `zones`

**Indexes**:
```sql
CREATE INDEX idx_analytics_camera_id ON analytics(camera_id);
CREATE INDEX idx_analytics_zone_id ON analytics(zone_id);
CREATE INDEX idx_analytics_period_type ON analytics(period_type);
CREATE INDEX idx_analytics_period_start ON analytics(period_start);
CREATE INDEX idx_analytics_camera_period ON analytics(camera_id, period_type, period_start);
```

**Chú ý**:
- Partitioning theo period_start
- Aggregated data từ counting_results
- Batch processing để tính toán

## 🔔 System Entities

### 8. alerts Table

**Mục đích**: Quản lý các cảnh báo và thông báo hệ thống.

**Mô tả**: Bảng này lưu trữ các cảnh báo từ hệ thống, bao gồm cảnh báo camera offline, lỗi AI model, và các sự kiện bất thường.

**Cấu trúc bảng**:
```sql
CREATE TABLE alerts (
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
```

**Chi tiết các trường**:
- `id`: Primary key, auto-increment
- `alert_type`: Loại cảnh báo (camera_offline, system_error, high_traffic, maintenance, detection_error)
- `severity`: Mức độ nghiêm trọng (low, medium, high, critical)
- `title`: Tiêu đề cảnh báo
- `message`: Nội dung cảnh báo
- `camera_id`: ID camera liên quan
- `zone_id`: ID zone liên quan
- `data`: Dữ liệu bổ sung (JSON)
- `is_resolved`: Trạng thái đã giải quyết
- `resolved_at`: Thời gian giải quyết
- `resolved_by`: User giải quyết
- `created_at`: Thời gian tạo
- `updated_at`: Thời gian cập nhật cuối

**Quan hệ**:
- N:1 với `cameras`
- N:1 với `zones`
- N:1 với `users` (resolved_by)

**Indexes**:
```sql
CREATE INDEX idx_alerts_alert_type ON alerts(alert_type);
CREATE INDEX idx_alerts_severity ON alerts(severity);
CREATE INDEX idx_alerts_camera_id ON alerts(camera_id);
CREATE INDEX idx_alerts_is_resolved ON alerts(is_resolved);
CREATE INDEX idx_alerts_created_at ON alerts(created_at);
```

**Chú ý**:
- Auto-resolution cho một số loại alert
- Notification integration
- Escalation rules

### 9. audit_logs Table

**Mục đích**: Ghi nhận tất cả các thay đổi trong hệ thống.

**Mô tả**: Bảng này lưu trữ audit trail cho tất cả các thay đổi dữ liệu trong hệ thống, đảm bảo tính minh bạch và có thể truy vết.

**Cấu trúc bảng**:
```sql
CREATE TABLE audit_logs (
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
```

**Chi tiết các trường**:
- `id`: Primary key, auto-increment
- `table_name`: Tên bảng được thay đổi
- `action`: Hành động (INSERT, UPDATE, DELETE)
- `record_id`: ID record được thay đổi
- `old_values`: Giá trị cũ (JSON)
- `new_values`: Giá trị mới (JSON)
- `user_id`: User thực hiện thay đổi
- `ip_address`: IP address của user
- `user_agent`: User agent của browser
- `timestamp`: Thời gian thay đổi

**Quan hệ**:
- N:1 với `users`

**Indexes**:
```sql
CREATE INDEX idx_audit_logs_table_name ON audit_logs(table_name);
CREATE INDEX idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_timestamp ON audit_logs(timestamp);
CREATE INDEX idx_audit_logs_action ON audit_logs(action);
```

**Chú ý**:
- Trigger-based logging
- Data retention policy
- Compliance requirements

### 10. user_sessions Table

**Mục đích**: Quản lý session của người dùng.

**Mô tả**: Bảng này lưu trữ thông tin session của người dùng, bao gồm token, thời gian hết hạn, và thông tin kết nối.

**Cấu trúc bảng**:
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

**Chi tiết các trường**:
- `id`: Primary key, auto-increment
- `user_id`: ID user
- `session_token`: Token session
- `refresh_token`: Token refresh
- `ip_address`: IP address của user
- `user_agent`: User agent của browser
- `is_active`: Trạng thái active
- `expires_at`: Thời gian hết hạn
- `created_at`: Thời gian tạo

**Quan hệ**:
- N:1 với `users`

**Indexes**:
```sql
CREATE INDEX idx_user_sessions_user_id ON user_sessions(user_id);
CREATE INDEX idx_user_sessions_token ON user_sessions(session_token);
CREATE INDEX idx_user_sessions_refresh_token ON user_sessions(refresh_token);
CREATE INDEX idx_user_sessions_expires_at ON user_sessions(expires_at);
```

**Chú ý**:
- Auto-cleanup expired sessions
- Security token rotation
- Multi-device support

## 📁 Supporting Entities

### 11. files Table

**Mục đích**: Quản lý các file media và tài liệu.

**Mô tả**: Bảng này lưu trữ thông tin về các file trong hệ thống, bao gồm video clips, screenshots, và các tài liệu khác.

**Cấu trúc bảng**:
```sql
CREATE TABLE files (
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
```

**Chi tiết các trường**:
- `id`: Primary key, auto-increment
- `filename`: Tên file trong hệ thống
- `original_filename`: Tên file gốc
- `file_path`: Đường dẫn file
- `file_size`: Kích thước file (bytes)
- `mime_type`: Loại MIME
- `file_type`: Loại file (media, document, log, backup)
- `camera_id`: ID camera liên quan
- `zone_id`: ID zone liên quan
- `metadata`: Metadata bổ sung (JSON)
- `is_public`: Có public không
- `expires_at`: Thời gian hết hạn
- `created_at`: Thời gian tạo

**Quan hệ**:
- N:1 với `cameras`
- N:1 với `zones`

**Indexes**:
```sql
CREATE INDEX idx_files_camera_id ON files(camera_id);
CREATE INDEX idx_files_file_type ON files(file_type);
CREATE INDEX idx_files_created_at ON files(created_at);
CREATE INDEX idx_files_expires_at ON files(expires_at);
```

**Chú ý**:
- Auto-cleanup expired files
- Storage optimization
- Backup strategy

---

**Tài liệu này mô tả chi tiết tất cả các entities trong database của AI Camera Counting System, bao gồm cấu trúc, quan hệ, và các chú ý quan trọng cho việc triển khai và bảo trì.** 