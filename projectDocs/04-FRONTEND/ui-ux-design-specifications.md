# 🎨 UI/UX Design Specifications - AI Camera Counting System

## 📊 **Tổng quan Design System**

Tài liệu này định nghĩa chi tiết design system, UI components, và UX patterns cho hệ thống AI Camera Counting frontend.

**🎯 Design Philosophy**: Modern, Clean, Professional, User-friendly  
**🎨 Design Style**: Dark theme với accent colors, Material Design principles  
**📱 Responsive**: Mobile-first approach với adaptive layouts  
**♿ Accessibility**: WCAG 2.1 AA compliance  

---

## 🎨 **Design System Foundation**

### **Color Palette**

#### **Primary Colors**
```css
/* Primary Brand Colors */
--primary-50: #F0F4FF;
--primary-100: #E1E9FF;
--primary-200: #C3D3FF;
--primary-300: #A5BDFF;
--primary-400: #87A7FF;
--primary-500: #4318FF;  /* Main Brand Color */
--primary-600: #3A16E6;
--primary-700: #2E12B3;
--primary-800: #220D80;
--primary-900: #16094D;
```

#### **Secondary Colors**
```css
/* Secondary Brand Colors */
--secondary-50: #F0FFF4;
--secondary-100: #E1FFE9;
--secondary-200: #C3FFD3;
--secondary-300: #A5FFBD;
--secondary-400: #87FFA7;
--secondary-500: #00B929;  /* Success/Green */
--secondary-600: #00A625;
--secondary-700: #008320;
--secondary-800: #00601A;
--secondary-900: #003D10;
```

#### **Status Colors**
```css
/* Status & Feedback Colors */
--success-50: #F0FFF4;
--success-500: #00B929;
--success-600: #00A625;

--warning-50: #FFFBEB;
--warning-500: #FFA500;
--warning-600: #E69500;

--error-50: #FEF2F2;
--error-500: #E53E3E;
--error-600: #DC2626;

--info-50: #EFF6FF;
--info-500: #3182CE;
--info-600: #2563EB;
```

#### **Neutral Colors**
```css
/* Background & Surface Colors */
--background-primary: #0F1535;
--background-secondary: #1A1F37;
--background-tertiary: #2D3748;
--background-elevated: #374151;

/* Text Colors */
--text-primary: #FFFFFF;
--text-secondary: #A0AEC0;
--text-tertiary: #718096;
--text-disabled: #4A5568;

/* Border Colors */
--border-primary: #2D3748;
--border-secondary: #4A5568;
--border-focus: #4318FF;
```

### **Typography System**

#### **Font Family**
```css
/* Font Stack */
--font-family-primary: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
--font-family-mono: 'JetBrains Mono', 'Fira Code', 'Monaco', 'Consolas', monospace;
```

#### **Font Sizes**
```css
/* Typography Scale */
--font-size-xs: 0.75rem;    /* 12px */
--font-size-sm: 0.875rem;   /* 14px */
--font-size-base: 1rem;     /* 16px */
--font-size-lg: 1.125rem;   /* 18px */
--font-size-xl: 1.25rem;    /* 20px */
--font-size-2xl: 1.5rem;    /* 24px */
--font-size-3xl: 1.875rem;  /* 30px */
--font-size-4xl: 2.25rem;   /* 36px */
--font-size-5xl: 3rem;      /* 48px */
--font-size-6xl: 3.75rem;   /* 60px */
```

#### **Font Weights**
```css
/* Font Weights */
--font-weight-light: 300;
--font-weight-normal: 400;
--font-weight-medium: 500;
--font-weight-semibold: 600;
--font-weight-bold: 700;
--font-weight-extrabold: 800;
```

#### **Line Heights**
```css
/* Line Heights */
--line-height-tight: 1.25;
--line-height-normal: 1.5;
--line-height-relaxed: 1.75;
--line-height-loose: 2;
```

### **Spacing System**

#### **Spacing Scale**
```css
/* Spacing Scale */
--spacing-0: 0;
--spacing-1: 0.25rem;   /* 4px */
--spacing-2: 0.5rem;    /* 8px */
--spacing-3: 0.75rem;   /* 12px */
--spacing-4: 1rem;      /* 16px */
--spacing-5: 1.25rem;   /* 20px */
--spacing-6: 1.5rem;    /* 24px */
--spacing-8: 2rem;      /* 32px */
--spacing-10: 2.5rem;   /* 40px */
--spacing-12: 3rem;     /* 48px */
--spacing-16: 4rem;     /* 64px */
--spacing-20: 5rem;     /* 80px */
--spacing-24: 6rem;     /* 96px */
```

### **Border Radius System**
```css
/* Border Radius */
--radius-none: 0;
--radius-sm: 0.125rem;   /* 2px */
--radius-base: 0.25rem;  /* 4px */
--radius-md: 0.375rem;   /* 6px */
--radius-lg: 0.5rem;     /* 8px */
--radius-xl: 0.75rem;    /* 12px */
--radius-2xl: 1rem;      /* 16px */
--radius-3xl: 1.5rem;    /* 24px */
--radius-full: 9999px;
```

### **Shadow System**
```css
/* Shadow System */
--shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
--shadow-base: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
--shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
--shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
--shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
--shadow-2xl: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
```

---

## 🧩 **Component Design Specifications**

### **Button Components**

#### **Primary Button**
```typescript
interface PrimaryButtonProps {
  variant: 'contained' | 'outlined' | 'text';
  size: 'small' | 'medium' | 'large';
  disabled?: boolean;
  loading?: boolean;
  startIcon?: React.ReactNode;
  endIcon?: React.ReactNode;
  onClick?: () => void;
  children: React.ReactNode;
}

// Primary Button Styles
const primaryButtonStyles = {
  contained: {
    backgroundColor: 'var(--primary-500)',
    color: 'white',
    border: 'none',
    '&:hover': {
      backgroundColor: 'var(--primary-600)',
      transform: 'translateY(-1px)',
      boxShadow: 'var(--shadow-md)'
    },
    '&:active': {
      transform: 'translateY(0)',
      boxShadow: 'var(--shadow-sm)'
    },
    '&:disabled': {
      backgroundColor: 'var(--text-disabled)',
      cursor: 'not-allowed'
    }
  },
  outlined: {
    backgroundColor: 'transparent',
    color: 'var(--primary-500)',
    border: '2px solid var(--primary-500)',
    '&:hover': {
      backgroundColor: 'var(--primary-500)',
      color: 'white'
    }
  }
};

// Button Sizes
const buttonSizes = {
  small: {
    padding: 'var(--spacing-2) var(--spacing-4)',
    fontSize: 'var(--font-size-sm)',
    borderRadius: 'var(--radius-md)'
  },
  medium: {
    padding: 'var(--spacing-3) var(--spacing-6)',
    fontSize: 'var(--font-size-base)',
    borderRadius: 'var(--radius-lg)'
  },
  large: {
    padding: 'var(--spacing-4) var(--spacing-8)',
    fontSize: 'var(--font-size-lg)',
    borderRadius: 'var(--radius-xl)'
  }
};
```

#### **Icon Button**
```typescript
interface IconButtonProps {
  icon: React.ReactNode;
  size: 'small' | 'medium' | 'large';
  variant: 'filled' | 'outlined' | 'ghost';
  color?: 'primary' | 'secondary' | 'success' | 'warning' | 'error';
  disabled?: boolean;
  onClick?: () => void;
}

// Icon Button Sizes
const iconButtonSizes = {
  small: {
    width: '32px',
    height: '32px',
    fontSize: 'var(--font-size-sm)'
  },
  medium: {
    width: '40px',
    height: '40px',
    fontSize: 'var(--font-size-base)'
  },
  large: {
    width: '48px',
    height: '48px',
    fontSize: 'var(--font-size-lg)'
  }
};
```

### **Form Components**

#### **Input Field**
```typescript
interface InputFieldProps {
  type: 'text' | 'email' | 'password' | 'number' | 'url' | 'tel';
  label: string;
  placeholder?: string;
  value: string;
  onChange: (value: string) => void;
  error?: string;
  helperText?: string;
  required?: boolean;
  disabled?: boolean;
  startIcon?: React.ReactNode;
  endIcon?: React.ReactNode;
}

// Input Field Styles
const inputFieldStyles = {
  container: {
    position: 'relative',
    marginBottom: 'var(--spacing-4)'
  },
  field: {
    width: '100%',
    padding: 'var(--spacing-3) var(--spacing-4)',
    backgroundColor: 'var(--background-secondary)',
    border: '2px solid var(--border-primary)',
    borderRadius: 'var(--radius-lg)',
    color: 'var(--text-primary)',
    fontSize: 'var(--font-size-base)',
    transition: 'all 0.2s ease',
    '&:focus': {
      outline: 'none',
      borderColor: 'var(--primary-500)',
      boxShadow: '0 0 0 3px rgba(67, 24, 255, 0.1)'
    },
    '&:disabled': {
      backgroundColor: 'var(--background-tertiary)',
      color: 'var(--text-disabled)',
      cursor: 'not-allowed'
    }
  },
  label: {
    display: 'block',
    marginBottom: 'var(--spacing-2)',
    color: 'var(--text-secondary)',
    fontSize: 'var(--font-size-sm)',
    fontWeight: 'var(--font-weight-medium)'
  },
  error: {
    color: 'var(--error-500)',
    fontSize: 'var(--font-size-sm)',
    marginTop: 'var(--spacing-1)'
  },
  helperText: {
    color: 'var(--text-tertiary)',
    fontSize: 'var(--font-size-sm)',
    marginTop: 'var(--spacing-1)'
  }
};
```

#### **Select Field**
```typescript
interface SelectFieldProps {
  label: string;
  value: string;
  onChange: (value: string) => void;
  options: Array<{ value: string; label: string; disabled?: boolean }>;
  placeholder?: string;
  error?: string;
  required?: boolean;
  disabled?: boolean;
  multiple?: boolean;
}

// Select Field Styles
const selectFieldStyles = {
  select: {
    backgroundColor: 'var(--background-secondary)',
    border: '2px solid var(--border-primary)',
    borderRadius: 'var(--radius-lg)',
    color: 'var(--text-primary)',
    '&:focus': {
      borderColor: 'var(--primary-500)',
      boxShadow: '0 0 0 3px rgba(67, 24, 255, 0.1)'
    }
  },
  menu: {
    backgroundColor: 'var(--background-secondary)',
    border: '1px solid var(--border-primary)',
    borderRadius: 'var(--radius-lg)',
    boxShadow: 'var(--shadow-lg)'
  },
  option: {
    backgroundColor: 'transparent',
    color: 'var(--text-primary)',
    '&:hover': {
      backgroundColor: 'var(--background-tertiary)'
    },
    '&:selected': {
      backgroundColor: 'var(--primary-500)',
      color: 'white'
    }
  }
};
```

### **Card Components**

#### **Basic Card**
```typescript
interface CardProps {
  variant: 'elevated' | 'outlined' | 'filled';
  padding: 'none' | 'small' | 'medium' | 'large';
  children: React.ReactNode;
}

// Card Styles
const cardStyles = {
  elevated: {
    backgroundColor: 'var(--background-secondary)',
    border: 'none',
    borderRadius: 'var(--radius-xl)',
    boxShadow: 'var(--shadow-lg)',
    transition: 'all 0.2s ease',
    '&:hover': {
      boxShadow: 'var(--shadow-xl)',
      transform: 'translateY(-2px)'
    }
  },
  outlined: {
    backgroundColor: 'transparent',
    border: '1px solid var(--border-primary)',
    borderRadius: 'var(--radius-lg)',
    boxShadow: 'none'
  },
  filled: {
    backgroundColor: 'var(--background-tertiary)',
    border: 'none',
    borderRadius: 'var(--radius-lg)',
    boxShadow: 'none'
  }
};

// Card Padding
const cardPadding = {
  none: { padding: 0 },
  small: { padding: 'var(--spacing-4)' },
  medium: { padding: 'var(--spacing-6)' },
  large: { padding: 'var(--spacing-8)' }
};
```

#### **Statistics Card**
```typescript
interface StatisticsCardProps {
  title: string;
  value: string | number;
  change?: {
    value: number;
    type: 'increase' | 'decrease';
  };
  icon?: React.ReactNode;
  color?: 'primary' | 'success' | 'warning' | 'error' | 'info';
  loading?: boolean;
}

// Statistics Card Styles
const statisticsCardStyles = {
  container: {
    backgroundColor: 'var(--background-secondary)',
    borderRadius: 'var(--radius-xl)',
    padding: 'var(--spacing-6)',
    border: '1px solid var(--border-primary)',
    transition: 'all 0.2s ease',
    '&:hover': {
      transform: 'translateY(-2px)',
      boxShadow: 'var(--shadow-lg)'
    }
  },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 'var(--spacing-4)'
  },
  title: {
    color: 'var(--text-secondary)',
    fontSize: 'var(--font-size-sm)',
    fontWeight: 'var(--font-weight-medium)',
    textTransform: 'uppercase',
    letterSpacing: '0.05em'
  },
  value: {
    color: 'var(--text-primary)',
    fontSize: 'var(--font-size-3xl)',
    fontWeight: 'var(--font-weight-bold)',
    lineHeight: 1.2
  },
  change: {
    display: 'flex',
    alignItems: 'center',
    fontSize: 'var(--font-size-sm)',
    fontWeight: 'var(--font-weight-medium)'
  }
};
```

### **Navigation Components**

#### **Sidebar Navigation**
```typescript
interface SidebarProps {
  isOpen: boolean;
  isCollapsed: boolean;
  onToggle: () => void;
  onCollapse: () => void;
  children: React.ReactNode;
}

// Sidebar Styles
const sidebarStyles = {
  container: {
    position: 'fixed',
    left: 0,
    top: 0,
    height: '100vh',
    backgroundColor: 'var(--background-secondary)',
    borderRight: '1px solid var(--border-primary)',
    transition: 'all 0.3s ease',
    zIndex: 1000
  },
  collapsed: {
    width: '64px'
  },
  expanded: {
    width: '280px'
  },
  header: {
    padding: 'var(--spacing-6)',
    borderBottom: '1px solid var(--border-primary)',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between'
  },
  logo: {
    fontSize: 'var(--font-size-xl)',
    fontWeight: 'var(--font-weight-bold)',
    color: 'var(--primary-500)'
  },
  nav: {
    padding: 'var(--spacing-4) 0'
  }
};
```

#### **Navigation Item**
```typescript
interface NavItemProps {
  icon: React.ReactNode;
  label: string;
  href: string;
  isActive?: boolean;
  isCollapsed?: boolean;
  badge?: string | number;
  onClick?: () => void;
}

// Nav Item Styles
const navItemStyles = {
  container: {
    display: 'flex',
    alignItems: 'center',
    padding: 'var(--spacing-3) var(--spacing-4)',
    margin: 'var(--spacing-1) var(--spacing-2)',
    borderRadius: 'var(--radius-lg)',
    color: 'var(--text-secondary)',
    textDecoration: 'none',
    transition: 'all 0.2s ease',
    cursor: 'pointer',
    '&:hover': {
      backgroundColor: 'var(--background-tertiary)',
      color: 'var(--text-primary)'
    }
  },
  active: {
    backgroundColor: 'var(--primary-500)',
    color: 'white',
    '&:hover': {
      backgroundColor: 'var(--primary-600)'
    }
  },
  icon: {
    marginRight: 'var(--spacing-3)',
    fontSize: 'var(--font-size-lg)'
  },
  label: {
    fontSize: 'var(--font-size-base)',
    fontWeight: 'var(--font-weight-medium)',
    flex: 1
  },
  badge: {
    backgroundColor: 'var(--error-500)',
    color: 'white',
    fontSize: 'var(--font-size-xs)',
    padding: 'var(--spacing-1) var(--spacing-2)',
    borderRadius: 'var(--radius-full)',
    minWidth: '20px',
    textAlign: 'center'
  }
};
```

---

## 📱 **Responsive Design System**

### **Breakpoint System**
```css
/* Breakpoint Definitions */
--breakpoint-xs: 0px;
--breakpoint-sm: 600px;
--breakpoint-md: 960px;
--breakpoint-lg: 1280px;
--breakpoint-xl: 1920px;

/* Responsive Utilities */
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 var(--spacing-4);
}

@media (max-width: 960px) {
  .container {
    padding: 0 var(--spacing-3);
  }
}

@media (max-width: 600px) {
  .container {
    padding: 0 var(--spacing-2);
  }
}
```

### **Grid System**
```typescript
interface GridProps {
  container?: boolean;
  item?: boolean;
  xs?: number;    // 0-12
  sm?: number;    // 0-12
  md?: number;    // 0-12
  lg?: number;    // 0-12
  xl?: number;    // 0-12
  spacing?: number;
  children: React.ReactNode;
}

// Grid Layout Examples
const gridLayouts = {
  dashboard: {
    xs: 12,    // Full width on mobile
    sm: 6,     // Half width on tablet
    md: 4,     // One-third on desktop
    lg: 3      // Quarter width on large screens
  },
  cameraGrid: {
    xs: 12,    // 1 column on mobile
    sm: 6,     // 2 columns on tablet
    md: 4,     // 3 columns on desktop
    lg: 3      // 4 columns on large screens
  }
};
```

### **Mobile-First Approach**
```css
/* Mobile-First CSS Example */
.card {
  /* Mobile styles (default) */
  padding: var(--spacing-4);
  margin-bottom: var(--spacing-4);
  
  /* Tablet styles */
  @media (min-width: 600px) {
    padding: var(--spacing-6);
    margin-bottom: var(--spacing-6);
  }
  
  /* Desktop styles */
  @media (min-width: 960px) {
    padding: var(--spacing-8);
    margin-bottom: var(--spacing-8);
  }
}
```

---

## ♿ **Accessibility Guidelines**

### **WCAG 2.1 AA Compliance**
```typescript
// Accessibility Requirements
const accessibilityRequirements = {
  colorContrast: {
    normal: '4.5:1',
    large: '3:1'
  },
  keyboardNavigation: '100%',
  screenReaderSupport: '100%',
  focusIndicators: 'visible',
  altText: 'required',
  semanticHTML: 'required'
};
```

### **Keyboard Navigation**
```css
/* Focus Styles */
.focus-visible {
  outline: 2px solid var(--primary-500);
  outline-offset: 2px;
}

/* Skip Links */
.skip-link {
  position: absolute;
  top: -40px;
  left: 6px;
  background: var(--primary-500);
  color: white;
  padding: 8px;
  text-decoration: none;
  border-radius: var(--radius-base);
  z-index: 10000;
}

.skip-link:focus {
  top: 6px;
}
```

### **Screen Reader Support**
```typescript
// ARIA Labels and Roles
interface AccessibleComponentProps {
  'aria-label'?: string;
  'aria-describedby'?: string;
  'aria-labelledby'?: string;
  role?: string;
  tabIndex?: number;
}

// Example Usage
const AccessibleButton = ({ children, ...props }: AccessibleComponentProps) => (
  <button
    aria-label={props['aria-label']}
    role={props.role || 'button'}
    tabIndex={props.tabIndex || 0}
    {...props}
  >
    {children}
  </button>
);
```

---

## 🎭 **Animation & Transitions**

### **Transition System**
```css
/* Transition Variables */
--transition-fast: 0.15s ease;
--transition-normal: 0.25s ease;
--transition-slow: 0.35s ease;

/* Common Transitions */
.transition-all {
  transition: all var(--transition-normal);
}

.transition-transform {
  transition: transform var(--transition-normal);
}

.transition-opacity {
  transition: opacity var(--transition-normal);
}
```

### **Animation Classes**
```css
/* Fade Animations */
.fade-in {
  animation: fadeIn 0.3s ease-in;
}

.fade-out {
  animation: fadeOut 0.3s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes fadeOut {
  from { opacity: 1; }
  to { opacity: 0; }
}

/* Slide Animations */
.slide-in-right {
  animation: slideInRight 0.3s ease-out;
}

@keyframes slideInRight {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

/* Scale Animations */
.scale-in {
  animation: scaleIn 0.2s ease-out;
}

@keyframes scaleIn {
  from {
    transform: scale(0.9);
    opacity: 0;
  }
  to {
    transform: scale(1);
    opacity: 1;
  }
}
```

### **Loading Animations**
```css
/* Spinner Animation */
.spinner {
  width: 20px;
  height: 20px;
  border: 2px solid var(--border-primary);
  border-top: 2px solid var(--primary-500);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Skeleton Loading */
.skeleton {
  background: linear-gradient(
    90deg,
    var(--background-tertiary) 25%,
    var(--background-secondary) 50%,
    var(--background-tertiary) 75%
  );
  background-size: 200% 100%;
  animation: skeleton-loading 1.5s infinite;
}

@keyframes skeleton-loading {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
```

---

## 📋 **Component Usage Guidelines**

### **Button Usage**
```typescript
// Primary Actions
<PrimaryButton variant="contained" size="medium">
  Save Changes
</PrimaryButton>

// Secondary Actions
<PrimaryButton variant="outlined" size="medium">
  Cancel
</PrimaryButton>

// Destructive Actions
<PrimaryButton variant="contained" color="error" size="medium">
  Delete
</PrimaryButton>

// Loading State
<PrimaryButton variant="contained" loading={true}>
  Processing...
</PrimaryButton>
```

### **Form Usage**
```typescript
// Input Field
<InputField
  type="email"
  label="Email Address"
  placeholder="Enter your email"
  value={email}
  onChange={setEmail}
  error={emailError}
  required
/>

// Select Field
<SelectField
  label="Camera Type"
  value={cameraType}
  onChange={setCameraType}
  options={[
    { value: 'ip', label: 'IP Camera' },
    { value: 'usb', label: 'USB Camera' },
    { value: 'webcam', label: 'Webcam' }
  ]}
  required
/>
```

### **Card Usage**
```typescript
// Statistics Card
<StatisticsCard
  title="Total Cameras"
  value="24"
  change={{ value: 12, type: 'increase' }}
  icon={<CameraIcon />}
  color="primary"
/>

// Content Card
<Card variant="elevated" padding="medium">
  <CardHeader title="Camera Settings" />
  <CardContent>
    <p>Camera configuration options...</p>
  </CardContent>
  <CardActions>
    <Button variant="contained">Save</Button>
    <Button variant="outlined">Cancel</Button>
  </CardActions>
</Card>
```

---

## 🎯 **Design Principles**

### **1. Consistency**
- Use consistent spacing, typography, and colors
- Maintain visual hierarchy across all components
- Follow established patterns for similar interactions

### **2. Clarity**
- Clear visual feedback for all user actions
- Intuitive navigation and information architecture
- Readable typography with proper contrast

### **3. Efficiency**
- Minimize cognitive load with clear layouts
- Provide shortcuts for power users
- Optimize for common user tasks

### **4. Accessibility**
- Ensure WCAG 2.1 AA compliance
- Support keyboard navigation
- Provide alternative text for images

### **5. Responsiveness**
- Mobile-first design approach
- Adaptive layouts for all screen sizes
- Touch-friendly interface elements

---

**📅 Last Updated**: 2025-01-14  
**👥 Author**: UI/UX Design Team  
**📊 Status**: Design System Complete - Ready for Implementation 