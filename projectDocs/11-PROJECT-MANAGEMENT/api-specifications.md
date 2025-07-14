# API Specifications - AI Camera Counting System

## 📊 Tổng quan
Tài liệu này định nghĩa các API endpoints cho hệ thống AI Camera Counting, bao gồm beAuth (Authentication) và beCamera (Camera Processing) services.

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │  beAuth API     │    │  beCamera API   │
│   (React)       │◄──►│   (Port 3001)   │    │   (Port 3002)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │              ┌─────────────────┐              │
         └──────────────►│   PostgreSQL    │◄─────────────┘
                        │   (Port 5432)   │
                        └─────────────────┘
```

## 🔐 beAuth API (Authentication Service)

### Base URL
```
http://localhost:3001/api/v1
```

### Authentication Endpoints

#### 1. User Registration
```http
POST /auth/register
Content-Type: application/json

{
  "username": "string",
  "email": "string",
  "password": "string",
  "first_name": "string",
  "last_name": "string",
  "registration_code": "string"
}
```

**Response (Success - 201)**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": 1,
      "username": "john_doe",
      "email": "john@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "role": "user",
      "is_active": true,
      "created_at": "2025-07-03T10:00:00Z"
    },
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  },
  "message": "User registered successfully"
}
```

**Response (Error - 400)**
```json
{
  "success": false,
  "error": "Validation error",
  "details": {
    "email": "Email is required",
    "password": "Password must be at least 8 characters"
  }
}
```

#### 2. User Login
```http
POST /auth/login
Content-Type: application/json

{
  "email": "string",
  "password": "string"
}
```

**Response (Success - 200)**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": 1,
      "username": "john_doe",
      "email": "john@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "role": "user",
      "is_active": true,
      "last_login": "2025-07-03T10:00:00Z"
    },
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

#### 3. Token Refresh
```http
POST /auth/refresh
Content-Type: application/json

{
  "refreshToken": "string"
}
```

**Response (Success - 200)**
```json
{
  "success": true,
  "data": {
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

#### 4. Get Current User
```http
GET /auth/me
Authorization: Bearer <access_token>
```

**Response (Success - 200)**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": 1,
      "username": "john_doe",
      "email": "john@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "role": "user",
      "is_active": true,
      "last_login": "2025-07-03T10:00:00Z",
      "created_at": "2025-07-01T10:00:00Z"
    }
  }
}
```

#### 5. User Logout
```http
POST /auth/logout
Authorization: Bearer <access_token>
```

**Response (Success - 200)**
```json
{
  "success": true,
  "message": "Logged out successfully"
}
```

### User Management Endpoints

#### 1. Update User Profile
```http
PUT /users/profile
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "first_name": "string",
  "last_name": "string",
  "email": "string"
}
```

#### 2. Change Password
```http
PUT /users/change-password
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "current_password": "string",
  "new_password": "string",
  "confirm_password": "string"
}
```

#### 3. Get All Users (Admin Only)
```http
GET /users?page=1&limit=10&search=john
Authorization: Bearer <access_token>
```

**Response (Success - 200)**
```json
{
  "success": true,
  "data": {
    "users": [
      {
        "id": 1,
        "username": "john_doe",
        "email": "john@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "role": "user",
        "is_active": true,
        "last_login": "2025-07-03T10:00:00Z",
        "created_at": "2025-07-01T10:00:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 10,
      "total": 25,
      "total_pages": 3
    }
  }
}
```

### System Endpoints

#### Health Check
```http
GET /health
```

**Response (Success - 200)**
```json
{
  "status": "OK",
  "timestamp": "2025-07-03T10:00:00Z",
  "service": "Authentication Service",
  "version": "1.0.0"
}
```

## 📹 beCamera API (Camera Processing Service)

### Base URL
```
http://localhost:3002/api/v1
```

### Camera Management Endpoints

#### 1. Get All Cameras
```http
GET /cameras?page=1&limit=10&status=active
Authorization: Bearer <access_token>
```

**Response (Success - 200)**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "Main Entrance Camera",
      "location": "Building A - Main Entrance",
      "stream_url": "rtsp://camera1.example.com/stream1",
      "status": "active",
      "created_at": "2025-07-01T10:00:00Z",
      "updated_at": "2025-07-03T10:00:00Z"
    }
  ],
  "count": 1
}
```

#### 2. Create Camera
```http
POST /cameras
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "name": "string",
  "location": "string",
  "stream_url": "string",
  "status": "offline"
}
```

**Response (Success - 201)**
```json
{
  "success": true,
  "data": {
    "id": 2,
    "name": "New Camera",
    "location": "Building B - Entrance",
    "stream_url": "rtsp://camera2.example.com/stream1",
    "status": "offline",
    "created_at": "2025-07-03T10:00:00Z"
  },
  "message": "Camera created successfully"
}
```

#### 3. Get Camera by ID
```http
GET /cameras/{id}
Authorization: Bearer <access_token>
```

#### 4. Update Camera
```http
PUT /cameras/{id}
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "name": "string",
  "location": "string",
  "stream_url": "string",
  "status": "active"
}
```

#### 5. Delete Camera
```http
DELETE /cameras/{id}
Authorization: Bearer <access_token>
```

### Count Data Endpoints

#### 1. Get Count Data
```http
GET /counts?camera_id=1&limit=100&start_date=2025-07-01&end_date=2025-07-03
Authorization: Bearer <access_token>
```

**Response (Success - 200)**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "camera_id": 1,
      "people_in": 25,
      "people_out": 18,
      "current_count": 7,
      "confidence": 0.92,
      "timestamp": "2025-07-03T10:00:00Z"
    }
  ],
  "count": 1
}
```

#### 2. Get Real-time Count
```http
GET /counts/realtime?camera_id=1
Authorization: Bearer <access_token>
```

**Response (Success - 200)**
```json
{
  "success": true,
  "data": {
    "camera_id": 1,
    "people_in": 25,
    "people_out": 18,
    "current_count": 7,
    "confidence": 0.92,
    "timestamp": "2025-07-03T10:00:00Z",
    "is_live": true
  }
}
```

### Analytics Endpoints

#### 1. Get Analytics Summary
```http
GET /analytics/summary?date=2025-07-03
Authorization: Bearer <access_token>
```

**Response (Success - 200)**
```json
{
  "success": true,
  "data": {
    "total_cameras": 5,
    "active_cameras": 3,
    "today_in": 150,
    "today_out": 120,
    "current_count": 30,
    "peak_hour": "09:00-10:00",
    "peak_count": 45
  }
}
```

#### 2. Get Hourly Analytics
```http
GET /analytics/hourly?date=2025-07-03&camera_id=1
Authorization: Bearer <access_token>
```

**Response (Success - 200)**
```json
{
  "success": true,
  "data": [
    {
      "hour": "09:00",
      "people_in": 25,
      "people_out": 18,
      "current_count": 7
    },
    {
      "hour": "10:00",
      "people_in": 30,
      "people_out": 22,
      "current_count": 15
    }
  ]
}
```

### System Endpoints

#### Health Check
```http
GET /health
```

**Response (Success - 200)**
```json
{
  "status": "healthy",
  "timestamp": "2025-07-03T10:00:00Z",
  "service": "ai-camera-counting",
  "database": "connected",
  "redis": "connected"
}
```

## 🔒 Authentication & Authorization

### JWT Token Structure
```json
{
  "header": {
    "alg": "HS256",
    "typ": "JWT"
  },
  "payload": {
    "user_id": 1,
    "email": "john@example.com",
    "role": "user",
    "iat": 1640995200,
    "exp": 1640998800
  }
}
```

### Authorization Headers
```http
Authorization: Bearer <access_token>
```

### Role-based Access Control
- **user**: Basic access to own data and camera viewing
- **admin**: Full access to all features and user management
- **viewer**: Read-only access to camera data

## 📊 Error Handling

### Standard Error Response Format
```json
{
  "success": false,
  "error": "Error message",
  "status": 400,
  "timestamp": "2025-07-03T10:00:00Z",
  "path": "/api/v1/cameras",
  "details": {
    "field": "validation error"
  }
}
```

### Common HTTP Status Codes
- **200**: Success
- **201**: Created
- **400**: Bad Request
- **401**: Unauthorized
- **403**: Forbidden
- **404**: Not Found
- **422**: Validation Error
- **500**: Internal Server Error

### Validation Error Example
```json
{
  "success": false,
  "error": "Validation failed",
  "status": 422,
  "details": {
    "email": "Invalid email format",
    "password": "Password must be at least 8 characters"
  }
}
```

## 🔄 Rate Limiting

### Default Limits
- **Authentication endpoints**: 5 requests per minute
- **API endpoints**: 100 requests per minute
- **File uploads**: 10 requests per minute

### Rate Limit Headers
```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640998800
```

## 📝 API Versioning

### Current Version
- **Version**: v1
- **Base URL**: `/api/v1`
- **Status**: Stable

### Versioning Strategy
- URL-based versioning: `/api/v1/`, `/api/v2/`
- Backward compatibility maintained for 6 months
- Deprecation notices in response headers

## 🧪 Testing Endpoints

### Test Authentication
```bash
# Register user
curl -X POST http://localhost:3001/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"password123","first_name":"Test","last_name":"User"}'

# Login
curl -X POST http://localhost:3001/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'

# Get cameras
curl -X GET http://localhost:3002/api/v1/cameras \
  -H "Authorization: Bearer <access_token>"
```

---

**Last Updated**: 2025-07-03  
**Version**: 1.0.0  
**Status**: Ready for Implementation 