// ChatSession data model implementation
class ChatSession {
  constructor({ conversationId, isTyping = false, inputText = '', error = null, connectionStatus = 'disconnected' }) {
    this.conversationId = conversationId;
    this.isTyping = isTyping;
    this.inputText = inputText;
    this.error = error;
    this.connectionStatus = connectionStatus; // 'connected', 'connecting', 'disconnected'

    this.validate();
  }

  validate() {
    if (this.conversationId && typeof this.conversationId !== 'string') {
      throw new Error('Conversation ID must be a string');
    }
    if (typeof this.isTyping !== 'boolean') {
      throw new Error('isTyping must be a boolean');
    }
    if (typeof this.inputText !== 'string') {
      throw new Error('inputText must be a string');
    }
    if (this.error && typeof this.error !== 'string' && !(this.error instanceof Error)) {
      throw new Error('error must be a string or Error object');
    }
    if (!['connected', 'connecting', 'disconnected'].includes(this.connectionStatus)) {
      throw new Error('connectionStatus must be one of: "connected", "connecting", "disconnected"');
    }
  }

  // Update conversation ID
  updateConversationId(id) {
    this.conversationId = id;
    return this;
  }

  // Set typing status
  setTyping(isTyping) {
    this.isTyping = Boolean(isTyping);
    return this;
  }

  // Update input text
  setInputText(text) {
    if (typeof text !== 'string') {
      throw new Error('Input text must be a string');
    }
    // Limit input length to prevent abuse
    this.inputText = text.substring(0, 1000);
    return this;
  }

  // Set error
  setError(error) {
    this.error = error ? (typeof error === 'string' ? error : error.message || 'Unknown error') : null;
    return this;
  }

  // Update connection status
  setConnectionStatus(status) {
    if (!['connected', 'connecting', 'disconnected'].includes(status)) {
      throw new Error('Invalid connection status');
    }
    this.connectionStatus = status;
    return this;
  }

  // Check if connected
  isConnected() {
    return this.connectionStatus === 'connected';
  }

  // Check if connecting
  isConnecting() {
    return this.connectionStatus === 'connecting';
  }

  // Check if disconnected
  isDisconnected() {
    return this.connectionStatus === 'disconnected';
  }

  // Get session state for persistence
  getState() {
    return {
      conversationId: this.conversationId,
      isTyping: this.isTyping,
      inputText: this.inputText,
      error: this.error,
      connectionStatus: this.connectionStatus
    };
  }

  // Create from state
  static fromState(state) {
    return new ChatSession(state);
  }
}

export default ChatSession;