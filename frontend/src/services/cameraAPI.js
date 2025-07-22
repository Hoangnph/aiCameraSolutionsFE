const CAMERA_API_BASE_URL = process.env.REACT_APP_CAMERA_API_URL || 'http://localhost:3002/api/v1';

// Mock data for development when backend is not ready
const MOCK_CAMERAS = [
  {
    id: 1,
    name: "Main Entrance Camera",
    ip_address: "192.168.1.100",
    rtsp_url: "rtsp://192.168.1.100:554/stream1",
    status: "active",
    location: "Main Entrance",
    created_at: "2024-07-15T10:00:00Z",
    updated_at: "2024-07-16T08:30:00Z"
  },
  {
    id: 2,
    name: "Parking Lot Camera",
    ip_address: "192.168.1.101",
    rtsp_url: "rtsp://192.168.1.101:554/stream1",
    status: "offline",
    location: "Parking Lot",
    created_at: "2024-07-15T11:00:00Z",
    updated_at: "2024-07-16T09:15:00Z"
  },
  {
    id: 3,
    name: "Office Building Camera",
    ip_address: "192.168.1.102",
    rtsp_url: "rtsp://192.168.1.102:554/stream1",
    status: "maintenance",
    location: "Office Building",
    created_at: "2024-07-15T12:00:00Z",
    updated_at: "2024-07-16T10:00:00Z"
  },
  {
    id: 4,
    name: "Security Gate Camera",
    ip_address: "192.168.1.103",
    rtsp_url: "rtsp://192.168.1.103:554/stream1",
    status: "active",
    location: "Security Gate",
    created_at: "2024-07-15T13:00:00Z",
    updated_at: "2024-07-16T11:30:00Z"
  }
];

class CameraAPI {
  constructor() {
    this.baseURL = CAMERA_API_BASE_URL;
    this.useMockData = false; // Flag to control mock data usage
    this.websocket = null;
    this.websocketUrl = process.env.REACT_APP_WEBSOCKET_URL || 'ws://localhost:3003';
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
  }

  // WebSocket connection management
  connectWebSocket(onMessage) {
    if (this.useMockData) {
      console.log('Using mock WebSocket for development');
      return this.createMockWebSocket(onMessage);
    }

    try {
      // Use correct WebSocket endpoint with client ID
      const clientId = 'frontend_' + Math.random().toString(36).substr(2, 9);
      const wsUrl = `${this.websocketUrl}/ws/camera-updates/${clientId}`;
      
      this.websocket = new WebSocket(wsUrl);
      
      this.websocket.onopen = () => {
        console.log('WebSocket connected to:', wsUrl);
        this.reconnectAttempts = 0;
      };
      
      this.websocket.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          onMessage(data);
        } catch (error) {
          console.error('Error parsing WebSocket message:', error);
        }
      };
      
      this.websocket.onclose = () => {
        console.log('WebSocket disconnected');
        this.attemptReconnect(onMessage);
      };
      
      this.websocket.onerror = (error) => {
        console.error('WebSocket error:', error);
      };
      
    } catch (error) {
      console.error('Failed to create WebSocket connection:', error);
      this.createMockWebSocket(onMessage);
    }
  }

  // Mock WebSocket for development
  createMockWebSocket(onMessage) {
    console.log('Creating mock WebSocket connection');
    
    // Simulate real-time updates every 5 seconds
    const mockInterval = setInterval(() => {
      const mockUpdate = {
        type: 'camera_update',
        data: {
          camera_id: Math.floor(Math.random() * 4) + 1,
          status: ['active', 'offline', 'maintenance'][Math.floor(Math.random() * 3)],
          people_count: Math.floor(Math.random() * 50),
          timestamp: new Date().toISOString()
        }
      };
      onMessage(mockUpdate);
    }, 5000);

    // Store interval ID for cleanup
    this.mockInterval = mockInterval;
  }

  // Attempt to reconnect WebSocket
  attemptReconnect(onMessage) {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      console.log(`Attempting WebSocket reconnection ${this.reconnectAttempts}/${this.maxReconnectAttempts}`);
      
      setTimeout(() => {
        this.connectWebSocket(onMessage);
      }, 2000 * this.reconnectAttempts); // Exponential backoff
    } else {
      console.log('Max WebSocket reconnection attempts reached');
    }
  }

  // Disconnect WebSocket
  disconnectWebSocket() {
    if (this.websocket) {
      this.websocket.close();
      this.websocket = null;
    }
    if (this.mockInterval) {
      clearInterval(this.mockInterval);
      this.mockInterval = null;
    }
  }

  // Send message via WebSocket
  sendWebSocketMessage(message) {
    if (this.websocket && this.websocket.readyState === WebSocket.OPEN) {
      this.websocket.send(JSON.stringify(message));
    } else {
      console.warn('WebSocket not connected, message not sent:', message);
    }
  }

  // Helper method to check if backend is available
  async checkBackendHealth() {
    try {
      const response = await fetch(`${this.baseURL.replace('/api/v1', '')}/health`, {
        method: 'GET',
        timeout: 3000
      });
      return response.ok;
    } catch (error) {
      console.warn('Backend health check failed, using mock data:', error.message);
      return false;
    }
  }

  // Helper method to make API calls with fallback to mock data
  async makeRequest(endpoint, options = {}) {
    // Check if we should use mock data
    if (this.useMockData) {
      return this.handleMockRequest(endpoint, options);
    }

    const url = `${this.baseURL}${endpoint}`;
    
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    // Add auth token if available
    const token = localStorage.getItem('accessToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    try {
      const response = await fetch(url, config);

      if (!response.ok) {
        // If backend returns 401 (Unauthorized), try test endpoint
        if (response.status === 401) {
          console.warn(`Authentication failed for ${endpoint}, trying test endpoint`);
          return this.makeTestRequest(endpoint, options);
        }
        
        // If other error, fallback to mock data
        console.warn(`Backend request failed for ${endpoint}, falling back to mock data`);
        this.useMockData = true;
        return this.handleMockRequest(endpoint, options);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.warn(`Network error for ${endpoint}, falling back to mock data:`, error.message);
      this.useMockData = true;
      return this.handleMockRequest(endpoint, options);
    }
  }

  // Make request to test endpoints (no authentication required)
  async makeTestRequest(endpoint, options = {}) {
    const testUrl = `${this.baseURL.replace('/api/v1', '/api/v1/test')}${endpoint}`;
    
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(testUrl, config);

      if (!response.ok) {
        console.warn(`Test endpoint failed for ${endpoint}, falling back to mock data`);
        this.useMockData = true;
        return this.handleMockRequest(endpoint, options);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.warn(`Test endpoint error for ${endpoint}, falling back to mock data:`, error.message);
      this.useMockData = true;
      return this.handleMockRequest(endpoint, options);
    }
  }

  // Handle mock data requests
  handleMockRequest(endpoint, options = {}) {
    console.log(`Using mock data for: ${endpoint}`);
    
    // Simulate network delay
    return new Promise((resolve) => {
      setTimeout(() => {
        switch (endpoint) {
          case '/cameras':
            if (options.method === 'GET') {
              resolve({ success: true, data: MOCK_CAMERAS });
            } else if (options.method === 'POST') {
              const newCamera = JSON.parse(options.body);
              newCamera.id = MOCK_CAMERAS.length + 1;
              newCamera.created_at = new Date().toISOString();
              newCamera.updated_at = new Date().toISOString();
              MOCK_CAMERAS.push(newCamera);
              resolve({ success: true, data: newCamera });
            }
            break;
            
          case (endpoint.match(/^\/cameras\/\d+$/) || {}).input:
            const id = parseInt(endpoint.split('/').pop());
            const camera = MOCK_CAMERAS.find(c => c.id === id);
            
            if (options.method === 'GET') {
              resolve({ success: true, data: camera });
            } else if (options.method === 'PUT') {
              const updatedData = JSON.parse(options.body);
              Object.assign(camera, updatedData, { updated_at: new Date().toISOString() });
              resolve({ success: true, data: camera });
            } else if (options.method === 'DELETE') {
              const index = MOCK_CAMERAS.findIndex(c => c.id === id);
              if (index > -1) {
                MOCK_CAMERAS.splice(index, 1);
              }
              resolve({ success: true, message: 'Camera deleted successfully' });
            }
            break;
            
          default:
            resolve({ success: false, message: 'Endpoint not found in mock data' });
        }
      }, 500); // Simulate 500ms delay
    });
  }

  // Get all cameras
  async getCameras() {
    const response = await this.makeRequest('/cameras');
    
    if (response.success) {
      return response.data;
    }
    
    throw new Error('Failed to get cameras');
  }

  // Create a new camera
  async createCamera(cameraData) {
    const response = await this.makeRequest('/cameras', {
      method: 'POST',
      body: JSON.stringify(cameraData),
    });

    if (response.success) {
      return response.data;
    }
    
    throw new Error('Failed to create camera');
  }

  // Get camera by ID
  async getCameraById(cameraId) {
    const response = await this.makeRequest(`/cameras/${cameraId}`);
    
    if (response.success) {
      return response.data;
    }
    
    throw new Error('Failed to get camera');
  }

  // Update camera
  async updateCamera(cameraId, cameraData) {
    const response = await this.makeRequest(`/cameras/${cameraId}`, {
      method: 'PUT',
      body: JSON.stringify(cameraData),
    });

    if (response.success) {
      return response.data;
    }
    
    throw new Error('Failed to update camera');
  }

  // Delete camera
  async deleteCamera(cameraId) {
    const response = await this.makeRequest(`/cameras/${cameraId}`, {
      method: 'DELETE',
    });

    if (response.success) {
      return { success: true, message: response.message };
    }
    
    throw new Error('Failed to delete camera');
  }

  // Get count data
  async getCountData(cameraId = null, limit = 100) {
    let endpoint = `/counts?limit=${limit}`;
    if (cameraId) {
      endpoint += `&camera_id=${cameraId}`;
    }
    
    const response = await this.makeRequest(endpoint);
    
    if (response.success) {
      return response.data;
    }
    
    throw new Error('Failed to get count data');
  }

  // Get analytics summary
  async getAnalyticsSummary() {
    const response = await this.makeRequest('/analytics/summary');
    
    if (response.success) {
      return response.data;
    }
    
    throw new Error('Failed to get analytics summary');
  }

  // Get real-time count updates (WebSocket)
  async getRealTimeCounts(cameraId) {
    // This would typically use WebSocket connection
    // For now, return a promise that resolves with mock data
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          camera_id: cameraId,
          people_in: Math.floor(Math.random() * 10),
          people_out: Math.floor(Math.random() * 8),
          current_count: Math.floor(Math.random() * 20),
          confidence: 0.85 + Math.random() * 0.1,
          timestamp: new Date().toISOString()
        });
      }, 1000);
    });
  }

  // Health check
  async healthCheck() {
    try {
      const response = await fetch(`${this.baseURL.replace('/api/v1', '')}/health`);
      const data = await response.json();
      return data;
    } catch (error) {
      throw new Error('Camera service health check failed');
    }
  }

  // Force use mock data (for development/testing)
  enableMockData() {
    this.useMockData = true;
    console.log('Mock data enabled for development');
  }

  // Disable mock data (use real API)
  disableMockData() {
    this.useMockData = false;
    console.log('Mock data disabled, using real API');
  }
}

export const cameraAPI = new CameraAPI(); 