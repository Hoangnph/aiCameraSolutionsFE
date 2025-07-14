# Coding Standards - AI Camera Counting System

## 📊 Tổng quan
Tài liệu này định nghĩa các tiêu chuẩn coding cho hệ thống AI Camera Counting, bao gồm naming conventions, code style, best practices và quality gates.

## 🎯 General Principles

### 1. Code Quality
- **Readability**: Code phải dễ đọc và hiểu
- **Maintainability**: Code phải dễ bảo trì và mở rộng
- **Consistency**: Tuân thủ conventions nhất quán
- **Performance**: Tối ưu hiệu suất khi cần thiết
- **Security**: Ưu tiên bảo mật trong mọi implementation

### 2. SOLID Principles
- **Single Responsibility**: Mỗi function/class chỉ có một trách nhiệm
- **Open/Closed**: Mở để mở rộng, đóng để sửa đổi
- **Liskov Substitution**: Subtypes có thể thay thế base types
- **Interface Segregation**: Interfaces nhỏ và focused
- **Dependency Inversion**: Phụ thuộc vào abstractions, không phải concretions

## 📝 Naming Conventions

### 1. JavaScript/TypeScript

#### Variables & Functions
```javascript
// ✅ Good
const userCount = 0;
const isAuthenticated = true;
const hasPermission = false;
const getUserById = (id) => { /* ... */ };
const validateEmail = (email) => { /* ... */ };
const handleSubmit = () => { /* ... */ };

// ❌ Bad
const count = 0;
const auth = true;
const perm = false;
const get = (id) => { /* ... */ };
const validate = (email) => { /* ... */ };
const submit = () => { /* ... */ };
```

#### Constants
```javascript
// ✅ Good
const API_BASE_URL = 'http://localhost:3001/api/v1';
const MAX_RETRY_ATTEMPTS = 3;
const DEFAULT_TIMEOUT = 5000;
const USER_ROLES = {
  ADMIN: 'admin',
  USER: 'user',
  VIEWER: 'viewer'
};

// ❌ Bad
const url = 'http://localhost:3001/api/v1';
const max = 3;
const timeout = 5000;
```

#### Classes & Components
```javascript
// ✅ Good
class UserService { /* ... */ }
class CameraManager { /* ... */ }
function UserProfile() { /* ... */ }
function CameraCard() { /* ... */ }

// ❌ Bad
class userService { /* ... */ }
class camera_manager { /* ... */ }
function user_profile() { /* ... */ }
```

#### Files & Directories
```
// ✅ Good
src/
├── components/
│   ├── CameraCard/
│   │   ├── index.js
│   │   ├── CameraCard.js
│   │   └── CameraCard.test.js
│   └── UserProfile/
├── services/
│   ├── authService.js
│   └── cameraService.js
├── utils/
│   ├── validation.js
│   └── formatters.js
└── hooks/
    ├── useAuth.js
    └── useCamera.js

// ❌ Bad
src/
├── Components/
├── services/
├── Utils/
└── Hooks/
```

### 2. Python

#### Variables & Functions
```python
# ✅ Good
user_count = 0
is_authenticated = True
has_permission = False

def get_user_by_id(user_id: int) -> User:
    """Get user by ID."""
    pass

def validate_email(email: str) -> bool:
    """Validate email format."""
    pass

def handle_submit() -> None:
    """Handle form submission."""
    pass

# ❌ Bad
count = 0
auth = True
perm = False

def get(id):
    pass

def validate(email):
    pass
```

#### Classes
```python
# ✅ Good
class UserService:
    """Service for user operations."""
    
    def __init__(self, db_connection):
        self.db_connection = db_connection
    
    def create_user(self, user_data: dict) -> User:
        """Create a new user."""
        pass

# ❌ Bad
class userService:
    def __init__(self, db):
        self.db = db
    
    def create(self, data):
        pass
```

#### Files & Directories
```
# ✅ Good
beCamera/
├── src/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── camera_routes.py
│   │   └── auth_routes.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── camera.py
│   │   └── user.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── camera_service.py
│   │   └── auth_service.py
│   └── utils/
│       ├── __init__.py
│       ├── validation.py
│       └── database.py

# ❌ Bad
beCamera/
├── src/
├── API/
├── Models/
└── Services/
```

## 🎨 Code Style

### 1. JavaScript/TypeScript

#### Formatting
```javascript
// ✅ Good - Consistent indentation
function processUserData(user) {
  const { id, name, email } = user;
  
  if (!id || !name || !email) {
    throw new Error('Invalid user data');
  }
  
  return {
    userId: id,
    userName: name,
    userEmail: email,
    processedAt: new Date().toISOString()
  };
}

// ❌ Bad - Inconsistent formatting
function processUserData(user){
const {id,name,email}=user;
if(!id||!name||!email){
throw new Error('Invalid user data');
}
return {userId:id,userName:name,userEmail:email,processedAt:new Date().toISOString()};
}
```

#### Function Structure
```javascript
// ✅ Good - Clear structure
async function createCamera(cameraData) {
  // 1. Validate input
  if (!cameraData.name || !cameraData.location) {
    throw new Error('Camera name and location are required');
  }
  
  // 2. Process data
  const processedData = {
    ...cameraData,
    status: cameraData.status || 'offline',
    created_at: new Date().toISOString()
  };
  
  // 3. Save to database
  const result = await cameraService.create(processedData);
  
  // 4. Return result
  return {
    success: true,
    data: result,
    message: 'Camera created successfully'
  };
}

// ❌ Bad - Unclear structure
async function createCamera(cameraData) {
  const result = await cameraService.create({
    ...cameraData,
    status: cameraData.status || 'offline',
    created_at: new Date().toISOString()
  });
  return { success: true, data: result, message: 'Camera created successfully' };
}
```

### 2. Python

#### Formatting (PEP 8)
```python
# ✅ Good - PEP 8 compliant
def create_camera(camera_data: dict) -> dict:
    """Create a new camera.
    
    Args:
        camera_data: Dictionary containing camera information
        
    Returns:
        Dictionary with camera creation result
        
    Raises:
        ValueError: If required fields are missing
    """
    # Validate input
    if not camera_data.get('name') or not camera_data.get('location'):
        raise ValueError('Camera name and location are required')
    
    # Process data
    processed_data = {
        **camera_data,
        'status': camera_data.get('status', 'offline'),
        'created_at': datetime.now().isoformat()
    }
    
    # Save to database
    result = camera_service.create(processed_data)
    
    # Return result
    return {
        'success': True,
        'data': result,
        'message': 'Camera created successfully'
    }

# ❌ Bad - Not PEP 8 compliant
def createCamera(cameraData):
    if not cameraData.get('name') or not cameraData.get('location'):
        raise ValueError('Camera name and location are required')
    processedData={**cameraData,'status':cameraData.get('status','offline'),'created_at':datetime.now().isoformat()}
    result=camera_service.create(processedData)
    return {'success':True,'data':result,'message':'Camera created successfully'}
```

## 🔧 Best Practices

### 1. Error Handling

#### JavaScript/TypeScript
```javascript
// ✅ Good - Proper error handling
async function fetchCameraData(cameraId) {
  try {
    const response = await fetch(`/api/v1/cameras/${cameraId}`);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Failed to fetch camera data:', error);
    throw new Error('Unable to fetch camera data');
  }
}

// ❌ Bad - Poor error handling
async function fetchCameraData(cameraId) {
  const response = await fetch(`/api/v1/cameras/${cameraId}`);
  const data = await response.json();
  return data;
}
```

#### Python
```python
# ✅ Good - Proper error handling
async def fetch_camera_data(camera_id: int) -> dict:
    """Fetch camera data from API.
    
    Args:
        camera_id: ID of the camera to fetch
        
    Returns:
        Camera data dictionary
        
    Raises:
        HTTPError: If API request fails
        ValueError: If camera_id is invalid
    """
    try:
        if not isinstance(camera_id, int) or camera_id <= 0:
            raise ValueError('Invalid camera ID')
            
        async with aiohttp.ClientSession() as session:
            async with session.get(f'/api/v1/cameras/{camera_id}') as response:
                response.raise_for_status()
                return await response.json()
                
    except aiohttp.ClientError as e:
        logger.error(f'Failed to fetch camera data: {e}')
        raise HTTPError(f'Unable to fetch camera data: {e}')

# ❌ Bad - Poor error handling
async def fetch_camera_data(camera_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'/api/v1/cameras/{camera_id}') as response:
            return await response.json()
```

### 2. Type Safety

#### TypeScript
```typescript
// ✅ Good - Strong typing
interface Camera {
  id: number;
  name: string;
  location: string;
  stream_url?: string;
  status: 'active' | 'inactive' | 'maintenance' | 'offline';
  created_at: string;
  updated_at: string;
}

interface CreateCameraRequest {
  name: string;
  location: string;
  stream_url?: string;
  status?: Camera['status'];
}

async function createCamera(data: CreateCameraRequest): Promise<Camera> {
  // Implementation
}

// ❌ Bad - No typing
function createCamera(data) {
  // Implementation
}
```

#### Python (Type Hints)
```python
# ✅ Good - Type hints
from typing import Optional, List, Dict, Any
from datetime import datetime

class Camera:
    def __init__(
        self,
        id: int,
        name: str,
        location: str,
        stream_url: Optional[str] = None,
        status: str = 'offline',
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.name = name
        self.location = location
        self.stream_url = stream_url
        self.status = status
        self.created_at = created_at or datetime.now()

def create_camera(data: Dict[str, Any]) -> Camera:
    """Create a new camera instance."""
    pass

# ❌ Bad - No type hints
class Camera:
    def __init__(self, id, name, location, stream_url=None, status='offline', created_at=None):
        self.id = id
        self.name = name
        self.location = location
        self.stream_url = stream_url
        self.status = status
        self.created_at = created_at

def create_camera(data):
    pass
```

### 3. Documentation

#### JavaScript/TypeScript
```javascript
/**
 * Creates a new camera in the system.
 * 
 * @param {Object} cameraData - Camera data object
 * @param {string} cameraData.name - Camera name (required)
 * @param {string} cameraData.location - Camera location (required)
 * @param {string} [cameraData.stream_url] - Camera stream URL
 * @param {string} [cameraData.status='offline'] - Camera status
 * 
 * @returns {Promise<Object>} Promise that resolves to camera creation result
 * @throws {Error} If camera data is invalid or creation fails
 * 
 * @example
 * const result = await createCamera({
 *   name: 'Main Entrance',
 *   location: 'Building A',
 *   stream_url: 'rtsp://camera.com/stream'
 * });
 */
async function createCamera(cameraData) {
  // Implementation
}
```

#### Python
```python
def create_camera(camera_data: dict) -> dict:
    """Create a new camera in the system.
    
    This function validates the camera data and creates a new camera
    record in the database. It ensures all required fields are present
    and sets default values for optional fields.
    
    Args:
        camera_data: Dictionary containing camera information
            - name (str): Camera name (required)
            - location (str): Camera location (required)
            - stream_url (str, optional): Camera stream URL
            - status (str, optional): Camera status (default: 'offline')
            
    Returns:
        dict: Camera creation result with success status and data
        
    Raises:
        ValueError: If required fields are missing or invalid
        DatabaseError: If database operation fails
        
    Example:
        >>> result = create_camera({
        ...     'name': 'Main Entrance',
        ...     'location': 'Building A',
        ...     'stream_url': 'rtsp://camera.com/stream'
        ... })
        >>> print(result['success'])
        True
    """
    # Implementation
    pass
```

## 🧪 Testing Standards

### 1. Test Structure
```javascript
// ✅ Good - Clear test structure
describe('CameraService', () => {
  let cameraService;
  let mockDatabase;

  beforeEach(() => {
    mockDatabase = createMockDatabase();
    cameraService = new CameraService(mockDatabase);
  });

  describe('createCamera', () => {
    it('should create camera with valid data', async () => {
      // Arrange
      const cameraData = {
        name: 'Test Camera',
        location: 'Test Location'
      };

      // Act
      const result = await cameraService.createCamera(cameraData);

      // Assert
      expect(result.success).toBe(true);
      expect(result.data.name).toBe(cameraData.name);
    });

    it('should throw error for invalid data', async () => {
      // Arrange
      const invalidData = { name: '' };

      // Act & Assert
      await expect(cameraService.createCamera(invalidData))
        .rejects.toThrow('Camera name is required');
    });
  });
});
```

### 2. Test Naming
```javascript
// ✅ Good - Descriptive test names
describe('User Authentication', () => {
  it('should login user with valid credentials', () => {});
  it('should reject login with invalid password', () => {});
  it('should lock account after 5 failed attempts', () => {});
  it('should refresh token before expiration', () => {});
});

// ❌ Bad - Unclear test names
describe('Auth', () => {
  it('should work', () => {});
  it('should fail', () => {});
  it('should do something', () => {});
});
```

## 🔒 Security Standards

### 1. Input Validation
```javascript
// ✅ Good - Input validation
function validateUserInput(userData) {
  const errors = [];

  if (!userData.email || !isValidEmail(userData.email)) {
    errors.push('Valid email is required');
  }

  if (!userData.password || userData.password.length < 8) {
    errors.push('Password must be at least 8 characters');
  }

  if (userData.username && !/^[a-zA-Z0-9_]{3,20}$/.test(userData.username)) {
    errors.push('Username must be 3-20 characters, alphanumeric and underscore only');
  }

  return errors;
}

// ❌ Bad - No validation
function processUserInput(userData) {
  return userData; // Dangerous!
}
```

### 2. SQL Injection Prevention
```javascript
// ✅ Good - Parameterized queries
async function getUserById(userId) {
  const query = 'SELECT * FROM users WHERE id = $1';
  const result = await db.query(query, [userId]);
  return result.rows[0];
}

// ❌ Bad - SQL injection vulnerable
async function getUserById(userId) {
  const query = `SELECT * FROM users WHERE id = ${userId}`;
  const result = await db.query(query);
  return result.rows[0];
}
```

## 📊 Code Quality Gates

### 1. Linting Rules
```json
// .eslintrc.js
module.exports = {
  extends: [
    'eslint:recommended',
    '@typescript-eslint/recommended',
    'react/recommended'
  ],
  rules: {
    'no-console': 'warn',
    'no-debugger': 'error',
    'no-unused-vars': 'error',
    'prefer-const': 'error',
    'no-var': 'error',
    'eqeqeq': 'error',
    'curly': 'error',
    'indent': ['error', 2],
    'quotes': ['error', 'single'],
    'semi': ['error', 'always']
  }
};
```

### 2. Pre-commit Hooks
```json
// package.json
{
  "husky": {
    "hooks": {
      "pre-commit": "lint-staged",
      "pre-push": "npm run test:coverage"
    }
  },
  "lint-staged": {
    "*.{js,jsx,ts,tsx}": [
      "eslint --fix",
      "prettier --write",
      "git add"
    ],
    "*.{py}": [
      "black",
      "flake8",
      "git add"
    ]
  }
}
```

### 3. Coverage Requirements
```json
// jest.config.js
module.exports = {
  collectCoverageFrom: [
    'src/**/*.{js,jsx,ts,tsx}',
    '!src/**/*.d.ts',
    '!src/index.js'
  ],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80
    }
  }
};
```

## 🚀 Performance Guidelines

### 1. React Optimization
```javascript
// ✅ Good - Memoized components
import React, { memo, useMemo, useCallback } from 'react';

const CameraCard = memo(function CameraCard({ camera, onSelect }) {
  const statusColor = useMemo(() => {
    switch (camera.status) {
      case 'active': return 'success';
      case 'inactive': return 'error';
      case 'maintenance': return 'warning';
      default: return 'default';
    }
  }, [camera.status]);

  const handleClick = useCallback(() => {
    onSelect(camera);
  }, [camera, onSelect]);

  return (
    <Card onClick={handleClick}>
      <CardHeader title={camera.name} />
      <CardContent>
        <Chip label={camera.status} color={statusColor} />
      </CardContent>
    </Card>
  );
});

// ❌ Bad - No optimization
function CameraCard({ camera, onSelect }) {
  const statusColor = camera.status === 'active' ? 'success' : 'error';
  
  return (
    <Card onClick={() => onSelect(camera)}>
      <CardHeader title={camera.name} />
      <CardContent>
        <Chip label={camera.status} color={statusColor} />
      </CardContent>
    </Card>
  );
}
```

### 2. API Optimization
```javascript
// ✅ Good - Efficient API calls
class CameraService {
  constructor() {
    this.cache = new Map();
    this.cacheTimeout = 5 * 60 * 1000; // 5 minutes
  }

  async getCamera(id) {
    const cacheKey = `camera_${id}`;
    const cached = this.cache.get(cacheKey);
    
    if (cached && Date.now() - cached.timestamp < this.cacheTimeout) {
      return cached.data;
    }

    const data = await this.fetchCamera(id);
    this.cache.set(cacheKey, {
      data,
      timestamp: Date.now()
    });

    return data;
  }
}

// ❌ Bad - No caching
class CameraService {
  async getCamera(id) {
    return await this.fetchCamera(id);
  }
}
```

---

**Last Updated**: 2025-07-03  
**Version**: 1.0.0  
**Status**: Ready for Implementation 