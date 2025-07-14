# 🔧 **BACKEND TEST CASES - AI Camera Counting System**

## 📊 **OVERVIEW**

Tài liệu này tổng hợp tất cả các test cases dành cho backend services của hệ thống AI Camera Counting.

---

## 🏗️ **BACKEND SERVICES**

### **🔐 Authentication Service (beAuth)**
- **Port**: 3001
- **Technology**: Node.js, Express, PostgreSQL, Redis
- **Test Cases**: 12 test cases

### **📹 Camera Management Service (beCamera)**
- **Port**: 3002
- **Technology**: Python, FastAPI, PostgreSQL, Redis
- **Test Cases**: 15 test cases

### **🗄️ Database Service**
- **Port**: 5432
- **Technology**: PostgreSQL
- **Test Cases**: 8 test cases

### **🔌 WebSocket Service**
- **Port**: 3003
- **Technology**: Python, WebSocket
- **Test Cases**: 6 test cases

---

## 📋 **TEST CASE CATEGORIES**

### **1. Authentication Service Tests**
| Test Case ID | Test Case Name | Priority | Type | Status |
|--------------|----------------|----------|------|--------|
| AUTH-REG-001 | Successful User Registration | High | Positive | Pending |
| AUTH-REG-002 | Registration with Invalid Code | High | Negative | Pending |
| AUTH-REG-003 | Registration with Duplicate Username | High | Negative | Pending |
| AUTH-LOGIN-001 | Successful Login with Username | High | Positive | Pending |
| AUTH-LOGIN-002 | Login with Invalid Credentials | High | Negative | Pending |
| AUTH-TOKEN-001 | Refresh Access Token | High | Positive | Pending |
| AUTH-TOKEN-002 | Logout User | Medium | Positive | Pending |
| AUTH-PROFILE-001 | Get User Profile | Medium | Positive | Pending |
| AUTH-PROFILE-002 | Update User Profile | Medium | Positive | Pending |
| AUTH-SEC-001 | Rate Limiting | High | Security | Pending |
| AUTH-SEC-002 | Password Validation | High | Validation | Pending |
| AUTH-ERR-001 | Database Connection Error | Medium | Error Handling | Pending |

### **2. Camera Management API Tests**
| Test Case ID | Test Case Name | Priority | Type | Status |
|--------------|----------------|----------|------|--------|
| CAM-CREATE-001 | Create New Camera | High | Positive | Pending |
| CAM-CREATE-002 | Create Camera with Invalid Data | High | Negative | Pending |
| CAM-READ-001 | Get All Cameras | Medium | Positive | Pending |
| CAM-READ-002 | Get Camera by ID | Medium | Positive | Pending |
| CAM-READ-003 | Get Non-existent Camera | Medium | Negative | Pending |
| CAM-UPDATE-001 | Update Camera Information | High | Positive | Pending |
| CAM-UPDATE-002 | Update Camera with Invalid Data | High | Negative | Pending |
| CAM-DELETE-001 | Delete Camera | High | Positive | Pending |
| CAM-DELETE-002 | Delete Non-existent Camera | Medium | Negative | Pending |
| CAM-STATUS-001 | Update Camera Status | High | Positive | Pending |
| CAM-STATUS-002 | Get Camera Status | Medium | Positive | Pending |
| CAM-START-001 | Start Camera Processing | High | Positive | Pending |
| CAM-STOP-001 | Stop Camera Processing | High | Positive | Pending |
| CAM-COUNT-001 | Get Count Data | Medium | Positive | Pending |
| CAM-ANALYTICS-001 | Get Analytics Summary | Medium | Positive | Pending |

### **3. Worker Pool Processing Tests**
| Test Case ID | Test Case Name | Priority | Type | Status |
|--------------|----------------|----------|------|--------|
| WORKER-STATUS-001 | Get Worker Pool Status | Medium | Positive | Pending |
| WORKER-SCALE-001 | Scale Worker Pool Up | High | Positive | Pending |
| WORKER-SCALE-002 | Scale Worker Pool Down | High | Positive | Pending |
| WORKER-TASK-001 | Submit Processing Task | High | Positive | Pending |
| WORKER-TASK-002 | Cancel Processing Task | Medium | Positive | Pending |
| WORKER-TASK-003 | Get Task Status | Medium | Positive | Pending |
| WORKER-ERROR-001 | Handle Worker Error | High | Error Handling | Pending |
| WORKER-PERF-001 | Worker Performance Test | Medium | Performance | Pending |

### **4. Database Tests**
| Test Case ID | Test Case Name | Priority | Type | Status |
|--------------|----------------|----------|------|--------|
| DB-CONN-001 | Database Connection Test | High | Positive | Pending |
| DB-QUERY-001 | Basic Query Performance | Medium | Performance | Pending |
| DB-INTEGRITY-001 | Data Integrity Check | High | Validation | Pending |
| DB-BACKUP-001 | Database Backup Test | Medium | Positive | Pending |
| DB-RESTORE-001 | Database Restore Test | Medium | Positive | Pending |
| DB-MIGRATION-001 | Schema Migration Test | High | Positive | Pending |
| DB-INDEX-001 | Index Performance Test | Medium | Performance | Pending |
| DB-CONCURRENT-001 | Concurrent Access Test | High | Stress | Pending |

### **5. Integration Tests**
| Test Case ID | Test Case Name | Priority | Type | Status |
|--------------|----------------|----------|------|--------|
| INT-AUTH-CAM-001 | Auth-Camera Service Integration | High | Integration | Pending |
| INT-CAM-WS-001 | Camera-WebSocket Integration | High | Integration | Pending |
| INT-DB-REDIS-001 | Database-Redis Integration | Medium | Integration | Pending |
| INT-API-FRONT-001 | API-Frontend Integration | High | Integration | Pending |
| INT-ERROR-001 | Cross-service Error Handling | High | Error Handling | Pending |
| INT-PERF-001 | End-to-end Performance | Medium | Performance | Pending |

### **6. Security Tests**
| Test Case ID | Test Case Name | Priority | Type | Status |
|--------------|----------------|----------|------|--------|
| SEC-JWT-001 | JWT Token Validation | High | Security | Pending |
| SEC-SQL-001 | SQL Injection Prevention | High | Security | Pending |
| SEC-XSS-001 | XSS Prevention | High | Security | Pending |
| SEC-CORS-001 | CORS Configuration | Medium | Security | Pending |
| SEC-RATE-001 | Rate Limiting | High | Security | Pending |
| SEC-AUTH-001 | Authentication Bypass | High | Security | Pending |
| SEC-SESSION-001 | Session Management | Medium | Security | Pending |
| SEC-INPUT-001 | Input Validation | High | Security | Pending |

### **7. Performance Tests**
| Test Case ID | Test Case Name | Priority | Type | Status |
|--------------|----------------|----------|------|--------|
| PERF-LOAD-001 | Load Testing (100 users) | Medium | Performance | Pending |
| PERF-STRESS-001 | Stress Testing (500 users) | High | Performance | Pending |
| PERF-SPIKE-001 | Spike Testing (1000 users) | High | Performance | Pending |
| PERF-MEMORY-001 | Memory Usage Test | Medium | Performance | Pending |
| PERF-RESPONSE-001 | Response Time Test | High | Performance | Pending |
| PERF-THROUGHPUT-001 | Throughput Test | Medium | Performance | Pending |

---

## 🎯 **TEST EXECUTION STRATEGY**

### **📋 Execution Order**
1. **Database Tests** (Foundation)
2. **Authentication Service Tests** (Core)
3. **Camera Management API Tests** (Core)
4. **Worker Pool Processing Tests** (Core)
5. **Integration Tests** (Cross-service)
6. **Security Tests** (Security)
7. **Performance Tests** (Performance)

### **⚙️ Test Environment**
- **Environment**: Development (Docker)
- **Database**: PostgreSQL (Port 5432)
- **Cache**: Redis (Port 6379)
- **API Base URL**: http://localhost:3001/api/v1
- **Camera API URL**: http://localhost:3002/api/v1
- **WebSocket URL**: ws://localhost:3003

### **🔧 Test Tools**
- **API Testing**: curl, HTTP requests, Newman
- **Database Testing**: PostgreSQL queries, Python scripts
- **Performance Testing**: Artillery, Apache Bench
- **Security Testing**: OWASP ZAP, custom scripts
- **Monitoring**: Health checks, logs analysis

---

## 📊 **TEST DATA REQUIREMENTS**

### **🔐 Authentication Test Data**
```json
{
  "test_users": [
    {
      "username": "admin",
      "email": "admin@aicamera.com",
      "password": "Admin123!",
      "role": "admin"
    },
    {
      "username": "user1",
      "email": "user1@aicamera.com",
      "password": "User123!",
      "role": "user"
    }
  ],
  "registration_codes": [
    {
      "code": "REG001",
      "max_uses": 100,
      "is_active": true
    }
  ]
}
```

### **📹 Camera Test Data**
```json
{
  "test_cameras": [
    {
      "name": "Test Camera 1",
      "location": "Test Location 1",
      "stream_url": "rtsp://test-camera-1.example.com/stream",
      "status": "active"
    },
    {
      "name": "Test Camera 2",
      "location": "Test Location 2",
      "stream_url": "rtsp://test-camera-2.example.com/stream",
      "status": "maintenance"
    }
  ]
}
```

---

## 📝 **TEST EXECUTION LOG**

### **📊 Progress Summary**
- **Total Backend Test Cases**: 67
- **Completed**: 0
- **In Progress**: 0
- **Pending**: 67
- **Passed**: 0
- **Failed**: 0
- **Success Rate**: 0%

### **🔄 Execution Log**
- **Start Date**: TBD
- **Expected Duration**: 8 hours
- **Current Status**: Planning Phase

---

## 🎯 **ACCEPTANCE CRITERIA**

### **✅ Functional Requirements**
- [ ] All API endpoints return correct HTTP status codes
- [ ] JWT tokens are properly generated and validated
- [ ] Database operations are atomic and consistent
- [ ] Error handling provides meaningful messages
- [ ] Input validation rejects invalid data

### **✅ Performance Requirements**
- [ ] API response time < 200ms for 95% of requests
- [ ] Database query time < 100ms for 95% of queries
- [ ] System can handle 100 concurrent users
- [ ] Memory usage remains stable under load

### **✅ Security Requirements**
- [ ] JWT tokens are properly secured
- [ ] SQL injection attempts are blocked
- [ ] XSS attempts are prevented
- [ ] Rate limiting prevents abuse
- [ ] CORS is properly configured

### **✅ Reliability Requirements**
- [ ] System uptime > 99.9%
- [ ] Database connection pool works correctly
- [ ] Error recovery mechanisms work
- [ ] Logging captures all important events

---

## 📞 **SUPPORT & CONTACT**

### **👥 Team Contacts**
- **QA Lead**: qa@aicamera.com
- **Backend Team**: backend@aicamera.com
- **DevOps Team**: devops@aicamera.com

### **📚 Documentation**
- **API Documentation**: `projectDocs/02-API-DOCUMENTATION/`
- **Database Schema**: `projectDocs/03-DATABASE/`
- **Testing Guide**: `projectDocs/07-TESTING/`

---

**📅 Created**: 2025-01-09  
**👥 Maintainer**: QA Team  
**�� Version**: 1.0.0 