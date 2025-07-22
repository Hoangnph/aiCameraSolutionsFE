# Frontend Architecture Documentation

## 📋 **TỔNG QUAN**

Frontend được xây dựng trên React với Vision UI Dashboard template, sử dụng Material-UI và custom components.

## 🏗️ **KIẾN TRÚC TỔNG THỂ**

### **App Structure**
```
App.js
├── ThemeProvider
├── Router (React Router v6)
├── AuthProvider
└── AppLayout
    ├── PageLayout
    ├── Sidenav (conditional)
    └── Routes
        ├── Public Routes (auth pages)
        └── Protected Routes (dashboard, etc.)
```

### **Layout System**
- **PageLayout**: Base layout cho tất cả pages
- **AppLayout**: Conditional layout logic
- **Sidenav**: Navigation menu (chỉ hiển thị ở protected routes)
- **CoverLayout**: Authentication pages layout

## 🔐 **AUTHENTICATION ARCHITECTURE**

### **Authentication Flow**
1. **Public Access**: Auth pages (sign-in, sign-up) không có menu
2. **Protected Access**: Dashboard pages có menu và require authentication
3. **Redirect Logic**: Authenticated users được redirect từ auth pages về dashboard

### **Components**
- **AuthProvider**: Global authentication state management
- **ProtectedRoute**: Route protection wrapper
- **LoadingSpinner**: Loading state component

### **Authentication States**
```javascript
{
  isAuthenticated: boolean,
  isLoading: boolean,
  user: object | null,
  error: string | null
}
```

## 🧭 **ROUTING ARCHITECTURE**

### **Route Types**
- **Public Routes**: `/authentication/*`, `/test-auth`, `/debug-*`
- **Protected Routes**: `/dashboard`, `/cameras`, `/analytics`, etc.

### **Route Protection**
- **ProtectedRoute Component**: Wraps all protected routes
- **Automatic Redirect**: Unauthenticated users → sign-in
- **Menu Logic**: Menu chỉ hiển thị ở protected routes

## 🎨 **COMPONENT ARCHITECTURE**

### **Core Components**
- **VuiBox**: Base layout component
- **VuiTypography**: Typography component
- **VuiInput**: Input component
- **VuiButton**: Button component
- **LoadingSpinner**: Loading state component

### **Layout Components**
- **DashboardLayout**: Dashboard page layout
- **CoverLayout**: Authentication page layout
- **PageLayout**: Base page wrapper

### **Chart Components**
- **LineChart**: Line chart với error handling
- **BarChart**: Bar chart với error handling
- **Chart Options**: Optimized cho string categories

## 🔧 **RECENT FIXES (2025-07-20)**

### **Authentication Logic**
- ✅ Fixed menu hiển thị ở auth pages
- ✅ Fixed redirect logic cho authenticated users
- ✅ Fixed infinite loading issues
- ✅ Fixed LoadingSpinner undefined errors

### **Chart Data**
- ✅ Fixed LineChart xaxis type (datetime → category)
- ✅ Added error handling cho chart components
- ✅ Fixed ApexCharts date format errors

### **React Router**
- ✅ Migrated từ useHistory sang useNavigate
- ✅ Added future flags để suppress warnings
- ✅ Fixed navigation compatibility

### **DefaultProps Warnings**
- ✅ Fixed defaultProps deprecation warnings
- ✅ Updated icon components với default parameters
- ✅ Improved React 18 compatibility

## 🧪 **TESTING ARCHITECTURE**

### **Test Types**
- **Authentication Tests**: Test auth flow và redirects
- **Component Tests**: Test individual components
- **Integration Tests**: Test page interactions
- **Loading Tests**: Test loading states

### **Test Files**
- `auth_loading_test.py`: Comprehensive auth testing
- `simple_auth_test.py`: HTTP-based auth testing
- `loading_spinner_test.py`: Component testing

## 📊 **PERFORMANCE OPTIMIZATIONS**

### **Loading Optimizations**
- Conditional rendering để tránh unnecessary loads
- Simplified authentication checks
- Optimized chart data handling

### **Error Handling**
- Comprehensive error boundaries
- Graceful fallbacks cho failed components
- User-friendly error messages

## 🔒 **SECURITY CONSIDERATIONS**

### **Route Protection**
- Server-side authentication checks
- Client-side route protection
- Automatic redirects cho unauthorized access

### **Data Validation**
- Input validation trên client-side
- API response validation
- Error handling cho invalid data

## 📱 **RESPONSIVE DESIGN**

### **Breakpoints**
- Mobile-first approach
- Responsive navigation
- Adaptive layouts

### **Component Responsiveness**
- Flexible grid systems
- Responsive typography
- Mobile-optimized interactions

## 🚀 **DEPLOYMENT CONSIDERATIONS**

### **Build Process**
- Optimized production builds
- Asset optimization
- Bundle size optimization

### **Environment Configuration**
- Development vs production settings
- API endpoint configuration
- Feature flags

## 📈 **MONITORING & ANALYTICS**

### **Error Tracking**
- Console error monitoring
- Runtime error detection
- Performance monitoring

### **User Analytics**
- Page view tracking
- User interaction tracking
- Performance metrics

---

**Last Updated**: 2025-07-20
**Version**: 2.0
**Status**: ✅ Current 