# Kiến trúc hệ thống - People Counting Dashboard

## Tổng quan kiến trúc

Hệ thống People Counting Dashboard được xây dựng theo kiến trúc microservices với frontend React và backend Python, sử dụng WebSocket để truyền dữ liệu thời gian thực.

## Sơ đồ kiến trúc

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   Database      │
│   (React)       │◄──►│   (Python)      │◄──►│  (PostgreSQL)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │              ┌─────────────────┐              │
         └──────────────►│   WebSocket     │◄─────────────┘
                        │   Server        │
                        └─────────────────┘
                                │
                        ┌─────────────────┐
                        │   Camera        │
                        │   Streams       │
                        └─────────────────┘
```

## Frontend Architecture

### 1. Component Hierarchy

```
App
├── ThemeProvider
├── CssBaseline
├── Sidenav
├── Configurator
└── Router
    ├── Dashboard
    │   ├── LiveCounters
    │   ├── CameraGrid
    │   ├── QuickStats
    │   └── AlertPanel
    ├── Cameras
    │   ├── CameraViewer
    │   ├── CameraControls
    │   ├── CameraSettings
    │   └── CameraManagement
    ├── Analytics
    │   ├── RealTimeChart
    │   ├── HistoricalChart
    │   ├── PeakHoursChart
    │   ├── MetricsCards
    │   ├── ReportGenerator
    │   ├── DataTable
    │   ├── ExportOptions
    │   └── FilterPanel
    ├── Alerts
    │   ├── AlertList
    │   └── NotificationCenter
    └── Settings
        ├── Profile
        ├── System
        ├── Detection
        └── Billing
```

### 2. State Management

```typescript
interface AppState {
  auth: AuthState;
  cameras: CameraState;
  analytics: AnalyticsState;
  alerts: AlertState;
  ui: UIState;
}

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
}

interface CameraState {
  list: Camera[];
  activeCamera: Camera | null;
  liveStream: StreamData | null;
  status: 'connecting' | 'connected' | 'disconnected' | 'error';
}

interface AnalyticsState {
  realtime: RealTimeData;
  historical: HistoricalData;
  reports: {
    peopleCount: PeopleCountReport;
    peakHours: PeakHoursReport;
  };
  selectedTimeRange: TimeRange;
  selectedReport: 'people-count' | 'peak-hours';
}

interface AlertState {
  notifications: Alert[];
  isAlertEnabled: boolean;
}

interface UIState {
  theme: 'light' | 'dark';
  sidebar: {
    isOpen: boolean;
    isCollapsed: boolean;
  };
  selectedView: 'live' | 'analytics' | 'alerts';
}
```

### 3. Routing Structure

```typescript
const routes = [
  {
    path: '/dashboard',
    component: Dashboard,
    exact: true
  },
  {
    path: '/cameras',
    component: Cameras,
    children: [
      { path: '/cameras/live', component: CameraLive },
      { path: '/cameras/management', component: CameraManagement },
      { path: '/cameras/settings', component: CameraSettings },
      { path: '/cameras/add', component: AddCamera }
    ]
  },
  {
    path: '/analytics',
    component: Analytics,
    children: [
      { path: '/analytics/realtime', component: RealTimeAnalytics },
      { path: '/analytics/daily', component: DailyAnalytics },
      { path: '/analytics/weekly', component: WeeklyAnalytics },
      { path: '/analytics/monthly', component: MonthlyAnalytics },
      { path: '/analytics/custom', component: CustomAnalytics },
      { path: '/analytics/people-count', component: PeopleCountReport },
      { path: '/analytics/peak-hours', component: PeakHoursReport },
      { path: '/analytics/export', component: ExportReports }
    ]
  },
  {
    path: '/alerts',
    component: Alerts,
    children: [
      { path: '/alerts/notifications', component: Notifications },
      { path: '/alerts/history', component: AlertHistory }
    ]
  },
  {
    path: '/settings',
    component: Settings,
    children: [
      { path: '/settings/profile', component: Profile },
      { path: '/settings/system', component: SystemSettings },
      { path: '/settings/detection', component: DetectionSettings },
      { path: '/settings/billing', component: Billing }
    ]
  }
];
```

## Backend Architecture

### 1. Service Structure

```
Backend/
├── main.py                 # FastAPI application
├── config/
│   ├── settings.py        # Configuration
│   └── database.py        # Database connection
├── models/
│   ├── user.py           # User model
│   ├── camera.py         # Camera model
│   ├── analytics.py      # Analytics model
│   └── alert.py          # Alert model
├── services/
│   ├── camera_service.py # Camera processing
│   ├── ai_service.py     # AI detection
│   ├── analytics_service.py # Analytics processing
│   └── websocket_service.py # WebSocket handling
├── routers/
│   ├── auth.py           # Authentication routes
│   ├── cameras.py        # Camera routes
│   ├── analytics.py      # Analytics routes
│   └── alerts.py         # Alert routes
└── utils/
    ├── ai_models.py      # AI model loading
    ├── image_processing.py # Image processing
    └── validators.py     # Data validation
```

### 2. AI Processing Pipeline

```
Camera Stream → Frame Capture → Preprocessing → SSD Detection → 
Person Tracking → Entry/Exit Detection → Count Update → 
Database Storage → WebSocket Broadcast → Frontend Update
```

### 3. Database Schema

```sql
-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Cameras table
CREATE TABLE cameras (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    location VARCHAR(200),
    stream_url VARCHAR(500) NOT NULL,
    status VARCHAR(20) DEFAULT 'offline',
    settings JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Count data table
CREATE TABLE count_data (
    id SERIAL PRIMARY KEY,
    camera_id INTEGER REFERENCES cameras(id),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    people_in INTEGER DEFAULT 0,
    people_out INTEGER DEFAULT 0,
    current_count INTEGER DEFAULT 0,
    confidence FLOAT
);

-- Alerts table
CREATE TABLE alerts (
    id SERIAL PRIMARY KEY,
    type VARCHAR(50) NOT NULL,
    severity VARCHAR(20) NOT NULL,
    title VARCHAR(200) NOT NULL,
    message TEXT,
    camera_id INTEGER REFERENCES cameras(id),
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Real-time Communication

### 1. WebSocket Events

```typescript
// Client to Server
interface ClientEvents {
  'subscribe:camera': (cameraId: string) => void;
  'subscribe:analytics': () => void;
  'unsubscribe:camera': (cameraId: string) => void;
  'unsubscribe:analytics': () => void;
}

// Server to Client
interface ServerEvents {
  'camera:frame': (data: FrameData) => void;
  'camera:count': (data: CountData) => void;
  'camera:alert': (data: AlertData) => void;
  'analytics:update': (data: AnalyticsData) => void;
  'system:status': (data: SystemStatus) => void;
}
```

### 2. Data Flow

```
1. Camera captures frame
2. Backend processes frame with AI
3. Detection results sent to database
4. WebSocket broadcasts update
5. Frontend receives update
6. UI updates in real-time
```

## Security Architecture

### 1. Authentication
- JWT token-based authentication
- Token refresh mechanism
- Role-based access control

### 2. Authorization
- Route-level protection
- Component-level permissions
- API endpoint security

### 3. Data Protection
- HTTPS encryption
- Input validation
- SQL injection prevention
- XSS protection

## Performance Optimization

### 1. Frontend
- React.memo for component optimization
- Lazy loading for routes
- Image compression and optimization
- Caching strategies

### 2. Backend
- Async/await for I/O operations
- Database connection pooling
- Caching with Redis
- Load balancing

### 3. Real-time
- WebSocket connection pooling
- Message queuing
- Efficient data serialization

## Deployment Architecture

### 1. Development
- Local development with hot reload
- Docker containers for services
- Environment-specific configurations

### 2. Production
- Nginx reverse proxy
- Docker containers orchestration
- Database clustering
- Monitoring and logging

## Monitoring and Logging

### 1. Application Monitoring
- Performance metrics
- Error tracking
- User analytics
- System health checks

### 2. Logging
- Structured logging
- Log aggregation
- Error reporting
- Audit trails 