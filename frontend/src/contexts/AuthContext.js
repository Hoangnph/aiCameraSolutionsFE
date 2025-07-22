import React, { createContext, useContext, useState, useEffect } from 'react';
import { authAPI, apiUtils } from '../services/api';

// Create Auth Context
const AuthContext = createContext();

// Auth Provider Component
export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  // Check authentication status on mount
  useEffect(() => {
    const checkAuthStatus = async () => {
      try {
        console.log('🔐 AuthContext: Starting authentication check...');
        setIsLoading(true);
        setError(null);

        // First check localStorage
        const token = localStorage.getItem('authToken');
        const userData = localStorage.getItem('user');
        
        console.log('🔐 AuthContext: LocalStorage check:', {
          hasToken: !!token,
          hasUser: !!userData
        });
        
        if (!token || !userData) {
          console.log('🔐 AuthContext: No token or user found, setting unauthenticated');
          setIsAuthenticated(false);
          setUser(null);
          setIsLoading(false);
          return;
        }

        // Try to parse user data
        let parsedUser = null;
        try {
          parsedUser = JSON.parse(userData);
        } catch (e) {
          console.log('🔐 AuthContext: Invalid user data in localStorage');
          localStorage.removeItem('authToken');
          localStorage.removeItem('user');
          setIsAuthenticated(false);
          setUser(null);
          setIsLoading(false);
          return;
        }

        // Set user from localStorage immediately
        setUser(parsedUser);
        setIsAuthenticated(true);
        console.log('🔐 AuthContext: Set authenticated from localStorage');

        // Verify token with server in background
        try {
          console.log('🔐 AuthContext: Verifying token with server...');
          const response = await authAPI.verifyToken();
          console.log('🔐 AuthContext: Token verification response:', response);
          
          if (response && response.success) {
            console.log('🔐 AuthContext: Token valid, keeping authenticated');
            setUser(response.data.user);
            setIsAuthenticated(true);
          } else {
            // Token is invalid, clear local storage
            console.log('🔐 AuthContext: Token invalid, clearing auth data');
            localStorage.removeItem('authToken');
            localStorage.removeItem('user');
            setUser(null);
            setIsAuthenticated(false);
          }
        } catch (error) {
          console.error('🔐 AuthContext: Token verification error:', error);
          // Keep authenticated if server is unreachable but we have valid localStorage data
          console.log('🔐 AuthContext: Server unreachable, keeping authenticated from localStorage');
        }
      } catch (error) {
        console.error('🔐 AuthContext: Auth check error:', error);
        localStorage.removeItem('authToken');
        localStorage.removeItem('user');
        setUser(null);
        setIsAuthenticated(false);
        setError('Authentication check failed');
      } finally {
        console.log('🔐 AuthContext: Auth check completed, setting loading to false');
        setIsLoading(false);
      }
    };

    checkAuthStatus();
  }, []); // Empty dependency array - only run once

  // Login user
  const login = async (credentials) => {
    try {
      setIsLoading(true);
      setError(null);

      const response = await authAPI.login(credentials);
      
      if (response.success) {
        setUser(response.data.user);
        setIsAuthenticated(true);
        return { success: true, data: response.data };
      } else {
        setError(response.error?.message || 'Login failed');
        return { success: false, error: response.error };
      }
    } catch (error) {
      console.error('Login error:', error);
      const errorMessage = error.response?.data?.error?.message || 'Login failed';
      setError(errorMessage);
      return { success: false, error: { message: errorMessage } };
    } finally {
      setIsLoading(false);
    }
  };

  // Register user
  const register = async (userData) => {
    try {
      setIsLoading(true);
      setError(null);

      const response = await authAPI.register(userData);
      
      if (response.success) {
        setUser(response.data.user);
        setIsAuthenticated(true);
        return { success: true, data: response.data };
      } else {
        setError(response.error?.message || 'Registration failed');
        return { success: false, error: response.error };
      }
    } catch (error) {
      console.error('Registration error:', error);
      const errorMessage = error.response?.data?.error?.message || 'Registration failed';
      setError(errorMessage);
      return { success: false, error: { message: errorMessage } };
    } finally {
      setIsLoading(false);
    }
  };

  // Logout user
  const logout = async () => {
    try {
      await authAPI.logout();
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      // Clear local state regardless of server response
      localStorage.removeItem('authToken');
      localStorage.removeItem('user');
      setUser(null);
      setIsAuthenticated(false);
      setError(null);
    }
  };

  // Clear error
  const clearError = () => {
    setError(null);
  };

  // Context value
  const value = {
    user,
    isAuthenticated,
    isLoading,
    error,
    login,
    register,
    logout,
    clearError,
  };

  // Debug: Log authentication state changes
  console.log('🔐 AuthContext State:', {
    user: !!user,
    isAuthenticated,
    isLoading,
    error: !!error
  });

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

// Custom hook to use auth context
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export default AuthContext; 