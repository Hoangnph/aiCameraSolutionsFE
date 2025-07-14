# Frontend Integration Guide
## AI Camera Counting System

### 📊 Tổng quan

Tài liệu này hướng dẫn team frontend tích hợp với backend services của hệ thống AI Camera Counting.

**🟢 Status: BACKEND READY - All APIs tested and documented**

---

## 🎯 Quick Start

### 1. Environment Setup
```bash
# Copy environment configuration
cp env.example .env

# Required environment variables for frontend
REACT_APP_API_URL=http://localhost:3001/api/v1
REACT_APP_CAMERA_API_URL=http://localhost:3002/api/v1
REACT_APP_WS_URL=ws://localhost:3004
```

### 2. Start Backend Services
```bash
# Start all backend services
docker-compose -f docker-compose.becamera.yml up -d
docker-compose -f docker-compose.beauth.yml up -d

# Verify services are running
curl http://localhost:3001/health
curl http://localhost:3002/health
```

### 3. Test API Connectivity
```bash
# Test authentication service
curl -X POST http://localhost:3001/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "TestPass123!",
    "confirmPassword": "TestPass123!",
    "firstName": "Test",
    "lastName": "User",
    "registrationCode": "REG001"
  }'
```

---

## 🔐 Authentication Integration

### Authentication Flow
1. **Register User** → Get JWT token
2. **Login User** → Get JWT token  
3. **Store Token** → Local storage or secure cookie
4. **Use Token** → Include in Authorization header for all protected requests

### Implementation Example
```javascript
// services/authService.js
class AuthService {
  constructor() {
    this.baseURL = process.env.REACT_APP_API_URL;
    this.token = localStorage.getItem('accessToken');
  }

  async register(userData) {
    const response = await fetch(`${this.baseURL}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(userData)
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Registration failed');
    }

    const data = await response.json();
    this.setToken(data.data.accessToken);
    return data;
  }

  async login(credentials) {
    const response = await fetch(`${this.baseURL}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(credentials)
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Login failed');
    }

    const data = await response.json();
    this.setToken(data.data.accessToken);
    return data;
  }

  async logout() {
    if (this.token) {
      await fetch(`${this.baseURL}/auth/logout`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${this.token}` }
      });
    }
    this.clearToken();
  }

  setToken(token) {
    this.token = token;
    localStorage.setItem('accessToken', token);
  }

  clearToken() {
    this.token = null;
    localStorage.removeItem('accessToken');
  }

  getToken() {
    return this.token;
  }

  isAuthenticated() {
    return !!this.token;
  }
}

export default new AuthService();
```

### React Context for Authentication
```javascript
// contexts/AuthContext.js
import React, { createContext, useContext, useState, useEffect } from 'react';
import AuthService from '../services/authService';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if user is already authenticated
    if (AuthService.isAuthenticated()) {
      fetchUserProfile();
    } else {
      setLoading(false);
    }
  }, []);

  const fetchUserProfile = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/auth/profile`, {
        headers: { 'Authorization': `Bearer ${AuthService.getToken()}` }
      });
      
      if (response.ok) {
        const data = await response.json();
        setUser(data.data);
      } else {
        AuthService.clearToken();
      }
    } catch (error) {
      AuthService.clearToken();
    } finally {
      setLoading(false);
    }
  };

  const login = async (credentials) => {
    const data = await AuthService.login(credentials);
    setUser(data.data.user);
    return data;
  };

  const register = async (userData) => {
    const data = await AuthService.register(userData);
    setUser(data.data.user);
    return data;
  };

  const logout = async () => {
    await AuthService.logout();
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{
      user,
      loading,
      login,
      register,
      logout,
      isAuthenticated: AuthService.isAuthenticated()
    }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
```

---

## 📹 Camera Management Integration

### Camera Service
```javascript
// services/cameraService.js
class CameraService {
  constructor() {
    this.baseURL = process.env.REACT_APP_CAMERA_API_URL;
  }

  getHeaders() {
    const token = localStorage.getItem('accessToken');
    return {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    };
  }

  async getCameras() {
    const response = await fetch(`${this.baseURL}/cameras`, {
      headers: this.getHeaders()
    });

    if (!response.ok) {
      throw new Error('Failed to fetch cameras');
    }

    return await response.json();
  }

  async getCamera(id) {
    const response = await fetch(`${this.baseURL}/cameras/${id}`, {
      headers: this.getHeaders()
    });

    if (!response.ok) {
      throw new Error('Failed to fetch camera');
    }

    return await response.json();
  }

  async createCamera(cameraData) {
    const response = await fetch(`${this.baseURL}/cameras`, {
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify(cameraData)
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to create camera');
    }

    return await response.json();
  }

  async updateCamera(id, updateData) {
    const response = await fetch(`${this.baseURL}/cameras/${id}`, {
      method: 'PUT',
      headers: this.getHeaders(),
      body: JSON.stringify(updateData)
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to update camera');
    }

    return await response.json();
  }

  async deleteCamera(id) {
    const response = await fetch(`${this.baseURL}/cameras/${id}`, {
      method: 'DELETE',
      headers: this.getHeaders()
    });

    if (!response.ok) {
      throw new Error('Failed to delete camera');
    }

    return await response.json();
  }
}

export default new CameraService();
```

### Camera Management Components
```javascript
// components/CameraList.js
import React, { useState, useEffect } from 'react';
import CameraService from '../services/cameraService';

const CameraList = () => {
  const [cameras, setCameras] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchCameras();
  }, []);

  const fetchCameras = async () => {
    try {
      setLoading(true);
      const data = await CameraService.getCameras();
      setCameras(data.data);
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div>Loading cameras...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className="camera-list">
      <h2>Cameras ({cameras.length})</h2>
      {cameras.map(camera => (
        <div key={camera.id} className="camera-item">
          <h3>{camera.name}</h3>
          <p>{camera.description}</p>
          <span className={`status ${camera.status}`}>
            {camera.status}
          </span>
        </div>
      ))}
    </div>
  );
};

export default CameraList;
```

```javascript
// components/CameraForm.js
import React, { useState } from 'react';
import CameraService from '../services/cameraService';

const CameraForm = ({ onSuccess }) => {
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    ip_address: '',
    rtsp_url: '',
    status: 'offline'
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      await CameraService.createCamera(formData);
      onSuccess();
      setFormData({
        name: '',
        description: '',
        ip_address: '',
        rtsp_url: '',
        status: 'offline'
      });
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  return (
    <form onSubmit={handleSubmit} className="camera-form">
      <h3>Add New Camera</h3>
      
      {error && <div className="error">{error}</div>}
      
      <div className="form-group">
        <label>Name *</label>
        <input
          type="text"
          name="name"
          value={formData.name}
          onChange={handleChange}
          required
          placeholder="Camera name"
        />
      </div>

      <div className="form-group">
        <label>Description</label>
        <textarea
          name="description"
          value={formData.description}
          onChange={handleChange}
          placeholder="Camera description"
        />
      </div>

      <div className="form-group">
        <label>IP Address *</label>
        <input
          type="text"
          name="ip_address"
          value={formData.ip_address}
          onChange={handleChange}
          required
          placeholder="192.168.1.100"
        />
      </div>

      <div className="form-group">
        <label>RTSP URL *</label>
        <input
          type="text"
          name="rtsp_url"
          value={formData.rtsp_url}
          onChange={handleChange}
          required
          placeholder="rtsp://192.168.1.100:554/stream"
        />
      </div>

      <div className="form-group">
        <label>Status</label>
        <select name="status" value={formData.status} onChange={handleChange}>
          <option value="offline">Offline</option>
          <option value="active">Active</option>
          <option value="maintenance">Maintenance</option>
          <option value="error">Error</option>
        </select>
      </div>

      <button type="submit" disabled={loading}>
        {loading ? 'Creating...' : 'Create Camera'}
      </button>
    </form>
  );
};

export default CameraForm;
```

---

## 📊 Analytics Integration

### Analytics Service
```javascript
// services/analyticsService.js
class AnalyticsService {
  constructor() {
    this.baseURL = process.env.REACT_APP_CAMERA_API_URL;
  }

  async getAnalyticsSummary() {
    const response = await fetch(`${this.baseURL}/analytics/summary`);
    
    if (!response.ok) {
      throw new Error('Failed to fetch analytics');
    }

    return await response.json();
  }

  async getCountData(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    const url = `${this.baseURL}/counts${queryString ? `?${queryString}` : ''}`;
    
    const response = await fetch(url);
    
    if (!response.ok) {
      throw new Error('Failed to fetch count data');
    }

    return await response.json();
  }
}

export default new AnalyticsService();
```

### Analytics Dashboard Component
```javascript
// components/AnalyticsDashboard.js
import React, { useState, useEffect } from 'react';
import AnalyticsService from '../services/analyticsService';

const AnalyticsDashboard = () => {
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchAnalytics();
  }, []);

  const fetchAnalytics = async () => {
    try {
      setLoading(true);
      const data = await AnalyticsService.getAnalyticsSummary();
      setAnalytics(data.data);
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div>Loading analytics...</div>;
  if (error) return <div>Error: {error}</div>;
  if (!analytics) return <div>No analytics data</div>;

  return (
    <div className="analytics-dashboard">
      <h2>Analytics Dashboard</h2>
      
      <div className="analytics-grid">
        <div className="analytics-card">
          <h3>Total Cameras</h3>
          <div className="value">{analytics.total_cameras}</div>
        </div>
        
        <div className="analytics-card">
          <h3>Active Cameras</h3>
          <div className="value">{analytics.active_cameras}</div>
        </div>
        
        <div className="analytics-card">
          <h3>Today In</h3>
          <div className="value">{analytics.today_in}</div>
        </div>
        
        <div className="analytics-card">
          <h3>Today Out</h3>
          <div className="value">{analytics.today_out}</div>
        </div>
        
        <div className="analytics-card">
          <h3>Current Count</h3>
          <div className="value">{analytics.current_count}</div>
        </div>
      </div>
    </div>
  );
};

export default AnalyticsDashboard;
```

---

## ⚠️ Error Handling

### Global Error Handler
```javascript
// utils/errorHandler.js
export const handleApiError = (error, navigate) => {
  if (error.status === 401) {
    // Token expired or invalid
    localStorage.removeItem('accessToken');
    navigate('/login');
  } else if (error.status === 429) {
    // Rate limit exceeded
    alert('Too many requests. Please wait a moment.');
  } else if (error.status >= 500) {
    // Server error
    alert('Server error. Please try again later.');
  } else {
    // Other errors
    alert(error.message || 'An error occurred');
  }
};

export const validateCameraData = (data) => {
  const errors = [];

  if (!data.name || data.name.trim().length === 0) {
    errors.push('Camera name is required');
  }

  if (data.name && data.name.length > 100) {
    errors.push('Camera name must be less than 100 characters');
  }

  if (data.ip_address && !isValidIP(data.ip_address)) {
    errors.push('Invalid IP address format');
  }

  if (data.rtsp_url && !isValidRTSPUrl(data.rtsp_url)) {
    errors.push('Invalid RTSP URL format');
  }

  return errors;
};

const isValidIP = (ip) => {
  const ipRegex = /^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;
  return ipRegex.test(ip);
};

const isValidRTSPUrl = (url) => {
  return url.startsWith('rtsp://') || url.startsWith('http://') || url.startsWith('https://');
};
```

### Protected Route Component
```javascript
// components/ProtectedRoute.js
import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return <div>Loading...</div>;
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return children;
};

export default ProtectedRoute;
```

---

## 🎨 UI/UX Best Practices

### Loading States
```javascript
// components/LoadingSpinner.js
const LoadingSpinner = ({ size = 'medium' }) => {
  return (
    <div className={`loading-spinner ${size}`}>
      <div className="spinner"></div>
      <p>Loading...</p>
    </div>
  );
};
```

### Toast Notifications
```javascript
// components/Toast.js
import React, { useState, useEffect } from 'react';

const Toast = ({ message, type = 'info', duration = 3000, onClose }) => {
  const [visible, setVisible] = useState(true);

  useEffect(() => {
    const timer = setTimeout(() => {
      setVisible(false);
      onClose?.();
    }, duration);

    return () => clearTimeout(timer);
  }, [duration, onClose]);

  if (!visible) return null;

  return (
    <div className={`toast ${type}`}>
      <span className="message">{message}</span>
      <button onClick={() => setVisible(false)}>×</button>
    </div>
  );
};
```

### Form Validation
```javascript
// hooks/useForm.js
import { useState, useCallback } from 'react';

export const useForm = (initialValues, validationRules) => {
  const [values, setValues] = useState(initialValues);
  const [errors, setErrors] = useState({});
  const [touched, setTouched] = useState({});

  const handleChange = useCallback((name, value) => {
    setValues(prev => ({ ...prev, [name]: value }));
    
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  }, [errors]);

  const handleBlur = useCallback((name) => {
    setTouched(prev => ({ ...prev, [name]: true }));
    
    // Validate field on blur
    if (validationRules[name]) {
      const error = validationRules[name](values[name]);
      setErrors(prev => ({ ...prev, [name]: error }));
    }
  }, [values, validationRules]);

  const validateForm = useCallback(() => {
    const newErrors = {};
    
    Object.keys(validationRules).forEach(field => {
      const error = validationRules[field](values[field]);
      if (error) {
        newErrors[field] = error;
      }
    });
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  }, [values, validationRules]);

  return {
    values,
    errors,
    touched,
    handleChange,
    handleBlur,
    validateForm,
    setValues
  };
};
```

---

## 🔧 Configuration

### Environment Configuration
```javascript
// config/api.js
const API_CONFIG = {
  AUTH_SERVICE: process.env.REACT_APP_API_URL || 'http://localhost:3001/api/v1',
  CAMERA_SERVICE: process.env.REACT_APP_CAMERA_API_URL || 'http://localhost:3002/api/v1',
  WS_SERVICE: process.env.REACT_APP_WS_URL || 'ws://localhost:3004',
  TIMEOUT: 10000,
  RETRY_ATTEMPTS: 3
};

export default API_CONFIG;
```

### API Client Configuration
```javascript
// utils/apiClient.js
import API_CONFIG from '../config/api';

class ApiClient {
  constructor() {
    this.baseURL = '';
    this.timeout = API_CONFIG.TIMEOUT;
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const token = localStorage.getItem('accessToken');
    
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...(token && { 'Authorization': `Bearer ${token}` }),
        ...options.headers
      },
      ...options
    };

    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), this.timeout);
      
      const response = await fetch(url, {
        ...config,
        signal: controller.signal
      });
      
      clearTimeout(timeoutId);

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || `HTTP ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      if (error.name === 'AbortError') {
        throw new Error('Request timeout');
      }
      throw error;
    }
  }

  get(endpoint) {
    return this.request(endpoint, { method: 'GET' });
  }

  post(endpoint, data) {
    return this.request(endpoint, {
      method: 'POST',
      body: JSON.stringify(data)
    });
  }

  put(endpoint, data) {
    return this.request(endpoint, {
      method: 'PUT',
      body: JSON.stringify(data)
    });
  }

  delete(endpoint) {
    return this.request(endpoint, { method: 'DELETE' });
  }
}

export default new ApiClient();
```

---

## 📱 Responsive Design

### CSS Variables for Theming
```css
/* styles/variables.css */
:root {
  /* Colors */
  --primary-color: #3b82f6;
  --secondary-color: #64748b;
  --success-color: #10b981;
  --warning-color: #f59e0b;
  --error-color: #ef4444;
  --background-color: #f8fafc;
  --surface-color: #ffffff;
  --text-primary: #1e293b;
  --text-secondary: #64748b;
  
  /* Spacing */
  --spacing-xs: 0.25rem;
  --spacing-sm: 0.5rem;
  --spacing-md: 1rem;
  --spacing-lg: 1.5rem;
  --spacing-xl: 2rem;
  
  /* Border radius */
  --radius-sm: 0.25rem;
  --radius-md: 0.5rem;
  --radius-lg: 0.75rem;
  
  /* Shadows */
  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1);
}

/* Dark theme */
@media (prefers-color-scheme: dark) {
  :root {
    --background-color: #0f172a;
    --surface-color: #1e293b;
    --text-primary: #f1f5f9;
    --text-secondary: #94a3b8;
  }
}
```

### Responsive Grid Layout
```css
/* styles/layout.css */
.analytics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: var(--spacing-lg);
  padding: var(--spacing-lg);
}

.camera-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: var(--spacing-md);
}

@media (max-width: 768px) {
  .analytics-grid {
    grid-template-columns: 1fr;
  }
  
  .camera-list {
    grid-template-columns: 1fr;
  }
}
```

---

## 🚀 Deployment Checklist

### Pre-deployment
- [ ] All API endpoints tested
- [ ] Error handling implemented
- [ ] Loading states added
- [ ] Form validation working
- [ ] Responsive design tested
- [ ] Authentication flow complete
- [ ] Environment variables configured

### Production Configuration
```javascript
// config/production.js
const PRODUCTION_CONFIG = {
  AUTH_SERVICE: 'https://api.yourdomain.com/auth',
  CAMERA_SERVICE: 'https://api.yourdomain.com/camera',
  WS_SERVICE: 'wss://api.yourdomain.com/ws',
  ENABLE_ANALYTICS: true,
  ENABLE_ERROR_TRACKING: true
};
```

### Performance Optimization
- [ ] Code splitting implemented
- [ ] Lazy loading for components
- [ ] Image optimization
- [ ] Bundle size optimized
- [ ] Caching strategies implemented

---

## 📚 Additional Resources

### Documentation
- [API Reference](../02-API-DOCUMENTATION/api-reference.md)
- [Integration Testing](../07-TESTING/integration-testing.md)
- [Database Schema](../03-DATABASE/database-schema.md)

### Support
- **Backend Team**: Available for integration support
- **Test Results**: All APIs tested and working (100% pass rate)
- **Status**: Ready for frontend integration

### Next Steps
1. Set up authentication flow
2. Implement camera management UI
3. Add analytics dashboard
4. Test error handling
5. Optimize performance
6. Deploy to production

---

**Document Version**: 1.0  
**Last Updated**: 2024-07-11  
**Status**: ✅ READY FOR FRONTEND DEVELOPMENT 