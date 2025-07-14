# Worker Pool Processing - Test Cases
## Workflow 3: AI Camera Stream Processing

### 📋 **WORKFLOW OVERVIEW**

**Component**: Python Worker Pool for Camera Stream Processing  
**Service**: beCamera (Port 3002)  
**Technology**: OpenCV, asyncio, ThreadPoolExecutor  
**Workers**: 4 concurrent workers  
**Processing**: Real-time AI people counting  

#### **Workflow Diagram**
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Camera        │───▶│  Worker Pool    │───▶│  AI Processing  │
│   Stream        │    │  Manager        │    │  (OpenCV)       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Task Queue     │    │  Worker         │    │  Frame          │
│  Management     │    │  Assignment     │    │  Analysis       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Database       │    │  Real-time      │    │  Analytics      │
│  Storage        │    │  Updates        │    │  Generation     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

#### **Key Features**
- Concurrent processing of multiple camera streams
- Automatic worker assignment and load balancing
- Real-time frame processing with OpenCV
- Error handling and recovery mechanisms
- Performance monitoring and metrics
- Graceful shutdown and cleanup

---

### 🧪 **TEST CASE 3.1: Worker Pool Initialization**

#### **Test Case ID**: `WORKER-INIT-001`
#### **Test Case Name**: Worker Pool Startup
#### **Priority**: High
#### **Test Type**: Positive

**Preconditions**:
- beCamera service is starting
- System resources are available
- OpenCV is properly installed

**Test Steps**:
1. Start beCamera service
2. Monitor worker pool initialization
3. Verify worker status

**Expected Results**:
- **Status**: All 4 workers initialized as "idle"
- **Logs**: "Worker pool started with 4 workers"
- **Memory**: Efficient memory allocation
- **Response**: Worker pool ready for tasks

**API Response**:
```json
{
  "success": true,
  "data": {
    "workers": [
      {
        "worker_id": "worker_1",
        "status": "idle",
        "current_task": null,
        "start_time": null,
        "processed_frames": 0,
        "error_count": 0
      },
      {
        "worker_id": "worker_2",
        "status": "idle",
        "current_task": null,
        "start_time": null,
        "processed_frames": 0,
        "error_count": 0
      }
    ],
    "total_workers": 4,
    "idle_workers": 4,
    "busy_workers": 0
  }
}
```

---

#### **Test Case ID**: `WORKER-INIT-002`
#### **Test Case Name**: Worker Pool Shutdown
#### **Priority**: High
#### **Test Type**: Positive

**Preconditions**: Worker pool is running with active tasks

**Test Steps**:
1. Stop beCamera service
2. Monitor graceful shutdown
3. Verify cleanup

**Expected Results**:
- **Status**: All workers stopped gracefully
- **Logs**: "Worker pool stopped"
- **Memory**: All resources released
- **Tasks**: All active tasks terminated properly

---

### 🧪 **TEST CASE 3.2: Task Management**

#### **Test Case ID**: `WORKER-TASK-001`
#### **Test Case Name**: Add Camera Task
#### **Priority**: High
#### **Test Type**: Positive

**Preconditions**: Worker pool is running with idle workers

**Test Data**:
```json
{
  "camera_id": 1,
  "stream_url": "rtsp://192.168.1.100:554/stream1"
}
```

**Test Steps**:
1. Send POST request to `/api/v1/cameras/1/start`
2. Monitor task assignment
3. Verify worker status

**Expected Results**:
- **Status Code**: 200 OK
- **Response**:
```json
{
  "success": true,
  "data": {
    "camera_id": 1,
    "status": "processing",
    "worker_id": "worker_1",
    "message": "Camera processing started"
  }
}
```
- **Worker Status**: One worker becomes "busy"
- **Task Queue**: Task properly assigned

---

#### **Test Case ID**: `WORKER-TASK-002`
#### **Test Case Name**: Remove Camera Task
#### **Priority**: High
#### **Test Type**: Positive

**Preconditions**: Camera task is running on worker

**Test Steps**:
1. Send POST request to `/api/v1/cameras/1/stop`
2. Monitor task removal
3. Verify worker status

**Expected Results**:
- **Status Code**: 200 OK
- **Response**:
```json
{
  "success": true,
  "data": {
    "camera_id": 1,
    "status": "stopped",
    "message": "Camera processing stopped"
  }
}
```
- **Worker Status**: Worker returns to "idle"
- **Task Queue**: Task properly removed

---

#### **Test Case ID**: `WORKER-TASK-003`
#### **Test Case Name**: Duplicate Task Prevention
#### **Priority**: Medium
#### **Test Type**: Negative

**Preconditions**: Camera task is already running

**Test Steps**:
1. Try to add same camera task again
2. Verify duplicate prevention

**Expected Results**:
- **Status Code**: 400 Bad Request
- **Response**: "Camera already has a task"
- **Worker Status**: No change in worker assignment

---

### 🧪 **TEST CASE 3.3: Load Balancing**

#### **Test Case ID**: `WORKER-LOAD-001`
#### **Test Case Name**: Multiple Camera Assignment
#### **Priority**: High
#### **Test Type**: Positive

**Preconditions**: Worker pool with 4 idle workers

**Test Steps**:
1. Start processing on 4 different cameras
2. Monitor worker assignment
3. Verify load distribution

**Expected Results**:
- **Assignment**: Each camera assigned to different worker
- **Status**: All 4 workers become "busy"
- **Load**: Even distribution across workers
- **Performance**: No worker overload

---

#### **Test Case ID**: `WORKER-LOAD-002`
#### **Test Case Name**: Worker Pool Exhaustion
#### **Priority**: Medium
#### **Test Type**: Negative

**Preconditions**: All 4 workers are busy

**Test Steps**:
1. Try to start 5th camera processing
2. Monitor queue behavior
3. Verify error handling

**Expected Results**:
- **Status Code**: 503 Service Unavailable
- **Response**: "No available workers"
- **Queue**: Task remains pending
- **Logs**: Warning logged about worker exhaustion

---

### 🧪 **TEST CASE 3.4: Frame Processing**

#### **Test Case ID**: `WORKER-FRAME-001`
#### **Test Case Name**: Frame Processing Success
#### **Priority**: High
#### **Test Type**: Positive

**Preconditions**: Camera stream is accessible

**Test Steps**:
1. Start camera processing
2. Monitor frame processing
3. Verify AI analysis

**Expected Results**:
- **Frame Count**: Frames processed continuously
- **Processing**: AI analysis working correctly
- **Performance**: Processing time < 100ms per frame
- **Memory**: Stable memory usage
- **Logs**: Frame processing logged every 100 frames

---

#### **Test Case ID**: `WORKER-FRAME-002`
#### **Test Case Name**: Stream Connection Error
#### **Priority**: Medium
#### **Test Type**: Error Handling

**Preconditions**: Invalid stream URL

**Test Data**:
```json
{
  "camera_id": 1,
  "stream_url": "rtsp://invalid.url:554/stream"
}
```

**Expected Results**:
- **Error Handling**: Graceful error handling
- **Worker Status**: Worker returns to "idle"
- **Error Count**: Error count incremented
- **Logs**: Connection error logged
- **Recovery**: Worker available for new tasks

---

#### **Test Case ID**: `WORKER-FRAME-003`
#### **Test Case Name**: Frame Processing Performance
#### **Priority**: Medium
#### **Test Type**: Performance

**Test Steps**:
1. Process 1000 frames
2. Measure processing metrics
3. Verify performance standards

**Expected Results**:
- **FPS**: > 10 frames per second
- **Memory**: < 500MB per worker
- **CPU**: < 80% per worker
- **Latency**: < 100ms per frame
- **Stability**: No memory leaks

---

### 🧪 **TEST CASE 3.5: Error Handling & Recovery**

#### **Test Case ID**: `WORKER-ERR-001`
#### **Test Case Name**: Worker Crash Recovery
#### **Priority**: High
#### **Test Type**: Error Handling

**Test Steps**:
1. Simulate worker crash
2. Monitor recovery process
3. Verify system stability

**Expected Results**:
- **Recovery**: Worker restarts automatically
- **Tasks**: Tasks reassigned to other workers
- **Stability**: System remains operational
- **Logs**: Crash and recovery logged
- **Performance**: Minimal impact on other workers

---

#### **Test Case ID**: `WORKER-ERR-002`
#### **Test Case Name**: Memory Leak Prevention
#### **Priority**: Medium
#### **Test Type**: Performance

**Test Steps**:
1. Run continuous processing for 1 hour
2. Monitor memory usage
3. Verify no memory leaks

**Expected Results**:
- **Memory**: Stable memory usage over time
- **Garbage Collection**: Proper cleanup
- **Performance**: No degradation over time
- **Stability**: System remains responsive

---

### 🧪 **TEST CASE 3.6: Monitoring & Metrics**

#### **Test Case ID**: `WORKER-MON-001`
#### **Test Case Name**: Worker Status Monitoring
#### **Priority**: Medium
#### **Test Type**: Monitoring

**Test Steps**:
1. Get worker pool status
2. Verify monitoring data
3. Check metrics accuracy

**Expected Results**:
- **Status**: Accurate worker status reporting
- **Metrics**: Correct frame counts and error counts
- **Timing**: Accurate start times and durations
- **Real-time**: Status updates in real-time

---

#### **Test Case ID**: `WORKER-MON-002`
#### **Test Case Name**: Performance Metrics Collection
#### **Priority**: Medium
#### **Test Type**: Monitoring

**Test Steps**:
1. Monitor performance metrics
2. Verify data collection
3. Check metric accuracy

**Expected Results**:
- **CPU Usage**: Accurate CPU utilization
- **Memory Usage**: Correct memory consumption
- **Processing Rate**: Accurate FPS measurement
- **Error Rate**: Correct error tracking

---

### 🧪 **TEST CASE 3.7: Integration Testing**

#### **Test Case ID**: `WORKER-INT-001`
#### **Test Case Name**: Database Integration
#### **Priority**: High
#### **Test Type**: Integration

**Test Steps**:
1. Start camera processing
2. Verify count data storage
3. Check database consistency

**Expected Results**:
- **Storage**: Count data stored in database
- **Consistency**: Data integrity maintained
- **Performance**: Database operations efficient
- **Real-time**: Data updated in real-time

---

#### **Test Case ID**: `WORKER-INT-002`
#### **Test Case Name**: Redis Cache Integration
#### **Priority**: Medium
#### **Test Type**: Integration

**Test Steps**:
1. Verify Redis connection
2. Test cache operations
3. Check cache consistency

**Expected Results**:
- **Connection**: Stable Redis connection
- **Cache**: Efficient caching operations
- **Performance**: Fast cache access
- **Reliability**: Cache data consistency

---

### 📊 **TEST EXECUTION MATRIX**

| Test Case | Priority | Status | Executed By | Date | Notes |
|-----------|----------|--------|-------------|------|-------|
| WORKER-INIT-001 | High | 🔄 | | | |
| WORKER-INIT-002 | High | 🔄 | | | |
| WORKER-TASK-001 | High | 🔄 | | | |
| WORKER-TASK-002 | High | 🔄 | | | |
| WORKER-TASK-003 | Medium | 🔄 | | | |
| WORKER-LOAD-001 | High | 🔄 | | | |
| WORKER-LOAD-002 | Medium | 🔄 | | | |
| WORKER-FRAME-001 | High | 🔄 | | | |
| WORKER-FRAME-002 | Medium | 🔄 | | | |
| WORKER-FRAME-003 | Medium | 🔄 | | | |
| WORKER-ERR-001 | High | 🔄 | | | |
| WORKER-ERR-002 | Medium | 🔄 | | | |
| WORKER-MON-001 | Medium | 🔄 | | | |
| WORKER-MON-002 | Medium | 🔄 | | | |
| WORKER-INT-001 | High | 🔄 | | | |
| WORKER-INT-002 | Medium | 🔄 | | | |

### 🎯 **ACCEPTANCE CRITERIA**

- ✅ Worker pool initializes correctly with 4 workers
- ✅ Tasks are assigned efficiently to available workers
- ✅ Load balancing works across all workers
- ✅ Frame processing maintains >10 FPS performance
- ✅ Error handling prevents system crashes
- ✅ Memory usage remains stable over time
- ✅ Database integration stores count data correctly
- ✅ Monitoring provides accurate real-time metrics
- ✅ Graceful shutdown releases all resources

### 📝 **NOTES**

- Worker pool tests require camera streams or mock data
- Performance tests should run for extended periods
- Memory monitoring is critical for long-running processes
- Error simulation should be done carefully to avoid system damage
- Integration tests require all services to be running
- Monitor system resources during all tests 