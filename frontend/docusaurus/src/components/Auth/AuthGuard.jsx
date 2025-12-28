import React from 'react';
import { Redirect, useLocation } from 'react-router-dom';
import useAuth from "../../hooks/useAuth";

const AuthGuard = ({ children, requireAuth = true, redirectPath = '/login' }) => {
  const { isAuthenticated, isLoadingAuth } = useAuth();
  const location = useLocation();

  // If auth is still loading, show a loading indicator
  if (isLoadingAuth) {
    return (
      <div className="auth-loading">
        <div className="spinner"></div>
        <p>Loading...</p>
      </div>
    );
  }

  // If authentication is required but user is not authenticated
  if (requireAuth && !isAuthenticated) {
    // Redirect to login page and save the original location
    return (
      <Redirect
        to={{
          pathname: redirectPath,
          state: { from: location },
        }}
      />
    );
  }

  // If authentication is NOT required but user IS authenticated (e.g., login/register pages)
  if (!requireAuth && isAuthenticated) {
    // Redirect to home page
    return <Redirect to="/" />;
  }

  // If all checks pass, render the children
  return children;
};

export default AuthGuard;
