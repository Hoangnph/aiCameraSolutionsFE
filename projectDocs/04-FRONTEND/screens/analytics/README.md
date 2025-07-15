# Analytics Screen Documentation

## Overview
Analytics screen provides comprehensive data analysis and reporting capabilities for the AI Camera Counting System, offering insights into people counting patterns, system performance, and business intelligence.

## Screen Requirements

### Functional Requirements
- Interactive data visualization charts
- Customizable date range selection
- Multi-camera data comparison
- Export reports in multiple formats
- Real-time data updates
- Trend analysis and forecasting
- Performance metrics dashboard
- Custom report builder
- Data filtering and segmentation
- Scheduled report generation

### Non-Functional Requirements
- Chart rendering: < 1 second for standard charts
- Data loading: < 3 seconds for large datasets
- Responsive design: Mobile-first approach
- Accessibility: WCAG 2.1 AA compliance
- Cross-browser compatibility
- Offline capability for cached reports

## Design Specifications

### Layout Structure
```
┌─────────────────────────────────────────────────────────────┐
│ Header (Title, Date Range, Export Button)                  │
├─────────────────────────────────────────────────────────────┤
│ Filter Bar (Cameras, Time Period, Metrics)                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────┐ ┌─────────────────────────────────┐ │
│  │   Key Metrics       │ │        Time Series Chart        │ │
│  │ ┌─────────────────┐ │ │ ┌─────────────────────────────┐ │ │
│  │ │ Total Count     │ │ │ │                             │ │ │
│  │ │ [Large Number]  │ │ │ │     [Line Chart Area]       │ │ │
│  │ └─────────────────┘ │ │ │                             │ │ │
│  │ ┌─────────────────┐ │ │ └─────────────────────────────┘ │ │
│  │ │ Peak Hour       │ │ │                                 │ │
│  │ │ [Time Display]  │ │ │  ┌─────────────────────────────┐ │ │
│  │ └─────────────────┘ │ │  │     Comparison Chart        │ │ │
│  │ ┌─────────────────┐ │ │  │   [Bar/Column Chart]        │ │ │
│  │ │ Avg Daily       │ │ │  └─────────────────────────────┘ │ │
│  │ │ [Number]        │ │ │                                 │ │
│  │ └─────────────────┘ │ │                                 │ │
│  └─────────────────────┘ └─────────────────────────────────┘ │
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                    Distribution Charts                  │ │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐      │ │
│  │  │ Hourly Dist │ │ Daily Dist  │ │ Camera Dist │      │ │
│  │  │ [Pie Chart] │ │ [Bar Chart] │ │ [Heat Map]  │      │ │
│  │  └─────────────┘ └─────────────┘ └─────────────┘      │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                    Data Table                           │ │
│  │  [Sortable columns, Pagination, Export options]        │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Visual Design
- **Color Scheme**: 
  - Primary: #1976d2 (Blue)
  - Secondary: #dc004e (Pink)
  - Success: #2e7d32 (Green)
  - Warning: #ed6c02 (Orange)
  - Error: #d32f2f (Red)
  - Neutral: #757575 (Gray)
- **Typography**: Roboto font family with hierarchy
- **Spacing**: 16px base unit, consistent grid
- **Shadows**: Material Design elevation levels
- **Animations**: Smooth transitions (200-300ms)

### Responsive Breakpoints
- **Mobile**: < 768px - Single column, stacked charts
- **Tablet**: 768px - 1024px - 2-column layout
- **Desktop**: > 1024px - Multi-column layout
- **Large Desktop**: > 1440px - Expanded layout with sidebars

## Components

### Core Components
1. **AnalyticsContainer** - Main wrapper with layout
2. **MetricsCards** - Key performance indicators
3. **ChartContainer** - Chart wrapper with controls
4. **DataTable** - Tabular data display
5. **FilterPanel** - Advanced filtering controls
6. **ExportPanel** - Report export functionality
7. **DateRangePicker** - Time period selection
8. **ReportBuilder** - Custom report creation

### Chart Components
- **LineChart** - Time series data visualization
- **BarChart** - Comparative data display
- **PieChart** - Distribution analysis
- **HeatMap** - Multi-dimensional data
- **GaugeChart** - Performance indicators
- **ScatterPlot** - Correlation analysis
- **AreaChart** - Cumulative data trends
- **CandlestickChart** - Range data visualization

### Interactive Components
- **ChartTooltip** - Interactive data tooltips
- **ChartLegend** - Chart legend with controls
- **ZoomControls** - Chart zoom and pan
- **DrillDown** - Data exploration controls
- **ChartExport** - Individual chart export
- **DataFilter** - Real-time data filtering

## Data Management

### Analytics Data Structure
```typescript
interface AnalyticsData {
  metrics: KeyMetrics;
  timeSeries: TimeSeriesData[];
  distributions: DistributionData[];
  comparisons: ComparisonData[];
  trends: TrendData[];
  performance: PerformanceMetrics;
}

interface KeyMetrics {
  totalCount: number;
  averageDaily: number;
  peakHour: string;
  peakCount: number;
  growthRate: number;
  accuracy: number;
  uptime: number;
}

interface TimeSeriesData {
  timestamp: Date;
  count: number;
  cameraId: string;
  location: string;
  category?: string;
}

interface DistributionData {
  category: string;
  value: number;
  percentage: number;
  color: string;
}

interface ComparisonData {
  label: string;
  current: number;
  previous: number;
  change: number;
  changePercent: number;
}
```

### API Endpoints
```typescript
// Get analytics data
GET /api/analytics
Query params: startDate, endDate, cameras, metrics, groupBy

// Get time series data
GET /api/analytics/timeseries
Query params: startDate, endDate, cameras, interval

// Get distribution data
GET /api/analytics/distribution
Query params: startDate, endDate, cameras, dimension

// Get comparison data
GET /api/analytics/comparison
Query params: startDate, endDate, compareDate, cameras

// Export report
POST /api/analytics/export
Body: { format: 'pdf' | 'excel' | 'csv', data: AnalyticsData }

// Get custom report
GET /api/analytics/reports/:id
```

### Data Fetching Strategy
```typescript
// Fetch analytics data with caching
const useAnalyticsData = (filters: AnalyticsFilters) => {
  return useQuery(
    ['analytics', filters],
    () => fetchAnalyticsData(filters),
    {
      staleTime: 5 * 60 * 1000, // 5 minutes
      cacheTime: 30 * 60 * 1000, // 30 minutes
      refetchInterval: 60 * 1000, // 1 minute
    }
  );
};

// Real-time updates for live data
const useRealTimeAnalytics = (filters: AnalyticsFilters) => {
  const [data, setData] = useState<AnalyticsData | null>(null);
  
  useEffect(() => {
    const ws = new WebSocket(WS_URL);
    
    ws.onmessage = (event) => {
      const update = JSON.parse(event.data);
      setData(prev => mergeAnalyticsData(prev, update));
    };
    
    return () => ws.close();
  }, [filters]);
  
  return data;
};
```

## Chart Configuration

### Chart.js Configuration
```typescript
interface ChartConfig {
  type: ChartType;
  data: ChartData;
  options: ChartOptions;
  plugins?: ChartPlugin[];
}

interface ChartOptions {
  responsive: boolean;
  maintainAspectRatio: boolean;
  animation: {
    duration: number;
    easing: string;
  };
  interaction: {
    mode: 'index' | 'dataset' | 'point' | 'nearest' | 'x' | 'y';
    intersect: boolean;
  };
  scales?: {
    x?: ScaleOptions;
    y?: ScaleOptions;
  };
  plugins?: {
    legend?: LegendOptions;
    tooltip?: TooltipOptions;
    zoom?: ZoomOptions;
  };
}

// Example Line Chart Configuration
const lineChartConfig: ChartConfig = {
  type: 'line',
  data: {
    labels: timeLabels,
    datasets: [{
      label: 'People Count',
      data: countData,
      borderColor: '#1976d2',
      backgroundColor: 'rgba(25, 118, 210, 0.1)',
      fill: true,
      tension: 0.4
    }]
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    interaction: {
      mode: 'index',
      intersect: false,
    },
    scales: {
      x: {
        type: 'time',
        time: {
          unit: 'hour'
        }
      },
      y: {
        beginAtZero: true
      }
    }
  }
};
```

### Custom Chart Components
```typescript
// Reusable chart component
const AnalyticsChart: React.FC<ChartProps> = ({
  type,
  data,
  options,
  height = 400,
  onDataPointClick
}) => {
  const chartRef = useRef<HTMLCanvasElement>(null);
  const chartInstance = useRef<Chart | null>(null);
  
  useEffect(() => {
    if (chartRef.current) {
      const ctx = chartRef.current.getContext('2d');
      if (ctx) {
        chartInstance.current = new Chart(ctx, {
          type,
          data,
          options: {
            ...options,
            onClick: (event, elements) => {
              if (elements.length > 0 && onDataPointClick) {
                onDataPointClick(elements[0]);
              }
            }
          }
        });
      }
    }
    
    return () => {
      if (chartInstance.current) {
        chartInstance.current.destroy();
      }
    };
  }, [type, data, options]);
  
  return <canvas ref={chartRef} height={height} />;
};
```

## Data Visualization Types

### Time Series Analysis
- **Hourly Trends**: People count by hour
- **Daily Patterns**: Daily traffic patterns
- **Weekly Cycles**: Weekly recurring patterns
- **Monthly Trends**: Long-term trends
- **Seasonal Analysis**: Seasonal variations

### Comparative Analysis
- **Camera Comparison**: Performance across cameras
- **Period Comparison**: Current vs previous periods
- **Location Analysis**: Performance by location
- **Category Comparison**: Different metrics comparison

### Distribution Analysis
- **Hourly Distribution**: Peak hours identification
- **Daily Distribution**: Busiest days
- **Camera Distribution**: Load distribution
- **Geographic Distribution**: Location-based patterns

### Performance Metrics
- **Accuracy Metrics**: Detection accuracy rates
- **Uptime Statistics**: System availability
- **Response Times**: Detection response times
- **Error Rates**: System error frequencies

## Filtering and Segmentation

### Filter Options
```typescript
interface AnalyticsFilters {
  dateRange: {
    start: Date;
    end: Date;
  };
  cameras: string[];
  locations: string[];
  timeGranularity: 'hour' | 'day' | 'week' | 'month';
  metrics: string[];
  groupBy: 'camera' | 'location' | 'time' | 'category';
  excludeOutliers: boolean;
  customFilters: CustomFilter[];
}

interface CustomFilter {
  field: string;
  operator: 'equals' | 'greater' | 'less' | 'contains' | 'between';
  value: any;
  value2?: any;
}
```

### Advanced Filtering
- **Date Range**: Custom date selection
- **Camera Selection**: Multi-camera filtering
- **Location Filtering**: Geographic filtering
- **Time Granularity**: Data aggregation level
- **Metric Selection**: Specific metrics focus
- **Outlier Exclusion**: Remove anomalous data

## Export and Reporting

### Export Formats
```typescript
enum ExportFormat {
  PDF = 'pdf',
  EXCEL = 'excel',
  CSV = 'csv',
  JSON = 'json',
  PNG = 'png',
  SVG = 'svg'
}

interface ExportOptions {
  format: ExportFormat;
  includeCharts: boolean;
  includeData: boolean;
  includeMetadata: boolean;
  filename: string;
  compression: boolean;
}
```

### Report Generation
```typescript
const generateReport = async (options: ExportOptions): Promise<Blob> => {
  const response = await api.post('/analytics/export', {
    format: options.format,
    data: currentAnalyticsData,
    options: {
      includeCharts: options.includeCharts,
      includeData: options.includeData,
      includeMetadata: options.includeMetadata
    }
  });
  
  return response.data;
};

const downloadReport = async (options: ExportOptions) => {
  const blob = await generateReport(options);
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = options.filename;
  link.click();
  URL.revokeObjectURL(url);
};
```

### Scheduled Reports
- **Daily Reports**: Automated daily summaries
- **Weekly Reports**: Weekly performance summaries
- **Monthly Reports**: Monthly trend analysis
- **Custom Schedules**: User-defined schedules
- **Email Delivery**: Automated email delivery

## Performance Optimization

### Data Loading
- **Lazy Loading**: Load charts on demand
- **Progressive Loading**: Load data in chunks
- **Caching Strategy**: Cache frequently accessed data
- **Data Compression**: Compress large datasets

### Chart Rendering
- **Virtual Scrolling**: For large datasets
- **Canvas Optimization**: Optimize chart rendering
- **Memory Management**: Clean up chart instances
- **Throttling**: Limit update frequency

### Real-Time Updates
- **WebSocket Connection**: Real-time data streaming
- **Update Batching**: Group multiple updates
- **Delta Updates**: Only update changed data
- **Connection Management**: Auto-reconnect handling

## Accessibility Features

### Chart Accessibility
- **ARIA Labels**: Descriptive chart labels
- **Keyboard Navigation**: Navigate chart elements
- **Screen Reader Support**: Chart data descriptions
- **High Contrast**: High contrast mode support

### Data Accessibility
- **Alternative Text**: Text descriptions for charts
- **Data Tables**: Tabular data for screen readers
- **Focus Indicators**: Clear focus indicators
- **Error Announcements**: Error state announcements

## Testing Strategy

### Unit Tests
- Chart component rendering
- Data transformation functions
- Filter logic testing
- Export functionality

### Integration Tests
- API integration testing
- Real-time data updates
- Chart interactions
- Export generation

### E2E Tests
- Complete analytics workflow
- Chart interactions
- Filter applications
- Report generation

### Performance Tests
- Large dataset handling
- Chart rendering performance
- Real-time update performance
- Export generation speed

## Implementation Checklist

### Phase 1: Core Structure
- [ ] Create AnalyticsContainer component
- [ ] Implement chart wrapper components
- [ ] Set up data fetching infrastructure
- [ ] Create basic chart components

### Phase 2: Data Visualization
- [ ] Implement line charts for time series
- [ ] Create bar charts for comparisons
- [ ] Add pie charts for distributions
- [ ] Implement heat maps

### Phase 3: Interactivity
- [ ] Add chart tooltips and interactions
- [ ] Implement filtering system
- [ ] Create drill-down functionality
- [ ] Add zoom and pan controls

### Phase 4: Advanced Features
- [ ] Implement export functionality
- [ ] Add custom report builder
- [ ] Create scheduled reports
- [ ] Add real-time updates

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
    "chart.js": "^4.2.0",
    "react-chartjs-2": "^5.2.0",
    "chartjs-adapter-date-fns": "^2.0.0",
    "chartjs-plugin-zoom": "^2.0.0",
    "@mui/material": "^5.11.0",
    "@mui/icons-material": "^5.11.0",
    "date-fns": "^2.29.0",
    "socket.io-client": "^4.6.0"
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
screens/analytics/
├── README.md
├── index.tsx
├── components/
│   ├── AnalyticsContainer.tsx
│   ├── MetricsCards.tsx
│   ├── ChartContainer.tsx
│   ├── DataTable.tsx
│   ├── FilterPanel.tsx
│   ├── ExportPanel.tsx
│   ├── DateRangePicker.tsx
│   └── ReportBuilder.tsx
├── charts/
│   ├── LineChart.tsx
│   ├── BarChart.tsx
│   ├── PieChart.tsx
│   ├── HeatMap.tsx
│   ├── GaugeChart.tsx
│   ├── ScatterPlot.tsx
│   ├── AreaChart.tsx
│   └── CandlestickChart.tsx
├── hooks/
│   ├── useAnalyticsData.ts
│   ├── useRealTimeAnalytics.ts
│   └── useChartInteractions.ts
├── utils/
│   ├── dataTransformers.ts
│   ├── chartHelpers.ts
│   ├── exportHelpers.ts
│   └── filterHelpers.ts
├── types/
│   └── analytics.types.ts
├── styles/
│   └── analytics.styles.ts
└── tests/
    ├── AnalyticsContainer.test.tsx
    ├── LineChart.test.tsx
    └── DataTable.test.tsx
```

## Status Tracking

### Development Status: 🟡 In Progress
- **Started**: [Date]
- **Estimated Completion**: [Date]
- **Current Phase**: Phase 1 - Core Structure
- **Next Milestone**: Data Visualization

### Review Status
- **Design Review**: ⏳ Pending
- **Code Review**: ⏳ Pending
- **QA Testing**: ⏳ Pending
- **Performance Review**: ⏳ Pending

### Dependencies
- **Backend API**: ✅ Ready
- **Chart Library**: ✅ Ready
- **Design System**: ✅ Ready
- **Testing Framework**: ✅ Ready 