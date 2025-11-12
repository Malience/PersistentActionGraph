/* eslint-disable @typescript-eslint/no-explicit-any */
import { memo } from "react";
import CustomNode from "../../../src/nodes/CustomNode";

const DictNode: CustomNode = ({ data, sendSignal }) => {
  const count = data?.count || 0;

  function handleClearDict() {
    sendSignal("clear", "");
  }

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        gap: "8px",
        padding: "12px",
        minWidth: "250px",
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
          Entries: <strong>{count}</strong>
        </div>
      </div>

      {/* Clear Button */}
      <button
        onClick={handleClearDict}
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
        disabled={count === 0}
      >
        Clear Dictionary ({count})
      </button>
    </div>
  );
};

export default memo(DictNode);
