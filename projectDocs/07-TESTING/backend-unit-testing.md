# Backend Unit Testing Guide
## AI Camera Counting System

### 📊 Tổng quan

Tài liệu này hướng dẫn unit testing cho backend services (Node.js và Python) trong hệ thống AI Camera Counting, sử dụng Jest cho Node.js và pytest cho Python.

### 🎯 Mục tiêu
- Đảm bảo code quality và reliability
- Tăng tốc độ development và debugging
- Giảm thiểu regression bugs
- Cải thiện code maintainability

### 🛠️ Node.js Testing Setup

#### Jest Configuration for Node.js
```javascript
// beAuth/jest.config.js
module.exports = {
  testEnvironment: 'node',
  roots: ['<rootDir>/src'],
  testMatch: [
    '**/__tests__/**/*.js',
    '**/?(*.)+(spec|test).js'
  ],
  collectCoverageFrom: [
    'src/**/*.js',
    '!src/**/*.test.js',
    '!src/index.js'
  ],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80
    }
  },
  setupFilesAfterEnv: ['<rootDir>/src/test/setup.js'],
  testTimeout: 10000
};
```

#### Test Setup
```javascript
// beAuth/src/test/setup.js
const mongoose = require('mongoose');
const { MongoMemoryServer } = require('mongodb-memory-server');

let mongoServer;

beforeAll(async () => {
  mongoServer = await MongoMemoryServer.create();
  const mongoUri = mongoServer.getUri();
  await mongoose.connect(mongoUri);
});

afterAll(async () => {
  await mongoose.disconnect();
  await mongoServer.stop();
});

afterEach(async () => {
  const collections = mongoose.connection.collections;
  for (const key in collections) {
    await collections[key].deleteMany();
  }
});
```

### 🧪 Authentication Service Testing

#### User Model Testing
```javascript
// beAuth/src/models/__tests__/User.test.js
const mongoose = require('mongoose');
const User = require('../User');
const bcrypt = require('bcryptjs');

describe('User Model', () => {
  test('should create user with valid data', async () => {
    const userData = {
      email: 'test@example.com',
      password: 'password123',
      firstName: 'John',
      lastName: 'Doe',
      role: 'user'
    };

    const user = new User(userData);
    await user.save();

    expect(user.email).toBe(userData.email);
    expect(user.firstName).toBe(userData.firstName);
    expect(user.lastName).toBe(userData.lastName);
    expect(user.role).toBe(userData.role);
    expect(user.password).not.toBe(userData.password); // Should be hashed
  });

  test('should hash password before saving', async () => {
    const userData = {
      email: 'test@example.com',
      password: 'password123',
      firstName: 'John',
      lastName: 'Doe'
    };

    const user = new User(userData);
    await user.save();

    const isPasswordValid = await bcrypt.compare('password123', user.password);
    expect(isPasswordValid).toBe(true);
  });

  test('should validate email format', async () => {
    const userData = {
      email: 'invalid-email',
      password: 'password123',
      firstName: 'John',
      lastName: 'Doe'
    };

    const user = new User(userData);
    let error;

    try {
      await user.save();
    } catch (err) {
      error = err;
    }

    expect(error).toBeDefined();
    expect(error.errors.email).toBeDefined();
  });

  test('should require email and password', async () => {
    const user = new User({});
    let error;

    try {
      await user.save();
    } catch (err) {
      error = err;
    }

    expect(error).toBeDefined();
    expect(error.errors.email).toBeDefined();
    expect(error.errors.password).toBeDefined();
  });

  test('should not allow duplicate emails', async () => {
    const userData = {
      email: 'test@example.com',
      password: 'password123',
      firstName: 'John',
      lastName: 'Doe'
    };

    await new User(userData).save();

    const duplicateUser = new User(userData);
    let error;

    try {
      await duplicateUser.save();
    } catch (err) {
      error = err;
    }

    expect(error).toBeDefined();
    expect(error.code).toBe(11000); // MongoDB duplicate key error
  });
});
```

#### Authentication Service Testing
```javascript
// beAuth/src/services/__tests__/authService.test.js
const authService = require('../authService');
const User = require('../../models/User');
const jwt = require('jsonwebtoken');
const bcrypt = require('bcryptjs');

// Mock JWT
jest.mock('jsonwebtoken');
jest.mock('bcryptjs');

describe('AuthService', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('register', () => {
    test('should register user successfully', async () => {
      const userData = {
        email: 'test@example.com',
        password: 'password123',
        firstName: 'John',
        lastName: 'Doe'
      };

      bcrypt.hash.mockResolvedValue('hashedPassword');
      jwt.sign.mockReturnValue('mockToken');

      const result = await authService.register(userData);

      expect(result.success).toBe(true);
      expect(result.user.email).toBe(userData.email);
      expect(result.token).toBe('mockToken');
      expect(bcrypt.hash).toHaveBeenCalledWith(userData.password, 10);
    });

    test('should handle duplicate email error', async () => {
      const userData = {
        email: 'existing@example.com',
        password: 'password123',
        firstName: 'John',
        lastName: 'Doe'
      };

      // Mock User.findOne to return existing user
      User.findOne = jest.fn().mockResolvedValue({ email: 'existing@example.com' });

      const result = await authService.register(userData);

      expect(result.success).toBe(false);
      expect(result.error).toBe('Email already exists');
    });

    test('should handle validation errors', async () => {
      const userData = {
        email: 'invalid-email',
        password: '123', // Too short
        firstName: 'John',
        lastName: 'Doe'
      };

      const result = await authService.register(userData);

      expect(result.success).toBe(false);
      expect(result.error).toContain('validation failed');
    });
  });

  describe('login', () => {
    test('should login user successfully', async () => {
      const loginData = {
        email: 'test@example.com',
        password: 'password123'
      };

      const mockUser = {
        _id: 'userId123',
        email: 'test@example.com',
        password: 'hashedPassword',
        firstName: 'John',
        lastName: 'Doe',
        role: 'user'
      };

      User.findOne = jest.fn().mockResolvedValue(mockUser);
      bcrypt.compare.mockResolvedValue(true);
      jwt.sign.mockReturnValue('mockToken');

      const result = await authService.login(loginData);

      expect(result.success).toBe(true);
      expect(result.user.email).toBe(loginData.email);
      expect(result.token).toBe('mockToken');
      expect(bcrypt.compare).toHaveBeenCalledWith(loginData.password, 'hashedPassword');
    });

    test('should handle invalid credentials', async () => {
      const loginData = {
        email: 'test@example.com',
        password: 'wrongpassword'
      };

      const mockUser = {
        email: 'test@example.com',
        password: 'hashedPassword'
      };

      User.findOne = jest.fn().mockResolvedValue(mockUser);
      bcrypt.compare.mockResolvedValue(false);

      const result = await authService.login(loginData);

      expect(result.success).toBe(false);
      expect(result.error).toBe('Invalid credentials');
    });

    test('should handle user not found', async () => {
      const loginData = {
        email: 'nonexistent@example.com',
        password: 'password123'
      };

      User.findOne = jest.fn().mockResolvedValue(null);

      const result = await authService.login(loginData);

      expect(result.success).toBe(false);
      expect(result.error).toBe('User not found');
    });
  });

  describe('verifyToken', () => {
    test('should verify valid token', async () => {
      const mockPayload = {
        userId: 'userId123',
        email: 'test@example.com'
      };

      jwt.verify.mockReturnValue(mockPayload);

      const result = await authService.verifyToken('validToken');

      expect(result.success).toBe(true);
      expect(result.userId).toBe('userId123');
      expect(jwt.verify).toHaveBeenCalledWith('validToken', process.env.JWT_SECRET);
    });

    test('should handle invalid token', async () => {
      jwt.verify.mockImplementation(() => {
        throw new Error('Invalid token');
      });

      const result = await authService.verifyToken('invalidToken');

      expect(result.success).toBe(false);
      expect(result.error).toBe('Invalid token');
    });
  });
});
```

#### Route Testing
```javascript
// beAuth/src/routes/__tests__/auth.test.js
const request = require('supertest');
const app = require('../../app');
const User = require('../../models/User');
const jwt = require('jsonwebtoken');

describe('Auth Routes', () => {
  beforeEach(async () => {
    await User.deleteMany({});
  });

  describe('POST /api/auth/register', () => {
    test('should register new user', async () => {
      const userData = {
        email: 'test@example.com',
        password: 'password123',
        firstName: 'John',
        lastName: 'Doe'
      };

      const response = await request(app)
        .post('/api/auth/register')
        .send(userData)
        .expect(201);

      expect(response.body.success).toBe(true);
      expect(response.body.user.email).toBe(userData.email);
      expect(response.body.token).toBeDefined();
    });

    test('should return 400 for invalid data', async () => {
      const invalidData = {
        email: 'invalid-email',
        password: '123'
      };

      const response = await request(app)
        .post('/api/auth/register')
        .send(invalidData)
        .expect(400);

      expect(response.body.success).toBe(false);
      expect(response.body.error).toBeDefined();
    });

    test('should return 409 for duplicate email', async () => {
      const userData = {
        email: 'test@example.com',
        password: 'password123',
        firstName: 'John',
        lastName: 'Doe'
      };

      // Create first user
      await request(app)
        .post('/api/auth/register')
        .send(userData);

      // Try to create duplicate
      const response = await request(app)
        .post('/api/auth/register')
        .send(userData)
        .expect(409);

      expect(response.body.success).toBe(false);
      expect(response.body.error).toContain('already exists');
    });
  });

  describe('POST /api/auth/login', () => {
    beforeEach(async () => {
      // Create a test user
      const userData = {
        email: 'test@example.com',
        password: 'password123',
        firstName: 'John',
        lastName: 'Doe'
      };

      await request(app)
        .post('/api/auth/register')
        .send(userData);
    });

    test('should login with valid credentials', async () => {
      const loginData = {
        email: 'test@example.com',
        password: 'password123'
      };

      const response = await request(app)
        .post('/api/auth/login')
        .send(loginData)
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(response.body.user.email).toBe(loginData.email);
      expect(response.body.token).toBeDefined();
    });

    test('should return 401 for invalid credentials', async () => {
      const loginData = {
        email: 'test@example.com',
        password: 'wrongpassword'
      };

      const response = await request(app)
        .post('/api/auth/login')
        .send(loginData)
        .expect(401);

      expect(response.body.success).toBe(false);
      expect(response.body.error).toBe('Invalid credentials');
    });
  });

  describe('GET /api/auth/profile', () => {
    let authToken;

    beforeEach(async () => {
      // Create user and get token
      const userData = {
        email: 'test@example.com',
        password: 'password123',
        firstName: 'John',
        lastName: 'Doe'
      };

      const registerResponse = await request(app)
        .post('/api/auth/register')
        .send(userData);

      authToken = registerResponse.body.token;
    });

    test('should return user profile with valid token', async () => {
      const response = await request(app)
        .get('/api/auth/profile')
        .set('Authorization', `Bearer ${authToken}`)
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(response.body.user.email).toBe('test@example.com');
      expect(response.body.user.password).toBeUndefined(); // Should not return password
    });

    test('should return 401 without token', async () => {
      const response = await request(app)
        .get('/api/auth/profile')
        .expect(401);

      expect(response.body.success).toBe(false);
      expect(response.body.error).toBe('No token provided');
    });

    test('should return 401 with invalid token', async () => {
      const response = await request(app)
        .get('/api/auth/profile')
        .set('Authorization', 'Bearer invalidToken')
        .expect(401);

      expect(response.body.success).toBe(false);
      expect(response.body.error).toBe('Invalid token');
    });
  });
});
```

### 🐍 Python Testing Setup

#### pytest Configuration
```python
# beCamera/pytest.ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    --strict-markers
    --disable-warnings
    --cov=src
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=80
markers =
    unit: Unit tests
    integration: Integration tests
    e2e: End-to-end tests
    slow: Slow running tests
    camera: Camera-related tests
    ai: AI model tests
```

#### Test Configuration
```python
# beCamera/tests/conftest.py
import pytest
import asyncio
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.main import app
from src.database import get_db, Base
from src.models import Camera, CountData, User

# Create in-memory database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database session for each test"""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with database session"""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture
def sample_camera():
    """Sample camera data for testing"""
    return {
        "name": "Test Camera",
        "location": "Building A",
        "ip_address": "192.168.1.100",
        "status": "active"
    }

@pytest.fixture
def sample_count_data():
    """Sample count data for testing"""
    return {
        "camera_id": 1,
        "count": 25,
        "confidence": 0.95,
        "object_type": "person"
    }
```

### 🧪 FastAPI Service Testing

#### Model Testing
```python
# beCamera/tests/test_models.py
import pytest
from datetime import datetime
from src.models import Camera, CountData, User
from sqlalchemy.orm import Session

class TestCamera:
    def test_create_camera(self, db_session: Session):
        """Test camera creation with valid data"""
        camera_data = {
            "name": "Test Camera",
            "location": "Building A",
            "ip_address": "192.168.1.100",
            "status": "active"
        }
        
        camera = Camera(**camera_data)
        db_session.add(camera)
        db_session.commit()
        
        assert camera.id is not None
        assert camera.name == camera_data["name"]
        assert camera.location == camera_data["location"]
        assert camera.ip_address == camera_data["ip_address"]
        assert camera.status == camera_data["status"]
        assert camera.created_at is not None
    
    def test_camera_ip_validation(self, db_session: Session):
        """Test camera IP address validation"""
        camera_data = {
            "name": "Test Camera",
            "location": "Building A",
            "ip_address": "invalid-ip",
            "status": "active"
        }
        
        camera = Camera(**camera_data)
        
        with pytest.raises(ValueError):
            db_session.add(camera)
            db_session.commit()
    
    def test_camera_status_enum(self, db_session: Session):
        """Test camera status enum validation"""
        camera_data = {
            "name": "Test Camera",
            "location": "Building A",
            "ip_address": "192.168.1.100",
            "status": "invalid_status"
        }
        
        camera = Camera(**camera_data)
        
        with pytest.raises(ValueError):
            db_session.add(camera)
            db_session.commit()

class TestCountData:
    def test_create_count_data(self, db_session: Session):
        """Test count data creation"""
        count_data = {
            "camera_id": 1,
            "count": 25,
            "confidence": 0.95,
            "object_type": "person",
            "timestamp": datetime.now()
        }
        
        count_record = CountData(**count_data)
        db_session.add(count_record)
        db_session.commit()
        
        assert count_record.id is not None
        assert count_record.count == count_data["count"]
        assert count_record.confidence == count_data["confidence"]
        assert count_record.object_type == count_data["object_type"]
    
    def test_count_validation(self, db_session: Session):
        """Test count validation"""
        count_data = {
            "camera_id": 1,
            "count": -5,  # Invalid negative count
            "confidence": 0.95,
            "object_type": "person"
        }
        
        count_record = CountData(**count_data)
        
        with pytest.raises(ValueError):
            db_session.add(count_record)
            db_session.commit()
    
    def test_confidence_validation(self, db_session: Session):
        """Test confidence validation"""
        count_data = {
            "camera_id": 1,
            "count": 25,
            "confidence": 1.5,  # Invalid confidence > 1.0
            "object_type": "person"
        }
        
        count_record = CountData(**count_data)
        
        with pytest.raises(ValueError):
            db_session.add(count_record)
            db_session.commit()
```

#### API Endpoint Testing
```python
# beCamera/tests/test_api.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

class TestCameraAPI:
    def test_get_cameras(self, client: TestClient, db_session: Session):
        """Test getting all cameras"""
        # Create test camera
        camera_data = {
            "name": "Test Camera",
            "location": "Building A",
            "ip_address": "192.168.1.100",
            "status": "active"
        }
        
        response = client.post("/api/cameras/", json=camera_data)
        assert response.status_code == 201
        
        # Get all cameras
        response = client.get("/api/cameras/")
        assert response.status_code == 200
        
        cameras = response.json()
        assert len(cameras) == 1
        assert cameras[0]["name"] == camera_data["name"]
    
    def test_create_camera(self, client: TestClient):
        """Test creating a new camera"""
        camera_data = {
            "name": "New Camera",
            "location": "Building B",
            "ip_address": "192.168.1.101",
            "status": "active"
        }
        
        response = client.post("/api/cameras/", json=camera_data)
        assert response.status_code == 201
        
        camera = response.json()
        assert camera["name"] == camera_data["name"]
        assert camera["location"] == camera_data["location"]
        assert camera["ip_address"] == camera_data["ip_address"]
        assert camera["status"] == camera_data["status"]
        assert "id" in camera
    
    def test_create_camera_invalid_data(self, client: TestClient):
        """Test creating camera with invalid data"""
        invalid_data = {
            "name": "",  # Empty name
            "location": "Building A",
            "ip_address": "invalid-ip",
            "status": "invalid_status"
        }
        
        response = client.post("/api/cameras/", json=invalid_data)
        assert response.status_code == 422
    
    def test_get_camera_by_id(self, client: TestClient, db_session: Session):
        """Test getting camera by ID"""
        # Create test camera
        camera_data = {
            "name": "Test Camera",
            "location": "Building A",
            "ip_address": "192.168.1.100",
            "status": "active"
        }
        
        create_response = client.post("/api/cameras/", json=camera_data)
        camera_id = create_response.json()["id"]
        
        # Get camera by ID
        response = client.get(f"/api/cameras/{camera_id}")
        assert response.status_code == 200
        
        camera = response.json()
        assert camera["id"] == camera_id
        assert camera["name"] == camera_data["name"]
    
    def test_get_camera_not_found(self, client: TestClient):
        """Test getting non-existent camera"""
        response = client.get("/api/cameras/999")
        assert response.status_code == 404
    
    def test_update_camera(self, client: TestClient, db_session: Session):
        """Test updating camera"""
        # Create test camera
        camera_data = {
            "name": "Test Camera",
            "location": "Building A",
            "ip_address": "192.168.1.100",
            "status": "active"
        }
        
        create_response = client.post("/api/cameras/", json=camera_data)
        camera_id = create_response.json()["id"]
        
        # Update camera
        update_data = {
            "name": "Updated Camera",
            "status": "inactive"
        }
        
        response = client.put(f"/api/cameras/{camera_id}", json=update_data)
        assert response.status_code == 200
        
        camera = response.json()
        assert camera["name"] == update_data["name"]
        assert camera["status"] == update_data["status"]
        assert camera["location"] == camera_data["location"]  # Unchanged
    
    def test_delete_camera(self, client: TestClient, db_session: Session):
        """Test deleting camera"""
        # Create test camera
        camera_data = {
            "name": "Test Camera",
            "location": "Building A",
            "ip_address": "192.168.1.100",
            "status": "active"
        }
        
        create_response = client.post("/api/cameras/", json=camera_data)
        camera_id = create_response.json()["id"]
        
        # Delete camera
        response = client.delete(f"/api/cameras/{camera_id}")
        assert response.status_code == 204
        
        # Verify camera is deleted
        get_response = client.get(f"/api/cameras/{camera_id}")
        assert get_response.status_code == 404

class TestCountDataAPI:
    def test_get_count_data(self, client: TestClient, db_session: Session):
        """Test getting count data"""
        # Create test count data
        count_data = {
            "camera_id": 1,
            "count": 25,
            "confidence": 0.95,
            "object_type": "person"
        }
        
        response = client.post("/api/count-data/", json=count_data)
        assert response.status_code == 201
        
        # Get count data
        response = client.get("/api/count-data/")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data) == 1
        assert data[0]["count"] == count_data["count"]
    
    def test_create_count_data(self, client: TestClient):
        """Test creating count data"""
        count_data = {
            "camera_id": 1,
            "count": 30,
            "confidence": 0.92,
            "object_type": "vehicle"
        }
        
        response = client.post("/api/count-data/", json=count_data)
        assert response.status_code == 201
        
        data = response.json()
        assert data["count"] == count_data["count"]
        assert data["confidence"] == count_data["confidence"]
        assert data["object_type"] == count_data["object_type"]
        assert "id" in data
        assert "timestamp" in data
    
    def test_get_count_data_by_camera(self, client: TestClient, db_session: Session):
        """Test getting count data by camera ID"""
        # Create test count data
        count_data = {
            "camera_id": 1,
            "count": 25,
            "confidence": 0.95,
            "object_type": "person"
        }
        
        client.post("/api/count-data/", json=count_data)
        
        # Get count data by camera
        response = client.get("/api/count-data/camera/1")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data) == 1
        assert data[0]["camera_id"] == 1
```

### 🧪 Service Layer Testing

#### Camera Service Testing
```python
# beCamera/tests/test_services.py
import pytest
from unittest.mock import Mock, patch
from src.services.camera_service import CameraService
from src.models import Camera

class TestCameraService:
    def test_get_all_cameras(self, db_session):
        """Test getting all cameras"""
        # Create test cameras
        camera1 = Camera(
            name="Camera 1",
            location="Building A",
            ip_address="192.168.1.100",
            status="active"
        )
        camera2 = Camera(
            name="Camera 2",
            location="Building B",
            ip_address="192.168.1.101",
            status="inactive"
        )
        
        db_session.add(camera1)
        db_session.add(camera2)
        db_session.commit()
        
        service = CameraService(db_session)
        cameras = service.get_all_cameras()
        
        assert len(cameras) == 2
        assert cameras[0].name == "Camera 1"
        assert cameras[1].name == "Camera 2"
    
    def test_get_camera_by_id(self, db_session):
        """Test getting camera by ID"""
        camera = Camera(
            name="Test Camera",
            location="Building A",
            ip_address="192.168.1.100",
            status="active"
        )
        
        db_session.add(camera)
        db_session.commit()
        
        service = CameraService(db_session)
        found_camera = service.get_camera_by_id(camera.id)
        
        assert found_camera is not None
        assert found_camera.name == "Test Camera"
    
    def test_get_camera_by_id_not_found(self, db_session):
        """Test getting non-existent camera"""
        service = CameraService(db_session)
        camera = service.get_camera_by_id(999)
        
        assert camera is None
    
    def test_create_camera(self, db_session):
        """Test creating camera"""
        camera_data = {
            "name": "New Camera",
            "location": "Building A",
            "ip_address": "192.168.1.100",
            "status": "active"
        }
        
        service = CameraService(db_session)
        camera = service.create_camera(camera_data)
        
        assert camera.id is not None
        assert camera.name == camera_data["name"]
        assert camera.location == camera_data["location"]
        assert camera.ip_address == camera_data["ip_address"]
        assert camera.status == camera_data["status"]
    
    def test_update_camera(self, db_session):
        """Test updating camera"""
        camera = Camera(
            name="Original Camera",
            location="Building A",
            ip_address="192.168.1.100",
            status="active"
        )
        
        db_session.add(camera)
        db_session.commit()
        
        update_data = {
            "name": "Updated Camera",
            "status": "inactive"
        }
        
        service = CameraService(db_session)
        updated_camera = service.update_camera(camera.id, update_data)
        
        assert updated_camera.name == "Updated Camera"
        assert updated_camera.status == "inactive"
        assert updated_camera.location == "Building A"  # Unchanged
    
    def test_delete_camera(self, db_session):
        """Test deleting camera"""
        camera = Camera(
            name="Test Camera",
            location="Building A",
            ip_address="192.168.1.100",
            status="active"
        )
        
        db_session.add(camera)
        db_session.commit()
        camera_id = camera.id
        
        service = CameraService(db_session)
        service.delete_camera(camera_id)
        
        # Verify camera is deleted
        deleted_camera = service.get_camera_by_id(camera_id)
        assert deleted_camera is None
```

#### AI Model Service Testing
```python
# beCamera/tests/test_ai_service.py
import pytest
from unittest.mock import Mock, patch
import numpy as np
from src.services.ai_service import AIService

class TestAIService:
    def setup_method(self):
        """Setup for each test"""
        self.ai_service = AIService()
    
    @patch('src.services.ai_service.cv2')
    def test_process_frame(self, mock_cv2):
        """Test processing a single frame"""
        # Mock frame data
        mock_frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        mock_cv2.imread.return_value = mock_frame
        
        # Mock detection results
        mock_detections = [
            {'bbox': [100, 100, 200, 200], 'confidence': 0.95, 'class': 'person'},
            {'bbox': [300, 300, 400, 400], 'confidence': 0.87, 'class': 'person'}
        ]
        
        with patch.object(self.ai_service.model, 'detect') as mock_detect:
            mock_detect.return_value = mock_detections
            
            result = self.ai_service.process_frame(mock_frame)
            
            assert result['count'] == 2
            assert result['confidence'] == 0.91  # Average confidence
            assert result['detections'] == mock_detections
    
    def test_calculate_confidence(self):
        """Test confidence calculation"""
        detections = [
            {'confidence': 0.95},
            {'confidence': 0.87},
            {'confidence': 0.92}
        ]
        
        confidence = self.ai_service.calculate_confidence(detections)
        expected_confidence = (0.95 + 0.87 + 0.92) / 3
        
        assert confidence == pytest.approx(expected_confidence, rel=1e-2)
    
    def test_filter_detections(self):
        """Test detection filtering"""
        detections = [
            {'confidence': 0.95, 'class': 'person'},
            {'confidence': 0.45, 'class': 'person'},  # Below threshold
            {'confidence': 0.92, 'class': 'vehicle'},  # Wrong class
            {'confidence': 0.88, 'class': 'person'}
        ]
        
        filtered = self.ai_service.filter_detections(detections, min_confidence=0.5)
        
        assert len(filtered) == 2
        assert filtered[0]['confidence'] == 0.95
        assert filtered[1]['confidence'] == 0.88
    
    @patch('src.services.ai_service.time')
    def test_process_video_stream(self, mock_time):
        """Test processing video stream"""
        # Mock time to control loop
        mock_time.time.side_effect = [0, 1, 2, 3, 4]  # 5 iterations
        
        # Mock frame generator
        def mock_frame_generator():
            for i in range(5):
                yield np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        
        with patch.object(self.ai_service, 'process_frame') as mock_process:
            mock_process.return_value = {'count': 1, 'confidence': 0.9}
            
            results = list(self.ai_service.process_video_stream(mock_frame_generator(), max_frames=3))
            
            assert len(results) == 3
            assert all(r['count'] == 1 for r in results)
            assert all(r['confidence'] == 0.9 for r in results)
    
    def test_validate_frame(self):
        """Test frame validation"""
        # Valid frame
        valid_frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        assert self.ai_service.validate_frame(valid_frame) is True
        
        # Invalid frame (None)
        assert self.ai_service.validate_frame(None) is False
        
        # Invalid frame (wrong shape)
        invalid_frame = np.random.randint(0, 255, (480, 640), dtype=np.uint8)
        assert self.ai_service.validate_frame(invalid_frame) is False
```

### 📊 Test Coverage

#### Coverage Configuration
```python
# beCamera/.coveragerc
[run]
source = src
omit = 
    */tests/*
    */test_*
    */__pycache__/*
    */migrations/*
    */venv/*
    */env/*

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    if self.debug:
    if settings.DEBUG
    raise AssertionError
    raise NotImplementedError
    if 0:
    if __name__ == .__main__.:
    class .*\bProtocol\):
    @(abc\.)?abstractmethod
```

### 🚀 Performance Testing

#### Load Testing
```python
# beCamera/tests/test_performance.py
import pytest
import asyncio
import time
from concurrent.futures import ThreadPoolExecutor
from src.services.camera_service import CameraService
from src.services.ai_service import AIService

class TestPerformance:
    def test_camera_service_performance(self, db_session):
        """Test camera service performance"""
        service = CameraService(db_session)
        
        # Create 1000 cameras
        start_time = time.time()
        
        for i in range(1000):
            camera_data = {
                "name": f"Camera {i}",
                "location": f"Building {i % 10}",
                "ip_address": f"192.168.1.{i % 255}",
                "status": "active" if i % 2 == 0 else "inactive"
            }
            service.create_camera(camera_data)
        
        creation_time = time.time() - start_time
        assert creation_time < 10.0  # Should create 1000 cameras in < 10 seconds
        
        # Test retrieval performance
        start_time = time.time()
        cameras = service.get_all_cameras()
        retrieval_time = time.time() - start_time
        
        assert len(cameras) == 1000
        assert retrieval_time < 1.0  # Should retrieve in < 1 second
    
    def test_ai_service_performance(self):
        """Test AI service performance"""
        ai_service = AIService()
        
        # Create test frame
        frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        
        # Test processing time
        start_time = time.time()
        
        for _ in range(100):
            result = ai_service.process_frame(frame)
        
        processing_time = time.time() - start_time
        avg_time_per_frame = processing_time / 100
        
        assert avg_time_per_frame < 0.1  # Should process frame in < 100ms
    
    def test_concurrent_requests(self, client):
        """Test concurrent API requests"""
        import threading
        import requests
        
        def make_request():
            response = client.get("/api/cameras/")
            return response.status_code
        
        # Create 10 threads making concurrent requests
        threads = []
        results = []
        
        start_time = time.time()
        
        for _ in range(10):
            thread = threading.Thread(target=lambda: results.append(make_request()))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        total_time = time.time() - start_time
        
        assert all(status == 200 for status in results)
        assert total_time < 5.0  # Should handle 10 concurrent requests in < 5 seconds
```

### 📋 Testing Best Practices

#### Test Organization
```python
# Recommended test structure
class TestComponent:
    def setup_method(self):
        """Setup for each test"""
        pass
    
    def teardown_method(self):
        """Cleanup after each test"""
        pass
    
    def test_happy_path(self):
        """Test normal operation"""
        pass
    
    def test_error_handling(self):
        """Test error conditions"""
        pass
    
    def test_edge_cases(self):
        """Test boundary conditions"""
        pass
    
    def test_performance(self):
        """Test performance requirements"""
        pass
```

#### Test Naming Conventions
```python
# Good test names
def test_should_create_user_with_valid_data(self):
    pass

def test_should_handle_duplicate_email_error(self):
    pass

def test_should_validate_email_format(self):
    pass

def test_should_hash_password_before_saving(self):
    pass

# Avoid these test names
def test_user(self):  # Too vague
    pass

def test_works(self):  # Too vague
    pass

def test1(self):  # Not descriptive
    pass
```

### 🚨 Common Testing Pitfalls

#### Anti-patterns to Avoid
```python
# ❌ Don't test implementation details
def test_should_call_private_method(self):
    # Testing internal implementation
    pass

# ✅ Do test behavior
def test_should_create_user_successfully(self):
    # Testing observable behavior
    pass

# ❌ Don't test third-party libraries
def test_should_use_sqlalchemy(self):
    # Testing library functionality
    pass

# ✅ Do test integration with libraries
def test_should_save_user_to_database(self):
    # Testing your code's behavior with the library
    pass

# ❌ Don't test everything
def test_should_have_exactly_three_attributes(self):
    # Testing implementation details
    pass

# ✅ Do test important behavior
def test_should_validate_user_data(self):
    # Testing user-visible behavior
    pass
```

### 📊 Test Metrics

#### Quality Metrics
- **Test Coverage**: > 80% for critical components
- **Test Reliability**: > 95% pass rate
- **Test Speed**: < 30 seconds for full suite
- **Test Maintainability**: < 10% test code changes per feature

#### Performance Metrics
- **Service Response Time**: < 200ms for API endpoints
- **Database Query Time**: < 50ms for simple queries
- **AI Processing Time**: < 100ms per frame
- **Memory Usage**: < 500MB for test suite

---

**Document Version**: 1.0  
**Last Updated**: 2025-07-03  
**Next Review**: 2025-07-10  
**Status**: Ready for Implementation 