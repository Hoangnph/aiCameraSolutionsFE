# Authentication Service (beAuth) - Test Cases
## Workflow 1: User Authentication & Management

### 📋 **WORKFLOW OVERVIEW**

**Service**: Node.js Express Authentication Service  
**Port**: 3001  
**Database**: PostgreSQL  
**Cache**: Redis  
**Authentication**: JWT (Access Token + Refresh Token)  

#### **Workflow Diagram**
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User Input    │───▶│  Validation     │───▶│  Database       │
│   (Register/    │    │  (Joi Schema)   │    │  (PostgreSQL)   │
│    Login)       │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  JWT Token      │    │  Error Handling │    │  Audit Logging  │
│  Generation     │    │  (HTTP Status)  │    │  (Winston)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

#### **Key Features**
- User registration with validation codes
- JWT-based authentication
- Role-based access control (admin, user, viewer)
- Password hashing with bcrypt
- Rate limiting protection
- Audit logging

---

### 🧪 **TEST CASE 1.1: User Registration**

#### **Test Case ID**: `AUTH-REG-001`
#### **Test Case Name**: Successful User Registration
#### **Priority**: High
#### **Test Type**: Positive

**Preconditions**:
- Database is running and accessible
- Registration code exists in database
- Service is running on port 3001

**Test Data**:
```json
{
  "username": "testuser001",
  "email": "testuser001@example.com",
  "password": "TestPassword123!",
  "confirmPassword": "TestPassword123!",
  "firstName": "Test",
  "lastName": "User",
  "registrationCode": "REG001"
}
```

**Test Steps**:
1. Send POST request to `/api/v1/auth/register`
2. Include test data in request body
3. Set Content-Type: application/json
4. Verify response

**Expected Results**:
- **Status Code**: 201 Created
- **Response Body**:
```json
{
  "success": true,
  "data": {
    "user": {
      "id": 1,
      "username": "testuser001",
      "email": "testuser001@example.com",
      "firstName": "Test",
      "lastName": "User",
      "role": "user"
    },
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```
- **Database**: User record created in `users` table
- **Logs**: Registration success logged

---

#### **Test Case ID**: `AUTH-REG-002`
#### **Test Case Name**: Registration with Invalid Code
#### **Priority**: High
#### **Test Type**: Negative

**Test Data**:
```json
{
  "username": "testuser002",
  "email": "testuser002@example.com",
  "password": "TestPassword123!",
  "confirmPassword": "TestPassword123!",
  "firstName": "Test",
  "lastName": "User",
  "registrationCode": "INVALID_CODE"
}
```

**Expected Results**:
- **Status Code**: 400 Bad Request
- **Response Body**:
```json
{
  "success": false,
  "error": {
    "code": 400,
    "message": "Mã đăng ký không hợp lệ"
  }
}
```

---

#### **Test Case ID**: `AUTH-REG-003`
#### **Test Case Name**: Registration with Duplicate Username
#### **Priority**: High
#### **Test Type**: Negative

**Preconditions**: User with username "existinguser" already exists

**Test Data**:
```json
{
  "username": "existinguser",
  "email": "newuser@example.com",
  "password": "TestPassword123!",
  "confirmPassword": "TestPassword123!",
  "firstName": "Test",
  "lastName": "User",
  "registrationCode": "REG001"
}
```

**Expected Results**:
- **Status Code**: 400 Bad Request
- **Response Body**:
```json
{
  "success": false,
  "error": {
    "code": 400,
    "message": "Username already exists"
  }
}
```

---

### 🧪 **TEST CASE 1.2: User Login**

#### **Test Case ID**: `AUTH-LOGIN-001`
#### **Test Case Name**: Successful Login with Username
#### **Priority**: High
#### **Test Type**: Positive

**Preconditions**: User exists in database

**Test Data**:
```json
{
  "username": "testuser001",
  "password": "TestPassword123!"
}
```

**Expected Results**:
- **Status Code**: 200 OK
- **Response Body**:
```json
{
  "success": true,
  "data": {
    "user": {
      "id": 1,
      "username": "testuser001",
      "email": "testuser001@example.com",
      "firstName": "Test",
      "lastName": "User",
      "role": "user"
    },
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```
- **Database**: `last_login` field updated
- **Logs**: Login success logged

---

#### **Test Case ID**: `AUTH-LOGIN-002`
#### **Test Case Name**: Login with Invalid Credentials
#### **Priority**: High
#### **Test Type**: Negative

**Test Data**:
```json
{
  "username": "testuser001",
  "password": "WrongPassword123!"
}
```

**Expected Results**:
- **Status Code**: 401 Unauthorized
- **Response Body**:
```json
{
  "success": false,
  "error": {
    "code": 401,
    "message": "Invalid credentials"
  }
}
```

---

### 🧪 **TEST CASE 1.3: Token Management**

#### **Test Case ID**: `AUTH-TOKEN-001`
#### **Test Case Name**: Refresh Access Token
#### **Priority**: High
#### **Test Type**: Positive

**Preconditions**: Valid refresh token exists

**Test Data**:
```json
{
  "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Expected Results**:
- **Status Code**: 200 OK
- **Response Body**:
```json
{
  "success": true,
  "data": {
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

---

#### **Test Case ID**: `AUTH-TOKEN-002`
#### **Test Case Name**: Logout User
#### **Priority**: Medium
#### **Test Type**: Positive

**Preconditions**: Valid access token

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
  "message": "Logged out successfully"
}
```
- **Database**: Refresh token invalidated

---

### 🧪 **TEST CASE 1.4: User Profile Management**

#### **Test Case ID**: `AUTH-PROFILE-001`
#### **Test Case Name**: Get User Profile
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
    "user": {
      "id": 1,
      "username": "testuser001",
      "email": "testuser001@example.com",
      "firstName": "Test",
      "lastName": "User",
      "role": "user",
      "isActive": true,
      "lastLogin": "2024-01-15T10:30:00Z",
      "createdAt": "2024-01-01T00:00:00Z",
      "updatedAt": "2024-01-15T10:30:00Z"
    }
  }
}
```

---

#### **Test Case ID**: `AUTH-PROFILE-002`
#### **Test Case Name**: Update User Profile
#### **Priority**: Medium
#### **Test Type**: Positive

**Headers**:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Test Data**:
```json
{
  "firstName": "Updated",
  "lastName": "Name",
  "email": "updated@example.com"
}
```

**Expected Results**:
- **Status Code**: 200 OK
- **Response Body**: Updated user data
- **Database**: Profile fields updated

---

### 🧪 **TEST CASE 1.5: Security & Validation**

#### **Test Case ID**: `AUTH-SEC-001`
#### **Test Case Name**: Rate Limiting
#### **Priority**: High
#### **Test Type**: Security

**Test Steps**:
1. Send 100+ requests to `/api/v1/auth/login` within 15 minutes
2. Verify rate limiting response

**Expected Results**:
- **Status Code**: 429 Too Many Requests
- **Response Body**:
```json
{
  "success": false,
  "error": {
    "code": 429,
    "message": "Too many requests"
  }
}
```

---

#### **Test Case ID**: `AUTH-SEC-002`
#### **Test Case Name**: Password Validation
#### **Priority**: High
#### **Test Type**: Validation

**Test Data**:
```json
{
  "username": "testuser",
  "password": "weak",
  "confirmPassword": "weak"
}
```

**Expected Results**:
- **Status Code**: 400 Bad Request
- **Response Body**: Password validation error

---

### 🧪 **TEST CASE 1.6: Error Handling**

#### **Test Case ID**: `AUTH-ERR-001`
#### **Test Case Name**: Database Connection Error
#### **Priority**: Medium
#### **Test Type**: Error Handling

**Test Steps**:
1. Stop PostgreSQL service
2. Send login request
3. Verify error handling

**Expected Results**:
- **Status Code**: 500 Internal Server Error
- **Response Body**: Database connection error message
- **Logs**: Error logged with details

---

### 📊 **TEST EXECUTION MATRIX**

| Test Case | Priority | Status | Executed By | Date | Notes |
|-----------|----------|--------|-------------|------|-------|
| AUTH-REG-001 | High | 🔄 | | | |
| AUTH-REG-002 | High | 🔄 | | | |
| AUTH-REG-003 | High | 🔄 | | | |
| AUTH-LOGIN-001 | High | 🔄 | | | |
| AUTH-LOGIN-002 | High | 🔄 | | | |
| AUTH-TOKEN-001 | High | 🔄 | | | |
| AUTH-TOKEN-002 | Medium | 🔄 | | | |
| AUTH-PROFILE-001 | Medium | 🔄 | | | |
| AUTH-PROFILE-002 | Medium | 🔄 | | | |
| AUTH-SEC-001 | High | 🔄 | | | |
| AUTH-SEC-002 | High | 🔄 | | | |
| AUTH-ERR-001 | Medium | 🔄 | | | |

### 🎯 **ACCEPTANCE CRITERIA**

- ✅ All API endpoints return correct HTTP status codes
- ✅ JWT tokens are properly generated and validated
- ✅ Password hashing works correctly
- ✅ Rate limiting prevents abuse
- ✅ Input validation rejects invalid data
- ✅ Error handling provides meaningful messages
- ✅ Audit logging captures all security events
- ✅ Database operations are atomic and consistent

### 📝 **NOTES**

- All test cases should be executed in isolated environment
- Database should be reset between test runs
- JWT tokens should be validated for proper expiration
- Performance tests should verify response times < 200ms
- Security tests should verify no sensitive data exposure 