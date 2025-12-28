import React, { createContext, useContext, useReducer, useEffect } from 'react';
import { authService } from '../services/authService';

// Create Auth Context
export const AuthContext = createContext();

// Initial state for the auth context
const initialState = {
  user: null,
  token: null,
  refreshToken: null,
  isAuthenticated: false,
  isLoading: true,
  error: null,
};

// Auth reducer to handle state changes
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
        token: action.payload.access_token,
        refreshToken: action.payload.refresh_token,
        isAuthenticated: true,
        isLoading: false,
        error: null,
      };
    case 'LOGIN_FAILURE':
      return {
        ...state,
        isAuthenticated: false,
        isLoading: false,
        error: action.payload.error,
      };
    case 'LOGOUT':
      return {
        ...state,
        user: null,
        token: null,
        refreshToken: null,
        isAuthenticated: false,
        isLoading: false,
        error: null,
      };
    case 'SET_USER':
      return {
        ...state,
        user: action.payload.user,
        isAuthenticated: true,
        isLoading: false,
      };
    case 'UPDATE_TOKENS':
      return {
        ...state,
        token: action.payload.accessToken,
        refreshToken: action.payload.refreshToken,
      };
    case 'SET_ERROR':
      return {
        ...state,
        error: action.payload.error,
      };
    case 'CLEAR_ERROR':
      return {
        ...state,
        error: null,
      };
    default:
      return state;
  }
};

// AuthProvider component
export const AuthProvider = ({ children }) => {
  const [state, dispatch] = useReducer(authReducer, initialState);

  // Check for existing tokens on initial load
  useEffect(() => {
    const checkAuthStatus = async () => {
      try {
        const tokens = authService.getTokens();
        if (tokens && tokens.accessToken) {
          // Verify the token is still valid
          const user = await authService.getCurrentUser();
          if (user) {
            dispatch({
              type: 'SET_USER',
              payload: { user },
            });
          } else {
            // Token is invalid, clear it
            authService.clearTokens();
            dispatch({ type: 'LOGOUT' });
          }
        } else {
          dispatch({ type: 'LOGOUT' });
        }
      } catch (error) {
        console.error('Error checking auth status:', error);
        authService.clearTokens();
        dispatch({ type: 'LOGOUT' });
      }
    };

    checkAuthStatus();
  }, []);

  // Login function
  const login = async (email, password, rememberMe = false) => {
    dispatch({ type: 'LOGIN_START' });
    try {
      const response = await authService.login(email, password, rememberMe);
      authService.setTokens(response.access_token, response.refresh_token, rememberMe);
      dispatch({
        type: 'LOGIN_SUCCESS',
        payload: response,
      });
      return { success: true };
    } catch (error) {
      const errorMessage = error.response?.data?.detail || error.message || 'Login failed';
      dispatch({
        type: 'LOGIN_FAILURE',
        payload: { error: errorMessage },
      });
      return { success: false, error: errorMessage };
    }
  };

  // Logout function
  const logout = async () => {
    try {
      await authService.logout();
    } catch (error) {
      console.error('Error during logout:', error);
    } finally {
      authService.clearTokens();
      dispatch({ type: 'LOGOUT' });
    }
  };

  // Register function
  const register = async (name, email, password) => {
    dispatch({ type: 'LOGIN_START' });
    try {
      const response = await authService.register(name, email, password);
      authService.setTokens(response.access_token, response.refresh_token, false);
      dispatch({
        type: 'LOGIN_SUCCESS',
        payload: response,
      });
      return { success: true };
    } catch (error) {
      const errorMessage = error.response?.data?.detail || error.message || 'Registration failed';
      dispatch({
        type: 'LOGIN_FAILURE',
        payload: { error: errorMessage },
      });
      return { success: false, error: errorMessage };
    }
  };

  // Handle OAuth login
  const oauthLogin = async (provider, code, redirectUri) => {
    dispatch({ type: 'LOGIN_START' });
    try {
      const response = await authService.oauthLogin(provider, code, redirectUri);
      authService.setTokens(response.access_token, response.refresh_token, false);
      dispatch({
        type: 'LOGIN_SUCCESS',
        payload: response,
      });
      return { success: true, isNewUser: response.is_new_user };
    } catch (error) {
      const errorMessage = error.response?.data?.detail || error.message || 'OAuth login failed';
      dispatch({
        type: 'LOGIN_FAILURE',
        payload: { error: errorMessage },
      });
      return { success: false, error: errorMessage };
    }
  };

  // Refresh token
  const refreshToken = async () => {
    try {
      const refreshToken = authService.getRefreshToken();
      if (!refreshToken) {
        throw new Error('No refresh token available');
      }

      const response = await authService.refreshToken(refreshToken);
      authService.setTokens(response.access_token, null, true); // Don't update refresh token unless provided
      dispatch({
        type: 'UPDATE_TOKENS',
        payload: {
          accessToken: response.access_token,
          refreshToken: response.refresh_token || authService.getRefreshToken(),
        },
      });
      return response.access_token;
    } catch (error) {
      console.error('Error refreshing token:', error);
      authService.clearTokens();
      dispatch({ type: 'LOGOUT' });
      throw error;
    }
  };

  // Request with automatic token refresh
  const authenticatedRequest = async (requestFn) => {
    try {
      return await requestFn();
    } catch (error) {
      if (error.response?.status === 401) {
        // Try to refresh the token
        try {
          await refreshToken();
          // Retry the original request
          return await requestFn();
        } catch (refreshError) {
          // If refresh fails, logout
          logout();
          throw refreshError;
        }
      }
      throw error;
    }
  };

  // Forgot password
  const forgotPassword = async (email) => {
    try {
      return await authService.forgotPassword(email);
    } catch (error) {
      const errorMessage = error.response?.data?.detail || error.message || 'Failed to send reset email';
      dispatch({
        type: 'SET_ERROR',
        payload: { error: errorMessage },
      });
      throw error;
    }
  };

  // Reset password
  const resetPassword = async (token, newPassword) => {
    try {
      return await authService.resetPassword(token, newPassword);
    } catch (error) {
      const errorMessage = error.response?.data?.detail || error.message || 'Failed to reset password';
      dispatch({
        type: 'SET_ERROR',
        payload: { error: errorMessage },
      });
      throw error;
    }
  };

  // Clear error
  const clearError = () => {
    dispatch({ type: 'CLEAR_ERROR' });
  };

  const value = {
    ...state,
    login,
    logout,
    register,
    oauthLogin,
    refreshToken,
    authenticatedRequest,
    forgotPassword,
    resetPassword,
    clearError,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

// Custom hook to use the auth context
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};