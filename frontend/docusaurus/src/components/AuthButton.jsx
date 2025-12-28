import React from 'react';
import { useAuth } from '../hooks/useAuth';
import Link from '@docusaurus/Link';

const AuthButton = () => {
  const { isAuthenticated, user, logout, isLoadingAuth } = useAuth();

  if (isLoadingAuth) {
    return (
      <div className="navbar__item navbar__link">
        <span>Loading...</span>
      </div>
    );
  }

  if (isAuthenticated) {
    return (
      <div className="navbar__item dropdown dropdown--right dropdown--username">
        <span className="navbar__link dropdown__link">
          {user?.name || user?.email || 'User'} ▼
        </span>
        <ul className="dropdown__menu">
          <li>
            <Link className="dropdown__link" to="/profile">
              Profile
            </Link>
          </li>
          <li>
            <button
              className="dropdown__link dropdown__logout-btn"
              onClick={logout}
              style={{
                background: 'none',
                border: 'none',
                padding: '0.5rem 1rem',
                cursor: 'pointer',
                textAlign: 'left',
                width: '100%'
              }}
            >
              Logout
            </button>
          </li>
        </ul>
      </div>
    );
  }

  return (
    <div className="navbar__item auth-buttons">
      <Link
        className="button button--secondary button--sm navbar__link auth-button auth-button--login"
        to="/login"
      >
        Sign In
      </Link>
      <Link
        className="button button--primary button--sm navbar__link auth-button auth-button--signup"
        to="/register"
      >
        Sign Up
      </Link>
    </div>
  );
};

export default AuthButton;