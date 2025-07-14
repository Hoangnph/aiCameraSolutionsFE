# MVP Feature Specifications
## AI Camera Counting System

### 📊 Tổng quan

Tài liệu này định nghĩa chi tiết các tính năng MVP cho hệ thống AI Camera Counting, bao gồm user stories, acceptance criteria, technical requirements, và implementation guidelines.

### 🎯 MVP Objectives
- Demo-ready system với core functionality
- Real-time camera counting với AI model
- Basic user authentication và management
- Simple dashboard với essential metrics
- Scalable architecture foundation

### 👥 User Stories & Acceptance Criteria

#### Authentication & User Management

**US-001: User Registration**
```
As a new user
I want to create an account
So that I can access the camera counting system

Acceptance Criteria:
- User can register with email and password
- Email validation is required
- Password must meet security requirements (min 8 chars, uppercase, lowercase, number)
- Registration confirmation email is sent
- User is redirected to login after successful registration
- Duplicate email addresses are rejected
```

**US-002: User Login**
```
As a registered user
I want to log into the system
So that I can access my camera dashboard

Acceptance Criteria:
- User can login with email and password
- Invalid credentials show appropriate error message
- Successful login redirects to dashboard
- Session is maintained for 24 hours
- Logout functionality is available
- Password reset functionality is available
```

**US-003: User Profile Management**
```
As a logged-in user
I want to manage my profile information
So that I can keep my account details updated

Acceptance Criteria:
- User can view current profile information
- User can update email, name, and password
- Password change requires current password verification
- Profile changes are saved immediately
- Validation errors are displayed clearly
```

#### Camera Management

**US-004: Add Camera**
```
As a logged-in user
I want to add a new camera to the system
So that I can start counting people/objects

Acceptance Criteria:
- User can add camera with name, location, and IP address
- Camera connection is tested automatically
- Camera is activated only after successful connection test
- Camera appears in dashboard after successful addition
- Duplicate camera names are rejected
- Invalid IP addresses are rejected
```

**US-005: View Camera List**
```
As a logged-in user
I want to see all my cameras
So that I can monitor their status and performance

Acceptance Criteria:
- All user's cameras are displayed in a list
- Each camera shows: name, location, status, last count, last update
- Cameras are sorted by name or last activity
- Search and filter functionality is available
- Camera status is updated in real-time
```

**US-006: Camera Details**
```
As a logged-in user
I want to view detailed information about a specific camera
So that I can monitor its performance and settings

Acceptance Criteria:
- Camera details page shows comprehensive information
- Real-time video feed is displayed (if available)
- Current count and confidence score are shown
- Historical count data is displayed in a chart
- Camera settings can be modified
- Camera can be enabled/disabled
```

**US-007: Edit Camera**
```
As a logged-in user
I want to edit camera information
So that I can update camera details as needed

Acceptance Criteria:
- User can edit camera name, location, and IP address
- Connection test is performed after IP change
- Changes are saved only after successful validation
- Camera remains active during editing process
- History of changes is maintained
```

**US-008: Delete Camera**
```
As a logged-in user
I want to remove a camera from the system
So that I can clean up unused cameras

Acceptance Criteria:
- User can delete camera with confirmation dialog
- Deleted camera data is archived for 30 days
- Camera stops processing immediately after deletion
- User is redirected to camera list after deletion
- Deletion can be undone within 24 hours
```

#### Real-time Counting

**US-009: Real-time Count Display**
```
As a logged-in user
I want to see real-time count data from my cameras
So that I can monitor current activity levels

Acceptance Criteria:
- Current count is displayed for each camera
- Count updates in real-time (every 5 seconds)
- Confidence score is shown alongside count
- Count history is maintained for 24 hours
- Anomalies in count data are highlighted
```

**US-010: Count Accuracy**
```
As a logged-in user
I want accurate count data from my cameras
So that I can rely on the information for decision making

Acceptance Criteria:
- AI model achieves >90% accuracy in controlled environments
- False positives are minimized (<5%)
- Count data is validated against known scenarios
- Confidence scores accurately reflect model certainty
- Model performance is monitored and reported
```

**US-011: Count History**
```
As a logged-in user
I want to view historical count data
So that I can analyze trends and patterns

Acceptance Criteria:
- Count history is available for last 30 days
- Data is displayed in interactive charts
- Time-based filtering is available (hourly, daily, weekly)
- Export functionality is available (CSV, JSON)
- Data can be filtered by camera and time range
```

#### Dashboard & Analytics

**US-012: Dashboard Overview**
```
As a logged-in user
I want to see an overview of all my cameras and their performance
So that I can quickly assess system status

Acceptance Criteria:
- Dashboard shows summary of all cameras
- Key metrics are displayed prominently
- System status is clearly indicated
- Quick actions are available (add camera, view details)
- Real-time updates are visible
```

**US-013: Performance Metrics**
```
As a logged-in user
I want to see performance metrics for my cameras
So that I can optimize system performance

Acceptance Criteria:
- Response time for each camera is displayed
- Processing accuracy is shown
- System uptime is tracked
- Error rates are monitored
- Performance trends are visualized
```

**US-014: Alert System**
```
As a logged-in user
I want to be notified of important events
So that I can respond quickly to issues

Acceptance Criteria:
- Camera offline alerts are sent immediately
- High count anomalies trigger notifications
- System performance alerts are configurable
- Alerts are sent via email and in-app notifications
- Alert history is maintained
```

### 🏗️ Technical Requirements

#### Frontend Requirements

**React Components Structure**
```typescript
// Core Components
interface CameraCardProps {
  camera: Camera;
  onEdit: (camera: Camera) => void;
  onDelete: (cameraId: string) => void;
  onViewDetails: (cameraId: string) => void;
}

interface CountDisplayProps {
  count: number;
  confidence: number;
  timestamp: Date;
  isRealTime: boolean;
}

interface DashboardProps {
  cameras: Camera[];
  counts: CountData[];
  systemStatus: SystemStatus;
}

// Data Models
interface Camera {
  id: string;
  name: string;
  location: string;
  ipAddress: string;
  status: 'active' | 'inactive' | 'error';
  lastCount: number;
  lastUpdate: Date;
  confidence: number;
}

interface CountData {
  cameraId: string;
  count: number;
  confidence: number;
  timestamp: Date;
  objectType: 'person' | 'vehicle' | 'object';
}

interface SystemStatus {
  totalCameras: number;
  activeCameras: number;
  totalCounts: number;
  systemHealth: 'healthy' | 'warning' | 'error';
}
```

**State Management**
```typescript
// Zustand Store
interface AppState {
  // Authentication
  user: User | null;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  
  // Cameras
  cameras: Camera[];
  selectedCamera: Camera | null;
  addCamera: (camera: Omit<Camera, 'id'>) => Promise<void>;
  updateCamera: (id: string, updates: Partial<Camera>) => Promise<void>;
  deleteCamera: (id: string) => Promise<void>;
  
  // Counts
  counts: CountData[];
  realTimeCounts: Map<string, CountData>;
  fetchCounts: (cameraId: string, timeRange: TimeRange) => Promise<void>;
  
  // System
  systemStatus: SystemStatus;
  refreshSystemStatus: () => Promise<void>;
}
```

#### Backend Requirements

**API Endpoints**
```python
# FastAPI Routes
@router.post("/cameras")
async def create_camera(camera: CameraCreate, user: User = Depends(get_current_user)):
    """Create a new camera"""
    pass

@router.get("/cameras")
async def list_cameras(user: User = Depends(get_current_user)):
    """List user's cameras"""
    pass

@router.get("/cameras/{camera_id}")
async def get_camera(camera_id: str, user: User = Depends(get_current_user)):
    """Get camera details"""
    pass

@router.put("/cameras/{camera_id}")
async def update_camera(camera_id: str, updates: CameraUpdate, user: User = Depends(get_current_user)):
    """Update camera"""
    pass

@router.delete("/cameras/{camera_id}")
async def delete_camera(camera_id: str, user: User = Depends(get_current_user)):
    """Delete camera"""
    pass

@router.get("/cameras/{camera_id}/counts")
async def get_counts(camera_id: str, time_range: TimeRange, user: User = Depends(get_current_user)):
    """Get count data for camera"""
    pass

@router.get("/system/status")
async def get_system_status(user: User = Depends(get_current_user)):
    """Get system status"""
    pass
```

**AI Model Integration**
```python
# AI Processing Service
class AICountingService:
    def __init__(self):
        self.model = self._load_model()
        self.preprocessor = self._load_preprocessor()
    
    async def process_frame(self, frame: np.ndarray, camera_id: str) -> CountResult:
        """Process camera frame and return count result"""
        try:
            # Preprocess frame
            processed_frame = self.preprocessor.process(frame)
            
            # Run inference
            predictions = self.model.predict(processed_frame)
            
            # Post-process results
            count_result = self._post_process(predictions)
            
            # Record metrics
            await self._record_metrics(camera_id, count_result)
            
            return count_result
        except Exception as e:
            logger.error(f"Error processing frame for camera {camera_id}: {e}")
            raise
    
    def _post_process(self, predictions: np.ndarray) -> CountResult:
        """Post-process model predictions"""
        # Count objects
        count = len(predictions)
        
        # Calculate confidence
        confidence = np.mean([pred['confidence'] for pred in predictions])
        
        return CountResult(
            count=count,
            confidence=confidence,
            objects=predictions,
            timestamp=datetime.utcnow()
        )
```

#### Database Schema

**PostgreSQL Tables**
```sql
-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Cameras table
CREATE TABLE cameras (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    location VARCHAR(500),
    ip_address INET NOT NULL,
    status VARCHAR(50) DEFAULT 'inactive',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Count data table
CREATE TABLE count_data (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    camera_id UUID REFERENCES cameras(id) ON DELETE CASCADE,
    count INTEGER NOT NULL,
    confidence DECIMAL(3,2) NOT NULL,
    object_type VARCHAR(50) DEFAULT 'person',
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- System events table
CREATE TABLE system_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    camera_id UUID REFERENCES cameras(id) ON DELETE CASCADE,
    event_type VARCHAR(50) NOT NULL,
    message TEXT,
    severity VARCHAR(20) DEFAULT 'info',
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_cameras_user_id ON cameras(user_id);
CREATE INDEX idx_count_data_camera_id ON count_data(camera_id);
CREATE INDEX idx_count_data_timestamp ON count_data(timestamp);
CREATE INDEX idx_system_events_camera_id ON system_events(camera_id);
```

### 🎨 UI/UX Requirements

#### Design System
```typescript
// Theme Configuration
const theme = {
  colors: {
    primary: '#3B82F6',
    secondary: '#6B7280',
    success: '#10B981',
    warning: '#F59E0B',
    error: '#EF4444',
    background: '#F9FAFB',
    surface: '#FFFFFF',
    text: {
      primary: '#111827',
      secondary: '#6B7280',
      disabled: '#9CA3AF'
    }
  },
  spacing: {
    xs: '0.25rem',
    sm: '0.5rem',
    md: '1rem',
    lg: '1.5rem',
    xl: '2rem',
    xxl: '3rem'
  },
  borderRadius: {
    sm: '0.25rem',
    md: '0.5rem',
    lg: '1rem',
    full: '9999px'
  }
};

// Component Variants
const buttonVariants = {
  primary: 'bg-blue-600 hover:bg-blue-700 text-white',
  secondary: 'bg-gray-600 hover:bg-gray-700 text-white',
  outline: 'border border-gray-300 hover:bg-gray-50 text-gray-700',
  danger: 'bg-red-600 hover:bg-red-700 text-white'
};
```

#### Responsive Design
```css
/* Mobile First Approach */
.camera-grid {
  display: grid;
  gap: 1rem;
  padding: 1rem;
}

/* Mobile */
@media (max-width: 640px) {
  .camera-grid {
    grid-template-columns: 1fr;
  }
}

/* Tablet */
@media (min-width: 641px) and (max-width: 1024px) {
  .camera-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* Desktop */
@media (min-width: 1025px) {
  .camera-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}
```

### 🔒 Security Requirements

#### Authentication & Authorization
```typescript
// JWT Token Management
interface JWTPayload {
  userId: string;
  email: string;
  role: 'user' | 'admin';
  exp: number;
  iat: number;
}

// Authorization Middleware
const requireAuth = (req: Request, res: Response, next: NextFunction) => {
  const token = req.headers.authorization?.replace('Bearer ', '');
  
  if (!token) {
    return res.status(401).json({ error: 'Authentication required' });
  }
  
  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET) as JWTPayload;
    req.user = decoded;
    next();
  } catch (error) {
    return res.status(401).json({ error: 'Invalid token' });
  }
};

// Role-based Authorization
const requireRole = (role: string) => {
  return (req: Request, res: Response, next: NextFunction) => {
    if (req.user.role !== role) {
      return res.status(403).json({ error: 'Insufficient permissions' });
    }
    next();
  };
};
```

#### Data Protection
```python
# Data Encryption
from cryptography.fernet import Fernet
import base64

class DataEncryption:
    def __init__(self):
        self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)
    
    def encrypt_sensitive_data(self, data: str) -> str:
        """Encrypt sensitive data"""
        return self.cipher.encrypt(data.encode()).decode()
    
    def decrypt_sensitive_data(self, encrypted_data: str) -> str:
        """Decrypt sensitive data"""
        return self.cipher.decrypt(encrypted_data.encode()).decode()

# Input Validation
from pydantic import BaseModel, validator
import re

class CameraCreate(BaseModel):
    name: str
    location: str
    ip_address: str
    
    @validator('name')
    def validate_name(cls, v):
        if len(v) < 2 or len(v) > 100:
            raise ValueError('Name must be between 2 and 100 characters')
        return v
    
    @validator('ip_address')
    def validate_ip_address(cls, v):
        ip_pattern = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')
        if not ip_pattern.match(v):
            raise ValueError('Invalid IP address format')
        return v
```

### 📊 Performance Requirements

#### Response Time Targets
- **Page Load**: < 2 seconds
- **API Response**: < 200ms (95th percentile)
- **Real-time Updates**: < 5 seconds
- **Image Processing**: < 1 second per frame

#### Scalability Targets
- **Concurrent Users**: 100+ simultaneous users
- **Cameras per User**: 50+ cameras per user
- **Data Retention**: 30 days of count data
- **System Uptime**: 99.9% availability

#### Resource Usage Limits
- **Memory Usage**: < 2GB per service instance
- **CPU Usage**: < 80% under normal load
- **Database Connections**: < 100 concurrent connections
- **File Storage**: < 10GB per user

### 🧪 Testing Requirements

#### Unit Testing
```typescript
// Component Testing
describe('CameraCard', () => {
  it('should display camera information correctly', () => {
    const camera = {
      id: '1',
      name: 'Test Camera',
      location: 'Test Location',
      status: 'active',
      lastCount: 5,
      confidence: 0.95
    };
    
    render(<CameraCard camera={camera} />);
    
    expect(screen.getByText('Test Camera')).toBeInTheDocument();
    expect(screen.getByText('Test Location')).toBeInTheDocument();
    expect(screen.getByText('5')).toBeInTheDocument();
  });
});

// API Testing
describe('Camera API', () => {
  it('should create camera successfully', async () => {
    const cameraData = {
      name: 'Test Camera',
      location: 'Test Location',
      ip_address: '192.168.1.100'
    };
    
    const response = await request(app)
      .post('/api/cameras')
      .send(cameraData)
      .set('Authorization', `Bearer ${token}`);
    
    expect(response.status).toBe(201);
    expect(response.body.name).toBe('Test Camera');
  });
});
```

#### Integration Testing
```python
# AI Model Integration Test
async def test_ai_processing_integration():
    """Test AI model integration with camera service"""
    # Setup test camera
    camera = await create_test_camera()
    
    # Generate test frame
    test_frame = generate_test_frame()
    
    # Process frame
    result = await ai_service.process_frame(test_frame, camera.id)
    
    # Verify results
    assert result.count >= 0
    assert 0 <= result.confidence <= 1
    assert result.timestamp is not None
    
    # Verify data persistence
    saved_data = await get_count_data(camera.id)
    assert len(saved_data) > 0
```

### 📋 Implementation Checklist

#### Phase 1: Core Infrastructure (Week 1)
- [ ] Setup authentication system
- [ ] Create database schema
- [ ] Implement basic API endpoints
- [ ] Setup frontend project structure
- [ ] Create basic UI components

#### Phase 2: Camera Management (Week 2)
- [ ] Implement camera CRUD operations
- [ ] Create camera dashboard
- [ ] Add camera connection testing
- [ ] Implement camera status monitoring
- [ ] Create camera detail views

#### Phase 3: AI Integration (Week 3)
- [ ] Integrate AI counting model
- [ ] Implement real-time processing
- [ ] Create count data storage
- [ ] Add confidence scoring
- [ ] Implement performance monitoring

#### Phase 4: Analytics & Polish (Week 4)
- [ ] Create analytics dashboard
- [ ] Implement data visualization
- [ ] Add export functionality
- [ ] Polish UI/UX
- [ ] Performance optimization

### 🎯 Success Metrics

#### Functional Metrics
- **Feature Completeness**: 100% of MVP features implemented
- **Bug Rate**: < 5% of tickets are bugs
- **Test Coverage**: > 80% code coverage
- **Documentation**: 100% of APIs documented

#### Performance Metrics
- **Response Time**: < 200ms for 95% of requests
- **Uptime**: > 99.9% availability
- **Error Rate**: < 1% error rate
- **Load Time**: < 2 seconds page load

#### User Experience Metrics
- **User Onboarding**: < 5 minutes to first camera setup
- **Task Completion**: > 90% success rate for core tasks
- **User Satisfaction**: > 4.0/5.0 rating
- **Support Tickets**: < 10% of users need support

---

**Document Version**: 1.0  
**Last Updated**: 2025-07-03  
**Next Review**: 2025-07-10  
**Status**: Ready for Implementation 