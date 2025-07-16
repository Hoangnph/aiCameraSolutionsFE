# Camera Management API (beCamera) - Test Cases
## Workflow 2: Camera Management & Analytics

### 📋 **WORKFLOW OVERVIEW**

**Service**: Python FastAPI Camera Management Service  
**Port**: 3002  
**Database**: PostgreSQL (shared with beAuth)  
**Cache**: Redis (dedicated for beCamera)  
**Authentication**: JWT (via beAuth service)  
**AI Processing**: OpenCV + Worker Pool  

#### **Workflow Diagram**
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Client        │───▶│  FastAPI        │───▶│  Authentication │
│   Request       │    │  Endpoints      │    │  (beAuth)       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Camera CRUD    │    │  Worker Pool    │    │  Analytics      │
│  Operations     │    │  Management     │    │  Processing     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Database       │    │  AI Processing  │    │  Real-time      │
│  (PostgreSQL)   │    │  (OpenCV)       │    │  Updates        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

#### **Key Features**
- Full CRUD operations for cameras
- Real-time people counting with AI
- Worker pool for concurrent processing
- Analytics and reporting
- JWT authentication integration
- Health monitoring

---

### 🧪 **TEST CASE 2.1: Camera CRUD Operations**

#### **Test Case ID**: `CAM-CRUD-001`
#### **Test Case Name**: Create New Camera
#### **Priority**: High
#### **Test Type**: Positive

**Preconditions**:
- Valid JWT token from beAuth service
- Database is accessible
- Service is running on port 3002

**Headers**:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json
```

**Test Data**:
```json
{
  "name": "Main Entrance Camera",
  "location": "Building A - Main Entrance",
  "stream_url": "rtsp://192.168.1.100:554/stream1",
  "status": "active"
}
```

**Test Steps**:
1. Send POST request to `/api/v1/cameras`
2. Include test data in request body
3. Verify response

**Expected Results**:
- **Status Code**: 201 Created
- **Response Body**:
```json
{
  "success": true,
  "data": {
    "camera": {
      "id": 1,
      "name": "Main Entrance Camera",
      "location": "Building A - Main Entrance",
      "stream_url": "rtsp://192.168.1.100:554/stream1",
      "status": "active",
      "created_at": "2024-01-15T10:30:00Z"
    }
  }
}
```
- **Database**: Camera record created in `cameras` table
- **Logs**: Camera creation logged

---

#### **Test Case ID**: `CAM-CRUD-002`
#### **Test Case Name**: Get All Cameras
#### **Priority**: High
#### **Test Type**: Positive

**Headers**:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Expected Results**:
- **Status Code**: 200 OK
- **Response Body**:
```json
{
  "success": true,
  "data": {
    "cameras": [
      {
        "id": 1,
        "name": "Main Entrance Camera",
        "location": "Building A - Main Entrance",
        "stream_url": "rtsp://192.168.1.100:554/stream1",
        "status": "active",
        "created_at": "2024-01-15T10:30:00Z"
      }
    ],
    "count": 1
  }
}
```

---

#### **Test Case ID**: `CAM-CRUD-003`
#### **Test Case Name**: Get Camera by ID
#### **Priority**: High
#### **Test Type**: Positive

**Preconditions**: Camera with ID 1 exists

**Headers**:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Expected Results**:
- **Status Code**: 200 OK
- **Response Body**:
```json
{
  "success": true,
  "data": {
    "camera": {
      "id": 1,
      "name": "Main Entrance Camera",
      "location": "Building A - Main Entrance",
      "stream_url": "rtsp://192.168.1.100:554/stream1",
      "status": "active",
      "created_at": "2024-01-15T10:30:00Z"
    }
  }
}
```

---

#### **Test Case ID**: `CAM-CRUD-004`
#### **Test Case Name**: Update Camera
#### **Priority**: Medium
#### **Test Type**: Positive

**Preconditions**: Camera with ID 1 exists

**Headers**:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json
```

**Test Data**:
```json
{
  "name": "Updated Main Entrance Camera",
  "location": "Building A - Updated Location",
  "stream_url": "rtsp://192.168.1.100:554/stream2"
}
```

**Expected Results**:
- **Status Code**: 200 OK
- **Response Body**: Updated camera data
- **Database**: Camera fields updated

---

#### **Test Case ID**: `CAM-CRUD-005`
#### **Test Case Name**: Delete Camera
#### **Priority**: Medium
#### **Test Type**: Positive

**Preconditions**: Camera with ID 1 exists

**Headers**:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Expected Results**:
- **Status Code**: 200 OK
- **Response Body**:
```json
{
  "success": true,
  "message": "Camera deleted successfully"
}
```
- **Database**: Camera record deleted

---

### 🧪 **TEST CASE 2.2: Camera Status Management**

#### **Test Case ID**: `CAM-STATUS-001`
#### **Test Case Name**: Update Camera Status
#### **Priority**: High
#### **Test Type**: Positive

**Preconditions**: Camera with ID 1 exists

**Headers**:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json
```

**Test Data**:
```json
{
  "status": "maintenance"
}
```

**Expected Results**:
- **Status Code**: 200 OK
- **Response Body**:
```json
{
  "success": true,
  "data": {
    "camera": {
      "id": 1,
      "name": "Main Entrance Camera",
      "status": "maintenance",
      "updated_at": "2024-01-15T10:35:00Z"
    }
  }
}
```

---

#### **Test Case ID**: `CAM-STATUS-002`
#### **Test Case Name**: Invalid Status Update
#### **Priority**: Medium
#### **Test Type**: Negative

**Test Data**:
```json
{
  "status": "invalid_status"
}
```

**Expected Results**:
- **Status Code**: 400 Bad Request
- **Response Body**: Status validation error

---

### 🧪 **TEST CASE 2.3: Worker Pool Management**

#### **Test Case ID**: `CAM-WORKER-001`
#### **Test Case Name**: Start Camera Processing
#### **Priority**: High
#### **Test Type**: Positive

**Preconditions**: Camera with ID 1 exists and is active

**Headers**:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Expected Results**:
- **Status Code**: 200 OK
- **Response Body**:
```json
{
  "success": true,
  "data": {
    "camera_id": 1,
    "status": "processing",
    "worker_id": "worker_1",
    "message": "Camera processing started"
  }
}
```
- **Worker Pool**: Camera assigned to available worker
- **Logs**: Processing start logged

---

#### **Test Case ID**: `CAM-WORKER-002`
#### **Test Case Name**: Stop Camera Processing
#### **Priority**: High
#### **Test Type**: Positive

**Preconditions**: Camera with ID 1 is being processed

**Headers**:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Expected Results**:
- **Status Code**: 200 OK
- **Response Body**:
```json
{
  "success": true,
  "data": {
    "camera_id": 1,
    "status": "stopped",
    "message": "Camera processing stopped"
  }
}
```
- **Worker Pool**: Camera task removed from worker
- **Logs**: Processing stop logged

---

#### **Test Case ID**: `CAM-WORKER-003`
#### **Test Case Name**: Get Worker Pool Status
#### **Priority**: Medium
#### **Test Type**: Positive

**Headers**:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Expected Results**:
- **Status Code**: 200 OK
- **Response Body**:
```json
{
  "success": true,
  "data": {
    "workers": [
      {
        "worker_id": "worker_1",
        "status": "busy",
        "current_task": 1,
        "start_time": "2024-01-15T10:30:00Z",
        "processed_frames": 150,
        "error_count": 0
      },
      {
        "worker_id": "worker_2",
        "status": "idle",
        "current_task": null,
        "start_time": null,
        "processed_frames": 0,
        "error_count": 0
      }
    ],
    "total_workers": 4,
    "idle_workers": 3,
    "busy_workers": 1
  }
}
```

---

### 🧪 **TEST CASE 2.4: Analytics & Reporting**

#### **Test Case ID**: `CAM-ANALYTICS-001`
#### **Test Case Name**: Get Count Data
#### **Priority**: High
#### **Test Type**: Positive

**Headers**:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Query Parameters**:
```
camera_id=1&limit=10
```

**Expected Results**:
- **Status Code**: 200 OK
- **Response Body**:
```json
{
  "success": true,
  "data": {
    "counts": [
      {
        "id": 1,
        "camera_id": 1,
        "people_in": 25,
        "people_out": 18,
        "current_count": 7,
        "confidence": 0.92,
        "timestamp": "2024-01-15T10:30:00Z"
      }
    ],
    "count": 1
  }
}
```

---

#### **Test Case ID**: `CAM-ANALYTICS-002`
#### **Test Case Name**: Get Analytics Summary
#### **Priority**: High
#### **Test Type**: Positive

**Headers**:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Expected Results**:
- **Status Code**: 200 OK
- **Response Body**:
```json
{
  "success": true,
  "data": {
    "total_cameras": 3,
    "active_cameras": 2,
    "offline_cameras": 1,
    "today_in": 150,
    "today_out": 120,
    "current_count": 30,
    "total_confidence": 0.89
  }
}
```

---

### 🧪 **TEST CASE 2.5: Authentication & Authorization**

#### **Test Case ID**: `CAM-AUTH-001`
#### **Test Case Name**: Access Without Token
#### **Priority**: High
#### **Test Type**: Security

**Test Steps**:
1. Send GET request to `/api/v1/cameras` without Authorization header
2. Verify authentication error

**Expected Results**:
- **Status Code**: 401 Unauthorized
- **Response Body**:
```json
{
  "detail": "Not authenticated"
}
```

---

#### **Test Case ID**: `CAM-AUTH-002`
#### **Test Case Name**: Access with Invalid Token
#### **Priority**: High
#### **Test Type**: Security

**Headers**:
```
Authorization: Bearer invalid_token_here
```

**Expected Results**:
- **Status Code**: 401 Unauthorized
- **Response Body**:
```json
{
  "detail": "Invalid token"
}
```

---

### 🧪 **TEST CASE 2.6: Error Handling**

#### **Test Case ID**: `CAM-ERR-001`
#### **Test Case Name**: Camera Not Found
#### **Priority**: Medium
#### **Test Type**: Error Handling

**Preconditions**: Camera with ID 999 does not exist

**Headers**:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Expected Results**:
- **Status Code**: 404 Not Found
- **Response Body**:
```json
{
  "success": false,
  "error": {
    "code": 404,
    "message": "Camera not found"
  }
}
```

---

#### **Test Case ID**: `CAM-ERR-002`
#### **Test Case Name**: Database Connection Error
#### **Priority**: Medium
#### **Test Type**: Error Handling

**Test Steps**:
1. Stop PostgreSQL service
2. Send camera request
3. Verify error handling

**Expected Results**:
- **Status Code**: 500 Internal Server Error
- **Response Body**: Database connection error message
- **Logs**: Error logged with details

---

### 🧪 **TEST CASE 2.7: Performance & Load Testing**

#### **Test Case ID**: `CAM-PERF-001`
#### **Test Case Name**: Response Time Test
#### **Priority**: Medium
#### **Test Type**: Performance

**Test Steps**:
1. Send 100 concurrent requests to `/api/v1/cameras`
2. Measure response times
3. Verify performance metrics

**Expected Results**:
- **Average Response Time**: < 200ms
- **95th Percentile**: < 500ms
- **Error Rate**: < 1%
- **Throughput**: > 100 requests/second

---

#### **Test Case ID**: `CAM-PERF-002`
#### **Test Case Name**: Worker Pool Load Test
#### **Priority**: Medium
#### **Test Type**: Performance

**Test Steps**:
1. Start processing on 4 cameras simultaneously
2. Monitor worker pool performance
3. Verify no worker crashes

**Expected Results**:
- **All Workers**: Remain stable under load
- **Processing**: Continues without interruption
- **Memory Usage**: Remains within limits
- **CPU Usage**: Efficient utilization

---

### 📊 **TEST EXECUTION MATRIX**

| Test Case | Priority | Status | Executed By | Date | Notes |
|-----------|----------|--------|-------------|------|-------|
| CAM-CRUD-001 | High | 🔄 | | | |
| CAM-CRUD-002 | High | 🔄 | | | |
| CAM-CRUD-003 | High | 🔄 | | | |
| CAM-CRUD-004 | Medium | 🔄 | | | |
| CAM-CRUD-005 | Medium | 🔄 | | | |
| CAM-STATUS-001 | High | 🔄 | | | |
| CAM-STATUS-002 | Medium | 🔄 | | | |
| CAM-WORKER-001 | High | 🔄 | | | |
| CAM-WORKER-002 | High | 🔄 | | | |
| CAM-WORKER-003 | Medium | 🔄 | | | |
| CAM-ANALYTICS-001 | High | 🔄 | | | |
| CAM-ANALYTICS-002 | High | 🔄 | | | |
| CAM-AUTH-001 | High | 🔄 | | | |
| CAM-AUTH-002 | High | 🔄 | | | |
| CAM-ERR-001 | Medium | 🔄 | | | |
| CAM-ERR-002 | Medium | 🔄 | | | |
| CAM-PERF-001 | Medium | 🔄 | | | |
| CAM-PERF-002 | Medium | 🔄 | | | |

### 🎯 **ACCEPTANCE CRITERIA**

- ✅ All CRUD operations work correctly
- ✅ Worker pool manages camera processing efficiently
- ✅ Analytics provide accurate data
- ✅ Authentication integration works properly
- ✅ Error handling provides meaningful messages
- ✅ Performance meets requirements (< 200ms response time)
- ✅ Worker pool handles concurrent processing
- ✅ Database operations are atomic and consistent

### 📝 **NOTES**

- All test cases require valid JWT token from beAuth service
- Worker pool tests should be run in isolated environment
- Performance tests should use realistic load patterns
- Database should be reset between test runs
- AI processing simulation should be consistent
- Monitor system resources during load tests 

### Test Case: Missing AUTH_SERVICE_URL (Regression)
- **Precondition:** beCamera container chạy nhưng thiếu biến môi trường AUTH_SERVICE_URL
- **Step:** Gửi request GET /api/v1/cameras với accessToken hợp lệ
- **Expected:** API trả về 503 Service Unavailable, log backend báo không kết nối được beAuth

### Test Case: Correct AUTH_SERVICE_URL (Happy Path)
- **Precondition:** beCamera container có biến môi trường AUTH_SERVICE_URL=http://ai_camera_beauth:3001
- **Step:** Gửi request GET /api/v1/cameras với accessToken hợp lệ
- **Expected:** API trả về 200, trả về danh sách camera đúng

### Troubleshooting
- Nếu gặp lỗi 503 khi đã login, kiểm tra biến môi trường AUTH_SERVICE_URL trong container:
  - `docker exec ai_camera_becamera env | grep AUTH_SERVICE_URL`
- Nếu thiếu, hãy thêm vào docker-compose.yml và rebuild container:
  - `docker-compose up -d --build becamera` 