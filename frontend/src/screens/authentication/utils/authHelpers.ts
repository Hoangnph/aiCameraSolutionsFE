import { User, LoginCredentials, RegisterData, ForgotPasswordData, AuthTokens } from '../types/auth.types';

// Token Management
export const storeTokens = (tokens: AuthTokens): void => {
  localStorage.setItem('accessToken', tokens.accessToken);
  localStorage.setItem('refreshToken', tokens.refreshToken);
};

export const getTokens = (): AuthTokens | null => {
  const accessToken = localStorage.getItem('accessToken');
  const refreshToken = localStorage.getItem('refreshToken');
  
  if (!accessToken || !refreshToken) {
    return null;
  }
  
  return { accessToken, refreshToken };
};

export const clearTokens = (): void => {
  localStorage.removeItem('accessToken');
  localStorage.removeItem('refreshToken');
};

export const isTokenExpired = (token: string): boolean => {
  try {
    const payload = JSON.parse(atob(token.split('.')[1]));
    const currentTime = Date.now() / 1000;
    return payload.exp < currentTime;
  } catch (error) {
    return true;
  }
};

// User Management
export const storeUser = (user: User): void => {
  localStorage.setItem('user', JSON.stringify(user));
};

export const getUser = (): User | null => {
  const userStr = localStorage.getItem('user');
  if (!userStr) {
    return null;
  }
  
  try {
    return JSON.parse(userStr);
  } catch (error) {
    return null;
  }
};

export const clearUser = (): void => {
  localStorage.removeItem('user');
};

// Form Data Helpers
export const createLoginData = (formData: Record<string, any>): LoginCredentials => {
  return {
    username: formData.username || formData.email,
    password: formData.password,
    rememberMe: formData.rememberMe || false
  };
};

export const createRegisterData = (formData: Record<string, any>): RegisterData => {
  return {
    username: formData.username,
    email: formData.email,
    password: formData.password,
    confirmPassword: formData.confirmPassword,
    firstName: formData.firstName,
    lastName: formData.lastName,
    registrationCode: formData.registrationCode,
    acceptTerms: formData.acceptTerms || false
  };
};

export const createForgotPasswordData = (formData: Record<string, any>): ForgotPasswordData => {
  return {
    email: formData.email
  };
};

// URL Helpers
export const getRedirectUrl = (): string => {
  const params = new URLSearchParams(window.location.search);
  return params.get('redirect') || '/dashboard';
};

export const addRedirectParam = (url: string, redirectUrl: string): string => {
  const urlObj = new URL(url, window.location.origin);
  urlObj.searchParams.set('redirect', redirectUrl);
  return urlObj.toString();
};

// Validation Helpers
export const sanitizeInput = (input: string): string => {
  return input.trim().replace(/[<>]/g, '');
};

export const validateFormData = (data: Record<string, any>): Record<string, string> => {
  const errors: Record<string, string> = {};
  
  // Basic validation
  Object.keys(data).forEach(key => {
    if (typeof data[key] === 'string') {
      data[key] = sanitizeInput(data[key]);
    }
  });
  
  return errors;
};

// Error Handling
export const handleAuthError = (error: any): string => {
  if (error?.status === 401) {
    return 'Invalid email or password';
  }
  
  if (error?.status === 429) {
    return 'Too many requests. Please wait a moment and try again';
  }
  
  if (error?.status === 500) {
    return 'Server error. Please try again later';
  }
  
  if (error?.message?.includes('Network')) {
    return 'Network error. Please check your connection and try again';
  }
  
  return error?.message || 'An unexpected error occurred';
};

// Session Management
export const checkSession = (): boolean => {
  const tokens = getTokens();
  if (!tokens) {
    return false;
  }
  
  return !isTokenExpired(tokens.accessToken);
};

export const refreshSession = async (): Promise<boolean> => {
  const tokens = getTokens();
  if (!tokens) {
    return false;
  }
  
  try {
    // Call refresh token API
    const response = await fetch('/api/v1/auth/refresh', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ refreshToken: tokens.refreshToken }),
    });
    
    if (response.ok) {
      const data = await response.json();
      storeTokens(data.data);
      return true;
    }
  } catch (error) {
    console.error('Token refresh failed:', error);
  }
  
  return false;
};

// UI Helpers
export const formatUserName = (user: User): string => {
  if (user.firstName && user.lastName) {
    return `${user.firstName} ${user.lastName}`;
  }
  
  if (user.firstName) {
    return user.firstName;
  }
  
  return user.username;
};

export const getInitials = (user: User): string => {
  if (user.firstName && user.lastName) {
    return `${user.firstName[0]}${user.lastName[0]}`.toUpperCase();
  }
  
  if (user.firstName) {
    return user.firstName[0].toUpperCase();
  }
  
  return user.username[0].toUpperCase();
};

// Security Helpers
export const generateCSRFToken = (): string => {
  return Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
};

export const validateCSRFToken = (token: string, storedToken: string): boolean => {
  return token === storedToken;
};

// Remember Me Functionality
export const setRememberMe = (remember: boolean): void => {
  if (remember) {
    localStorage.setItem('rememberMe', 'true');
  } else {
    localStorage.removeItem('rememberMe');
  }
};

export const getRememberMe = (): boolean => {
  return localStorage.getItem('rememberMe') === 'true';
};

// Analytics Helpers
export const trackAuthEvent = (event: string, properties?: Record<string, any>): void => {
  // Track authentication events for analytics
  if (typeof window !== 'undefined' && (window as any).gtag) {
    (window as any).gtag('event', event, {
      event_category: 'authentication',
      ...properties
    });
  }
};

// Accessibility Helpers
export const announceToScreenReader = (message: string): void => {
  const announcement = document.createElement('div');
  announcement.setAttribute('aria-live', 'polite');
  announcement.setAttribute('aria-atomic', 'true');
  announcement.style.position = 'absolute';
  announcement.style.left = '-10000px';
  announcement.style.width = '1px';
  announcement.style.height = '1px';
  announcement.style.overflow = 'hidden';
  
  announcement.textContent = message;
  document.body.appendChild(announcement);
  
  setTimeout(() => {
    document.body.removeChild(announcement);
  }, 1000);
};

// Form State Helpers
export const createInitialFormState = (fields: string[]): Record<string, any> => {
  const state: Record<string, any> = {};
  
  fields.forEach(field => {
    state[field] = '';
  });
  
  return state;
};

export const updateFormState = (
  currentState: Record<string, any>,
  field: string,
  value: any
): Record<string, any> => {
  return {
    ...currentState,
    [field]: value
  };
};

// Loading State Helpers
export const createLoadingState = (isLoading: boolean = false): Record<string, boolean> => {
  return {
    isLoading,
    isSubmitting: false,
    isRefreshing: false
  };
};

// Success/Error State Helpers
export const createMessageState = (): Record<string, string | null> => {
  return {
    success: null,
    error: null
  };
};

// Constants
export const AUTH_CONSTANTS = {
  ACCESS_TOKEN_KEY: 'accessToken',
  REFRESH_TOKEN_KEY: 'refreshToken',
  USER_KEY: 'user',
  REMEMBER_ME_KEY: 'rememberMe',
  REDIRECT_KEY: 'redirect',
  SESSION_TIMEOUT: 15 * 60 * 1000, // 15 minutes
  REFRESH_TIMEOUT: 7 * 24 * 60 * 60 * 1000, // 7 days
  MAX_LOGIN_ATTEMPTS: 5,
  LOCKOUT_DURATION: 15 * 60 * 1000, // 15 minutes
  PASSWORD_MIN_LENGTH: 8,
  PASSWORD_MAX_LENGTH: 128,
  USERNAME_MIN_LENGTH: 3,
  USERNAME_MAX_LENGTH: 30,
  EMAIL_MAX_LENGTH: 254,
  NAME_MIN_LENGTH: 2,
  NAME_MAX_LENGTH: 50
};

// Rate Limiting Helpers
export const checkRateLimit = (action: string): boolean => {
  const now = Date.now();
  const key = `rateLimit_${action}`;
  const attempts = JSON.parse(localStorage.getItem(key) || '[]');
  
  // Remove old attempts (older than 15 minutes)
  const validAttempts = attempts.filter((timestamp: number) => 
    now - timestamp < 15 * 60 * 1000
  );
  
  if (validAttempts.length >= 5) {
    return false; // Rate limited
  }
  
  // Add current attempt
  validAttempts.push(now);
  localStorage.setItem(key, JSON.stringify(validAttempts));
  
  return true;
};

export const clearRateLimit = (action: string): void => {
  localStorage.removeItem(`rateLimit_${action}`);
};

// Password History (for change password)
export const addPasswordToHistory = (password: string): void => {
  const history = JSON.parse(localStorage.getItem('passwordHistory') || '[]');
  history.push(password);
  
  // Keep only last 5 passwords
  if (history.length > 5) {
    history.shift();
  }
  
  localStorage.setItem('passwordHistory', JSON.stringify(history));
};

export const isPasswordInHistory = (password: string): boolean => {
  const history = JSON.parse(localStorage.getItem('passwordHistory') || '[]');
  return history.includes(password);
};

// Device Fingerprinting (for security)
export const generateDeviceFingerprint = (): string => {
  const canvas = document.createElement('canvas');
  const ctx = canvas.getContext('2d');
  ctx?.fillText('Device Fingerprint', 10, 10);
  
  const fingerprint = [
    navigator.userAgent,
    navigator.language,
    screen.width,
    screen.height,
    new Date().getTimezoneOffset(),
    canvas.toDataURL()
  ].join('|');
  
  return btoa(fingerprint);
};

// Session Activity Tracking
export const updateSessionActivity = (): void => {
  localStorage.setItem('lastActivity', Date.now().toString());
};

export const getLastActivity = (): number => {
  return parseInt(localStorage.getItem('lastActivity') || '0');
};

export const isSessionActive = (): boolean => {
  const lastActivity = getLastActivity();
  const now = Date.now();
  const timeout = 30 * 60 * 1000; // 30 minutes
  
  return (now - lastActivity) < timeout;
}; 