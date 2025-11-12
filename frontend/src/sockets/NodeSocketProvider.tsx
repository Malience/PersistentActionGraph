import React, { useEffect, useRef } from "react";
import { NodeSocketManager } from "./NodeSocketManager";
import {
  NodeSocketContext,
  type NodeSocketContextType,
} from "./NodeSocketContext";

export const NodeSocketProvider: React.FC<{
  children: React.ReactNode;
  socketUrl: string;
}> = ({ children, socketUrl }) => {
  const nodeSocketManager = useRef<NodeSocketManager | undefined>(undefined);

  useEffect(() => {
    let isMounted = true;

    if (isMounted) {
      nodeSocketManager.current = new NodeSocketManager(socketUrl);
    }

    return () => {
      isMounted = false;
      nodeSocketManager.current?.close();
    };
  }, [socketUrl]);

  const contextValue: NodeSocketContextType = {
    sendMessage: (nodeId, data) =>
      nodeSocketManager.current?.send(nodeId, data),
    registerNodeHandler: (nodeId, handler) =>
      nodeSocketManager.current?.registerNodeHandler(nodeId, handler),
    unregisterNodeHandler: (nodeId) =>
      nodeSocketManager.current?.unregisterNodeHandler(nodeId),
  };

  return (
    <NodeSocketContext.Provider value={contextValue}>
      {children}
    </NodeSocketContext.Provider>
  );
};
