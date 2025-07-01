# Integration Guide - Authentication Microservice

## Tổng quan

Hướng dẫn tích hợp chi tiết cho frontend với Backend Authentication Service. Tài liệu này cung cấp các bước thực hiện, code mẫu và best practices để tích hợp authentication vào ứng dụng frontend.

## Mục lục

1. [Cấu hình kết nối](#cấu-hình-kết-nối)
2. [Luồng xác thực cơ bản](#luồng-xác-thực-cơ-bản)
3. [Tích hợp với React](#tích-hợp-với-react)
4. [Tích hợp với Next.js](#tích-hợp-với-nextjs)
5. [Tích hợp với Vue.js](#tích-hợp-với-vuejs)
6. [Xử lý lỗi và bảo mật](#xử-lý-lỗi-và-bảo-mật)
7. [Best Practices](#best-practices)
8. [Troubleshooting](#troubleshooting)

## Cấu hình kết nối

### Environment Configuration

```javascript
// config/api.js
const API_CONFIG = {
  // Development
  development: {
    baseURL: 'http://localhost:3001/api/v1',
    timeout: 10000
  },
  // Production
  production: {
    baseURL: 'https://api.peoplecounting.com/api/v1',
    timeout: 15000
  }
};

export const getApiConfig = () => {
  const env = process.env.NODE_ENV || 'development';
  return API_CONFIG[env];
};
```

### API Client Setup

```javascript
// services/apiClient.js
import axios from 'axios';
import { getApiConfig } from '../config/api';

const apiClient = axios.create({
  baseURL: getApiConfig().baseURL,
  timeout: getApiConfig().timeout,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Request interceptor - thêm token vào header
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('accessToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor - xử lý token expired
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        const refreshToken = localStorage.getItem('refreshToken');
        const response = await axios.post('/auth/refresh', { refreshToken });
        
        if (response.data.success) {
          localStorage.setItem('accessToken', response.data.data.accessToken);
          localStorage.setItem('refreshToken', response.data.data.refreshToken);
          
          originalRequest.headers.Authorization = `Bearer ${response.data.data.accessToken}`;
          return apiClient(originalRequest);
        }
      } catch (refreshError) {
        // Refresh token cũng hết hạn, logout user
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
        window.location.href = '/login';
      }
    }
    
    return Promise.reject(error);
  }
);

export default apiClient;
```

## Luồng xác thực cơ bản

### 1. Đăng ký tài khoản

```javascript
// services/authService.js
export const registerUser = async (userData) => {
  try {
    const response = await apiClient.post('/auth/register', {
      username: userData.username,
      email: userData.email,
      password: userData.password,
      confirmPassword: userData.confirmPassword,
      firstName: userData.firstName,
      lastName: userData.lastName
    });
    
    if (response.data.success) {
      // Lưu token sau khi đăng ký thành công
      localStorage.setItem('accessToken', response.data.data.accessToken);
      localStorage.setItem('refreshToken', response.data.data.refreshToken);
      return response.data;
    }
  } catch (error) {
    throw new Error(error.response?.data?.error?.message || 'Registration failed');
  }
};
```

### 2. Đăng nhập

```javascript
export const loginUser = async (credentials) => {
  try {
    const response = await apiClient.post('/auth/login', {
      username: credentials.username, // hoặc email
      password: credentials.password
    });
    
    if (response.data.success) {
      // Lưu token và thông tin user
      localStorage.setItem('accessToken', response.data.data.accessToken);
      localStorage.setItem('refreshToken', response.data.data.refreshToken);
      localStorage.setItem('user', JSON.stringify(response.data.data.user));
      return response.data;
    }
  } catch (error) {
    throw new Error(error.response?.data?.error?.message || 'Login failed');
  }
};
```

### 3. Lấy thông tin user hiện tại

```javascript
export const getCurrentUser = async () => {
  try {
    const response = await apiClient.get('/auth/me');
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.error?.message || 'Failed to get user info');
  }
};
```

### 4. Cập nhật profile

```javascript
export const updateProfile = async (profileData) => {
  try {
    const response = await apiClient.put('/users/profile', {
      firstName: profileData.firstName,
      lastName: profileData.lastName,
      email: profileData.email,
      username: profileData.username
    });
    
    if (response.data.success) {
      // Cập nhật thông tin user trong localStorage
      localStorage.setItem('user', JSON.stringify(response.data.data.user));
      return response.data;
    }
  } catch (error) {
    throw new Error(error.response?.data?.error?.message || 'Profile update failed');
  }
};
```

### 5. Đổi mật khẩu

```javascript
export const changePassword = async (passwordData) => {
  try {
    const response = await apiClient.put('/users/change-password', {
      currentPassword: passwordData.currentPassword,
      newPassword: passwordData.newPassword,
      confirmNewPassword: passwordData.confirmNewPassword
    });
    
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.error?.message || 'Password change failed');
  }
};
```

### 6. Đăng xuất

```javascript
export const logoutUser = async () => {
  try {
    await apiClient.post('/auth/logout');
  } catch (error) {
    console.error('Logout error:', error);
  } finally {
    // Xóa token và thông tin user
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('user');
  }
};
```

## Tích hợp với React

### Context Provider cho Authentication

```javascript
// contexts/AuthContext.js
import React, { createContext, useContext, useState, useEffect } from 'react';
import { getCurrentUser, loginUser, registerUser, logoutUser } from '../services/authService';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Kiểm tra user đã đăng nhập khi component mount
  useEffect(() => {
    const checkAuth = async () => {
      const token = localStorage.getItem('accessToken');
      if (token) {
        try {
          const response = await getCurrentUser();
          setUser(response.data.user);
        } catch (error) {
          localStorage.removeItem('accessToken');
          localStorage.removeItem('refreshToken');
        }
      }
      setLoading(false);
    };

    checkAuth();
  }, []);

  const login = async (credentials) => {
    try {
      setError(null);
      const response = await loginUser(credentials);
      setUser(response.data.user);
      return response;
    } catch (error) {
      setError(error.message);
      throw error;
    }
  };

  const register = async (userData) => {
    try {
      setError(null);
      const response = await registerUser(userData);
      setUser(response.data.user);
      return response;
    } catch (error) {
      setError(error.message);
      throw error;
    }
  };

  const logout = async () => {
    try {
      await logoutUser();
      setUser(null);
    } catch (error) {
      console.error('Logout error:', error);
    }
  };

  const value = {
    user,
    loading,
    error,
    login,
    register,
    logout,
    isAuthenticated: !!user
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};
```

### Protected Route Component

```javascript
// components/ProtectedRoute.js
import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

export const ProtectedRoute = ({ children, requiredRole = null }) => {
  const { user, loading, isAuthenticated } = useAuth();
  const location = useLocation();

  if (loading) {
    return <div>Loading...</div>;
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  if (requiredRole && user.role !== requiredRole) {
    return <Navigate to="/unauthorized" replace />;
  }

  return children;
};
```

### Login Component

```javascript
// components/Login.js
import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

export const Login = () => {
  const [credentials, setCredentials] = useState({
    username: '',
    password: ''
  });
  const [loading, setLoading] = useState(false);
  const { login, error } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const from = location.state?.from?.pathname || '/dashboard';

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      await login(credentials);
      navigate(from, { replace: true });
    } catch (error) {
      console.error('Login failed:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    setCredentials({
      ...credentials,
      [e.target.name]: e.target.value
    });
  };

  return (
    <div className="login-container">
      <form onSubmit={handleSubmit}>
        <h2>Đăng nhập</h2>
        
        {error && <div className="error-message">{error}</div>}
        
        <div className="form-group">
          <label htmlFor="username">Tên đăng nhập hoặc Email:</label>
          <input
            type="text"
            id="username"
            name="username"
            value={credentials.username}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="password">Mật khẩu:</label>
          <input
            type="password"
            id="password"
            name="password"
            value={credentials.password}
            onChange={handleChange}
            required
          />
        </div>

        <button type="submit" disabled={loading}>
          {loading ? 'Đang đăng nhập...' : 'Đăng nhập'}
        </button>
      </form>
    </div>
  );
};
```

### App Component với Routing

```javascript
// App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import { ProtectedRoute } from './components/ProtectedRoute';
import { Login } from './components/Login';
import { Register } from './components/Register';
import { Dashboard } from './components/Dashboard';
import { Profile } from './components/Profile';

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route 
            path="/dashboard" 
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/profile" 
            element={
              <ProtectedRoute>
                <Profile />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/admin" 
            element={
              <ProtectedRoute requiredRole="admin">
                <AdminPanel />
              </ProtectedRoute>
            } 
          />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
```

## Tích hợp với Next.js

### API Routes cho Server-Side

```javascript
// pages/api/auth/login.js
export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ message: 'Method not allowed' });
  }

  try {
    const { username, password } = req.body;
    
    const response = await fetch(`${process.env.AUTH_API_URL}/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username, password }),
    });

    const data = await response.json();

    if (data.success) {
      // Set HTTP-only cookies
      res.setHeader('Set-Cookie', [
        `accessToken=${data.data.accessToken}; HttpOnly; Secure; SameSite=Strict; Max-Age=900`,
        `refreshToken=${data.data.refreshToken}; HttpOnly; Secure; SameSite=Strict; Max-Age=604800`
      ]);
      
      return res.status(200).json(data);
    } else {
      return res.status(400).json(data);
    }
  } catch (error) {
    return res.status(500).json({ message: 'Internal server error' });
  }
}
```

### Middleware cho Authentication

```javascript
// middleware/auth.js
import { NextResponse } from 'next/server';

export function middleware(request) {
  const token = request.cookies.get('accessToken');
  const isAuthPage = request.nextUrl.pathname.startsWith('/login') || 
                     request.nextUrl.pathname.startsWith('/register');
  const isProtectedPage = request.nextUrl.pathname.startsWith('/dashboard') ||
                          request.nextUrl.pathname.startsWith('/profile');

  if (isProtectedPage && !token) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  if (isAuthPage && token) {
    return NextResponse.redirect(new URL('/dashboard', request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/dashboard/:path*', '/profile/:path*', '/login', '/register']
};
```

### Custom Hook cho Next.js

```javascript
// hooks/useAuth.js
import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';

export const useAuth = () => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    try {
      const response = await fetch('/api/auth/me');
      if (response.ok) {
        const data = await response.json();
        setUser(data.user);
      }
    } catch (error) {
      console.error('Auth check failed:', error);
    } finally {
      setLoading(false);
    }
  };

  const login = async (credentials) => {
    const response = await fetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(credentials),
    });

    const data = await response.json();
    
    if (data.success) {
      setUser(data.data.user);
      router.push('/dashboard');
    }
    
    return data;
  };

  const logout = async () => {
    await fetch('/api/auth/logout', { method: 'POST' });
    setUser(null);
    router.push('/login');
  };

  return { user, loading, login, logout, isAuthenticated: !!user };
};
```

## Tích hợp với Vue.js

### Vuex Store cho Authentication

```javascript
// store/auth.js
import apiClient from '@/services/apiClient';

export default {
  namespaced: true,
  
  state: {
    user: null,
    token: localStorage.getItem('accessToken') || null,
    loading: false,
    error: null
  },

  mutations: {
    SET_USER(state, user) {
      state.user = user;
    },
    SET_TOKEN(state, token) {
      state.token = token;
      if (token) {
        localStorage.setItem('accessToken', token);
      } else {
        localStorage.removeItem('accessToken');
      }
    },
    SET_LOADING(state, loading) {
      state.loading = loading;
    },
    SET_ERROR(state, error) {
      state.error = error;
    }
  },

  actions: {
    async login({ commit }, credentials) {
      commit('SET_LOADING', true);
      commit('SET_ERROR', null);
      
      try {
        const response = await apiClient.post('/auth/login', credentials);
        
        if (response.data.success) {
          commit('SET_USER', response.data.data.user);
          commit('SET_TOKEN', response.data.data.accessToken);
          localStorage.setItem('refreshToken', response.data.data.refreshToken);
        }
        
        return response.data;
      } catch (error) {
        const message = error.response?.data?.error?.message || 'Login failed';
        commit('SET_ERROR', message);
        throw error;
      } finally {
        commit('SET_LOADING', false);
      }
    },

    async logout({ commit }) {
      try {
        await apiClient.post('/auth/logout');
      } catch (error) {
        console.error('Logout error:', error);
      } finally {
        commit('SET_USER', null);
        commit('SET_TOKEN', null);
        localStorage.removeItem('refreshToken');
      }
    },

    async getCurrentUser({ commit }) {
      try {
        const response = await apiClient.get('/auth/me');
        commit('SET_USER', response.data.data.user);
        return response.data;
      } catch (error) {
        commit('SET_USER', null);
        commit('SET_TOKEN', null);
        throw error;
      }
    }
  },

  getters: {
    isAuthenticated: state => !!state.token,
    user: state => state.user,
    loading: state => state.loading,
    error: state => state.error
  }
};
```

### Vue Router Guard

```javascript
// router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import store from '@/store';

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { requiresGuest: true }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('@/views/Dashboard.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('@/views/Profile.vue'),
    meta: { requiresAuth: true }
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

router.beforeEach(async (to, from, next) => {
  const isAuthenticated = store.getters['auth/isAuthenticated'];
  
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login');
  } else if (to.meta.requiresGuest && isAuthenticated) {
    next('/dashboard');
  } else {
    next();
  }
});

export default router;
```

## Xử lý lỗi và bảo mật

### Error Handling

```javascript
// utils/errorHandler.js
export const handleApiError = (error) => {
  if (error.response) {
    // Server trả về response với status code ngoài 2xx
    const { status, data } = error.response;
    
    switch (status) {
      case 400:
        return `Dữ liệu không hợp lệ: ${data.error?.message || 'Bad Request'}`;
      case 401:
        return 'Phiên đăng nhập đã hết hạn. Vui lòng đăng nhập lại.';
      case 403:
        return 'Bạn không có quyền truy cập trang này.';
      case 404:
        return 'Không tìm thấy tài nguyên yêu cầu.';
      case 429:
        return 'Quá nhiều yêu cầu. Vui lòng thử lại sau.';
      case 500:
        return 'Lỗi server. Vui lòng thử lại sau.';
      default:
        return data.error?.message || 'Đã xảy ra lỗi không xác định.';
    }
  } else if (error.request) {
    // Request được gửi nhưng không nhận được response
    return 'Không thể kết nối đến server. Vui lòng kiểm tra kết nối mạng.';
  } else {
    // Lỗi khác
    return error.message || 'Đã xảy ra lỗi không xác định.';
  }
};
```

### Security Best Practices

```javascript
// utils/security.js
export const sanitizeInput = (input) => {
  if (typeof input !== 'string') return input;
  
  return input
    .replace(/[<>]/g, '')
    .replace(/javascript:/gi, '')
    .replace(/on\w+=/gi, '')
    .trim();
};

export const validatePassword = (password) => {
  const minLength = 8;
  const hasUpperCase = /[A-Z]/.test(password);
  const hasLowerCase = /[a-z]/.test(password);
  const hasNumbers = /\d/.test(password);
  const hasSpecialChar = /[@$!%*?&]/.test(password);
  
  const errors = [];
  
  if (password.length < minLength) {
    errors.push(`Mật khẩu phải có ít nhất ${minLength} ký tự`);
  }
  if (!hasUpperCase) {
    errors.push('Mật khẩu phải có ít nhất 1 chữ hoa');
  }
  if (!hasLowerCase) {
    errors.push('Mật khẩu phải có ít nhất 1 chữ thường');
  }
  if (!hasNumbers) {
    errors.push('Mật khẩu phải có ít nhất 1 số');
  }
  if (!hasSpecialChar) {
    errors.push('Mật khẩu phải có ít nhất 1 ký tự đặc biệt (@$!%*?&)');
  }
  
  return errors;
};

export const secureStorage = {
  setItem: (key, value) => {
    try {
      const encryptedValue = btoa(JSON.stringify(value));
      localStorage.setItem(key, encryptedValue);
    } catch (error) {
      console.error('Storage error:', error);
    }
  },
  
  getItem: (key) => {
    try {
      const value = localStorage.getItem(key);
      return value ? JSON.parse(atob(value)) : null;
    } catch (error) {
      console.error('Storage error:', error);
      return null;
    }
  },
  
  removeItem: (key) => {
    localStorage.removeItem(key);
  }
};
```

## Best Practices

### 1. Token Management

```javascript
// utils/tokenManager.js
class TokenManager {
  static getAccessToken() {
    return localStorage.getItem('accessToken');
  }
  
  static getRefreshToken() {
    return localStorage.getItem('refreshToken');
  }
  
  static setTokens(accessToken, refreshToken) {
    localStorage.setItem('accessToken', accessToken);
    localStorage.setItem('refreshToken', refreshToken);
  }
  
  static clearTokens() {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
  }
  
  static isTokenExpired(token) {
    if (!token) return true;
    
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      return payload.exp * 1000 < Date.now();
    } catch (error) {
      return true;
    }
  }
  
  static getTokenExpiration(token) {
    if (!token) return null;
    
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      return new Date(payload.exp * 1000);
    } catch (error) {
      return null;
    }
  }
}

export default TokenManager;
```

### 2. Auto Refresh Token

```javascript
// utils/autoRefresh.js
import TokenManager from './tokenManager';
import apiClient from '../services/apiClient';

class AutoRefresh {
  constructor() {
    this.refreshPromise = null;
  }
  
  async refreshToken() {
    if (this.refreshPromise) {
      return this.refreshPromise;
    }
    
    this.refreshPromise = this.performRefresh();
    return this.refreshPromise;
  }
  
  async performRefresh() {
    try {
      const refreshToken = TokenManager.getRefreshToken();
      
      if (!refreshToken) {
        throw new Error('No refresh token available');
      }
      
      const response = await apiClient.post('/auth/refresh', { refreshToken });
      
      if (response.data.success) {
        TokenManager.setTokens(
          response.data.data.accessToken,
          response.data.data.refreshToken
        );
        return response.data.data.accessToken;
      }
    } catch (error) {
      TokenManager.clearTokens();
      window.location.href = '/login';
      throw error;
    } finally {
      this.refreshPromise = null;
    }
  }
}

export default new AutoRefresh();
```

### 3. Form Validation

```javascript
// utils/validation.js
export const validationRules = {
  username: {
    required: 'Tên đăng nhập là bắt buộc',
    minLength: (min) => `Tên đăng nhập phải có ít nhất ${min} ký tự`,
    maxLength: (max) => `Tên đăng nhập không được quá ${max} ký tự`,
    pattern: 'Tên đăng nhập chỉ được chứa chữ cái, số và dấu gạch dưới'
  },
  
  email: {
    required: 'Email là bắt buộc',
    pattern: 'Email không hợp lệ'
  },
  
  password: {
    required: 'Mật khẩu là bắt buộc',
    minLength: (min) => `Mật khẩu phải có ít nhất ${min} ký tự`,
    pattern: 'Mật khẩu phải chứa chữ hoa, chữ thường, số và ký tự đặc biệt'
  }
};

export const validateField = (value, rules) => {
  const errors = [];
  
  if (rules.required && !value) {
    errors.push(rules.required);
  }
  
  if (value) {
    if (rules.minLength && value.length < rules.minLength) {
      errors.push(rules.minLength(rules.minLength));
    }
    
    if (rules.maxLength && value.length > rules.maxLength) {
      errors.push(rules.maxLength(rules.maxLength));
    }
    
    if (rules.pattern && !rules.pattern.test(value)) {
      errors.push(rules.pattern);
    }
  }
  
  return errors;
};
```

## Troubleshooting

### Các lỗi thường gặp

#### 1. CORS Error
```javascript
// Lỗi: Access to fetch at 'http://localhost:3001/api/v1/auth/login' from origin 'http://localhost:3000' has been blocked by CORS policy

// Giải pháp: Đảm bảo backend đã cấu hình CORS đúng
// Backend cần có:
app.use(cors({
  origin: 'http://localhost:3000',
  credentials: true
}));
```

#### 2. Token Expired
```javascript
// Lỗi: 401 Unauthorized - Token expired

// Giải pháp: Implement auto refresh token
// Sử dụng interceptor như đã hướng dẫn ở trên
```

#### 3. Network Error
```javascript
// Lỗi: Network Error - Cannot connect to server

// Giải pháp: Kiểm tra
// 1. Backend có đang chạy không?
// 2. Port có đúng không?
// 3. Firewall có chặn không?
// 4. Docker container có running không?
```

#### 4. Validation Error
```javascript
// Lỗi: 400 Bad Request - Validation failed

// Giải pháp: Kiểm tra dữ liệu gửi lên có đúng format không
// Xem chi tiết trong error.details
```

### Debug Tips

```javascript
// 1. Enable debug logging
localStorage.setItem('debug', 'auth:*');

// 2. Check network tab trong browser dev tools
// 3. Kiểm tra localStorage/sessionStorage
// 4. Sử dụng React DevTools hoặc Vue DevTools
// 5. Console.log để debug flow
```

### Performance Optimization

```javascript
// 1. Debounce API calls
import { debounce } from 'lodash';

const debouncedSearch = debounce(async (query) => {
  const response = await apiClient.get(`/users?search=${query}`);
  return response.data;
}, 300);

// 2. Cache user data
const userCache = new Map();

export const getUserById = async (id) => {
  if (userCache.has(id)) {
    return userCache.get(id);
  }
  
  const response = await apiClient.get(`/users/${id}`);
  userCache.set(id, response.data);
  return response.data;
};

// 3. Lazy load components
const LazyProfile = React.lazy(() => import('./Profile'));
```

## Kết luận

Tài liệu này cung cấp hướng dẫn chi tiết để tích hợp Authentication Microservice với frontend. Đảm bảo:

1. **Bảo mật**: Luôn validate input, sử dụng HTTPS, bảo vệ token
2. **UX tốt**: Loading states, error handling, auto refresh token
3. **Performance**: Debounce, cache, lazy loading
4. **Maintainability**: Tách biệt concerns, reusable components

Để hỗ trợ thêm, hãy tham khảo:
- [API Reference](./api-reference.md)
- [Security Guide](./security-guide.md)
- [Deployment Guide](./deployment-guide.md) 