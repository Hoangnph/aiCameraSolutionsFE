# Component Structure - People Counting Dashboard

## Tổng quan Component Architecture

Hệ thống sử dụng React với Material-UI, được tổ chức theo cấu trúc component hierarchy rõ ràng với separation of concerns.

## Component Hierarchy

```
App (Root Component)
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

## Component Categories

### 1. Common Components

#### Header
```typescript
interface HeaderProps {
  title: string;
  subtitle?: string;
  actions?: React.ReactNode;
  breadcrumbs?: BreadcrumbItem[];
}

// Features:
// - Page title and subtitle
// - Action buttons
// - Breadcrumb navigation
// - User profile menu
```

#### Sidebar
```typescript
interface SidebarProps {
  routes: Route[];
  isOpen: boolean;
  isCollapsed: boolean;
  onToggle: () => void;
  onCollapse: () => void;
}

// Features:
// - Navigation menu
// - Collapsible sidebar
// - Active route highlighting
// - User profile section
```

#### Loading
```typescript
interface LoadingProps {
  size?: 'small' | 'medium' | 'large';
  color?: string;
  text?: string;
  fullScreen?: boolean;
}

// Features:
// - Spinner animation
// - Loading text
// - Full screen overlay
// - Customizable size and color
```

#### ErrorBoundary
```typescript
interface ErrorBoundaryProps {
  children: React.ReactNode;
  fallback?: React.ComponentType<{ error: Error }>;
}

// Features:
// - Error catching
// - Fallback UI
// - Error reporting
// - Recovery mechanisms
```

### 2. Dashboard Components

#### LiveCounters
```typescript
interface LiveCountersProps {
  data: {
    currentCount: number;
    peopleIn: number;
    peopleOut: number;
    occupancy: number;
  };
  isLoading?: boolean;
}

// Features:
// - Real-time counters
// - Animated number changes
// - Color-coded indicators
// - Responsive design
```

#### CameraGrid
```typescript
interface CameraGridProps {
  cameras: Camera[];
  onCameraSelect: (cameraId: string) => void;
  layout?: 'grid' | 'list';
  showControls?: boolean;
}

// Features:
// - Grid/list layout
// - Camera thumbnails
// - Status indicators
// - Quick controls
```

#### QuickStats
```typescript
interface QuickStatsProps {
  stats: {
    today: StatData;
    week: StatData;
    month: StatData;
  };
  timeRange: 'today' | 'week' | 'month';
  onTimeRangeChange: (range: string) => void;
}

// Features:
// - Quick statistics
// - Time range selector
// - Trend indicators
// - Comparison views
```

#### AlertPanel
```typescript
interface AlertPanelProps {
  alerts: Alert[];
  maxAlerts?: number;
  onAlertClick: (alert: Alert) => void;
  onMarkAllRead: () => void;
}

// Features:
// - Alert list
// - Severity indicators
// - Mark as read functionality
// - Alert filtering
```

### 3. Camera Components

#### CameraViewer
```typescript
interface CameraViewerProps {
  camera: Camera;
  streamUrl: string;
  isLive: boolean;
  onError: (error: Error) => void;
  controls?: CameraControls;
}

// Features:
// - Video stream display
// - Fullscreen support
// - Quality selection
// - Recording controls
```

#### CameraControls
```typescript
interface CameraControlsProps {
  camera: Camera;
  onSettingsChange: (settings: CameraSettings) => void;
  onStatusChange: (status: CameraStatus) => void;
}

// Features:
// - Camera settings
// - Status controls
// - Detection settings
// - Recording options
```

#### CameraSettings
```typescript
interface CameraSettingsProps {
  camera: Camera;
  onSave: (settings: CameraSettings) => void;
  onCancel: () => void;
}

// Features:
// - Settings form
// - Validation
// - Save/cancel actions
// - Real-time preview
```

#### CameraManagement
```typescript
interface CameraManagementProps {
  cameras: Camera[];
  onAddCamera: (camera: NewCamera) => void;
  onEditCamera: (camera: Camera) => void;
  onDeleteCamera: (cameraId: string) => void;
}

// Features:
// - Camera list
// - Add/edit/delete actions
// - Bulk operations
// - Search and filter
```

### 4. Analytics Components

#### RealTimeChart
```typescript
interface RealTimeChartProps {
  data: RealTimeData[];
  timeRange: TimeRange;
  onTimeRangeChange: (range: TimeRange) => void;
  height?: number;
}

// Features:
// - Real-time line chart
// - Time range selector
// - Auto-refresh
// - Zoom and pan
```

#### HistoricalChart
```typescript
interface HistoricalChartProps {
  data: HistoricalData[];
  chartType: 'line' | 'bar' | 'area';
  timeRange: TimeRange;
  onChartTypeChange: (type: string) => void;
}

// Features:
// - Historical data visualization
// - Multiple chart types
// - Time range filtering
// - Data export
```

#### PeakHoursChart
```typescript
interface PeakHoursChartProps {
  data: PeakHoursData[];
  date: string;
  onDateChange: (date: string) => void;
}

// Features:
// - Peak hours visualization
// - Hourly breakdown
// - Recommendations
// - Comparison views
```

#### MetricsCards
```typescript
interface MetricsCardsProps {
  metrics: {
    totalPeopleIn: number;
    totalPeopleOut: number;
    peakOccupancy: number;
    averageOccupancy: number;
  };
  isLoading?: boolean;
}

// Features:
// - Key metrics display
// - Trend indicators
// - Color coding
// - Responsive layout
```

#### ReportGenerator
```typescript
interface ReportGeneratorProps {
  reportType: 'people-count' | 'peak-hours';
  timeRange: TimeRange;
  cameras: string[];
  onGenerate: (params: ReportParams) => void;
  onExport: (format: 'pdf' | 'excel') => void;
}

// Features:
// - Report configuration
// - Parameter selection
// - Preview generation
// - Export options
```

#### DataTable
```typescript
interface DataTableProps {
  data: any[];
  columns: Column[];
  pagination?: PaginationConfig;
  sorting?: SortingConfig;
  filtering?: FilterConfig;
  onRowClick?: (row: any) => void;
}

// Features:
// - Sortable columns
// - Pagination
// - Filtering
// - Row selection
// - Export functionality
```

#### ExportOptions
```typescript
interface ExportOptionsProps {
  formats: ('pdf' | 'excel' | 'csv')[];
  onExport: (format: string) => void;
  isLoading?: boolean;
}

// Features:
// - Format selection
// - Export progress
// - Download links
// - Error handling
```

#### FilterPanel
```typescript
interface FilterPanelProps {
  filters: Filter[];
  onFilterChange: (filters: Filter[]) => void;
  onReset: () => void;
}

// Features:
// - Multiple filter types
// - Date range picker
// - Camera selection
// - Filter presets
```

### 5. Alert Components

#### AlertList
```typescript
interface AlertListProps {
  alerts: Alert[];
  onAlertClick: (alert: Alert) => void;
  onMarkAsRead: (alertId: string) => void;
  onDelete: (alertId: string) => void;
  filters?: AlertFilters;
}

// Features:
// - Alert list display
// - Severity filtering
// - Read/unread status
// - Bulk actions
```

#### NotificationCenter
```typescript
interface NotificationCenterProps {
  notifications: Notification[];
  onNotificationClick: (notification: Notification) => void;
  onMarkAllRead: () => void;
  onClearAll: () => void;
}

// Features:
// - Notification list
// - Real-time updates
// - Mark as read
// - Clear all
```

### 6. Settings Components

#### Profile
```typescript
interface ProfileProps {
  user: User;
  onUpdate: (userData: Partial<User>) => void;
  onPasswordChange: (passwordData: PasswordChange) => void;
}

// Features:
// - User profile form
// - Password change
// - Avatar upload
// - Validation
```

#### SystemSettings
```typescript
interface SystemSettingsProps {
  settings: SystemSettings;
  onSave: (settings: SystemSettings) => void;
}

// Features:
// - System configuration
// - Detection settings
// - Alert preferences
// - Data retention
```

#### DetectionSettings
```typescript
interface DetectionSettingsProps {
  settings: DetectionSettings;
  onSave: (settings: DetectionSettings) => void;
}

// Features:
// - AI model settings
// - Sensitivity controls
// - Zone configuration
// - Performance tuning
```

## Component Patterns

### 1. Container/Presentational Pattern
```typescript
// Container Component
const DashboardContainer = () => {
  const { data, loading, error } = useDashboardData();
  
  if (loading) return <Loading />;
  if (error) return <ErrorBoundary error={error} />;
  
  return <Dashboard data={data} />;
};

// Presentational Component
const Dashboard = ({ data }) => {
  return (
    <div>
      <LiveCounters data={data.counters} />
      <CameraGrid cameras={data.cameras} />
      <QuickStats stats={data.stats} />
    </div>
  );
};
```

### 2. Custom Hooks Pattern
```typescript
const useCameraData = (cameraId: string) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  useEffect(() => {
    // Data fetching logic
  }, [cameraId]);
  
  return { data, loading, error };
};
```

### 3. Higher-Order Component Pattern
```typescript
const withAuthentication = (Component: React.ComponentType) => {
  return (props: any) => {
    const { isAuthenticated } = useAuth();
    
    if (!isAuthenticated) {
      return <Redirect to="/login" />;
    }
    
    return <Component {...props} />;
  };
};
```

## Styling Approach

### 1. Material-UI Theme
```typescript
const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
  },
});
```

### 2. Component Styling
```typescript
const useStyles = makeStyles((theme) => ({
  root: {
    padding: theme.spacing(2),
  },
  card: {
    minHeight: 200,
  },
  chart: {
    height: 400,
  },
}));
```

### 3. Responsive Design
```typescript
const useResponsive = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  const isTablet = useMediaQuery(theme.breakpoints.down('md'));
  
  return { isMobile, isTablet };
};
```

## Performance Optimization

### 1. React.memo
```typescript
const LiveCounters = React.memo(({ data }) => {
  return (
    <div>
      <Counter value={data.currentCount} />
      <Counter value={data.peopleIn} />
      <Counter value={data.peopleOut} />
    </div>
  );
});
```

### 2. useMemo
```typescript
const processedData = useMemo(() => {
  return data.map(item => ({
    ...item,
    percentage: (item.value / total) * 100
  }));
}, [data, total]);
```

### 3. useCallback
```typescript
const handleFilterChange = useCallback((filters) => {
  setFilters(filters);
}, []);
```

## Error Handling

### 1. Error Boundaries
```typescript
class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }
  
  static getDerivedStateFromError(error) {
    return { hasError: true };
  }
  
  componentDidCatch(error, errorInfo) {
    console.error('Error caught by boundary:', error, errorInfo);
  }
  
  render() {
    if (this.state.hasError) {
      return <ErrorFallback />;
    }
    
    return this.props.children;
  }
}
```

### 2. Loading States
```typescript
const DataComponent = () => {
  const { data, loading, error } = useData();
  
  if (loading) return <Loading />;
  if (error) return <ErrorMessage error={error} />;
  
  return <DataDisplay data={data} />;
};
```

## Testing Strategy

### 1. Unit Tests
```typescript
describe('LiveCounters', () => {
  it('should display correct counts', () => {
    const data = {
      currentCount: 45,
      peopleIn: 1234,
      peopleOut: 1189
    };
    
    render(<LiveCounters data={data} />);
    
    expect(screen.getByText('45')).toBeInTheDocument();
    expect(screen.getByText('1,234')).toBeInTheDocument();
    expect(screen.getByText('1,189')).toBeInTheDocument();
  });
});
```

### 2. Integration Tests
```typescript
describe('Dashboard Integration', () => {
  it('should load and display dashboard data', async () => {
    render(<Dashboard />);
    
    await waitFor(() => {
      expect(screen.getByText('Live Counters')).toBeInTheDocument();
    });
  });
});
```

### 3. E2E Tests
```typescript
describe('Dashboard E2E', () => {
  it('should navigate through dashboard sections', () => {
    cy.visit('/dashboard');
    cy.get('[data-testid="camera-grid"]').should('be.visible');
    cy.get('[data-testid="analytics-link"]').click();
    cy.url().should('include', '/analytics');
  });
});
``` 