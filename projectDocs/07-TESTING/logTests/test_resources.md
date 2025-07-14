# 🧪 **TEST RESOURCES - AI Camera Counting System**

## 📊 **TEST ENVIRONMENT INFORMATION**

### **🏗️ Infrastructure Status**
- **Date**: 2025-01-09
- **Environment**: Development (Docker)
- **Docker Compose**: Unified (docker-compose.yml)
- **Status**: All services running

### **🔗 Service URLs & Ports**
| Service | URL | Port | Status | Health Check |
|---------|-----|------|--------|--------------|
| **Frontend** | http://localhost:3000 | 3000 | ✅ Running | http://localhost:3000/vision-ui-dashboard-react |
| **beAuth API** | http://localhost:3001 | 3001 | ✅ Running | http://localhost:3001/health |
| **beCamera API** | http://localhost:3002 | 3002 | ✅ Running | http://localhost:3002/health |
| **WebSocket** | ws://localhost:3003 | 3003 | ✅ Running | - |
| **PostgreSQL** | localhost:5432 | 5432 | ✅ Running | - |
| **Redis** | localhost:6379 | 6379 | ✅ Running | - |

---

## 🧪 **AUTOMATION TEST STRUCTURE**

### **📁 Directory Structure**
```
sharedResource/automationTest/
├── README.md                    # Hướng dẫn sử dụng
├── backend/                     # Backend test scripts
│   ├── auth/                    # Authentication service tests
│   ├── camera/                  # Camera management tests
│   ├── database/                # Database tests
│   ├── integration/             # Integration tests
│   ├── results/                 # Test results
│   └── logs/                    # Test logs
├── frontend/                    # Frontend test scripts
│   ├── components/              # Component tests
│   ├── pages/                   # Page tests
│   ├── e2e/                     # End-to-end tests
│   ├── results/                 # Test results
│   └── logs/                    # Test logs
├── performance/                 # Performance test scripts
├── security/                    # Security test scripts
├── utils/                       # Test utilities
└── config/                      # Test configuration files
```

### **🔧 Test Tools & Frameworks**
- **API Testing**: Newman, curl, HTTP requests
- **Database Testing**: PostgreSQL queries, Python scripts
- **Frontend Testing**: Playwright, React Testing Library, Jest
- **Performance Testing**: Artillery, Apache Bench
- **Security Testing**: OWASP ZAP, custom scripts
- **Visual Testing**: Percy, Chromatic

---

## 👤 **TEST USER ACCOUNTS**

### **🔐 Authentication Test Users**
```json
{
  "admin_user": {
    "username": "admin",
    "email": "admin@aicamera.com",
    "password": "Admin123!",
    "role": "admin",
    "expected_status": "active"
  },
  "regular_user": {
    "username": "user1",
    "email": "user1@aicamera.com", 
    "password": "User123!",
    "role": "user",
    "expected_status": "active"
  },
  "test_user": {
    "username": "testuser",
    "email": "test@aicamera.com",
    "password": "Test123!",
    "role": "user",
    "expected_status": "active"
  }
}
```

### **📝 Registration Test Data**
```json
{
  "valid_registration": {
    "username": "newuser",
    "email": "newuser@aicamera.com",
    "password": "NewUser123!",
    "first_name": "New",
    "last_name": "User",
    "registration_code": "REG001"
  },
  "invalid_registration": {
    "username": "invalid",
    "email": "invalid-email",
    "password": "weak",
    "first_name": "",
    "last_name": "",
    "registration_code": "INVALID"
  }
}
```

### **🔑 Available Registration Codes**
```json
{
  "REG001": {
    "description": "Test registration code for development",
    "max_uses": 100,
    "current_uses": 0,
    "is_active": true,
    "expires_at": "2025-12-31 23:59:59"
  },
  "REG002": {
    "description": "Another test registration code",
    "max_uses": 50,
    "current_uses": 0,
    "is_active": true,
    "expires_at": "2025-12-31 23:59:59"
  },
  "EXPIRED": {
    "description": "Expired registration code",
    "max_uses": 10,
    "current_uses": 0,
    "is_active": false,
    "expires_at": "2024-01-01 00:00:00"
  },
  "LIMITED": {
    "description": "Limited use registration code",
    "max_uses": 1,
    "current_uses": 0,
    "is_active": true,
    "expires_at": "2025-12-31 23:59:59"
  }
}
```

---

## 📹 **CAMERA TEST DATA**

### **📷 Camera Instances**
```json
{
  "test_camera_1": {
    "name": "Test Camera 1",
    "location": "Test Location 1",
    "stream_url": "rtsp://test-camera-1.example.com/stream",
    "status": "active"
  },
  "test_camera_2": {
    "name": "Test Camera 2", 
    "location": "Test Location 2",
    "stream_url": "rtsp://test-camera-2.example.com/stream",
    "status": "maintenance"
  },
  "test_camera_3": {
    "name": "Test Camera 3",
    "location": "Test Location 3", 
    "stream_url": "rtsp://test-camera-3.example.com/stream",
    "status": "offline"
  }
}
```

### **📊 Count Data Samples**
```json
{
  "valid_count_data": {
    "camera_id": 1,
    "people_in": 25,
    "people_out": 18,
    "current_count": 7,
    "confidence": 0.92
  },
  "edge_case_data": {
    "camera_id": 1,
    "people_in": 0,
    "people_out": 0,
    "current_count": 0,
    "confidence": 1.0
  }
}
```

---

## 🔑 **API TEST CREDENTIALS**

### **🔐 JWT Tokens**
```json
{
  "admin_token": "TO_BE_GENERATED",
  "user_token": "TO_BE_GENERATED", 
  "expired_token": "TO_BE_GENERATED",
  "invalid_token": "invalid.jwt.token"
}
```

### **🔒 API Headers**
```json
{
  "content_type": "application/json",
  "authorization": "Bearer {token}",
  "accept": "application/json"
}
```

---

## 🧪 **TEST CONFIGURATION**

### **⚙️ Environment Variables**
```bash
# Test Environment
TEST_ENV=development
API_BASE_URL=http://localhost:3001/api/v1
CAMERA_API_URL=http://localhost:3002/api/v1
FRONTEND_URL=http://localhost:3000
WS_URL=ws://localhost:3003

# Database
TEST_DB_HOST=localhost
TEST_DB_PORT=5432
TEST_DB_NAME=people_counting_db
TEST_DB_USER=postgres
TEST_DB_PASSWORD=postgres123

# Redis
TEST_REDIS_HOST=localhost
TEST_REDIS_PORT=6379

# JWT
JWT_SECRET=dev_jwt_secret_key_2024_ai_camera_system
JWT_ACCESS_TOKEN_EXPIRY=15m
JWT_REFRESH_TOKEN_EXPIRY=7d

# Test Credentials
TEST_ADMIN_USERNAME=admin
TEST_ADMIN_PASSWORD=Admin123!
TEST_USER_USERNAME=testuser
TEST_USER_PASSWORD=Test123!
```

### **📋 Test Parameters**
```json
{
  "timeout": {
    "short": 5000,
    "medium": 10000,
    "long": 30000
  },
  "retry": {
    "max_attempts": 3,
    "delay": 1000
  },
  "performance": {
    "load_test_users": 100,
    "stress_test_users": 500,
    "spike_test_users": 1000
  }
}
```

---

## 📊 **TEST EXECUTION WORKFLOW**

### **🔄 Backend Test Phases**
1. **Phase 1**: Database Tests (8 test cases) - 45 minutes
2. **Phase 2**: Authentication Service Tests (12 test cases) - 60 minutes
3. **Phase 3**: Camera Management API Tests (15 test cases) - 75 minutes
4. **Phase 4**: Worker Pool Processing Tests (8 test cases) - 45 minutes
5. **Phase 5**: Integration Tests (6 test cases) - 60 minutes
6. **Phase 6**: Security Tests (8 test cases) - 90 minutes
7. **Phase 7**: Performance Tests (6 test cases) - 120 minutes

### **🔄 Frontend Test Phases**
1. **Phase 1**: Authentication & Navigation Tests (18 test cases) - 90 minutes
2. **Phase 2**: Core Functionality Tests (20 test cases) - 120 minutes
3. **Phase 3**: Advanced Features Tests (7 test cases) - 90 minutes

### **📊 Total Test Coverage**
- **Backend Test Cases**: 67
- **Frontend Test Cases**: 45
- **Total Test Cases**: 112
- **Estimated Duration**: 8 hours (Backend) + 5 hours (Frontend) = 13 hours

---

## 📝 **TEST EXECUTION NOTES**

### **✅ Completed Tests**
- [ ] Database Tests (Phase 1)
- [ ] Authentication Service Tests (Phase 2)
- [ ] Camera Management API Tests (Phase 3)
- [ ] Worker Pool Processing Tests (Phase 4)
- [ ] Integration Tests (Phase 5)
- [ ] Security Tests (Phase 6)
- [ ] Performance Tests (Phase 7)
- [ ] Frontend Authentication Tests (Phase 1)
- [ ] Frontend Core Functionality Tests (Phase 2)
- [ ] Frontend Advanced Features Tests (Phase 3)

### **⚠️ Known Issues**
- None reported yet

### **📊 Test Results Summary**
- **Total Test Cases**: 112
- **Backend Test Cases**: 67
- **Frontend Test Cases**: 45
- **Completed**: 0
- **Passed**: 0
- **Failed**: 0
- **Success Rate**: 0%

---

## 🚀 **AUTOMATION SCRIPTS**

### **📁 Script Locations**
- **Backend Scripts**: `sharedResource/automationTest/backend/`
- **Frontend Scripts**: `sharedResource/automationTest/frontend/`
- **Performance Scripts**: `sharedResource/automationTest/performance/`
- **Security Scripts**: `sharedResource/automationTest/security/`
- **Utility Scripts**: `sharedResource/automationTest/utils/`

### **🔧 Script Types**
- **Shell Scripts**: Environment setup, service health checks
- **Python Scripts**: API testing, database testing
- **JavaScript Scripts**: Frontend testing, E2E testing
- **YAML Configs**: Performance test configurations
- **JSON Configs**: Test data and configurations

### **📊 Results & Reports**
- **HTML Reports**: Detailed test reports
- **JSON Reports**: Machine-readable results
- **JUnit XML**: CI/CD integration
- **Console Output**: Real-time test progress

---

## 📞 **SUPPORT & CONTACT**

### **👥 Team Contacts**
- **QA Lead**: qa@aicamera.com
- **Backend Team**: backend@aicamera.com
- **Frontend Team**: frontend@aicamera.com
- **DevOps Team**: devops@aicamera.com

### **📚 Documentation**
- **API Documentation**: `projectDocs/02-API-DOCUMENTATION/`
- **Database Schema**: `projectDocs/03-DATABASE/`
- **Testing Guide**: `projectDocs/07-TESTING/`
- **Automation Guide**: `sharedResource/automationTest/README.md`

---

**📅 Last Updated**: 2025-01-09 14:00:00  
**👥 Maintainer**: QA Team  
**🔄 Version**: 2.0.0 - Complete Test Resources 

## [2025-07-11] ĐÃ KHỞI TẠO LẠI DATABASE TỪ SCHEMA HỢP NHẤT

- Database đã được khởi tạo lại từ sharedResource/init.sql hợp nhất (đầy đủ enum, bảng, index, trigger, sample data)
- Các file .sql cũ (beAuth/init.sql, beCamera/database/init.sql) đã được xóa
- Mọi hướng dẫn, cấu hình, test script đều tham chiếu duy nhất sharedResource/init.sql
- Sẵn sàng chạy lại automation test

### Trạng thái: Đang thực hiện 