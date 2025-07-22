# Workflow 3: Camera Management API - Enhanced Task List
## AI Camera Counting System - Senior Developer Edition

### 📊 Tổng quan
Workflow 3 tập trung vào việc phát triển Camera Management API cho hệ thống AI Camera Counting, bao gồm CRUD operations, real-time streaming, health monitoring, và integration với AI processing. Tài liệu này được thiết kế cho senior developers với đầy đủ technical specifications và implementation patterns.

### 🎯 Mục tiêu kỹ thuật
- **API Performance**: Response time <200ms, throughput >1000 req/s
- **Database Optimization**: Query time <50ms, proper indexing và connection pooling
- **Security**: JWT authentication, RBAC, input validation, SQL injection prevention
- **Scalability**: Support 100+ concurrent camera streams với worker pool architecture
- **Monitoring**: Real-time health monitoring, metrics collection, và alerting
- **Error Handling**: Comprehensive error handling, circuit breaker pattern, retry logic
- **Real-time Processing**: WebSocket integration, event-driven architecture

### 🏗️ Enhanced Camera Management Architecture

#### System Architecture Overview
```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              ENHANCED CAMERA MANAGEMENT ARCHITECTURE            │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              PRESENTATION LAYER                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   React     │  │   Mobile    │  │   Admin     │  │   API       │        │ │
│  │  │   Dashboard │  │   Client    │  │   Panel     │  │   Gateway   │        │ │
│  │  │   (Port 3000)│  │   (React)   │  │   (React)   │  │   (NGINX)   │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                             │
│                                    ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              API GATEWAY LAYER                              │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Load      │  │   Rate      │  │   Auth      │  │   Request   │        │ │
│  │  │   Balancer  │  │   Limiting  │  │   Gateway   │  │   Routing   │        │ │
│  │  │   (HAProxy) │  │   (Redis)   │  │   (JWT)     │  │   (Proxy)   │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                             │
│                                    ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              APPLICATION LAYER                              │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   beAuth    │  │   beCamera  │  │   WebSocket │  │   Analytics │        │ │
│  │  │   Service   │  │   Service   │  │   Service   │  │   Service   │        │ │
│  │  │   (Node.js) │  │   (Python)  │  │   (Node.js) │  │   (Python)  │        │ │
│  │  │   Port 3001 │  │   Port 3002 │  │   Port 3003 │  │   Port 3004 │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                             │
│                                    ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              SERVICE LAYER                                  │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Camera    │  │   Stream    │  │   Worker    │  │   Cache     │        │ │
│  │  │   Service   │  │   Service   │  │   Pool      │  │   Service   │        │ │
│  │  │   (FastAPI) │  │   (OpenCV)  │  │   (Celery)  │  │   (Redis)   │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                             │
│                                    ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              DATA LAYER                                     │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Camera    │  │   Count     │  │   Health    │  │   Settings  │        │ │
│  │  │   Database  │  │   Database  │  │   Database  │  │   Cache     │        │ │
│  │  │   (PostgreSQL)│ │   (PostgreSQL)│ │   (PostgreSQL)│ │   (Redis)   │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              INFRASTRUCTURE LAYER                           │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Monitoring│  │   Logging   │  │   Security  │  │   Backup    │        │ │
│  │  │   (Prometheus)│ │   (ELK)     │  │   (WAF)     │  │   (Automated)│       │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

#### Worker Pool Architecture Integration
```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              WORKER POOL INTEGRATION                            │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              CAMERA STREAM PROCESSING                       │ │
│  │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │ │
│  │  │   Camera    │    │   Task      │    │   Worker    │    │   AI        │  │ │
│  │  │   Stream    │    │   Queue     │    │   Pool      │    │   Model     │  │ │
│  │  │   (RTSP)    │    │   (RabbitMQ)│    │   (Celery)  │    │   (YOLO)    │  │ │
│  │  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘  │ │
│  │         │                   │                   │                   │      │ │
│  │         │ 1. Stream Input   │                   │                   │      │ │
│  │         │──────────────────►│                   │                   │      │ │
│  │         │                   │                   │                   │      │ │
│  │         │                   │ 2. Task Creation  │                   │      │ │
│  │         │                   │──────────────────►│                   │      │ │
│  │         │                   │                   │                   │      │ │
│  │         │                   │                   │ 3. Frame Processing│     │ │
│  │         │                   │                   │──────────────────►│      │ │
│  │         │                   │                   │                   │      │ │
│  │         │                   │                   │ 4. Detection Result│     │ │
│  │         │                   │                   │◄──────────────────│      │ │
│  │         │                   │                   │                   │      │ │
│  │         │                   │ 5. Result Storage │                   │      │ │
│  │         │                   │◄──────────────────│                   │      │ │
│  │         │                   │                   │                   │      │ │
│  │         │ 6. Real-time      │                   │                   │      │ │
│  │         │ Updates           │                   │                   │      │ │
│  │         │◄──────────────────│                   │                   │      │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 📋 Enhanced Task List

#### Phase 1: Database Schema & Models (Priority: Critical) ✅ **COMPLETED**
- [x] **Task 1.1**: Design comprehensive camera database schema ✅
  - [x] Create `cameras` table với đầy đủ fields ✅
  - [x] Create `count_data` table cho analytics ✅
  - [x] Database migration đã chạy thành công ✅
  - [x] Dữ liệu mẫu đã được tạo ✅
  - [ ] Create `cameras` table với đầy đủ fields:
    ```sql
    CREATE TABLE cameras (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        location VARCHAR(500),
        description TEXT,
        stream_url TEXT NOT NULL,
        stream_type VARCHAR(20) DEFAULT 'rtsp',
        status VARCHAR(20) DEFAULT 'offline',
        worker_id VARCHAR(50),
        settings JSONB DEFAULT '{}',
        metadata JSONB DEFAULT '{}',
        security_config JSONB DEFAULT '{}',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        created_by INTEGER REFERENCES users(id),
        updated_by INTEGER REFERENCES users(id),
        CONSTRAINT valid_status CHECK (status IN ('online', 'offline', 'maintenance', 'error')),
        CONSTRAINT valid_stream_type CHECK (stream_type IN ('rtsp', 'http', 'file', 'rtmp'))
    );
    ```
  - [ ] Create `camera_health` table cho monitoring:
    ```sql
    CREATE TABLE camera_health (
        id SERIAL PRIMARY KEY,
        camera_id INTEGER REFERENCES cameras(id) ON DELETE CASCADE,
        status VARCHAR(20) DEFAULT 'online',
        last_heartbeat TIMESTAMP,
        uptime_percentage DECIMAL(5,2),
        response_time_ms INTEGER,
        stream_quality_score DECIMAL(3,2),
        error_count INTEGER DEFAULT 0,
        last_error_message TEXT,
        last_error_timestamp TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        INDEX idx_camera_health_camera_id (camera_id),
        INDEX idx_camera_health_status (status),
        INDEX idx_camera_health_last_heartbeat (last_heartbeat)
    );
    ```
  - [ ] Create `camera_events` table cho logging:
    ```sql
    CREATE TABLE camera_events (
        id SERIAL PRIMARY KEY,
        camera_id INTEGER REFERENCES cameras(id) ON DELETE CASCADE,
        event_type VARCHAR(50) NOT NULL,
        event_data JSONB,
        severity VARCHAR(20) DEFAULT 'info',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        INDEX idx_camera_events_camera_id (camera_id),
        INDEX idx_camera_events_event_type (event_type),
        INDEX idx_camera_events_created_at (created_at),
        INDEX idx_camera_events_severity (severity)
    );
    ```
  - [ ] Create `camera_counts` table cho analytics:
    ```sql
    CREATE TABLE camera_counts (
        id SERIAL PRIMARY KEY,
        camera_id INTEGER REFERENCES cameras(id) ON DELETE CASCADE,
        count_in INTEGER DEFAULT 0,
        count_out INTEGER DEFAULT 0,
        total_count INTEGER DEFAULT 0,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        confidence_score DECIMAL(3,2),
        frame_data JSONB,
        INDEX idx_camera_counts_camera_id (camera_id),
        INDEX idx_camera_counts_timestamp (timestamp),
        INDEX idx_camera_counts_camera_timestamp (camera_id, timestamp)
    );
    ```
  - [ ] Add proper indexes và constraints
  - [ ] Create migration scripts với versioning

- [ ] **Task 1.2**: Design Pydantic models với validation
  - [ ] Create `CameraCreate` model:
    ```python
    from pydantic import BaseModel, HttpUrl, validator
    from typing import Optional, Dict, Any
    from enum import Enum
    
    class StreamType(str, Enum):
        RTSP = "rtsp"
        HTTP = "http"
        FILE = "file"
        RTMP = "rtmp"
    
    class CameraStatus(str, Enum):
        ONLINE = "online"
        OFFLINE = "offline"
        MAINTENANCE = "maintenance"
        ERROR = "error"
    
    class CameraCreate(BaseModel):
        name: str
        location: Optional[str] = None
        description: Optional[str] = None
        stream_url: str
        stream_type: StreamType = StreamType.RTSP
        settings: Optional[Dict[str, Any]] = {}
        metadata: Optional[Dict[str, Any]] = {}
        security_config: Optional[Dict[str, Any]] = {}
        
        @validator('name')
        def validate_name(cls, v):
            if len(v.strip()) < 2:
                raise ValueError('Camera name must be at least 2 characters')
            return v.strip()
        
        @validator('stream_url')
        def validate_stream_url(cls, v):
            if not v.startswith(('rtsp://', 'http://', 'https://', 'file://')):
                raise ValueError('Invalid stream URL format')
            return v
    ```
  - [ ] Create `CameraUpdate` model với partial updates
  - [ ] Create `CameraResponse` model với computed fields
  - [ ] Create `CameraHealth` model cho monitoring
  - [ ] Create validation schemas với custom validators

- [ ] **Task 1.3**: Database connection setup với connection pooling
  - [ ] Configure PostgreSQL connection pool với asyncpg:
    ```python
    import asyncpg
    from typing import Optional
    
    class DatabaseManager:
        def __init__(self):
            self.pool: Optional[asyncpg.Pool] = None
        
        async def create_pool(self, dsn: str, min_size: int = 10, max_size: int = 20):
            self.pool = await asyncpg.create_pool(
                dsn=dsn,
                min_size=min_size,
                max_size=max_size,
                command_timeout=60,
                statement_cache_size=0,
                max_cached_statement_lifetime=0,
                max_cached_statement_size=0
            )
        
        async def get_connection(self):
            if not self.pool:
                raise RuntimeError("Database pool not initialized")
            return await self.pool.acquire()
        
        async def release_connection(self, conn):
            if self.pool:
                await self.pool.release(conn)
    ```
  - [ ] Setup connection management với context managers
  - [ ] Add connection health checks
  - [ ] Implement connection retry logic với exponential backoff

#### Phase 2: Core API Endpoints (Priority: Critical) ✅ **COMPLETED**
- [x] **Task 2.1**: Camera CRUD Operations với comprehensive validation ✅
  - [x] `GET /api/v1/cameras` - List all cameras ✅
  - [x] `POST /api/v1/cameras` - Create new camera ✅
  - [x] `GET /api/v1/cameras/{id}` - Get camera by ID với error handling ✅
  - [x] `PUT /api/v1/cameras/{id}` - Update camera với optimistic locking ✅
  - [x] `DELETE /api/v1/cameras/{id}` - Delete camera với cascade handling ✅
  - [x] `PATCH /api/v1/cameras/{id}/status` - Update camera status với state validation ✅
  - [x] `GET /api/v1/counts` - Get count data ✅
  - [x] `GET /api/v1/analytics/summary` - Analytics summary ✅
    ```python
    @router.get("/cameras", response_model=PaginatedCameraResponse)
    async def list_cameras(
        skip: int = Query(0, ge=0, description="Number of records to skip"),
        limit: int = Query(10, ge=1, le=100, description="Number of records to return"),
        status: Optional[CameraStatus] = Query(None, description="Filter by status"),
        location: Optional[str] = Query(None, description="Filter by location"),
        search: Optional[str] = Query(None, description="Search in name and description"),
        current_user: User = Depends(get_current_user)
    ):
        # Implementation with proper filtering and pagination
    ```
  - [ ] `POST /api/v1/cameras` - Create new camera với validation
  - [ ] `GET /api/v1/cameras/{id}` - Get camera by ID với error handling
  - [ ] `PUT /api/v1/cameras/{id}` - Update camera với optimistic locking
  - [ ] `DELETE /api/v1/cameras/{id}` - Delete camera với cascade handling
  - [ ] `PATCH /api/v1/cameras/{id}/status` - Update camera status với state validation

- [ ] **Task 2.2**: Camera Control Operations với worker pool integration
  - [ ] `POST /api/v1/cameras/{id}/start` - Start camera processing:
    ```python
    @router.post("/cameras/{camera_id}/start")
    async def start_camera(
        camera_id: int,
        current_user: User = Depends(get_current_user),
        db: DatabaseManager = Depends(get_database)
    ):
        # Validate camera exists and user has permission
        # Check if camera is already running
        # Assign to worker pool
        # Update status
        # Return worker assignment details
    ```
  - [ ] `POST /api/v1/cameras/{id}/stop` - Stop camera processing
  - [ ] `POST /api/v1/cameras/{id}/restart` - Restart camera với health check
  - [ ] `GET /api/v1/cameras/{id}/status` - Get detailed status với metrics

- [ ] **Task 2.3**: Camera Configuration với validation
  - [ ] `GET /api/v1/cameras/{id}/config` - Get camera configuration
  - [ ] `PUT /api/v1/cameras/{id}/config` - Update camera configuration
  - [ ] `POST /api/v1/cameras/{id}/test-connection` - Test camera connection

#### Phase 3: Authentication & Security (Priority: Critical) 🔄 **IN PROGRESS**
- [x] **Task 3.1**: JWT Authentication Integration với beAuth 🔄
  - [x] Integrate với beAuth service ✅
  - [x] Implement JWT token validation ✅
  - [x] Add authentication middleware to all endpoints ✅
  - [x] Test endpoint without authentication for development ✅
  - [ ] Add role-based access control (RBAC)
  - [ ] Implement user permissions cho camera operations
  - [ ] Integrate với beAuth service:
    ```python
    from fastapi import Depends, HTTPException, status
    from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
    import httpx
    
    security = HTTPBearer()
    
    async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
        token = credentials.credentials
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{AUTH_SERVICE_URL}/verify",
                headers={"Authorization": f"Bearer {token}"}
            )
            if response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token"
                )
            return response.json()
    ```
  - [ ] Implement JWT token validation với caching
  - [ ] Add role-based access control (RBAC):
    ```python
    from enum import Enum
    from typing import List
    
    class Permission(str, Enum):
        CAMERA_READ = "camera:read"
        CAMERA_WRITE = "camera:write"
        CAMERA_DELETE = "camera:delete"
        CAMERA_CONTROL = "camera:control"
        CAMERA_ADMIN = "camera:admin"
    
    def require_permissions(required_permissions: List[Permission]):
        def decorator(func):
            async def wrapper(*args, **kwargs):
                user = kwargs.get('current_user')
                if not user:
                    raise HTTPException(status_code=401, detail="Authentication required")
                
                user_permissions = await get_user_permissions(user.id)
                for permission in required_permissions:
                    if permission not in user_permissions:
                        raise HTTPException(
                            status_code=403, 
                            detail=f"Permission {permission} required"
                        )
                return await func(*args, **kwargs)
            return wrapper
        return decorator
    ```
  - [ ] Implement user permissions cho camera operations

- [ ] **Task 3.2**: Input Validation & Security
  - [ ] Implement comprehensive input validation với Pydantic
  - [ ] Add SQL injection prevention với parameterized queries
  - [ ] Implement rate limiting với Redis:
    ```python
    import redis.asyncio as redis
    from fastapi import HTTPException
    
    async def rate_limit(key: str, limit: int, window: int = 60):
        r = redis.Redis(host='localhost', port=6379, db=0)
        current = await r.incr(key)
        if current == 1:
            await r.expire(key, window)
        
        if current > limit:
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded"
            )
    ```
  - [ ] Add request logging và audit trail

- [ ] **Task 3.3**: Error Handling với circuit breaker pattern
  - [ ] Implement global error handler:
    ```python
    from fastapi import Request
    from fastapi.responses import JSONResponse
    import logging
    
    logger = logging.getLogger(__name__)
    
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled exception: {exc}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal server error",
                "message": "An unexpected error occurred",
                "request_id": request.headers.get("X-Request-ID", "unknown")
            }
        )
    ```
  - [ ] Create custom exception classes
  - [ ] Add proper HTTP status codes
  - [ ] Implement error logging với structured logging

#### Phase 4: Worker Pool Integration (Priority: High) ✅ **COMPLETED**
- [x] **Task 4.1**: Worker Pool Architecture Implementation ✅
  - [x] Setup worker pool với async processing ✅
  - [x] Implement task queue management ✅
  - [x] Add worker health monitoring ✅
  - [x] Implement load balancing strategies ✅
  - [x] Create worker pool endpoints ✅
  - [ ] Setup Celery worker pool:
    ```python
    from celery import Celery
    from celery.utils.log import get_task_logger
    
    app = Celery('camera_processing')
    app.config_from_object('celeryconfig')
    
    logger = get_task_logger(__name__)
    
    @app.task(bind=True, max_retries=3)
    def process_camera_stream(self, camera_id: int, stream_url: str):
        try:
            # Process camera stream
            result = process_stream(camera_id, stream_url)
            return result
        except Exception as exc:
            logger.error(f"Error processing camera {camera_id}: {exc}")
            raise self.retry(exc=exc, countdown=60)
    ```
  - [ ] Implement task queue management với RabbitMQ
  - [ ] Add worker health monitoring
  - [ ] Implement load balancing strategies

- [ ] **Task 4.2**: Camera Stream Processing
  - [ ] Implement OpenCV stream processing:
    ```python
    import cv2
    import numpy as np
    from typing import Generator, Tuple
    
    class CameraStreamProcessor:
        def __init__(self, stream_url: str):
            self.stream_url = stream_url
            self.cap = None
        
        async def connect(self) -> bool:
            try:
                self.cap = cv2.VideoCapture(self.stream_url)
                return self.cap.isOpened()
            except Exception as e:
                logger.error(f"Failed to connect to stream: {e}")
                return False
        
        async def process_frames(self) -> Generator[Tuple[np.ndarray, dict], None, None]:
            if not self.cap:
                raise RuntimeError("Camera not connected")
            
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    break
                
                # Process frame with AI model
                processed_frame, metadata = await self.process_frame(frame)
                yield processed_frame, metadata
        
        async def process_frame(self, frame: np.ndarray) -> Tuple[np.ndarray, dict]:
            # AI processing logic here
            # Return processed frame and metadata
            pass
    ```
  - [ ] Add AI model integration với YOLO
  - [ ] Implement frame buffering và queue management
  - [ ] Add stream quality monitoring

- [ ] **Task 4.3**: Real-time Data Processing
  - [ ] Implement WebSocket broadcasting:
    ```python
    import asyncio
    import json
    from fastapi import WebSocket
    from typing import List
    
    class WebSocketManager:
        def __init__(self):
            self.active_connections: List[WebSocket] = []
        
        async def connect(self, websocket: WebSocket):
            await websocket.accept()
            self.active_connections.append(websocket)
        
        def disconnect(self, websocket: WebSocket):
            self.active_connections.remove(websocket)
        
        async def broadcast(self, message: dict):
            for connection in self.active_connections:
                try:
                    await connection.send_text(json.dumps(message))
                except Exception as e:
                    logger.error(f"Error broadcasting message: {e}")
                    self.active_connections.remove(connection)
    ```
  - [ ] Add real-time count aggregation
  - [ ] Implement event streaming
  - [ ] Add data persistence với batch processing

#### Phase 5: Camera Health Monitoring (Priority: High)
- [ ] **Task 5.1**: Health Check Endpoints với comprehensive monitoring
  - [ ] `GET /api/v1/cameras/{id}/health` - Get camera health status:
    ```python
    @router.get("/cameras/{camera_id}/health", response_model=CameraHealthResponse)
    async def get_camera_health(
        camera_id: int,
        current_user: User = Depends(get_current_user),
        db: DatabaseManager = Depends(get_database)
    ):
        # Get camera health data
        # Calculate uptime percentage
        # Check last heartbeat
        # Return comprehensive health status
    ```
  - [ ] `GET /api/v1/cameras/health/summary` - Get health summary
  - [ ] `POST /api/v1/cameras/{id}/health-check` - Trigger health check

- [ ] **Task 5.2**: Health Monitoring Service với background tasks
  - [ ] Implement background health monitoring:
    ```python
    from fastapi import BackgroundTasks
    import asyncio
    
    async def monitor_camera_health(camera_id: int):
        while True:
            try:
                health_status = await check_camera_health(camera_id)
                await update_camera_health(camera_id, health_status)
                
                if health_status.status == "error":
                    await send_alert(camera_id, health_status)
                
                await asyncio.sleep(30)  # Check every 30 seconds
            except Exception as e:
                logger.error(f"Health monitoring error for camera {camera_id}: {e}")
                await asyncio.sleep(60)  # Wait longer on error
    
    @router.post("/cameras/{camera_id}/start-monitoring")
    async def start_health_monitoring(
        camera_id: int,
        background_tasks: BackgroundTasks,
        current_user: User = Depends(get_current_user)
    ):
        background_tasks.add_task(monitor_camera_health, camera_id)
        return {"message": "Health monitoring started"}
    ```
  - [ ] Add health metrics collection với Prometheus
  - [ ] Implement health alerts với multiple channels
  - [ ] Add health dashboard endpoints

- [ ] **Task 5.3**: Performance Metrics với monitoring
  - [ ] Track response times với histogram metrics
  - [ ] Monitor stream quality với quality scores
  - [ ] Track error rates với alerting
  - [ ] Implement performance alerts với thresholds

#### Phase 6: Real-time Features (Priority: Medium)
- [ ] **Task 6.1**: WebSocket Integration với connection management
  - [ ] Setup WebSocket server với connection pooling
  - [ ] Implement real-time camera status updates
  - [ ] Add real-time count updates với batching
  - [ ] Implement connection management với authentication

- [ ] **Task 6.2**: Stream Management với quality monitoring
  - [ ] Implement stream URL validation với format checking
  - [ ] Add stream quality monitoring với metrics
  - [ ] Implement stream recovery logic với automatic retry
  - [ ] Add stream configuration management

- [ ] **Task 6.3**: Real-time Analytics với aggregation
  - [ ] Implement real-time count aggregation với time windows
  - [ ] Add real-time occupancy tracking
  - [ ] Implement real-time alerts với threshold management
  - [ ] Add real-time dashboard data với caching

#### Phase 7: Integration & Testing (Priority: Medium)
- [ ] **Task 7.1**: Integration với beAuth
  - [ ] Test authentication flow với token validation
  - [ ] Verify user permissions với role testing
  - [ ] Test cross-service communication với circuit breaker
  - [ ] Add integration tests với test containers

- [ ] **Task 7.2**: Integration với Frontend
  - [ ] Test API endpoints với frontend components
  - [ ] Verify data format compatibility với schema validation
  - [ ] Test real-time updates với WebSocket testing
  - [ ] Add end-to-end tests với Playwright

- [ ] **Task 7.3**: Performance Testing với load testing
  - [ ] Load testing với multiple cameras:
    ```python
    import asyncio
    import aiohttp
    import time
    from typing import List
    
    async def load_test_cameras(num_cameras: int, duration: int):
        async with aiohttp.ClientSession() as session:
            tasks = []
            for i in range(num_cameras):
                task = asyncio.create_task(
                    simulate_camera_stream(session, f"camera_{i}")
                )
                tasks.append(task)
            
            start_time = time.time()
            while time.time() - start_time < duration:
                await asyncio.sleep(1)
            
            for task in tasks:
                task.cancel()
            
            await asyncio.gather(*tasks, return_exceptions=True)
    ```
  - [ ] Stress testing với high concurrency
  - [ ] Performance benchmarking với metrics collection
  - [ ] Optimization based on results

#### Phase 8: Documentation & Deployment (Priority: Low)
- [ ] **Task 8.1**: API Documentation với OpenAPI
  - [ ] Generate OpenAPI/Swagger documentation với examples
  - [ ] Add comprehensive endpoint documentation với response schemas
  - [ ] Create integration guides với code examples
  - [ ] Add code examples với multiple languages

- [ ] **Task 8.2**: Deployment Preparation với Docker
  - [ ] Create Docker configuration với multi-stage builds
  - [ ] Setup environment variables với validation
  - [ ] Create deployment scripts với health checks
  - [ ] Add health check endpoints với readiness/liveness probes

- [ ] **Task 8.3**: Monitoring Setup với observability
  - [ ] Setup application monitoring với Prometheus
  - [ ] Add performance metrics với custom dashboards
  - [ ] Implement alerting với multiple channels
  - [ ] Create monitoring dashboards với Grafana

### 🔧 Enhanced Technical Requirements

#### Database Schema Requirements với Advanced Features
```sql
-- Enhanced camera table với additional fields
CREATE TABLE cameras (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    location VARCHAR(500),
    description TEXT,
    stream_url TEXT NOT NULL,
    stream_type VARCHAR(20) DEFAULT 'rtsp',
    status VARCHAR(20) DEFAULT 'offline',
    worker_id VARCHAR(50),
    settings JSONB DEFAULT '{}',
    metadata JSONB DEFAULT '{}',
    security_config JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER REFERENCES users(id),
    updated_by INTEGER REFERENCES users(id),
    version INTEGER DEFAULT 1,
    CONSTRAINT valid_status CHECK (status IN ('online', 'offline', 'maintenance', 'error')),
    CONSTRAINT valid_stream_type CHECK (stream_type IN ('rtsp', 'http', 'file', 'rtmp'))
);

-- Create indexes for performance
CREATE INDEX idx_cameras_status ON cameras(status);
CREATE INDEX idx_cameras_worker_id ON cameras(worker_id);
CREATE INDEX idx_cameras_created_at ON cameras(created_at);
CREATE INDEX idx_cameras_location ON cameras(location);
CREATE INDEX idx_cameras_stream_type ON cameras(stream_type);

-- Create GIN indexes for JSONB fields
CREATE INDEX idx_cameras_settings_gin ON cameras USING GIN (settings);
CREATE INDEX idx_cameras_metadata_gin ON cameras USING GIN (metadata);

-- Enhanced camera health monitoring
CREATE TABLE camera_health (
    id SERIAL PRIMARY KEY,
    camera_id INTEGER REFERENCES cameras(id) ON DELETE CASCADE,
    status VARCHAR(20) DEFAULT 'online',
    last_heartbeat TIMESTAMP,
    uptime_percentage DECIMAL(5,2),
    response_time_ms INTEGER,
    stream_quality_score DECIMAL(3,2),
    error_count INTEGER DEFAULT 0,
    last_error_message TEXT,
    last_error_timestamp TIMESTAMP,
    cpu_usage DECIMAL(5,2),
    memory_usage DECIMAL(5,2),
    network_bandwidth DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Enhanced camera events with structured logging
CREATE TABLE camera_events (
    id SERIAL PRIMARY KEY,
    camera_id INTEGER REFERENCES cameras(id) ON DELETE CASCADE,
    event_type VARCHAR(50) NOT NULL,
    event_data JSONB,
    severity VARCHAR(20) DEFAULT 'info',
    source VARCHAR(50) DEFAULT 'system',
    user_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Camera counts with time-series optimization
CREATE TABLE camera_counts (
    id SERIAL PRIMARY KEY,
    camera_id INTEGER REFERENCES cameras(id) ON DELETE CASCADE,
    count_in INTEGER DEFAULT 0,
    count_out INTEGER DEFAULT 0,
    total_count INTEGER DEFAULT 0,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    confidence_score DECIMAL(3,2),
    frame_data JSONB,
    processing_time_ms INTEGER,
    ai_model_version VARCHAR(20)
);

-- Partitioned table for time-series data
CREATE TABLE camera_counts_hourly (
    id SERIAL,
    camera_id INTEGER,
    count_in INTEGER DEFAULT 0,
    count_out INTEGER DEFAULT 0,
    total_count INTEGER DEFAULT 0,
    hour_start TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id, hour_start)
) PARTITION BY RANGE (hour_start);

-- Create partitions for the last 30 days
CREATE TABLE camera_counts_hourly_2024_01 PARTITION OF camera_counts_hourly
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');
```

#### API Endpoint Specifications với Advanced Features
```python
# Base URL: http://localhost:3002/api/v1

# Camera Management với advanced features
GET    /cameras                    # List cameras with pagination, filtering, sorting
POST   /cameras                    # Create new camera with validation
GET    /cameras/{id}              # Get camera details with related data
PUT    /cameras/{id}              # Update camera with optimistic locking
DELETE /api/v1/cameras/{id}              # Delete camera with cascade handling
PATCH  /cameras/{id}/status       # Update status with state validation

# Camera Control với worker pool integration
POST   /cameras/{id}/start        # Start processing with worker assignment
POST   /cameras/{id}/stop         # Stop processing with graceful shutdown
POST   /cameras/{id}/restart      # Restart camera with health check
GET    /cameras/{id}/status       # Get detailed status with metrics

# Camera Health với comprehensive monitoring
GET    /cameras/{id}/health       # Get health status with metrics
GET    /cameras/health/summary    # Health summary with aggregation
POST   /cameras/{id}/health-check # Trigger health check
GET    /cameras/{id}/metrics      # Get performance metrics

# Camera Configuration với validation
GET    /cameras/{id}/config       # Get configuration with defaults
PUT    /cameras/{id}/config       # Update configuration with validation
POST   /cameras/{id}/test-connection # Test connection with timeout
GET    /cameras/{id}/stream-info  # Get stream information

# Real-time Data với WebSocket support
GET    /cameras/{id}/stream       # Get live stream data
WS     /ws/cameras/{id}          # WebSocket for real-time updates
GET    /cameras/{id}/counts       # Get count history
POST   /cameras/{id}/counts       # Add count data

# Analytics với time-series data
GET    /cameras/{id}/analytics    # Get analytics data
GET    /cameras/{id}/reports      # Get generated reports
POST   /cameras/{id}/export       # Export data in various formats

# Worker Pool Management
GET    /workers                   # List available workers
GET    /workers/{id}             # Get worker details
POST   /workers/{id}/assign      # Assign camera to worker
POST    /workers/{id}/release     # Release worker assignment
```

#### Performance Requirements với Advanced Metrics
- **Response Time**: <200ms cho 95% requests, <500ms cho 99% requests
- **Database Queries**: <50ms average, <100ms cho 95% queries
- **Concurrent Users**: Support 100+ simultaneous users với connection pooling
- **Camera Streams**: Support 50+ concurrent camera streams với worker pool
- **Memory Usage**: <2GB per instance với memory monitoring
- **CPU Usage**: <80% under normal load với auto-scaling
- **WebSocket Connections**: Support 1000+ concurrent connections
- **Throughput**: >1000 req/s với load balancing
- **Uptime**: 99.9% availability với health monitoring

#### Security Requirements với Advanced Protection
- **Authentication**: JWT token validation với refresh tokens
- **Authorization**: Role-based access control (RBAC) với fine-grained permissions
- **Input Validation**: Comprehensive validation với Pydantic schemas
- **SQL Injection**: Prevention through parameterized queries và ORM
- **Rate Limiting**: 100 requests/minute per user với Redis
- **Audit Logging**: Log tất cả critical operations với structured logging
- **Data Encryption**: Encrypt sensitive data at rest và in transit
- **API Security**: CORS configuration, security headers, input sanitization
- **Monitoring**: Security event monitoring với alerting

### 📊 Enhanced Success Metrics

#### Functional Metrics với Comprehensive Testing
- [ ] All CRUD operations working correctly với validation
- [ ] Real-time status updates functional với WebSocket
- [ ] Health monitoring operational với alerting
- [ ] Authentication integration complete với RBAC
- [ ] Error handling comprehensive với circuit breaker
- [ ] Worker pool integration functional với load balancing
- [ ] Analytics processing operational với time-series data

#### Performance Metrics với Monitoring
- [ ] API response time <200ms cho 95% requests
- [ ] Database query time <50ms cho 95% queries
- [ ] Support 100+ concurrent users với connection pooling
- [ ] Support 50+ camera streams với worker pool
- [ ] 99.9% uptime achieved với health monitoring
- [ ] WebSocket latency <100ms cho real-time updates
- [ ] Memory usage <2GB với garbage collection optimization

#### Quality Metrics với Comprehensive Coverage
- [ ] 90%+ test coverage với unit, integration, và e2e tests
- [ ] Zero critical security vulnerabilities với security scanning
- [ ] Comprehensive error handling với graceful degradation
- [ ] Complete API documentation với OpenAPI specification
- [ ] Performance benchmarks met với load testing
- [ ] Code quality standards met với linting và formatting
- [ ] Database optimization với proper indexing và query optimization

### 🚨 Enhanced Risk Mitigation

#### Technical Risks với Advanced Solutions
- **Risk**: Database performance issues → Mitigation: Proper indexing, query optimization, connection pooling, read replicas
- **Risk**: Memory leaks → Mitigation: Connection pooling, resource cleanup, garbage collection monitoring, memory profiling
- **Risk**: Security vulnerabilities → Mitigation: Input validation, SQL injection prevention, security scanning, penetration testing
- **Risk**: Worker pool bottlenecks → Mitigation: Auto-scaling, load balancing, health monitoring, circuit breaker pattern
- **Risk**: WebSocket connection issues → Mitigation: Connection pooling, heartbeat monitoring, automatic reconnection

#### Integration Risks với Comprehensive Testing
- **Risk**: beAuth integration issues → Mitigation: Comprehensive testing, fallback mechanisms, circuit breaker, health checks
- **Risk**: Frontend compatibility → Mitigation: API versioning, backward compatibility, contract testing, schema validation
- **Risk**: Real-time performance → Mitigation: WebSocket optimization, caching, batching, performance monitoring
- **Risk**: Database connection issues → Mitigation: Connection pooling, retry logic, health checks, failover mechanisms

#### Operational Risks với Monitoring
- **Risk**: Deployment issues → Mitigation: Docker configuration, environment setup, health checks, rollback procedures
- **Risk**: Monitoring gaps → Mitigation: Comprehensive logging, alerting setup, metrics collection, dashboard monitoring
- **Risk**: Scalability issues → Mitigation: Load testing, performance optimization, auto-scaling, capacity planning
- **Risk**: Data loss → Mitigation: Backup procedures, data replication, disaster recovery, point-in-time recovery

### 🔄 Implementation Workflow

#### Development Workflow với Best Practices
1. **Feature Development**: Branch-based development với feature flags
2. **Code Review**: Mandatory code review với automated checks
3. **Testing**: Comprehensive testing với CI/CD pipeline
4. **Deployment**: Blue-green deployment với health checks
5. **Monitoring**: Real-time monitoring với alerting
6. **Documentation**: Continuous documentation updates

#### Quality Gates với Automated Checks
- [ ] Code quality checks với linting và formatting
- [ ] Security scanning với vulnerability assessment
- [ ] Performance testing với load testing
- [ ] Integration testing với service communication
- [ ] Documentation completeness với API documentation
- [ ] Test coverage với minimum thresholds

---

**Document Version**: 2.0  
**Created**: 2024-07-09  
**Last Updated**: 2024-12-19  
**Status**: Enhanced for Senior Development  
**Next Review**: After Phase 1 completion  
**Contributors**: Senior Development Team  
**Reviewers**: Architecture Team, Security Team, DevOps Team 