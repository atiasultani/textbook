import React, { useState, useEffect, useRef } from 'react';
import { useLocation } from '@docusaurus/router';
import useAuth from "../hooks/useAuth";
import AuthGuard from './Auth/AuthGuard';

const Chatbot = () => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [sessionId, setSessionId] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [selectedText, setSelectedText] = useState('');
  const [isExpanded, setIsExpanded] = useState(false);
  const [suggestedQuestions, setSuggestedQuestions] = useState([]);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);
  const location = useLocation();

  const { isAuthenticated, token, login, logout, getAccessToken } = useAuth();

  // Initialize chat session when component mounts
  useEffect(() => {
    if (isAuthenticated && getAccessToken()) {
      const initSession = async () => {
        try {
          const response = await fetch('http://localhost:8000/api/v1/chat/start', {
            method: 'POST',
            headers: {
              'Authorization': `Bearer ${getAccessToken()}`,
              'Content-Type': 'application/json',
            },
          });

          if (response.ok) {
            const data = await response.json();
            setSessionId(data.id);
          } else {
            if (response.status === 401) {
              logout();
            }
          }
        } catch (error) {
          console.error('Error initializing chat session:', error);
        }
      };

      initSession();
    }
  }, [isAuthenticated, getAccessToken, logout]);

  // Scroll to bottom of messages
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  
  const sendMessage = async (message = null) => {
    const messageToSend = message || inputValue;
    if (!messageToSend.trim() || !sessionId || isLoading || !isAuthenticated || !getAccessToken()) return;

    const userMessage = { role: 'user', content: messageToSend, timestamp: new Date() };
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      const response = await fetch(`http://localhost:8000/api/v1/chat/${sessionId}/query`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${getAccessToken()}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: messageToSend,
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
          logout();
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

  const handleLogout = () => {
    logout();
    setMessages([]);
    setSessionId(null);
    setSuggestedQuestions([]);
  };

  const handleSuggestedQuestion = (question) => {
    sendMessage(question);
  };

  const toggleExpand = () => {
    setIsExpanded(!isExpanded);
  };

  return (
    <div className={`chatbot-container chatbot-container--modern ${isExpanded ? 'chatbot-container--expanded' : ''}`}>
      <div className="chatbot-header">
        <div className="chatbot-header-content">
          <h3 className="chatbot-title">Textbook Assistant</h3>
          <div className="chatbot-controls">
            <button className="chatbot-expand-btn" onClick={toggleExpand} title={isExpanded ? "Minimize" : "Expand"}>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                {isExpanded ? (
                  <path d="M6 14H9M9 14V11M9 14L3 20M18 10H15M15 10V13M15 10L21 4" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                ) : (
                  <path d="M8 3H5C4.46957 3 3.96086 3.21071 3.58579 3.58579C3.21071 3.96086 3 4.46957 3 5V8M21 8V5C21 4.46957 20.7893 3.96086 20.4142 3.58579C20.0391 3.21071 19.5304 3 19 3H16M16 21H19C19.5304 21 20.0391 20.7893 20.4142 20.4142C20.7893 20.0391 21 19.5304 21 19V16M3 16V19C3 19.5304 3.21071 20.0391 3.58579 20.4142C3.96086 20.7893 4.46957 21 5 21H8" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                )}
              </svg>
            </button>
            <button className="chatbot-logout-btn" onClick={handleLogout} title="Logout">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M17 16L21 12M21 12L17 8M21 12H9M15 3H19C20.1046 3 21 3.89543 21 5V19C21 20.1046 20.1046 21 19 21H5C3.89543 21 3 20.1046 3 19V5C3 3.89543 3.89543 3 5 3H9" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </button>
          </div>
        </div>
        {selectedText && (
          <div className="selected-text-preview">
            <span className="selected-text-label">Context:</span> "{selectedText.substring(0, 60)}{selectedText.length > 60 ? '...' : ''}"
          </div>
        )}
      </div>

      <div className="chat-messages">
        {messages.length === 0 && (
          <div className="chat-welcome">
            <div className="chat-welcome-icon">📚</div>
            <h4>Welcome to the Textbook Assistant!</h4>
            <p>Ask me anything about the textbook content. I can help explain concepts, provide examples, and answer questions based on the material.</p>

            {suggestedQuestions.length > 0 && (
              <div className="suggested-questions">
                <h5>Try asking:</h5>
                <div className="suggested-questions-grid">
                  {suggestedQuestions.map((question, index) => (
                    <button
                      key={index}
                      className="suggested-question-btn"
                      onClick={() => handleSuggestedQuestion(question)}
                    >
                      {question}
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {messages.map((msg, index) => (
          <div key={index} className={`message message--${msg.role}`}>
            <div className="message-avatar">
              {msg.role === 'user' ? (
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M20 21V19C20 16.2386 17.7614 14 15 14H9C6.23858 14 4 16.2386 4 19V21M16 7C16 9.20914 14.2091 11 12 11C9.79086 11 8 9.20914 8 7C8 4.79086 9.79086 3 12 3C14.2091 3 16 4.79086 16 7Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
              ) : (
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M12 8V12L15 15M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
              )}
            </div>
            <div className="message-content">
              <div className={`message-bubble message-bubble--${msg.role}`}>
                {msg.content}

                {msg.sources && msg.sources.length > 0 && (
                  <div className="message-sources">
                    <details className="sources-details">
                      <summary>Sources</summary>
                      <ul>
                        {msg.sources.map((source, idx) => (
                          <li key={idx} className="source-item">
                            <span className="source-title">{source.chapter_title}</span>
                          </li>
                        ))}
                      </ul>
                    </details>
                  </div>
                )}

                {(msg.confidence !== undefined || msg.is_hallucinated) && (
                  <div className="message-meta">
                    {msg.confidence !== undefined && (
                      <span className="confidence-score">Confidence: {(msg.confidence * 100).toFixed(1)}%</span>
                    )}
                    {msg.is_hallucinated && (
                      <span className="hallucination-warning">⚠️ Potential hallucination</span>
                    )}
                  </div>
                )}
              </div>
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="message message--assistant">
            <div className="message-avatar">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 8V12L15 15M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </div>
            <div className="message-content">
              <div className="message-bubble message-bubble--assistant">
                <div className="typing-indicator">
                  <div className="typing-dot"></div>
                  <div className="typing-dot"></div>
                  <div className="typing-dot"></div>
                </div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input-area">
        <div className="chat-input-container">
          <textarea
            ref={inputRef}
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask a question about the textbook..."
            className="chat-input"
            rows="1"
            disabled={isLoading || !sessionId || !isAuthenticated || !getAccessToken()}
          />
          <button
            onClick={sendMessage}
            disabled={isLoading || !sessionId || !inputValue.trim() || !isAuthenticated || !getAccessToken()}
            className="chat-send-btn"
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M22 2L11 13M22 2L15 22L11 13M11 13L2 9L22 2" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </button>
        </div>
        <div className="chat-input-hint">
          Tip: Select text on the page to provide context for your question
        </div>
      </div>
    </div>
  );
};


export default Chatbot;