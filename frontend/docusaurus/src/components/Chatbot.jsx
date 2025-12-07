import React, { useState, useEffect } from 'react';
import { useLocation } from '@docusaurus/router';

const Chatbot = () => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [sessionId, setSessionId] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const location = useLocation();

  // Initialize chat session when component mounts
  useEffect(() => {
    const initSession = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/v1/chat/start', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
        });
        const data = await response.json();
        setSessionId(data.id);
      } catch (error) {
        console.error('Error initializing chat session:', error);
      }
    };

    initSession();
  }, []);

  const sendMessage = async () => {
    if (!inputValue.trim() || !sessionId || isLoading) return;

    const userMessage = { role: 'user', content: inputValue, timestamp: new Date() };
    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const response = await fetch(`http://localhost:8000/api/v1/chat/${sessionId}/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: inputValue,
          context: [] // For simplicity, not sending context
        }),
      });

      const data = await response.json();

      const botMessage = {
        role: 'assistant',
        content: data.response,
        sources: data.sources,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, botMessage]);
      setInputValue('');
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

  return (
    <div className="chatbot-container" style={{
      border: '1px solid #ddd',
      borderRadius: '8px',
      padding: '16px',
      marginTop: '16px',
      backgroundColor: '#f9f9f9'
    }}>
      <h3>Textbook Assistant</h3>
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
          disabled={isLoading || !sessionId}
        />
        <button
          onClick={sendMessage}
          disabled={isLoading || !sessionId || !inputValue.trim()}
          style={{
            padding: '8px 16px',
            backgroundColor: '#007cba',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: (isLoading || !sessionId || !inputValue.trim()) ? 'not-allowed' : 'pointer'
          }}
        >
          Send
        </button>
      </div>
    </div>
  );
};

export default Chatbot;