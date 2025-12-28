// API service to handle chat endpoints
class ChatApiService {
  constructor(baseURL, apiKey = null) {
    this.baseURL = baseURL;
    this.apiKey = apiKey;
  }

  // Set API key
  setApiKey(apiKey) {
    this.apiKey = apiKey;
  }

  // Get headers with authentication
  getHeaders() {
    const headers = {
      'Content-Type': 'application/json',
    };

    if (this.apiKey) {
      headers['Authorization'] = `Bearer ${this.apiKey}`;
    }

    return headers;
  }

  // Start a new conversation
  async startConversation(context = {}) {
    try {
      const response = await fetch(`${this.baseURL}/chat/start`, {
        method: 'POST',
        headers: this.getHeaders(),
        body: JSON.stringify({
          context: context.context || '',
          user_preferences: context.user_preferences || {
            response_style: 'professional',
            language: 'en'
          }
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error starting conversation:', error);
      throw error;
    }
  }

  // Send a message in a conversation
  async sendMessage(conversationId, message, timestamp = new Date().toISOString()) {
    try {
      const response = await fetch(`${this.baseURL}/chat/${conversationId}/message`, {
        method: 'POST',
        headers: this.getHeaders(),
        body: JSON.stringify({
          message: message,
          timestamp: timestamp
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error sending message:', error);
      throw error;
    }
  }

  // Get conversation history
  async getConversationHistory(conversationId) {
    try {
      const response = await fetch(`${this.baseURL}/chat/${conversationId}/history`, {
        method: 'GET',
        headers: this.getHeaders()
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error getting conversation history:', error);
      throw error;
    }
  }

  // Check if bot is typing
  async getTypingStatus(conversationId) {
    try {
      const response = await fetch(`${this.baseURL}/chat/${conversationId}/typing`, {
        method: 'GET',
        headers: this.getHeaders()
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error getting typing status:', error);
      throw error;
    }
  }

  // Update conversation context
  async updateConversationContext(conversationId, context) {
    try {
      const response = await fetch(`${this.baseURL}/chat/${conversationId}/context`, {
        method: 'POST',
        headers: this.getHeaders(),
        body: JSON.stringify({ context })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error updating conversation context:', error);
      throw error;
    }
  }

  // Check API connectivity
  async checkConnectivity() {
    try {
      const response = await fetch(`${this.baseURL}/health`, {
        method: 'GET',
        headers: this.getHeaders()
      });

      return response.ok;
    } catch (error) {
      console.error('Error checking connectivity:', error);
      return false;
    }
  }
}

export default ChatApiService;