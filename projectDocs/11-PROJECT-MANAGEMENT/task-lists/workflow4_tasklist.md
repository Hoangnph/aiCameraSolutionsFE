# Workflow 4: Frontend Integration - Task List
## AI Camera Counting System - Frontend Development

### 📊 Tổng quan
Workflow 4 tập trung vào việc phát triển Frontend React application để tích hợp với các backend services đã hoàn thành trong Workflow 1-3. Frontend sẽ cung cấp giao diện người dùng hoàn chỉnh cho việc quản lý cameras, monitoring real-time, và analytics dashboard.

### 🎯 Mục tiêu kỹ thuật
- **Performance**: Page load time <3s, smooth interactions <100ms
- **Responsive Design**: Mobile-first approach, support all devices
- **User Experience**: Intuitive UI/UX, accessibility compliance
- **Real-time Updates**: WebSocket integration, live data streaming
- **Security**: JWT token management, secure API communication
- **Scalability**: Component-based architecture, code splitting
- **Testing**: Unit tests, integration tests, E2E tests

### 🏗️ Frontend Architecture Overview

#### System Architecture
```
┌─────────────────────────────────────────────────────────────────┐
│                    FRONTEND INTEGRATION ARCHITECTURE            │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │                    REACT APPLICATION                        │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Pages     │  │ Components  │  │   Services  │        │ │
│  │  │   & Routes  │  │   & Hooks   │  │   & Utils   │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                    │                             │
│                                    ▼                             │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │                    API INTEGRATION LAYER                    │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   beAuth    │  │   beCamera  │  │   WebSocket │        │ │
│  │  │   API       │  │   API       │  │   Service   │        │ │
│  │  │   Port 3001 │  │   Port 3002 │  │   Port 3003 │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                    │                             │
│                                    ▼                             │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │                    BACKEND SERVICES                         │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   beAuth    │  │   beCamera  │  │   Worker    │        │ │
│  │  │   Service   │  │   Service   │  │   Pool      │        │ │
│  │  │   (Node.js) │  │   (Python)  │  │   (4 workers)│       │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

#### Component Architecture
```
┌─────────────────────────────────────────────────────────────────┐
│                    COMPONENT HIERARCHY                          │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │                    APP LAYOUT                               │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Header    │  │   Sidebar   │  │   Main      │        │ │
│  │  │   (Navbar)  │  │   (Menu)    │  │   Content   │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                    │                             │
│                                    ▼                             │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │                    PAGE COMPONENTS                           │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Dashboard │  │   Cameras   │  │   Analytics │        │ │
│  │  │   Page      │  │   Page      │  │   Page      │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                    │                             │
│                                    ▼                             │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │                    SHARED COMPONENTS                         │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Camera    │  │   Charts    │  │   Forms     │        │ │
│  │  │   Cards     │  │   & Graphs  │  │   & Modals  │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### 📋 Task List

#### Phase 1: Project Setup & Configuration (Priority: Critical)
- [ ] **Task 1.1**: Initialize React Application
  - [ ] Create React app với TypeScript
  - [ ] Setup project structure và folder organization
  - [ ] Configure build tools (Webpack, Babel)
  - [ ] Setup development environment
  - [ ] Configure ESLint và Prettier

- [ ] **Task 1.2**: Install Dependencies
  - [ ] Core dependencies:
    ```json
    {
      "react": "^18.2.0",
      "react-dom": "^18.2.0",
      "react-router-dom": "^6.8.0",
      "typescript": "^4.9.0",
      "@types/react": "^18.0.0",
      "@types/react-dom": "^18.0.0"
    }
    ```
  - [ ] UI Framework:
    ```json
    {
      "tailwindcss": "^3.2.0",
      "@headlessui/react": "^1.7.0",
      "@heroicons/react": "^2.0.0",
      "clsx": "^1.2.0"
    }
    ```
  - [ ] State Management:
    ```json
    {
      "zustand": "^4.3.0",
      "react-query": "^3.39.0"
    }
    ```
  - [ ] HTTP Client:
    ```json
    {
      "axios": "^1.3.0",
      "socket.io-client": "^4.6.0"
    }
    ```

- [ ] **Task 1.3**: Environment Configuration
  - [ ] Create `.env` files cho development/production
  - [ ] Configure API endpoints:
    ```env
    REACT_APP_API_URL=http://localhost:3001/api/v1
    REACT_APP_CAMERA_API_URL=http://localhost:3002/api/v1
    REACT_APP_WS_URL=ws://localhost:3003
    REACT_APP_AUTH_SERVICE_URL=http://localhost:3001
    ```
  - [ ] Setup proxy configuration cho development

#### Phase 2: Authentication & User Management (Priority: Critical)
- [ ] **Task 2.1**: Authentication Service Integration
  - [ ] Create authentication service:
    ```typescript
    // services/authService.ts
    interface LoginCredentials {
      username: string;
      password: string;
    }
    
    interface AuthResponse {
      success: boolean;
      data: {
        user: User;
        accessToken: string;
        refreshToken: string;
      };
    }
    
    class AuthService {
      async login(credentials: LoginCredentials): Promise<AuthResponse>
      async logout(): Promise<void>
      async refreshToken(): Promise<AuthResponse>
      async getCurrentUser(): Promise<User>
      isAuthenticated(): boolean
    }
    ```
  - [ ] Implement JWT token management
  - [ ] Add token refresh logic
  - [ ] Create authentication context/provider

- [ ] **Task 2.2**: Authentication UI Components
  - [ ] Login page với form validation
  - [ ] Register page (nếu cần)
  - [ ] Protected route wrapper
  - [ ] Authentication guard component
  - [ ] User profile dropdown

- [ ] **Task 2.3**: Route Protection
  - [ ] Implement protected routes
  - [ ] Add role-based access control
  - [ ] Create route guards
  - [ ] Handle authentication redirects

#### Phase 3: Core Layout & Navigation (Priority: High)
- [ ] **Task 3.1**: Application Layout
  - [ ] Create main layout component:
    ```typescript
    // components/layout/MainLayout.tsx
    interface MainLayoutProps {
      children: React.ReactNode;
    }
    
    const MainLayout: React.FC<MainLayoutProps> = ({ children }) => {
      return (
        <div className="min-h-screen bg-gray-50">
          <Header />
          <div className="flex">
            <Sidebar />
            <main className="flex-1 p-6">
              {children}
            </main>
          </div>
        </div>
      );
    };
    ```
  - [ ] Header component với navigation
  - [ ] Sidebar component với menu
  - [ ] Responsive design cho mobile

- [ ] **Task 3.2**: Navigation System
  - [ ] Setup React Router
  - [ ] Create navigation menu
  - [ ] Add breadcrumbs
  - [ ] Implement active route highlighting

#### Phase 4: Camera Management Interface (Priority: High)
- [ ] **Task 4.1**: Camera List Page
  - [ ] Create camera list component:
    ```typescript
    // pages/CamerasPage.tsx
    interface Camera {
      id: number;
      name: string;
      location: string;
      stream_url: string;
      status: 'active' | 'offline' | 'maintenance' | 'error';
      created_at: string;
    }
    
    const CamerasPage: React.FC = () => {
      const [cameras, setCameras] = useState<Camera[]>([]);
      const [loading, setLoading] = useState(true);
      
      // Implementation
    };
    ```
  - [ ] Camera card component với status indicators
  - [ ] Camera grid/list view toggle
  - [ ] Search và filter functionality
  - [ ] Pagination cho large lists

- [ ] **Task 4.2**: Camera Detail Page
  - [ ] Individual camera view
  - [ ] Camera settings form
  - [ ] Real-time status monitoring
  - [ ] Camera control buttons (start/stop)

- [ ] **Task 4.3**: Camera Forms
  - [ ] Add camera form
  - [ ] Edit camera form
  - [ ] Form validation
  - [ ] Success/error handling

#### Phase 5: Dashboard & Analytics (Priority: High)
- [ ] **Task 5.1**: Dashboard Overview
  - [ ] Create dashboard page:
    ```typescript
    // pages/DashboardPage.tsx
    interface DashboardData {
      total_cameras: number;
      active_cameras: number;
      today_in: number;
      today_out: number;
      current_count: number;
    }
    
    const DashboardPage: React.FC = () => {
      const [dashboardData, setDashboardData] = useState<DashboardData>();
      
      // Implementation with charts and metrics
    };
    ```
  - [ ] Key metrics cards
  - [ ] Real-time count display
  - [ ] System status overview

- [ ] **Task 5.2**: Analytics Charts
  - [ ] People count charts (Chart.js/Recharts)
  - [ ] Camera activity graphs
  - [ ] Time-series data visualization
  - [ ] Export functionality

- [ ] **Task 5.3**: Analytics Page
  - [ ] Detailed analytics view
  - [ ] Date range picker
  - [ ] Filter by camera
  - [ ] Data export options

#### Phase 6: Real-time Features (Priority: Medium)
- [ ] **Task 6.1**: WebSocket Integration
  - [ ] Setup WebSocket connection:
    ```typescript
    // services/websocketService.ts
    class WebSocketService {
      private socket: WebSocket;
      
      connect(): void
      disconnect(): void
      subscribe(event: string, callback: Function): void
      unsubscribe(event: string): void
      send(event: string, data: any): void
    }
    ```
  - [ ] Real-time count updates
  - [ ] Camera status changes
  - [ ] System notifications

- [ ] **Task 6.2**: Live Camera Streams
  - [ ] Camera stream viewer component
  - [ ] Video player integration
  - [ ] Stream quality controls
  - [ ] Multiple stream support

#### Phase 7: State Management & Data Fetching (Priority: High)
- [ ] **Task 7.1**: State Management Setup
  - [ ] Configure Zustand stores:
    ```typescript
    // stores/authStore.ts
    interface AuthState {
      user: User | null;
      isAuthenticated: boolean;
      loading: boolean;
      login: (credentials: LoginCredentials) => Promise<void>;
      logout: () => void;
    }
    
    // stores/cameraStore.ts
    interface CameraState {
      cameras: Camera[];
      selectedCamera: Camera | null;
      loading: boolean;
      fetchCameras: () => Promise<void>;
      addCamera: (camera: Partial<Camera>) => Promise<void>;
      updateCamera: (id: number, data: Partial<Camera>) => Promise<void>;
      deleteCamera: (id: number) => Promise<void>;
    }
    ```
  - [ ] Global state management
  - [ ] Local state optimization

- [ ] **Task 7.2**: API Integration
  - [ ] Create API service classes:
    ```typescript
    // services/apiService.ts
    class ApiService {
      private baseURL: string;
      private token: string;
      
      constructor(baseURL: string) {
        this.baseURL = baseURL;
      }
      
      setToken(token: string): void
      get<T>(endpoint: string): Promise<T>
      post<T>(endpoint: string, data: any): Promise<T>
      put<T>(endpoint: string, data: any): Promise<T>
      delete<T>(endpoint: string): Promise<T>
    }
    ```
  - [ ] Error handling middleware
  - [ ] Request/response interceptors
  - [ ] Retry logic

#### Phase 8: UI/UX Enhancement (Priority: Medium)
- [ ] **Task 8.1**: Component Library
  - [ ] Create reusable components:
    ```typescript
    // components/ui/Button.tsx
    interface ButtonProps {
      variant: 'primary' | 'secondary' | 'danger';
      size: 'sm' | 'md' | 'lg';
      loading?: boolean;
      disabled?: boolean;
      children: React.ReactNode;
      onClick?: () => void;
    }
    
    // components/ui/Modal.tsx
    // components/ui/Table.tsx
    // components/ui/Form.tsx
    ```
  - [ ] Consistent design system
  - [ ] Dark/light theme support
  - [ ] Responsive components

- [ ] **Task 8.2**: Loading States & Error Handling
  - [ ] Loading spinners
  - [ ] Error boundaries
  - [ ] Empty states
  - [ ] Toast notifications

#### Phase 9: Testing & Quality Assurance (Priority: High)
- [ ] **Task 9.1**: Unit Testing
  - [ ] Setup Jest và React Testing Library
  - [ ] Test components
  - [ ] Test services
  - [ ] Test utilities

- [ ] **Task 9.2**: Integration Testing
  - [ ] API integration tests
  - [ ] Authentication flow tests
  - [ ] User interaction tests

- [ ] **Task 9.3**: E2E Testing
  - [ ] Setup Cypress
  - [ ] Critical user journey tests
  - [ ] Cross-browser testing

#### Phase 10: Performance Optimization (Priority: Medium)
- [ ] **Task 10.1**: Code Splitting
  - [ ] Route-based code splitting
  - [ ] Component lazy loading
  - [ ] Bundle optimization

- [ ] **Task 10.2**: Performance Monitoring
  - [ ] Setup performance monitoring
  - [ ] Bundle size analysis
  - [ ] Core Web Vitals optimization

#### Phase 11: Deployment & CI/CD (Priority: Medium)
- [ ] **Task 11.1**: Build Configuration
  - [ ] Production build setup
  - [ ] Environment-specific builds
  - [ ] Asset optimization

- [ ] **Task 11.2**: Docker Integration
  - [ ] Create Dockerfile
  - [ ] Multi-stage builds
  - [ ] Docker Compose integration

### 🎯 Success Criteria

#### Technical Metrics
- **Page Load Time**: <3 seconds
- **Time to Interactive**: <5 seconds
- **Bundle Size**: <2MB gzipped
- **Lighthouse Score**: >90 for all categories
- **Test Coverage**: >80%

#### User Experience Metrics
- **Mobile Responsiveness**: 100% device support
- **Accessibility**: WCAG 2.1 AA compliance
- **Cross-browser**: Chrome, Firefox, Safari, Edge
- **Error Rate**: <1%

### 📊 API Integration Points

#### beAuth Service (Port 3001)
```typescript
// Authentication endpoints
POST /api/v1/auth/login
POST /api/v1/auth/logout
POST /api/v1/auth/refresh
GET /api/v1/auth/me
```

#### beCamera Service (Port 3002)
```typescript
// Camera management endpoints
GET /api/v1/cameras
POST /api/v1/cameras
GET /api/v1/cameras/{id}
PUT /api/v1/cameras/{id}
DELETE /api/v1/cameras/{id}
PATCH /api/v1/cameras/{id}/status

// Analytics endpoints
GET /api/v1/counts
GET /api/v1/analytics/summary

// Worker pool endpoints
POST /api/v1/cameras/{id}/start
POST /api/v1/cameras/{id}/stop
GET /api/v1/cameras/{id}/status
GET /api/v1/workers/status
```

### 🚀 Implementation Timeline

#### Week 1: Setup & Authentication
- Project setup và configuration
- Authentication integration
- Basic layout và navigation

#### Week 2: Core Features
- Camera management interface
- Dashboard implementation
- Basic analytics

#### Week 3: Advanced Features
- Real-time updates
- Advanced analytics
- UI/UX enhancement

#### Week 4: Testing & Deployment
- Comprehensive testing
- Performance optimization
- Deployment preparation

### 📋 Dependencies

#### Backend Dependencies
- ✅ beAuth Service (Workflow 1) - Completed
- ✅ beCamera Service (Workflow 3) - Completed
- ✅ Database Schema - Completed
- ✅ API Documentation - Available

#### Frontend Dependencies
- Node.js 16+
- npm/yarn package manager
- Modern browser support
- Development tools (VS Code recommended)

---

**Workflow 4 Status**: 🔄 **PLANNED**  
**Estimated Duration**: 4 weeks  
**Priority**: High  
**Dependencies**: Workflow 1, 2, 3 completed 