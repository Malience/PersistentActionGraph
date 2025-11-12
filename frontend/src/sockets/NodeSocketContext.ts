/* eslint-disable @typescript-eslint/no-explicit-any */
import { createContext } from "react";

export interface NodeSocketContextType {
  sendMessage: (nodeId: string, data: any) => void;
  registerNodeHandler: (nodeId: string, handler: (data: any) => void) => void;
  unregisterNodeHandler: (nodeId: string) => void;
}

export const NodeSocketContext = createContext<
  NodeSocketContextType | undefined
>(undefined);
