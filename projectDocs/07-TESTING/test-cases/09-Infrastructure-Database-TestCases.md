# Infrastructure & Database Testing - Test Cases
## Test Cases cho Infrastructure và Database

### 🎯 **TỔNG QUAN**

**Mục tiêu**: Kiểm tra toàn bộ infrastructure và database của hệ thống  
**Phạm vi**: PostgreSQL, Redis, Docker Containers, Networking  
**Tổng số test cases**: 25 test cases  
**Thời gian ước tính**: 3 giờ  
**Priority**: CRITICAL  

---

### 📋 **TEST CASES**

#### **🔴 CRITICAL PRIORITY**

##### **TC-INFRA-001: PostgreSQL Database Connection**
- **ID**: TC-INFRA-001
- **Title**: PostgreSQL Database Connection Test
- **Description**: Kiểm tra kết nối database PostgreSQL
- **Precondition**: Docker containers đang chạy
- **Test Steps**:
  1. Kết nối đến PostgreSQL (Port 5432)
  2. Thực hiện query test: `SELECT version();`
  3. Kiểm tra response time
- **Expected Result**: 
  - Kết nối thành công
  - Response time < 50ms
  - Trả về PostgreSQL version
- **Priority**: Critical
- **Category**: Database

##### **TC-INFRA-002: Database Schema Validation**
- **ID**: TC-INFRA-002
- **Title**: Database Schema Validation
- **Description**: Kiểm tra schema database có đúng thiết kế
- **Precondition**: Database đã được migrate
- **Test Steps**:
  1. Kiểm tra bảng `users` có đủ columns
  2. Kiểm tra bảng `cameras` có đủ columns
  3. Kiểm tra bảng `count_data` có đủ columns
  4. Kiểm tra foreign key constraints
- **Expected Result**: 
  - Tất cả tables tồn tại
  - Columns đúng thiết kế
  - Constraints hoạt động
- **Priority**: Critical
- **Category**: Database

##### **TC-INFRA-003: Database Migration Scripts**
- **ID**: TC-INFRA-003
- **Title**: Database Migration Scripts Test
- **Description**: Kiểm tra scripts migration database
- **Precondition**: Database backup đã tạo
- **Test Steps**:
  1. Chạy migration scripts
  2. Kiểm tra tables được tạo
  3. Kiểm tra data integrity
  4. Test rollback migration
- **Expected Result**: 
  - Migration thành công
  - Data không bị mất
  - Rollback hoạt động
- **Priority**: Critical
- **Category**: Database

##### **TC-INFRA-004: Database Performance Test**
- **ID**: TC-INFRA-004
- **Title**: Database Performance Test
- **Description**: Kiểm tra performance database queries
- **Precondition**: Database có test data
- **Test Steps**:
  1. Thực hiện SELECT queries
  2. Thực hiện INSERT queries
  3. Thực hiện UPDATE queries
  4. Thực hiện DELETE queries
  5. Đo response time
- **Expected Result**: 
  - Tất cả queries < 100ms
  - Indexes hoạt động hiệu quả
  - Connection pooling hoạt động
- **Priority**: Critical
- **Category**: Database

##### **TC-INFRA-005: Redis Cache Connection**
- **ID**: TC-INFRA-005
- **Title**: Redis Cache Connection Test
- **Description**: Kiểm tra kết nối Redis cache
- **Precondition**: Redis container đang chạy
- **Test Steps**:
  1. Kết nối đến Redis (Port 6379)
  2. Thực hiện SET/GET operations
  3. Kiểm tra response time
- **Expected Result**: 
  - Kết nối thành công
  - SET/GET operations hoạt động
  - Response time < 10ms
- **Priority**: Critical
- **Category**: Cache

##### **TC-INFRA-006: Redis Session Management**
- **ID**: TC-INFRA-006
- **Title**: Redis Session Management Test
- **Description**: Kiểm tra quản lý session trong Redis
- **Precondition**: Redis đang chạy
- **Test Steps**:
  1. Tạo session data
  2. Store session trong Redis
  3. Retrieve session data
  4. Test session expiration
- **Expected Result**: 
  - Session được lưu trữ
  - Session được retrieve đúng
  - Expiration hoạt động
- **Priority**: Critical
- **Category**: Cache

##### **TC-INFRA-007: Redis Data Persistence**
- **ID**: TC-INFRA-007
- **Title**: Redis Data Persistence Test
- **Description**: Kiểm tra data persistence trong Redis
- **Precondition**: Redis đang chạy
- **Test Steps**:
  1. Lưu data vào Redis
  2. Restart Redis container
  3. Kiểm tra data còn lại
- **Expected Result**: 
  - Data được persist
  - Không mất data sau restart
- **Priority**: Critical
- **Category**: Cache

##### **TC-INFRA-008: Docker Container Health**
- **ID**: TC-INFRA-008
- **Title**: Docker Container Health Check
- **Description**: Kiểm tra health của tất cả containers
- **Precondition**: Docker Compose đang chạy
- **Test Steps**:
  1. Kiểm tra beAuth container (Port 3001)
  2. Kiểm tra beCamera container (Port 3002)
  3. Kiểm tra PostgreSQL container (Port 5432)
  4. Kiểm tra Redis container (Port 6379)
- **Expected Result**: 
  - Tất cả containers đang chạy
  - Health checks pass
  - Ports accessible
- **Priority**: Critical
- **Category**: Infrastructure

##### **TC-INFRA-009: Container Networking**
- **ID**: TC-INFRA-009
- **Title**: Container Networking Test
- **Description**: Kiểm tra networking giữa các containers
- **Precondition**: Tất cả containers đang chạy
- **Test Steps**:
  1. Test beAuth → PostgreSQL connection
  2. Test beCamera → PostgreSQL connection
  3. Test beCamera → Redis connection
  4. Test beAuth → beCamera communication
- **Expected Result**: 
  - Tất cả connections thành công
  - Network latency < 10ms
- **Priority**: Critical
- **Category**: Infrastructure

##### **TC-INFRA-010: Container Resource Usage**
- **ID**: TC-INFRA-010
- **Title**: Container Resource Usage Test
- **Description**: Kiểm tra resource usage của containers
- **Precondition**: Hệ thống đang chạy
- **Test Steps**:
  1. Monitor CPU usage
  2. Monitor memory usage
  3. Monitor disk usage
  4. Monitor network usage
- **Expected Result**: 
  - CPU < 70%
  - Memory < 80%
  - Disk < 90%
- **Priority**: Critical
- **Category**: Infrastructure

#### **🟡 HIGH PRIORITY**

##### **TC-INFRA-011: Database Index Performance**
- **ID**: TC-INFRA-011
- **Title**: Database Index Performance Test
- **Description**: Kiểm tra hiệu quả của database indexes
- **Precondition**: Database có test data
- **Test Steps**:
  1. Query với index
  2. Query không có index
  3. So sánh performance
  4. Kiểm tra index usage
- **Expected Result**: 
  - Indexed queries nhanh hơn
  - Index usage được report
- **Priority**: High
- **Category**: Database

##### **TC-INFRA-012: Database Connection Pooling**
- **ID**: TC-INFRA-012
- **Title**: Database Connection Pooling Test
- **Description**: Kiểm tra connection pooling
- **Precondition**: Database đang chạy
- **Test Steps**:
  1. Tạo multiple connections
  2. Monitor connection pool
  3. Test connection reuse
  4. Test connection limits
- **Expected Result**: 
  - Connection pooling hoạt động
  - Connections được reuse
  - Limits được enforce
- **Priority**: High
- **Category**: Database

##### **TC-INFRA-013: Redis Cache Performance**
- **ID**: TC-INFRA-013
- **Title**: Redis Cache Performance Test
- **Description**: Kiểm tra performance của Redis cache
- **Precondition**: Redis đang chạy
- **Test Steps**:
  1. Load test với nhiều operations
  2. Monitor response time
  3. Test cache hit/miss ratio
  4. Monitor memory usage
- **Expected Result**: 
  - Response time < 10ms
  - High cache hit ratio
  - Memory usage stable
- **Priority**: High
- **Category**: Cache

##### **TC-INFRA-014: Container Restart Recovery**
- **ID**: TC-INFRA-014
- **Title**: Container Restart Recovery Test
- **Description**: Kiểm tra recovery sau khi restart containers
- **Precondition**: Hệ thống đang chạy
- **Test Steps**:
  1. Restart beAuth container
  2. Restart beCamera container
  3. Restart PostgreSQL container
  4. Restart Redis container
  5. Kiểm tra system recovery
- **Expected Result**: 
  - Containers restart thành công
  - Services recover tự động
  - Data không bị mất
- **Priority**: High
- **Category**: Infrastructure

##### **TC-INFRA-015: Database Backup & Restore**
- **ID**: TC-INFRA-015
- **Title**: Database Backup & Restore Test
- **Description**: Kiểm tra backup và restore database
- **Precondition**: Database có test data
- **Test Steps**:
  1. Tạo database backup
  2. Restore database từ backup
  3. Kiểm tra data integrity
  4. Test backup compression
- **Expected Result**: 
  - Backup thành công
  - Restore thành công
  - Data integrity maintained
- **Priority**: High
- **Category**: Database

#### **🟢 MEDIUM PRIORITY**

##### **TC-INFRA-016: Database Concurrent Access**
- **ID**: TC-INFRA-016
- **Title**: Database Concurrent Access Test
- **Description**: Kiểm tra concurrent access database
- **Precondition**: Database đang chạy
- **Test Steps**:
  1. Tạo multiple concurrent connections
  2. Thực hiện concurrent reads
  3. Thực hiện concurrent writes
  4. Kiểm tra data consistency
- **Expected Result**: 
  - Concurrent access hoạt động
  - Data consistency maintained
  - No deadlocks
- **Priority**: Medium
- **Category**: Database

##### **TC-INFRA-017: Redis Cluster Scaling**
- **ID**: TC-INFRA-017
- **Title**: Redis Cluster Scaling Test
- **Description**: Kiểm tra Redis cluster scaling
- **Precondition**: Redis cluster setup
- **Test Steps**:
  1. Add Redis nodes
  2. Remove Redis nodes
  3. Test data distribution
  4. Test failover
- **Expected Result**: 
  - Scaling hoạt động
  - Data distribution balanced
  - Failover automatic
- **Priority**: Medium
- **Category**: Cache

##### **TC-INFRA-018: Container Orchestration**
- **ID**: TC-INFRA-018
- **Title**: Container Orchestration Test
- **Description**: Kiểm tra container orchestration
- **Precondition**: Orchestration platform setup
- **Test Steps**:
  1. Scale containers up/down
  2. Test load balancing
  3. Test service discovery
  4. Test rolling updates
- **Expected Result**: 
  - Orchestration hoạt động
  - Load balancing effective
  - Rolling updates smooth
- **Priority**: Medium
- **Category**: Infrastructure

##### **TC-INFRA-019: Database Monitoring**
- **ID**: TC-INFRA-019
- **Title**: Database Monitoring Test
- **Description**: Kiểm tra database monitoring
- **Precondition**: Monitoring tools setup
- **Test Steps**:
  1. Monitor query performance
  2. Monitor connection count
  3. Monitor disk usage
  4. Monitor slow queries
- **Expected Result**: 
  - Monitoring data collected
  - Alerts triggered properly
  - Performance metrics accurate
- **Priority**: Medium
- **Category**: Database

##### **TC-INFRA-020: Cache Invalidation**
- **ID**: TC-INFRA-020
- **Title**: Cache Invalidation Test
- **Description**: Kiểm tra cache invalidation
- **Precondition**: Redis đang chạy
- **Test Steps**:
  1. Cache data
  2. Invalidate cache
  3. Verify cache cleared
  4. Test TTL expiration
- **Expected Result**: 
  - Cache invalidation hoạt động
  - TTL expiration correct
  - Memory freed properly
- **Priority**: Medium
- **Category**: Cache

#### **🔵 LOW PRIORITY**

##### **TC-INFRA-021: Database Optimization**
- **ID**: TC-INFRA-021
- **Title**: Database Optimization Test
- **Description**: Kiểm tra database optimization
- **Precondition**: Database có production data
- **Test Steps**:
  1. Analyze query performance
  2. Optimize slow queries
  3. Update statistics
  4. Vacuum database
- **Expected Result**: 
  - Performance improved
  - Statistics updated
  - Database optimized
- **Priority**: Low
- **Category**: Database

##### **TC-INFRA-022: Redis Memory Management**
- **ID**: TC-INFRA-022
- **Title**: Redis Memory Management Test
- **Description**: Kiểm tra memory management Redis
- **Precondition**: Redis đang chạy
- **Test Steps**:
  1. Monitor memory usage
  2. Test memory limits
  3. Test eviction policies
  4. Test memory fragmentation
- **Expected Result**: 
  - Memory managed properly
  - Eviction policies work
  - No memory leaks
- **Priority**: Low
- **Category**: Cache

##### **TC-INFRA-023: Container Security**
- **ID**: TC-INFRA-023
- **Title**: Container Security Test
- **Description**: Kiểm tra security của containers
- **Precondition**: Containers đang chạy
- **Test Steps**:
  1. Scan container images
  2. Check container privileges
  3. Test network isolation
  4. Verify security policies
- **Expected Result**: 
  - No security vulnerabilities
  - Proper isolation
  - Security policies enforced
- **Priority**: Low
- **Category**: Infrastructure

##### **TC-INFRA-024: Database Replication**
- **ID**: TC-INFRA-024
- **Title**: Database Replication Test
- **Description**: Kiểm tra database replication
- **Precondition**: Replication setup
- **Test Steps**:
  1. Test master-slave replication
  2. Test failover
  3. Test data consistency
  4. Test replication lag
- **Expected Result**: 
  - Replication hoạt động
  - Failover automatic
  - Data consistent
- **Priority**: Low
- **Category**: Database

##### **TC-INFRA-025: Infrastructure Documentation**
- **ID**: TC-INFRA-025
- **Title**: Infrastructure Documentation Test
- **Description**: Kiểm tra documentation infrastructure
- **Precondition**: Documentation available
- **Test Steps**:
  1. Review setup guides
  2. Test troubleshooting procedures
  3. Verify configuration examples
  4. Check maintenance procedures
- **Expected Result**: 
  - Documentation complete
  - Procedures accurate
  - Examples working
- **Priority**: Low
- **Category**: Documentation

---

### 📊 **TEST EXECUTION SUMMARY**

#### **Test Categories**
- **Database Testing**: 10 test cases
- **Cache Testing**: 6 test cases  
- **Infrastructure Testing**: 6 test cases
- **Performance Testing**: 3 test cases

#### **Priority Distribution**
- **Critical**: 10 test cases
- **High**: 5 test cases
- **Medium**: 5 test cases
- **Low**: 5 test cases

#### **Execution Time Estimate**
- **Critical Tests**: 1.5 giờ
- **High Priority Tests**: 1 giờ
- **Medium Priority Tests**: 0.5 giờ
- **Total**: 3 giờ

---

### 🎯 **ACCEPTANCE CRITERIA**

#### **Database Requirements**
- ✅ All database connections successful
- ✅ Query performance < 100ms
- ✅ Schema validation passed
- ✅ Migration scripts working
- ✅ Backup/restore functional

#### **Cache Requirements**
- ✅ Redis connections successful
- ✅ Session management working
- ✅ Data persistence verified
- ✅ Performance < 10ms
- ✅ Memory management proper

#### **Infrastructure Requirements**
- ✅ All containers healthy
- ✅ Networking functional
- ✅ Resource usage optimal
- ✅ Security policies enforced
- ✅ Monitoring operational

---

**Test Lead**: [Tên Test Lead]  
**Created**: [Ngày tạo]  
**Last Updated**: [Ngày cập nhật]  
**Status**: Ready for Execution 