# API Reference Documentation
## AI Camera Counting System

### 📊 Tổng quan

Tài liệu này cung cấp thông tin chi tiết về tất cả API endpoints của hệ thống AI Camera Counting, bao gồm authentication, camera management, analytics, và error handling.

**🟢 Status: READY FOR FRONTEND INTEGRATION**

### 🔐 Authentication

#### Base URL
- **beAuth Service**: `http://localhost:3001`
- **beCamera Service**: `http://localhost:3002`

#### Authentication Flow
1. Register user → Get JWT token
2. Login user → Get JWT token
3. Use JWT token in Authorization header for protected endpoints

---

## 🔐 Authentication API (beAuth Service)

### POST /api/v1/auth/register
**Register a new user**

#### Request Body
```json
{
  "username": "user123",
  "email": "user@example.com",
  "password": "Password123!",
  "confirmPassword": "Password123!",
  "firstName": "John",
  "lastName": "Doe",
  "registrationCode": "REG001"
}
```

#### Response (201 Created)
```json
{
  "success": true,
  "data": {
    "user": {
      "id": 1,
      "username": "user123",
      "email": "user@example.com",
      "firstName": "John",
      "lastName": "Doe",
      "role": "user",
      "createdAt": "2024-07-11T16:30:00.000Z"
    },
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  },
  "message": "User registered successfully"
}
```

#### Error Responses
```json
// 400 Bad Request - Invalid data
{
  "success": false,
  "error": "Invalid registration data",
  "details": ["Username is required", "Email format is invalid"]
}

// 400 Bad Request - Invalid registration code
{
  "success": false,
  "error": "Invalid registration code"
}

// 409 Conflict - Username already exists
{
  "success": false,
  "error": "Username already exists"
}
```

---

### POST /api/v1/auth/login
**Login user**

#### Request Body
```json
{
  "username": "user123",
  "password": "Password123!"
}
```

#### Response (200 OK)
```json
{
  "success": true,
  "data": {
    "user": {
      "id": 1,
      "username": "user123",
      "email": "user@example.com",
      "firstName": "John",
      "lastName": "Doe",
      "role": "user"
    },
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  },
  "message": "Login successful"
}
```

#### Error Responses
```json
// 401 Unauthorized - Invalid credentials
{
  "success": false,
  "error": "Invalid username or password"
}
```

---

### POST /api/v1/auth/verify
**Verify JWT token**

#### Headers
```
Authorization: Bearer <access_token>
```

#### Response (200 OK)
```json
{
  "success": true,
  "data": {
    "userId": 1,
    "username": "user123",
    "role": "user",
    "exp": 1640995200
  }
}
```

#### Error Responses
```json
// 401 Unauthorized - Invalid token
{
  "success": false,
  "error": "Invalid token"
}

// 401 Unauthorized - Token expired
{
  "success": false,
  "error": "Token expired"
}
```

---

### POST /api/v1/auth/logout
**Logout user**

#### Headers
```
Authorization: Bearer <access_token>
```

#### Response (200 OK)
```json
{
  "success": true,
  "message": "Logout successful"
}
```

---

### GET /api/v1/auth/profile
**Get user profile**

#### Headers
```
Authorization: Bearer <access_token>
```

#### Response (200 OK)
```json
{
  "success": true,
  "data": {
    "id": 1,
    "username": "user123",
    "email": "user@example.com",
    "firstName": "John",
    "lastName": "Doe",
    "role": "user",
    "createdAt": "2024-07-11T16:30:00.000Z",
    "updatedAt": "2024-07-11T16:30:00.000Z"
  }
}
```

---

### PUT /api/v1/auth/profile
**Update user profile**

#### Headers
```
Authorization: Bearer <access_token>
```

#### Request Body
```json
{
  "firstName": "John Updated",
  "lastName": "Doe Updated",
  "email": "updated@example.com"
}
```

#### Response (200 OK)
```json
{
  "success": true,
  "data": {
    "id": 1,
    "username": "user123",
    "email": "updated@example.com",
    "firstName": "John Updated",
    "lastName": "Doe Updated",
    "role": "user",
    "updatedAt": "2024-07-11T16:35:00.000Z"
  },
  "message": "Profile updated successfully"
}
```

---

## 📹 Camera Management API (beCamera Service)

### GET /api/v1/cameras
**Get all cameras**

#### Headers
```
Authorization: Bearer <access_token>
```

#### Response (200 OK)
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "Camera 1",
      "description": "Main entrance camera",
      "ip_address": "192.168.1.100",
      "rtsp_url": "rtsp://192.168.1.100:554/stream",
      "status": "active",
      "created_at": "2024-07-11T16:30:00.000Z"
    }
  ],
  "count": 1
}
```

---

### POST /api/v1/cameras
**Create new camera**

#### Headers
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

#### Request Body
```json
{
  "name": "New Camera",
  "description": "Camera description",
  "ip_address": "192.168.1.101",
  "rtsp_url": "rtsp://192.168.1.101:554/stream",
  "status": "offline"
}
```

#### Response (200 OK)
```json
{
  "success": true,
  "data": {
    "id": 2,
    "name": "New Camera",
    "description": "Camera description",
    "ip_address": "192.168.1.101",
    "rtsp_url": "rtsp://192.168.1.101:554/stream",
    "status": "offline",
    "created_at": "2024-07-11T16:40:00.000Z"
  },
  "message": "Camera created successfully"
}
```

#### Error Responses
```json
// 400 Bad Request - Invalid data
{
  "detail": "Camera name is required"
}

// 400 Bad Request - Unsafe characters
{
  "detail": "Camera name contains unsafe characters"
}

// 400 Bad Request - Invalid IP address
{
  "detail": "Invalid IP address format"
}

// 400 Bad Request - Invalid RTSP URL
{
  "detail": "Invalid RTSP URL format"
}

// 400 Bad Request - Invalid status
{
  "detail": "Invalid status value"
}
```

---

### GET /api/v1/cameras/{id}
**Get camera by ID**

#### Headers
```
Authorization: Bearer <access_token>
```

#### Response (200 OK)
```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "Camera 1",
    "description": "Main entrance camera",
    "ip_address": "192.168.1.100",
    "rtsp_url": "rtsp://192.168.1.100:554/stream",
    "status": "active",
    "created_at": "2024-07-11T16:30:00.000Z"
  }
}
```

#### Error Responses
```json
// 404 Not Found
{
  "detail": "Camera not found"
}
```

---

### PUT /api/v1/cameras/{id}
**Update camera**

#### Headers
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

#### Request Body
```json
{
  "name": "Updated Camera Name",
  "description": "Updated description",
  "status": "maintenance"
}
```

#### Response (200 OK)
```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "Updated Camera Name",
    "description": "Updated description",
    "ip_address": "192.168.1.100",
    "rtsp_url": "rtsp://192.168.1.100:554/stream",
    "status": "maintenance",
    "created_at": "2024-07-11T16:30:00.000Z"
  },
  "message": "Camera updated successfully"
}
```

#### Error Responses
```json
// 404 Not Found
{
  "detail": "Camera not found"
}

// 400 Bad Request - No valid fields
{
  "detail": "No valid fields to update"
}
```

---

### DELETE /api/v1/cameras/{id}
**Delete camera**

#### Headers
```
Authorization: Bearer <access_token>
```

#### Response (200 OK)
```json
{
  "success": true,
  "message": "Camera deleted successfully"
}
```

#### Error Responses
```json
// 404 Not Found
{
  "detail": "Camera not found"
}
```

---

## 📊 Analytics API (beCamera Service)

### GET /api/v1/analytics/summary
**Get analytics summary**

#### Response (200 OK)
```json
{
  "success": true,
  "data": {
    "total_cameras": 10,
    "active_cameras": 8,
    "today_in": 150,
    "today_out": 120,
    "current_count": 30
  }
}
```

---

### GET /api/v1/counts
**Get count data**

#### Query Parameters
- `camera_id` (optional): Filter by camera ID
- `start_date` (optional): Start date (YYYY-MM-DD)
- `end_date` (optional): End date (YYYY-MM-DD)

#### Response (200 OK)
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "camera_id": 1,
      "count_in": 5,
      "count_out": 3,
      "confidence": 0.95,
      "timestamp": "2024-07-11T16:30:00.000Z"
    }
  ],
  "count": 1
}
```

---

## 🏥 Health Check API

### GET /health (beAuth Service)
**Check authentication service health**

#### Response (200 OK)
```json
{
  "status": "healthy",
  "service": "beAuth",
  "timestamp": "2024-07-11T16:30:00.000Z",
  "version": "1.0.0"
}
```

### GET /health (beCamera Service)
**Check camera service health**

#### Response (200 OK)
```json
{
  "status": "healthy",
  "service": "beCamera",
  "timestamp": "2024-07-11T16:30:00.000Z",
  "version": "1.0.0"
}
```

---

## ⚠️ Error Handling

### Standard Error Response Format
```json
{
  "detail": "Error message",
  "status_code": 400
}
```

### HTTP Status Codes
- **200 OK**: Request successful
- **201 Created**: Resource created successfully
- **400 Bad Request**: Invalid request data
- **401 Unauthorized**: Authentication required
- **403 Forbidden**: Access denied
- **404 Not Found**: Resource not found
- **409 Conflict**: Resource conflict
- **429 Too Many Requests**: Rate limit exceeded
- **500 Internal Server Error**: Server error

### Common Error Messages
```json
// Authentication errors
{
  "detail": "Invalid token"
}
{
  "detail": "Token expired"
}
{
  "detail": "Not authenticated"
}

// Validation errors
{
  "detail": "Camera name is required"
}
{
  "detail": "Camera name contains unsafe characters"
}
{
  "detail": "Invalid IP address format"
}
{
  "detail": "Invalid RTSP URL format"
}

// Rate limiting
{
  "detail": "Rate limit exceeded. Try again in 60 seconds."
}
```

---

## 🔒 Security & Rate Limiting

### Authentication
- All protected endpoints require JWT token in Authorization header
- Token format: `Bearer <access_token>`
- Token expiration: 15 minutes (configurable)

### Rate Limiting
- **Default**: 10 requests per minute per user
- **Authentication endpoints**: 5 requests per minute per IP
- **Headers returned**:
  - `X-RateLimit-Limit`: Request limit
  - `X-RateLimit-Remaining`: Remaining requests
  - `X-RateLimit-Reset`: Reset time (Unix timestamp)

### Input Validation
- **Camera Names**: Letters, numbers, spaces, hyphens, underscores, dots, commas, quotes
- **IP Addresses**: Valid IPv4 format
- **RTSP URLs**: Must start with rtsp://, http://, or https://
- **Status Values**: "active", "offline", "maintenance", "error"

### Security Measures
- SQL injection prevention
- XSS prevention
- Input sanitization
- CORS configuration
- Rate limiting

---

## 📝 Frontend Integration Examples

### JavaScript/TypeScript Examples

#### Authentication Flow
```javascript
// Register user
const registerUser = async (userData) => {
  const response = await fetch('http://localhost:3001/api/v1/auth/register', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(userData)
  });
  
  if (!response.ok) {
    throw new Error('Registration failed');
  }
  
  const data = await response.json();
  return data.data.accessToken;
};

// Login user
const loginUser = async (credentials) => {
  const response = await fetch('http://localhost:3001/api/v1/auth/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(credentials)
  });
  
  if (!response.ok) {
    throw new Error('Login failed');
  }
  
  const data = await response.json();
  return data.data.accessToken;
};

// Use token for protected requests
const getCameras = async (token) => {
  const response = await fetch('http://localhost:3002/api/v1/cameras', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  
  if (!response.ok) {
    throw new Error('Failed to fetch cameras');
  }
  
  return await response.json();
};
```

#### Camera Management
```javascript
// Create camera
const createCamera = async (cameraData, token) => {
  const response = await fetch('http://localhost:3002/api/v1/cameras', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify(cameraData)
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail);
  }
  
  return await response.json();
};

// Update camera
const updateCamera = async (id, updateData, token) => {
  const response = await fetch(`http://localhost:3002/api/v1/cameras/${id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify(updateData)
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail);
  }
  
  return await response.json();
};
```

#### Error Handling
```javascript
// Handle API errors
const handleApiError = (error) => {
  if (error.status === 401) {
    // Redirect to login
    window.location.href = '/login';
  } else if (error.status === 429) {
    // Show rate limit message
    alert('Too many requests. Please wait a moment.');
  } else {
    // Show generic error
    alert('An error occurred. Please try again.');
  }
};

// API wrapper with error handling
const apiCall = async (url, options = {}) => {
  try {
    const response = await fetch(url, options);
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'API request failed');
    }
    
    return await response.json();
  } catch (error) {
    handleApiError(error);
    throw error;
  }
};
```

---

## 🔧 Configuration

### Environment Variables
```bash
# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=people_counting_db
DB_USER=postgres
DB_PASSWORD=dev_password

# JWT
JWT_SECRET=dev_jwt_secret_key_2024_ai_camera_system
JWT_ACCESS_TOKEN_EXPIRY=15m
JWT_REFRESH_TOKEN_EXPIRY=7d

# Rate Limiting
RATE_LIMIT_WINDOW_MS=900000
RATE_LIMIT_MAX_REQUESTS=100

# CORS
CORS_ORIGIN=http://localhost:3000
```

### Service URLs
```javascript
const API_CONFIG = {
  AUTH_SERVICE: 'http://localhost:3001',
  CAMERA_SERVICE: 'http://localhost:3002',
  API_VERSION: 'v1'
};
```

---

## 📚 Additional Resources

### Documentation
- [Integration Testing Guide](../07-TESTING/integration-testing.md)
- [Database Schema](../03-DATABASE/database-schema.md)
- [Security Guidelines](../09-SECURITY/auth-security-guide.md)

### Support
- **Backend Team**: Available for integration support
- **Test Results**: All APIs tested and working
- **Status**: Ready for frontend integration

---

**Document Version**: 2.0  
**Last Updated**: 2024-07-11  
**Status**: ✅ READY FOR FRONTEND INTEGRATION 