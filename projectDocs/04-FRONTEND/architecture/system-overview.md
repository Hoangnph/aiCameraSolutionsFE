# 🏗️ System Overview - Frontend Architecture

## 📊 **Tổng quan kiến trúc**

Tài liệu này trình bày kiến trúc tổng thể của frontend application cho hệ thống AI Camera Counting, áp dụng CLEAN Architecture principles.

**🎯 Kiến trúc**: CLEAN Architecture + Component-based design  
**🏗️ Pattern**: Layered Architecture với separation of concerns  
**📱 Framework**: React 18.2.0 + TypeScript  
**🎨 UI Library**: Material-UI + Custom Vui Components  

---

## 🏗️ **Architecture Layers**

### **High-Level Architecture**
```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              FRONTEND ARCHITECTURE                              │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              PRESENTATION LAYER                             │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Pages     │  │   Layouts   │  │   Templates │  │   Navigation│        │ │
│  │  │   (Screens) │  │   (Wrappers)│  │   (Structure)│ │   (Routing) │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                             │
│                                    ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              DOMAIN LAYER                                   │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Entities  │  │   Use Cases │  │   Interfaces│  │   Services  │        │ │
│  │  │   (Models)  │  │   (Business)│  │   (Contracts)│ │   (Logic)   │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                             │
│                                    ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              DATA LAYER                                     │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   API       │  │   WebSocket │  │   Local     │  │   Cache     │        │ │
│  │  │   Services  │  │   Services  │  │   Storage   │  │   Services  │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                             │
│                                    ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              INFRASTRUCTURE LAYER                           │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   State     │  │   Routing   │  │   Security  │  │   Utils     │        │ │
│  │  │   Management│  │   (React    │  │   (Auth,    │  │   (Helpers) │        │ │
│  │  │   (Context) │  │   Router)   │  │   Validation)│ │             │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 📁 **Project Structure**

### **Directory Organization**
```
src/
├── presentation/                    # Presentation Layer
│   ├── pages/                      # Screen components
│   │   ├── authentication/         # Auth screens
│   │   ├── dashboard/              # Dashboard screen
│   │   ├── camera-management/      # Camera screens
│   │   ├── analytics/              # Analytics screens
│   │   ├── real-time-monitoring/   # Monitoring screens
│   │   └── settings/               # Settings screens
│   ├── layouts/                    # Layout components
│   │   ├── DashboardLayout.tsx
│   │   ├── AuthLayout.tsx
│   │   └── MainLayout.tsx
│   ├── navigation/                 # Navigation components
│   │   ├── Sidebar.tsx
│   │   ├── Header.tsx
│   │   └── Breadcrumbs.tsx
│   └── templates/                  # Page templates
│       ├── PageTemplate.tsx
│       └── ModalTemplate.tsx
├── domain/                         # Domain Layer
│   ├── entities/                   # Business entities
│   │   ├── User.ts
│   │   ├── Camera.ts
│   │   ├── CountData.ts
│   │   └── Alert.ts
│   ├── use-cases/                  # Business logic
│   │   ├── authentication/
│   │   ├── camera-management/
│   │   ├── analytics/
│   │   └── monitoring/
│   ├── interfaces/                 # Contracts
│   │   ├── repositories/
│   │   ├── services/
│   │   └── presenters/
│   └── services/                   # Domain services
│       ├── AuthService.ts
│       ├── CameraService.ts
│       └── AnalyticsService.ts
├── data/                           # Data Layer
│   ├── api/                        # API services
│   │   ├── authAPI.ts
│   │   ├── cameraAPI.ts
│   │   └── analyticsAPI.ts
│   ├── websocket/                  # WebSocket services
│   │   ├── WebSocketService.ts
│   │   └── RealTimeService.ts
│   ├── storage/                    # Local storage
│   │   ├── LocalStorage.ts
│   │   └── SessionStorage.ts
│   └── cache/                      # Cache services
│       ├── CacheService.ts
│       └── QueryCache.ts
├── infrastructure/                 # Infrastructure Layer
│   ├── state/                      # State management
│   │   ├── contexts/
│   │   ├── hooks/
│   │   └── reducers/
│   ├── routing/                    # Routing configuration
│   │   ├── routes.ts
│   │   └── guards.ts
│   ├── security/                   # Security utilities
│   │   ├── auth.ts
│   │   ├── validation.ts
│   │   └── encryption.ts
│   └── utils/                      # Utility functions
│       ├── formatters.ts
│       ├── validators.ts
│       └── helpers.ts
├── shared/                         # Shared components
│   ├── components/                 # Reusable components
│   │   ├── atomic/                 # Atomic components
│   │   ├── molecular/              # Molecular components
│   │   └── organisms/              # Organism components
│   ├── hooks/                      # Custom hooks
│   │   ├── useAuth.ts
│   │   ├── useCamera.ts
│   │   └── useWebSocket.ts
│   └── constants/                  # Constants
│       ├── api.ts
│       ├── routes.ts
│       └── config.ts
└── types/                          # TypeScript types
    ├── api.ts
    ├── entities.ts
    └── common.ts
```

---

## 🔄 **Data Flow Architecture**

### **Unidirectional Data Flow**
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   User      │    │   Component │    │   State     │    │   Backend   │
│   Action    │    │   (UI)      │    │   Store     │    │   API       │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
       │                   │                   │                   │
       │ 1. User Click     │                   │                   │
       │──────────────────►│                   │                   │
       │                   │                   │                   │
       │                   │ 2. Dispatch Action│                   │
       │                   │──────────────────►│                   │
       │                   │                   │                   │
       │                   │                   │ 3. API Call       │
       │                   │                   │──────────────────►│
       │                   │                   │                   │
       │                   │                   │ 4. API Response   │
       │                   │                   │◄──────────────────┤
       │                   │                   │                   │
       │                   │ 5. State Update   │                   │
       │                   │◄──────────────────┤                   │
       │                   │                   │                   │
       │ 6. UI Update      │                   │                   │
       │◄──────────────────┤                   │                   │
       │                   │                   │                   │
```

### **Real-time Data Flow**
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   WebSocket │    │   Real-time │    │   State     │    │   Component │
│   Server    │    │   Service   │    │   Store     │    │   (UI)      │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
       │                   │                   │                   │
       │ 1. Real-time Data │                   │                   │
       │──────────────────►│                   │                   │
       │                   │                   │                   │
       │                   │ 2. Process Data   │                   │
       │                   │──────────────────►│                   │
       │                   │                   │                   │
       │                   │                   │ 3. Update State   │
       │                   │                   │──────────────────►│
       │                   │                   │                   │
       │                   │                   │ 4. UI Re-render   │
       │                   │                   │──────────────────►│
       │                   │                   │                   │
```

---

## 🎯 **CLEAN Architecture Implementation**

### **1. Presentation Layer (UI)**
```typescript
// Pages - Screen components
interface PageProps {
  // Page-specific props
}

// Layouts - Wrapper components
interface LayoutProps {
  children: React.ReactNode;
  title?: string;
  breadcrumbs?: BreadcrumbItem[];
}

// Navigation - Routing components
interface NavigationProps {
  routes: Route[];
  currentRoute: string;
}
```

### **2. Domain Layer (Business Logic)**
```typescript
// Entities - Business models
interface User {
  id: string;
  email: string;
  role: UserRole;
  permissions: Permission[];
}

interface Camera {
  id: string;
  name: string;
  location: string;
  status: CameraStatus;
  streamUrl: string;
}

// Use Cases - Business logic
interface AuthenticationUseCase {
  login(credentials: LoginCredentials): Promise<AuthResult>;
  logout(): Promise<void>;
  refreshToken(): Promise<AuthResult>;
}

interface CameraManagementUseCase {
  getCameras(): Promise<Camera[]>;
  createCamera(camera: CreateCameraRequest): Promise<Camera>;
  updateCamera(id: string, camera: UpdateCameraRequest): Promise<Camera>;
  deleteCamera(id: string): Promise<void>;
}
```

### **3. Data Layer (External Interfaces)**
```typescript
// Repository interfaces
interface UserRepository {
  findByEmail(email: string): Promise<User | null>;
  save(user: User): Promise<User>;
  update(id: string, user: Partial<User>): Promise<User>;
}

interface CameraRepository {
  findAll(): Promise<Camera[]>;
  findById(id: string): Promise<Camera | null>;
  create(camera: CreateCameraRequest): Promise<Camera>;
  update(id: string, camera: UpdateCameraRequest): Promise<Camera>;
  delete(id: string): Promise<void>;
}

// Service interfaces
interface AuthService {
  authenticate(credentials: LoginCredentials): Promise<AuthResult>;
  validateToken(token: string): Promise<boolean>;
  refreshToken(refreshToken: string): Promise<AuthResult>;
}
```

### **4. Infrastructure Layer (External Dependencies)**
```typescript
// State management
interface AppState {
  auth: AuthState;
  cameras: CameraState;
  analytics: AnalyticsState;
  realtime: RealtimeState;
}

// Security utilities
interface SecurityService {
  encrypt(data: string): string;
  decrypt(data: string): string;
  hashPassword(password: string): string;
  validatePassword(password: string, hash: string): boolean;
}
```

---

## 🔧 **Technology Stack**

### **Core Technologies**
```json
{
  "framework": {
    "name": "React",
    "version": "18.2.0",
    "features": ["Hooks", "Context", "Suspense"]
  },
  "language": {
    "name": "TypeScript",
    "version": "5.0+",
    "features": ["Strict mode", "Advanced types"]
  },
  "ui": {
    "library": "Material-UI",
    "version": "5.9.2",
    "components": "Custom Vui components"
  },
  "state": {
    "management": "React Context + Hooks",
    "patterns": ["Provider pattern", "Custom hooks"]
  },
  "routing": {
    "library": "React Router DOM",
    "version": "5.2.0",
    "features": ["Nested routes", "Route guards"]
  }
}
```

### **Development Tools**
```json
{
  "build": {
    "tool": "Vite",
    "features": ["Fast HMR", "TypeScript support"]
  },
  "testing": {
    "framework": "Jest",
    "library": "React Testing Library",
    "coverage": ">80%"
  },
  "linting": {
    "eslint": "Airbnb config",
    "prettier": "Code formatting"
  },
  "documentation": {
    "storybook": "Component documentation",
    "typedoc": "API documentation"
  }
}
```

---

## 🎨 **Component Architecture**

### **Atomic Design Pattern**
```
Atoms (Basic Components)
├── VuiButton
├── VuiInput
├── VuiTypography
├── VuiIcon
└── VuiBadge

Molecules (Composite Components)
├── VuiFormField
├── VuiCard
├── VuiAlert
├── VuiModal
└── VuiTooltip

Organisms (Complex Components)
├── VuiNavigation
├── VuiDataTable
├── VuiChart
├── VuiCameraGrid
└── VuiDashboard

Templates (Page Layouts)
├── DashboardLayout
├── AuthLayout
├── CameraLayout
└── AnalyticsLayout
```

---

## 🔒 **Security Architecture**

### **Authentication Flow**
```typescript
// JWT-based authentication
interface AuthFlow {
  login: (credentials: LoginCredentials) => Promise<AuthResult>;
  logout: () => Promise<void>;
  refresh: (refreshToken: string) => Promise<AuthResult>;
  validate: (token: string) => Promise<boolean>;
}

// Route protection
interface RouteGuard {
  requireAuth: (component: React.ComponentType) => React.ComponentType;
  requireRole: (roles: UserRole[]) => (component: React.ComponentType) => React.ComponentType;
}
```

### **Data Protection**
```typescript
// Input validation
interface ValidationRules {
  required: boolean;
  minLength?: number;
  maxLength?: number;
  pattern?: RegExp;
  custom?: (value: any) => boolean;
}

// XSS prevention
interface SecurityUtils {
  sanitizeInput: (input: string) => string;
  escapeHtml: (html: string) => string;
  validateUrl: (url: string) => boolean;
}
```

---

## 📊 **Performance Architecture**

### **Optimization Strategies**
```typescript
// Code splitting
const lazyComponents = {
  Dashboard: lazy(() => import('./pages/Dashboard')),
  CameraManagement: lazy(() => import('./pages/CameraManagement')),
  Analytics: lazy(() => import('./pages/Analytics'))
};

// Memoization
const memoizedComponents = {
  CameraGrid: memo(CameraGrid),
  StatisticsCard: memo(StatisticsCard),
  ChartComponent: memo(ChartComponent)
};

// Caching
const cacheStrategies = {
  api: 'stale-while-revalidate',
  images: 'cache-first',
  static: 'cache-first'
};
```

### **Bundle Optimization**
```json
{
  "splitting": {
    "vendor": "node_modules",
    "pages": "route-based",
    "components": "dynamic imports"
  },
  "compression": {
    "gzip": true,
    "brotli": true
  },
  "treeShaking": {
    "enabled": true,
    "sideEffects": false
  }
}
```

---

## 🧪 **Testing Architecture**

### **Testing Strategy**
```typescript
// Unit tests
interface UnitTestStrategy {
  components: 'React Testing Library';
  hooks: 'Custom test utilities';
  utilities: 'Jest';
  coverage: '>80%';
}

// Integration tests
interface IntegrationTestStrategy {
  api: 'MSW (Mock Service Worker)';
  routing: 'React Router testing';
  state: 'Context testing';
}

// E2E tests
interface E2ETestStrategy {
  framework: 'Playwright';
  scenarios: 'Critical user paths';
  browsers: 'Chrome, Firefox, Safari';
}
```

---

## 🚀 **Deployment Architecture**

### **Build Pipeline**
```yaml
# Build stages
stages:
  - lint: "ESLint + Prettier"
  - test: "Unit + Integration tests"
  - build: "Production build"
  - analyze: "Bundle analysis"
  - deploy: "Docker deployment"
```

### **Environment Configuration**
```typescript
// Environment variables
interface EnvironmentConfig {
  development: {
    apiUrl: 'http://localhost:3001/api/v1';
    wsUrl: 'ws://localhost:3003';
    debug: true;
  };
  production: {
    apiUrl: 'https://api.aicamera.com/v1';
    wsUrl: 'wss://ws.aicamera.com';
    debug: false;
  };
}
```

---

**📅 Last Updated**: 2025-01-14  
**👥 Author**: Frontend Architecture Team  
**📊 Status**: Architecture Complete - Ready for Implementation 