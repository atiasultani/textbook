import React from 'react';

// Individual message display component
const ChatMessage = ({ message, isLastMessage = false }) => {
  const { sender, content, timestamp, type = 'text', metadata = {}, status } = message;

  // Format timestamp for display
  const formatTime = (timestamp) => {
    if (!timestamp) return '';
    const date = new Date(timestamp);
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  // Render different message types
  const renderContent = () => {
    switch (type) {
      case 'code':
        return (
          <pre className="message-code">
            <code className={`language-${metadata.language || ''}`}>
              {content}
            </code>
          </pre>
        );
      case 'list':
        try {
          // If content is a string that looks like JSON array, parse it
          const listItems = typeof content === 'string' && content.startsWith('[')
            ? JSON.parse(content)
            : Array.isArray(content) ? content : [content];

          return (
            <ul className="message-list">
              {listItems.map((item, index) => (
                <li key={index}>{item}</li>
              ))}
            </ul>
          );
        } catch (e) {
          // If parsing fails, just display as regular text
          return <div className="message-text">{content}</div>;
        }
      case 'error':
        return (
          <div className="message-error">
            ⚠️ {content}
          </div>
        );
      default:
        return <div className="message-text">{content}</div>;
    }
  };

  return (
    <div className={`message message--${sender} ${status ? `message--${status}` : ''}`}>
      <div className="message-content">
        <div className={`message-bubble message-bubble--${sender}`}>
          {renderContent()}
          {timestamp && (
            <div className="message-timestamp">
              {formatTime(timestamp)}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ChatMessage;