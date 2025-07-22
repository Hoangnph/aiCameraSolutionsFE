// WebSocket Configuration
const WS_CONFIG = {
  URL: process.env.REACT_APP_WS_URL || 'ws://localhost:3003',
  OPTIONS: {
    timeout: 10000,
    reconnectionAttempts: 5,
    reconnectionDelay: 1000,
    reconnectionDelayMax: 5000,
  },
};

class WebSocketService {
  constructor() {
    this.socket = null;
    this.isConnected = false;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
    this.listeners = new Map();
    this.clientId = 'frontend_' + Math.random().toString(36).substr(2, 9);
  }

  // Connect to WebSocket server
  connect() {
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      console.log('WebSocket already connected');
      return;
    }

    try {
      // Connect to camera updates endpoint
      this.socket = new WebSocket(`${WS_CONFIG.URL}/ws/camera-updates/${this.clientId}`);

      this.socket.onopen = () => {
        console.log('WebSocket connected');
        this.isConnected = true;
        this.reconnectAttempts = 0;
        this.emit('client_ready', { clientId: this.clientId, timestamp: Date.now() });
        
        // Send initial ping to test connection
        this.sendPing();
      };

      this.socket.onclose = (event) => {
        console.log('WebSocket disconnected:', event.code, event.reason);
        this.isConnected = false;
        this.handleReconnect();
      };

      this.socket.onerror = (error) => {
        console.error('WebSocket error:', error);
        this.handleReconnect();
      };

      this.socket.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          this.handleMessage(data);
        } catch (error) {
          console.error('Error parsing WebSocket message:', error);
        }
      };

    } catch (error) {
      console.error('Error creating WebSocket connection:', error);
      this.handleReconnect();
    }
  }

  // Handle incoming messages
  handleMessage(data) {
    console.log('Received WebSocket message:', data);
    
    // Emit to registered listeners
    if (data.type && this.listeners.has(data.type)) {
      this.listeners.get(data.type).forEach(callback => {
        try {
          callback(data);
        } catch (error) {
          console.error('Error in WebSocket message handler:', error);
        }
      });
    }
  }

  // Handle reconnection
  handleReconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      const delay = Math.min(1000 * this.reconnectAttempts, 5000);
      console.log(`Attempting to reconnect in ${delay}ms (${this.reconnectAttempts}/${this.maxReconnectAttempts})`);
      
      setTimeout(() => {
        if (!this.isConnected) {
          this.connect();
        }
      }, delay);
    } else {
      console.error('Max reconnection attempts reached');
    }
  }

  // Disconnect from WebSocket server
  disconnect() {
    if (this.socket) {
      this.socket.close(1000, 'User initiated disconnect');
      this.socket = null;
      this.isConnected = false;
      this.listeners.clear();
    }
  }

  // Send message to server
  emit(event, data) {
    if (this.socket && this.isConnected) {
      const message = {
        type: event,
        data: data,
        timestamp: Date.now()
      };
      this.socket.send(JSON.stringify(message));
    } else {
      console.warn('WebSocket not connected, cannot emit event:', event);
    }
  }

  // Listen for events from server
  on(event, callback) {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, []);
    }
    this.listeners.get(event).push(callback);
  }

  // Remove event listener
  off(event, callback) {
    if (this.listeners.has(event)) {
      const listeners = this.listeners.get(event);
      if (callback) {
        const index = listeners.indexOf(callback);
        if (index > -1) {
          listeners.splice(index, 1);
        }
      } else {
        this.listeners.delete(event);
      }
    }
  }

  // Remove all listeners
  removeAllListeners() {
    this.listeners.clear();
  }

  // Get connection status
  getConnectionStatus() {
    return {
      isConnected: this.isConnected,
      reconnectAttempts: this.reconnectAttempts,
      maxReconnectAttempts: this.maxReconnectAttempts,
      readyState: this.socket ? this.socket.readyState : null,
    };
  }

  // Subscribe to camera count updates
  subscribeToCameraCounts(cameraId) {
    this.emit('subscribe_camera_counts', { cameraId });
  }

  // Unsubscribe from camera count updates
  unsubscribeFromCameraCounts(cameraId) {
    this.emit('unsubscribe_camera_counts', { cameraId });
  }

  // Subscribe to system status updates
  subscribeToSystemStatus() {
    this.emit('subscribe_system_status');
  }

  // Unsubscribe from system status updates
  unsubscribeFromSystemStatus() {
    this.emit('unsubscribe_system_status');
  }

  // Request camera count data
  requestCameraCounts(cameraId, limit = 100) {
    this.emit('request_camera_counts', { cameraId, limit });
  }

  // Request system analytics
  requestSystemAnalytics() {
    this.emit('request_system_analytics');
  }

  // Send ping to test connection
  sendPing() {
    if (this.isConnected && this.socket) {
      this.socket.send(JSON.stringify({
        type: 'ping',
        clientId: this.clientId,
        timestamp: Date.now()
      }));
    }
  }

  // Send camera update
  sendCameraUpdate(cameraId, data) {
    if (this.isConnected && this.socket) {
      this.socket.send(JSON.stringify({
        type: 'camera_update',
        camera_id: cameraId,
        data: data,
        timestamp: Date.now()
      }));
    }
  }

  // Send analytics update
  sendAnalyticsUpdate(data) {
    if (this.isConnected && this.socket) {
      this.socket.send(JSON.stringify({
        type: 'analytics_update',
        data: data,
        timestamp: Date.now()
      }));
    }
  }

  // Send system status update
  sendSystemStatus(data) {
    if (this.isConnected && this.socket) {
      this.socket.send(JSON.stringify({
        type: 'system_status',
        data: data,
        timestamp: Date.now()
      }));
    }
  }

  // Send alert
  sendAlert(alertType, message, severity = 'info') {
    if (this.isConnected && this.socket) {
      this.socket.send(JSON.stringify({
        type: 'alert',
        alert_type: alertType,
        message: message,
        severity: severity,
        timestamp: Date.now()
      }));
    }
  }

  // Get real-time camera status
  getRealTimeCameraStatus(cameraId) {
    return new Promise((resolve, reject) => {
      if (!this.isConnected) {
        reject(new Error('WebSocket not connected'));
        return;
      }

      const timeout = setTimeout(() => {
        reject(new Error('Timeout waiting for camera status'));
      }, 5000);

      const handler = (data) => {
        if (data.type === 'camera_update' && data.camera_id === cameraId) {
          clearTimeout(timeout);
          this.off('camera_update', handler);
          resolve(data);
        }
      };

      this.on('camera_update', handler);
      this.sendCameraUpdate(cameraId, { request_status: true });
    });
  }

  // Subscribe to real-time analytics
  subscribeToRealTimeAnalytics(callback) {
    this.on('analytics_update', callback);
    this.requestSystemAnalytics();
  }

  // Subscribe to real-time system status
  subscribeToRealTimeSystemStatus(callback) {
    this.on('system_status', callback);
    this.sendSystemStatus({ request_status: true });
  }

  // Subscribe to real-time alerts
  subscribeToRealTimeAlerts(callback) {
    this.on('alert', callback);
  }
}

// Create singleton instance
const websocketService = new WebSocketService();

// Event types for real-time updates
export const WS_EVENTS = {
  // Camera events
  CAMERA_COUNT_UPDATE: 'camera_count_update',
  CAMERA_STATUS_UPDATE: 'camera_status_update',
  CAMERA_PROCESSING_START: 'camera_processing_start',
  CAMERA_PROCESSING_STOP: 'camera_processing_stop',
  CAMERA_ERROR: 'camera_error',

  // System events
  SYSTEM_STATUS_UPDATE: 'system_status_update',
  WORKER_POOL_UPDATE: 'worker_pool_update',
  ANALYTICS_UPDATE: 'analytics_update',

  // Client events
  CLIENT_READY: 'client_ready',
  CLIENT_DISCONNECT: 'client_disconnect',

  // Error events
  ERROR: 'error',
  CONNECTION_ERROR: 'connection_error',
};

// Hook for React components
export const useWebSocket = () => {
  return {
    connect: () => websocketService.connect(),
    disconnect: () => websocketService.disconnect(),
    emit: (event, data) => websocketService.emit(event, data),
    on: (event, callback) => websocketService.on(event, callback),
    off: (event, callback) => websocketService.off(event, callback),
    isConnected: websocketService.isConnected,
    getConnectionStatus: () => websocketService.getConnectionStatus(),
    subscribeToCameraCounts: (cameraId) => websocketService.subscribeToCameraCounts(cameraId),
    unsubscribeFromCameraCounts: (cameraId) => websocketService.unsubscribeFromCameraCounts(cameraId),
    subscribeToSystemStatus: () => websocketService.subscribeToSystemStatus(),
    unsubscribeFromSystemStatus: () => websocketService.unsubscribeFromSystemStatus(),
    requestCameraCounts: (cameraId, limit) => websocketService.requestCameraCounts(cameraId, limit),
    requestSystemAnalytics: () => websocketService.requestSystemAnalytics(),
    
    // New real-time methods
    sendPing: () => websocketService.sendPing(),
    sendCameraUpdate: (cameraId, data) => websocketService.sendCameraUpdate(cameraId, data),
    sendAnalyticsUpdate: (data) => websocketService.sendAnalyticsUpdate(data),
    sendSystemStatus: (data) => websocketService.sendSystemStatus(data),
    sendAlert: (alertType, message, severity) => websocketService.sendAlert(alertType, message, severity),
    getRealTimeCameraStatus: (cameraId) => websocketService.getRealTimeCameraStatus(cameraId),
    subscribeToRealTimeAnalytics: (callback) => websocketService.subscribeToRealTimeAnalytics(callback),
    subscribeToRealTimeSystemStatus: (callback) => websocketService.subscribeToRealTimeSystemStatus(callback),
    subscribeToRealTimeAlerts: (callback) => websocketService.subscribeToRealTimeAlerts(callback),
  };
};

export default websocketService; 