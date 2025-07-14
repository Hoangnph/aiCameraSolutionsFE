# 📝 **TEST EXECUTION LOG - AI Camera Counting System**

## 🧪 **AUTHENTICATION SERVICE TESTS LOG**

### **📊 Test Session Information**
- **Session ID**: AUTH-TEST-2025-07-09-001
- **Start Time**: 2025-07-09 10:00:00
- **Environment**: Development (Docker)
- **Tester**: AI Assistant (Dev-Test Expert)
- **Service**: beAuth (Port 3001)

---

## 🔍 **PRE-TEST VERIFICATION**

### **✅ Environment Check**
```bash
# Service Health Check
curl -f http://localhost:3001/health
# Response: {"status":"OK","timestamp":"2025-07-09T09:42:55.089Z","service":"Authentication Service","version":"1.0.0"}

# Database Connection Check
docker exec ai_camera_postgres pg_isready -U postgres
# Response: localhost:5432 - accepting connections

# Redis Connection Check  
docker exec ai_camera_redis redis-cli ping
# Response: PONG
```

### **✅ Service Status**
- **beAuth Service**: ✅ Running (Port 3001)
- **PostgreSQL**: ✅ Running (Port 5432)
- **Redis**: ✅ Running (Port 6379)
- **Frontend**: ✅ Running (Port 3000)
- **beCamera**: ✅ Running (Port 3002)
- **WebSocket**: ✅ Running (Port 3003)

---

## 🧪 **TEST CASE EXECUTION**

### **📋 Test Case: AUTH-REG-001 - Successful User Registration**
- **Status**: ✅ **PASSED**
- **Start Time**: 2025-07-09 10:05:00
- **End Time**: 2025-07-09 10:25:00
- **Priority**: High
- **Test Type**: Positive

#### **Test Steps**
1. **Precondition Check**: Đảm bảo có registration code hợp lệ (`REG001`) trong DB
2. **API Call**: POST /api/v1/auth/register với dữ liệu:
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
3. **Data Validation**: Kiểm tra response trả về
4. **Database Verification**: Kiểm tra user đã được tạo
5. **Token Validation**: Kiểm tra accessToken, refreshToken

#### **Expected Results**
- Status Code: 201 Created
- Response: User data + JWT tokens
- Database: User record created
- Logs: Registration success logged

#### **Actual Results**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": 4,
      "username": "testuser001",
      "email": "testuser001@example.com",
      "firstName": "Test",
      "lastName": "User",
      "role": "user"
    },
    "accessToken": "<jwt_access_token>",
    "refreshToken": "<jwt_refresh_token>",
    "tokenType": "bearer"
  }
}
```
- User mới đã được tạo thành công trong DB
- accessToken và refreshToken hợp lệ

#### **Lỗi gặp phải & Cách khắc phục**
- **Lỗi 1:** `relation "registration_codes" does not exist` → **Fix:** Tạo bảng registration_codes bằng migration và cập nhật schema
- **Lỗi 2:** `column "name" does not exist` → **Fix:** Thêm cột name, used_count vào registration_codes
- **Lỗi 3:** `column "registration_code_id" of relation "users" does not exist` → **Fix:** Thêm cột registration_code_id vào users
- **Đã cập nhật lại file init.sql để đồng bộ schema, đảm bảo khởi tạo mới không lỗi**

#### **Kết luận**
- Test case đã pass hoàn toàn, backend đã sẵn sàng cho các test case tiếp theo.
- Đã ghi nhận lại toàn bộ quá trình fix schema, đảm bảo tài liệu hóa cho các lần test sau.

---

### **📋 Test Case: AUTH-REG-002 - Registration with Invalid Code**
- **Status**: ✅ **PASSED**
- **Start Time**: 2025-07-09 10:30:00
- **Priority**: High
- **Test Type**: Negative

#### **Test Data**
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

#### **Expected Results**
- Status Code: 400 Bad Request
- Response: Invalid registration code error

#### **Actual Results**
```json
{
  "success": false,
  "error": {
    "code": 400,
    "message": "Mã đăng ký không hợp lệ"
  }
}
```
- API trả về đúng lỗi 400 với message tiếng Việt
- Validation hoạt động chính xác

---

### **📋 Test Case: AUTH-REG-003 - Registration with Duplicate Username**
- **Status**: ✅ **PASSED**
- **Start Time**: 2025-07-09 10:32:00
- **Priority**: High
- **Test Type**: Negative

#### **Test Data**
```json
{
  "username": "testuser001",
  "email": "newuser@example.com",
  "password": "TestPassword123!",
  "confirmPassword": "TestPassword123!",
  "firstName": "Test",
  "lastName": "User",
  "registrationCode": "REG001"
}
```

#### **Expected Results**
- Status Code: 400 Bad Request
- Response: Username already exists error

#### **Actual Results**
```json
{
  "success": false,
  "error": {
    "code": 400,
    "message": "Username already exists"
  }
}
```
- API trả về đúng lỗi 400 với message "Username already exists"
- Unique constraint hoạt động chính xác

---

### **📋 Test Case: AUTH-LOGIN-001 - Successful Login with Username**
- **Status**: ✅ **PASSED**
- **Start Time**: 2025-07-09 10:35:00
- **Priority**: High
- **Test Type**: Positive

#### **Test Data**
```json
{
  "username": "testuser001",
  "password": "TestPassword123!"
}
```

#### **Expected Results**
- Status Code: 200 OK
- Response: User data + JWT tokens
- Database: last_login updated

#### **Actual Results**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": 4,
      "username": "testuser001",
      "email": "testuser001@example.com",
      "firstName": "Test",
      "lastName": "User",
      "role": "user"
    },
    "accessToken": "<jwt_access_token>",
    "refreshToken": "<jwt_refresh_token>",
    "tokenType": "bearer"
  }
}
```
- Login thành công, trả về đầy đủ user data và tokens
- JWT tokens được tạo chính xác

---

### **📋 Test Case: AUTH-LOGIN-002 - Login with Invalid Credentials**
- **Status**: ✅ **PASSED**
- **Start Time**: 2025-07-09 10:37:00
- **Priority**: High
- **Test Type**: Negative

#### **Test Data**
```json
{
  "username": "testuser001",
  "password": "WrongPassword123!"
}
```

#### **Expected Results**
- Status Code: 401 Unauthorized
- Response: Invalid credentials error

#### **Actual Results**
```json
{
  "success": false,
  "error": {
    "code": 401,
    "message": "Invalid credentials"
  }
}
```
- API trả về đúng lỗi 401 với message "Invalid credentials"
- Password validation hoạt động chính xác

---

### **📋 Test Case: AUTH-TOKEN-001 - Refresh Access Token**
- **Status**: ✅ **PASSED**
- **Start Time**: 2025-07-09 10:40:00
- **Priority**: High
- **Test Type**: Positive

#### **Test Data**
```json
{
  "refreshToken": "<valid_refresh_token>"
}
```

#### **Expected Results**
- Status Code: 200 OK
- Response: New access token + refresh token

#### **Actual Results**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": 4,
      "username": "testuser001",
      "email": "testuser001@example.com",
      "firstName": "Test",
      "lastName": "User",
      "role": "user"
    },
    "accessToken": "<new_jwt_access_token>",
    "refreshToken": "<new_jwt_refresh_token>",
    "tokenType": "bearer"
  }
}
```
- Refresh token thành công, trả về access token mới
- JWT token rotation hoạt động chính xác

---

### **📋 Test Case: AUTH-REG-003 - Registration with Duplicate Username**
- **Status**: ⏸️ **PENDING**
- **Priority**: High
- **Test Type**: Negative

#### **Test Data**
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

#### **Expected Results**
- Status Code: 400 Bad Request
- Response: Username already exists error

---

### **📋 Test Case: AUTH-LOGIN-001 - Successful Login with Username**
- **Status**: ⏸️ **PENDING**
- **Priority**: High
- **Test Type**: Positive

#### **Test Data**
```json
{
  "username": "testuser001",
  "password": "TestPassword123!"
}
```

#### **Expected Results**
- Status Code: 200 OK
- Response: User data + JWT tokens
- Database: last_login updated

---

### **📋 Test Case: AUTH-LOGIN-002 - Login with Invalid Credentials**
- **Status**: ⏸️ **PENDING**
- **Priority**: High
- **Test Type**: Negative

#### **Test Data**
```json
{
  "username": "testuser001",
  "password": "WrongPassword123!"
}
```

#### **Expected Results**
- Status Code: 401 Unauthorized
- Response: Invalid credentials error

---

### **📋 Test Case: AUTH-TOKEN-001 - Refresh Access Token**
- **Status**: ⏸️ **PENDING**
- **Priority**: High
- **Test Type**: Positive

#### **Test Data**
```json
{
  "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

#### **Expected Results**
- Status Code: 200 OK
- Response: New access token + refresh token

---

### **📋 Test Case: AUTH-TOKEN-002 - Logout User**
- **Status**: ⏸️ **PENDING**
- **Priority**: Medium
- **Test Type**: Positive

#### **Headers**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

#### **Expected Results**
- Status Code: 200 OK
- Response: Logout success message
- Database: Refresh token invalidated

---

### **📋 Test Case: AUTH-PROFILE-001 - Get User Profile**
- **Status**: ⏸️ **PENDING**
- **Priority**: Medium
- **Test Type**: Positive

#### **Headers**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

#### **Expected Results**
- Status Code: 200 OK
- Response: Complete user profile data

---

### **📋 Test Case: AUTH-PROFILE-002 - Update User Profile**
- **Status**: ⏸️ **PENDING**
- **Priority**: Medium
- **Test Type**: Positive

#### **Test Data**
```json
{
  "firstName": "Updated",
  "lastName": "Name",
  "email": "updated@example.com"
}
```

#### **Expected Results**
- Status Code: 200 OK
- Response: Updated user data
- Database: Profile fields updated

---

### **📋 Test Case: AUTH-SEC-001 - Rate Limiting**
- **Status**: ⏸️ **PENDING**
- **Priority**: High
- **Test Type**: Security

#### **Test Steps**
1. Send 100+ requests to /api/v1/auth/login within 15 minutes
2. Verify rate limiting response

#### **Expected Results**
- Status Code: 429 Too Many Requests
- Response: Rate limit exceeded error

---

### **📋 Test Case: AUTH-SEC-002 - Password Validation**
- **Status**: ⏸️ **PENDING**
- **Priority**: High
- **Test Type**: Validation

#### **Test Data**
```json
{
  "username": "testuser",
  "password": "weak",
  "confirmPassword": "weak"
}
```

#### **Expected Results**
- Status Code: 400 Bad Request
- Response: Password validation error

---

### **📋 Test Case: AUTH-ERR-001 - Database Connection Error**
- **Status**: ⏸️ **PENDING**
- **Priority**: Medium
- **Test Type**: Error Handling

#### **Test Steps**
1. Stop PostgreSQL service
2. Send login request
3. Verify error handling

#### **Expected Results**
- Status Code: 500 Internal Server Error
- Response: Database connection error message
- Logs: Error logged with details

---

## 📊 **TEST RESULTS SUMMARY**

### **📈 Current Progress**
- **Total Test Cases**: 12
- **Completed**: 0
- **In Progress**: 1
- **Pending**: 11
- **Passed**: 0
- **Failed**: 0
- **Success Rate**: 0%

### **⚠️ Issues Found**
- None reported yet

### **🔧 Fixes Applied**
- None required yet

---

## 📝 **EXECUTION NOTES**

### **🔄 Real-time Updates**

#### **2025-07-09 10:00:00**
- Started Authentication Service Tests
- Verified environment health
- Prepared test data
- Created execution log

#### **2025-07-09 10:05:00**
- Started AUTH-REG-001 test case
- Test in progress...

### **📋 Next Steps**
1. Complete AUTH-REG-001 test case
2. Execute remaining registration tests
3. Execute login tests
4. Execute token management tests
5. Execute profile management tests
6. Execute security tests
7. Execute error handling tests
8. Generate test report

---

## 🎯 **ACCEPTANCE CRITERIA VERIFICATION**

- [ ] All API endpoints return correct HTTP status codes
- [ ] JWT tokens are properly generated and validated
- [ ] Password hashing works correctly
- [ ] Rate limiting prevents abuse
- [ ] Input validation rejects invalid data
- [ ] Error handling provides meaningful messages
- [ ] Audit logging captures all security events
- [ ] Database operations are atomic and consistent 