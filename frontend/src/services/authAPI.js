const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:3001/api/v1';

class AuthAPI {
  constructor() {
    this.baseURL = API_BASE_URL;
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
        // Handle token refresh if 401
        if (response.status === 401 && endpoint !== '/auth/refresh') {
          const refreshResult = await this.refreshToken();
          if (refreshResult.success) {
            config.headers.Authorization = `Bearer ${localStorage.getItem('accessToken')}`;
            const retryResponse = await fetch(url, config);
            const retryData = await retryResponse.json();
            if (!retryResponse.ok) {
              throw { status: retryResponse.status, ...retryData };
            }
            return retryData;
          } else {
            localStorage.removeItem('accessToken');
            localStorage.removeItem('refreshToken');
            window.location.href = '/authentication/sign-in';
            throw { status: 401, message: 'Session expired. Please login again.' };
          }
        }
        // Throw toàn bộ object lỗi backend
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

  // Login user
  async login(credentials) {
    const response = await this.makeRequest('/auth/login', {
      method: 'POST',
      body: JSON.stringify(credentials),
    });

    if (response.success && response.data) {
      return {
        user: response.data.user,
        accessToken: response.data.accessToken,
        refreshToken: response.data.refreshToken,
      };
    }
    
    throw new Error('Login failed');
  }

  // Register user
  async register(userData) {
    try {
      const response = await this.makeRequest('/auth/register', {
        method: 'POST',
        body: JSON.stringify(userData),
      });
      return response;
    } catch (error) {
      // Just throw the error without console logging
      throw error;
    }
  }

  // Logout user
  async logout() {
    try {
      await this.makeRequest('/auth/logout', {
        method: 'POST',
      });
    } catch (error) {
      // Even if logout API fails, we still want to clear local storage
      console.error('Logout API error:', error);
    }
  }

  // Get current user
  async getCurrentUser() {
    const response = await this.makeRequest('/auth/me');
    
    if (response.success && response.data) {
      return response.data.user;
    }
    
    throw new Error('Failed to get user data');
  }

  // Refresh token
  async refreshToken() {
    const refreshToken = localStorage.getItem('refreshToken');
    if (!refreshToken) {
      return { success: false };
    }

    try {
      const response = await this.makeRequest('/auth/refresh', {
        method: 'POST',
        body: JSON.stringify({ refreshToken }),
      });

      if (response.success && response.data) {
        localStorage.setItem('accessToken', response.data.accessToken);
        localStorage.setItem('refreshToken', response.data.refreshToken);
        return { success: true };
      }
    } catch (error) {
      console.error('Token refresh failed:', error);
    }

    return { success: false };
  }

  // Forgot password
  async forgotPassword(email) {
    const response = await this.makeRequest('/auth/forgot-password', {
      method: 'POST',
      body: JSON.stringify({ email }),
    });

    if (response.success) {
      return { success: true, message: response.message };
    }
    
    throw new Error('Failed to send reset email');
  }

  // Reset password
  async resetPassword(token, password) {
    const response = await this.makeRequest('/auth/reset-password', {
      method: 'POST',
      body: JSON.stringify({ token, password }),
    });

    if (response.success) {
      return { success: true, message: response.message };
    }
    
    throw new Error('Failed to reset password');
  }

  // Update user profile
  async updateProfile(profileData) {
    const response = await this.makeRequest('/users/profile', {
      method: 'PUT',
      body: JSON.stringify(profileData),
    });

    if (response.success && response.data) {
      return response.data.user;
    }
    
    throw new Error('Failed to update profile');
  }

  // Change password
  async changePassword(passwordData) {
    const response = await this.makeRequest('/users/change-password', {
      method: 'PUT',
      body: JSON.stringify(passwordData),
    });

    if (response.success) {
      return { success: true, message: response.message };
    }
    
    throw new Error('Failed to change password');
  }
}

export const authAPI = new AuthAPI(); 