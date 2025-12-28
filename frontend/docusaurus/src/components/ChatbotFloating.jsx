import React, { useState, useEffect } from 'react';
import useAuth  from '../hooks/useAuth';

const ChatbotFloating = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [showWidget, setShowWidget] = useState(false);
  const { isAuthenticated } = useAuth();

  // Show widget after component mounts to ensure it's properly positioned
  useEffect(() => {
    setShowWidget(true);
  }, []);

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  const closeChat = () => {
    setIsOpen(false);
  };

  if (!showWidget) {
    return null;
  }

  return (
    <>
      {isOpen && (
        <div className="chatbot-floating-overlay" onClick={closeChat}>
          <div className="chatbot-floating-container" onClick={(e) => e.stopPropagation()}>
            <div className="chatbot-floating-header">
              <h4>AI Assistant</h4>
              <button className="chatbot-floating-close" onClick={closeChat}>
                ×
              </button>
            </div>
            <div className="chatbot-floating-content">
              {!isAuthenticated ? (
                <div className="chatbot-floating-login-prompt">
                  <p>Please sign in to use the chatbot.</p>
                  <div className="chatbot-floating-auth-buttons">
                    <a href="/login" className="chatbot-login-btn">Sign In</a>
                    <a href="/register" className="chatbot-register-btn">Sign Up</a>
                  </div>
                </div>
              ) : (
                <div className="chatbot-floating-chat">
                  <div className="chatbot-floating-messages">
                    <div className="chatbot-msg chatbot-msg-assistant">
                      <div className="chatbot-avatar">🤖</div>
                      <div className="chatbot-bubble">
                        <p>Hello! I'm your AI assistant. How can I help you with the textbook content today?</p>
                      </div>
                    </div>
                    <div className="chatbot-msg chatbot-msg-user">
                      <div className="chatbot-avatar">👤</div>
                      <div className="chatbot-bubble">
                        <p>Can you explain the concept of humanoid robotics?</p>
                      </div>
                    </div>
                    <div className="chatbot-msg chatbot-msg-assistant">
                      <div className="chatbot-avatar">🤖</div>
                      <div className="chatbot-bubble">
                        <p>Certainly! Humanoid robotics involves creating robots that resemble and mimic human behavior and appearance...</p>
                      </div>
                    </div>
                  </div>
                  <div className="chatbot-floating-input">
                    <input
                      type="text"
                      placeholder="Type your question..."
                      disabled
                    />
                    <button disabled>Send</button>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      <button
        className={`chatbot-floating-btn ${isOpen ? 'chatbot-floating-btn-open' : ''}`}
        onClick={toggleChat}
        aria-label={isOpen ? "Close chat" : "Open chat"}
      >
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M21 15C21 15.5304 20.7893 16.0391 20.4142 16.4142C20.0391 16.7893 19.5304 17 19 17H16.41L16.41 17.03C16.2 17.66 15.97 18.29 15.72 18.91L15.46 19.54C15.38 19.73 15.27 19.91 15.13 20.07C14.99 20.23 14.82 20.37 14.64 20.48C14.46 20.59 14.26 20.67 14.05 20.72C13.84 20.77 13.62 20.79 13.4 20.78L13.4 20.78C13.16 20.77 12.93 20.72 12.7 20.64L12.7 20.64C12.47 20.56 12.25 20.45 12.04 20.3L11.4 19.87C10.77 19.62 10.14 19.39 9.51 19.18L9.51 19.18L9.09 19H9C8.46957 19 7.96086 18.7893 7.58579 18.4142C7.21071 18.0391 7 17.5304 7 17V15" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          <path d="M7 7C7 7.53043 7.21071 8.03914 7.58579 8.41421C7.96086 8.78929 8.46957 9 9 9H15C15.5304 9 16.0391 8.78929 16.4142 8.41421C16.7893 8.03914 17 7.53043 17 7C17 6.46957 16.7893 5.96086 16.4142 5.58579C16.0391 5.21071 15.5304 5 15 5H9C8.46957 5 7.96086 5.21071 7.58579 5.58579C7.21071 5.96086 7 6.46957 7 7Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          <path d="M7 11H11" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          <path d="M13 11H15" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
        </svg>
      </button>
    </>
  );
};

export default ChatbotFloating;