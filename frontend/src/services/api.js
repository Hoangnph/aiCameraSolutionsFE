import axios from 'axios';

// API Configuration
const API_CONFIG = {
  AUTH_BASE_URL: process.env.REACT_APP_AUTH_SERVICE_URL || 'http://localhost:3001',
  CAMERA_BASE_URL: process.env.REACT_APP_CAMERA_API_URL || 'http://localhost:3002/api/v1',
  WS_URL: process.env.REACT_APP_WS_URL || 'ws://localhost:3003',
  TIMEOUT: 10000,
  RETRY_ATTEMPTS: 3,
};

// Create axios instances
const authClient = axios.create({
  baseURL: API_CONFIG.AUTH_BASE_URL,
  timeout: API_CONFIG.TIMEOUT,
});

const cameraClient = axios.create({
  baseURL: API_CONFIG.CAMERA_BASE_URL,
  timeout: API_CONFIG.TIMEOUT,
});

// Request interceptors
authClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

cameraClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptors
const responseInterceptor = (response) => {
  // Return the full response object, not just response.data
  return response;
};

const errorInterceptor = (error) => {
  if (error.response?.status === 401) {
    localStorage.removeItem('authToken');
    localStorage.removeItem('user');
    // Don't redirect automatically to prevent loops
    // window.location.href = '/authentication/sign-in';
  }
  return Promise.reject(error);
};

authClient.interceptors.response.use(responseInterceptor, errorInterceptor);
cameraClient.interceptors.response.use(responseInterceptor, errorInterceptor);

// Authentication API
export const authAPI = {
  // Login user
  login: async (credentials) => {
    try {
      const response = await authClient.post('/api/v1/auth/login', credentials);
      // response is now the full axios response object
      if (response.data && response.data.success) {
        localStorage.setItem('authToken', response.data.data.accessToken);
        localStorage.setItem('user', JSON.stringify(response.data.data.user));
        return response.data;
      }
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // Register user
  register: async (userData) => {
    try {
      const response = await authClient.post('/api/v1/auth/register', userData);
      // response is now the full axios response object
      if (response.data && response.data.success) {
        localStorage.setItem('authToken', response.data.data.accessToken);
        localStorage.setItem('user', JSON.stringify(response.data.data.user));
        return response.data;
      }
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // Logout user
  logout: async () => {
    try {
      await authClient.post('/api/v1/auth/logout');
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      localStorage.removeItem('authToken');
      localStorage.removeItem('user');
    }
  },

  // Get current user
  getCurrentUser: async () => {
    try {
      const response = await authClient.get('/api/v1/auth/me');
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // Verify token
  verifyToken: async () => {
    try {
      const response = await authClient.post('/api/v1/auth/verify');
      return response.data;
    } catch (error) {
      throw error;
    }
  },
};

// Camera Management API
export const cameraAPI = {
  // Get all cameras
  getCameras: async () => {
    try {
      const response = await cameraClient.get('/cameras');
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // Get camera by ID
  getCamera: async (cameraId) => {
    try {
      const response = await cameraClient.get(`/cameras/${cameraId}`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // Create new camera
  createCamera: async (cameraData) => {
    try {
      const response = await cameraClient.post('/cameras', cameraData);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // Update camera
  updateCamera: async (cameraId, cameraData) => {
    try {
      const response = await cameraClient.put(`/cameras/${cameraId}`, cameraData);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // Delete camera
  deleteCamera: async (cameraId) => {
    try {
      const response = await cameraClient.delete(`/cameras/${cameraId}`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // Update camera status
  updateCameraStatus: async (cameraId, status) => {
    try {
      const response = await cameraClient.patch(`/cameras/${cameraId}/status`, { status });
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // Start camera processing
  startCameraProcessing: async (cameraId) => {
    try {
      const response = await cameraClient.post(`/cameras/${cameraId}/start`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // Stop camera processing
  stopCameraProcessing: async (cameraId) => {
    try {
      const response = await cameraClient.post(`/cameras/${cameraId}/stop`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // Get camera processing status
  getCameraProcessingStatus: async (cameraId) => {
    try {
      const response = await cameraClient.get(`/cameras/${cameraId}/status`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // Test camera connection
  testCameraConnection: async (cameraId) => {
    try {
      const response = await cameraClient.post(`/cameras/${cameraId}/test-connection`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // Get count data
  getCountData: async (cameraId = null, limit = 100) => {
    try {
      const params = { limit };
      if (cameraId) params.camera_id = cameraId;
      const response = await cameraClient.get('/counts', { params });
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // Get analytics summary
  getAnalyticsSummary: async () => {
    try {
      const response = await cameraClient.get('/analytics/summary');
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // Get worker pool status
  getWorkerPoolStatus: async () => {
    try {
      const response = await cameraClient.get('/workers/status');
      return response.data;
    } catch (error) {
      throw error;
    }
  },
};

// Test API (no authentication required)
export const testAPI = {
  // Get cameras (test endpoint)
  getCameras: async () => {
    try {
      const response = await axios.get(`${API_CONFIG.CAMERA_BASE_URL}/test/cameras`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // Get worker pool status (test endpoint)
  getWorkerPoolStatus: async () => {
    try {
      const response = await axios.get(`${API_CONFIG.CAMERA_BASE_URL}/test/workers/status`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },
};

// Health check API
export const healthAPI = {
  // Check beAuth health
  checkAuthHealth: async () => {
    try {
      const response = await axios.get(`${API_CONFIG.AUTH_BASE_URL}/health`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // Check beCamera health
  checkCameraHealth: async () => {
    try {
      const response = await axios.get(`${API_CONFIG.CAMERA_BASE_URL.replace('/api/v1', '')}/health`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },
};

// Utility functions
export const apiUtils = {
  // Check if user is authenticated
  isAuthenticated: () => {
    const token = localStorage.getItem('authToken');
    return !!token;
  },

  // Get current user from localStorage
  getCurrentUser: () => {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
  },

  // Clear authentication data
  clearAuth: () => {
    localStorage.removeItem('authToken');
    localStorage.removeItem('user');
  },

  // Get auth token
  getAuthToken: () => {
    return localStorage.getItem('authToken');
  },
};

export default {
  authAPI,
  cameraAPI,
  testAPI,
  healthAPI,
  apiUtils,
  API_CONFIG,
}; 