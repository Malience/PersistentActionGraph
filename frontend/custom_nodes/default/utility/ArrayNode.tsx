/* eslint-disable @typescript-eslint/no-explicit-any */
import { memo } from "react";
import CustomNode from "../../../src/nodes/CustomNode";

const ArrayNode: CustomNode = ({ data, sendSignal }) => {
  const length = data?.length || 0;
  const elements = data?.elements || [];

  function handleClearArray() {
    sendSignal("clear", "");
  }

  function handlePopElement() {
    sendSignal("pop", "");
  }

  function handleDequeueElement() {
    sendSignal("dequeue", "");
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
          Elements: <strong>{length}</strong>
        </div>
      </div>

      {/* Array Elements Preview */}
      {elements.length > 0 && (
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
            Array Elements (First 2 & Last 2):
          </div>
          {/* First two elements */}
          {elements.slice(0, 2).map((element: any, index: number) => (
            <div
              key={`first-${index}`}
              style={{
                padding: "2px 4px",
                backgroundColor: "#e9e9e9",
                borderRadius: "2px",
                overflow: "hidden",
                textOverflow: "ellipsis",
                whiteSpace: "nowrap",
              }}
              title={JSON.stringify(element)}
            >
              <span style={{ fontWeight: "bold", color: "#666" }}>
                [{index}]:
              </span>{" "}
              {typeof element === "object"
                ? JSON.stringify(element).substring(0, 25) +
                  (JSON.stringify(element).length > 25 ? "..." : "")
                : String(element).substring(0, 25) +
                  (String(element).length > 25 ? "..." : "")}
            </div>
          ))}

          {/* Separator if there are more than 4 elements */}
          {elements.length > 4 && (
            <div
              style={{
                textAlign: "center",
                fontSize: "9px",
                color: "#999",
                padding: "2px",
              }}
            >
              ...
            </div>
          )}

          {/* Last two elements */}
          {elements.slice(-2).map((element: any, index: number) => (
            <div
              key={`last-${index}`}
              style={{
                padding: "2px 4px",
                backgroundColor: "#e9e9e9",
                borderRadius: "2px",
                overflow: "hidden",
                textOverflow: "ellipsis",
                whiteSpace: "nowrap",
              }}
              title={JSON.stringify(element)}
            >
              <span style={{ fontWeight: "bold", color: "#666" }}>
                [{elements.length - 2 + index}]:
              </span>{" "}
              {typeof element === "object"
                ? JSON.stringify(element).substring(0, 25) +
                  (JSON.stringify(element).length > 25 ? "..." : "")
                : String(element).substring(0, 25) +
                  (String(element).length > 25 ? "..." : "")}
            </div>
          ))}
        </div>
      )}

      {/* Clear Button */}
      <button
        onClick={handleClearArray}
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
        disabled={length === 0}
      >
        Clear Array ({length})
      </button>

      {/* Pop Element Button */}
      <button
        onClick={handlePopElement}
        style={{
          padding: "6px 12px",
          backgroundColor: "#4dabf7",
          color: "white",
          border: "none",
          borderRadius: "4px",
          cursor: "pointer",
          fontSize: "12px",
          fontWeight: "500",
        }}
        disabled={length === 0}
      >
        Pop Element
      </button>

      {/* Dequeue Element Button */}
      <button
        onClick={handleDequeueElement}
        style={{
          padding: "6px 12px",
          backgroundColor: "#69db7c",
          color: "white",
          border: "none",
          borderRadius: "4px",
          cursor: "pointer",
          fontSize: "12px",
          fontWeight: "500",
        }}
        disabled={length === 0}
      >
        Dequeue Element
      </button>
    </div>
  );
};

export default memo(ArrayNode);
