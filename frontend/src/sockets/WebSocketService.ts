/* eslint-disable @typescript-eslint/no-explicit-any */
export type MessageHandler = (data: any) => void;

export class WebSocketService {
  private socket: WebSocket | null = null;
  private handlers: Set<MessageHandler> = new Set();
  private url: string;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectDelay = 1000;

  constructor(url: string) {
    this.url = url;
    this.connect();
  }

  private connect() {
    try {
      this.socket = new WebSocket(this.url);

      this.socket.onopen = () => {
        console.log(`WebSocket connected to ${this.url}`);
        this.reconnectAttempts = 0;
      };

      this.socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        this.handleMessage(data);
      };

      this.socket.onclose = () => {
        console.log(`WebSocket disconnected from ${this.url}`);
        this.attemptReconnect();
      };

      this.socket.onerror = (error) => {
        console.error(`WebSocket error for ${this.url}:`, error);
      };
    } catch (error) {
      console.error(`Failed to connect to ${this.url}:`, error);
    }
  }

  private attemptReconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      console.log(
        `Attempting to reconnect (${this.reconnectAttempts}/${this.maxReconnectAttempts})...`
      );
      setTimeout(
        () => this.connect(),
        this.reconnectDelay * this.reconnectAttempts
      );
    }
  }

  private handleMessage(data: any) {
    // Send message to all registered handlers
    this.handlers.forEach((handler) => {
      try {
        handler(data);
      } catch (error) {
        console.error("Error in WebSocket message handler:", error);
      }
    });
  }

  send(data: any) {
    if (this.socket?.readyState === WebSocket.OPEN) {
      this.socket.send(JSON.stringify(data));
    } else {
      console.warn("WebSocket not connected, message not sent:", data);
    }
  }

  registerHandler(handler: MessageHandler) {
    this.handlers.add(handler);
  }

  unregisterHandler(handler: MessageHandler) {
    this.handlers.delete(handler);
  }

  close() {
    this.socket?.close();
    this.handlers.clear();
  }

  get isConnected() {
    return this.socket?.readyState === WebSocket.OPEN;
  }
}
