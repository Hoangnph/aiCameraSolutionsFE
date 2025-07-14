# Frontend Technical Requirements
## AI Camera Counting System

### 📊 Tổng quan

Tài liệu này định nghĩa các yêu cầu kỹ thuật chi tiết cho frontend development của hệ thống AI Camera Counting, bao gồm architecture patterns, performance requirements, và implementation guidelines.

### 🎯 Mục tiêu kỹ thuật

#### Mục tiêu chính
- Xây dựng scalable và maintainable frontend architecture
- Đảm bảo performance tối ưu với real-time updates
- Cung cấp user experience tốt trên mọi thiết bị
- Tuân thủ accessibility standards
- Tối ưu hóa bundle size và loading performance

#### Mục tiêu kỹ thuật
- First Contentful Paint <1.5s
- Largest Contentful Paint <2.5s
- Bundle size <500KB initial bundle
- WCAG 2.1 AA compliance
- Mobile-first responsive design
- Real-time updates <100ms latency

### 🏗️ Architecture Patterns

#### 1. State Management Architecture

##### Redux Toolkit + RTK Query Implementation

```typescript
// Store Configuration
import { configureStore } from '@reduxjs/toolkit';
import { setupListeners } from '@reduxjs/toolkit/query';
import { cameraApi } from './services/cameraApi';
import { authSlice } from './slices/authSlice';
import { uiSlice } from './slices/uiSlice';

export const store = configureStore({
  reducer: {
    auth: authSlice.reducer,
    ui: uiSlice.reducer,
    [cameraApi.reducerPath]: cameraApi.reducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(cameraApi.middleware),
});

setupListeners(store.dispatch);

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
```

##### RTK Query API Configuration

```typescript
// Camera API Service
import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';

export const cameraApi = createApi({
  reducerPath: 'cameraApi',
  baseQuery: fetchBaseQuery({
    baseUrl: '/api/v1',
    prepareHeaders: (headers, { getState }) => {
      const token = (getState() as RootState).auth.token;
      if (token) {
        headers.set('authorization', `Bearer ${token}`);
      }
      return headers;
    },
  }),
  tagTypes: ['Camera', 'Count', 'Alert'],
  endpoints: (builder) => ({
    getCameras: builder.query<Camera[], void>({
      query: () => 'cameras',
      providesTags: ['Camera'],
    }),
    getCameraById: builder.query<Camera, string>({
      query: (id) => `cameras/${id}`,
      providesTags: (result, error, id) => [{ type: 'Camera', id }],
    }),
    getRealTimeCounts: builder.query<CountData[], void>({
      query: () => 'counts/realtime',
      async onCacheEntryAdded(
        arg,
        { updateCachedData, cacheDataLoaded, cacheEntryRemoved }
      ) {
        const ws = new WebSocket('ws://localhost:8004/ws/counts');
        try {
          await cacheDataLoaded;
          const listener = (event: MessageEvent) => {
            const data = JSON.parse(event.data);
            updateCachedData((draft) => {
              draft.push(data);
            });
          };
          ws.addEventListener('message', listener);
        } catch {
          // Handle error
        }
        await cacheEntryRemoved;
        ws.close();
      },
    }),
  }),
});

export const {
  useGetCamerasQuery,
  useGetCameraByIdQuery,
  useGetRealTimeCountsQuery,
} = cameraApi;
```

#### 2. Component Library Specification

##### Material-UI + Custom Components Architecture

```typescript
// Design System Configuration
import { createTheme, ThemeProvider } from '@mui/material/styles';
import { CssBaseline } from '@mui/material';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
      light: '#42a5f5',
      dark: '#1565c0',
    },
    secondary: {
      main: '#dc004e',
      light: '#ff5983',
      dark: '#9a0036',
    },
    background: {
      default: '#f5f5f5',
      paper: '#ffffff',
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
    h1: {
      fontSize: '2.5rem',
      fontWeight: 500,
    },
    h2: {
      fontSize: '2rem',
      fontWeight: 500,
    },
    h3: {
      fontSize: '1.75rem',
      fontWeight: 500,
    },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
          borderRadius: 8,
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 12,
          boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
        },
      },
    },
  },
});
```

##### Custom Component Library

```typescript
// Camera Card Component
import React from 'react';
import { Card, CardContent, CardMedia, Typography, Chip, Box } from '@mui/material';
import { styled } from '@mui/material/styles';

interface CameraCardProps {
  camera: Camera;
  onSelect: (camera: Camera) => void;
}

const StyledCard = styled(Card)(({ theme }) => ({
  cursor: 'pointer',
  transition: 'transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out',
  '&:hover': {
    transform: 'translateY(-4px)',
    boxShadow: theme.shadows[8],
  },
}));

const StatusChip = styled(Chip)(({ theme, status }: { theme: any; status: string }) => ({
  backgroundColor: status === 'active' ? theme.palette.success.main : theme.palette.error.main,
  color: 'white',
  fontWeight: 600,
}));

export const CameraCard: React.FC<CameraCardProps> = ({ camera, onSelect }) => {
  return (
    <StyledCard onClick={() => onSelect(camera)}>
      <CardMedia
        component="img"
        height="200"
        image={camera.thumbnailUrl}
        alt={camera.name}
        sx={{ objectFit: 'cover' }}
      />
      <CardContent>
        <Typography variant="h6" gutterBottom>
          {camera.name}
        </Typography>
        <Typography variant="body2" color="text.secondary" gutterBottom>
          {camera.location}
        </Typography>
        <Box display="flex" justifyContent="space-between" alignItems="center">
          <StatusChip
            label={camera.status}
            status={camera.status}
            size="small"
          />
          <Typography variant="caption" color="text.secondary">
            Count: {camera.currentCount}
          </Typography>
        </Box>
      </CardContent>
    </StyledCard>
  );
};
```

#### 3. Real-time UI Patterns

##### WebSocket Integration

```typescript
// WebSocket Service
class WebSocketService {
  private ws: WebSocket | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectDelay = 1000;

  constructor(private url: string, private onMessage: (data: any) => void) {}

  connect() {
    try {
      this.ws = new WebSocket(this.url);
      
      this.ws.onopen = () => {
        console.log('WebSocket connected');
        this.reconnectAttempts = 0;
      };

      this.ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          this.onMessage(data);
        } catch (error) {
          console.error('Error parsing WebSocket message:', error);
        }
      };

      this.ws.onclose = () => {
        console.log('WebSocket disconnected');
        this.attemptReconnect();
      };

      this.ws.onerror = (error) => {
        console.error('WebSocket error:', error);
      };
    } catch (error) {
      console.error('Error creating WebSocket:', error);
    }
  }

  private attemptReconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      setTimeout(() => {
        console.log(`Attempting to reconnect (${this.reconnectAttempts}/${this.maxReconnectAttempts})`);
        this.connect();
      }, this.reconnectDelay * this.reconnectAttempts);
    }
  }

  send(data: any) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(data));
    }
  }

  disconnect() {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }
}
```

##### Real-time Dashboard Component

```typescript
// Real-time Dashboard
import React, { useEffect, useState } from 'react';
import { Grid, Paper, Typography, Box } from '@mui/material';
import { useGetRealTimeCountsQuery } from '../services/cameraApi';

interface CountData {
  cameraId: string;
  count: number;
  timestamp: string;
  confidence: number;
}

export const RealTimeDashboard: React.FC = () => {
  const { data: counts, isLoading, error } = useGetRealTimeCountsQuery();
  const [lastUpdate, setLastUpdate] = useState<Date>(new Date());

  useEffect(() => {
    const interval = setInterval(() => {
      setLastUpdate(new Date());
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error loading data</div>;

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Real-time Camera Counts
      </Typography>
      <Typography variant="body2" color="text.secondary" gutterBottom>
        Last updated: {lastUpdate.toLocaleTimeString()}
      </Typography>
      
      <Grid container spacing={3}>
        {counts?.map((count) => (
          <Grid item xs={12} sm={6} md={4} key={count.cameraId}>
            <Paper elevation={2} sx={{ p: 2 }}>
              <Typography variant="h6">Camera {count.cameraId}</Typography>
              <Typography variant="h4" color="primary">
                {count.count}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Confidence: {(count.confidence * 100).toFixed(1)}%
              </Typography>
            </Paper>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
};
```

#### 4. Performance Optimization

##### Code Splitting Strategy

```typescript
// Lazy Loading Components
import React, { Suspense, lazy } from 'react';
import { CircularProgress, Box } from '@mui/material';

// Lazy load heavy components
const CameraManagement = lazy(() => import('./pages/CameraManagement'));
const Analytics = lazy(() => import('./pages/Analytics'));
const Reports = lazy(() => import('./pages/Reports'));

// Loading component
const LoadingSpinner: React.FC = () => (
  <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
    <CircularProgress />
  </Box>
);

// Route configuration with lazy loading
const routes = [
  {
    path: '/cameras',
    component: () => (
      <Suspense fallback={<LoadingSpinner />}>
        <CameraManagement />
      </Suspense>
    ),
  },
  {
    path: '/analytics',
    component: () => (
      <Suspense fallback={<LoadingSpinner />}>
        <Analytics />
      </Suspense>
    ),
  },
  {
    path: '/reports',
    component: () => (
      <Suspense fallback={<LoadingSpinner />}>
        <Reports />
      </Suspense>
    ),
  },
];
```

##### Memoization and Optimization

```typescript
// Optimized Components
import React, { memo, useMemo, useCallback } from 'react';

// Memoized component
export const CameraGrid = memo<{ cameras: Camera[]; onSelect: (camera: Camera) => void }>(
  ({ cameras, onSelect }) => {
    // Memoize filtered cameras
    const activeCameras = useMemo(() => 
      cameras.filter(camera => camera.status === 'active'),
      [cameras]
    );

    // Memoize callback
    const handleSelect = useCallback((camera: Camera) => {
      onSelect(camera);
    }, [onSelect]);

    return (
      <Grid container spacing={2}>
        {activeCameras.map((camera) => (
          <Grid item xs={12} sm={6} md={4} key={camera.id}>
            <CameraCard camera={camera} onSelect={handleSelect} />
          </Grid>
        ))}
      </Grid>
    );
  }
);

// Virtual scrolling for large lists
import { FixedSizeList as List } from 'react-window';

const VirtualizedCameraList: React.FC<{ cameras: Camera[] }> = ({ cameras }) => {
  const Row = ({ index, style }: { index: number; style: React.CSSProperties }) => (
    <div style={style}>
      <CameraCard camera={cameras[index]} onSelect={() => {}} />
    </div>
  );

  return (
    <List
      height={600}
      itemCount={cameras.length}
      itemSize={200}
      width="100%"
    >
      {Row}
    </List>
  );
};
```

#### 5. Mobile-First Design System

##### Responsive Design Patterns

```typescript
// Responsive Layout Components
import { useTheme, useMediaQuery } from '@mui/material';

// Responsive hook
const useResponsive = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  const isTablet = useMediaQuery(theme.breakpoints.between('sm', 'md'));
  const isDesktop = useMediaQuery(theme.breakpoints.up('md'));

  return { isMobile, isTablet, isDesktop };
};

// Responsive dashboard layout
export const ResponsiveDashboard: React.FC = () => {
  const { isMobile, isTablet, isDesktop } = useResponsive();

  return (
    <Box>
      {isMobile && <MobileDashboard />}
      {isTablet && <TabletDashboard />}
      {isDesktop && <DesktopDashboard />}
    </Box>
  );
};

// Mobile-optimized navigation
const MobileNavigation: React.FC = () => {
  const [drawerOpen, setDrawerOpen] = useState(false);

  return (
    <>
      <AppBar position="fixed">
        <Toolbar>
          <IconButton
            edge="start"
            color="inherit"
            onClick={() => setDrawerOpen(true)}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" sx={{ flexGrow: 1 }}>
            AI Camera System
          </Typography>
        </Toolbar>
      </AppBar>
      
      <Drawer
        anchor="left"
        open={drawerOpen}
        onClose={() => setDrawerOpen(false)}
      >
        <List>
          <ListItem button>
            <ListItemIcon><DashboardIcon /></ListItemIcon>
            <ListItemText primary="Dashboard" />
          </ListItem>
          <ListItem button>
            <ListItemIcon><CameraIcon /></ListItemIcon>
            <ListItemText primary="Cameras" />
          </ListItem>
          <ListItem button>
            <ListItemIcon><AnalyticsIcon /></ListItemIcon>
            <ListItemText primary="Analytics" />
          </ListItem>
        </List>
      </Drawer>
    </>
  );
};
```

#### 6. Accessibility Standards (WCAG 2.1 AA)

##### Accessibility Implementation

```typescript
// Accessible components
import { useId } from 'react';

// Accessible form component
export const AccessibleForm: React.FC = () => {
  const emailId = useId();
  const passwordId = useId();

  return (
    <form role="form" aria-label="Login form">
      <div>
        <label htmlFor={emailId}>Email Address</label>
        <input
          id={emailId}
          type="email"
          aria-required="true"
          aria-describedby="email-error"
        />
        <div id="email-error" role="alert" aria-live="polite">
          {/* Error message */}
        </div>
      </div>
      
      <div>
        <label htmlFor={passwordId}>Password</label>
        <input
          id={passwordId}
          type="password"
          aria-required="true"
          aria-describedby="password-error"
        />
        <div id="password-error" role="alert" aria-live="polite">
          {/* Error message */}
        </div>
      </div>
    </form>
  );
};

// Keyboard navigation support
export const KeyboardNavigableGrid: React.FC<{ cameras: Camera[] }> = ({ cameras }) => {
  const [focusedIndex, setFocusedIndex] = useState(0);

  const handleKeyDown = (event: React.KeyboardEvent, index: number) => {
    switch (event.key) {
      case 'ArrowRight':
        event.preventDefault();
        setFocusedIndex((prev) => (prev + 1) % cameras.length);
        break;
      case 'ArrowLeft':
        event.preventDefault();
        setFocusedIndex((prev) => (prev - 1 + cameras.length) % cameras.length);
        break;
      case 'Enter':
      case ' ':
        event.preventDefault();
        // Handle selection
        break;
    }
  };

  return (
    <Grid container spacing={2}>
      {cameras.map((camera, index) => (
        <Grid item xs={12} sm={6} md={4} key={camera.id}>
          <Card
            tabIndex={0}
            role="button"
            aria-label={`Select camera ${camera.name}`}
            onKeyDown={(e) => handleKeyDown(e, index)}
            sx={{
              outline: focusedIndex === index ? '2px solid #1976d2' : 'none',
            }}
          >
            {/* Card content */}
          </Card>
        </Grid>
      ))}
    </Grid>
  );
};
```

#### 7. Bundle Size Optimization

##### Webpack Configuration

```javascript
// webpack.config.js
const path = require('path');
const { BundleAnalyzerPlugin } = require('webpack-bundle-analyzer');

module.exports = {
  entry: './src/index.tsx',
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: '[name].[contenthash].js',
    chunkFilename: '[name].[contenthash].chunk.js',
  },
  optimization: {
    splitChunks: {
      chunks: 'all',
      cacheGroups: {
        vendor: {
          test: /[\\/]node_modules[\\/]/,
          name: 'vendors',
          chunks: 'all',
        },
        common: {
          name: 'common',
          minChunks: 2,
          chunks: 'all',
          enforce: true,
        },
      },
    },
    runtimeChunk: 'single',
  },
  plugins: [
    new BundleAnalyzerPlugin({
      analyzerMode: process.env.ANALYZE === 'true' ? 'server' : 'disabled',
    }),
  ],
};
```

##### Tree Shaking and Dead Code Elimination

```typescript
// Optimized imports
// ✅ Good - Tree shakeable
import { Button } from '@mui/material/Button';
import { Card } from '@mui/material/Card';

// ❌ Bad - Imports entire library
import { Button, Card } from '@mui/material';

// Dynamic imports for code splitting
const loadHeavyComponent = () => import('./HeavyComponent');

// Usage
const HeavyComponent = React.lazy(loadHeavyComponent);
```

#### 8. PWA Requirements

##### Service Worker Implementation

```typescript
// service-worker.ts
const CACHE_NAME = 'ai-camera-cache-v1';
const urlsToCache = [
  '/',
  '/static/js/bundle.js',
  '/static/css/main.css',
  '/manifest.json',
];

self.addEventListener('install', (event: any) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll(urlsToCache))
  );
});

self.addEventListener('fetch', (event: any) => {
  event.respondWith(
    caches.match(event.request)
      .then((response) => {
        // Return cached version or fetch from network
        return response || fetch(event.request);
      })
  );
});

// Offline support
self.addEventListener('fetch', (event: any) => {
  if (event.request.mode === 'navigate') {
    event.respondWith(
      fetch(event.request).catch(() => {
        return caches.match('/offline.html');
      })
    );
  }
});
```

##### PWA Manifest

```json
{
  "name": "AI Camera Counting System",
  "short_name": "AI Camera",
  "description": "Real-time camera counting system with AI",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#1976d2",
  "icons": [
    {
      "src": "/icon-192x192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/icon-512x512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}
```

### 📋 Implementation Checklist

#### Phase 1: Foundation Setup (Week 1)
- [ ] Setup React 18 with TypeScript
- [ ] Configure Redux Toolkit + RTK Query
- [ ] Setup Material-UI theme system
- [ ] Configure Webpack for optimization
- [ ] Setup ESLint and Prettier

#### Phase 2: Core Components (Week 2)
- [ ] Implement design system components
- [ ] Create responsive layout components
- [ ] Setup routing with lazy loading
- [ ] Implement authentication UI
- [ ] Create camera management components

#### Phase 3: Real-time Features (Week 3)
- [ ] Implement WebSocket service
- [ ] Create real-time dashboard
- [ ] Setup RTK Query for real-time data
- [ ] Implement live camera feeds
- [ ] Create notification system

#### Phase 4: Performance & Accessibility (Week 4)
- [ ] Implement code splitting
- [ ] Setup bundle optimization
- [ ] Add accessibility features
- [ ] Implement PWA features
- [ ] Setup performance monitoring

### 🎯 Success Metrics

#### Performance Metrics
- **First Contentful Paint**: <1.5s
- **Largest Contentful Paint**: <2.5s
- **First Input Delay**: <100ms
- **Cumulative Layout Shift**: <0.1
- **Bundle Size**: <500KB initial bundle

#### Accessibility Metrics
- **WCAG 2.1 AA Compliance**: 100%
- **Keyboard Navigation**: Fully functional
- **Screen Reader Support**: Complete
- **Color Contrast**: Meets AA standards
- **Focus Management**: Proper implementation

#### User Experience Metrics
- **Mobile Responsiveness**: 100% responsive
- **Real-time Updates**: <100ms latency
- **Offline Functionality**: Basic features available
- **Error Handling**: Graceful degradation
- **Loading States**: Smooth transitions

### 🚨 Risk Mitigation

#### Performance Risks
- **Risk**: Large bundle size affecting load time
- **Mitigation**: Implement code splitting, lazy loading, tree shaking

#### Accessibility Risks
- **Risk**: Non-compliance with WCAG standards
- **Mitigation**: Regular accessibility audits, automated testing

#### Real-time Risks
- **Risk**: WebSocket connection failures
- **Mitigation**: Implement reconnection logic, fallback to polling

#### Mobile Risks
- **Risk**: Poor mobile performance
- **Mitigation**: Mobile-first design, performance optimization

---

**Document Version**: 1.0  
**Last Updated**: [Current Date]  
**Next Review**: [Date + 2 weeks]  
**Status**: Ready for Implementation
