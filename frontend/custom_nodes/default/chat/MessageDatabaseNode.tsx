import { memo } from "react";
import CustomNode from "../../../src/nodes/CustomNode";

interface Message {
  role: string;
  content: string;
}

const MessageDatabaseNode: CustomNode = ({ data, sendSignal }) => {
  const messageCount = data?.message_count || 0;
  const messages = data?.messages || [];

  function handleClearDatabase() {
    sendSignal("clear_database", "");
  }

  function handleDeleteLastMessage() {
    sendSignal("delete_last_message", "");
  }

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        gap: "8px",
        padding: "12px",
        minWidth: "200px",
      }}
    >
      {/* Statistics Section */}
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          gap: "4px",
          padding: "8px",
          backgroundColor: "#f5f5f5",
          borderRadius: "4px",
        }}
      >
        <div style={{ fontSize: "12px", fontWeight: "600" }}>Statistics</div>
        <div style={{ fontSize: "11px" }}>
          Messages: <strong>{messageCount}</strong>
        </div>
      </div>

      {/* Recent Messages Preview */}
      {messages.length > 0 && (
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            gap: "4px",
            maxHeight: "120px",
            overflowY: "auto",
            padding: "4px",
            backgroundColor: "#f9f9f9",
            borderRadius: "4px",
            fontSize: "10px",
          }}
        >
          <div style={{ fontSize: "11px", fontWeight: "600" }}>
            Recent Messages:
          </div>
          {messages.slice(-3).map((message: Message, index: number) => (
            <div
              key={index}
              style={{
                padding: "2px 4px",
                backgroundColor: "#e9e9e9",
                borderRadius: "2px",
                overflow: "hidden",
                textOverflow: "ellipsis",
                whiteSpace: "nowrap",
              }}
              title={`${message.role}: ${message.content}`}
            >
              <span style={{ fontWeight: "bold", color: "#666" }}>
                {message.role}:
              </span>{" "}
              {message.content.substring(0, 30)}
              {message.content.length > 30 ? "..." : ""}
            </div>
          ))}
        </div>
      )}

      {/* Clear Button */}
      <button
        onClick={handleClearDatabase}
        style={{
          padding: "6px 12px",
          backgroundColor: "#ff6b6b",
          color: "white",
          border: "none",
          borderRadius: "4px",
          cursor: "pointer",
          fontSize: "12px",
          fontWeight: "500",
        }}
        disabled={messageCount === 0}
      >
        Clear Database ({messageCount})
      </button>

      {/* Delete Last Message Button */}
      <button
        onClick={handleDeleteLastMessage}
        style={{
          padding: "6px 12px",
          backgroundColor: "#ffa94d",
          color: "white",
          border: "none",
          borderRadius: "4px",
          cursor: "pointer",
          fontSize: "12px",
          fontWeight: "500",
        }}
        disabled={messageCount === 0}
      >
        Delete Last Message
      </button>
    </div>
  );
};

export default memo(MessageDatabaseNode);
