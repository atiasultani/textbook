import React from 'react';
import { useAuth } from '../../hooks/useAuth';
import { Link } from 'react-router-dom';

const NavbarAuth = () => {
  const { isAuthenticated, user, logout, getDisplayName } = useAuth();

  const handleLogout = async () => {
    try {
      await logout();
    } catch (error) {
      console.error('Logout error:', error);
    }
  };

  if (isAuthenticated) {
    return (
      <div className="navbar-auth">
        <span className="user-display">Hello, {getDisplayName()}!</span>
        <Link to="/chat" className="nav-link">Chatbot</Link>
        <button onClick={handleLogout} className="logout-button">
          Logout
        </button>
      </div>
    );
  } else {
    return (
      <div className="navbar-auth">
        <Link to="/register" className="nav-link register-link">Sign Up</Link>
        <Link to="/login" className="nav-link login-link">Sign In</Link>
      </div>
    );
  }
};

export default NavbarAuth;