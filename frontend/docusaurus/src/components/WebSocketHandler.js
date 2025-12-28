// WebSocket connection handler for real-time updates
class WebSocketHandler {
  constructor(url, onMessage, onError, onOpen, onClose) {
    this.url = url;
    this.onMessage = onMessage || (() => {});
    this.onError = onError || (() => {});
    this.onOpen = onOpen || (() => {});
    this.onClose = onClose || (() => {});
    this.websocket = null;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
    this.reconnectInterval = 3000; // 3 seconds
    this.shouldReconnect = true;
  }

  // Connect to WebSocket
  connect() {
    try {
      this.websocket = new WebSocket(this.url);

      this.websocket.onopen = (event) => {
        console.log('WebSocket connected');
        this.reconnectAttempts = 0; // Reset on successful connection
        this.onOpen(event);
      };

      this.websocket.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          this.onMessage(data);
        } catch (error) {
          console.error('Error parsing WebSocket message:', error);
          this.onError(new Error('Invalid message format received from server'));
        }
      };

      this.websocket.onerror = (event) => {
        console.error('WebSocket error:', event);
        this.onError(event);
      };

      this.websocket.onclose = (event) => {
        console.log('WebSocket disconnected:', event.code, event.reason);

        if (this.shouldReconnect && this.reconnectAttempts < this.maxReconnectAttempts) {
          this.reconnectAttempts++;
          console.log(`Attempting to reconnect... (${this.reconnectAttempts}/${this.maxReconnectAttempts})`);

          setTimeout(() => {
            this.connect();
          }, this.reconnectInterval * this.reconnectAttempts); // Increasing delay with each attempt
        } else {
          this.onClose(event);
        }
      };
    } catch (error) {
      console.error('Error creating WebSocket connection:', error);
      this.onError(error);
    }
  }

  // Send message through WebSocket
  send(data) {
    if (this.websocket && this.websocket.readyState === WebSocket.OPEN) {
      const message = typeof data === 'string' ? data : JSON.stringify(data);
      this.websocket.send(message);
    } else {
      throw new Error('WebSocket is not connected');
    }
  }

  // Check if WebSocket is connected
  isConnected() {
    return this.websocket && this.websocket.readyState === WebSocket.OPEN;
  }

  // Check connection state
  getConnectionState() {
    if (!this.websocket) {
      return 'CLOSED';
    }

    const states = {
      [WebSocket.CONNECTING]: 'CONNECTING',
      [WebSocket.OPEN]: 'OPEN',
      [WebSocket.CLOSING]: 'CLOSING',
      [WebSocket.CLOSED]: 'CLOSED'
    };

    return states[this.websocket.readyState];
  }

  // Close WebSocket connection
  close() {
    this.shouldReconnect = false;
    if (this.websocket) {
      this.websocket.close();
    }
  }

  // Reconnect WebSocket
  reconnect() {
    this.shouldReconnect = true;
    if (this.websocket) {
      this.websocket.close();
    }
    this.connect();
  }

  // Set event handlers after initialization
  setEventHandlers(handlers) {
    if (handlers.onMessage) this.onMessage = handlers.onMessage;
    if (handlers.onError) this.onError = handlers.onError;
    if (handlers.onOpen) this.onOpen = handlers.onOpen;
    if (handlers.onClose) this.onClose = handlers.onClose;
  }
}

export default WebSocketHandler;