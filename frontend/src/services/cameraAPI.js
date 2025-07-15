const CAMERA_API_BASE_URL = process.env.REACT_APP_CAMERA_API_URL || 'http://localhost:3002/api/v1';

class CameraAPI {
  constructor() {
    this.baseURL = CAMERA_API_BASE_URL;
  }

  // Helper method to make API calls
  async makeRequest(endpoint, options = {}) {
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
      const data = await response.json();

      if (!response.ok) {
        throw { status: response.status, ...data };
      }

      return data;
    } catch (error) {
      if (error.name === 'TypeError' && error.message.includes('fetch')) {
        throw new Error('Network error. Please check your connection.');
      }
      throw error;
    }
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
}

export const cameraAPI = new CameraAPI(); 