# 🧩 Component Library - AI Camera Counting System

## 📊 **Tổng quan Component Library**

Tài liệu này định nghĩa chi tiết component library cho hệ thống AI Camera Counting, bao gồm component specifications, usage examples, và implementation guidelines.

**🎯 Design System**: Material-UI + Custom Vui Components  
**📦 Component Types**: Atomic Design (Atoms, Molecules, Organisms)  
**🎨 Theme**: Dark theme với consistent styling  
**♿ Accessibility**: WCAG 2.1 AA compliant  

---

## 🏗️ **Component Architecture**

### **Atomic Design Structure**
```
Component Library
├── Atoms (Basic Components)
│   ├── VuiButton
│   ├── VuiInput
│   ├── VuiTypography
│   ├── VuiIcon
│   └── VuiBadge
├── Molecules (Composite Components)
│   ├── VuiCard
│   ├── VuiFormField
│   ├── VuiAlert
│   ├── VuiModal
│   └── VuiTooltip
├── Organisms (Complex Components)
│   ├── VuiNavigation
│   ├── VuiDataTable
│   ├── VuiChart
│   ├── VuiCameraGrid
│   └── VuiDashboard
└── Templates (Page Layouts)
    ├── DashboardLayout
    ├── AuthLayout
    ├── CameraLayout
    └── AnalyticsLayout
```

---

## ⚛️ **Atomic Components**

### **VuiButton Component**

#### **Component Specification**
```typescript
interface VuiButtonProps {
  variant: 'contained' | 'outlined' | 'text' | 'ghost';
  color: 'primary' | 'secondary' | 'success' | 'warning' | 'error' | 'info';
  size: 'small' | 'medium' | 'large';
  disabled?: boolean;
  loading?: boolean;
  fullWidth?: boolean;
  startIcon?: React.ReactNode;
  endIcon?: React.ReactNode;
  onClick?: (event: React.MouseEvent<HTMLButtonElement>) => void;
  children: React.ReactNode;
  className?: string;
  type?: 'button' | 'submit' | 'reset';
}

const VuiButton: React.FC<VuiButtonProps> = ({
  variant = 'contained',
  color = 'primary',
  size = 'medium',
  disabled = false,
  loading = false,
  fullWidth = false,
  startIcon,
  endIcon,
  onClick,
  children,
  className,
  type = 'button',
  ...props
}) => {
  // Component implementation
};
```

#### **Usage Examples**
```tsx
// Primary Button
<VuiButton variant="contained" color="primary" onClick={handleClick}>
  Save Changes
</VuiButton>

// Secondary Button with Icon
<VuiButton 
  variant="outlined" 
  color="secondary" 
  startIcon={<SaveIcon />}
  onClick={handleSave}
>
  Save
</VuiButton>

// Loading Button
<VuiButton 
  variant="contained" 
  loading={true}
  disabled={true}
>
  Processing...
</VuiButton>

// Full Width Button
<VuiButton 
  variant="contained" 
  fullWidth={true}
  onClick={handleSubmit}
>
  Submit Form
</VuiButton>
```

#### **Style Variants**
```css
/* Button Base Styles */
.vui-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border: none;
  border-radius: var(--radius-lg);
  font-family: var(--font-family-primary);
  font-weight: var(--font-weight-medium);
  text-decoration: none;
  cursor: pointer;
  transition: all var(--transition-normal);
  position: relative;
  overflow: hidden;
}

/* Contained Variant */
.vui-button--contained {
  background-color: var(--primary-500);
  color: white;
  box-shadow: var(--shadow-sm);
}

.vui-button--contained:hover {
  background-color: var(--primary-600);
  box-shadow: var(--shadow-md);
  transform: translateY(-1px);
}

/* Outlined Variant */
.vui-button--outlined {
  background-color: transparent;
  color: var(--primary-500);
  border: 2px solid var(--primary-500);
}

.vui-button--outlined:hover {
  background-color: var(--primary-500);
  color: white;
}

/* Size Variants */
.vui-button--small {
  padding: var(--spacing-2) var(--spacing-4);
  font-size: var(--font-size-sm);
  min-height: 32px;
}

.vui-button--medium {
  padding: var(--spacing-3) var(--spacing-6);
  font-size: var(--font-size-base);
  min-height: 40px;
}

.vui-button--large {
  padding: var(--spacing-4) var(--spacing-8);
  font-size: var(--font-size-lg);
  min-height: 48px;
}
```

### **VuiInput Component**

#### **Component Specification**
```typescript
interface VuiInputProps {
  type: 'text' | 'email' | 'password' | 'number' | 'url' | 'tel' | 'search';
  label?: string;
  placeholder?: string;
  value: string;
  onChange: (value: string) => void;
  onBlur?: () => void;
  onFocus?: () => void;
  error?: string;
  helperText?: string;
  required?: boolean;
  disabled?: boolean;
  readOnly?: boolean;
  startIcon?: React.ReactNode;
  endIcon?: React.ReactNode;
  fullWidth?: boolean;
  multiline?: boolean;
  rows?: number;
  maxLength?: number;
  minLength?: number;
  pattern?: string;
  autoComplete?: string;
  autoFocus?: boolean;
  name?: string;
  id?: string;
  className?: string;
}

const VuiInput: React.FC<VuiInputProps> = ({
  type = 'text',
  label,
  placeholder,
  value,
  onChange,
  onBlur,
  onFocus,
  error,
  helperText,
  required = false,
  disabled = false,
  readOnly = false,
  startIcon,
  endIcon,
  fullWidth = false,
  multiline = false,
  rows = 1,
  maxLength,
  minLength,
  pattern,
  autoComplete,
  autoFocus = false,
  name,
  id,
  className,
  ...props
}) => {
  // Component implementation
};
```

#### **Usage Examples**
```tsx
// Basic Input
<VuiInput
  type="text"
  label="Username"
  placeholder="Enter your username"
  value={username}
  onChange={setUsername}
  required
/>

// Input with Icon
<VuiInput
  type="email"
  label="Email Address"
  placeholder="Enter your email"
  value={email}
  onChange={setEmail}
  startIcon={<EmailIcon />}
  error={emailError}
/>

// Password Input
<VuiInput
  type="password"
  label="Password"
  placeholder="Enter your password"
  value={password}
  onChange={setPassword}
  endIcon={<VisibilityIcon />}
  helperText="Must be at least 8 characters"
/>

// Multiline Input
<VuiInput
  type="text"
  label="Description"
  placeholder="Enter description"
  value={description}
  onChange={setDescription}
  multiline
  rows={4}
  maxLength={500}
/>
```

### **VuiTypography Component**

#### **Component Specification**
```typescript
interface VuiTypographyProps {
  variant: 'h1' | 'h2' | 'h3' | 'h4' | 'h5' | 'h6' | 'body1' | 'body2' | 'caption' | 'overline';
  color?: 'primary' | 'secondary' | 'text' | 'error' | 'success' | 'warning' | 'info';
  align?: 'left' | 'center' | 'right' | 'justify';
  weight?: 'light' | 'normal' | 'medium' | 'semibold' | 'bold' | 'extrabold';
  gutterBottom?: boolean;
  noWrap?: boolean;
  children: React.ReactNode;
  className?: string;
  component?: React.ElementType;
}

const VuiTypography: React.FC<VuiTypographyProps> = ({
  variant = 'body1',
  color = 'text',
  align = 'left',
  weight = 'normal',
  gutterBottom = false,
  noWrap = false,
  children,
  className,
  component,
  ...props
}) => {
  // Component implementation
};
```

#### **Usage Examples**
```tsx
// Headings
<VuiTypography variant="h1" color="primary" gutterBottom>
  Dashboard
</VuiTypography>

<VuiTypography variant="h2" color="text">
  Camera Management
</VuiTypography>

// Body Text
<VuiTypography variant="body1" color="secondary">
  This is the main content text.
</VuiTypography>

<VuiTypography variant="body2" color="text" align="center">
  Centered text with custom alignment.
</VuiTypography>

// Caption Text
<VuiTypography variant="caption" color="secondary">
  Additional information or notes.
</VuiTypography>
```

---

## 🧬 **Molecular Components**

### **VuiCard Component**

#### **Component Specification**
```typescript
interface VuiCardProps {
  variant: 'elevated' | 'outlined' | 'filled';
  padding: 'none' | 'small' | 'medium' | 'large';
  children: React.ReactNode;
  className?: string;
  onClick?: () => void;
  hoverable?: boolean;
  loading?: boolean;
}

interface VuiCardHeaderProps {
  title: string;
  subtitle?: string;
  avatar?: React.ReactNode;
  action?: React.ReactNode;
  className?: string;
}

interface VuiCardContentProps {
  children: React.ReactNode;
  className?: string;
}

interface VuiCardActionsProps {
  children: React.ReactNode;
  className?: string;
  align?: 'left' | 'center' | 'right';
}

const VuiCard: React.FC<VuiCardProps> & {
  Header: React.FC<VuiCardHeaderProps>;
  Content: React.FC<VuiCardContentProps>;
  Actions: React.FC<VuiCardActionsProps>;
} = ({ variant = 'elevated', padding = 'medium', children, className, onClick, hoverable = false, loading = false }) => {
  // Component implementation
};
```

#### **Usage Examples**
```tsx
// Basic Card
<VuiCard variant="elevated" padding="medium">
  <VuiCard.Header title="Card Title" subtitle="Card subtitle" />
  <VuiCard.Content>
    <p>Card content goes here...</p>
  </VuiCard.Content>
</VuiCard>

// Card with Actions
<VuiCard variant="outlined" padding="large">
  <VuiCard.Header 
    title="Camera Settings" 
    action={<VuiButton variant="text" size="small">Edit</VuiButton>}
  />
  <VuiCard.Content>
    <p>Camera configuration options...</p>
  </VuiCard.Content>
  <VuiCard.Actions align="right">
    <VuiButton variant="outlined">Cancel</VuiButton>
    <VuiButton variant="contained">Save</VuiButton>
  </VuiCard.Actions>
</VuiCard>

// Interactive Card
<VuiCard 
  variant="elevated" 
  hoverable={true} 
  onClick={handleCardClick}
>
  <VuiCard.Content>
    <p>Clickable card content...</p>
  </VuiCard.Content>
</VuiCard>
```

### **VuiFormField Component**

#### **Component Specification**
```typescript
interface VuiFormFieldProps {
  label: string;
  required?: boolean;
  error?: string;
  helperText?: string;
  disabled?: boolean;
  children: React.ReactNode;
  className?: string;
}

const VuiFormField: React.FC<VuiFormFieldProps> = ({
  label,
  required = false,
  error,
  helperText,
  disabled = false,
  children,
  className
}) => {
  // Component implementation
};
```

#### **Usage Examples**
```tsx
// Form Field with Input
<VuiFormField 
  label="Email Address" 
  required 
  error={emailError}
  helperText="We'll never share your email"
>
  <VuiInput
    type="email"
    placeholder="Enter your email"
    value={email}
    onChange={setEmail}
  />
</VuiFormField>

// Form Field with Select
<VuiFormField 
  label="Camera Type" 
  required
  error={cameraTypeError}
>
  <VuiSelect
    value={cameraType}
    onChange={setCameraType}
    options={cameraOptions}
  />
</VuiFormField>
```

### **VuiAlert Component**

#### **Component Specification**
```typescript
interface VuiAlertProps {
  severity: 'success' | 'info' | 'warning' | 'error';
  title?: string;
  message: string;
  action?: React.ReactNode;
  onClose?: () => void;
  closable?: boolean;
  className?: string;
}

const VuiAlert: React.FC<VuiAlertProps> = ({
  severity = 'info',
  title,
  message,
  action,
  onClose,
  closable = false,
  className
}) => {
  // Component implementation
};
```

#### **Usage Examples**
```tsx
// Success Alert
<VuiAlert 
  severity="success" 
  title="Success!" 
  message="Camera settings saved successfully."
  closable
  onClose={handleClose}
/>

// Error Alert
<VuiAlert 
  severity="error" 
  title="Error" 
  message="Failed to connect to camera. Please check your connection."
  action={<VuiButton variant="outlined" size="small">Retry</VuiButton>}
/>

// Info Alert
<VuiAlert 
  severity="info" 
  message="System maintenance scheduled for tonight at 2 AM."
/>
```

---

## 🧠 **Organism Components**

### **VuiDataTable Component**

#### **Component Specification**
```typescript
interface VuiDataTableProps<T> {
  data: T[];
  columns: VuiDataTableColumn<T>[];
  loading?: boolean;
  error?: string;
  pagination?: {
    page: number;
    pageSize: number;
    total: number;
    onPageChange: (page: number) => void;
    onPageSizeChange: (pageSize: number) => void;
  };
  sorting?: {
    field: keyof T;
    direction: 'asc' | 'desc';
    onSort: (field: keyof T) => void;
  };
  selection?: {
    selectedRows: T[];
    onSelectionChange: (selectedRows: T[]) => void;
    selectable?: boolean;
  };
  search?: {
    value: string;
    onSearch: (value: string) => void;
    placeholder?: string;
  };
  actions?: React.ReactNode;
  className?: string;
}

interface VuiDataTableColumn<T> {
  field: keyof T;
  header: string;
  width?: number | string;
  sortable?: boolean;
  render?: (value: any, row: T) => React.ReactNode;
}

const VuiDataTable = <T extends Record<string, any>>({
  data,
  columns,
  loading = false,
  error,
  pagination,
  sorting,
  selection,
  search,
  actions,
  className
}: VuiDataTableProps<T>) => {
  // Component implementation
};
```

#### **Usage Examples**
```tsx
// Basic Data Table
<VuiDataTable
  data={cameras}
  columns={[
    { field: 'name', header: 'Camera Name', sortable: true },
    { field: 'location', header: 'Location' },
    { field: 'status', header: 'Status', render: (value) => <StatusBadge status={value} /> },
    { field: 'lastSeen', header: 'Last Seen', render: (value) => formatDate(value) }
  ]}
  loading={loading}
  error={error}
/>

// Data Table with Pagination and Search
<VuiDataTable
  data={cameras}
  columns={cameraColumns}
  pagination={{
    page: currentPage,
    pageSize: pageSize,
    total: totalCount,
    onPageChange: setCurrentPage,
    onPageSizeChange: setPageSize
  }}
  search={{
    value: searchTerm,
    onSearch: setSearchTerm,
    placeholder: "Search cameras..."
  }}
  actions={
    <VuiButton variant="contained" onClick={handleAddCamera}>
      Add Camera
    </VuiButton>
  }
/>
```

### **VuiChart Component**

#### **Component Specification**
```typescript
interface VuiChartProps {
  type: 'line' | 'bar' | 'pie' | 'area' | 'scatter' | 'heatmap';
  data: any;
  options: any;
  height?: number | string;
  width?: number | string;
  loading?: boolean;
  error?: string;
  onPointClick?: (point: any) => void;
  className?: string;
}

const VuiChart: React.FC<VuiChartProps> = ({
  type,
  data,
  options,
  height = 400,
  width = '100%',
  loading = false,
  error,
  onPointClick,
  className
}) => {
  // Component implementation using ApexCharts
};
```

#### **Usage Examples**
```tsx
// Line Chart
<VuiChart
  type="line"
  data={chartData}
  options={{
    chart: { type: 'line' },
    xaxis: { categories: timeCategories },
    yaxis: { title: { text: 'Count' } },
    title: { text: 'People Count Over Time' }
  }}
  height={300}
  onPointClick={handlePointClick}
/>

// Bar Chart
<VuiChart
  type="bar"
  data={analyticsData}
  options={{
    chart: { type: 'bar' },
    xaxis: { categories: cameraNames },
    yaxis: { title: { text: 'Count' } },
    title: { text: 'Camera Performance' }
  }}
  height={400}
/>
```

### **VuiCameraGrid Component**

#### **Component Specification**
```typescript
interface VuiCameraGridProps {
  cameras: Camera[];
  layout: 'grid' | 'list';
  onCameraClick?: (camera: Camera) => void;
  onCameraEdit?: (camera: Camera) => void;
  onCameraDelete?: (camera: Camera) => void;
  onCameraStart?: (camera: Camera) => void;
  onCameraStop?: (camera: Camera) => void;
  loading?: boolean;
  error?: string;
  className?: string;
}

const VuiCameraGrid: React.FC<VuiCameraGridProps> = ({
  cameras,
  layout = 'grid',
  onCameraClick,
  onCameraEdit,
  onCameraDelete,
  onCameraStart,
  onCameraStop,
  loading = false,
  error,
  className
}) => {
  // Component implementation
};
```

#### **Usage Examples**
```tsx
// Camera Grid
<VuiCameraGrid
  cameras={cameras}
  layout="grid"
  onCameraClick={handleCameraClick}
  onCameraEdit={handleCameraEdit}
  onCameraDelete={handleCameraDelete}
  onCameraStart={handleCameraStart}
  onCameraStop={handleCameraStop}
  loading={loading}
  error={error}
/>

// Camera List
<VuiCameraGrid
  cameras={cameras}
  layout="list"
  onCameraClick={handleCameraClick}
/>
```

---

## 📐 **Template Components**

### **DashboardLayout Component**

#### **Component Specification**
```typescript
interface DashboardLayoutProps {
  children: React.ReactNode;
  title?: string;
  subtitle?: string;
  breadcrumbs?: BreadcrumbItem[];
  actions?: React.ReactNode;
  sidebar?: React.ReactNode;
  header?: React.ReactNode;
  footer?: React.ReactNode;
  className?: string;
}

interface BreadcrumbItem {
  label: string;
  href?: string;
  active?: boolean;
}

const DashboardLayout: React.FC<DashboardLayoutProps> = ({
  children,
  title,
  subtitle,
  breadcrumbs,
  actions,
  sidebar,
  header,
  footer,
  className
}) => {
  // Component implementation
};
```

#### **Usage Examples**
```tsx
// Basic Dashboard Layout
<DashboardLayout
  title="Dashboard"
  subtitle="Overview of your camera system"
  breadcrumbs={[
    { label: 'Home', href: '/' },
    { label: 'Dashboard', active: true }
  ]}
  actions={
    <VuiButton variant="contained">
      Add Camera
    </VuiButton>
  }
>
  <DashboardContent />
</DashboardLayout>

// Dashboard with Custom Header
<DashboardLayout
  title="Camera Management"
  header={<CustomHeader />}
  sidebar={<NavigationSidebar />}
>
  <CameraManagementContent />
</DashboardLayout>
```

---

## 🎨 **Theme Integration**

### **Theme Provider Setup**
```typescript
// theme/index.ts
import { createTheme } from '@mui/material/styles';

export const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#4318FF',
      light: '#6B46C1',
      dark: '#2D3748',
    },
    secondary: {
      main: '#00B929',
      light: '#48BB78',
      dark: '#2F855A',
    },
    background: {
      default: '#0F1535',
      paper: '#1A1F37',
    },
    text: {
      primary: '#FFFFFF',
      secondary: '#A0AEC0',
    },
  },
  typography: {
    fontFamily: 'Inter, sans-serif',
    h1: {
      fontSize: '2.25rem',
      fontWeight: 700,
    },
    h2: {
      fontSize: '1.875rem',
      fontWeight: 600,
    },
    // ... more typography variants
  },
  shape: {
    borderRadius: 12,
  },
  shadows: [
    'none',
    '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
    // ... custom shadows
  ],
});
```

### **Theme Usage in Components**
```typescript
// Using theme in components
import { useTheme } from '@mui/material/styles';

const VuiButton: React.FC<VuiButtonProps> = ({ variant, color, ...props }) => {
  const theme = useTheme();
  
  return (
    <button
      style={{
        backgroundColor: theme.palette[color].main,
        color: theme.palette[color].contrastText,
        borderRadius: theme.shape.borderRadius,
        // ... other styles
      }}
      {...props}
    />
  );
};
```

---

## 🧪 **Testing Components**

### **Component Testing Examples**
```typescript
// VuiButton.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { VuiButton } from './VuiButton';

describe('VuiButton', () => {
  it('renders with correct text', () => {
    render(<VuiButton>Click me</VuiButton>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  it('calls onClick when clicked', () => {
    const handleClick = jest.fn();
    render(<VuiButton onClick={handleClick}>Click me</VuiButton>);
    
    fireEvent.click(screen.getByText('Click me'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('is disabled when disabled prop is true', () => {
    render(<VuiButton disabled>Click me</VuiButton>);
    expect(screen.getByText('Click me')).toBeDisabled();
  });

  it('shows loading state', () => {
    render(<VuiButton loading>Click me</VuiButton>);
    expect(screen.getByRole('progressbar')).toBeInTheDocument();
  });
});
```

### **Accessibility Testing**
```typescript
// Accessibility tests
import { axe, toHaveNoViolations } from 'jest-axe';

expect.extend(toHaveNoViolations);

describe('VuiButton Accessibility', () => {
  it('should not have accessibility violations', async () => {
    const { container } = render(<VuiButton>Click me</VuiButton>);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it('should have proper ARIA attributes', () => {
    render(<VuiButton aria-label="Save changes">Save</VuiButton>);
    expect(screen.getByLabelText('Save changes')).toBeInTheDocument();
  });
});
```

---

## 📚 **Documentation Guidelines**

### **Component Documentation Template**
```markdown
## Component Name

Brief description of the component and its purpose.

### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `prop1` | `string` | `''` | Description of prop1 |
| `prop2` | `number` | `0` | Description of prop2 |

### Usage

```tsx
import { ComponentName } from './ComponentName';

<ComponentName prop1="value" prop2={42} />
```

### Examples

#### Basic Usage
```tsx
<ComponentName>Content</ComponentName>
```

#### With Props
```tsx
<ComponentName variant="outlined" color="primary">
  Custom Content
</ComponentName>
```

### Accessibility

- Supports keyboard navigation
- Includes proper ARIA attributes
- WCAG 2.1 AA compliant
```

---

**📅 Last Updated**: 2025-01-14  
**👥 Author**: Component Library Team  
**📊 Status**: Component Library Complete - Ready for Implementation 