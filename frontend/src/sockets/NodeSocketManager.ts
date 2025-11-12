/* eslint-disable @typescript-eslint/no-explicit-any */
import { WebSocketService } from "./WebSocketService";
import type { MessageHandler } from "./WebSocketService";

export class NodeSocketManager {
  private webSocketService: WebSocketService;
  private nodeHandlers: Map<string, MessageHandler> = new Map();

  constructor(url: string) {
    this.webSocketService = new WebSocketService(url);

    // Register a generic handler that routes messages to specific nodes
    this.webSocketService.registerHandler(
      this.handleIncomingMessage.bind(this)
    );
  }

  private handleIncomingMessage(data: any) {
    // Route message to appropriate node handler based on nodeid
    // Utilizes encapsulation based on standard networking protocols
    const nodeId = data.nodeid;
    const nodedata = data.data;
    if (nodeId && this.nodeHandlers.has(nodeId)) {
      const handler = this.nodeHandlers.get(nodeId);
      if (handler) {
        try {
          handler(nodedata);
        } catch (error) {
          console.error(`Error in node handler for ${nodeId}:`, error);
        }
      }
    }
  }

  send(nodeId: string, data: any) {
    this.webSocketService.send({
      nodeid: nodeId,
      data: data,
    });
  }

  registerNodeHandler(nodeId: string, handler: MessageHandler) {
    this.nodeHandlers.set(nodeId, handler);
  }

  unregisterNodeHandler(nodeId: string) {
    this.nodeHandlers.delete(nodeId);
  }

  close() {
    this.webSocketService.close();
    this.nodeHandlers.clear();
  }

  get isConnected() {
    return this.webSocketService.isConnected;
  }
}
