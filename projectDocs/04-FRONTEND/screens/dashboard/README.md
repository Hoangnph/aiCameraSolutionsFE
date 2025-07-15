# Dashboard Screen Documentation

## Overview
Dashboard screen serves as the main control center for the AI Camera Counting System, providing real-time monitoring, analytics, and quick access to key system features.

## Screen Requirements

### Functional Requirements
- Real-time camera status overview
- Live people counting statistics
- System health monitoring
- Quick access to camera management
- Alert notifications display
- Performance metrics visualization
- User activity summary
- System configuration shortcuts

### Non-Functional Requirements
- Real-time updates: < 1 second latency
- Responsive design: Mobile-first approach
- Performance: < 3 seconds initial load
- Accessibility: WCAG 2.1 AA compliance
- Cross-browser compatibility
- Offline capability for cached data

## Design Specifications

### Layout Structure
```
┌─────────────────────────────────────────────────────────────┐
│ Header (Logo, User Menu, Notifications)                    │
├─────────────────────────────────────────────────────────────┤
│ Sidebar Navigation                                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐          │
│  │ Total Cameras│ │ Active Cameras│ │ Total Count │          │
│  │     [Icon]   │ │     [Icon]   │ │    [Icon]   │          │
│  │     Count    │ │     Count    │ │    Count    │          │
│  └─────────────┘ └─────────────┘ └─────────────┘          │
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                    Live Feed Grid                       │ │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐      │ │
│  │  │ Camera 1│ │ Camera 2│ │ Camera 3│ │ Camera 4│      │ │
│  │  │ [Stream]│ │ [Stream]│ │ [Stream]│ │ [Stream]│      │ │
│  │  │ Count: X│ │ Count: Y│ │ Count: Z│ │ Count: W│      │ │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘      │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌─────────────────────┐ ┌─────────────────────────────────┐ │
│  │   Recent Alerts     │ │        Analytics Chart          │ │
│  │ ┌─────────────────┐ │ │ ┌─────────────────────────────┐ │ │
│  │ │ Alert 1         │ │ │ │                             │ │ │
│  │ │ Alert 2         │ │ │ │     [Chart Component]       │ │ │
│  │ │ Alert 3         │ │ │ │                             │ │ │
│  │ └─────────────────┘ │ │ └─────────────────────────────┘ │ │
│  └─────────────────────┘ └─────────────────────────────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Visual Design
- **Color Scheme**: 
  - Primary: #1976d2 (Blue)
  - Success: #2e7d32 (Green)
  - Warning: #ed6c02 (Orange)
  - Error: #d32f2f (Red)
  - Neutral: #757575 (Gray)
- **Typography**: Roboto font family with hierarchy
- **Spacing**: 16px base unit, consistent grid system
- **Shadows**: Material Design elevation (0-24px)
- **Animations**: Smooth transitions (200-300ms)

### Responsive Breakpoints
- **Mobile**: < 768px - Single column, stacked cards
- **Tablet**: 768px - 1024px - 2-column grid
- **Desktop**: > 1024px - 3-4 column grid
- **Large Desktop**: > 1440px - Expanded layout

## Components

### Core Components
1. **DashboardContainer** - Main wrapper with grid layout
2. **StatsCards** - Key metrics display cards
3. **LiveFeedGrid** - Real-time camera streams
4. **AnalyticsChart** - Data visualization component
5. **AlertPanel** - Recent alerts and notifications
6. **QuickActions** - Shortcut buttons for common tasks
7. **SystemHealth** - System status indicators
8. **UserActivity** - Recent user actions summary

### Data Visualization Components
- **LineChart** - Time-series data (people count over time)
- **BarChart** - Comparative data (camera performance)
- **PieChart** - Distribution data (camera status)
- **GaugeChart** - System health indicators
- **HeatMap** - Activity patterns
- **DataTable** - Detailed statistics

### Interactive Components
- **CameraCard** - Individual camera status card
- **AlertItem** - Individual alert notification
- **MetricCard** - Individual statistic card
- **ChartTooltip** - Interactive chart tooltips
- **FilterPanel** - Data filtering controls
- **RefreshButton** - Manual refresh trigger

## Data Management

### Real-Time Data Sources
```typescript
interface DashboardData {
  cameras: CameraStatus[];
  statistics: SystemStats;
  alerts: Alert[];
  analytics: AnalyticsData;
  systemHealth: HealthStatus;
  userActivity: UserActivity[];
}

interface CameraStatus {
  id: string;
  name: string;
  status: 'online' | 'offline' | 'error';
  currentCount: number;
  totalCount: number;
  lastUpdate: Date;
  streamUrl: string;
  location: string;
}

interface SystemStats {
  totalCameras: number;
  activeCameras: number;
  totalCount: number;
  todayCount: number;
  weeklyCount: number;
  monthlyCount: number;
}
```

### WebSocket Integration
```typescript
interface WebSocketMessage {
  type: 'camera_update' | 'alert' | 'stats_update' | 'system_health';
  data: any;
  timestamp: Date;
}

// WebSocket event handlers
const handleCameraUpdate = (data: CameraStatus) => {
  updateCameraStatus(data);
  updateStatistics();
};

const handleAlert = (data: Alert) => {
  addAlert(data);
  showNotification(data);
};
```

### Data Fetching Strategy
```typescript
// Initial data load
const fetchDashboardData = async () => {
  const [cameras, stats, alerts, analytics] = await Promise.all([
    fetchCameras(),
    fetchStatistics(),
    fetchAlerts(),
    fetchAnalytics()
  ]);
  
  return { cameras, stats, alerts, analytics };
};

// Real-time updates via WebSocket
const setupWebSocket = () => {
  const ws = new WebSocket(WS_URL);
  
  ws.onmessage = (event) => {
    const message: WebSocketMessage = JSON.parse(event.data);
    handleWebSocketMessage(message);
  };
};
```

## State Management

### Local State
```typescript
interface DashboardState {
  cameras: CameraStatus[];
  statistics: SystemStats;
  alerts: Alert[];
  analytics: AnalyticsData;
  isLoading: boolean;
  error: string | null;
  filters: DashboardFilters;
  refreshInterval: number;
  selectedTimeRange: TimeRange;
}

interface DashboardFilters {
  cameraIds: string[];
  alertTypes: AlertType[];
  dateRange: DateRange;
  status: CameraStatus[];
}
```

### Global State (Context)
```typescript
interface DashboardContext {
  data: DashboardData;
  refreshData: () => Promise<void>;
  updateFilters: (filters: DashboardFilters) => void;
  setRefreshInterval: (interval: number) => void;
  markAlertAsRead: (alertId: string) => void;
  getCameraById: (id: string) => CameraStatus | undefined;
}
```

## Performance Optimization

### Data Loading Strategy
- **Initial Load**: Critical data first, then secondary data
- **Lazy Loading**: Non-critical components loaded on demand
- **Caching**: Cache frequently accessed data
- **Pagination**: Large datasets paginated

### Real-Time Updates
- **Throttling**: Limit update frequency to prevent UI lag
- **Batching**: Group multiple updates together
- **Priority Queue**: High-priority updates first
- **Connection Management**: Auto-reconnect on disconnect

### Rendering Optimization
- **Virtual Scrolling**: For large lists
- **Memoization**: Prevent unnecessary re-renders
- **Code Splitting**: Lazy load components
- **Image Optimization**: Compress and cache images

## Analytics & Metrics

### Key Performance Indicators (KPIs)
1. **System Uptime**: Percentage of time system is operational
2. **Camera Availability**: Number of active cameras
3. **Detection Accuracy**: Accuracy of people counting
4. **Response Time**: Time to detect and count people
5. **Alert Response**: Time to acknowledge alerts

### Data Visualization Types
- **Time Series**: People count over time
- **Comparative**: Camera performance comparison
- **Distribution**: Camera status distribution
- **Correlation**: Traffic patterns vs. time
- **Trend Analysis**: Long-term patterns

### Chart Configuration
```typescript
interface ChartConfig {
  type: 'line' | 'bar' | 'pie' | 'gauge';
  data: ChartData;
  options: ChartOptions;
  responsive: boolean;
  animation: boolean;
}

interface ChartData {
  labels: string[];
  datasets: Dataset[];
}

interface Dataset {
  label: string;
  data: number[];
  backgroundColor?: string;
  borderColor?: string;
  fill?: boolean;
}
```

## Alert System

### Alert Types
```typescript
enum AlertType {
  CAMERA_OFFLINE = 'camera_offline',
  HIGH_TRAFFIC = 'high_traffic',
  SYSTEM_ERROR = 'system_error',
  MAINTENANCE = 'maintenance',
  SECURITY = 'security'
}

interface Alert {
  id: string;
  type: AlertType;
  title: string;
  message: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  timestamp: Date;
  cameraId?: string;
  isRead: boolean;
  actions?: AlertAction[];
}
```

### Alert Management
- **Real-time Notifications**: Push notifications for critical alerts
- **Alert History**: Persistent storage of all alerts
- **Alert Acknowledgment**: Mark alerts as read
- **Alert Filtering**: Filter by type, severity, camera
- **Alert Escalation**: Automatic escalation for unacknowledged alerts

## Accessibility Features

### Keyboard Navigation
- Tab navigation through all interactive elements
- Arrow keys for chart navigation
- Enter/Space for button activation
- Escape key for modal dismissal

### Screen Reader Support
- Descriptive labels for all charts and data
- Status announcements for real-time updates
- Alert announcements with priority
- Chart data descriptions

### Visual Accessibility
- High contrast mode support
- Color-blind friendly color schemes
- Focus indicators for all interactive elements
- Loading state indicators

## Testing Strategy

### Unit Tests
- Component rendering and interactions
- Data transformation functions
- State management logic
- Utility functions

### Integration Tests
- API integration
- WebSocket connection
- Real-time data updates
- Chart interactions

### E2E Tests
- Complete dashboard workflow
- Real-time updates
- Alert handling
- Responsive design

### Performance Tests
- Load time testing
- Memory usage monitoring
- WebSocket performance
- Chart rendering performance

## Implementation Checklist

### Phase 1: Core Structure
- [ ] Create DashboardContainer component
- [ ] Implement responsive grid layout
- [ ] Set up routing and navigation
- [ ] Create basic card components

### Phase 2: Data Integration
- [ ] Implement API data fetching
- [ ] Set up WebSocket connection
- [ ] Create data transformation utilities
- [ ] Implement error handling

### Phase 3: Visualization
- [ ] Implement chart components
- [ ] Create real-time data updates
- [ ] Add interactive features
- [ ] Implement filtering system

### Phase 4: Real-Time Features
- [ ] Add WebSocket integration
- [ ] Implement alert system
- [ ] Create notification system
- [ ] Add auto-refresh functionality

### Phase 5: Polish & Testing
- [ ] Add animations and transitions
- [ ] Implement accessibility features
- [ ] Write comprehensive tests
- [ ] Performance optimization

## Dependencies

### Required Packages
```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-router-dom": "^6.8.0",
    "axios": "^1.3.0",
    "react-query": "^3.39.0",
    "chart.js": "^4.2.0",
    "react-chartjs-2": "^5.2.0",
    "@mui/material": "^5.11.0",
    "@mui/icons-material": "^5.11.0",
    "socket.io-client": "^4.6.0",
    "date-fns": "^2.29.0"
  },
  "devDependencies": {
    "@testing-library/react": "^13.4.0",
    "@testing-library/jest-dom": "^5.16.5",
    "jest": "^29.4.0",
    "cypress": "^12.0.0"
  }
}
```

## File Structure
```
screens/dashboard/
├── README.md
├── index.tsx
├── components/
│   ├── DashboardContainer.tsx
│   ├── StatsCards.tsx
│   ├── LiveFeedGrid.tsx
│   ├── AnalyticsChart.tsx
│   ├── AlertPanel.tsx
│   ├── QuickActions.tsx
│   ├── SystemHealth.tsx
│   └── UserActivity.tsx
├── charts/
│   ├── LineChart.tsx
│   ├── BarChart.tsx
│   ├── PieChart.tsx
│   ├── GaugeChart.tsx
│   └── HeatMap.tsx
├── hooks/
│   ├── useDashboardData.ts
│   ├── useWebSocket.ts
│   └── useRealTimeUpdates.ts
├── utils/
│   ├── dataTransformers.ts
│   ├── chartHelpers.ts
│   └── alertHelpers.ts
├── types/
│   └── dashboard.types.ts
├── styles/
│   └── dashboard.styles.ts
└── tests/
    ├── DashboardContainer.test.tsx
    ├── StatsCards.test.tsx
    └── AnalyticsChart.test.tsx
```

## Status Tracking

### Development Status: 🟡 In Progress
- **Started**: [Date]
- **Estimated Completion**: [Date]
- **Current Phase**: Phase 1 - Core Structure
- **Next Milestone**: Data Integration

### Review Status
- **Design Review**: ⏳ Pending
- **Code Review**: ⏳ Pending
- **QA Testing**: ⏳ Pending
- **Performance Review**: ⏳ Pending

### Dependencies
- **Backend API**: ✅ Ready
- **WebSocket Service**: ✅ Ready
- **Chart Library**: ✅ Ready
- **Design System**: ✅ Ready 