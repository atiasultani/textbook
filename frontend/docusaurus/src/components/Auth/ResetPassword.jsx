import React, { useState } from 'react';
import { useHistory } from 'react-router-dom'; // <-- useHistory instead of useNavigate
import useAuth from "../../hooks/useAuth";
import './Auth.css';

const ResetPassword = () => {
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [errors, setErrors] = useState({});

  const { resetPassword, clearError } = useAuth();
  const history = useHistory(); // <-- replace useNavigate

  // Extract token from URL manually
  const queryParams = new URLSearchParams(window.location.search);
  const token = queryParams.get('token');

  const validateForm = () => {
    const newErrors = {};

    if (!password) {
      newErrors.password = 'Password is required';
    } else if (password.length < 8) {
      newErrors.password = 'Password must be at least 8 characters';
    } else if (!/(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/.test(password)) {
      newErrors.password = 'Password must contain at least one uppercase, one lowercase, and one number';
    }

    if (!confirmPassword) {
      newErrors.confirmPassword = 'Please confirm your password';
    } else if (password !== confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!validateForm() || !token) return;

    setIsLoading(true);
    clearError?.();

    try {
      await resetPassword(token, password);
      setMessage('Your password has been reset successfully. You can now sign in.');
      setPassword('');
      setConfirmPassword('');

      // Redirect to login page after reset
      history.push('/login'); // <-- v5 navigation
    } catch (error) {
      console.error('Reset password error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-form">
        <h2>Reset Password</h2>

        {message ? (
          <div className="success-message">{message}</div>
        ) : (
          <>
            <p className="form-description">
              Enter your new password below.
            </p>

            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label htmlFor="password">New Password</label>
                <input
                  type="password"
                  id="password"
                  value={password}
                  onChange={(e) => {
                    setPassword(e.target.value);
                    if (errors.password) setErrors({ ...errors, password: '' });
                  }}
                  className={errors.password ? 'error' : ''}
                  placeholder="Enter new password"
                  disabled={isLoading}
                />
                {errors.password && <div className="error-text">{errors.password}</div>}
              </div>

              <div className="form-group">
                <label htmlFor="confirmPassword">Confirm New Password</label>
                <input
                  type="password"
                  id="confirmPassword"
                  value={confirmPassword}
                  onChange={(e) => {
                    setConfirmPassword(e.target.value);
                    if (errors.confirmPassword) setErrors({ ...errors, confirmPassword: '' });
                  }}
                  className={errors.confirmPassword ? 'error' : ''}
                  placeholder="Confirm new password"
                  disabled={isLoading}
                />
                {errors.confirmPassword && <div className="error-text">{errors.confirmPassword}</div>}
              </div>

              <button type="submit" className="auth-button" disabled={isLoading}>
                {isLoading ? 'Resetting...' : 'Reset Password'}
              </button>
            </form>
          </>
        )}

        <div className="auth-footer">
          <p>
            <a href="/login">Back to Sign In</a>
          </p>
        </div>
      </div>
    </div>
  );
};

export default ResetPassword;
