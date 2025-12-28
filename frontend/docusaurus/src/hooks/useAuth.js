import { useContext } from 'react';
import { AuthContext } from '../context/AuthContext';

// Custom hook to access auth context with additional utility functions
const useAuth = () => {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }

  // Check if user is authenticated
  const isAuthenticated = context.isAuthenticated && !!context.token;

  // Check if user has a specific role (if roles are implemented)
  const hasRole = (role) => {
    if (!context.user || !context.user.roles) return false;
    return context.user.roles.includes(role);
  };

  // Check if user has specific permissions (if permissions are implemented)
  const hasPermission = (permission) => {
    if (!context.user || !context.user.permissions) return false;
    return context.user.permissions.includes(permission);
  };

  // Get user's display name
  const getDisplayName = () => {
    if (!context.user) return '';
    return context.user.name || context.user.email || '';
  };

  // Check if auth is still loading
  const isLoadingAuth = context.isLoading;

  return {
    ...context,
    isAuthenticated,
    hasRole,
    hasPermission,
    getDisplayName,
    isLoadingAuth,
  };
};

export default useAuth;