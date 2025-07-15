# Camera Management Screen Documentation

## Overview
Camera Management screen provides comprehensive control over all cameras in the AI Camera Counting System, including camera configuration, status monitoring, and administrative functions.

## Screen Requirements

### Functional Requirements
- Camera listing with search and filtering
- Add new camera with configuration
- Edit existing camera settings
- Delete camera with confirmation
- Camera status monitoring
- Camera stream preview
- Configuration management
- Bulk operations (enable/disable multiple cameras)
- Camera grouping and organization
- Permission-based access control

### Non-Functional Requirements
- Response time: < 2 seconds for CRUD operations
- Real-time status updates
- Responsive design for all devices
- Accessibility: WCAG 2.1 AA compliance
- Offline capability for viewing cached data
- Secure data transmission

## Design Specifications

### Layout Structure
```
┌─────────────────────────────────────────────────────────────┐
│ Header (Title, Add Camera Button, Search)                  │
├─────────────────────────────────────────────────────────────┤
│ Filter Bar (Status, Location, Type, Date Range)            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                    Camera Grid                          │ │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐      │ │
│  │  │ Camera Card │ │ Camera Card │ │ Camera Card │      │ │
│  │  │ [Preview]   │ │ [Preview]   │ │ [Preview]   │      │ │
│  │  │ Name        │ │ Name        │ │ Name        │      │ │
│  │  │ Status      │ │ Status      │ │ Status      │      │ │
│  │  │ [Actions]   │ │ [Actions]   │ │ [Actions]   │      │ │
│  │  └─────────────┘ └─────────────┘ └─────────────┘      │ │
│  │                                                         │ │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐      │ │
│  │  │ Camera Card │ │ Camera Card │ │ Camera Card │      │ │
│  │  │ [Preview]   │ │ [Preview]   │ │ [Preview]   │      │ │
│  │  │ Name        │ │ Name        │ │ Name        │      │ │
│  │  │ Status      │ │ Status      │ │ Status      │      │ │
│  │  │ [Actions]   │ │ [Actions]   │ │ [Actions]   │      │ │
│  │  └─────────────┘ └─────────────┘ └─────────────┘      │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                    Pagination                           │ │
│  │  [Previous] [1] [2] [3] ... [Next] [Items per page]    │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Visual Design
- **Color Scheme**: 
  - Primary: #1976d2 (Blue)
  - Success: #2e7d32 (Green)
  - Warning: #ed6c02 (Orange)
  - Error: #d32f2f (Red)
  - Offline: #757575 (Gray)
- **Typography**: Roboto font family
- **Spacing**: 16px base unit, consistent grid
- **Shadows**: Material Design elevation levels
- **Animations**: Smooth transitions (200-300ms)

### Responsive Breakpoints
- **Mobile**: < 768px - Single column, stacked cards
- **Tablet**: 768px - 1024px - 2-column grid
- **Desktop**: > 1024px - 3-4 column grid
- **Large Desktop**: > 1440px - 4-5 column grid

## Components

### Core Components
1. **CameraManagementContainer** - Main wrapper with layout
2. **CameraGrid** - Grid layout for camera cards
3. **CameraCard** - Individual camera display card
4. **AddCameraModal** - Modal for adding new camera
5. **EditCameraModal** - Modal for editing camera
6. **CameraPreview** - Live stream preview component
7. **FilterPanel** - Search and filter controls
8. **BulkActions** - Bulk operation controls

### Form Components
- **CameraForm** - Reusable form for add/edit
- **StreamConfigForm** - Stream configuration
- **LocationForm** - Location and positioning
- **ScheduleForm** - Operating schedule
- **AlertConfigForm** - Alert configuration

### Interactive Components
- **StatusIndicator** - Camera status with color coding
- **ActionMenu** - Context menu for camera actions
- **SearchBar** - Real-time search functionality
- **FilterChips** - Active filter display
- **Pagination** - Page navigation controls

## Data Management

### Camera Data Structure
```typescript
interface Camera {
  id: string;
  name: string;
  description?: string;
  location: Location;
  status: CameraStatus;
  configuration: CameraConfig;
  stream: StreamConfig;
  schedule: Schedule;
  alerts: AlertConfig;
  metadata: CameraMetadata;
  createdAt: Date;
  updatedAt: Date;
}

interface Location {
  address: string;
  coordinates: {
    latitude: number;
    longitude: number;
  };
  building?: string;
  floor?: string;
  room?: string;
}

interface CameraConfig {
  resolution: '720p' | '1080p' | '4K';
  fps: number;
  quality: 'low' | 'medium' | 'high';
  recording: boolean;
  motionDetection: boolean;
  nightVision: boolean;
  audio: boolean;
}

interface StreamConfig {
  url: string;
  protocol: 'rtsp' | 'rtmp' | 'http';
  port: number;
  username?: string;
  password?: string;
  encoding: 'h264' | 'h265';
  bitrate: number;
}

interface Schedule {
  enabled: boolean;
  timezone: string;
  operatingHours: {
    start: string;
    end: string;
  };
  daysOfWeek: number[];
  exceptions: ScheduleException[];
}
```

### API Endpoints
```typescript
// Get all cameras
GET /api/cameras
Query params: page, limit, status, location, search

// Get single camera
GET /api/cameras/:id

// Create camera
POST /api/cameras
Body: CameraCreateData

// Update camera
PUT /api/cameras/:id
Body: CameraUpdateData

// Delete camera
DELETE /api/cameras/:id

// Bulk operations
POST /api/cameras/bulk
Body: { action: 'enable' | 'disable' | 'delete', ids: string[] }

// Camera status
GET /api/cameras/:id/status

// Stream configuration
GET /api/cameras/:id/stream
PUT /api/cameras/:id/stream
```

### State Management
```typescript
interface CameraManagementState {
  cameras: Camera[];
  selectedCameras: string[];
  filters: CameraFilters;
  pagination: PaginationState;
  isLoading: boolean;
  error: string | null;
  modalState: {
    isAddOpen: boolean;
    isEditOpen: boolean;
    editingCamera: Camera | null;
  };
}

interface CameraFilters {
  status: CameraStatus[];
  location: string[];
  type: string[];
  dateRange: DateRange;
  search: string;
}

interface PaginationState {
  currentPage: number;
  itemsPerPage: number;
  totalItems: number;
  totalPages: number;
}
```

## CRUD Operations

### Create Camera
```typescript
const createCamera = async (cameraData: CameraCreateData): Promise<Camera> => {
  const response = await api.post('/cameras', cameraData);
  return response.data;
};

interface CameraCreateData {
  name: string;
  description?: string;
  location: Location;
  configuration: CameraConfig;
  stream: StreamConfig;
  schedule: Schedule;
  alerts: AlertConfig;
}
```

### Read Cameras
```typescript
const fetchCameras = async (filters: CameraFilters, pagination: PaginationState) => {
  const params = new URLSearchParams({
    page: pagination.currentPage.toString(),
    limit: pagination.itemsPerPage.toString(),
    ...filters
  });
  
  const response = await api.get(`/cameras?${params}`);
  return response.data;
};
```

### Update Camera
```typescript
const updateCamera = async (id: string, updateData: Partial<Camera>): Promise<Camera> => {
  const response = await api.put(`/cameras/${id}`, updateData);
  return response.data;
};
```

### Delete Camera
```typescript
const deleteCamera = async (id: string): Promise<void> => {
  await api.delete(`/cameras/${id}`);
};
```

## Camera Configuration

### Stream Configuration
- **Protocol Support**: RTSP, RTMP, HTTP
- **Resolution Options**: 720p, 1080p, 4K
- **Frame Rate**: 15, 25, 30 fps
- **Encoding**: H.264, H.265
- **Quality Settings**: Low, Medium, High

### Location Configuration
- **Address Input**: Manual entry with validation
- **GPS Coordinates**: Automatic geocoding
- **Building Information**: Building, floor, room
- **Map Integration**: Visual location selection

### Schedule Configuration
- **Operating Hours**: Start/end time
- **Days of Week**: Selectable days
- **Timezone Support**: Multiple timezone support
- **Exceptions**: Holiday and maintenance schedules

### Alert Configuration
- **Motion Detection**: Sensitivity settings
- **Threshold Alerts**: Count-based alerts
- **Status Alerts**: Offline/error notifications
- **Email/SMS**: Notification delivery

## Search and Filtering

### Search Functionality
```typescript
interface SearchConfig {
  fields: ('name' | 'description' | 'location')[];
  operator: 'contains' | 'startsWith' | 'exact';
  caseSensitive: boolean;
}

const searchCameras = (cameras: Camera[], query: string, config: SearchConfig) => {
  return cameras.filter(camera => {
    return config.fields.some(field => {
      const value = camera[field];
      if (typeof value === 'string') {
        switch (config.operator) {
          case 'contains':
            return value.toLowerCase().includes(query.toLowerCase());
          case 'startsWith':
            return value.toLowerCase().startsWith(query.toLowerCase());
          case 'exact':
            return value.toLowerCase() === query.toLowerCase();
        }
      }
      return false;
    });
  });
};
```

### Filter Options
- **Status**: Online, Offline, Error, Maintenance
- **Location**: By building, floor, area
- **Type**: Indoor, Outdoor, PTZ, Fixed
- **Date Range**: Installation date, last update
- **Configuration**: Resolution, features

## Bulk Operations

### Supported Operations
```typescript
enum BulkOperation {
  ENABLE = 'enable',
  DISABLE = 'disable',
  DELETE = 'delete',
  UPDATE_CONFIG = 'update_config',
  EXPORT = 'export',
  IMPORT = 'import'
}

interface BulkOperationData {
  operation: BulkOperation;
  cameraIds: string[];
  data?: any;
}
```

### Implementation
```typescript
const executeBulkOperation = async (operation: BulkOperationData) => {
  const response = await api.post('/cameras/bulk', operation);
  return response.data;
};

const handleBulkDelete = async (cameraIds: string[]) => {
  const confirmed = await showConfirmationDialog({
    title: 'Delete Cameras',
    message: `Are you sure you want to delete ${cameraIds.length} cameras?`,
    confirmText: 'Delete',
    cancelText: 'Cancel'
  });
  
  if (confirmed) {
    await executeBulkOperation({
      operation: BulkOperation.DELETE,
      cameraIds
    });
  }
};
```

## Real-Time Updates

### WebSocket Integration
```typescript
interface CameraUpdateMessage {
  type: 'status_update' | 'config_update' | 'stream_update';
  cameraId: string;
  data: any;
  timestamp: Date;
}

const handleCameraUpdate = (message: CameraUpdateMessage) => {
  switch (message.type) {
    case 'status_update':
      updateCameraStatus(message.cameraId, message.data);
      break;
    case 'config_update':
      updateCameraConfig(message.cameraId, message.data);
      break;
    case 'stream_update':
      updateStreamInfo(message.cameraId, message.data);
      break;
  }
};
```

### Status Monitoring
- **Heartbeat**: Regular status checks
- **Connection Monitoring**: Stream connectivity
- **Performance Metrics**: FPS, bitrate, quality
- **Error Tracking**: Connection failures, errors

## Security Features

### Access Control
- **Role-based Permissions**: Admin, Operator, Viewer
- **Camera-level Permissions**: Individual camera access
- **Operation Restrictions**: Create, Read, Update, Delete
- **Audit Logging**: All operations logged

### Data Protection
- **Encrypted Storage**: Sensitive data encryption
- **Secure Transmission**: HTTPS for all API calls
- **Token-based Authentication**: JWT tokens
- **Session Management**: Secure session handling

## Performance Optimization

### Data Loading
- **Pagination**: Load cameras in chunks
- **Virtual Scrolling**: For large camera lists
- **Lazy Loading**: Load camera details on demand
- **Caching**: Cache frequently accessed data

### Image Optimization
- **Thumbnail Generation**: Optimized preview images
- **Progressive Loading**: Low-res to high-res
- **Compression**: Efficient image compression
- **CDN Integration**: Fast image delivery

## Testing Strategy

### Unit Tests
- Component rendering and interactions
- Form validation logic
- Data transformation functions
- Utility functions

### Integration Tests
- API integration
- CRUD operations
- Real-time updates
- Bulk operations

### E2E Tests
- Complete camera management workflow
- Add/edit/delete camera flows
- Search and filtering
- Bulk operations

### Performance Tests
- Large dataset handling
- Real-time update performance
- Image loading performance
- API response times

## Implementation Checklist

### Phase 1: Core Structure
- [ ] Create CameraManagementContainer
- [ ] Implement camera grid layout
- [ ] Create CameraCard component
- [ ] Set up routing and navigation

### Phase 2: CRUD Operations
- [ ] Implement camera listing
- [ ] Create add camera modal
- [ ] Create edit camera modal
- [ ] Implement delete functionality

### Phase 3: Search and Filtering
- [ ] Add search functionality
- [ ] Implement filter panel
- [ ] Create filter chips
- [ ] Add pagination

### Phase 4: Advanced Features
- [ ] Implement bulk operations
- [ ] Add real-time updates
- [ ] Create camera preview
- [ ] Add configuration forms

### Phase 5: Polish and Testing
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
    "@mui/material": "^5.11.0",
    "@mui/icons-material": "^5.11.0",
    "react-hook-form": "^7.43.0",
    "yup": "^1.0.0",
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
screens/camera-management/
├── README.md
├── index.tsx
├── components/
│   ├── CameraManagementContainer.tsx
│   ├── CameraGrid.tsx
│   ├── CameraCard.tsx
│   ├── AddCameraModal.tsx
│   ├── EditCameraModal.tsx
│   ├── CameraPreview.tsx
│   ├── FilterPanel.tsx
│   └── BulkActions.tsx
├── forms/
│   ├── CameraForm.tsx
│   ├── StreamConfigForm.tsx
│   ├── LocationForm.tsx
│   ├── ScheduleForm.tsx
│   └── AlertConfigForm.tsx
├── hooks/
│   ├── useCameras.ts
│   ├── useCameraOperations.ts
│   └── useRealTimeUpdates.ts
├── utils/
│   ├── cameraHelpers.ts
│   ├── searchUtils.ts
│   └── validationUtils.ts
├── types/
│   └── camera.types.ts
├── styles/
│   └── cameraManagement.styles.ts
└── tests/
    ├── CameraManagementContainer.test.tsx
    ├── CameraCard.test.tsx
    └── CameraForm.test.tsx
```

## Status Tracking

### Development Status: 🟡 In Progress
- **Started**: [Date]
- **Estimated Completion**: [Date]
- **Current Phase**: Phase 1 - Core Structure
- **Next Milestone**: CRUD Operations

### Review Status
- **Design Review**: ⏳ Pending
- **Code Review**: ⏳ Pending
- **QA Testing**: ⏳ Pending
- **Security Review**: ⏳ Pending

### Dependencies
- **Backend API**: ✅ Ready
- **Authentication Service**: ✅ Ready
- **Design System**: ✅ Ready
- **Testing Framework**: ✅ Ready 