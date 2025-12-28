import React, { useState } from "react";
import { useHistory, Link } from "react-router-dom"; // <-- useHistory
import useAuth from "../../hooks/useAuth";
import "./Auth.css";

const ForgotPassword = () => {
  const [email, setEmail] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [errors, setErrors] = useState({});
  const [serverError, setServerError] = useState("");

  const history = useHistory(); // <-- replace useNavigate

  const { forgotPassword, clearError } = useAuth() || {};

  const validateEmail = () => {
    const newErrors = {};
    if (!email) {
      newErrors.email = "Email is required";
    } else if (!/\S+@\S+\.\S+/.test(email)) {
      newErrors.email = "Email is invalid";
    }
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!validateEmail()) return;

    if (!forgotPassword) {
      setServerError(
        "Authentication is not initialized. Make sure AuthProvider is wrapping your app."
      );
      return;
    }

    setIsLoading(true);
    clearError?.();
    setServerError("");
    setMessage("");

    try {
      await forgotPassword(email);
      setMessage(
        "If an account exists with this email, a password reset link has been sent."
      );
      setEmail("");

      // Example: redirect to login after successful submission
      history.push("/login"); // <-- useHistory replacement
    } catch (error) {
      console.error("Forgot password error:", error);
      setServerError(error?.message || "Something went wrong. Try again.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-form">
        <h2>Forgot Password</h2>

        {message && <div className="success-message">{message}</div>}
        {serverError && <div className="error-text">{serverError}</div>}

        <p className="form-description">
          Enter your email address and we'll send you a link to reset your password.
        </p>

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="email">Email Address</label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => {
                setEmail(e.target.value);
                if (errors.email) setErrors({ ...errors, email: "" });
              }}
              className={errors.email ? "error" : ""}
              placeholder="Enter your email"
              disabled={isLoading}
            />
            {errors.email && <div className="error-text">{errors.email}</div>}
          </div>

          <button type="submit" className="auth-button" disabled={isLoading}>
            {isLoading ? "Sending..." : "Send Reset Link"}
          </button>
        </form>

        <div className="auth-footer">
          <p>
            Remember your password? <Link to="/login">Sign in</Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default ForgotPassword;
