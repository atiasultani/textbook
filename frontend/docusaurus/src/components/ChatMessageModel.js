// ChatMessage data model implementation
class ChatMessage {
  constructor({ id, content, sender, timestamp, status = 'sent', type = 'text', metadata = {} }) {
    this.id = id || this.generateId();
    this.content = content;
    this.sender = sender; // 'user' or 'bot'
    this.timestamp = timestamp || new Date().toISOString();
    this.status = status; // 'sent', 'delivered', 'error'
    this.type = type; // 'text', 'code', 'list', 'error'
    this.metadata = metadata;

    this.validate();
  }

  generateId() {
    return `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  validate() {
    if (!this.content) {
      throw new Error('Content cannot be empty');
    }
    if (!['user', 'bot'].includes(this.sender)) {
      throw new Error('Sender must be either "user" or "bot"');
    }
    if (!['sent', 'delivered', 'error'].includes(this.status)) {
      throw new Error('Status must be one of: "sent", "delivered", "error"');
    }
    if (!['text', 'code', 'list', 'error'].includes(this.type)) {
      throw new Error('Type must be one of: "text", "code", "list", "error"');
    }
    if (!(this.timestamp instanceof Date) && typeof this.timestamp !== 'string') {
      throw new Error('Timestamp must be a Date or string');
    }
  }

  // Update status
  updateStatus(newStatus) {
    if (!['sent', 'delivered', 'error'].includes(newStatus)) {
      throw new Error('Status must be one of: "sent", "delivered", "error"');
    }
    this.status = newStatus;
    return this;
  }

  // Check if message is from user
  isFromUser() {
    return this.sender === 'user';
  }

  // Check if message is from bot
  isFromBot() {
    return this.sender === 'bot';
  }

  // Format for display
  getDisplayContent() {
    return this.content;
  }
}

export default ChatMessage;