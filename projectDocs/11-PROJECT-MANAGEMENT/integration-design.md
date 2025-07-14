# Integration Design - AI Camera Counting System

## 📋 Table of Contents
1. [System Architecture Overview](#system-architecture-overview)
2. [Service Integration Patterns](#service-integration-patterns)
3. [Data Flow Design](#data-flow-design)
4. [API Integration](#api-integration)
5. [Error Handling](#error-handling)
6. [Security Integration](#security-integration)
7. [Performance Optimization](#performance-optimization)
8. [Monitoring & Observability](#monitoring--observability)

## 🏗️ System Architecture Overview

### High-Level Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   beAuth        │    │   beCamera      │
│   (React)       │◄──►│   Service       │◄──►│   Service       │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Nginx         │    │   PostgreSQL    │    │   Redis         │
│   (Reverse      │    │   Database      │    │   (Cache &      │
│    Proxy)       │    │                 │    │    Sessions)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Service Communication Flow
```
Frontend → Nginx → beAuth/beCamera → Database/Cache
    ↑         ↓         ↓              ↓
    └─────────┴─────────┴──────────────┘
              WebSocket
              Real-time Updates
```

## 🔗 Service Integration Patterns

### 1. Synchronous Communication

#### HTTP REST API Pattern
```javascript
// Frontend to Backend Communication
const apiClient = {
  // GET Request
  async getCameras() {
    const response = await fetch('/api/v1/cameras', {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });
    return response.json();
  },

  // POST Request
  async createCamera(cameraData) {
    const response = await fetch('/api/v1/cameras', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(cameraData)
    });
    return response.json();
  }
};
```

#### Service-to-Service Communication
```python
# beCamera to beAuth Communication
import httpx

class AuthService:
    def __init__(self):
        self.base_url = "http://beauth:3001"
        self.client = httpx.AsyncClient()
    
    async def validate_token(self, token: str) -> dict:
        """Validate JWT token with beAuth service"""
        try:
            response = await self.client.post(
                f"{self.base_url}/api/v1/auth/validate",
                json={"token": token}
            )
            return response.json()
        except Exception as e:
            logger.error(f"Token validation failed: {e}")
            raise AuthenticationError("Invalid token")
```

### 2. Asynchronous Communication

#### Event-Driven Pattern
```python
# Redis Pub/Sub for Event Communication
import redis.asyncio as redis
import json

class EventBus:
    def __init__(self):
        self.redis_client = redis.Redis(host='redis', port=6379, decode_responses=True)
        self.pubsub = self.redis_client.pubsub()
    
    async def publish_event(self, event_type: str, data: dict):
        """Publish event to Redis"""
        event = {
            "type": event_type,
            "data": data,
            "timestamp": datetime.utcnow().isoformat()
        }
        await self.redis_client.publish(event_type, json.dumps(event))
    
    async def subscribe_to_events(self, event_types: list, callback):
        """Subscribe to events"""
        await self.pubsub.subscribe(*event_types)
        async for message in self.pubsub.listen():
            if message['type'] == 'message':
                event_data = json.loads(message['data'])
                await callback(event_data)
```

#### Message Queue Pattern
```python
# Celery for Background Tasks
from celery import Celery

# Configure Celery
celery_app = Celery(
    'ai_camera_tasks',
    broker='redis://redis:6379/0',
    backend='redis://redis:6379/1'
)

@celery_app.task
def process_camera_image(camera_id: str, image_url: str):
    """Process camera image asynchronously"""
    try:
        # AI processing logic
        result = ai_model.process_image(image_url)
        
        # Update database
        update_count_in_database(camera_id, result['count'])
        
        # Publish event
        event_bus.publish_event('camera_processed', {
            'camera_id': camera_id,
            'count': result['count'],
            'timestamp': datetime.utcnow()
        })
        
        return result
    except Exception as e:
        logger.error(f"Image processing failed: {e}")
        raise
```

### 3. Real-time Communication

#### WebSocket Integration
```javascript
// Frontend WebSocket Client
class WebSocketClient {
  constructor() {
    this.ws = null;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
  }

  connect() {
    this.ws = new WebSocket('ws://localhost:3003/ws/camera-updates/client-1');
    
    this.ws.onopen = () => {
      console.log('WebSocket connected');
      this.reconnectAttempts = 0;
    };

    this.ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      this.handleMessage(data);
    };

    this.ws.onclose = () => {
      console.log('WebSocket disconnected');
      this.reconnect();
    };
  }

  handleMessage(data) {
    switch (data.type) {
      case 'camera_update':
        this.updateCameraCount(data.camera_id, data.data);
        break;
      case 'alert':
        this.showAlert(data.message, data.severity);
        break;
      case 'system_status':
        this.updateSystemStatus(data.data);
        break;
    }
  }

  reconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      setTimeout(() => this.connect(), 1000 * this.reconnectAttempts);
    }
  }
}
```

## 📊 Data Flow Design

### 1. Camera Data Flow
```
Camera Device → beCamera Service → Database → Frontend
     ↓              ↓                ↓         ↓
  Image Data    AI Processing    Count Data  Real-time UI
     ↓              ↓                ↓         ↓
  Validation    Result Storage   Analytics   WebSocket
```

### 2. Authentication Flow
```
Frontend → beAuth Service → Database → JWT Token
    ↓           ↓              ↓         ↓
Login Form   Validation    User Data   Session
    ↓           ↓              ↓         ↓
Token Store  Password Hash  Permissions  API Access
```

### 3. Analytics Data Flow
```
Database → Analytics Service → Cache → Frontend
    ↓            ↓              ↓        ↓
Raw Data    Aggregation    Results   Charts
    ↓            ↓              ↓        ↓
Scheduled   Calculations   Storage   Real-time
```

### 4. Alert Flow
```
System Event → Alert Service → Notification → User
     ↓             ↓              ↓          ↓
Detection      Rule Engine    Channels    Interface
     ↓             ↓              ↓          ↓
Monitoring    Severity       Email/SMS   Dashboard
```

## 🔌 API Integration

### 1. External Camera API Integration
```python
# Camera API Client
class CameraAPIClient:
    def __init__(self, base_url: str, username: str, password: str):
        self.base_url = base_url
        self.auth = (username, password)
        self.session = requests.Session()
    
    def get_snapshot(self) -> bytes:
        """Get current snapshot from camera"""
        try:
            response = self.session.get(
                f"{self.base_url}/snapshot",
                auth=self.auth,
                timeout=10
            )
            response.raise_for_status()
            return response.content
        except requests.RequestException as e:
            logger.error(f"Failed to get snapshot: {e}")
            raise CameraConnectionError(f"Camera API error: {e}")
    
    def get_status(self) -> dict:
        """Get camera status"""
        try:
            response = self.session.get(
                f"{self.base_url}/status",
                auth=self.auth,
                timeout=5
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Failed to get status: {e}")
            raise CameraConnectionError(f"Camera API error: {e}")
```

### 2. AI Model Integration
```python
# AI Model Service Integration
class AIModelService:
    def __init__(self):
        self.model = self.load_model()
        self.preprocessor = self.load_preprocessor()
    
    def load_model(self):
        """Load AI model"""
        try:
            # Load pre-trained model
            model = cv2.dnn.readNetFromCaffe(
                'models/MobileNetSSD_deploy.prototxt',
                'models/MobileNetSSD_deploy.caffemodel'
            )
            return model
        except Exception as e:
            logger.error(f"Failed to load AI model: {e}")
            raise ModelLoadError(f"Model loading failed: {e}")
    
    async def process_image(self, image_data: bytes) -> dict:
        """Process image and return people count"""
        try:
            # Preprocess image
            processed_image = self.preprocess_image(image_data)
            
            # Run inference
            detections = self.model.forward(processed_image)
            
            # Post-process results
            people_count = self.count_people(detections)
            
            return {
                'count': people_count,
                'confidence': self.calculate_confidence(detections),
                'processing_time': self.get_processing_time()
            }
        except Exception as e:
            logger.error(f"Image processing failed: {e}")
            raise ProcessingError(f"AI processing failed: {e}")
```

### 3. Third-Party Service Integration
```python
# Email Service Integration
class EmailService:
    def __init__(self):
        self.smtp_host = os.getenv('SMTP_HOST')
        self.smtp_port = int(os.getenv('SMTP_PORT'))
        self.smtp_user = os.getenv('SMTP_USER')
        self.smtp_password = os.getenv('SMTP_PASSWORD')
    
    async def send_alert_email(self, to_email: str, subject: str, message: str):
        """Send alert email"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.smtp_user
            msg['To'] = to_email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(message, 'plain'))
            
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
                
            logger.info(f"Alert email sent to {to_email}")
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            raise EmailSendError(f"Email sending failed: {e}")
```

## ⚠️ Error Handling

### 1. Service-Level Error Handling
```python
# Centralized Error Handler
class ErrorHandler:
    @staticmethod
    async def handle_service_error(error: Exception, context: str) -> dict:
        """Handle service-level errors"""
        error_id = str(uuid.uuid4())
        
        # Log error
        logger.error(f"Error {error_id} in {context}: {str(error)}")
        
        # Determine error type
        if isinstance(error, AuthenticationError):
            return {
                'error_id': error_id,
                'type': 'authentication_error',
                'message': 'Authentication failed',
                'status_code': 401
            }
        elif isinstance(error, ValidationError):
            return {
                'error_id': error_id,
                'type': 'validation_error',
                'message': str(error),
                'status_code': 400
            }
        elif isinstance(error, DatabaseError):
            return {
                'error_id': error_id,
                'type': 'database_error',
                'message': 'Database operation failed',
                'status_code': 500
            }
        else:
            return {
                'error_id': error_id,
                'type': 'internal_error',
                'message': 'Internal server error',
                'status_code': 500
            }
```

### 2. Circuit Breaker Pattern
```python
# Circuit Breaker Implementation
class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = 'CLOSED'  # CLOSED, OPEN, HALF_OPEN
    
    async def call(self, func, *args, **kwargs):
        """Execute function with circuit breaker"""
        if self.state == 'OPEN':
            if time.time() - self.last_failure_time > self.timeout:
                self.state = 'HALF_OPEN'
            else:
                raise CircuitBreakerOpenError("Circuit breaker is open")
        
        try:
            result = await func(*args, **kwargs)
            self.on_success()
            return result
        except Exception as e:
            self.on_failure()
            raise e
    
    def on_success(self):
        """Handle successful call"""
        self.failure_count = 0
        self.state = 'CLOSED'
    
    def on_failure(self):
        """Handle failed call"""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.failure_count >= self.failure_threshold:
            self.state = 'OPEN'
```

### 3. Retry Pattern
```python
# Retry Mechanism
class RetryHandler:
    def __init__(self, max_retries: int = 3, backoff_factor: float = 2.0):
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
    
    async def execute_with_retry(self, func, *args, **kwargs):
        """Execute function with retry logic"""
        last_exception = None
        
        for attempt in range(self.max_retries + 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                
                if attempt < self.max_retries:
                    wait_time = self.backoff_factor ** attempt
                    logger.warning(f"Attempt {attempt + 1} failed, retrying in {wait_time}s: {e}")
                    await asyncio.sleep(wait_time)
                else:
                    logger.error(f"All {self.max_retries + 1} attempts failed: {e}")
                    raise last_exception
```

## 🔒 Security Integration

### 1. Authentication Integration
```python
# JWT Authentication Middleware
class JWTAuthMiddleware:
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
    
    async def authenticate(self, request: Request) -> dict:
        """Authenticate JWT token"""
        auth_header = request.headers.get('Authorization')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            raise AuthenticationError("Missing or invalid authorization header")
        
        token = auth_header.split(' ')[1]
        
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            raise AuthenticationError("Token has expired")
        except jwt.InvalidTokenError:
            raise AuthenticationError("Invalid token")
```

### 2. Rate Limiting
```python
# Rate Limiting Middleware
class RateLimitMiddleware:
    def __init__(self, redis_client: redis.Redis):
        self.redis_client = redis_client
    
    async def check_rate_limit(self, key: str, limit: int, window: int) -> bool:
        """Check if request is within rate limit"""
        current = await self.redis_client.get(key)
        
        if current is None:
            await self.redis_client.setex(key, window, 1)
            return True
        
        current_count = int(current)
        if current_count >= limit:
            return False
        
        await self.redis_client.incr(key)
        return True
```

### 3. Input Validation
```python
# Input Validation Service
class ValidationService:
    @staticmethod
    def validate_camera_data(data: dict) -> dict:
        """Validate camera creation/update data"""
        schema = {
            'name': {'type': 'string', 'required': True, 'minlength': 1, 'maxlength': 100},
            'location': {'type': 'string', 'required': True, 'minlength': 1, 'maxlength': 200},
            'ip_address': {'type': 'string', 'required': True, 'regex': r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'},
            'port': {'type': 'integer', 'required': True, 'min': 1, 'max': 65535},
            'username': {'type': 'string', 'required': True, 'minlength': 1, 'maxlength': 50},
            'password': {'type': 'string', 'required': True, 'minlength': 6, 'maxlength': 100}
        }
        
        return validate(data, schema)
```

## ⚡ Performance Optimization

### 1. Caching Strategy
```python
# Multi-Level Caching
class CacheManager:
    def __init__(self):
        self.redis_client = redis.Redis(host='redis', port=6379)
        self.local_cache = {}
    
    async def get_cached_data(self, key: str, ttl: int = 300):
        """Get data from cache with fallback"""
        # Try local cache first
        if key in self.local_cache:
            return self.local_cache[key]
        
        # Try Redis cache
        cached_data = await self.redis_client.get(key)
        if cached_data:
            data = json.loads(cached_data)
            self.local_cache[key] = data
            return data
        
        return None
    
    async def set_cached_data(self, key: str, data: dict, ttl: int = 300):
        """Set data in cache"""
        # Set in Redis
        await self.redis_client.setex(key, ttl, json.dumps(data))
        
        # Set in local cache
        self.local_cache[key] = data
```

### 2. Database Connection Pooling
```python
# Database Connection Pool
class DatabasePool:
    def __init__(self):
        self.pool = None
    
    async def initialize_pool(self):
        """Initialize connection pool"""
        self.pool = await asyncpg.create_pool(
            host=os.getenv('DB_HOST'),
            port=int(os.getenv('DB_PORT')),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME'),
            min_size=5,
            max_size=20
        )
    
    async def get_connection(self):
        """Get connection from pool"""
        return await self.pool.acquire()
    
    async def release_connection(self, connection):
        """Release connection back to pool"""
        await self.pool.release(connection)
```

### 3. Async Processing
```python
# Async Task Queue
class AsyncTaskQueue:
    def __init__(self):
        self.queue = asyncio.Queue()
        self.workers = []
    
    async def start_workers(self, num_workers: int = 4):
        """Start worker processes"""
        for _ in range(num_workers):
            worker = asyncio.create_task(self.worker())
            self.workers.append(worker)
    
    async def worker(self):
        """Worker process"""
        while True:
            try:
                task = await self.queue.get()
                await self.process_task(task)
                self.queue.task_done()
            except Exception as e:
                logger.error(f"Worker error: {e}")
    
    async def add_task(self, task):
        """Add task to queue"""
        await self.queue.put(task)
```

## 📊 Monitoring & Observability

### 1. Metrics Collection
```python
# Prometheus Metrics
from prometheus_client import Counter, Histogram, Gauge

# Define metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
REQUEST_DURATION = Histogram('http_request_duration_seconds', 'HTTP request duration')
ACTIVE_CONNECTIONS = Gauge('websocket_connections_active', 'Active WebSocket connections')
CAMERA_PROCESSING_TIME = Histogram('camera_processing_duration_seconds', 'Camera processing duration')

# Metrics middleware
class MetricsMiddleware:
    async def collect_metrics(self, request: Request, response: Response, duration: float):
        """Collect request metrics"""
        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=request.url.path,
            status=response.status_code
        ).inc()
        
        REQUEST_DURATION.observe(duration)
```

### 2. Distributed Tracing
```python
# OpenTelemetry Integration
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode

class TracingService:
    def __init__(self):
        self.tracer = trace.get_tracer(__name__)
    
    async def trace_operation(self, operation_name: str, func, *args, **kwargs):
        """Trace operation execution"""
        with self.tracer.start_as_current_span(operation_name) as span:
            try:
                result = await func(*args, **kwargs)
                span.set_status(Status(StatusCode.OK))
                return result
            except Exception as e:
                span.set_status(Status(StatusCode.ERROR, str(e)))
                span.record_exception(e)
                raise
```

### 3. Health Checks
```python
# Health Check Service
class HealthCheckService:
    def __init__(self):
        self.checks = {
            'database': self.check_database,
            'redis': self.check_redis,
            'ai_model': self.check_ai_model
        }
    
    async def perform_health_check(self) -> dict:
        """Perform comprehensive health check"""
        results = {}
        
        for check_name, check_func in self.checks.items():
            try:
                await check_func()
                results[check_name] = {'status': 'healthy'}
            except Exception as e:
                results[check_name] = {
                    'status': 'unhealthy',
                    'error': str(e)
                }
        
        return results
    
    async def check_database(self):
        """Check database connectivity"""
        # Implementation
        pass
    
    async def check_redis(self):
        """Check Redis connectivity"""
        # Implementation
        pass
    
    async def check_ai_model(self):
        """Check AI model availability"""
        # Implementation
        pass
```

## 🎯 Integration Testing

### 1. Service Integration Tests
```python
# Integration Test Suite
class TestServiceIntegration:
    @pytest.fixture
    async def setup_services(self):
        """Setup test services"""
        # Start test services
        # Setup test data
        yield
        # Cleanup
    
    async def test_camera_processing_flow(self, setup_services):
        """Test complete camera processing flow"""
        # Test camera creation
        camera = await create_test_camera()
        
        # Test image processing
        result = await process_test_image(camera.id)
        
        # Test database update
        count = await get_camera_count(camera.id)
        
        # Verify results
        assert result['count'] == count
        assert result['status'] == 'success'
    
    async def test_authentication_flow(self, setup_services):
        """Test authentication flow"""
        # Test user registration
        user = await register_test_user()
        
        # Test login
        token = await login_user(user.email, user.password)
        
        # Test token validation
        is_valid = await validate_token(token)
        
        # Verify results
        assert is_valid == True
```

### 2. API Contract Testing
```python
# API Contract Tests
class TestAPIContracts:
    def test_camera_api_contract(self):
        """Test camera API contract"""
        # Test request schema
        request_data = {
            'name': 'Test Camera',
            'location': 'Test Location',
            'ip_address': '192.168.1.100',
            'port': 8080,
            'username': 'admin',
            'password': 'password123'
        }
        
        # Validate request schema
        validate_camera_request(request_data)
        
        # Test response schema
        response_data = {
            'id': 'camera-123',
            'name': 'Test Camera',
            'status': 'active',
            'created_at': '2024-01-01T00:00:00Z'
        }
        
        # Validate response schema
        validate_camera_response(response_data)
```

---

**Last Updated**: December 2024  
**Version**: 1.0.0  
**Status**: Ready for Implementation 