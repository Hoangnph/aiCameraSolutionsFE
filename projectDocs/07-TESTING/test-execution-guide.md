# Test Execution Guide
## Hướng dẫn thực thi test toàn bộ hệ thống AI Camera Counting

### 📋 **TỔNG QUAN TEST PLAN**

**Dự án**: AI Camera Counting System  
**Kiến trúc**: Microservices (React + Node.js + Python)  
**Phạm vi test**: 4 Workflows chính + Integration Testing  
**Thời gian ước tính**: 2-3 ngày cho toàn bộ test suite  

#### **Test Workflows**
1. **Authentication Service (beAuth)** - 13 test cases
2. **Camera Management API (beCamera)** - 18 test cases  
3. **Worker Pool Processing** - 16 test cases
4. **Frontend Integration** - 22 test cases
5. **Production Deployment & Advanced Features** - 23 test cases
6. **Integration Testing** - 16 test cases
7. **Dataflow Testing** - 22 test cases

**Tổng cộng**: 130 test cases

---

### 🚀 **CHUẨN BỊ MÔI TRƯỜNG TEST**

#### **Yêu cầu hệ thống**
```bash
# Kiểm tra Docker containers đang chạy
docker ps

# Expected containers:
# - people_counting_db (PostgreSQL)
# - auth_redis (Redis)
# - auth_service (beAuth)
# - ai-camera-service (beCamera)
```

#### **Kiểm tra services**
```bash
# Health check các services
curl http://localhost:3001/health  # beAuth
curl http://localhost:3002/health  # beCamera
curl http://localhost:3000         # Frontend (nếu đang chạy)
```

#### **Chuẩn bị test data**
```sql
-- Kết nối database và tạo test data
docker exec -it people_counting_db psql -U postgres -d people_counting_db

-- Tạo registration code cho test
INSERT INTO registration_codes (code, name, max_uses, used_count, is_active) 
VALUES ('REG001', 'Test Registration Code', 100, 0, true);
```

---

### 📋 **TEST EXECUTION SCHEDULE**

#### **Ngày 1: Backend Services Testing**

**Buổi sáng (4 giờ)**
- **Workflow 1**: Authentication Service Testing
- **Workflow 2**: Camera Management API Testing

**Buổi chiều (4 giờ)**
- **Workflow 3**: Worker Pool Processing Testing
- **Dataflow Testing**: Core Dataflows

#### **Ngày 2: Frontend & Advanced Features Testing**

**Buổi sáng (4 giờ)**
- **Workflow 4**: Frontend Integration Testing
- **Workflow 5**: Production Deployment Testing

**Buổi chiều (4 giờ)**
- **Dataflow Testing**: Advanced Dataflows
- **Performance Testing**

#### **Ngày 3: Integration & Final Testing**

**Buổi sáng (4 giờ)**
- **Integration Testing**: End-to-End Testing
- **Security Testing**

**Buổi chiều (4 giờ)**
- **Regression Testing**
- **Test report generation**
- **Documentation updates**

---

### 🧪 **DETAILED TEST EXECUTION**

#### **Phase 1: Authentication Service (beAuth)**

**Test Environment Setup**:
```bash
# 1. Verify beAuth service
curl http://localhost:3001/health

# 2. Check database connection
docker exec -it people_counting_db psql -U postgres -d people_counting_db -c "SELECT COUNT(*) FROM users;"

# 3. Verify Redis connection
docker exec -it auth_redis redis-cli ping
```

**Test Cases Execution Order**:
1. `AUTH-REG-001`: Successful User Registration
2. `AUTH-REG-002`: Registration with Invalid Code
3. `AUTH-REG-003`: Registration with Duplicate Username
4. `AUTH-LOGIN-001`: Successful Login
5. `AUTH-LOGIN-002`: Login with Invalid Credentials
6. `AUTH-TOKEN-001`: Refresh Access Token
7. `AUTH-TOKEN-002`: Logout User
8. `AUTH-PROFILE-001`: Get User Profile
9. `AUTH-PROFILE-002`: Update User Profile
10. `AUTH-SEC-001`: Rate Limiting
11. `AUTH-SEC-002`: Password Validation
12. `AUTH-ERR-001`: Database Connection Error

**Tools & Commands**:
```bash
# Test registration
curl -X POST http://localhost:3001/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser001",
    "email": "testuser001@example.com",
    "password": "TestPassword123!",
    "confirmPassword": "TestPassword123!",
    "firstName": "Test",
    "lastName": "User",
    "registrationCode": "REG001"
  }'

# Test login
curl -X POST http://localhost:3001/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser001",
    "password": "TestPassword123!"
  }'
```

#### **Phase 2: Camera Management API (beCamera)**

**Test Environment Setup**:
```bash
# 1. Verify beCamera service
curl http://localhost:3002/health

# 2. Check worker pool status
curl http://localhost:3002/api/v1/test/workers/status

# 3. Verify camera data
curl http://localhost:3002/api/v1/test/cameras
```

**Test Cases Execution Order**:
1. `CAM-CRUD-001`: Create New Camera
2. `CAM-CRUD-002`: Get All Cameras
3. `CAM-CRUD-003`: Get Camera by ID
4. `CAM-CRUD-004`: Update Camera
5. `CAM-CRUD-005`: Delete Camera
6. `CAM-STATUS-001`: Update Camera Status
7. `CAM-STATUS-002`: Invalid Status Update
8. `CAM-WORKER-001`: Start Camera Processing
9. `CAM-WORKER-002`: Stop Camera Processing
10. `CAM-WORKER-003`: Get Worker Pool Status
11. `CAM-ANALYTICS-001`: Get Count Data
12. `CAM-ANALYTICS-002`: Get Analytics Summary
13. `CAM-AUTH-001`: Access Without Token
14. `CAM-AUTH-002`: Access with Invalid Token
15. `CAM-ERR-001`: Camera Not Found
16. `CAM-ERR-002`: Database Connection Error
17. `CAM-PERF-001`: Response Time Test
18. `CAM-PERF-002`: Worker Pool Load Test

**Tools & Commands**:
```bash
# Get JWT token first
TOKEN=$(curl -s -X POST http://localhost:3001/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser001", "password": "TestPassword123!"}' | jq -r '.data.accessToken')

# Test camera creation
curl -X POST http://localhost:3002/api/v1/cameras \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Camera",
    "location": "Test Location",
    "stream_url": "rtsp://192.168.1.100:554/stream1",
    "status": "active"
  }'

# Test camera list
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:3002/api/v1/cameras
```

#### **Phase 3: Worker Pool Processing**

**Test Environment Setup**:
```bash
# 1. Check worker pool initialization
curl http://localhost:3002/api/v1/test/workers/status

# 2. Verify camera exists for testing
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:3002/api/v1/cameras
```

**Test Cases Execution Order**:
1. `WORKER-INIT-001`: Worker Pool Startup
2. `WORKER-INIT-002`: Worker Pool Shutdown
3. `WORKER-TASK-001`: Add Camera Task
4. `WORKER-TASK-002`: Remove Camera Task
5. `WORKER-TASK-003`: Duplicate Task Prevention
6. `WORKER-LOAD-001`: Multiple Camera Assignment
7. `WORKER-LOAD-002`: Worker Pool Exhaustion
8. `WORKER-FRAME-001`: Frame Processing Success
9. `WORKER-FRAME-002`: Stream Connection Error
10. `WORKER-FRAME-003`: Frame Processing Performance
11. `WORKER-ERR-001`: Worker Crash Recovery
12. `WORKER-ERR-002`: Memory Leak Prevention
13. `WORKER-MON-001`: Worker Status Monitoring
14. `WORKER-MON-002`: Performance Metrics Collection
15. `WORKER-INT-001`: Database Integration
16. `WORKER-INT-002`: Redis Cache Integration

**Tools & Commands**:
```bash
# Start camera processing
curl -X POST http://localhost:3002/api/v1/cameras/1/start \
  -H "Authorization: Bearer $TOKEN"

# Check processing status
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:3002/api/v1/cameras/1/status

# Stop camera processing
curl -X POST http://localhost:3002/api/v1/cameras/1/stop \
  -H "Authorization: Bearer $TOKEN"
```

#### **Phase 4: Frontend Integration**

**Test Environment Setup**:
```bash
# 1. Start frontend (if not running)
cd src && npm start

# 2. Verify frontend accessibility
curl http://localhost:3000

# 3. Check browser compatibility
# - Chrome (latest)
# - Firefox (latest)
# - Safari (latest)
```

**Test Cases Execution Order**:
1. `FE-AUTH-001`: Successful Login
2. `FE-AUTH-002`: Login with Invalid Credentials
3. `FE-AUTH-003`: Logout Functionality
4. `FE-ROUTE-001`: Access Protected Route with Valid Token
5. `FE-ROUTE-002`: Access Protected Route without Token
6. `FE-CAM-001`: Display Camera List
7. `FE-CAM-002`: Add New Camera
8. `FE-CAM-003`: Edit Camera
9. `FE-CAM-004`: Delete Camera
10. `FE-ANALYTICS-001`: Display Analytics Summary
11. `FE-ANALYTICS-002`: Real-time Count Updates
12. `FE-UI-001`: Responsive Design
13. `FE-UI-002`: Loading States
14. `FE-UI-003`: Error Handling
15. `FE-PERF-001`: Page Load Performance
16. `FE-PERF-002`: API Response Performance
17. `FE-BROWSER-001`: Chrome Compatibility
18. `FE-BROWSER-002`: Firefox Compatibility
19. `FE-BROWSER-003`: Safari Compatibility
20. `FE-SEC-001`: XSS Prevention
21. `FE-SEC-002`: CSRF Protection

**Manual Testing Steps**:
```bash
# 1. Open browser and navigate to http://localhost:3000
# 2. Test login functionality
# 3. Navigate through different pages
# 4. Test camera management features
# 5. Verify responsive design on different screen sizes
# 6. Test error scenarios
```

#### **Phase 5: Integration Testing**

**Test Environment Setup**:
```bash
# 1. Ensure all services are running
docker ps

# 2. Verify all health endpoints
curl http://localhost:3001/health
curl http://localhost:3002/health
curl http://localhost:3000

# 3. Check database connectivity
docker exec -it people_counting_db psql -U postgres -d people_counting_db -c "SELECT version();"
```

**Test Cases Execution Order**:
1. `INT-JOURNEY-001`: End-to-End User Registration & Login
2. `INT-JOURNEY-002`: Camera Management Workflow
3. `INT-COMM-001`: beAuth to beCamera Authentication
4. `INT-COMM-002`: Database Consistency Across Services
5. `INT-REALTIME-001`: Camera Processing to Analytics
6. `INT-REALTIME-002`: Cache Synchronization
7. `INT-ERROR-001`: Service Failure Recovery
8. `INT-ERROR-002`: Database Connection Failure
9. `INT-PERF-001`: Concurrent User Load
10. `INT-PERF-002`: Multiple Camera Processing
11. `INT-DATA-001`: User Data Consistency
12. `INT-DATA-002`: Camera Data Synchronization
13. `INT-SEC-001`: Cross-Service Authentication
14. `INT-SEC-002`: Role-Based Access Control
15. `INT-MON-001`: System Health Monitoring
16. `INT-MON-002`: Performance Metrics Collection

**Integration Test Commands**:
```bash
# Test complete user journey
# 1. Register user
# 2. Login user
# 3. Access camera management
# 4. Create camera
# 5. Start processing
# 6. Monitor analytics

# Test service communication
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:3002/api/v1/cameras

# Test real-time data flow
# Monitor database for count data updates
docker exec -it people_counting_db psql -U postgres -d people_counting_db -c "SELECT * FROM count_data ORDER BY timestamp DESC LIMIT 5;"
```

---

### 📊 **TEST REPORTING**

#### **Test Execution Template**
```markdown
## Test Execution Report

**Date**: [Date]
**Tester**: [Name]
**Environment**: [Development/Staging/Production]

### Summary
- **Total Test Cases**: 85
- **Passed**: [Number]
- **Failed**: [Number]
- **Skipped**: [Number]
- **Success Rate**: [Percentage]%

### Detailed Results

#### Workflow 1: Authentication Service
- **Test Cases**: 13
- **Passed**: [Number]
- **Failed**: [Number]
- **Issues**: [List any issues found]

#### Workflow 2: Camera Management API
- **Test Cases**: 18
- **Passed**: [Number]
- **Failed**: [Number]
- **Issues**: [List any issues found]

#### Workflow 3: Worker Pool Processing
- **Test Cases**: 16
- **Passed**: [Number]
- **Failed**: [Number]
- **Issues**: [List any issues found]

#### Workflow 4: Frontend Integration
- **Test Cases**: 22
- **Passed**: [Number]
- **Failed**: [Number]
- **Issues**: [List any issues found]

#### Integration Testing
- **Test Cases**: 16
- **Passed**: [Number]
- **Failed**: [Number]
- **Issues**: [List any issues found]

### Critical Issues
[List any critical issues that need immediate attention]

### Recommendations
[List recommendations for improvements]

### Sign-off
- **QA Lead**: [Name] - [Date]
- **Development Lead**: [Name] - [Date]
- **Project Manager**: [Name] - [Date]
```

#### **Bug Report Template**
```markdown
## Bug Report

**Bug ID**: [Auto-generated]
**Title**: [Brief description]
**Severity**: [Critical/High/Medium/Low]
**Priority**: [High/Medium/Low]
**Status**: [Open/In Progress/Fixed/Verified]

### Description
[Detailed description of the bug]

### Steps to Reproduce
1. [Step 1]
2. [Step 2]
3. [Step 3]

### Expected Result
[What should happen]

### Actual Result
[What actually happened]

### Environment
- **OS**: [Operating System]
- **Browser**: [Browser and version]
- **Service Versions**: [beAuth, beCamera, Frontend versions]

### Screenshots/Logs
[Attach relevant screenshots or logs]

### Additional Information
[Any other relevant information]
```

---

### 🎯 **ACCEPTANCE CRITERIA**

#### **Overall System Acceptance**
- ✅ All 130 test cases pass
- ✅ No critical bugs found
- ✅ Performance meets requirements
- ✅ Security measures verified
- ✅ User experience is satisfactory
- ✅ All dataflows validated
- ✅ Production deployment verified

#### **Performance Requirements**
- **API Response Time**: < 200ms
- **Page Load Time**: < 3 seconds
- **Concurrent Users**: Support 100+ users
- **Camera Processing**: > 10 FPS per camera
- **System Uptime**: > 99.9%

#### **Security Requirements**
- ✅ JWT authentication working
- ✅ Role-based access control implemented
- ✅ Input validation and sanitization
- ✅ XSS and CSRF protection
- ✅ Secure data transmission

---

### 📝 **NOTES & BEST PRACTICES**

#### **Test Execution Tips**
1. **Environment Isolation**: Use separate test environment
2. **Data Cleanup**: Reset database between test runs
3. **Documentation**: Document all findings and issues
4. **Communication**: Report issues immediately
5. **Regression Testing**: Re-test after bug fixes

#### **Common Issues & Solutions**
1. **Service Not Starting**: Check Docker containers and ports
2. **Database Connection**: Verify PostgreSQL is running
3. **Authentication Issues**: Check JWT token validity
4. **Performance Issues**: Monitor system resources
5. **Frontend Issues**: Clear browser cache and cookies

#### **Quality Gates**
- **Code Coverage**: > 80%
- **Performance**: Meet all performance requirements
- **Security**: Pass all security tests
- **Usability**: Pass all UX tests
- **Documentation**: Complete and up-to-date

---

### 🔄 **CONTINUOUS TESTING**

#### **Automated Testing Setup**
```bash
# Run automated tests
npm test

# Run specific test suites
npm run test:auth
npm run test:camera
npm run test:integration

# Generate test coverage report
npm run test:coverage
```

#### **Monitoring & Alerts**
- Set up monitoring for all services
- Configure alerts for critical issues
- Monitor performance metrics
- Track error rates and response times

---

**Test Execution Status**: 🔄 **READY TO START**  
**Estimated Duration**: 2-3 days  
**Team Size**: 2-3 QA Engineers  
**Risk Level**: Low  
**Confidence Level**: High 