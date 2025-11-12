import { memo, useRef, useEffect } from "react";
import CustomNode from "../../../src/nodes/CustomNode";
import BooleanSwitchComponent from "../../../src/components/BooleanSwitchComponent";

interface Message {
  role: string;
  content: string;
}

const ChatDisplayNode: CustomNode = ({ data, sync }) => {
  const messages = data?.messages || [];
  const autoScroll = data?.auto_scroll ?? true;
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const scrollContainerRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    if (autoScroll) {
      scrollToBottom();
    }
  }, [messages, autoScroll]);

  const getMessageStyle = (role: string) => {
    const isUser = role === "user";
    const isSystem = role === "system";

    let backgroundColor, color, borderColor;

    if (isUser) {
      backgroundColor = "#007bff";
      color = "white";
      borderColor = "none";
    } else if (isSystem) {
      backgroundColor = "#805ad5"; // Purple for system messages
      color = "white";
      borderColor = "#6b46c1";
    } else {
      // Assistant messages
      backgroundColor = "#2d3748";
      color = "#e2e8f0";
      borderColor = "#4a5568";
    }

    return {
      maxWidth: "80%",
      padding: "8px 12px",
      margin: "2px 0",
      borderRadius: "12px",
      fontSize: "13px",
      lineHeight: "1.4",
      whiteSpace: "pre-wrap" as const,
      wordWrap: "break-word" as const,
      alignSelf: isUser ? "flex-end" : "flex-start",
      backgroundColor,
      color,
      borderBottomRightRadius: isUser ? "4px" : "12px",
      borderBottomLeftRadius: isUser ? "12px" : "4px",
      border: isUser ? "none" : `1px solid ${borderColor}`,
    };
  };

  const getRoleLabel = (role: string) => {
    switch (role) {
      case "user":
        return "User";
      case "assistant":
        return "Assistant";
      case "system":
        return "System";
      default:
        return role;
    }
  };

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        height: "100%",
        width: "100%",
        minHeight: "0",
      }}
    >
      {/* Auto-scroll Toggle */}
      <div style={{ padding: "8px", paddingBottom: "4px" }}>
        <BooleanSwitchComponent
          data={data}
          sync={sync}
          dataField="auto_scroll"
          label="Auto-scroll"
        />
      </div>
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          flex: 1,
          minHeight: "0", // Important for flex children to shrink properly
          padding: "0 8px 8px 8px",
        }}
      >
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            flex: 1,
            backgroundColor: "#1a202c",
            borderRadius: "8px",
            border: "1px solid #2d3748",
            overflow: "hidden",
          }}
        >
          {/* Messages Container */}
          <div
            ref={scrollContainerRef}
            style={{
              display: "flex",
              flexDirection: "column",
              gap: "4px",
              height: "100%",
              overflowY: "auto",
              padding: "4px 8px 4px 4px",
              backgroundColor: "#1a202c",
              cursor: "default",
            }}
            tabIndex={0}
            onWheel={(e) => {
              // Doesn't work, I tried my best :(
              // Allow natural scroll wheel behavior
              e.stopPropagation();
            }}
          >
            {messages.length === 0 ? (
              <div
                style={{
                  textAlign: "center",
                  color: "#a0aec0",
                  fontSize: "12px",
                  fontStyle: "italic",
                  padding: "20px",
                }}
              >
                No messages to display
              </div>
            ) : (
              messages.map((message: Message, index: number) => (
                <div
                  key={index}
                  style={{
                    display: "flex",
                    flexDirection: "column",
                    alignItems:
                      message.role === "user" ? "flex-end" : "flex-start",
                    marginBottom: "2px",
                  }}
                >
                  {/* Role Label */}
                  <div
                    style={{
                      fontSize: "9px",
                      color: "#a0aec0",
                      marginBottom: "1px",
                      padding: "0 8px",
                      opacity: 0.8,
                    }}
                  >
                    {getRoleLabel(message.role)}
                  </div>

                  {/* Message Bubble */}
                  <div style={getMessageStyle(message.role)}>
                    {message.content}
                  </div>
                </div>
              ))
            )}
            <div ref={messagesEndRef} />
          </div>
        </div>
      </div>
    </div>
  );
};

export default memo(ChatDisplayNode);
