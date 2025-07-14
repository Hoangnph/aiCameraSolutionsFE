# UI/UX Specifications - AI Camera Counting System

## 📋 Table of Contents
1. [Design System](#design-system)
2. [Component Specifications](#component-specifications)
3. [Page Layouts](#page-layouts)
4. [User Flows](#user-flows)
5. [Responsive Design](#responsive-design)
6. [Accessibility](#accessibility)
7. [Wireframes](#wireframes)
8. [Design Guidelines](#design-guidelines)

## 🎨 Design System

### Color Palette
```css
/* Primary Colors */
--primary-50: #eff6ff;
--primary-100: #dbeafe;
--primary-500: #3b82f6;
--primary-600: #2563eb;
--primary-700: #1d4ed8;
--primary-900: #1e3a8a;

/* Secondary Colors */
--secondary-50: #f8fafc;
--secondary-100: #f1f5f9;
--secondary-500: #64748b;
--secondary-600: #475569;
--secondary-700: #334155;

/* Success Colors */
--success-50: #f0fdf4;
--success-500: #22c55e;
--success-600: #16a34a;
--success-700: #15803d;

/* Warning Colors */
--warning-50: #fffbeb;
--warning-500: #f59e0b;
--warning-600: #d97706;
--warning-700: #b45309;

/* Error Colors */
--error-50: #fef2f2;
--error-500: #ef4444;
--error-600: #dc2626;
--error-700: #b91c1c;

/* Neutral Colors */
--white: #ffffff;
--black: #000000;
--gray-50: #f9fafb;
--gray-100: #f3f4f6;
--gray-200: #e5e7eb;
--gray-300: #d1d5db;
--gray-400: #9ca3af;
--gray-500: #6b7280;
--gray-600: #4b5563;
--gray-700: #374151;
--gray-800: #1f2937;
--gray-900: #111827;
```

### Typography
```css
/* Font Family */
--font-family-primary: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
--font-family-mono: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;

/* Font Sizes */
--text-xs: 0.75rem;    /* 12px */
--text-sm: 0.875rem;   /* 14px */
--text-base: 1rem;     /* 16px */
--text-lg: 1.125rem;   /* 18px */
--text-xl: 1.25rem;    /* 20px */
--text-2xl: 1.5rem;    /* 24px */
--text-3xl: 1.875rem;  /* 30px */
--text-4xl: 2.25rem;   /* 36px */
--text-5xl: 3rem;      /* 48px */

/* Font Weights */
--font-light: 300;
--font-normal: 400;
--font-medium: 500;
--font-semibold: 600;
--font-bold: 700;
--font-extrabold: 800;

/* Line Heights */
--leading-tight: 1.25;
--leading-normal: 1.5;
--leading-relaxed: 1.75;
```

### Spacing System
```css
/* Spacing Scale */
--space-0: 0;
--space-1: 0.25rem;   /* 4px */
--space-2: 0.5rem;    /* 8px */
--space-3: 0.75rem;   /* 12px */
--space-4: 1rem;      /* 16px */
--space-5: 1.25rem;   /* 20px */
--space-6: 1.5rem;    /* 24px */
--space-8: 2rem;      /* 32px */
--space-10: 2.5rem;   /* 40px */
--space-12: 3rem;     /* 48px */
--space-16: 4rem;     /* 64px */
--space-20: 5rem;     /* 80px */
--space-24: 6rem;     /* 96px */
```

### Border Radius
```css
--radius-none: 0;
--radius-sm: 0.125rem;   /* 2px */
--radius-base: 0.25rem;  /* 4px */
--radius-md: 0.375rem;   /* 6px */
--radius-lg: 0.5rem;     /* 8px */
--radius-xl: 0.75rem;    /* 12px */
--radius-2xl: 1rem;      /* 16px */
--radius-full: 9999px;
```

### Shadows
```css
--shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
--shadow-base: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
--shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
--shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
--shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);
```

## 🧩 Component Specifications

### Button Components

#### Primary Button
```jsx
// Primary Button
<Button variant="primary" size="md">
  Add Camera
</Button>

// Specifications
- Background: var(--primary-600)
- Text Color: var(--white)
- Hover: var(--primary-700)
- Active: var(--primary-800)
- Border: none
- Border Radius: var(--radius-md)
- Padding: var(--space-3) var(--space-4)
- Font Weight: var(--font-medium)
- Transition: all 0.2s ease-in-out
```

#### Secondary Button
```jsx
// Secondary Button
<Button variant="secondary" size="md">
  Cancel
</Button>

// Specifications
- Background: var(--white)
- Text Color: var(--gray-700)
- Border: 1px solid var(--gray-300)
- Hover: var(--gray-50)
- Active: var(--gray-100)
- Border Radius: var(--radius-md)
- Padding: var(--space-3) var(--space-4)
- Font Weight: var(--font-medium)
```

#### Danger Button
```jsx
// Danger Button
<Button variant="danger" size="md">
  Delete Camera
</Button>

// Specifications
- Background: var(--error-600)
- Text Color: var(--white)
- Hover: var(--error-700)
- Active: var(--error-800)
- Border: none
- Border Radius: var(--radius-md)
- Padding: var(--space-3) var(--space-4)
- Font Weight: var(--font-medium)
```

### Form Components

#### Input Field
```jsx
// Input Field
<Input
  type="text"
  placeholder="Enter camera name"
  label="Camera Name"
  required
/>

// Specifications
- Border: 1px solid var(--gray-300)
- Border Radius: var(--radius-md)
- Padding: var(--space-3)
- Font Size: var(--text-base)
- Focus: border-color var(--primary-500), box-shadow var(--shadow-sm)
- Error: border-color var(--error-500)
- Success: border-color var(--success-500)
```

#### Select Dropdown
```jsx
// Select Dropdown
<Select
  options={[
    { value: 'active', label: 'Active' },
    { value: 'inactive', label: 'Inactive' }
  ]}
  placeholder="Select status"
  label="Status"
/>

// Specifications
- Border: 1px solid var(--gray-300)
- Border Radius: var(--radius-md)
- Padding: var(--space-3)
- Background: var(--white)
- Dropdown Arrow: var(--gray-400)
- Focus: border-color var(--primary-500)
```

### Card Components

#### Camera Card
```jsx
// Camera Card
<CameraCard
  camera={camera}
  onEdit={handleEdit}
  onDelete={handleDelete}
/>

// Specifications
- Background: var(--white)
- Border: 1px solid var(--gray-200)
- Border Radius: var(--radius-lg)
- Padding: var(--space-6)
- Shadow: var(--shadow-sm)
- Hover: var(--shadow-md)
- Transition: all 0.2s ease-in-out
```

#### Statistics Card
```jsx
// Statistics Card
<StatisticsCard
  title="Total Count"
  value="1,234"
  change="+12%"
  trend="up"
/>

// Specifications
- Background: var(--white)
- Border: 1px solid var(--gray-200)
- Border Radius: var(--radius-lg)
- Padding: var(--space-6)
- Shadow: var(--shadow-sm)
- Title: var(--text-sm), var(--gray-600)
- Value: var(--text-3xl), var(--font-bold)
- Change: var(--text-sm), var(--success-600) or var(--error-600)
```

### Table Components

#### Data Table
```jsx
// Data Table
<DataTable
  columns={columns}
  data={cameras}
  pagination={true}
  search={true}
/>

// Specifications
- Background: var(--white)
- Border: 1px solid var(--gray-200)
- Border Radius: var(--radius-lg)
- Header: var(--gray-50), var(--font-semibold)
- Row Hover: var(--gray-50)
- Border: 1px solid var(--gray-200) between rows
- Pagination: var(--space-4) margin top
```

## 📱 Page Layouts

### Dashboard Layout
```jsx
// Dashboard Layout
<DashboardLayout>
  <Sidebar />
  <MainContent>
    <Header />
    <PageContent>
      <StatisticsGrid />
      <RecentActivity />
      <CameraMap />
    </PageContent>
  </MainContent>
</DashboardLayout>

// Specifications
- Sidebar Width: 280px (collapsed: 64px)
- Header Height: 64px
- Main Content: flex-1
- Background: var(--gray-50)
- Content Padding: var(--space-6)
```

### Camera Management Layout
```jsx
// Camera Management Layout
<CameraManagementLayout>
  <PageHeader title="Camera Management" />
  <Toolbar>
    <SearchInput />
    <FilterDropdown />
    <AddCameraButton />
  </Toolbar>
  <CameraGrid />
  <Pagination />
</CameraManagementLayout>

// Specifications
- Page Header: var(--space-6) padding
- Toolbar: var(--space-4) padding, var(--gray-100) background
- Camera Grid: var(--space-6) gap
- Pagination: var(--space-6) margin top
```

### Camera Detail Layout
```jsx
// Camera Detail Layout
<CameraDetailLayout>
  <PageHeader title="Camera Details" backButton />
  <ContentGrid>
    <CameraInfo />
    <LiveStream />
    <CountHistory />
    <Settings />
  </ContentGrid>
</CameraDetailLayout>

// Specifications
- Content Grid: 2 columns (desktop), 1 column (mobile)
- Gap: var(--space-6)
- Live Stream: 16:9 aspect ratio
- Count History: 400px height
```

## 🔄 User Flows

### Camera Setup Flow
```
1. User clicks "Add Camera"
2. Form opens with camera details
3. User fills in required fields:
   - Camera name
   - IP address
   - Port
   - Username/Password
4. System validates connection
5. User configures detection settings
6. Camera is activated
7. Success message displayed
```

### Alert Management Flow
```
1. User receives alert notification
2. Clicks on alert to view details
3. Alert details page opens
4. User can:
   - Acknowledge alert
   - Resolve alert
   - Add notes
   - Escalate if needed
5. Alert status updated
6. Notification sent to relevant parties
```

### Analytics Review Flow
```
1. User navigates to Analytics page
2. Selects date range and filters
3. System loads analytics data
4. User views:
   - Count trends
   - Peak hours
   - Camera performance
   - Anomalies
5. User can export data
6. User can set up alerts
```

## 📱 Responsive Design

### Breakpoints
```css
/* Mobile First Approach */
--breakpoint-sm: 640px;   /* Small tablets */
--breakpoint-md: 768px;   /* Tablets */
--breakpoint-lg: 1024px;  /* Laptops */
--breakpoint-xl: 1280px;  /* Desktop */
--breakpoint-2xl: 1536px; /* Large Desktop */
```

### Mobile Adaptations
```jsx
// Mobile Navigation
<MobileNavigation>
  <BottomNavigation>
    <NavItem icon="dashboard" label="Dashboard" />
    <NavItem icon="camera" label="Cameras" />
    <NavItem icon="analytics" label="Analytics" />
    <NavItem icon="settings" label="Settings" />
  </BottomNavigation>
</MobileNavigation>

// Specifications
- Bottom Navigation: fixed bottom, var(--white) background
- Icon Size: 24px
- Label: var(--text-xs)
- Active: var(--primary-600)
- Inactive: var(--gray-400)
```

### Tablet Adaptations
```jsx
// Tablet Layout
<TabletLayout>
  <Sidebar collapsed />
  <MainContent>
    <Header />
    <Content />
  </MainContent>
</TabletLayout>

// Specifications
- Sidebar: collapsed by default, expandable
- Content: full width
- Cards: 2 columns
- Tables: scrollable horizontally
```

## ♿ Accessibility

### WCAG 2.1 AA Compliance
```jsx
// Accessible Button
<Button
  aria-label="Add new camera"
  aria-describedby="camera-help"
  onClick={handleAddCamera}
>
  Add Camera
</Button>

// Specifications
- Color Contrast: 4.5:1 minimum
- Focus Indicators: visible and clear
- Keyboard Navigation: full support
- Screen Reader: proper ARIA labels
- Alternative Text: for all images
```

### Keyboard Navigation
```jsx
// Keyboard Navigation
<div role="navigation" aria-label="Main navigation">
  <a href="/dashboard" tabIndex="0">Dashboard</a>
  <a href="/cameras" tabIndex="0">Cameras</a>
  <a href="/analytics" tabIndex="0">Analytics</a>
</div>

// Specifications
- Tab Order: logical and intuitive
- Skip Links: for main content
- Focus Management: proper focus handling
- Keyboard Shortcuts: for common actions
```

### Screen Reader Support
```jsx
// Screen Reader Support
<div role="main" aria-labelledby="page-title">
  <h1 id="page-title">Camera Management</h1>
  <div role="region" aria-label="Camera list">
    {cameras.map(camera => (
      <div key={camera.id} role="article" aria-label={`Camera ${camera.name}`}>
        {/* Camera content */}
      </div>
    ))}
  </div>
</div>

// Specifications
- Semantic HTML: proper use of HTML elements
- ARIA Labels: descriptive and helpful
- Live Regions: for dynamic content
- Status Messages: for user feedback
```

## 🎨 Wireframes

### Dashboard Wireframe
```
┌─────────────────────────────────────────────────────────┐
│ Header: Logo | Search | Notifications | User Menu      │
├─────────────┬───────────────────────────────────────────┤
│ Sidebar     │ Main Content                              │
│ • Dashboard │ ┌─────────────┬─────────────┬─────────────┐ │
│ • Cameras   │ │ Stats Card  │ Stats Card  │ Stats Card  │ │
│ • Analytics │ │ Total Count │ Active Cam  │ Today Count │ │
│ • Settings  │ └─────────────┴─────────────┴─────────────┘ │
│             │                                             │
│             │ ┌─────────────────────────────────────────┐ │
│             │ │ Recent Activity                         │ │
│             │ │ • Camera 1: 15 people detected          │ │
│             │ │ • Camera 2: Alert triggered             │ │
│             │ │ • Camera 3: Connection restored         │ │
│             │ └─────────────────────────────────────────┘ │
│             │                                             │
│             │ ┌─────────────────────────────────────────┐ │
│             │ │ Camera Map                              │ │
│             │ │ [Interactive map with camera locations] │ │
│             │ └─────────────────────────────────────────┘ │
└─────────────┴─────────────────────────────────────────────┘
```

### Camera Management Wireframe
```
┌─────────────────────────────────────────────────────────┐
│ Header: Camera Management | Add Camera Button          │
├─────────────────────────────────────────────────────────┤
│ Toolbar: Search | Filter | Sort | View Toggle          │
├─────────────────────────────────────────────────────────┤
│ ┌─────────────┬─────────────┬─────────────┬─────────────┐ │
│ │ Camera 1    │ Camera 2    │ Camera 3    │ Camera 4    │ │
│ │ [Preview]   │ [Preview]   │ [Preview]   │ [Preview]   │ │
│ │ Name: Main  │ Name: Side  │ Name: Back  │ Name: Front │ │
│ │ Status: ✅  │ Status: ⚠️  │ Status: ❌  │ Status: ✅  │ │
│ │ Count: 45   │ Count: 12   │ Count: 0    │ Count: 78   │ │
│ │ [Edit] [Del]│ [Edit] [Del]│ [Edit] [Del]│ [Edit] [Del]│ │
│ └─────────────┴─────────────┴─────────────┴─────────────┘ │
├─────────────────────────────────────────────────────────┤
│ Pagination: < 1 2 3 ... 10 > | Showing 1-12 of 48      │
└─────────────────────────────────────────────────────────┘
```

### Camera Detail Wireframe
```
┌─────────────────────────────────────────────────────────┐
│ Header: Camera Details | Back | Edit | Delete          │
├─────────────────────────────────────────────────────────┤
│ ┌─────────────────────────┬─────────────────────────────┐ │
│ │ Camera Information      │ Live Stream                 │ │
│ │ • Name: Main Entrance   │ ┌─────────────────────────┐ │ │
│ │ • Location: Building A  │ │                         │ │
│ │ • IP: 192.168.1.100    │ │     Live Video Feed     │ │
│ │ • Status: Active        │ │                         │ │
│ │ • Last Update: 2 min    │ │                         │ │
│ │                         │ └─────────────────────────┘ │ │
│ │ Settings                │ Controls: Play | Pause | Rec│ │
│ │ • Detection Sensitivity │                             │ │
│ │ • Alert Thresholds      │ ┌─────────────────────────┐ │ │
│ │ • Recording Schedule    │ │ Count History Chart     │ │
│ │ • Notification Rules    │ │ [Line chart showing     │ │
│ │                         │ │  people count over time]│ │
│ │ [Save Settings]         │ └─────────────────────────┘ │ │
│ └─────────────────────────┴─────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

## 📋 Design Guidelines

### Visual Hierarchy
```css
/* Primary Headings */
h1 {
  font-size: var(--text-4xl);
  font-weight: var(--font-bold);
  color: var(--gray-900);
  margin-bottom: var(--space-4);
}

/* Secondary Headings */
h2 {
  font-size: var(--text-2xl);
  font-weight: var(--font-semibold);
  color: var(--gray-800);
  margin-bottom: var(--space-3);
}

/* Section Headings */
h3 {
  font-size: var(--text-xl);
  font-weight: var(--font-medium);
  color: var(--gray-700);
  margin-bottom: var(--space-2);
}
```

### Spacing Guidelines
```css
/* Component Spacing */
.component {
  margin-bottom: var(--space-6);
}

/* Section Spacing */
.section {
  margin-bottom: var(--space-8);
}

/* Page Spacing */
.page {
  padding: var(--space-6);
}

/* Card Spacing */
.card {
  padding: var(--space-6);
  margin-bottom: var(--space-4);
}
```

### Color Usage Guidelines
```css
/* Primary Actions */
.primary-action {
  background-color: var(--primary-600);
  color: var(--white);
}

/* Secondary Actions */
.secondary-action {
  background-color: var(--white);
  color: var(--gray-700);
  border: 1px solid var(--gray-300);
}

/* Success States */
.success {
  color: var(--success-600);
  background-color: var(--success-50);
}

/* Warning States */
.warning {
  color: var(--warning-600);
  background-color: var(--warning-50);
}

/* Error States */
.error {
  color: var(--error-600);
  background-color: var(--error-50);
}
```

### Animation Guidelines
```css
/* Micro-interactions */
.micro-interaction {
  transition: all 0.2s ease-in-out;
}

/* Page Transitions */
.page-transition {
  transition: opacity 0.3s ease-in-out;
}

/* Loading States */
.loading {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}
```

## 🎯 Implementation Notes

### Component Library
- Use existing MUI components as base
- Extend with custom components following design system
- Maintain consistency across all components
- Document component usage and props

### State Management
- Use React Context for global state
- Local state for component-specific data
- Optimistic updates for better UX
- Error boundaries for graceful error handling

### Performance Considerations
- Lazy load components and routes
- Optimize images and assets
- Use React.memo for expensive components
- Implement virtual scrolling for large lists

### Testing Strategy
- Unit tests for all components
- Integration tests for user flows
- Visual regression tests for UI consistency
- Accessibility tests for compliance

---

**Last Updated**: December 2024  
**Version**: 1.0.0  
**Status**: Ready for Implementation 