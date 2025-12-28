import React, { useEffect, useRef } from 'react';
import ChatMessage from './ChatMessage';

// Message history display component
const ChatHistory = ({ messages = [], isTyping = false }) => {
  const messagesEndRef = useRef(null);

  // Scroll to bottom when messages change
  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <div className="chat-history-container">
      <div className="chat-messages">
        {messages.length === 0 ? (
          <div className="chat-empty-state">
            <p>No messages yet. Start a conversation!</p>
          </div>
        ) : (
          <>
            {messages.map((message, index) => (
              <ChatMessage
                key={message.id || `msg-${index}`}
                message={message}
                isLastMessage={index === messages.length - 1}
              />
            ))}
            {isTyping && (
              <div className="message message--bot message--typing">
                <div className="message-content">
                  <div className="message-bubble message-bubble--bot">
                    <div className="typing-indicator">
                      <div className="typing-dot"></div>
                      <div className="typing-dot"></div>
                      <div className="typing-dot"></div>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </>
        )}
      </div>
      <div ref={messagesEndRef} />
    </div>
  );
};

export default ChatHistory;