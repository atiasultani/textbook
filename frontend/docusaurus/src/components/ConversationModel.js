import ChatMessage from './ChatMessageModel';

// Conversation data model implementation
class Conversation {
  constructor({ id, createdAt, context = {}, isActive = true }) {
    this.id = id || this.generateId();
    this.createdAt = createdAt || new Date().toISOString();
    this.lastActiveAt = new Date().toISOString();
    this.messages = [];
    this.context = context;
    this.isActive = isActive;

    this.validate();
  }

  generateId() {
    return `conv_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  validate() {
    if (!this.id) {
      throw new Error('Conversation ID cannot be empty');
    }
    if (!(this.createdAt instanceof Date) && typeof this.createdAt !== 'string') {
      throw new Error('createdAt must be a Date or string');
    }
    if (!Array.isArray(this.messages)) {
      throw new Error('Messages must be an array');
    }
    if (typeof this.isActive !== 'boolean') {
      throw new Error('isActive must be a boolean');
    }
  }

  // Add a message to the conversation
  addMessage(messageData) {
    const message = new ChatMessage(messageData);
    this.messages.push(message);
    this.lastActiveAt = new Date().toISOString();
    return message;
  }

  // Get all messages
  getMessages() {
    return [...this.messages];
  }

  // Get messages by sender
  getMessagesBySender(sender) {
    return this.messages.filter(msg => msg.sender === sender);
  }

  // Get the last message
  getLastMessage() {
    return this.messages.length > 0 ? this.messages[this.messages.length - 1] : null;
  }

  // Update context
  updateContext(newContext) {
    this.context = { ...this.context, ...newContext };
    return this;
  }

  // Mark as inactive
  markInactive() {
    this.isActive = false;
    return this;
  }

  // Mark as active
  markActive() {
    this.isActive = true;
    this.lastActiveAt = new Date().toISOString();
    return this;
  }

  // Check if conversation is active
  isActiveConversation() {
    // Check if conversation has been inactive for more than 30 minutes
    const lastActive = new Date(this.lastActiveAt);
    const now = new Date();
    const inactiveDuration = (now - lastActive) / (1000 * 60); // in minutes

    if (inactiveDuration > 30) {
      this.isActive = false;
    }

    return this.isActive;
  }

  // Get conversation summary
  getSummary() {
    return {
      id: this.id,
      messageCount: this.messages.length,
      userMessageCount: this.getMessagesBySender('user').length,
      botMessageCount: this.getMessagesBySender('bot').length,
      isActive: this.isActive,
      createdAt: this.createdAt,
      lastActiveAt: this.lastActiveAt
    };
  }
}

export default Conversation;