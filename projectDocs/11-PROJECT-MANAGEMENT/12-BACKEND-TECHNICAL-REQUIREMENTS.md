# Backend Technical Requirements
## AI Camera Counting System

### 📊 Tổng quan

Tài liệu này định nghĩa các yêu cầu kỹ thuật chi tiết cho backend development của hệ thống AI Camera Counting, bao gồm API design patterns, database optimization, caching strategy, error handling, rate limiting, và API versioning.

### 🎯 Mục tiêu kỹ thuật

#### Mục tiêu chính
- Xây dựng scalable và maintainable backend architecture
- Đảm bảo performance tối ưu với high concurrency
- Cung cấp robust error handling và monitoring
- Tuân thủ security best practices
- Tối ưu hóa database performance và caching

#### Mục tiêu kỹ thuật
- API response time <200ms
- Database query time <50ms
- 99.9% uptime SLA
- Zero critical security vulnerabilities
- Comprehensive error handling
- Rate limiting implementation

### 🏗️ Architecture Patterns

#### 1. REST API Design Patterns

##### Resource-based URL Design

```python
# API Endpoint Structure
# Base URL: /api/v1

# Camera Management
GET    /api/v1/cameras              # List all cameras
POST   /api/v1/cameras              # Create new camera
GET    /api/v1/cameras/{id}         # Get camera by ID
PUT    /api/v1/cameras/{id}         # Update camera
DELETE /api/v1/cameras/{id}         # Delete camera
PATCH  /api/v1/cameras/{id}/status  # Update camera status

# Counting Data
GET    /api/v1/cameras/{id}/counts  # Get counts for camera
POST   /api/v1/cameras/{id}/counts  # Add new count data
GET    /api/v1/counts/realtime      # Get real-time counts
GET    /api/v1/counts/analytics     # Get analytics data

# User Management
GET    /api/v1/users                # List users
POST   /api/v1/users                # Create user
GET    /api/v1/users/{id}           # Get user by ID
PUT    /api/v1/users/{id}           # Update user
DELETE /api/v1/users/{id}           # Delete user

# Authentication
POST   /api/v1/auth/login           # User login
POST   /api/v1/auth/logout          # User logout
POST   /api/v1/auth/refresh         # Refresh token
POST   /api/v1/auth/register        # User registration
```

##### HTTP Methods Implementation

```python
# FastAPI Implementation
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List, Optional
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="AI Camera API", version="1.0.0")
security = HTTPBearer()

# Pydantic Models
class CameraCreate(BaseModel):
    name: str
    location: str
    ip_address: str
    port: int
    username: Optional[str] = None
    password: Optional[str] = None
    status: str = "inactive"

class CameraUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    status: Optional[str] = None

class CountData(BaseModel):
    camera_id: str
    count: int
    timestamp: str
    confidence: float
    image_url: Optional[str] = None

# Camera Endpoints
@app.get("/api/v1/cameras", response_model=List[Camera])
async def get_cameras(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    """Get list of cameras with pagination and filtering"""
    try:
        cameras = await camera_service.get_cameras(
            skip=skip, 
            limit=limit, 
            status=status,
            user_id=current_user.id
        )
        return cameras
    except Exception as e:
        logger.error(f"Error fetching cameras: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@app.post("/api/v1/cameras", response_model=Camera, status_code=201)
async def create_camera(
    camera: CameraCreate,
    current_user: User = Depends(get_current_user)
):
    """Create a new camera"""
    try:
        # Validate camera connection
        is_connected = await camera_service.test_connection(camera)
        if not is_connected:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot connect to camera"
            )
        
        new_camera = await camera_service.create_camera(camera, current_user.id)
        return new_camera
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating camera: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@app.get("/api/v1/cameras/{camera_id}", response_model=Camera)
async def get_camera(
    camera_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get camera by ID"""
    try:
        camera = await camera_service.get_camera_by_id(camera_id, current_user.id)
        if not camera:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Camera not found"
            )
        return camera
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching camera {camera_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@app.put("/api/v1/cameras/{camera_id}", response_model=Camera)
async def update_camera(
    camera_id: str,
    camera_update: CameraUpdate,
    current_user: User = Depends(get_current_user)
):
    """Update camera"""
    try:
        updated_camera = await camera_service.update_camera(
            camera_id, 
            camera_update, 
            current_user.id
        )
        if not updated_camera:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Camera not found"
            )
        return updated_camera
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating camera {camera_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@app.delete("/api/v1/cameras/{camera_id}", status_code=204)
async def delete_camera(
    camera_id: str,
    current_user: User = Depends(get_current_user)
):
    """Delete camera"""
    try:
        success = await camera_service.delete_camera(camera_id, current_user.id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Camera not found"
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting camera {camera_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
```

#### 2. Database Optimization

##### Indexing Strategy

```sql
-- Database Schema with Optimized Indexes

-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'user',
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for users table
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_created_at ON users(created_at);

-- Cameras table
CREATE TABLE cameras (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    location VARCHAR(500),
    ip_address INET NOT NULL,
    port INTEGER NOT NULL DEFAULT 554,
    username VARCHAR(100),
    password_hash VARCHAR(255),
    status VARCHAR(50) DEFAULT 'inactive',
    last_connected TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for cameras table
CREATE INDEX idx_cameras_user_id ON cameras(user_id);
CREATE INDEX idx_cameras_status ON cameras(status);
CREATE INDEX idx_cameras_ip_address ON cameras(ip_address);
CREATE INDEX idx_cameras_created_at ON cameras(created_at);
CREATE INDEX idx_cameras_user_status ON cameras(user_id, status);

-- Count data table
CREATE TABLE count_data (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    camera_id UUID NOT NULL REFERENCES cameras(id) ON DELETE CASCADE,
    count INTEGER NOT NULL,
    confidence DECIMAL(5,4) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    image_url VARCHAR(500),
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for count_data table
CREATE INDEX idx_count_data_camera_id ON count_data(camera_id);
CREATE INDEX idx_count_data_timestamp ON count_data(timestamp);
CREATE INDEX idx_count_data_camera_timestamp ON count_data(camera_id, timestamp);
CREATE INDEX idx_count_data_created_at ON count_data(created_at);

-- Partitioning for large datasets
CREATE TABLE count_data_2024_01 PARTITION OF count_data
FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

CREATE TABLE count_data_2024_02 PARTITION OF count_data
FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');
```

##### Query Optimization

```python
# Optimized Database Queries
from sqlalchemy import select, func, and_, desc
from sqlalchemy.orm import joinedload, selectinload
from typing import List, Optional
import asyncio

class CameraRepository:
    def __init__(self, db_session):
        self.db = db_session

    async def get_cameras_with_counts(
        self, 
        user_id: str, 
        status: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Camera]:
        """Get cameras with latest count data"""
        query = (
            select(Camera)
            .options(
                selectinload(Camera.latest_count),
                selectinload(Camera.user)
            )
            .where(Camera.user_id == user_id)
        )
        
        if status:
            query = query.where(Camera.status == status)
        
        query = query.limit(limit).offset(offset)
        
        result = await self.db.execute(query)
        return result.scalars().unique().all()

    async def get_camera_analytics(
        self, 
        camera_id: str, 
        start_date: datetime,
        end_date: datetime
    ) -> dict:
        """Get analytics data for camera with optimized queries"""
        
        # Use CTE for complex analytics
        analytics_query = """
        WITH hourly_counts AS (
            SELECT 
                DATE_TRUNC('hour', timestamp) as hour,
                AVG(count) as avg_count,
                MAX(count) as max_count,
                MIN(count) as min_count,
                COUNT(*) as total_records
            FROM count_data 
            WHERE camera_id = :camera_id 
            AND timestamp BETWEEN :start_date AND :end_date
            GROUP BY DATE_TRUNC('hour', timestamp)
        ),
        daily_totals AS (
            SELECT 
                DATE(timestamp) as day,
                SUM(count) as total_count,
                AVG(confidence) as avg_confidence
            FROM count_data 
            WHERE camera_id = :camera_id 
            AND timestamp BETWEEN :start_date AND :end_date
            GROUP BY DATE(timestamp)
        )
        SELECT 
            (SELECT COUNT(*) FROM count_data WHERE camera_id = :camera_id) as total_records,
            (SELECT AVG(count) FROM count_data WHERE camera_id = :camera_id) as overall_avg,
            (SELECT MAX(count) FROM count_data WHERE camera_id = :camera_id) as peak_count
        """
        
        result = await self.db.execute(
            analytics_query,
            {
                "camera_id": camera_id,
                "start_date": start_date,
                "end_date": end_date
            }
        )
        
        return result.fetchone()

    async def get_real_time_counts(self, user_id: str) -> List[dict]:
        """Get real-time counts for all user cameras"""
        query = """
        SELECT 
            c.id as camera_id,
            c.name as camera_name,
            c.status,
            cd.count,
            cd.confidence,
            cd.timestamp
        FROM cameras c
        LEFT JOIN LATERAL (
            SELECT count, confidence, timestamp
            FROM count_data 
            WHERE camera_id = c.id 
            ORDER BY timestamp DESC 
            LIMIT 1
        ) cd ON true
        WHERE c.user_id = :user_id
        ORDER BY cd.timestamp DESC NULLS LAST
        """
        
        result = await self.db.execute(query, {"user_id": user_id})
        return [dict(row) for row in result.fetchall()]
```

#### 3. Caching Strategy

##### Redis Cache Implementation

```python
# Redis Cache Service
import redis.asyncio as redis
import json
import pickle
from typing import Any, Optional, Union
from datetime import timedelta
import hashlib

class CacheService:
    def __init__(self, redis_url: str):
        self.redis = redis.from_url(redis_url)
        self.default_ttl = 3600  # 1 hour

    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        try:
            value = await self.redis.get(key)
            if value:
                return pickle.loads(value)
            return None
        except Exception as e:
            logger.error(f"Cache get error: {str(e)}")
            return None

    async def set(
        self, 
        key: str, 
        value: Any, 
        ttl: Optional[int] = None
    ) -> bool:
        """Set value in cache"""
        try:
            ttl = ttl or self.default_ttl
            serialized_value = pickle.dumps(value)
            await self.redis.setex(key, ttl, serialized_value)
            return True
        except Exception as e:
            logger.error(f"Cache set error: {str(e)}")
            return False

    async def delete(self, key: str) -> bool:
        """Delete value from cache"""
        try:
            await self.redis.delete(key)
            return True
        except Exception as e:
            logger.error(f"Cache delete error: {str(e)}")
            return False

    async def invalidate_pattern(self, pattern: str) -> bool:
        """Invalidate all keys matching pattern"""
        try:
            keys = await self.redis.keys(pattern)
            if keys:
                await self.redis.delete(*keys)
            return True
        except Exception as e:
            logger.error(f"Cache pattern invalidation error: {str(e)}")
            return False

    def generate_key(self, *args, **kwargs) -> str:
        """Generate cache key from arguments"""
        key_parts = [str(arg) for arg in args]
        key_parts.extend([f"{k}:{v}" for k, v in sorted(kwargs.items())])
        key_string = "|".join(key_parts)
        return hashlib.md5(key_string.encode()).hexdigest()

# Cache Decorator
def cache_result(ttl: int = 3600, key_prefix: str = ""):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            cache_service = CacheService(settings.REDIS_URL)
            
            # Generate cache key
            cache_key = f"{key_prefix}:{cache_service.generate_key(*args, **kwargs)}"
            
            # Try to get from cache
            cached_result = await cache_service.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            # Execute function and cache result
            result = await func(*args, **kwargs)
            await cache_service.set(cache_key, result, ttl)
            
            return result
        return wrapper
    return decorator

# Usage Examples
class CameraService:
    def __init__(self, db_session, cache_service):
        self.db = db_session
        self.cache = cache_service

    @cache_result(ttl=300, key_prefix="camera")
    async def get_camera_by_id(self, camera_id: str, user_id: str) -> Optional[Camera]:
        """Get camera with caching"""
        return await self.db.get_camera(camera_id, user_id)

    @cache_result(ttl=60, key_prefix="counts")
    async def get_real_time_counts(self, user_id: str) -> List[dict]:
        """Get real-time counts with caching"""
        return await self.db.get_real_time_counts(user_id)

    async def update_camera(self, camera_id: str, data: dict, user_id: str) -> Camera:
        """Update camera and invalidate cache"""
        updated_camera = await self.db.update_camera(camera_id, data, user_id)
        
        # Invalidate related cache
        await self.cache.invalidate_pattern(f"camera:*{camera_id}*")
        await self.cache.invalidate_pattern(f"counts:*{user_id}*")
        
        return updated_camera
```

#### 4. Error Handling

##### Global Error Handler

```python
# Global Error Handler
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging
import traceback
from typing import Union

logger = logging.getLogger(__name__)

class CustomHTTPException(HTTPException):
    def __init__(
        self,
        status_code: int,
        detail: str,
        error_code: str = None,
        error_type: str = None
    ):
        super().__init__(status_code=status_code, detail=detail)
        self.error_code = error_code
        self.error_type = error_type

class ErrorHandler:
    @staticmethod
    async def http_exception_handler(request: Request, exc: HTTPException):
        """Handle HTTP exceptions"""
        error_response = {
            "error": {
                "code": getattr(exc, 'error_code', 'HTTP_ERROR'),
                "type": getattr(exc, 'error_type', 'HTTP_EXCEPTION'),
                "message": exc.detail,
                "status_code": exc.status_code,
                "path": request.url.path,
                "timestamp": datetime.utcnow().isoformat()
            }
        }
        
        logger.error(f"HTTP Exception: {error_response}")
        return JSONResponse(
            status_code=exc.status_code,
            content=error_response
        )

    @staticmethod
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """Handle validation errors"""
        error_response = {
            "error": {
                "code": "VALIDATION_ERROR",
                "type": "VALIDATION_EXCEPTION",
                "message": "Request validation failed",
                "details": exc.errors(),
                "status_code": 422,
                "path": request.url.path,
                "timestamp": datetime.utcnow().isoformat()
            }
        }
        
        logger.error(f"Validation Error: {error_response}")
        return JSONResponse(
            status_code=422,
            content=error_response
        )

    @staticmethod
    async def general_exception_handler(request: Request, exc: Exception):
        """Handle general exceptions"""
        error_response = {
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "type": "GENERAL_EXCEPTION",
                "message": "An unexpected error occurred",
                "status_code": 500,
                "path": request.url.path,
                "timestamp": datetime.utcnow().isoformat()
            }
        }
        
        # Log full error details
        logger.error(f"General Exception: {str(exc)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        
        # In production, don't expose internal errors
        if settings.DEBUG:
            error_response["error"]["details"] = str(exc)
            error_response["error"]["traceback"] = traceback.format_exc()
        
        return JSONResponse(
            status_code=500,
            content=error_response
        )

# Custom Error Classes
class CameraNotFoundError(CustomHTTPException):
    def __init__(self, camera_id: str):
        super().__init__(
            status_code=404,
            detail=f"Camera with ID {camera_id} not found",
            error_code="CAMERA_NOT_FOUND",
            error_type="NOT_FOUND"
        )

class CameraConnectionError(CustomHTTPException):
    def __init__(self, camera_id: str, reason: str):
        super().__init__(
            status_code=400,
            detail=f"Cannot connect to camera {camera_id}: {reason}",
            error_code="CAMERA_CONNECTION_ERROR",
            error_type="CONNECTION_ERROR"
        )

class PermissionDeniedError(CustomHTTPException):
    def __init__(self, resource: str):
        super().__init__(
            status_code=403,
            detail=f"Permission denied to access {resource}",
            error_code="PERMISSION_DENIED",
            error_type="AUTHORIZATION_ERROR"
        )

class RateLimitExceededError(CustomHTTPException):
    def __init__(self, retry_after: int = 60):
        super().__init__(
            status_code=429,
            detail="Rate limit exceeded",
            error_code="RATE_LIMIT_EXCEEDED",
            error_type="RATE_LIMIT"
        )

# Register error handlers
app.add_exception_handler(HTTPException, ErrorHandler.http_exception_handler)
app.add_exception_handler(RequestValidationError, ErrorHandler.validation_exception_handler)
app.add_exception_handler(Exception, ErrorHandler.general_exception_handler)
```

#### 5. Rate Limiting

##### Token Bucket Algorithm Implementation

```python
# Rate Limiting Service
import time
import asyncio
from typing import Dict, Tuple
from dataclasses import dataclass
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)

@dataclass
class RateLimitConfig:
    requests_per_minute: int = 60
    requests_per_hour: int = 1000
    burst_size: int = 10

class TokenBucket:
    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = capacity
        self.last_refill = time.time()

    def consume(self, tokens: int = 1) -> bool:
        """Consume tokens from bucket"""
        now = time.time()
        
        # Refill tokens
        time_passed = now - self.last_refill
        tokens_to_add = time_passed * self.refill_rate
        self.tokens = min(self.capacity, self.tokens + tokens_to_add)
        self.last_refill = now
        
        # Check if enough tokens available
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False

class RateLimiter:
    def __init__(self):
        self.buckets: Dict[str, TokenBucket] = {}
        self.configs: Dict[str, RateLimitConfig] = defaultdict(
            lambda: RateLimitConfig()
        )

    def set_config(self, key: str, config: RateLimitConfig):
        """Set rate limit configuration for key"""
        self.configs[key] = config

    def is_allowed(self, key: str, cost: int = 1) -> Tuple[bool, int]:
        """Check if request is allowed"""
        if key not in self.buckets:
            config = self.configs[key]
            self.buckets[key] = TokenBucket(
                capacity=config.burst_size,
                refill_rate=config.requests_per_minute / 60.0
            )
        
        bucket = self.buckets[key]
        allowed = bucket.consume(cost)
        
        # Calculate retry after
        if not allowed:
            retry_after = int(60 / self.configs[key].requests_per_minute)
        else:
            retry_after = 0
        
        return allowed, retry_after

# Rate Limiting Middleware
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
import time

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, rate_limiter: RateLimiter):
        super().__init__(app)
        self.rate_limiter = rate_limiter

    async def dispatch(self, request: Request, call_next):
        # Get client identifier
        client_id = self.get_client_id(request)
        
        # Check rate limit
        allowed, retry_after = self.rate_limiter.is_allowed(client_id)
        
        if not allowed:
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded",
                headers={"Retry-After": str(retry_after)}
            )
        
        # Add rate limit headers
        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = "60"
        response.headers["X-RateLimit-Remaining"] = "59"  # Calculate actual remaining
        response.headers["X-RateLimit-Reset"] = str(int(time.time()) + 60)
        
        return response

    def get_client_id(self, request: Request) -> str:
        """Get client identifier for rate limiting"""
        # Use IP address as default
        client_ip = request.client.host
        
        # If user is authenticated, use user ID
        if hasattr(request.state, 'user'):
            return f"user:{request.state.user.id}"
        
        return f"ip:{client_ip}"

# Usage
rate_limiter = RateLimiter()

# Set different limits for different endpoints
rate_limiter.set_config(
    "api:cameras", 
    RateLimitConfig(requests_per_minute=30, requests_per_hour=500)
)

rate_limiter.set_config(
    "api:counts", 
    RateLimitConfig(requests_per_minute=100, requests_per_hour=2000)
)

# Add middleware to app
app.add_middleware(RateLimitMiddleware, rate_limiter=rate_limiter)
```

#### 6. API Versioning

##### URL Versioning Implementation

```python
# API Versioning
from fastapi import APIRouter, Depends
from typing import Dict, Any

# Version 1 API
v1_router = APIRouter(prefix="/api/v1")

@v1_router.get("/cameras")
async def get_cameras_v1():
    """Version 1 camera endpoint"""
    return {"version": "1.0", "endpoint": "cameras"}

# Version 2 API
v2_router = APIRouter(prefix="/api/v2")

@v2_router.get("/cameras")
async def get_cameras_v2():
    """Version 2 camera endpoint with enhanced features"""
    return {"version": "2.0", "endpoint": "cameras", "features": ["pagination", "filtering"]}

# Include routers
app.include_router(v1_router, tags=["v1"])
app.include_router(v2_router, tags=["v2"])

# Version Management
class APIVersionManager:
    def __init__(self):
        self.versions = {
            "1.0": {
                "status": "stable",
                "deprecated": False,
                "sunset_date": None,
                "features": ["basic_crud", "authentication"]
            },
            "2.0": {
                "status": "beta",
                "deprecated": False,
                "sunset_date": None,
                "features": ["basic_crud", "authentication", "pagination", "filtering", "analytics"]
            }
        }

    def get_version_info(self, version: str) -> Dict[str, Any]:
        """Get version information"""
        return self.versions.get(version, {})

    def is_deprecated(self, version: str) -> bool:
        """Check if version is deprecated"""
        version_info = self.versions.get(version, {})
        return version_info.get("deprecated", False)

    def get_sunset_date(self, version: str) -> str:
        """Get sunset date for version"""
        version_info = self.versions.get(version, {})
        return version_info.get("sunset_date")

# Version middleware
class VersionMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, version_manager: APIVersionManager):
        super().__init__(app)
        self.version_manager = version_manager

    async def dispatch(self, request: Request, call_next):
        # Check if version is deprecated
        path = request.url.path
        if "/api/v" in path:
            version = path.split("/api/v")[1].split("/")[0]
            if self.version_manager.is_deprecated(version):
                sunset_date = self.version_manager.get_sunset_date(version)
                response = JSONResponse(
                    status_code=410,
                    content={
                        "error": "API version deprecated",
                        "sunset_date": sunset_date,
                        "message": f"Please upgrade to a newer version"
                    }
                )
                response.headers["Sunset"] = sunset_date
                return response
        
        response = await call_next(request)
        
        # Add version headers
        if "/api/v" in path:
            version = path.split("/api/v")[1].split("/")[0]
            version_info = self.version_manager.get_version_info(version)
            response.headers["X-API-Version"] = version
            response.headers["X-API-Status"] = version_info.get("status", "unknown")
        
        return response
```

#### 7. Database Migration Strategy

##### Alembic Migration Implementation

```python
# Database Migration with Alembic
from alembic import command
from alembic.config import Config
from alembic.script import ScriptDirectory
from alembic.runtime.migration import MigrationContext
from sqlalchemy import create_engine, text
import logging

logger = logging.getLogger(__name__)

class DatabaseMigrator:
    def __init__(self, database_url: str, alembic_cfg_path: str = "alembic.ini"):
        self.database_url = database_url
        self.alembic_cfg = Config(alembic_cfg_path)
        self.alembic_cfg.set_main_option("sqlalchemy.url", database_url)

    def create_migration(self, message: str) -> str:
        """Create a new migration"""
        try:
            command.revision(self.alembic_cfg, message=message, autogenerate=True)
            logger.info(f"Created migration: {message}")
            return "Migration created successfully"
        except Exception as e:
            logger.error(f"Error creating migration: {str(e)}")
            raise

    def upgrade_database(self, revision: str = "head") -> str:
        """Upgrade database to specified revision"""
        try:
            command.upgrade(self.alembic_cfg, revision)
            logger.info(f"Database upgraded to revision: {revision}")
            return "Database upgraded successfully"
        except Exception as e:
            logger.error(f"Error upgrading database: {str(e)}")
            raise

    def downgrade_database(self, revision: str) -> str:
        """Downgrade database to specified revision"""
        try:
            command.downgrade(self.alembic_cfg, revision)
            logger.info(f"Database downgraded to revision: {revision}")
            return "Database downgraded successfully"
        except Exception as e:
            logger.error(f"Error downgrading database: {str(e)}")
            raise

    def get_current_revision(self) -> str:
        """Get current database revision"""
        try:
            engine = create_engine(self.database_url)
            with engine.connect() as connection:
                context = MigrationContext.configure(connection)
                return context.get_current_revision()
        except Exception as e:
            logger.error(f"Error getting current revision: {str(e)}")
            return "unknown"

    def get_migration_history(self) -> list:
        """Get migration history"""
        try:
            script_dir = ScriptDirectory.from_config(self.alembic_cfg)
            return [rev.revision for rev in script_dir.walk_revisions()]
        except Exception as e:
            logger.error(f"Error getting migration history: {str(e)}")
            return []

# Migration Scripts
# migrations/versions/001_initial_schema.py
"""Initial schema

Revision ID: 001
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create users table
    op.create_table('users',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('username', sa.String(length=100), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('role', sa.String(length=50), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=True),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username')
    )

    # Create cameras table
    op.create_table('cameras',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('location', sa.String(length=500), nullable=True),
        sa.Column('ip_address', postgresql.INET(), nullable=False),
        sa.Column('port', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=100), nullable=True),
        sa.Column('password_hash', sa.String(length=255), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=True),
        sa.Column('last_connected', sa.TIMESTAMP(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=True),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Create indexes
    op.create_index('idx_cameras_user_id', 'cameras', ['user_id'])
    op.create_index('idx_cameras_status', 'cameras', ['status'])

def downgrade():
    op.drop_index('idx_cameras_status', table_name='cameras')
    op.drop_index('idx_cameras_user_id', table_name='cameras')
    op.drop_table('cameras')
    op.drop_table('users')
```

#### 8. API Documentation

##### OpenAPI 3.0 Configuration

```python
# OpenAPI Configuration
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="AI Camera Counting API",
        version="1.0.0",
        description="""
        ## AI Camera Counting System API
        
        This API provides endpoints for managing AI-powered camera counting systems.
        
        ### Features
        * Camera Management
        * Real-time Counting
        * Analytics and Reporting
        * User Authentication
        * Rate Limiting
        
        ### Authentication
        All endpoints require authentication using JWT tokens.
        
        ### Rate Limiting
        API requests are rate limited to ensure fair usage.
        
        ### Versioning
        API versioning is supported through URL paths (/api/v1, /api/v2).
        """,
        routes=app.routes,
    )
    
    # Custom OpenAPI schema
    openapi_schema["info"]["x-logo"] = {
        "url": "https://example.com/logo.png"
    }
    
    # Add security schemes
    openapi_schema["components"]["securitySchemes"] = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    
    # Add global security
    openapi_schema["security"] = [{"bearerAuth": []}]
    
    # Add server information
    openapi_schema["servers"] = [
        {
            "url": "https://api.aicamera.com",
            "description": "Production server"
        },
        {
            "url": "https://staging-api.aicamera.com",
            "description": "Staging server"
        },
        {
            "url": "http://localhost:8000",
            "description": "Development server"
        }
    ]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Documentation Examples
from pydantic import BaseModel, Field
from typing import List, Optional

class CameraResponse(BaseModel):
    id: str = Field(..., description="Unique camera identifier")
    name: str = Field(..., description="Camera name")
    location: Optional[str] = Field(None, description="Camera location")
    status: str = Field(..., description="Camera status (active/inactive)")
    ip_address: str = Field(..., description="Camera IP address")
    port: int = Field(..., description="Camera port")
    created_at: str = Field(..., description="Creation timestamp")
    
    class Config:
        schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "name": "Main Entrance Camera",
                "location": "Building A, Floor 1",
                "status": "active",
                "ip_address": "192.168.1.100",
                "port": 554,
                "created_at": "2024-01-01T00:00:00Z"
            }
        }

class CountDataResponse(BaseModel):
    camera_id: str = Field(..., description="Camera identifier")
    count: int = Field(..., description="Number of people detected")
    confidence: float = Field(..., description="Detection confidence (0-1)")
    timestamp: str = Field(..., description="Detection timestamp")
    image_url: Optional[str] = Field(None, description="Captured image URL")
    
    class Config:
        schema_extra = {
            "example": {
                "camera_id": "550e8400-e29b-41d4-a716-446655440000",
                "count": 5,
                "confidence": 0.95,
                "timestamp": "2024-01-01T12:00:00Z",
                "image_url": "https://example.com/images/capture.jpg"
            }
        }

# Enhanced endpoint documentation
@app.get(
    "/api/v1/cameras",
    response_model=List[CameraResponse],
    summary="Get all cameras",
    description="Retrieve a list of all cameras for the authenticated user",
    response_description="List of cameras",
    tags=["Cameras"]
)
async def get_cameras(
    skip: int = Field(0, ge=0, description="Number of records to skip"),
    limit: int = Field(100, ge=1, le=1000, description="Maximum number of records to return"),
    status: Optional[str] = Field(None, description="Filter by camera status"),
    current_user: User = Depends(get_current_user)
):
    """
    Get all cameras for the authenticated user.
    
    - **skip**: Number of records to skip for pagination
    - **limit**: Maximum number of records to return (max 1000)
    - **status**: Filter cameras by status (active/inactive)
    
    Returns a list of cameras with their basic information.
    """
    pass
```

### 📋 Implementation Checklist

#### Phase 1: Foundation Setup (Week 1)
- [ ] Setup FastAPI with proper project structure
- [ ] Configure database connection and models
- [ ] Implement basic CRUD operations
- [ ] Setup authentication system
- [ ] Configure logging and monitoring

#### Phase 2: API Development (Week 2)
- [ ] Implement REST API endpoints
- [ ] Add request/response validation
- [ ] Implement error handling
- [ ] Add rate limiting
- [ ] Setup API documentation

#### Phase 3: Performance Optimization (Week 3)
- [ ] Implement caching strategy
- [ ] Optimize database queries
- [ ] Add database indexing
- [ ] Implement connection pooling
- [ ] Setup performance monitoring

#### Phase 4: Security & Production (Week 4)
- [ ] Implement security middleware
- [ ] Add API versioning
- [ ] Setup database migrations
- [ ] Configure production settings
- [ ] Implement health checks

### 🎯 Success Metrics

#### Performance Metrics
- **API Response Time**: <200ms average
- **Database Query Time**: <50ms average
- **Cache Hit Rate**: >80%
- **Error Rate**: <1%
- **Uptime**: 99.9%

#### Security Metrics
- **Security Vulnerabilities**: 0 critical
- **Authentication Success Rate**: >99%
- **Rate Limiting Effectiveness**: 100%
- **Data Encryption**: 100%

#### Quality Metrics
- **Code Coverage**: >80%
- **API Documentation**: 100% complete
- **Error Handling**: Comprehensive
- **Logging**: Complete audit trail

### 🚨 Risk Mitigation

#### Performance Risks
- **Risk**: Database performance degradation
- **Mitigation**: Proper indexing, query optimization, caching

#### Security Risks
- **Risk**: API security vulnerabilities
- **Mitigation**: Input validation, rate limiting, authentication

#### Scalability Risks
- **Risk**: System overload under high load
- **Mitigation**: Horizontal scaling, load balancing, caching

#### Data Risks
- **Risk**: Data loss or corruption
- **Mitigation**: Regular backups, data validation, transaction management

---

**Document Version**: 1.0  
**Last Updated**: [Current Date]  
**Next Review**: [Date + 2 weeks]  
**Status**: Ready for Implementation
