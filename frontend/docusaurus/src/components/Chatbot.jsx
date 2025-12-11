import React, { useState, useEffect, useRef } from 'react';
import { useLocation } from '@docusaurus/router';

const Chatbot = () => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [sessionId, setSessionId] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [selectedText, setSelectedText] = useState('');
  const [showLogin, setShowLogin] = useState(false);
  const [authToken, setAuthToken] = useState('');
  const messagesEndRef = useRef(null);
  const location = useLocation();

  // Check for stored auth token on component mount
  useEffect(() => {
    const storedToken = localStorage.getItem('authToken');
    if (storedToken) {
      setAuthToken(storedToken);
    } else {
      setShowLogin(true);
    }
  }, []);

  // Initialize chat session when component mounts
  useEffect(() => {
    if (authToken) {
      const initSession = async () => {
        try {
          const response = await fetch('/api/v1/chat/start', {
            method: 'POST',
            headers: {
              'Authorization': `Bearer ${authToken}`,
              'Content-Type': 'application/json',
            },
          });

          if (response.ok) {
            const data = await response.json();
            setSessionId(data.id);
          } else {
            if (response.status === 401) {
              setShowLogin(true);
              localStorage.removeItem('authToken');
            }
          }
        } catch (error) {
          console.error('Error initializing chat session:', error);
        }
      };

      initSession();
    }
  }, [authToken]);

  // Scroll to bottom of messages
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  const handleLogin = async (username, password) => {
    try {
      const response = await fetch('/token', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
          username: username,
          password: password,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        const token = data.access_token;
        setAuthToken(token);
        localStorage.setItem('authToken', token);
        setShowLogin(false);

        // Initialize session after login
        const sessionResponse = await fetch('/api/v1/chat/start', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        });

        if (sessionResponse.ok) {
          const sessionData = await sessionResponse.json();
          setSessionId(sessionData.id);
        }
      } else {
        alert('Login failed. Please check your credentials.');
      }
    } catch (error) {
      console.error('Login error:', error);
      alert('Login failed. Please try again.');
    }
  };

  const sendMessage = async () => {
    if (!inputValue.trim() || !sessionId || isLoading || !authToken) return;

    const userMessage = { role: 'user', content: inputValue, timestamp: new Date() };
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      const response = await fetch(`/api/v1/chat/${sessionId}/query`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${authToken}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: inputValue,
          selected_text: selectedText || null, // Include selected text if available
          context: [] // For simplicity, not sending context
        }),
      });

      if (response.ok) {
        const data = await response.json();

        const botMessage = {
          role: 'assistant',
          content: data.response,
          sources: data.sources,
          confidence: data.confidence_score,
          is_hallucinated: data.is_hallucinated,
          timestamp: new Date()
        };

        setMessages(prev => [...prev, botMessage]);
        // Clear selected text after using it
        setSelectedText('');
      } else {
        if (response.status === 401) {
          setShowLogin(true);
          localStorage.removeItem('authToken');
        } else {
          const errorData = await response.json();
          const errorMessage = {
            role: 'assistant',
            content: `Error: ${errorData.detail || 'Failed to get response'}`,
            timestamp: new Date()
          };
          setMessages(prev => [...prev, errorMessage]);
        }
      }
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        role: 'assistant',
        content: 'Sorry, I encountered an error processing your request. Please try again.',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  // Function to capture selected text
  useEffect(() => {
    const handleSelection = () => {
      const selectedText = window.getSelection().toString().trim();
      if (selectedText) {
        setSelectedText(selectedText);
      }
    };

    document.addEventListener('mouseup', handleSelection);
    return () => {
      document.removeEventListener('mouseup', handleSelection);
    };
  }, []);

  if (showLogin) {
    return (
      <div className="chatbot-container" style={{
        border: '1px solid #ddd',
        borderRadius: '8px',
        padding: '16px',
        marginTop: '16px',
        backgroundColor: '#f9f9f9'
      }}>
        <div className="chatbot-login" style={{
          textAlign: 'center',
          padding: '20px'
        }}>
          <h3>Chatbot Access</h3>
          <p>Please log in to use the chatbot:</p>
          <LoginForm onLogin={handleLogin} />
        </div>
      </div>
    );
  }

  return (
    <div className="chatbot-container" style={{
      border: '1px solid #ddd',
      borderRadius: '8px',
      padding: '16px',
      marginTop: '16px',
      backgroundColor: '#f9f9f9'
    }}>
      <div className="chatbot-header" style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: '12px'
      }}>
        <h3>Textbook Assistant</h3>
        {selectedText && (
          <div className="selected-text-preview" style={{
            fontSize: '0.8em',
            fontStyle: 'italic',
            padding: '4px 8px',
            backgroundColor: '#e3f2fd',
            borderRadius: '4px'
          }}>
            Selected: "{selectedText.substring(0, 50)}{selectedText.length > 50 ? '...' : ''}"
          </div>
        )}
      </div>

      <div className="chat-messages" style={{
        maxHeight: '300px',
        overflowY: 'auto',
        marginBottom: '16px',
        padding: '8px',
        backgroundColor: 'white',
        borderRadius: '4px'
      }}>
        {messages.map((msg, index) => (
          <div key={index} style={{
            textAlign: msg.role === 'user' ? 'right' : 'left',
            marginBottom: '8px'
          }}>
            <div style={{
              display: 'inline-block',
              padding: '8px 12px',
              borderRadius: '8px',
              backgroundColor: msg.role === 'user' ? '#007cba' : '#e9ecef',
              color: msg.role === 'user' ? 'white' : 'black',
              maxWidth: '80%'
            }}>
              {msg.content}
              {msg.sources && msg.sources.length > 0 && (
                <div style={{ marginTop: '4px', fontSize: '0.8em' }}>
                  <strong>Sources:</strong>
                  <ul style={{ margin: '4px 0', padding: '0 0 0 16px' }}>
                    {msg.sources.map((source, idx) => (
                      <li key={idx}>{source.chapter_title}</li>
                    ))}
                  </ul>
                </div>
              )}
              {msg.confidence !== undefined && (
                <div style={{ marginTop: '4px', fontSize: '0.8em', fontStyle: 'italic' }}>
                  Confidence: {(msg.confidence * 100).toFixed(1)}%
                  {msg.is_hallucinated && <span style={{ color: 'red' }}> (Potential hallucination)</span>}
                </div>
              )}
            </div>
          </div>
        ))}
        {isLoading && (
          <div style={{ textAlign: 'left' }}>
            <div style={{
              display: 'inline-block',
              padding: '8px 12px',
              borderRadius: '8px',
              backgroundColor: '#e9ecef',
              color: 'black'
            }}>
              Thinking...
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      <div className="chat-input" style={{
        display: 'flex',
        gap: '8px'
      }}>
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Ask a question about the textbook..."
          style={{
            flex: 1,
            padding: '8px',
            border: '1px solid #ddd',
            borderRadius: '4px'
          }}
          disabled={isLoading || !sessionId || !authToken}
        />
        <button
          onClick={sendMessage}
          disabled={isLoading || !sessionId || !inputValue.trim() || !authToken}
          style={{
            padding: '8px 16px',
            backgroundColor: '#007cba',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: (isLoading || !sessionId || !inputValue.trim() || !authToken) ? 'not-allowed' : 'pointer'
          }}
        >
          Send
        </button>
      </div>
    </div>
  );
};

const LoginForm = ({ onLogin }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onLogin(username, password);
  };

  return (
    <form onSubmit={handleSubmit} className="login-form" style={{
      display: 'flex',
      flexDirection: 'column',
      gap: '12px',
      maxWidth: '300px',
      margin: '0 auto'
    }}>
      <div className="form-group" style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'flex-start'
      }}>
        <label htmlFor="username" style={{ marginBottom: '4px' }}>Username:</label>
        <input
          type="text"
          id="username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
          style={{
            padding: '8px',
            border: '1px solid #ddd',
            borderRadius: '4px',
            width: '100%'
          }}
        />
      </div>
      <div className="form-group" style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'flex-start'
      }}>
        <label htmlFor="password" style={{ marginBottom: '4px' }}>Password:</label>
        <input
          type="password"
          id="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          style={{
            padding: '8px',
            border: '1px solid #ddd',
            borderRadius: '4px',
            width: '100%'
          }}
        />
      </div>
      <button
        type="submit"
        className="login-button"
        style={{
          padding: '8px 16px',
          backgroundColor: '#007cba',
          color: 'white',
          border: 'none',
          borderRadius: '4px',
          cursor: 'pointer'
        }}
      >
        Login
      </button>
    </form>
  );
};

export default Chatbot;