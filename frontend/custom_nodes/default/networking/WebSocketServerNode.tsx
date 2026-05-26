/* eslint-disable @typescript-eslint/no-explicit-any */
import { memo } from "react";
import CustomNode from "../../../src/nodes/CustomNode";
import TextComponent from "../../../src/components/TextComponent";

const WebSocketServerNode: CustomNode = ({ data, sync, sendSignal }) => {
  const handleSetSocketClick = () => {
    sendSignal("set_socket", null);
    sendSignal("sync", null);
  };

  const handleRemoveSocketClick = () => {
    sendSignal("remove_socket", null);
    sendSignal("sync", null);
  };

  const handleDataChange = (data: any) => {
    sync(data);
    // Remove the last socket if the data changes
    sendSignal("sync", null);
  };

  const handleSendClick = () => {
    sendSignal("send", null);
  };

  const isSocketSet = data?._socket !== undefined && data?._socket !== null;

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        gap: "8px",
        padding: "8px",
      }}
    >
      {/* Path Input */}
      <TextComponent
        data={data}
        sync={handleDataChange}
        dataField="path"
        label="WebSocket Path"
        placeholder="/my-websocket"
        multiline={false}
      />

      {/* Status Display */}
      <div
        style={{
          padding: "4px 8px",
          borderRadius: "4px",
          backgroundColor: isSocketSet ? "#d4edda" : "#f8d7da",
          color: isSocketSet ? "#155724" : "#721c24",
          fontSize: "12px",
          fontWeight: "bold",
        }}
      >
        {isSocketSet ? "✓ WebSocket Active" : "✗ WebSocket Not Set"}
      </div>

      {/* Set/Remove Socket Buttons */}
      <div style={{ display: "flex", gap: "8px" }}>
        <button
          onClick={handleSetSocketClick}
          style={{
            flex: 1,
            backgroundColor: "#007bff",
            color: "white",
            border: "none",
            padding: "6px 12px",
            borderRadius: "4px",
            cursor: "pointer",
          }}
        >
          Set WebSocket
        </button>
        <button
          onClick={handleRemoveSocketClick}
          style={{
            flex: 1,
            backgroundColor: "#dc3545",
            color: "white",
            border: "none",
            padding: "6px 12px",
            borderRadius: "4px",
            cursor: "pointer",
          }}
        >
          Remove
        </button>
      </div>

      {/* Send Message Button */}
      <button
        onClick={handleSendClick}
        style={{
          backgroundColor: "#28a745",
          color: "white",
          border: "none",
          padding: "6px 12px",
          borderRadius: "4px",
          cursor: "pointer",
        }}
      >
        Send Message to Clients
      </button>

      {/* WebSocket URL Display */}
      {isSocketSet && (
        <div
          style={{
            padding: "8px",
            backgroundColor: "#f8f9fa",
            borderRadius: "4px",
            fontSize: "12px",
            border: "1px solid #dee2e6",
          }}
        >
          <div style={{ fontWeight: "bold", marginBottom: "4px" }}>
            Active WebSocket:
          </div>
          <div style={{ fontFamily: "monospace" }}>{data?._socket || ""}</div>
          <div style={{ fontSize: "10px", color: "#6c757d", marginTop: "4px" }}>
            Connect at: ws://localhost:8000{data?._socket || ""}
          </div>
        </div>
      )}
    </div>
  );
};

export default memo(WebSocketServerNode);
