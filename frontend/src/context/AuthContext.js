import React, { createContext, useContext, useReducer, useEffect, useCallback } from 'react';
import { authAPI } from '../services/authAPI';

const AuthContext = createContext();

const initialState = {
  user: null,
  isAuthenticated: false,
  isLoading: true,
  error: null,
  accessToken: localStorage.getItem('accessToken'),
  refreshToken: localStorage.getItem('refreshToken'),
};

const authReducer = (state, action) => {
  switch (action.type) {
    case 'LOGIN_START':
      return {
        ...state,
        isLoading: true,
        error: null,
      };
    case 'LOGIN_SUCCESS':
      return {
        ...state,
        user: action.payload.user,
        isAuthenticated: true,
        isLoading: false,
        error: null,
        accessToken: action.payload.accessToken,
        refreshToken: action.payload.refreshToken,
      };
    case 'LOGIN_FAILURE':
      return {
        ...state,
        isLoading: false,
        error: action.payload,
        isAuthenticated: false,
        user: null,
      };
    case 'LOGOUT':
      return {
        ...state,
        user: null,
        isAuthenticated: false,
        isLoading: false,
        error: null,
        accessToken: null,
        refreshToken: null,
      };
    case 'SET_LOADING':
      return {
        ...state,
        isLoading: action.payload,
      };
    case 'SET_ERROR':
      return {
        ...state,
        error: action.payload,
      };
    case 'UPDATE_USER':
      return {
        ...state,
        user: { ...state.user, ...action.payload },
      };
    default:
      return state;
  }
};

export const AuthProvider = ({ children }) => {
  const [state, dispatch] = useReducer(authReducer, initialState);

  // Check if user is authenticated on app load
  useEffect(() => {
    const checkAuth = async () => {
      if (state.accessToken) {
        try {
          dispatch({ type: 'SET_LOADING', payload: true });
          const userData = await authAPI.getCurrentUser();
          dispatch({
            type: 'LOGIN_SUCCESS',
            payload: {
              user: userData,
              accessToken: state.accessToken,
              refreshToken: state.refreshToken,
            },
          });
        } catch (error) {
          console.error('Auth check failed:', error);
          // Clear invalid tokens
          localStorage.removeItem('accessToken');
          localStorage.removeItem('refreshToken');
          dispatch({ type: 'LOGOUT' });
        }
      } else {
        dispatch({ type: 'SET_LOADING', payload: false });
      }
    };

    checkAuth();
  }, []);

  const login = async (credentials) => {
    try {
      dispatch({ type: 'LOGIN_START' });
      const response = await authAPI.login(credentials);
      
      // Store tokens
      localStorage.setItem('accessToken', response.accessToken);
      localStorage.setItem('refreshToken', response.refreshToken);
      
      dispatch({
        type: 'LOGIN_SUCCESS',
        payload: response,
      });
      
      return { success: true };
    } catch (error) {
      dispatch({
        type: 'LOGIN_FAILURE',
        payload: error.message || 'Login failed',
      });
      return { success: false, error: error.message };
    }
  };

  const register = async (userData) => {
    try {
      // KHÔNG dispatch LOGIN_START ở đây để tránh reset state context
      const response = await authAPI.register(userData);
      
      // KHÔNG tự động lưu tokens và đăng nhập sau khi đăng ký
      // Chỉ trả về success message để UI hiển thị thông báo
      return { 
        success: true, 
        message: 'Đăng ký thành công! Vui lòng đăng nhập để tiếp tục.',
        user: response.user || null
      };
    } catch (error) {
      // KHÔNG dispatch LOGIN_FAILURE ở đây để tránh reset state context và local state của SignUp
      // Chỉ throw error cho UI xử lý
      throw error; // Trả về toàn bộ object lỗi cho UI xử lý
    }
  };

  const logout = async () => {
    try {
      if (state.accessToken) {
        await authAPI.logout();
      }
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      // Clear tokens regardless of API call success
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
      dispatch({ type: 'LOGOUT' });
    }
  };

  const updateUser = (userData) => {
    dispatch({ type: 'UPDATE_USER', payload: userData });
  };

  const changePassword = async (passwordData) => {
    try {
      const response = await authAPI.changePassword(passwordData);
      return { success: true, message: response.message };
    } catch (error) {
      return { success: false, error: error.message };
    }
  };

  const clearError = useCallback(() => {
    dispatch({ type: 'SET_ERROR', payload: null });
  }, []);

  const value = {
    ...state,
    login,
    register,
    logout,
    updateUser,
    changePassword,
    clearError,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}; 