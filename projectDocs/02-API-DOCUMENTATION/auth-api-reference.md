# API Reference - Authentication Service

## Base URL

```
Development: http://localhost:3001/api/v1
Production: https://api.peoplecounting.com/api/v1
```

## Authentication

### JWT Token Authentication

```http
Authorization: Bearer <jwt_token>
```

### Token Types
- **Access Token**: 15 phút, dùng cho API calls
- **Refresh Token**: 7 ngày, dùng để refresh access token

## API Endpoints

### 1. Authentication

#### Register User
```http
POST /auth/register
Content-Type: application/json

{
  "username": "string",
  "email": "string",
  "password": "string",
  "confirmPassword": "string",
  "firstName": "string",
  "lastName": "string",
  "registrationCode": "string"
}
```

**Validation Rules:**
- `username`: 3-30 chars, alphanumeric only
- `email`: Valid email format
- `password`: 8+ chars, uppercase, lowercase, number, special char
- `confirmPassword`: Must match password
- `firstName`: 2-50 chars (optional)
- `lastName`: 2-50 chars (optional)
- `registrationCode`: Required, must be a valid active registration code

**Response (201):**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": 1,
      "username": "newuser",
      "email": "user@example.com",
      "firstName": "John",
      "lastName": "Doe",
      "role": "user"
    },
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "tokenType": "bearer"
  }
}
```

**Error Response (400):**
```json
{
  "success": false,
  "error": {
    "code": 400,
    "message": "Validation failed",
    "details": [
      "Username already exists",
      "Password must contain at least one uppercase letter"
    ]
  }
}
```

#### Login User
```http
POST /auth/login
Content-Type: application/json

{
  "username": "string",
  "password": "string"
}
```

**Notes:**
- `username` có thể là username hoặc email
- Password phải khớp với user đã đăng ký

**Response (200):**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": 1,
      "username": "admin",
      "email": "admin@peoplecounting.com",
      "firstName": "System",
      "lastName": "Administrator",
      "role": "admin"
    },
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "tokenType": "bearer"
  }
}
```

**Error Response (401):**
```json
{
  "success": false,
  "error": {
    "code": 401,
    "message": "Invalid credentials"
  }
}
```

#### Refresh Token
```http
POST /auth/refresh
Content-Type: application/json

{
  "refreshToken": "string"
}
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": 1,
      "username": "admin",
      "email": "admin@peoplecounting.com",
      "firstName": "System",
      "lastName": "Administrator",
      "role": "admin"
    },
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "tokenType": "bearer"
  }
}
```

#### Logout User
```http
POST /auth/logout
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "success": true,
  "message": "Logged out successfully"
}
```

#### Forgot Password
```http
POST /auth/forgot-password
Content-Type: application/json

{
  "email": "string"
}
```

**Response (200):**
```json
{
  "success": true,
  "message": "If the email exists, a password reset link has been sent"
}
```

#### Reset Password
```http
POST /auth/reset-password
Content-Type: application/json

{
  "token": "string",
  "password": "string",
  "confirmPassword": "string"
}
```

**Response (200):**
```json
{
  "success": true,
  "message": "Password reset successfully"
}
```

#### Get Current User
```http
GET /auth/me
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": 1,
      "username": "admin",
      "email": "admin@peoplecounting.com",
      "firstName": "System",
      "lastName": "Administrator",
      "role": "admin"
    }
  }
}
```

### 2. User Management

#### Get User Profile
```http
GET /users/profile
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": 1,
      "username": "admin",
      "email": "admin@peoplecounting.com",
      "firstName": "System",
      "lastName": "Administrator",
      "role": "admin",
      "isActive": true,
      "lastLogin": "2024-01-01T12:00:00Z",
      "createdAt": "2024-01-01T00:00:00Z",
      "updatedAt": "2024-01-01T12:00:00Z"
    }
  }
}
```

#### Update User Profile
```http
PUT /users/profile
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "username": "string",
  "email": "string",
  "firstName": "string",
  "lastName": "string"
}
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": 1,
      "username": "updateduser",
      "email": "updated@example.com",
      "firstName": "Updated",
      "lastName": "Name",
      "role": "admin",
      "isActive": true,
      "updatedAt": "2024-01-01T12:00:00Z"
    }
  }
}
```

#### Change Password
```http
PUT /users/change-password
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "currentPassword": "string",
  "newPassword": "string",
  "confirmNewPassword": "string"
}
```

**Response (200):**
```json
{
  "success": true,
  "message": "Password changed successfully"
}
```

#### Get All Users (Admin Only)
```http
GET /users?page=1&limit=10&search=john&role=user
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `page`: Page number (default: 1)
- `limit`: Items per page (default: 10, max: 100)
- `search`: Search in username, email, firstName, lastName
- `role`: Filter by role (admin, user, viewer)
- `isActive`: Filter by active status (true, false)

**Response (200):**
```json
{
  "success": true,
  "data": {
    "users": [
      {
        "id": 1,
        "username": "admin",
        "email": "admin@peoplecounting.com",
        "firstName": "System",
        "lastName": "Administrator",
        "role": "admin",
        "isActive": true,
        "lastLogin": "2024-01-01T12:00:00Z",
        "createdAt": "2024-01-01T00:00:00Z",
        "updatedAt": "2024-01-01T12:00:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 10,
      "total": 1,
      "pages": 1
    }
  }
}
```

#### Get User by ID (Admin Only)
```http
GET /users/{id}
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": 1,
      "username": "admin",
      "email": "admin@peoplecounting.com",
      "firstName": "System",
      "lastName": "Administrator",
      "role": "admin",
      "isActive": true,
      "lastLogin": "2024-01-01T12:00:00Z",
      "createdAt": "2024-01-01T00:00:00Z",
      "updatedAt": "2024-01-01T12:00:00Z"
    }
  }
}
```

#### Update User by ID (Admin Only)
```http
PUT /users/{id}
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "username": "string",
  "email": "string",
  "firstName": "string",
  "lastName": "string",
  "role": "admin|user|viewer",
  "isActive": true
}
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": 1,
      "username": "updateduser",
      "email": "updated@example.com",
      "firstName": "Updated",
      "lastName": "Name",
      "role": "admin",
      "isActive": true,
      "updatedAt": "2024-01-01T12:00:00Z"
    }
  }
}
```

#### Delete User (Admin Only)
```http
DELETE /users/{id}
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "success": true,
  "message": "User deleted successfully"
}
```

### 3. System

#### Health Check
```http
GET /health
```

**Response (200):**
```json
{
  "status": "OK",
  "timestamp": "2024-01-01T12:00:00Z",
  "service": "Authentication Service",
  "version": "1.0.0"
}
```

### 3. Registration Codes (Admin Only)

#### Get All Registration Codes
```http
GET /users/registration-codes?page=1&limit=10&search=code&type=organization&isActive=true
Authorization: Bearer <admin_token>
```

**Query Parameters:**
- `page`: Page number (default: 1)
- `limit`: Items per page (default: 10)
- `search`: Search in code, name, description
- `type`: Filter by type (organization, department, general)
- `isActive`: Filter by active status (true/false)

**Response (200):**
```json
{
  "success": true,
  "data": {
    "codes": [
      {
        "id": 1,
        "code": "adminfe",
        "name": "Admin Future Eyes",
        "description": "Mã đăng ký mặc định cho hệ thống Future Eyes",
        "type": "organization",
        "max_uses": null,
        "used_count": 4,
        "is_active": true,
        "expires_at": null,
        "created_at": "2025-07-01T08:36:17.651Z",
        "updated_at": "2025-07-01T08:36:17.658Z",
        "created_by_username": "admin"
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 10,
      "total": 1,
      "pages": 1
    }
  }
}
```

#### Get Registration Code by ID
```http
GET /users/registration-codes/:id
Authorization: Bearer <admin_token>
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "code": {
      "id": 1,
      "code": "adminfe",
      "name": "Admin Future Eyes",
      "description": "Mã đăng ký mặc định cho hệ thống Future Eyes",
      "type": "organization",
      "max_uses": null,
      "used_count": 4,
      "is_active": true,
      "expires_at": null,
      "created_at": "2025-07-01T08:36:17.651Z",
      "updated_at": "2025-07-01T08:36:17.658Z",
      "created_by_username": "admin"
    }
  }
}
```

#### Create Registration Code
```http
POST /users/registration-codes
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "code": "string",
  "name": "string",
  "description": "string",
  "type": "organization|department|general",
  "maxUses": 10,
  "expiresAt": "2025-12-31T23:59:59Z"
}
```

**Validation Rules:**
- `code`: Required, unique, 1-50 characters
- `name`: Required, 1-100 characters
- `description`: Optional
- `type`: Optional, defaults to "organization"
- `maxUses`: Optional, integer (null = unlimited)
- `expiresAt`: Optional, ISO date string (null = never expires)

**Response (201):**
```json
{
  "success": true,
  "data": {
    "code": {
      "id": 2,
      "code": "testcode",
      "name": "Test Code",
      "description": "Mã đăng ký test",
      "type": "department",
      "max_uses": 10,
      "used_count": 0,
      "is_active": true,
      "expires_at": null,
      "created_at": "2025-07-01T10:40:34.626Z"
    }
  }
}
```

#### Update Registration Code
```http
PUT /users/registration-codes/:id
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "name": "Updated Name",
  "description": "Updated description",
  "type": "department",
  "maxUses": 5,
  "isActive": false,
  "expiresAt": "2025-12-31T23:59:59Z"
}
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "code": {
      "id": 2,
      "code": "testcode",
      "name": "Updated Name",
      "description": "Updated description",
      "type": "department",
      "max_uses": 5,
      "used_count": 0,
      "is_active": false,
      "expires_at": "2025-12-31T23:59:59Z",
      "updated_at": "2025-07-01T10:40:41.992Z"
    }
  }
}
```

#### Delete Registration Code
```http
DELETE /users/registration-codes/:id
Authorization: Bearer <admin_token>
```

**Notes:**
- Chỉ có thể xóa mã chưa được sử dụng (used_count = 0)

**Response (200):**
```json
{
  "success": true,
  "message": "Registration code deleted successfully"
}
```

**Error Response (400):**
```json
{
  "success": false,
  "error": {
    "code": 400,
    "message": "Cannot delete registration code that has been used"
  }
}
```

## Error Responses

### Standard Error Format
```json
{
  "success": false,
  "error": {
    "code": 400,
    "message": "Human readable error message",
    "details": [
      "Additional error details"
    ]
  }
}
```

### Common Error Codes

| Code | Description |
|------|-------------|
| 400 | Bad Request - Validation error |
| 401 | Unauthorized - Invalid or missing token |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource not found |
| 429 | Too Many Requests - Rate limit exceeded |
| 500 | Internal Server Error - Server error |

### Validation Errors
```json
{
  "success": false,
  "error": {
    "code": 400,
    "message": "Validation failed",
    "details": [
      "Username must be at least 3 characters long",
      "Email must be a valid email address",
      "Password must contain at least one uppercase letter"
    ]
  }
}
```

### Authentication Errors
```json
{
  "success": false,
  "error": {
    "code": 401,
    "message": "Not authorized to access this route"
  }
}
```

### Permission Errors
```json
{
  "success": false,
  "error": {
    "code": 403,
    "message": "User role user is not authorized to access this route"
  }
}
```

## Rate Limiting

- **Limit**: 100 requests per 15 minutes per IP
- **Headers**: 
  - `X-RateLimit-Limit`: Request limit
  - `X-RateLimit-Remaining`: Remaining requests
  - `X-RateLimit-Reset`: Reset time

## CORS

- **Origin**: Configurable via `CORS_ORIGIN` environment variable
- **Methods**: GET, POST, PUT, DELETE, OPTIONS
- **Headers**: Content-Type, Authorization
- **Credentials**: true

## Testing

### Test Users
| Username | Password | Role |
|----------|----------|------|
| admin | Admin123! | admin |
| testuser | Test123! | user |
| viewer | Viewer123! | viewer |

### Example cURL Commands

#### Register User
```bash
curl -X POST http://localhost:3001/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "email": "newuser@example.com",
    "password": "Password123!",
    "confirmPassword": "Password123!",
    "firstName": "New",
    "lastName": "User",
    "registrationCode": "adminfe"
  }'
```

#### Login User
```bash
curl -X POST http://localhost:3001/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "Admin123!"
  }'
```

#### Get Profile (with token)
```bash
curl -X GET http://localhost:3001/api/v1/auth/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

#### Update Profile
```bash
curl -X PUT http://localhost:3001/api/v1/users/profile \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "firstName": "Updated",
    "lastName": "Name"
  }'
```

## SDK Examples

### JavaScript/Node.js
```javascript
const axios = require('axios');

const API_BASE = 'http://localhost:3001/api/v1';

// Login
const login = async (username, password) => {
  const response = await axios.post(`${API_BASE}/auth/login`, {
    username,
    password
  });
  return response.data;
};

// Get profile with token
const getProfile = async (token) => {
  const response = await axios.get(`${API_BASE}/auth/me`, {
    headers: { Authorization: `Bearer ${token}` }
  });
  return response.data;
};
```

### Python
```python
import requests

API_BASE = 'http://localhost:3001/api/v1'

# Login
def login(username, password):
    response = requests.post(f'{API_BASE}/auth/login', json={
        'username': username,
        'password': password
    })
    return response.json()

# Get profile with token
def get_profile(token):
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f'{API_BASE}/auth/me', headers=headers)
    return response.json()
```

## Versioning

API versioning được quản lý qua URL path:
- Current version: `/api/v1/`
- Future versions: `/api/v2/`, `/api/v3/`, etc.

## Deprecation Policy

- API endpoints sẽ được thông báo deprecation 6 tháng trước khi remove
- Deprecated endpoints sẽ trả về warning header
- Breaking changes chỉ được thực hiện trong major version updates 