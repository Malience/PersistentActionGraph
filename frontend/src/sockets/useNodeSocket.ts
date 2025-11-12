import { useContext } from "react";
import { NodeSocketContext } from "./NodeSocketContext";

export const useNodeSocket = () => {
  const context = useContext(NodeSocketContext);
  if (!context)
    throw new Error("useNodeSocket must be used within NodeSocketProvider");
  return context;
};
