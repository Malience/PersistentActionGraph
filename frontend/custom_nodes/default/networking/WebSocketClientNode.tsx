/* eslint-disable @typescript-eslint/no-explicit-any */
import { memo } from "react";
import CustomNode from "../../../src/nodes/CustomNode";
import TextComponent from "../../../src/components/TextComponent";

const WebSocketClientNode: CustomNode = ({ data, sync, sendSignal }) => {
  const handleConnectClick = () => {
    sendSignal("connect", null);
  };

  const handleDisconnectClick = () => {
    sendSignal("disconnect", null);
  };

  const handleSendClick = () => {
    sendSignal("activate", null);
  };

  const isConnected = data?._connected === true;

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        gap: "8px",
        padding: "8px",
      }}
    >
      {/* URL Input */}
      <TextComponent
        data={data}
        sync={sync}
        dataField="url"
        label="WebSocket URL"
        placeholder="ws://localhost:8000/wsapi/path"
        multiline={false}
      />

      {/* Status Display */}
      <div
        style={{
          padding: "4px 8px",
          borderRadius: "4px",
          backgroundColor: isConnected ? "#d4edda" : "#f8d7da",
          color: isConnected ? "#155724" : "#721c24",
          fontSize: "12px",
          fontWeight: "bold",
        }}
      >
        {isConnected ? "✓ Connected" : "✗ Disconnected"}
      </div>

      {/* Connection Button */}
      <div style={{ display: "flex", gap: "8px" }}>
        <button
          onClick={isConnected ? handleDisconnectClick : handleConnectClick}
          style={{
            flex: 1,
            backgroundColor: isConnected ? "#dc3545" : "#007bff",
            color: "white",
            border: "none",
            padding: "6px 12px",
            borderRadius: "4px",
            cursor: "pointer",
            opacity: 1,
          }}
        >
          {isConnected ? "Disconnect" : "Connect"}
        </button>
      </div>

      {/* Send Button */}
      <button
        onClick={handleSendClick}
        disabled={!isConnected}
        style={{
          backgroundColor: !isConnected ? "#6c757d" : "#28a745",
          color: "white",
          border: "none",
          padding: "6px 12px",
          borderRadius: "4px",
          cursor: !isConnected ? "not-allowed" : "pointer",
          opacity: !isConnected ? 0.6 : 1,
        }}
      >
        Send Message
      </button>
    </div>
  );
};

export default memo(WebSocketClientNode);
