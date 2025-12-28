import axios from 'axios';

// Base API URL - you can change this based on your environment
const API_BASE_URL = 'http://localhost:8000/v1/auth';

// Create an axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
});

// Auth service object
export const authService = {
  // Login user
  async login(email, password, rememberMe = false) {
    try {
      const response = await api.post('/login', {
        email,
        password,
        remember_me: rememberMe
      });
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // Register user
  async register(name, email, password) {
    try {
      const response = await api.post('/register', {
        name,
        email,
        password
      });
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // Logout user
  async logout() {
    try {
      // Get the access token to include in the request
      const accessToken = this.getAccessToken();
      if (accessToken) {
        // Include the access token in the request
        await api.post('/logout', {}, {
          headers: {
            'Authorization': `Bearer ${accessToken}`
          }
        });
      }
    } catch (error) {
      // Even if the logout request fails, we should still clear the local tokens
      console.error('Logout API call failed:', error);
    } finally {
      // Always clear the tokens locally
      this.clearTokens();
    }
  },

  // Refresh access token
  async refreshToken(refreshToken) {
    try {
      const response = await api.post('/refresh', {
        refresh_token: refreshToken
      });
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // Get current user info
  async getCurrentUser() {
    try {
      const accessToken = this.getAccessToken();
      if (!accessToken) {
        throw new Error('No access token available');
      }

      const response = await api.get('/me', {
        headers: {
          'Authorization': `Bearer ${accessToken}`
        }
      });
      return response.data.user;
    } catch (error) {
      throw error;
    }
  },

  // Forgot password
  async forgotPassword(email) {
    try {
      const response = await api.post('/forgot-password', {
        email
      });
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // Reset password
  async resetPassword(token, newPassword) {
    try {
      const response = await api.post('/reset-password', {
        token,
        new_password: newPassword
      });
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // OAuth login
  async oauthLogin(provider, code, redirectUri) {
    try {
      const response = await api.post('/oauth/callback', {
        provider,
        code,
        redirect_uri: redirectUri
      });
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // Verify email
  async verifyEmail(token) {
    try {
      const response = await api.post('/verify-email', {
        token
      });
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // Change password
  async changePassword(currentPassword, newPassword) {
    try {
      const accessToken = this.getAccessToken();
      if (!accessToken) {
        throw new Error('No access token available');
      }

      const response = await api.post('/change-password', {
        current_password: currentPassword,
        new_password: newPassword
      }, {
        headers: {
          'Authorization': `Bearer ${accessToken}`
        }
      });
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // Set tokens in localStorage or sessionStorage based on rememberMe setting
  setTokens(accessToken, refreshToken, rememberMe = false) {
    if (rememberMe) {
      // Store in localStorage to persist after browser closes
      if (accessToken) localStorage.setItem('access_token', accessToken);
      if (refreshToken) localStorage.setItem('refresh_token', refreshToken);
    } else {
      // Store in sessionStorage to clear when browser tab closes
      if (accessToken) sessionStorage.setItem('access_token', accessToken);
      if (refreshToken) sessionStorage.setItem('refresh_token', refreshToken);
    }
  },

  // Get access token from storage
  getAccessToken() {
    // Check both localStorage and sessionStorage
    return localStorage.getItem('access_token') || sessionStorage.getItem('access_token');
  },

  // Get refresh token from storage
  getRefreshToken() {
    // Check both localStorage and sessionStorage
    return localStorage.getItem('refresh_token') || sessionStorage.getItem('refresh_token');
  },

  // Get both tokens
  getTokens() {
    const accessToken = this.getAccessToken();
    const refreshToken = this.getRefreshToken();

    if (accessToken) {
      return { accessToken, refreshToken };
    }
    return null;
  },

  // Clear tokens from storage
  clearTokens() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    sessionStorage.removeItem('access_token');
    sessionStorage.removeItem('refresh_token');
  },

  // Set up axios interceptors for automatic token inclusion
  setupAxiosInterceptors() {
    // Request interceptor to add token to requests
    api.interceptors.request.use(
      (config) => {
        const token = this.getAccessToken();
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // Response interceptor to handle token expiration
    api.interceptors.response.use(
      (response) => {
        return response;
      },
      async (error) => {
        const originalRequest = error.config;

        // If the error is due to token expiration and we haven't retried yet
        if (error.response?.status === 401 && !originalRequest._retry) {
          originalRequest._retry = true;

          try {
            const refreshToken = this.getRefreshToken();
            if (!refreshToken) {
              throw new Error('No refresh token available');
            }

            const response = await this.refreshToken(refreshToken);
            const newAccessToken = response.access_token;

            // Update the token in storage
            const rememberMe = localStorage.getItem('access_token') !== null;
            this.setTokens(newAccessToken, null, rememberMe); // Don't update refresh token unless provided

            // Update the original request with the new token
            originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;

            // Retry the original request
            return api(originalRequest);
          } catch (refreshError) {
            // If refresh fails, clear tokens and redirect to login
            this.clearTokens();
            window.location.href = '/login';
            return Promise.reject(refreshError);
          }
        }

        return Promise.reject(error);
      }
    );
  }
};

// Initialize axios interceptors when the service is imported
authService.setupAxiosInterceptors();

export default authService;