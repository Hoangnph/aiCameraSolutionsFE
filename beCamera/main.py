from fastapi import FastAPI, HTTPException, Depends, Request, Body, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
import uvicorn
import os
# Remove load_dotenv() to use container environment variables
import psycopg2
import redis
import logging
from datetime import datetime
import httpx
from typing import Optional
from worker_pool import worker_pool
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from pydantic import BaseModel
import re
import time

# Rate limit configuration model
class RateLimitConfig(BaseModel):
    rate_limit: str
    description: Optional[str] = None

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Custom exception handler for authentication
async def auth_exception_handler(request: Request, exc: HTTPException):
    """Custom exception handler for authentication errors"""
    if exc.status_code == 403 and "Not authenticated" in str(exc.detail):
        return JSONResponse(
            status_code=401,
            content={"detail": "Not authenticated"}
        )
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

# Initialize FastAPI app
app = FastAPI(
    title="AI Camera Counting Service",
    description="Service for processing camera feeds and counting people using AI",
    version="1.0.0"
)

# Add custom exception handler
app.add_exception_handler(HTTPException, auth_exception_handler)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("CORS_ORIGIN", "http://localhost:3000")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    """Startup event - initialize worker pool"""
    await worker_pool.start()
    logger.info("Application started - worker pool initialized")

@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event - cleanup worker pool"""
    await worker_pool.stop()
    logger.info("Application shutdown - worker pool stopped")

# Utility functions
def is_valid_ip(ip_address: str) -> bool:
    """Validate IP address format"""
    try:
        import ipaddress
        ipaddress.ip_address(ip_address)
        return True
    except ValueError:
        return False

def is_safe_string(value: str) -> bool:
    """Check for truly dangerous SQLi/XSS patterns, allow normal camera names"""
    if not value:
        return True
    # Only reject if contains script tag, SQL keywords, or obvious XSS
    dangerous_patterns = [
        '<script', '</script>', 'javascript:', 'onerror', 'onload', 'alert(', 'document.cookie',
        'src=', 'eval(', 'base64', 'fromCharCode', 'iframe', 'window.location', 'prompt(',
        ';', '--', '/*', '*/', 'xp_', 'union select', 'select from', 'insert into', 'update set', 'delete from', 'drop table', 'alter table',
        'delete from', 'drop table', 'alter table', 'create table', 'truncate table', 'exec ', 'execute ',
        'union all', 'union select', 'select *', 'select count', 'select id', 'select name'
    ]
    value_lower = value.lower()
    for pattern in dangerous_patterns:
        if pattern in value_lower:
            return False
    # Allow: chữ, số, khoảng trắng, gạch ngang, gạch dưới, dấu chấm, phẩy, ngoặc đơn, ngoặc kép
    import re
    if not re.match(r"^[\w\s\-\_\.\,\'\"]+$", value):
        return False
    return True

def is_safe_rtsp_url(value: str) -> bool:
    """Check if RTSP URL is safe and valid"""
    if not value:
        return True
    # Check for dangerous patterns in URL
    dangerous_patterns = [
        'javascript:', 'data:', 'vbscript:', 'file:', 'ftp:', 'gopher:', 'mailto:',
        ';', '--', '/*', '*/', 'union', 'select', 'insert', 'update', 'delete', 'drop', 'alter', 'create', 'exec'
    ]
    value_lower = value.lower()
    for pattern in dangerous_patterns:
        if pattern in value_lower:
            return False
    # Check if it's a valid RTSP URL format
    import re
    if not re.match(r"^rtsp://[\w\-\.]+(:\d+)?(/[\w\-\./]*)?$", value):
        return False
    return True

# Authentication functions
async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify JWT token with beAuth service"""
    token = credentials.credentials
    auth_service_url = os.getenv("AUTH_SERVICE_URL", "http://beauth_service:3001")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{auth_service_url}/api/v1/auth/verify",
                headers={"Authorization": f"Bearer {token}"}
            )
            if response.status_code != 200:
                raise HTTPException(
                    status_code=401,
                    detail="Invalid token"
                )
            return response.json()
    except httpx.RequestError as e:
        logger.error(f"Error connecting to auth service: {e}")
        raise HTTPException(
            status_code=503,
            detail="Authentication service unavailable"
        )

async def get_current_user(token_data: dict = Depends(verify_token)):
    """Get current user from token data"""
    return token_data

# Database connection
def get_db_connection():
    """Get PostgreSQL database connection using shared resources"""
    try:
        connection = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", "5432"),
            database=os.getenv("DB_NAME", "people_counting_db"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "dev_password")
        )
        return connection
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        raise HTTPException(status_code=500, detail="Database connection failed")

# Redis connection
def get_redis_connection():
    """Get Redis connection using shared resources"""
    try:
        redis_client = redis.Redis(
            host=os.getenv("REDIS_HOST", "localhost"),
            port=os.getenv("REDIS_PORT", "6379"),
            password=os.getenv("REDIS_PASSWORD", None),
            decode_responses=True
        )
        # Test connection
        redis_client.ping()
        return redis_client
    except Exception as e:
        logger.error(f"Redis connection error: {e}")
        raise HTTPException(status_code=500, detail="Redis connection failed")

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Test database connection
        db_conn = get_db_connection()
        db_conn.close()
        
        # Test Redis connection
        redis_conn = get_redis_connection()
        redis_conn.ping()
        
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "service": "ai-camera-counting",
            "database": "connected",
            "redis": "connected"
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Service unhealthy")

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "AI Camera Counting Service",
        "version": "1.0.0",
        "status": "running"
    }

# Test endpoint without authentication
@app.get("/api/v1/test/cameras")
async def test_get_cameras():
    """Test endpoint - Get all cameras without authentication"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, name, description, ip_address, rtsp_url, status, created_at 
            FROM cameras 
            ORDER BY created_at DESC
        """)
        
        cameras = []
        for row in cursor.fetchall():
            cameras.append({
                "id": row[0],
                "name": row[1],
                "description": row[2],
                "ip_address": str(row[3]) if row[3] else None,
                "rtsp_url": row[4],
                "status": row[5],
                "created_at": row[6].isoformat() if row[6] else None
            })
        
        cursor.close()
        conn.close()
        
        return {
            "success": True,
            "data": cameras,
            "count": len(cameras)
        }
    except Exception as e:
        logger.error(f"Error getting cameras: {e}")
        raise HTTPException(status_code=500, detail="Failed to get cameras")

@app.get("/api/v1/test/workers/status")
async def test_get_worker_pool_status():
    """Test endpoint - Get worker pool status without authentication"""
    try:
        worker_status = worker_pool.get_worker_status()
        
        return {
            "success": True,
            "data": {
                "workers": worker_status,
                "total_workers": len(worker_status),
                "idle_workers": len([w for w in worker_status if w["status"] == "idle"]),
                "busy_workers": len([w for w in worker_status if w["status"] == "busy"])
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting worker pool status: {e}")
        raise HTTPException(status_code=500, detail="Failed to get worker pool status")

# Rate limiting config - optimized for testing environment
def get_rate_limit_for_environment():
    """Get rate limit based on environment"""
    env = os.getenv("NODE_ENV", "development")
    if env == "production":
        return os.getenv("RATE_LIMIT", "100/minute")
    elif env == "testing":
        return os.getenv("RATE_LIMIT", "1000/minute")
    else:  # development
        return os.getenv("RATE_LIMIT", "2000/minute")

# Custom key function: rate limit theo user id nếu có, fallback theo IP
def user_rate_limit_key(request: Request):
    """Rate limit key function - use user_id if available, fallback to IP"""
    # Check if user_id is stored in request state (set by middleware)
    if hasattr(request, "state") and hasattr(request.state, "user_id") and request.state.user_id:
        return f"user:{request.state.user_id}"
    
    # Fallback to IP address
    return get_remote_address(request)

# Middleware to extract and store user_id from token
@app.middleware("http")
async def extract_user_id_middleware(request: Request, call_next):
    """Extract user_id from JWT token and store in request state, with debug logging"""
    try:
        # Check if Authorization header exists
        auth_header = request.headers.get("authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            logger.info(f"[extract_user_id_middleware] Verifying token for request: {request.url.path}")
            # Verify token with beAuth service
            auth_service_url = os.getenv("AUTH_SERVICE_URL", "http://beauth_service:3001")
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        f"{auth_service_url}/api/v1/auth/verify",
                        headers={"Authorization": f"Bearer {token}"}
                    )
                    logger.info(f"[extract_user_id_middleware] beAuth verify status: {response.status_code}, response: {response.text}")
                    if response.status_code == 200:
                        token_data = response.json()
                        # Store user_id in request state
                        request.state.user_id = token_data.get("userId") or token_data.get("user_id")
                        logger.info(f"[extract_user_id_middleware] user_id extracted: {request.state.user_id}")
                    else:
                        logger.warning(f"[extract_user_id_middleware] Token verify failed: {response.status_code} - {response.text}")
            except Exception as e:
                logger.error(f"[extract_user_id_middleware] Error verifying token with beAuth: {e}")
    except Exception as e:
        logger.error(f"[extract_user_id_middleware] Error extracting user_id from token: {e}")
        # Continue without user_id, will fallback to IP
    
    response = await call_next(request)
    return response

# Custom middleware to add rate limiting headers
@app.middleware("http")
async def add_rate_limit_headers_middleware(request: Request, call_next):
    """Add rate limiting headers to all responses"""
    response = await call_next(request)
    
    try:
        # Always add rate limit headers for authenticated endpoints
        if request.url.path.startswith("/api/"):
            limiter = request.app.state.limiter
            key = limiter.key_func(request)
            
            # Get current rate limit info
            current_limit = get_current_rate_limit()
            limit_parts = current_limit.split('/')
            limit_number = int(limit_parts[0])
            
            # Add basic rate limit headers
            response.headers["X-RateLimit-Limit"] = str(limit_number)
            response.headers["X-RateLimit-Window"] = limit_parts[1]
            
            # Try to get remaining requests from limiter
            try:
                rate_limit = limiter.get_window_stats(key, request)
                if rate_limit:
                    response.headers["X-RateLimit-Remaining"] = str(rate_limit.remaining)
                    response.headers["X-RateLimit-Reset"] = str(rate_limit.reset_time)
                else:
                    # Fallback: assume some requests used
                    response.headers["X-RateLimit-Remaining"] = str(max(0, limit_number - 1))
                    response.headers["X-RateLimit-Reset"] = str(int(time.time()) + 60)
            except Exception as e:
                logger.debug(f"Could not get window stats: {e}")
                # Fallback headers
                response.headers["X-RateLimit-Remaining"] = str(max(0, limit_number - 1))
                response.headers["X-RateLimit-Reset"] = str(int(time.time()) + 60)
                
    except Exception as e:
        logger.error(f"Error adding rate limit headers: {e}")
        # Ensure basic headers are always present
        response.headers["X-RateLimit-Limit"] = "1000"
        response.headers["X-RateLimit-Remaining"] = "999"
        response.headers["X-RateLimit-Reset"] = str(int(time.time()) + 60)
    
    return response

# Custom exception handler for rate limiting
async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    """Custom rate limit exceeded handler with headers"""
    response = JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded"}
    )
    
    # Add retry after header if available
    if hasattr(exc, 'retry_after'):
        response.headers["Retry-After"] = str(exc.retry_after)
    
    # Add rate limit headers - ensure they are always present
    try:
        limiter = request.app.state.limiter
        key = limiter.key_func(request)
        rate_limit = limiter.get_window_stats(key, request)
        if rate_limit:
            response.headers["X-RateLimit-Limit"] = str(rate_limit.limit)
            response.headers["X-RateLimit-Remaining"] = str(rate_limit.remaining)
            response.headers["X-RateLimit-Reset"] = str(rate_limit.reset_time)
        else:
            # Fallback headers if window stats not available
            current_limit = get_current_rate_limit()
            response.headers["X-RateLimit-Limit"] = current_limit.split('/')[0]
            response.headers["X-RateLimit-Remaining"] = "0"
            response.headers["X-RateLimit-Reset"] = str(int(time.time()) + 60)  # 1 minute from now
    except Exception as e:
        logger.error(f"Error adding rate limit headers: {e}")
        # Fallback headers
        response.headers["X-RateLimit-Limit"] = "5"
        response.headers["X-RateLimit-Remaining"] = "0"
        response.headers["X-RateLimit-Reset"] = str(int(time.time()) + 60)
    
    return response

limiter = Limiter(key_func=user_rate_limit_key, default_limits=[get_rate_limit_for_environment()])
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)

# App state for dynamic rate limit
class AppState:
    rate_limit: str = get_rate_limit_for_environment()

app.state.custom = AppState()

# Helper to get current rate limit
def get_current_rate_limit() -> str:
    return getattr(app.state.custom, "rate_limit", get_rate_limit_for_environment())

# Helper to update limiter with new rate limit
def update_limiter(new_limit: str):
    app.state.custom.rate_limit = new_limit
    # Re-create limiter with new limit
    global limiter
    limiter = Limiter(key_func=user_rate_limit_key, default_limits=[new_limit])
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)

# Admin API to get/set rate limit (for dev/admin only)
@app.get("/admin/rate-limit")
async def get_rate_limit(current_user: dict = Depends(get_current_user)):
    # TODO: check admin role if needed
    return {"rate_limit": get_current_rate_limit()}

@app.put("/admin/rate-limit")
async def set_rate_limit(config: RateLimitConfig, current_user: dict = Depends(get_current_user)):
    # TODO: check admin role if needed
    # Validate format: N/period (e.g. 10/minute, 5/second, 100/hour)
    if not re.match(r"^\d+\/(second|minute|hour|day|month|year)s?$", config.rate_limit):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid rate limit format. Use N/period, e.g. 10/minute")
    update_limiter(config.rate_limit)
    return {"rate_limit": get_current_rate_limit()}

# Camera management endpoints
@app.get("/api/v1/cameras")
@limiter.limit(get_current_rate_limit())
async def get_cameras(request: Request, current_user: dict = Depends(get_current_user)):
    """Get all cameras"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, name, description, ip_address, rtsp_url, status, created_at 
            FROM cameras 
            ORDER BY created_at DESC
        """)
        
        cameras = []
        for row in cursor.fetchall():
            cameras.append({
                "id": row[0],
                "name": row[1],
                "description": row[2],
                "ip_address": str(row[3]) if row[3] else None,
                "rtsp_url": row[4],
                "status": row[5],
                "created_at": row[6].isoformat() if row[6] else None
            })
        
        cursor.close()
        conn.close()
        
        return {
            "success": True,
            "data": cameras,
            "count": len(cameras)
        }
    except Exception as e:
        logger.error(f"Error getting cameras: {e}")
        raise HTTPException(status_code=500, detail="Failed to get cameras")

def validate_camera_id(camera_id: int) -> int:
    """Validate camera ID to prevent SQL injection"""
    try:
        # Ensure it's a positive integer
        if not isinstance(camera_id, int) or camera_id <= 0:
            raise HTTPException(status_code=400, detail="Invalid camera ID format")
        return camera_id
    except (ValueError, TypeError):
        raise HTTPException(status_code=400, detail="Invalid camera ID format")

@app.get("/api/v1/cameras/{camera_id}")
@limiter.limit(get_current_rate_limit())
async def get_camera(request: Request, camera_id: int, current_user: dict = Depends(get_current_user)):
    """Get camera by ID"""
    try:
        # Validate camera_id
        camera_id = validate_camera_id(camera_id)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, name, description, ip_address, rtsp_url, status, created_at 
            FROM cameras 
            WHERE id = %s
        """, (camera_id,))
        
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if not row:
            raise HTTPException(status_code=404, detail="Camera not found")
        
        return {
            "success": True,
            "data": {
                "id": row[0],
                "name": row[1],
                "description": row[2],
                "ip_address": str(row[3]) if row[3] else None,
                "rtsp_url": row[4],
                "status": row[5],
                "created_at": row[6].isoformat() if row[6] else None
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting camera {camera_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to get camera")

@app.post("/api/v1/cameras")
@limiter.limit(get_current_rate_limit())
async def create_camera(request: Request, camera_data: dict, current_user: dict = Depends(get_current_user)):
    """Create a new camera"""
    try:
        # Validate input data
        if not camera_data:
            raise HTTPException(status_code=400, detail="Camera data is required")
        
        # Validate required fields
        name = camera_data.get("name")
        if not name or not name.strip():
            raise HTTPException(status_code=400, detail="Camera name is required")
        if not is_safe_string(name):
            raise HTTPException(status_code=400, detail="Camera name contains unsafe characters")
        
        # Validate description if provided
        description = camera_data.get("description")
        if description and not is_safe_string(description):
            raise HTTPException(status_code=400, detail="Camera description contains unsafe characters")
        
        # Handle ip_address - extract from rtsp_url if not provided
        ip_address = camera_data.get("ip_address")
        rtsp_url = camera_data.get("rtsp_url")
        
        if not ip_address and rtsp_url:
            # Extract IP from rtsp_url (e.g., rtsp://192.168.1.100:554/stream -> 192.168.1.100)
            import re
            ip_match = re.search(r'rtsp://([^:/]+)', rtsp_url)
            if ip_match:
                ip_address = ip_match.group(1)
            else:
                ip_address = "127.0.0.1"  # Default fallback
        elif not ip_address:
            ip_address = "127.0.0.1"  # Default fallback
        
        # Validate IP address
        if not is_valid_ip(ip_address):
            raise HTTPException(status_code=400, detail="Invalid IP address format")
        
        # Validate RTSP URL if provided
        if rtsp_url and not is_safe_rtsp_url(rtsp_url):
            raise HTTPException(status_code=400, detail="Invalid RTSP URL format or contains unsafe characters")
        
        status = camera_data.get("status", "offline")
        if status not in ["active", "offline", "maintenance", "error"]:
            raise HTTPException(status_code=400, detail="Invalid status value")
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO cameras (name, description, ip_address, rtsp_url, status)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id, name, description, ip_address, rtsp_url, status, created_at
        """, (
            name,
            camera_data.get("description"),
            ip_address,
            rtsp_url,
            status
        ))
        
        row = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        
        return {
            "success": True,
            "data": {
                "id": row[0],
                "name": row[1],
                "description": row[2],
                "ip_address": str(row[3]) if row[3] else None,
                "rtsp_url": row[4],
                "status": row[5],
                "created_at": row[6].isoformat() if row[6] else None
            },
            "message": "Camera created successfully"
        }
    except HTTPException:
        raise
    except psycopg2.IntegrityError as e:
        logger.error(f"Database integrity error creating camera: {e}")
        conn.rollback()
        cursor.close()
        conn.close()
        if "duplicate key" in str(e).lower():
            raise HTTPException(status_code=409, detail="Camera with this name already exists")
        else:
            raise HTTPException(status_code=400, detail="Invalid data provided")
    except psycopg2.Error as e:
        logger.error(f"Database error creating camera: {e}")
        conn.rollback()
        cursor.close()
        conn.close()
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        logger.error(f"Error creating camera: {e}")
        if 'conn' in locals() and conn:
            conn.rollback()
            cursor.close()
            conn.close()
        raise HTTPException(status_code=500, detail="Failed to create camera")

@app.put("/api/v1/cameras/{camera_id}")
@limiter.limit(get_current_rate_limit())
async def update_camera(request: Request, camera_id: int, camera_data: dict, current_user: dict = Depends(get_current_user)):
    """Update camera"""
    try:
        # Validate input data
        if not camera_data:
            raise HTTPException(status_code=400, detail="Camera data is required")
        
        # Validate required fields
        name = camera_data.get("name")
        if name and not is_safe_string(name):
            raise HTTPException(status_code=400, detail="Camera name contains unsafe characters")
        
        # Validate description if provided
        description = camera_data.get("description")
        if description and not is_safe_string(description):
            raise HTTPException(status_code=400, detail="Camera description contains unsafe characters")
        
        # Validate status if provided
        status = camera_data.get("status")
        if status and status not in ["active", "offline", "maintenance", "error"]:
            raise HTTPException(status_code=400, detail="Invalid status value")
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if camera exists
        cursor.execute("SELECT id FROM cameras WHERE id = %s", (camera_id,))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            raise HTTPException(status_code=404, detail="Camera not found")
        
        # Build update query dynamically based on provided fields
        update_fields = []
        update_values = []
        
        if "name" in camera_data:
            update_fields.append("name = %s")
            update_values.append(camera_data["name"])
        
        if "description" in camera_data:
            update_fields.append("description = %s")
            update_values.append(camera_data["description"])
        
        if "ip_address" in camera_data:
            update_fields.append("ip_address = %s")
            update_values.append(camera_data["ip_address"])
        
        if "rtsp_url" in camera_data:
            update_fields.append("rtsp_url = %s")
            update_values.append(camera_data["rtsp_url"])
        
        if "status" in camera_data:
            update_fields.append("status = %s")
            update_values.append(camera_data["status"])
        
        if not update_fields:
            raise HTTPException(status_code=400, detail="No valid fields to update")
        
        # Add camera_id to values
        update_values.append(camera_id)
        
        query = f"""
            UPDATE cameras 
            SET {', '.join(update_fields)}
            WHERE id = %s
            RETURNING id, name, description, ip_address, rtsp_url, status, created_at
        """
        
        cursor.execute(query, update_values)
        row = cursor.fetchone()
        
        if not row:
            cursor.close()
            conn.close()
            raise HTTPException(status_code=500, detail="Failed to update camera")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return {
            "success": True,
            "data": {
                "id": row[0],
                "name": row[1],
                "description": row[2],
                "ip_address": str(row[3]) if row[3] else None,
                "rtsp_url": row[4],
                "status": row[5],
                "created_at": row[6].isoformat() if row[6] else None
            },
            "message": "Camera updated successfully"
        }
    except HTTPException:
        raise
    except psycopg2.Error as e:
        logger.error(f"Database error updating camera {camera_id}: {e}")
        conn.rollback()
        cursor.close()
        conn.close()
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        logger.error(f"Error updating camera {camera_id}: {e}")
        if 'conn' in locals() and conn:
            conn.rollback()
            cursor.close()
            conn.close()
        raise HTTPException(status_code=500, detail="Failed to update camera")

@app.delete("/api/v1/cameras/{camera_id}")
@limiter.limit(get_current_rate_limit())
async def delete_camera(request: Request, camera_id: int, current_user: dict = Depends(get_current_user)):
    """Delete camera"""
    try:
        # Validate camera_id
        camera_id = validate_camera_id(camera_id)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if camera exists
        cursor.execute("SELECT id FROM cameras WHERE id = %s", (camera_id,))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            raise HTTPException(status_code=404, detail="Camera not found")
        
        # Delete camera
        cursor.execute("DELETE FROM cameras WHERE id = %s", (camera_id,))
        conn.commit()
        cursor.close()
        conn.close()
        
        return {
            "success": True,
            "message": "Camera deleted successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting camera {camera_id}: {e}")
        if 'conn' in locals() and conn:
            conn.rollback()
            cursor.close()
            conn.close()
        raise HTTPException(status_code=500, detail="Failed to delete camera")

@app.patch("/api/v1/cameras/{camera_id}/status")
@limiter.limit(get_current_rate_limit())
async def update_camera_status(request: Request, camera_id: int, status_data: dict, current_user: dict = Depends(get_current_user)):
    """Update camera status"""
    try:
        # Validate camera_id
        camera_id = validate_camera_id(camera_id)
        
        # Validate status
        status = status_data.get("status")
        if not status or status not in ["active", "offline", "maintenance", "error"]:
            raise HTTPException(status_code=400, detail="Invalid status value")
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if camera exists
        cursor.execute("SELECT id FROM cameras WHERE id = %s", (camera_id,))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            raise HTTPException(status_code=404, detail="Camera not found")
        
        # Update status
        cursor.execute("""
            UPDATE cameras 
            SET status = %s 
            WHERE id = %s
            RETURNING id, name, status
        """, (status, camera_id))
        
        row = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        
        return {
            "success": True,
            "data": {
                "id": row[0],
                "name": row[1],
                "status": row[2]
            },
            "message": "Camera status updated successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating camera status {camera_id}: {e}")
        if 'conn' in locals() and conn:
            conn.rollback()
            cursor.close()
            conn.close()
        raise HTTPException(status_code=500, detail="Failed to update camera status")

# Count data endpoints
@app.get("/api/v1/counts")
@limiter.limit(get_current_rate_limit())
async def get_count_data(request: Request, camera_id: int = None, limit: int = 100):
    """Get count data"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if camera_id:
            cursor.execute("""
                SELECT id, camera_id, count_in, count_out, total_count, confidence, timestamp
                FROM counting_results 
                WHERE camera_id = %s
                ORDER BY timestamp DESC 
                LIMIT %s
            """, (camera_id, limit))
        else:
            cursor.execute("""
                SELECT id, camera_id, count_in, count_out, total_count, confidence, timestamp
                FROM counting_results 
                ORDER BY timestamp DESC 
                LIMIT %s
            """, (limit,))
        
        counts = []
        for row in cursor.fetchall():
            counts.append({
                "id": row[0],
                "camera_id": row[1],
                "count_in": row[2],
                "count_out": row[3],
                "total_count": row[4],
                "confidence": row[5],
                "timestamp": row[6].isoformat() if row[6] else None
            })
        
        cursor.close()
        conn.close()
        
        return {
            "success": True,
            "data": counts,
            "count": len(counts)
        }
    except Exception as e:
        logger.error(f"Error getting count data: {e}")
        raise HTTPException(status_code=500, detail="Failed to get count data")

# Analytics endpoints
@app.get("/api/v1/analytics/summary")
@limiter.limit(get_current_rate_limit())
async def get_analytics_summary(request: Request):
    """Get analytics summary"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get total cameras
        cursor.execute("SELECT COUNT(*) FROM cameras")
        total_cameras = cursor.fetchone()[0]
        
        # Get active cameras
        cursor.execute("SELECT COUNT(*) FROM cameras WHERE status = 'active'")
        active_cameras = cursor.fetchone()[0]
        
        # Get total counts today
        cursor.execute("""
            SELECT COALESCE(SUM(count_in), 0) as total_in, 
                   COALESCE(SUM(count_out), 0) as total_out
            FROM counting_results 
            WHERE DATE(timestamp) = CURRENT_DATE
        """)
        today_counts = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return {
            "success": True,
            "data": {
                "total_cameras": total_cameras,
                "active_cameras": active_cameras,
                "today_in": today_counts[0],
                "today_out": today_counts[1],
                "current_count": today_counts[0] - today_counts[1]
            }
        }
    except Exception as e:
        logger.error(f"Error getting analytics summary: {e}")
        raise HTTPException(status_code=500, detail="Failed to get analytics summary")

# Worker Pool Management Endpoints
@app.post("/api/v1/cameras/{camera_id}/start")
@limiter.limit(get_current_rate_limit())
async def start_camera_processing(request: Request, camera_id: int, current_user: dict = Depends(get_current_user)):
    """Start camera processing with worker pool"""
    try:
        # Validate camera_id
        camera_id = validate_camera_id(camera_id)
        
        # Get camera details
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, name, rtsp_url, status 
            FROM cameras 
            WHERE id = %s
        """, (camera_id,))
        
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if not row:
            raise HTTPException(status_code=404, detail="Camera not found")
        
        camera_id, name, rtsp_url, status = row
        
        if status != "active":
            raise HTTPException(status_code=400, detail="Camera must be active to start processing")
        
        # Add to worker pool
        success = worker_pool.add_camera_task(camera_id, rtsp_url)
        if not success:
            raise HTTPException(status_code=400, detail="Camera is already being processed")
        
        return {
            "success": True,
            "message": f"Camera {name} processing started",
            "data": {
                "camera_id": camera_id,
                "status": "processing_started"
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error starting camera processing {camera_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to start camera processing")

@app.post("/api/v1/cameras/{camera_id}/stop")
@limiter.limit(get_current_rate_limit())
async def stop_camera_processing(request: Request, camera_id: int, current_user: dict = Depends(get_current_user)):
    """Stop camera processing"""
    try:
        # Validate camera_id
        camera_id = validate_camera_id(camera_id)
        
        # Stop processing
        success = worker_pool.remove_camera_task(camera_id)
        if not success:
            raise HTTPException(status_code=400, detail="Camera is not being processed")
        
        return {
            "success": True,
            "message": f"Camera {camera_id} processing stopped",
            "data": {
                "camera_id": camera_id,
                "status": "processing_stopped"
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error stopping camera processing {camera_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to stop camera processing")

@app.get("/api/v1/cameras/{camera_id}/status")
@limiter.limit(get_current_rate_limit())
async def get_camera_processing_status(request: Request, camera_id: int, current_user: dict = Depends(get_current_user)):
    """Get camera processing status"""
    try:
        # Validate camera_id
        camera_id = validate_camera_id(camera_id)
        
        # Get status from worker pool
        status = worker_pool.get_camera_status(camera_id)
        
        return {
            "success": True,
            "data": {
                "camera_id": camera_id,
                "status": status
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting camera status {camera_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to get camera status")

@app.get("/api/v1/workers/status")
@limiter.limit(get_current_rate_limit())
async def get_worker_pool_status(request: Request, current_user: dict = Depends(get_current_user)):
    """Get worker pool status"""
    try:
        status = worker_pool.get_status()
        
        return {
            "success": True,
            "data": status
        }
        
    except Exception as e:
        logger.error(f"Error getting worker pool status: {e}")
        raise HTTPException(status_code=500, detail="Failed to get worker pool status")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 3002))
    uvicorn.run(app, host="0.0.0.0", port=port, reload=True) 