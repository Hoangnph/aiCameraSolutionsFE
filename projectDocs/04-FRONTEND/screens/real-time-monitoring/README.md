# Real-time Monitoring Screen Documentation

## Overview
Real-time Monitoring screen provides live monitoring capabilities for the AI Camera Counting System, displaying live camera feeds, real-time people counting, and instant alert notifications.

## Screen Requirements

### Functional Requirements
- Live camera stream display
- Real-time people counting updates
- Multi-camera grid layout
- Alert notifications and management
- Camera status monitoring
- Live chat/communication
- Recording controls
- Emergency response tools
- Performance metrics display
- Mobile monitoring support

### Non-Functional Requirements
- Stream latency: < 500ms
- Update frequency: Real-time (WebSocket)
- Responsive design: Mobile-first approach
- Accessibility: WCAG 2.1 AA compliance
- Cross-browser compatibility
- Offline capability for cached data

## Design Specifications

### Layout Structure
```
┌─────────────────────────────────────────────────────────────┐
│ Header (Title, Time, Alert Count, Emergency Button)        │
├─────────────────────────────────────────────────────────────┤
│ Control Bar (View Mode, Camera Selection, Recording)       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                    Live Stream Grid                     │ │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐      │ │
│  │  │ Camera 1    │ │ Camera 2    │ │ Camera 3    │      │ │
│  │  │ [Live Feed] │ │ [Live Feed] │ │ [Live Feed] │      │ │
│  │  │ Count: 15   │ │ Count: 8    │ │ Count: 23   │      │ │
│  │  │ Status: OK  │ │ Status: OK  │ │ Alert: High │      │ │
│  │  │ [Controls]  │ │ [Controls]  │ │ [Controls]  │      │ │
│  │  └─────────────┘ └─────────────┘ └─────────────┘      │ │
│  │                                                         │ │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐      │ │
│  │  │ Camera 4    │ │ Camera 5    │ │ Camera 6    │      │ │
│  │  │ [Live Feed] │ │ [Live Feed] │ │ [Live Feed] │      │ │
│  │  │ Count: 12   │ │ Count: 19   │ │ Count: 5    │      │ │
│  │  │ Status: OK  │ │ Status: OK  │ │ Status: OK  │      │ │
│  │  │ [Controls]  │ │ [Controls]  │ │ [Controls]  │      │ │
│  │  └─────────────┘ └─────────────┘ └─────────────┘      │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌─────────────────────┐ ┌─────────────────────────────────┐ │
│  │   Live Alerts       │ │        Performance Panel        │ │
│  │ ┌─────────────────┐ │ │ ┌─────────────────────────────┐ │ │
│  │ │ Alert 1 - High  │ │ │ │ System Uptime: 99.8%        │ │ │
│  │ │ Camera 3        │ │ │ │ Active Cameras: 6/6         │ │ │
│  │ │ Count: 45       │ │ │ │ Total Count: 82             │ │ │
│  │ └─────────────────┘ │ │ │ Response Time: 120ms        │ │ │
│  │ ┌─────────────────┐ │ │ └─────────────────────────────┘ │ │
│  │ │ Alert 2 - Med   │ │ │                                 │ │
│  │ │ Camera 5        │ │ │  ┌─────────────────────────────┐ │ │
│  │ │ Count: 32       │ │ │  │     Live Chat Panel         │ │ │
│  │ └─────────────────┘ │ │ │  │ [Chat Messages]            │ │ │
│  └─────────────────────┘ │ │  └─────────────────────────────┘ │
│                          └─────────────────────────────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Visual Design
- **Color Scheme**: 
  - Primary: #1976d2 (Blue)
  - Success: #2e7d32 (Green)
  - Warning: #ed6c02 (Orange)
  - Error: #d32f2f (Red)
  - Alert: #f57c00 (Deep Orange)
  - Neutral: #757575 (Gray)
- **Typography**: Roboto font family
- **Spacing**: 16px base unit, consistent grid
- **Shadows**: Material Design elevation levels
- **Animations**: Smooth transitions (200-300ms)

### Responsive Breakpoints
- **Mobile**: < 768px - Single camera view, stacked layout
- **Tablet**: 768px - 1024px - 2x2 grid layout
- **Desktop**: > 1024px - 3x2 grid layout
- **Large Desktop**: > 1440px - 4x2 grid layout

## Components

### Core Components
1. **MonitoringContainer** - Main wrapper with layout
2. **LiveStreamGrid** - Grid layout for camera feeds
3. **CameraFeed** - Individual camera stream component
4. **AlertPanel** - Real-time alert notifications
5. **PerformancePanel** - System performance metrics
6. **ControlBar** - Monitoring controls and settings
7. **EmergencyPanel** - Emergency response tools
8. **ChatPanel** - Live communication system

### Stream Components
- **VideoPlayer** - Live video stream player
- **StreamControls** - Play, pause, fullscreen controls
- **StreamInfo** - Stream metadata and status
- **RecordingControls** - Start/stop recording
- **QualitySelector** - Stream quality options

### Interactive Components
- **AlertItem** - Individual alert notification
- **StatusIndicator** - Camera status with color coding
- **CountDisplay** - Real-time people count
- **EmergencyButton** - Emergency response trigger
- **ChatMessage** - Individual chat message
- **ControlButton** - Camera control buttons

## Data Management

### Real-Time Data Structure
```typescript
interface MonitoringData {
  cameras: CameraFeed[];
  alerts: LiveAlert[];
  performance: PerformanceMetrics;
  chat: ChatMessage[];
  systemStatus: SystemStatus;
}

interface CameraFeed {
  id: string;
  name: string;
  streamUrl: string;
  status: 'online' | 'offline' | 'error';
  currentCount: number;
  totalCount: number;
  lastUpdate: Date;
  location: string;
  recording: boolean;
  quality: 'low' | 'medium' | 'high';
  metadata: StreamMetadata;
}

interface LiveAlert {
  id: string;
  type: AlertType;
  severity: 'low' | 'medium' | 'high' | 'critical';
  cameraId: string;
  cameraName: string;
  message: string;
  count: number;
  threshold: number;
  timestamp: Date;
  acknowledged: boolean;
  acknowledgedBy?: string;
  acknowledgedAt?: Date;
}

interface PerformanceMetrics {
  systemUptime: number;
  activeCameras: number;
  totalCameras: number;
  totalCount: number;
  averageResponseTime: number;
  errorRate: number;
  bandwidthUsage: number;
  cpuUsage: number;
  memoryUsage: number;
}

interface ChatMessage {
  id: string;
  sender: string;
  message: string;
  timestamp: Date;
  type: 'system' | 'user' | 'alert';
  priority: 'low' | 'medium' | 'high';
}
```

### WebSocket Integration
```typescript
interface WebSocketMessage {
  type: 'stream_update' | 'alert' | 'chat' | 'performance' | 'emergency';
  data: any;
  timestamp: Date;
  cameraId?: string;
}

// WebSocket event handlers
const handleStreamUpdate = (data: StreamUpdate) => {
  updateCameraFeed(data.cameraId, data);
  updatePerformanceMetrics(data.performance);
};

const handleAlert = (data: LiveAlert) => {
  addAlert(data);
  showNotification(data);
  updateChat(data);
};

const handleEmergency = (data: EmergencyEvent) => {
  triggerEmergencyResponse(data);
  notifyAllUsers(data);
  logEmergencyEvent(data);
};
```

### State Management
```typescript
interface MonitoringState {
  cameras: CameraFeed[];
  alerts: LiveAlert[];
  performance: PerformanceMetrics;
  chat: ChatMessage[];
  selectedCameras: string[];
  viewMode: 'grid' | 'single' | 'fullscreen';
  recordingState: Record<string, boolean>;
  alertFilters: AlertFilters;
  chatEnabled: boolean;
  emergencyMode: boolean;
}

interface AlertFilters {
  severity: AlertSeverity[];
  cameras: string[];
  acknowledged: boolean;
  timeRange: TimeRange;
}
```

## Live Streaming

### Stream Configuration
```typescript
interface StreamConfig {
  url: string;
  protocol: 'rtsp' | 'rtmp' | 'webrtc' | 'hls';
  quality: 'low' | 'medium' | 'high';
  fps: number;
  resolution: string;
  bitrate: number;
  codec: 'h264' | 'h265' | 'vp8' | 'vp9';
}

// Stream player component
const VideoPlayer: React.FC<VideoPlayerProps> = ({
  streamUrl,
  quality,
  onCountUpdate,
  onError,
  controls = true
}) => {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);

  useEffect(() => {
    if (videoRef.current) {
      const video = videoRef.current;
      
      // Set up video event listeners
      video.addEventListener('play', () => setIsPlaying(true));
      video.addEventListener('pause', () => setIsPlaying(false));
      video.addEventListener('timeupdate', () => setCurrentTime(video.currentTime));
      video.addEventListener('loadedmetadata', () => setDuration(video.duration));
      
      // Start streaming
      video.src = streamUrl;
      video.play().catch(onError);
    }
  }, [streamUrl]);

  return (
    <div className="video-player">
      <video
        ref={videoRef}
        controls={controls}
        autoPlay
        muted
        playsInline
        className="stream-video"
      />
      <StreamControls
        isPlaying={isPlaying}
        currentTime={currentTime}
        duration={duration}
        onPlayPause={() => videoRef.current?.paused ? videoRef.current.play() : videoRef.current?.pause()}
        onFullscreen={() => videoRef.current?.requestFullscreen()}
      />
    </div>
  );
};
```

### Stream Quality Management
- **Adaptive Bitrate**: Automatic quality adjustment
- **Bandwidth Monitoring**: Real-time bandwidth usage
- **Quality Selection**: Manual quality control
- **Fallback Streams**: Backup stream sources
- **Error Recovery**: Automatic reconnection

## Alert Management

### Alert Types
```typescript
enum AlertType {
  HIGH_COUNT = 'high_count',
  CAMERA_OFFLINE = 'camera_offline',
  SYSTEM_ERROR = 'system_error',
  SECURITY_BREACH = 'security_breach',
  MAINTENANCE = 'maintenance',
  EMERGENCY = 'emergency'
}

interface AlertAction {
  id: string;
  label: string;
  action: () => void;
  type: 'primary' | 'secondary' | 'danger';
}
```

### Alert Processing
```typescript
const processAlert = (alert: LiveAlert) => {
  // Add to alert list
  addAlert(alert);
  
  // Show notification
  showNotification({
    title: alert.type,
    message: alert.message,
    severity: alert.severity,
    action: () => focusCamera(alert.cameraId)
  });
  
  // Update chat
  addChatMessage({
    id: generateId(),
    sender: 'System',
    message: `Alert: ${alert.message}`,
    timestamp: new Date(),
    type: 'alert',
    priority: alert.severity
  });
  
  // Trigger emergency if critical
  if (alert.severity === 'critical') {
    triggerEmergencyProtocol(alert);
  }
};
```

### Alert Acknowledgment
```typescript
const acknowledgeAlert = async (alertId: string, userId: string) => {
  const response = await api.put(`/alerts/${alertId}/acknowledge`, {
    acknowledgedBy: userId,
    acknowledgedAt: new Date()
  });
  
  updateAlert(alertId, response.data);
  addChatMessage({
    id: generateId(),
    sender: getUserName(userId),
    message: `Acknowledged alert: ${getAlertById(alertId).message}`,
    timestamp: new Date(),
    type: 'user',
    priority: 'medium'
  });
};
```

## Emergency Response

### Emergency Protocols
```typescript
interface EmergencyProtocol {
  id: string;
  name: string;
  triggers: AlertType[];
  actions: EmergencyAction[];
  escalation: EscalationLevel;
}

interface EmergencyAction {
  type: 'notification' | 'recording' | 'lockdown' | 'evacuation' | 'police';
  target: string[];
  message: string;
  delay: number;
}

const triggerEmergencyProtocol = (alert: LiveAlert) => {
  const protocol = getEmergencyProtocol(alert.type);
  
  // Execute emergency actions
  protocol.actions.forEach(action => {
    setTimeout(() => {
      executeEmergencyAction(action, alert);
    }, action.delay);
  });
  
  // Notify all users
  notifyAllUsers({
    type: 'emergency',
    message: `Emergency: ${alert.message}`,
    priority: 'critical'
  });
  
  // Start emergency recording
  startEmergencyRecording(alert.cameraId);
};
```

### Emergency Controls
- **Emergency Button**: One-click emergency trigger
- **Lockdown Controls**: System lockdown functionality
- **Evacuation Alerts**: Mass notification system
- **Police Contact**: Direct emergency services contact
- **Recording Controls**: Emergency recording management

## Performance Monitoring

### Real-Time Metrics
```typescript
const usePerformanceMonitoring = () => {
  const [metrics, setMetrics] = useState<PerformanceMetrics | null>(null);
  
  useEffect(() => {
    const interval = setInterval(async () => {
      const response = await api.get('/monitoring/performance');
      setMetrics(response.data);
    }, 5000); // Update every 5 seconds
    
    return () => clearInterval(interval);
  }, []);
  
  return metrics;
};

// Performance display component
const PerformancePanel: React.FC = () => {
  const metrics = usePerformanceMonitoring();
  
  if (!metrics) return <div>Loading...</div>;
  
  return (
    <div className="performance-panel">
      <div className="metric">
        <span className="label">System Uptime</span>
        <span className="value">{metrics.systemUptime}%</span>
      </div>
      <div className="metric">
        <span className="label">Active Cameras</span>
        <span className="value">{metrics.activeCameras}/{metrics.totalCameras}</span>
      </div>
      <div className="metric">
        <span className="label">Total Count</span>
        <span className="value">{metrics.totalCount}</span>
      </div>
      <div className="metric">
        <span className="label">Response Time</span>
        <span className="value">{metrics.averageResponseTime}ms</span>
      </div>
    </div>
  );
};
```

## Live Communication

### Chat System
```typescript
interface ChatSystem {
  messages: ChatMessage[];
  users: ChatUser[];
  sendMessage: (message: string) => void;
  acknowledgeAlert: (alertId: string) => void;
}

const useChatSystem = (): ChatSystem => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [users, setUsers] = useState<ChatUser[]>([]);
  
  const sendMessage = (message: string) => {
    const newMessage: ChatMessage = {
      id: generateId(),
      sender: getCurrentUser().name,
      message,
      timestamp: new Date(),
      type: 'user',
      priority: 'medium'
    };
    
    setMessages(prev => [...prev, newMessage]);
    broadcastMessage(newMessage);
  };
  
  return { messages, users, sendMessage, acknowledgeAlert };
};
```

### Communication Features
- **Real-time Chat**: Live messaging between users
- **Alert Integration**: Automatic alert notifications
- **User Presence**: Show online users
- **Message History**: Persistent chat history
- **File Sharing**: Share images and documents

## Mobile Monitoring

### Mobile Optimization
```typescript
const useMobileMonitoring = () => {
  const [isMobile, setIsMobile] = useState(false);
  const [orientation, setOrientation] = useState<'portrait' | 'landscape'>('portrait');
  
  useEffect(() => {
    const checkMobile = () => {
      setIsMobile(window.innerWidth < 768);
      setOrientation(window.innerWidth > window.innerHeight ? 'landscape' : 'portrait');
    };
    
    checkMobile();
    window.addEventListener('resize', checkMobile);
    return () => window.removeEventListener('resize', checkMobile);
  }, []);
  
  return { isMobile, orientation };
};
```

### Mobile Features
- **Touch Controls**: Touch-friendly interface
- **Gesture Support**: Swipe and pinch gestures
- **Offline Mode**: Cached data when offline
- **Push Notifications**: Mobile push alerts
- **Battery Optimization**: Power-efficient monitoring

## Testing Strategy

### Unit Tests
- Component rendering and interactions
- Stream player functionality
- Alert processing logic
- Chat system operations

### Integration Tests
- WebSocket connection
- Real-time data updates
- Alert system integration
- Emergency protocols

### E2E Tests
- Complete monitoring workflow
- Emergency response procedures
- Mobile monitoring experience
- Multi-user scenarios

### Performance Tests
- Stream performance testing
- Real-time update performance
- Mobile performance testing
- Emergency response times

## Implementation Checklist

### Phase 1: Core Structure
- [ ] Create MonitoringContainer component
- [ ] Implement live stream grid layout
- [ ] Set up WebSocket connection
- [ ] Create basic camera feed components

### Phase 2: Streaming
- [ ] Implement video player component
- [ ] Add stream quality controls
- [ ] Create recording functionality
- [ ] Add stream error handling

### Phase 3: Alert System
- [ ] Implement alert processing
- [ ] Create alert notification system
- [ ] Add alert acknowledgment
- [ ] Implement emergency protocols

### Phase 4: Communication
- [ ] Add live chat system
- [ ] Implement user presence
- [ ] Create emergency controls
- [ ] Add performance monitoring

### Phase 5: Polish and Testing
- [ ] Add mobile optimization
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
    "socket.io-client": "^4.6.0",
    "hls.js": "^1.4.0",
    "webrtc-adapter": "^8.2.0",
    "@mui/material": "^5.11.0",
    "@mui/icons-material": "^5.11.0",
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
screens/real-time-monitoring/
├── README.md
├── index.tsx
├── components/
│   ├── MonitoringContainer.tsx
│   ├── LiveStreamGrid.tsx
│   ├── CameraFeed.tsx
│   ├── AlertPanel.tsx
│   ├── PerformancePanel.tsx
│   ├── ControlBar.tsx
│   ├── EmergencyPanel.tsx
│   └── ChatPanel.tsx
├── streaming/
│   ├── VideoPlayer.tsx
│   ├── StreamControls.tsx
│   ├── StreamInfo.tsx
│   ├── RecordingControls.tsx
│   └── QualitySelector.tsx
├── alerts/
│   ├── AlertItem.tsx
│   ├── AlertProcessor.tsx
│   ├── EmergencyProtocol.tsx
│   └── AlertActions.tsx
├── chat/
│   ├── ChatMessage.tsx
│   ├── ChatInput.tsx
│   ├── UserList.tsx
│   └── ChatHistory.tsx
├── hooks/
│   ├── useMonitoringData.ts
│   ├── useWebSocket.ts
│   ├── useStreaming.ts
│   └── useEmergency.ts
├── utils/
│   ├── streamHelpers.ts
│   ├── alertHelpers.ts
│   ├── emergencyHelpers.ts
│   └── chatHelpers.ts
├── types/
│   └── monitoring.types.ts
├── styles/
│   └── monitoring.styles.ts
└── tests/
    ├── MonitoringContainer.test.tsx
    ├── VideoPlayer.test.tsx
    └── AlertPanel.test.tsx
```

## Status Tracking

### Development Status: 🟡 In Progress
- **Started**: [Date]
- **Estimated Completion**: [Date]
- **Current Phase**: Phase 1 - Core Structure
- **Next Milestone**: Streaming Implementation

### Review Status
- **Design Review**: ⏳ Pending
- **Code Review**: ⏳ Pending
- **QA Testing**: ⏳ Pending
- **Performance Review**: ⏳ Pending

### Dependencies
- **Backend API**: ✅ Ready
- **WebSocket Service**: ✅ Ready
- **Streaming Service**: ✅ Ready
- **Design System**: ✅ Ready 