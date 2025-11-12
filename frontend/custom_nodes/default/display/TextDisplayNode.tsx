/* eslint-disable @typescript-eslint/no-explicit-any */
import { memo } from "react";
import CustomNode from "../../../src/nodes/CustomNode";

interface TextDisplayNodeProps {
  data: any;
}

const TextDisplayNode: CustomNode = ({ data }: TextDisplayNodeProps) => {
  const displayText = data?.display_text || "";

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        gap: "4px",
        padding: "4px 8px",
        minWidth: "200px",
        minHeight: "100px",
      }}
    >
      <label
        style={{
          fontSize: "12px",
          fontWeight: "500",
          color: "#999999",
        }}
      >
        Text Display
      </label>
      <textarea
        value={displayText}
        readOnly
        placeholder="No text to display"
        rows={6}
        style={{
          width: "100%",
          background: "#222222",
          border: "1px solid #111",
          borderRadius: "4px",
          fontSize: "12px",
          color: "#ddd",
          resize: "vertical",
          fontFamily: "inherit",
          cursor: "default",
        }}
      />
    </div>
  );
};

export default memo(TextDisplayNode);
