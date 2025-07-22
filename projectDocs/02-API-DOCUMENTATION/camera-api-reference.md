# Camera API Specification

## 📊 Tổng quan

API quản lý camera cho hệ thống People Counting với đầy đủ CRUD operations và real-time streaming.

## 🏗️ API Architecture Overview

### System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              CAMERA API ARCHITECTURE                            │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              CLIENT LAYER                                   │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Web       │  │   Mobile    │  │   Desktop   │  │   IoT       │        │ │
│  │  │   Client    │  │   Client    │  │   Client    │  │   Device    │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                             │
│                                    ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              API GATEWAY LAYER                              │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Load      │  │   Rate      │  │   Auth      │  │   Request   │        │ │
│  │  │   Balancer  │  │   Limiting  │  │   Gateway   │  │   Routing   │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                             │
│                                    ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              API SERVICE LAYER                              │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Camera    │  │   Stream    │  │   Analytics │  │   Health    │        │ │
│  │  │   Manager   │  │   Processor │  │   Service   │  │   Monitor   │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                             │
│                                    ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              DATA LAYER                                      │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Camera    │  │   Analytics │  │   Stream    │  │   Settings  │        │ │
│  │  │   Database  │  │   Database  │  │   Storage   │  │   Cache     │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              EXTERNAL SYSTEMS                               │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Camera    │  │   AI Model  │  │   Worker    │  │   Monitoring│        │ │
│  │  │   Devices   │  │   Service   │  │   Pool      │  │   System    │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### API Request/Response Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              API REQUEST/RESPONSE FLOW                          │
│                                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐      │
│  │   Client    │    │   API       │    │   Service   │    │   Database  │      │
│  │   Request   │    │   Gateway   │    │   Layer     │    │   Layer     │      │
│  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘      │
│         │                   │                   │                   │          │
│         │ 1. HTTP Request   │                   │                   │          │
│         │ (GET/POST/PUT/DEL)│                   │                   │          │
│         │──────────────────►│                   │                   │          │
│         │                   │                   │                   │          │
│         │                   │ 2. Auth Check     │                   │          │
│         │                   │ Rate Limiting     │                   │          │
│         │                   │ Request Routing   │                   │          │
│         │                   │──────────────────►│                   │          │
│         │                   │                   │                   │          │
│         │                   │                   │ 3. Business Logic │          │
│         │                   │                   │ Data Validation   │          │
│         │                   │                   │──────────────────►│          │
│         │                   │                   │                   │          │
│         │                   │                   │                   │ 4. Query │
│         │                   │                   │                   │ Database │
│         │                   │                   │                   │◄─────────┤
│         │                   │                   │                   │          │
│         │                   │                   │ 5. Process Data   │          │
│         │                   │                   │◄──────────────────┤          │
│         │                   │                   │                   │          │
│         │                   │ 6. Format Response│                   │          │
│         │                   │◄──────────────────┤                   │          │
│         │                   │                   │                   │          │
│         │ 7. HTTP Response  │                   │                   │          │
│         │◄──────────────────┤                   │                   │          │
│         │                   │                   │                   │          │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### API Authentication Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              API AUTHENTICATION FLOW                            │
│                                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐      │
│  │   Client    │    │   API       │    │   Auth      │    │   Database  │      │
│  │   (Frontend)│    │   Gateway   │    │   Service   │    │             │      │
│  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘      │
│         │                   │                   │                   │          │
│         │ 1. Login Request  │                   │                   │          │
│         │ (username/password)│                   │                   │          │
│         │──────────────────►│                   │                   │          │
│         │                   │                   │                   │          │
│         │                   │ 2. Forward to Auth│                   │          │
│         │                   │ Service           │                   │          │
│         │                   │──────────────────►│                   │          │
│         │                   │                   │                   │          │
│         │                   │                   │ 3. Validate Credentials│      │
│         │                   │                   │──────────────────►│          │
│         │                   │                   │                   │          │
│         │                   │                   │                   │ 4. Check │
│         │                   │                   │                   │ User DB  │
│         │                   │                   │                   │◄─────────┤
│         │                   │                   │                   │          │
│         │                   │                   │ 5. Generate JWT   │          │
│         │                   │                   │◄──────────────────┤          │
│         │                   │                   │                   │          │
│         │                   │ 6. Return JWT     │                   │          │
│         │                   │◄──────────────────┤                   │          │
│         │                   │                   │                   │          │
│         │ 7. JWT Token      │                   │                   │          │
│         │◄──────────────────┤                   │                   │          │
│         │                   │                   │                   │          │
│         │ 8. API Request    │                   │                   │          │
│         │ with JWT Header   │                   │                   │          │
│         │──────────────────►│                   │                   │          │
│         │                   │                   │                   │          │
│         │                   │ 9. Validate JWT   │                   │          │
│         │                   │──────────────────►│                   │          │
│         │                   │                   │                   │          │
│         │                   │                   │ 10. Verify Token  │          │
│         │                   │                   │ & Check Permissions│         │
│         │                   │                   │◄──────────────────┤          │
│         │                   │                   │                   │          │
│         │                   │ 11. Authorized    │                   │          │
│         │                   │ Request           │                   │          │
│         │                   │◄──────────────────┤                   │          │
│         │                   │                   │                   │          │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### API Error Handling Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              API ERROR HANDLING FLOW                            │
│                                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐      │
│  │   Client    │    │   API       │    │   Error     │    │   Logging   │      │
│  │   Request   │    │   Gateway   │    │   Handler   │    │   Service   │      │
│  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘      │
│         │                   │                   │                   │          │
│         │ 1. API Request    │                   │                   │          │
│         │──────────────────►│                   │                   │          │
│         │                   │                   │                   │          │
│         │                   │ 2. Process Request│                   │          │
│         │                   │ (Error Occurs)    │                   │          │
│         │                   │──────────────────►│                   │          │
│         │                   │                   │                   │          │
│         │                   │                   │ 3. Error Analysis │          │
│         │                   │                   │ & Classification  │          │
│         │                   │                   │──────────────────►│          │
│         │                   │                   │                   │          │
│         │                   │                   │                   │ 4. Log   │
│         │                   │                   │                   │ Error    │
│         │                   │                   │                   │◄─────────┤
│         │                   │                   │                   │          │
│         │                   │                   │ 5. Format Error   │          │
│         │                   │                   │ Response          │          │
│         │                   │                   │◄──────────────────┤          │
│         │                   │                   │                   │          │
│         │                   │ 6. Return Error   │                   │          │
│         │                   │ Response          │                   │          │
│         │                   │◄──────────────────┤                   │          │
│         │                   │                   │                   │          │
│         │ 7. Error Response │                   │                   │          │
│         │◄──────────────────┤                   │                   │          │
│         │                   │                   │                   │          │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              ERROR CLASSIFICATION                            │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   4xx       │  │   5xx       │  │   Business  │  │   System    │        │ │
│  │  │   Client    │  │   Server    │  │   Logic     │  │   Errors    │        │ │
│  │  │   Errors    │  │   Errors    │  │   Errors    │  │             │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### API Rate Limiting Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              API RATE LIMITING ARCHITECTURE                     │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              RATE LIMITING LAYERS                           │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Global    │  │   User      │  │   IP        │  │   Endpoint  │        │ │
│  │  │   Limits    │  │   Limits    │  │   Limits    │  │   Limits    │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                             │
│                                    ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              RATE LIMITING FLOW                             │ │
│  │                                                                             │ │
│  │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │ │
│  │  │   Request   │    │   Rate      │    │   Token     │    │   Response  │  │ │
│  │  │   Arrives   │    │   Limiter   │    │   Bucket    │    │   Decision  │  │ │
│  │  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘  │ │
│  │         │                   │                   │                   │      │ │
│  │         │ 1. Check Limits   │                   │                   │      │ │
│  │         │──────────────────►│                   │                   │      │ │
│  │         │                   │                   │                   │      │ │
│  │         │                   │ 2. Token Available│                   │      │ │
│  │         │                   │──────────────────►│                   │      │ │
│  │         │                   │                   │                   │      │ │
│  │         │                   │                   │ 3. Consume Token │      │ │
│  │         │                   │                   │──────────────────►│      │ │
│  │         │                   │                   │                   │      │ │
│  │         │                   │                   │ 4. Allow Request │      │ │
│  │         │                   │                   │◄──────────────────┤      │ │
│  │         │                   │                   │                   │      │ │
│  │         │                   │ 5. Process Request│                   │      │ │
│  │         │                   │◄──────────────────┤                   │      │ │
│  │         │                   │                   │                   │      │ │
│  │         │ 6. Return Response│                   │                   │      │ │
│  │         │◄──────────────────┤                   │                   │      │ │
│  │         │                   │                   │                   │      │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              RATE LIMIT CONFIGURATION                        │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   GET       │  │   POST      │  │   PUT       │  │   DELETE    │        │ │
│  │  │   100/min   │  │   20/min    │  │   20/min    │  │   10/min    │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### API Monitoring Dashboard

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              API MONITORING DASHBOARD                           │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              REAL-TIME METRICS                              │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Request   │  │   Response  │  │   Error     │  │   Active    │        │ │
│  │  │   Rate      │  │   Time      │  │   Rate      │  │   Users     │        │ │
│  │  │   1,250/min │  │   150ms     │  │   0.5%      │  │   45        │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              ENDPOINT PERFORMANCE                           │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   GET       │  │   POST      │  │   PUT       │  │   DELETE    │        │ │
│  │  │   /cameras  │  │   /cameras  │  │   /cameras  │  │   /cameras  │        │ │
│  │  │   850/min   │  │   120/min   │  │   80/min    │  │   40/min    │        │ │
│  │  │   120ms     │  │   200ms     │  │   180ms     │  │   150ms     │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              SYSTEM HEALTH                                   │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   CPU       │  │   Memory    │  │   Network   │  │   Database  │        │ │
│  │  │   45%       │  │   67%       │  │   2.5 Mbps  │  │   95%       │        │ │
│  │  │   Normal    │  │   Normal    │  │   Normal    │  │   Normal    │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              ALERTS & NOTIFICATIONS                         │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   High      │  │   Rate      │  │   Error     │  │   Security  │        │ │
│  │  │   Latency   │  │   Limit     │  │   Spike     │  │   Alert     │        │ │
│  │  │   Alert     │  │   Exceeded  │  │   Detected  │  │   Triggered │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 🔗 Base URL

```
Production: https://api.camera-system.com/v1
Development: http://localhost:8000/v1
```

## 🔐 Authentication

Tất cả API endpoints yêu cầu JWT token trong header:

```
Authorization: Bearer <jwt_token>
```

## 📋 API Endpoints

### 1. Camera Management

#### 1.1 Get All Cameras

**Endpoint:** `GET /api/v1/cameras`

**Description:** Lấy danh sách tất cả cameras

**Query Parameters:**
- `status` (optional): Filter theo status (online, offline, error)
- `location` (optional): Filter theo location
- `page` (optional): Page number (default: 1)
- `limit` (optional): Items per page (default: 20)

**Response:**
```json
{
  "success": true,
  "data": {
    "cameras": [
      {
        "id": 1,
        "name": "Main Entrance",
        "location": "Building A - Floor 1",
        "description": "Camera monitoring main entrance",
        "stream_url": "rtsp://192.168.1.100:554/stream",
        "stream_type": "rtsp",
        "status": "online",
        "worker_id": "worker-1",
        "settings": {
          "detection_sensitivity": 0.8,
          "max_occupancy": 50,
          "counting_zones": [
            {"x": 100, "y": 200, "width": 300, "height": 100}
          ]
        },
        "metadata": {
          "manufacturer": "Hikvision",
          "model": "DS-2CD2142FWD-I",
          "resolution": "1920x1080"
        },
        "current_count": 15,
        "created_at": "2024-01-15T10:30:00Z",
        "updated_at": "2024-01-15T10:30:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 50,
      "pages": 3
    }
  }
}
```

#### 1.2 Get Camera by ID

**Endpoint:** `GET /api/v1/cameras/{id}`

**Description:** Lấy thông tin chi tiết của camera

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "Main Entrance",
    "location": "Building A - Floor 1",
    "description": "Camera monitoring main entrance",
    "stream_url": "rtsp://192.168.1.100:554/stream",
    "stream_type": "rtsp",
    "status": "online",
    "worker_id": "worker-1",
    "settings": {
      "detection_sensitivity": 0.8,
      "max_occupancy": 50,
      "counting_zones": [
        {"x": 100, "y": 200, "width": 300, "height": 100}
      ],
      "alert_threshold": 40,
      "notification_enabled": true
    },
    "metadata": {
      "manufacturer": "Hikvision",
      "model": "DS-2CD2142FWD-I",
      "resolution": "1920x1080",
      "fps": 25,
      "bitrate": "2048kbps"
    },
    "security_config": {
      "encryption_enabled": true,
      "access_control": ["user1", "user2"],
      "ip_whitelist": ["192.168.1.0/24"]
    },
    "current_count": 15,
    "last_activity": "2024-01-15T10:30:00Z",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
}
```

#### 1.3 Add New Camera

**Endpoint:** `POST /api/v1/cameras`

**Description:** Thêm camera mới vào hệ thống

**Request Body:**
```json
{
  "name": "New Camera",
  "location": "Building B - Floor 2",
  "description": "Camera for monitoring lobby",
  "stream_url": "rtsp://192.168.1.101:554/stream",
  "stream_type": "rtsp",
  "settings": {
    "detection_sensitivity": 0.8,
    "max_occupancy": 30,
    "counting_zones": [
      {"x": 50, "y": 100, "width": 200, "height": 80}
    ],
    "alert_threshold": 25,
    "notification_enabled": true
  },
  "metadata": {
    "manufacturer": "Dahua",
    "model": "IPC-HDW4431C-A",
    "resolution": "1920x1080"
  },
  "security_config": {
    "encryption_enabled": true,
    "access_control": ["admin"],
    "ip_whitelist": ["192.168.1.0/24"]
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 2,
    "name": "New Camera",
    "status": "offline",
    "message": "Camera added successfully. Processing will start automatically."
  }
}
```

#### 1.4 Update Camera

**Endpoint:** `PUT /api/v1/cameras/{id}`

**Description:** Cập nhật thông tin camera

**Request Body:** (Tương tự như Add Camera, nhưng chỉ cần gửi các field cần update)

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "message": "Camera updated successfully"
  }
}
```

#### 1.5 Delete Camera

**Endpoint:** `DELETE /api/v1/cameras/{id}`

**Description:** Xóa camera khỏi hệ thống

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "message": "Camera deleted successfully"
  }
}
```

### 2. Camera Control

#### 2.1 Start Camera Processing

**Endpoint:** `POST /api/v1/cameras/{id}/start`

**Description:** Bắt đầu xử lý camera stream

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "status": "online",
    "worker_id": "worker-1",
    "message": "Camera processing started successfully"
  }
}
```

#### 2.2 Stop Camera Processing

**Endpoint:** `POST /api/v1/cameras/{id}/stop`

**Description:** Dừng xử lý camera stream

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "status": "offline",
    "message": "Camera processing stopped successfully"
  }
}
```

#### 2.3 Restart Camera Processing

**Endpoint:** `POST /api/v1/cameras/{id}/restart`

**Description:** Khởi động lại xử lý camera stream

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "status": "online",
    "worker_id": "worker-2",
    "message": "Camera processing restarted successfully"
  }
}
```

### 3. Camera Settings

#### 3.1 Update Camera Settings

**Endpoint:** `PUT /api/v1/cameras/{id}/settings`

**Description:** Cập nhật cài đặt camera

**Request Body:**
```json
{
  "detection_sensitivity": 0.9,
  "max_occupancy": 40,
  "counting_zones": [
    {"x": 100, "y": 200, "width": 300, "height": 100},
    {"x": 400, "y": 200, "width": 200, "height": 100}
  ],
  "alert_threshold": 35,
  "notification_enabled": true
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "message": "Camera settings updated successfully"
  }
}
```

#### 3.2 Get Camera Settings

**Endpoint:** `GET /api/v1/cameras/{id}/settings`

**Description:** Lấy cài đặt camera

**Response:**
```json
{
  "success": true,
  "data": {
    "detection_sensitivity": 0.8,
    "max_occupancy": 50,
    "counting_zones": [
      {"x": 100, "y": 200, "width": 300, "height": 100}
    ],
    "alert_threshold": 40,
    "notification_enabled": true,
    "ai_model_id": 1,
    "processing_fps": 25,
    "quality_threshold": 0.7
  }
}
```

### 4. Camera Health & Status

#### 4.1 Get Camera Health

**Endpoint:** `GET /api/v1/cameras/{id}/health`

**Description:** Lấy thông tin sức khỏe camera

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "status": "online",
    "health_score": 95,
    "last_heartbeat": "2024-01-15T10:30:00Z",
    "uptime": "24h 30m 15s",
    "error_count": 0,
    "performance_metrics": {
      "fps": 25,
      "latency": 150,
      "accuracy": 92.5,
      "cpu_usage": 45.2,
      "memory_usage": 67.8
    }
  }
}
```

#### 4.2 Get Camera Status

**Endpoint:** `GET /api/v1/cameras/{id}/status`

**Description:** Lấy trạng thái camera

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "status": "online",
    "worker_id": "worker-1",
    "current_count": 15,
    "last_activity": "2024-01-15T10:30:00Z",
    "processing_status": "active",
    "stream_quality": "good",
    "ai_model_status": "loaded"
  }
}
```

### 5. Camera Analytics

#### 5.1 Get Camera Analytics

**Endpoint:** `GET /api/v1/cameras/{id}/analytics`

**Description:** Lấy analytics data của camera

**Query Parameters:**
- `period` (optional): Time period (hourly, daily, weekly, monthly)
- `start_date` (optional): Start date (ISO format)
- `end_date` (optional): End date (ISO format)

**Response:**
```json
{
  "success": true,
  "data": {
    "camera_id": 1,
    "period": "daily",
    "start_date": "2024-01-15",
    "end_date": "2024-01-15",
    "analytics": {
      "total_people_count": 1250,
      "total_people_in": 680,
      "total_people_out": 570,
      "peak_hour": "14:00",
      "peak_count": 45,
      "avg_confidence": 92.5,
      "uptime_percentage": 99.8,
      "error_rate": 0.2
    },
    "hourly_data": [
      {
        "hour": "00:00",
        "people_count": 5,
        "people_in": 3,
        "people_out": 2
      }
    ]
  }
}
```

#### 5.2 Get Camera Performance Metrics

**Endpoint:** `GET /api/v1/cameras/{id}/performance`

**Description:** Lấy performance metrics của camera

**Response:**
```json
{
  "success": true,
  "data": {
    "camera_id": 1,
    "metrics": {
      "processing_latency": 150,
      "detection_accuracy": 92.5,
      "false_positive_rate": 2.1,
      "false_negative_rate": 1.8,
      "fps": 25,
      "cpu_usage": 45.2,
      "memory_usage": 67.8,
      "network_bandwidth": "2.5 Mbps"
    },
    "trends": {
      "latency_trend": "stable",
      "accuracy_trend": "improving",
      "performance_score": 88.5
    }
  }
}
```

## 🔧 Error Handling

### Error Response Format

```json
{
  "success": false,
  "error": {
    "code": "CAMERA_NOT_FOUND",
    "message": "Camera with ID 123 not found",
    "details": {
      "camera_id": 123,
      "timestamp": "2024-01-15T10:30:00Z"
    }
  }
}
```

### Common Error Codes

| Code | Description | HTTP Status |
|------|-------------|-------------|
| `CAMERA_NOT_FOUND` | Camera không tồn tại | 404 |
| `CAMERA_ALREADY_EXISTS` | Camera đã tồn tại | 409 |
| `INVALID_STREAM_URL` | Stream URL không hợp lệ | 400 |
| `STREAM_CONNECTION_FAILED` | Không thể kết nối stream | 503 |
| `WORKER_NOT_AVAILABLE` | Không có worker available | 503 |
| `INVALID_SETTINGS` | Cài đặt không hợp lệ | 400 |
| `PERMISSION_DENIED` | Không có quyền truy cập | 403 |
| `INTERNAL_ERROR` | Lỗi hệ thống | 500 |

## 📊 Rate Limiting

### Rate Limits
- **GET requests**: 100 requests/minute
- **POST requests**: 20 requests/minute
- **PUT requests**: 20 requests/minute
- **DELETE requests**: 10 requests/minute

### Rate Limit Headers
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1642234567
```

## 🔐 Security Headers

### Required Headers
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
X-Request-ID: <unique_request_id>
```

### Response Headers
```
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000; includeSubDomains
```

## 📋 Pagination

### Pagination Parameters
- `page`: Page number (default: 1)
- `limit`: Items per page (default: 20, max: 100)

### Pagination Response
```json
{
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 150,
    "pages": 8,
    "has_next": true,
    "has_prev": false
  }
}
```

## 📝 Data Validation

### Camera Name
- Required: Yes
- Type: String
- Length: 1-100 characters
- Pattern: Alphanumeric, spaces, hyphens, underscores

### Stream URL
- Required: Yes
- Type: String
- Pattern: Valid RTSP/RTMP URL
- Max length: 500 characters

### Detection Sensitivity
- Required: No
- Type: Number
- Range: 0.1 - 1.0
- Default: 0.8

### Max Occupancy
- Required: No
- Type: Integer
- Range: 1 - 1000
- Default: 50

---

**Tài liệu này cung cấp đặc tả đầy đủ cho Camera Management API, bao gồm endpoints, request/response formats, error handling, và security considerations.** 