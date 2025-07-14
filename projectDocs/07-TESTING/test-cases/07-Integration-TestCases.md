# Integration Testing - Test Cases
## Workflow 5: End-to-End System Integration

### 📋 **WORKFLOW OVERVIEW**

**Scope**: Complete system integration testing  
**Services**: beAuth (3001) + beCamera (3002) + Frontend (3000)  
**Database**: PostgreSQL (5432)  
**Cache**: Redis (6379)  
**Testing**: End-to-end workflows  

#### **Current System Architecture**
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │───▶│  beAuth         │───▶│  PostgreSQL     │
│   (Port 3000)   │    │  (Port 3001)    │    │  (Port 5432)    │
│   [Unhealthy]   │    │  [Unhealthy]    │    │  [Healthy]      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  beCamera       │───▶│  Worker Pool    │───▶│  Redis Cache    │
│  (Port 3002)    │    │  (4 Workers)    │    │  (Port 6379)    │
│  [Unhealthy]    │    │  [Active]       │    │  [Healthy]      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  WebSocket      │    │  Analytics      │    │  Monitoring     │
│  (Port 3004)    │    │  Processing     │    │  & Logging      │
│  [Unhealthy]    │    │  [Active]       │    │  [Active]       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

#### **Current System Status**
- ✅ **Database**: PostgreSQL healthy and accessible
- ✅ **Cache**: Redis healthy and accessible  
- ✅ **Authentication**: JWT token validation working
- ✅ **Rate Limiting**: Implemented (10 requests/minute per user)
- ⚠️ **Services**: All services running but health checks failing
- ⚠️ **Frontend**: React app accessible but health check failing

#### **Key Integration Points**
- Authentication flow across all services (JWT token validation)
- Camera management with real-time processing
- Data consistency across shared database
- Cache synchronization between services
- Error propagation and handling
- Performance under load with rate limiting
- WebSocket real-time communication

---

### 🧪 **TEST CASE 5.1: Complete User Journey**

#### **Test Case ID**: `INT-JOURNEY-001`
#### **Test Case Name**: End-to-End User Registration & Login
#### **Priority**: High
#### **Test Type**: Positive

**Preconditions**:
- All services running (beAuth, beCamera, Frontend)
- Database and Redis accessible
- Clean test environment

**Test Steps**:
1. **Frontend**: Navigate to registration page
2. **Frontend**: Fill registration form
3. **beAuth**: Verify registration API call (`POST /api/v1/auth/register`)
4. **Database**: Confirm user creation in `users` table
5. **Frontend**: Complete registration flow
6. **Frontend**: Navigate to login page
7. **beAuth**: Verify login API call (`POST /api/v1/auth/login`)
8. **Frontend**: Access protected dashboard with JWT token

**Test Data**:
```json
{
  "username": "integration_user",
  "email": "integration@test.com",
  "password": "IntegrationPass123!",
  "confirmPassword": "IntegrationPass123!",
  "firstName": "Integration",
  "lastName": "User",
  "registrationCode": "REG001"
}
```

**Expected Results**:
- **Frontend**: Registration form works correctly
- **beAuth**: Registration API returns 201 with user data
- **Database**: User record created with hashed password
- **Frontend**: Login form works correctly
- **beAuth**: Login API returns 200 with JWT tokens
- **Frontend**: Dashboard accessible after login
- **State**: User authenticated across all components

---

#### **Test Case ID**: `INT-JOURNEY-002`
#### **Test Case Name**: Camera Management Workflow
#### **Priority**: High
#### **Test Type**: Positive

**Preconditions**: User is authenticated with valid JWT token

**Test Steps**:
1. **Frontend**: Navigate to camera management
2. **beCamera**: Verify camera list API call (`GET /api/v1/cameras`)
3. **Frontend**: Add new camera
4. **beCamera**: Verify camera creation API (`POST /api/v1/cameras`)
5. **Database**: Confirm camera record creation in `cameras` table
6. **Frontend**: Start camera processing
7. **Worker Pool**: Verify task assignment
8. **Frontend**: Monitor real-time updates via WebSocket

**Test Data**:
```json
{
  "name": "Integration Test Camera",
  "location": "Test Building - Main Entrance",
  "stream_url": "rtsp://192.168.1.150:554/stream1",
  "status": "active"
}
```

**Expected Results**:
- **Frontend**: Camera list displays correctly
- **beCamera**: Camera creation API returns 201
- **Database**: Camera record created with user_id
- **Worker Pool**: Camera task assigned to worker
- **Frontend**: Real-time status updates via WebSocket
- **Analytics**: Count data generated and stored in `count_data` table

---

### 🧪 **TEST CASE 5.2: Service Communication**

#### **Test Case ID**: `INT-COMM-001`
#### **Test Case Name**: beAuth to beCamera Authentication
#### **Priority**: High
#### **Test Type**: Integration

**Preconditions**: User has valid JWT token

**Test Steps**:
1. **Frontend**: Make authenticated request to beCamera
2. **beCamera**: Verify JWT token with beAuth (`POST /api/v1/auth/verify`)
3. **beAuth**: Validate token and return user data
4. **beCamera**: Process request with user context

**Expected Results**:
- **beAuth**: Token validation successful (200 response)
- **beCamera**: Request processed with user context
- **Response**: Proper data returned to frontend
- **Security**: Authentication flow secure across services

---

#### **Test Case ID**: `INT-COMM-002`
#### **Test Case Name**: Database Consistency Across Services
#### **Priority**: High
#### **Test Type**: Integration

**Test Steps**:
1. **beAuth**: Create user record in `users` table
2. **beCamera**: Verify user access via JWT validation
3. **Database**: Check data consistency across tables
4. **Frontend**: Display user data from both services

**Expected Results**:
- **Database**: Consistent user data across `users`, `cameras`, `count_data` tables
- **beAuth**: User creation successful with proper hashing
- **beCamera**: User access verified via JWT
- **Frontend**: Correct user data displayed
- **Integrity**: No data corruption or inconsistency

---

### 🧪 **TEST CASE 5.3: Real-time Data Flow**

#### **Test Case ID**: `INT-REALTIME-001`
#### **Test Case Name**: Camera Processing to Analytics
#### **Priority**: High
#### **Test Type**: Integration

**Preconditions**: Camera is processing with valid stream

**Test Steps**:
1. **Worker Pool**: Process camera frames from stream
2. **AI Processing**: Generate count data using OpenCV
3. **Database**: Store count records in `count_data` table
4. **Analytics**: Calculate summary statistics
5. **Frontend**: Display real-time analytics via WebSocket

**Expected Results**:
- **Processing**: Frames processed continuously (>10 FPS)
- **Database**: Count data stored in real-time with timestamps
- **Analytics**: Summary calculations accurate
- **Frontend**: Real-time updates via WebSocket connection
- **Performance**: No lag in data flow

---

#### **Test Case ID**: `INT-REALTIME-002`
#### **Test Case Name**: WebSocket Communication
#### **Priority**: Medium
#### **Test Type**: Integration

**Test Steps**:
1. **Frontend**: Establish WebSocket connection to port 3004
2. **beCamera**: Send real-time count updates
3. **Frontend**: Receive and display live data
4. **Connection**: Test connection stability and reconnection

**Expected Results**:
- **WebSocket**: Connection established successfully
- **Data Flow**: Real-time count data transmitted
- **Frontend**: Live updates displayed correctly
- **Stability**: Connection remains stable during processing
- **Reconnection**: Automatic reconnection on disconnect

---

### 🧪 **TEST CASE 5.4: Error Handling & Recovery**

#### **Test Case ID**: `INT-ERROR-001`
#### **Test Case Name**: Service Failure Recovery
#### **Priority**: High
#### **Test Type**: Error Handling

**Test Steps**:
1. **Simulate**: beAuth service failure
2. **Frontend**: Attempt authenticated request to beCamera
3. **beCamera**: Handle authentication failure gracefully
4. **Recovery**: Restart beAuth service
5. **Verify**: System recovery and functionality

**Expected Results**:
- **Error Handling**: Graceful error handling with proper HTTP codes
- **User Experience**: Clear error messages displayed
- **Recovery**: System recovers after service restart
- **Data**: No data loss during failure
- **Logging**: Errors logged appropriately in service logs

---

#### **Test Case ID**: `INT-ERROR-002`
#### **Test Case Name**: Rate Limiting Behavior
#### **Priority**: High
#### **Test Type**: Error Handling

**Test Steps**:
1. **Load Test**: Send 15 requests in 1 minute to beCamera
2. **Rate Limiting**: Verify rate limiting kicks in after 10 requests
3. **Response**: Check 429 Too Many Requests response
4. **Recovery**: Wait for rate limit window to reset
5. **Verify**: Normal functionality restored

**Expected Results**:
- **Rate Limiting**: 429 response after 10 requests/minute
- **Headers**: Proper rate limit headers included
- **Recovery**: Normal access restored after window expires
- **User Experience**: Clear rate limit error message
- **Security**: Rate limiting prevents abuse

---

### 🧪 **TEST CASE 5.5: Performance Under Load**

#### **Test Case ID**: `INT-PERF-001`
#### **Test Case Name**: Concurrent User Load
#### **Priority**: Medium
#### **Test Type**: Performance

**Test Steps**:
1. **Load Test**: 50 concurrent users (respecting rate limits)
2. **Monitor**: System performance metrics
3. **Verify**: Response times and throughput
4. **Check**: Resource utilization

**Expected Results**:
- **Response Time**: < 200ms for API calls
- **Throughput**: Handle 50+ concurrent users
- **CPU Usage**: < 80% across all services
- **Memory Usage**: Stable memory consumption
- **Database**: Efficient query performance

---

#### **Test Case ID**: `INT-PERF-002`
#### **Test Case Name**: Multiple Camera Processing
#### **Priority**: Medium
#### **Test Type**: Performance

**Test Steps**:
1. **Setup**: 4 cameras processing simultaneously
2. **Monitor**: Worker pool performance
3. **Verify**: Frame processing rates
4. **Check**: System stability

**Expected Results**:
- **Processing**: All cameras processed simultaneously
- **Performance**: > 10 FPS per camera
- **Stability**: System remains stable
- **Memory**: Efficient memory usage
- **CPU**: Balanced CPU utilization across workers

---

### 🧪 **TEST CASE 5.6: Data Integrity & Consistency**

#### **Test Case ID**: `INT-DATA-001`
#### **Test Case Name**: User Data Consistency
#### **Priority**: High
#### **Test Type**: Data Integrity

**Test Steps**:
1. **beAuth**: Update user profile via API
2. **Database**: Verify data consistency in `users` table
3. **beCamera**: Access updated user data via JWT
4. **Frontend**: Display updated information

**Expected Results**:
- **Consistency**: User data consistent across services
- **Updates**: Profile updates reflected everywhere
- **Integrity**: No data corruption
- **Performance**: Fast data access

---

#### **Test Case ID**: `INT-DATA-002`
#### **Test Case Name**: Camera Data Synchronization
#### **Priority**: High
#### **Test Type**: Data Integrity

**Test Steps**:
1. **Frontend**: Update camera settings via API
2. **beCamera**: Process camera update
3. **Database**: Verify data persistence in `cameras` table
4. **Worker Pool**: Apply updated settings to processing

**Expected Results**:
- **Synchronization**: Camera data synchronized
- **Persistence**: Data persisted correctly
- **Application**: Settings applied to processing
- **Consistency**: Data consistent across components

---

### 🧪 **TEST CASE 5.7: Security Integration**

#### **Test Case ID**: `INT-SEC-001`
#### **Test Case Name**: Cross-Service Authentication
#### **Priority**: High
#### **Test Type**: Security

**Test Steps**:
1. **Frontend**: Login with valid credentials
2. **beAuth**: Generate JWT token with proper claims
3. **beCamera**: Validate token for requests
4. **Verify**: Secure communication between services

**Expected Results**:
- **Authentication**: Secure token validation
- **Authorization**: Proper access control
- **Security**: No unauthorized access
- **Communication**: Encrypted data transmission

---

#### **Test Case ID**: `INT-SEC-002`
#### **Test Case Name**: Input Validation & Sanitization
#### **Priority**: Medium
#### **Test Type**: Security

**Test Steps**:
1. **Test**: SQL injection attempts in user inputs
2. **Test**: XSS attempts in camera names/locations
3. **Test**: Malicious file uploads
4. **Verify**: Proper input validation and sanitization

**Expected Results**:
- **SQL Injection**: Properly blocked and logged
- **XSS**: Input sanitized and safe
- **File Uploads**: Validated and restricted
- **Security**: No vulnerabilities exploited

---

### 🧪 **TEST CASE 5.8: Monitoring & Observability**

#### **Test Case ID**: `INT-MON-001`
#### **Test Case Name**: System Health Monitoring
#### **Priority**: Medium
#### **Test Type**: Monitoring

**Test Steps**:
1. **Monitor**: All service health endpoints
2. **Verify**: Health check responses
3. **Check**: Log aggregation
4. **Test**: Alert mechanisms

**Expected Results**:
- **Health Checks**: All services report status
- **Logging**: Centralized log collection
- **Monitoring**: Real-time system metrics
- **Alerts**: Proper alert mechanisms

---

#### **Test Case ID**: `INT-MON-002`
#### **Test Case Name**: Performance Metrics Collection
#### **Priority**: Medium
#### **Test Type**: Monitoring

**Test Steps**:
1. **Collect**: Performance metrics from all services
2. **Aggregate**: Centralized metrics collection
3. **Visualize**: Dashboard metrics display
4. **Alert**: Performance threshold alerts

**Expected Results**:
- **Metrics**: Comprehensive performance data
- **Collection**: Efficient metrics gathering
- **Visualization**: Clear metrics display
- **Alerts**: Timely performance alerts

---

### 📊 **TEST EXECUTION MATRIX**

| Test Case | Priority | Status | Executed By | Date | Notes |
|-----------|----------|--------|-------------|------|-------|
| INT-JOURNEY-001 | High | 🔄 | | | |
| INT-JOURNEY-002 | High | 🔄 | | | |
| INT-COMM-001 | High | ✅ | | | JWT validation working |
| INT-COMM-002 | High | 🔄 | | | |
| INT-REALTIME-001 | High | 🔄 | | | |
| INT-REALTIME-002 | Medium | 🔄 | | | |
| INT-ERROR-001 | High | 🔄 | | | |
| INT-ERROR-002 | High | ✅ | | | Rate limiting working |
| INT-PERF-001 | Medium | 🔄 | | | |
| INT-PERF-002 | Medium | 🔄 | | | |
| INT-DATA-001 | High | 🔄 | | | |
| INT-DATA-002 | High | 🔄 | | | |
| INT-SEC-001 | High | ✅ | | | Authentication working |
| INT-SEC-002 | Medium | ✅ | | | Input validation implemented |
| INT-MON-001 | Medium | 🔄 | | | |
| INT-MON-002 | Medium | 🔄 | | | |

### 🎯 **ACCEPTANCE CRITERIA**

- ✅ All services communicate seamlessly
- ✅ End-to-end user journeys work correctly
- ✅ Data consistency maintained across services
- ✅ Real-time data flow functions properly
- ✅ Error handling and recovery work effectively
- ✅ Performance meets requirements under load
- ✅ Security measures protect the entire system
- ✅ Monitoring provides comprehensive visibility
- ✅ System remains stable during failures
- ✅ Integration points handle edge cases

### 📝 **CURRENT IMPLEMENTATION STATUS**

#### **✅ Completed Features**
- JWT-based authentication between services
- Rate limiting (10 requests/minute per user)
- Input validation and sanitization
- Database consistency across services
- Real-time WebSocket communication
- Error handling and logging
- Security measures (SQL injection, XSS protection)
- **Health check endpoints working for all services**
- **Docker health checks properly configured**

#### **✅ Current System Health**
- **beAuth Service**: Healthy ✅ (Port 3001)
- **beCamera Service**: Healthy ✅ (Port 3002)
- **WebSocket Service**: Healthy ✅ (Port 3004)
- **PostgreSQL Database**: Healthy ✅ (Port 5432)
- **Redis Cache**: Healthy ✅ (Port 6379)
- **Frontend**: Accessible but health check needs fixing ⚠️ (Port 3000)

#### **🔄 Next Steps**
1. ✅ ~~Fix service health check endpoints~~ **COMPLETED**
2. Complete integration test automation
3. Implement comprehensive E2E testing
4. Add performance monitoring
5. Enhance error recovery mechanisms
6. Fix frontend health check 