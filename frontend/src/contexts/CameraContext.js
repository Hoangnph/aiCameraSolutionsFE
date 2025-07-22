import React, { createContext, useContext, useState, useEffect } from 'react';
import { cameraAPI, testAPI } from '../services/api';
import websocketService from '../services/websocket';

// Create Camera Context
const CameraContext = createContext();

// Camera Provider Component
export const CameraProvider = ({ children }) => {
  const [cameras, setCameras] = useState([]);
  const [selectedCamera, setSelectedCamera] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [analytics, setAnalytics] = useState(null);
  const [workerPoolStatus, setWorkerPoolStatus] = useState(null);
  const [realTimeData, setRealTimeData] = useState({});

  // Load cameras on mount - only run once
  useEffect(() => {
    const initializeData = async () => {
      try {
        // Load cameras
        const camerasResponse = await cameraAPI.getCameras();
        if (camerasResponse.success) {
          setCameras(camerasResponse.data || []);
        }

        // Load analytics
        try {
          const analyticsResponse = await cameraAPI.getAnalyticsSummary();
          if (analyticsResponse.success) {
            setAnalytics(analyticsResponse.data);
          }
        } catch (error) {
          console.error('Load analytics error:', error);
        }

        // Load worker pool status
        try {
          const workerResponse = await cameraAPI.getWorkerPoolStatus();
          if (workerResponse.success) {
            setWorkerPoolStatus(workerResponse.data);
          }
        } catch (error) {
          console.error('Load worker pool status error:', error);
        }

        // Setup WebSocket
        setupWebSocket();
      } catch (error) {
        console.error('Initialize data error:', error);
        setError('Failed to load initial data');
      }
    };

    initializeData();
  }, []); // Empty dependency array - only run once

  // Setup WebSocket listeners
  const setupWebSocket = () => {
    // Camera count updates
    websocketService.on('camera_count_update', (data) => {
      setRealTimeData(prev => ({
        ...prev,
        [data.camera_id]: data
      }));
    });

    // Camera status updates
    websocketService.on('camera_status_update', (data) => {
      setCameras(prev => prev.map(camera => 
        camera.id === data.camera_id 
          ? { ...camera, status: data.status }
          : camera
      ));
    });

    // System analytics updates
    websocketService.on('analytics_update', (data) => {
      setAnalytics(data);
    });

    // Worker pool updates
    websocketService.on('worker_pool_update', (data) => {
      setWorkerPoolStatus(data);
    });

    // Error handling
    websocketService.on('camera_error', (data) => {
      setError(`Camera ${data.camera_id} error: ${data.message}`);
    });

    // Connect to WebSocket
    websocketService.connect();
  };

  // Load all cameras
  const loadCameras = async (useTestAPI = false) => {
    try {
      setIsLoading(true);
      setError(null);

      let response;
      if (useTestAPI) {
        response = await testAPI.getCameras();
      } else {
        response = await cameraAPI.getCameras();
      }

      if (response.success || useTestAPI) {
        const cameraData = useTestAPI ? response : response.data;
        setCameras(cameraData);
        return { success: true, data: cameraData };
      } else {
        setError(response.error?.message || 'Failed to load cameras');
        return { success: false, error: response.error };
      }
    } catch (error) {
      console.error('Load cameras error:', error);
      const errorMessage = error.response?.data?.error?.message || 'Failed to load cameras';
      setError(errorMessage);
      return { success: false, error: { message: errorMessage } };
    } finally {
      setIsLoading(false);
    }
  };

  // Create new camera
  const createCamera = async (cameraData) => {
    try {
      setIsLoading(true);
      setError(null);

      const response = await cameraAPI.createCamera(cameraData);
      
      if (response.success) {
        const newCamera = response.data;
        setCameras(prev => [...prev, newCamera]);
        return { success: true, data: newCamera };
      } else {
        setError(response.error?.message || 'Failed to create camera');
        return { success: false, error: response.error };
      }
    } catch (error) {
      console.error('Create camera error:', error);
      const errorMessage = error.response?.data?.error?.message || 'Failed to create camera';
      setError(errorMessage);
      return { success: false, error: { message: errorMessage } };
    } finally {
      setIsLoading(false);
    }
  };

  // Update camera
  const updateCamera = async (cameraId, cameraData) => {
    try {
      setIsLoading(true);
      setError(null);

      const response = await cameraAPI.updateCamera(cameraId, cameraData);
      
      if (response.success) {
        const updatedCamera = response.data;
        setCameras(prev => prev.map(camera => 
          camera.id === cameraId ? updatedCamera : camera
        ));
        return { success: true, data: updatedCamera };
      } else {
        setError(response.error?.message || 'Failed to update camera');
        return { success: false, error: response.error };
      }
    } catch (error) {
      console.error('Update camera error:', error);
      const errorMessage = error.response?.data?.error?.message || 'Failed to update camera';
      setError(errorMessage);
      return { success: false, error: { message: errorMessage } };
    } finally {
      setIsLoading(false);
    }
  };

  // Delete camera
  const deleteCamera = async (cameraId) => {
    try {
      setIsLoading(true);
      setError(null);

      const response = await cameraAPI.deleteCamera(cameraId);
      
      if (response.success) {
        setCameras(prev => prev.filter(camera => camera.id !== cameraId));
        if (selectedCamera?.id === cameraId) {
          setSelectedCamera(null);
        }
        return { success: true };
      } else {
        setError(response.error?.message || 'Failed to delete camera');
        return { success: false, error: response.error };
      }
    } catch (error) {
      console.error('Delete camera error:', error);
      const errorMessage = error.response?.data?.error?.message || 'Failed to delete camera';
      setError(errorMessage);
      return { success: false, error: { message: errorMessage } };
    } finally {
      setIsLoading(false);
    }
  };

  // Update camera status
  const updateCameraStatus = async (cameraId, status) => {
    try {
      const response = await cameraAPI.updateCameraStatus(cameraId, status);
      
      if (response.success) {
        setCameras(prev => prev.map(camera => 
          camera.id === cameraId ? { ...camera, status } : camera
        ));
        return { success: true };
      } else {
        setError(response.error?.message || 'Failed to update camera status');
        return { success: false, error: response.error };
      }
    } catch (error) {
      console.error('Update camera status error:', error);
      const errorMessage = error.response?.data?.error?.message || 'Failed to update camera status';
      setError(errorMessage);
      return { success: false, error: { message: errorMessage } };
    }
  };

  // Start camera processing
  const startCameraProcessing = async (cameraId) => {
    try {
      const response = await cameraAPI.startCameraProcessing(cameraId);
      
      if (response.success) {
        setCameras(prev => prev.map(camera => 
          camera.id === cameraId ? { ...camera, status: 'processing' } : camera
        ));
        return { success: true };
      } else {
        setError(response.error?.message || 'Failed to start camera processing');
        return { success: false, error: response.error };
      }
    } catch (error) {
      console.error('Start camera processing error:', error);
      const errorMessage = error.response?.data?.error?.message || 'Failed to start camera processing';
      setError(errorMessage);
      return { success: false, error: { message: errorMessage } };
    }
  };

  // Stop camera processing
  const stopCameraProcessing = async (cameraId) => {
    try {
      const response = await cameraAPI.stopCameraProcessing(cameraId);
      
      if (response.success) {
        setCameras(prev => prev.map(camera => 
          camera.id === cameraId ? { ...camera, status: 'offline' } : camera
        ));
        return { success: true };
      } else {
        setError(response.error?.message || 'Failed to stop camera processing');
        return { success: false, error: response.error };
      }
    } catch (error) {
      console.error('Stop camera processing error:', error);
      const errorMessage = error.response?.data?.error?.message || 'Failed to stop camera processing';
      setError(errorMessage);
      return { success: false, error: { message: errorMessage } };
    }
  };

  // Test camera connection
  const testCameraConnection = async (cameraId) => {
    try {
      const response = await cameraAPI.testCameraConnection(cameraId);
      return response;
    } catch (error) {
      console.error('Test camera connection error:', error);
      const errorMessage = error.response?.data?.error?.message || 'Failed to test camera connection';
      setError(errorMessage);
      return { success: false, error: { message: errorMessage } };
    }
  };

  // Get count data
  const getCountData = async (cameraId = null, limit = 100) => {
    try {
      const response = await cameraAPI.getCountData(cameraId, limit);
      return response;
    } catch (error) {
      console.error('Get count data error:', error);
      const errorMessage = error.response?.data?.error?.message || 'Failed to get count data';
      setError(errorMessage);
      return { success: false, error: { message: errorMessage } };
    }
  };

  // Subscribe to camera real-time updates
  const subscribeToCamera = (cameraId) => {
    websocketService.subscribeToCameraCounts(cameraId);
  };

  // Unsubscribe from camera real-time updates
  const unsubscribeFromCamera = (cameraId) => {
    websocketService.unsubscribeFromCameraCounts(cameraId);
  };

  // Clear error
  const clearError = () => {
    setError(null);
  };

  // Context value
  const value = {
    cameras,
    selectedCamera,
    isLoading,
    error,
    analytics,
    workerPoolStatus,
    realTimeData,
    setSelectedCamera,
    loadCameras,
    createCamera,
    updateCamera,
    deleteCamera,
    updateCameraStatus,
    startCameraProcessing,
    stopCameraProcessing,
    testCameraConnection,
    getCountData,
    subscribeToCamera,
    unsubscribeFromCamera,
    clearError,
  };

  return (
    <CameraContext.Provider value={value}>
      {children}
    </CameraContext.Provider>
  );
};

// Custom hook to use camera context
export const useCamera = () => {
  const context = useContext(CameraContext);
  if (!context) {
    throw new Error('useCamera must be used within a CameraProvider');
  }
  return context;
};

export default CameraContext; 