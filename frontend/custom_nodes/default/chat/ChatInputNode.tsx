/* eslint-disable @typescript-eslint/no-explicit-any */
import { memo, useCallback, KeyboardEvent } from "react";
import CustomNode from "../../../src/nodes/CustomNode";

interface ChatInputNodeProps {
  data: any;
  sync: (data: any) => void;
  sendSignal: (signal: string, params: any) => void;
}

const ChatInputNode: CustomNode = ({
  data,
  sync,
  sendSignal,
}: ChatInputNodeProps) => {
  const handleTextChange = useCallback(
    (event: React.ChangeEvent<HTMLTextAreaElement>) => {
      const updatedData = { ...data, text: event.target.value };
      sync(updatedData);
    },
    [data, sync]
  );

  const handleKeyDown = useCallback(
    (event: KeyboardEvent<HTMLTextAreaElement>) => {
      if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        sendSignal("submit", "");
      }
    },
    [sendSignal]
  );

  const handleSubmit = useCallback(() => {
    sendSignal("submit", "");
  }, [sendSignal]);

  const text = data?.text || "";
  const placeholder = data?.placeholder || "Type a message...";

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        gap: "8px",
        padding: "8px",
        minWidth: "250px",
      }}
    >
      <div
        style={{
          display: "flex",
          flexDirection: "row",
          gap: "4px",
        }}
      >
        <textarea
          value={text}
          onChange={handleTextChange}
          onKeyDown={handleKeyDown}
          placeholder={placeholder}
          rows={1}
          style={{
            width: "100%",
            background: "#222222",
            border: "1px solid #111",
            borderRadius: "4px",
            fontSize: "12px",
            color: "#ddd",
            padding: "6px 8px",
            outline: "none",
            resize: "vertical",
            minHeight: "32px",
            fontFamily: "inherit",
          }}
        />
        <button
          onClick={handleSubmit}
          style={{
            background: "#007acc",
            border: "none",
            borderRadius: "4px",
            color: "white",
            fontSize: "12px",
            padding: "6px 12px",
            cursor: "pointer",
            alignSelf: "flex-end",
          }}
        >
          Send
        </button>
      </div>
    </div>
  );
};

export default memo(ChatInputNode);
