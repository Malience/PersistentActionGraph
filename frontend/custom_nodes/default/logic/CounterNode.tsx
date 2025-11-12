import { memo } from "react";
import CustomNode from "../../../src/nodes/CustomNode";
import NumberComponent from "../../../src/components/NumberComponent";
import BooleanSwitchComponent from "../../../src/components/BooleanSwitchComponent";

const CounterNode: CustomNode = ({ data, sync, sendSignal }) => {
  const currentValue = data?.current_value || 0;

  const handleIncrementClick = () => {
    // Send signal to backend to increment the counter
    sendSignal("increment", "");
  };

  const handleDecrementClick = () => {
    // Send signal to backend to decrement the counter
    sendSignal("decrement", "");
  };

  const handleClearClick = () => {
    // Send signal to backend to clear the counter
    sendSignal("clear", "");
  };

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
      {/* Large Value Display */}
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: "4px",
          padding: "12px",
          backgroundColor: "#f5f5f5",
          borderRadius: "8px",
          border: "2px solid #ddd",
        }}
      >
        <div style={{ fontSize: "10px", fontWeight: "600", color: "#666" }}>
          Current Value
        </div>
        <div style={{ fontSize: "24px", fontWeight: "bold", color: "#333" }}>
          {currentValue}
        </div>
      </div>

      {/* Configuration Settings */}
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          gap: "6px",
          padding: "8px",
          backgroundColor: "#f8f9fa",
          borderRadius: "4px",
        }}
      >
        <div style={{ fontSize: "11px", fontWeight: "600", color: "#495057" }}>
          Configuration
        </div>

        {/* Looping Toggle */}
        <BooleanSwitchComponent
          data={data}
          sync={sync}
          dataField="looping"
          label="Looping"
        />

        {/* Step Size */}
        <NumberComponent
          data={data}
          sync={sync}
          dataField="step"
          label="Step"
          min="1"
          step="1"
          placeholder="1"
        />

        {/* Minimum Value */}
        <NumberComponent
          data={data}
          sync={sync}
          dataField="min"
          label="Min"
          step="1"
          placeholder="0"
        />

        {/* Maximum Value */}
        <NumberComponent
          data={data}
          sync={sync}
          dataField="max"
          label="Max"
          step="1"
          placeholder="100"
        />
      </div>

      {/* Control Buttons */}
      <div
        style={{
          display: "flex",
          gap: "4px",
          justifyContent: "space-between",
        }}
      >
        <button
          onClick={handleDecrementClick}
          style={{
            flex: 1,
            padding: "6px 8px",
            backgroundColor: "#dc3545",
            color: "white",
            border: "none",
            borderRadius: "4px",
            cursor: "pointer",
            fontSize: "12px",
            fontWeight: "600",
          }}
          onMouseEnter={(e) =>
            (e.currentTarget.style.backgroundColor = "#c82333")
          }
          onMouseLeave={(e) =>
            (e.currentTarget.style.backgroundColor = "#dc3545")
          }
        >
          -
        </button>
        <button
          onClick={handleClearClick}
          style={{
            flex: 1,
            padding: "6px 8px",
            backgroundColor: "#6c757d",
            color: "white",
            border: "none",
            borderRadius: "4px",
            cursor: "pointer",
            fontSize: "12px",
            fontWeight: "600",
          }}
          onMouseEnter={(e) =>
            (e.currentTarget.style.backgroundColor = "#5a6268")
          }
          onMouseLeave={(e) =>
            (e.currentTarget.style.backgroundColor = "#6c757d")
          }
        >
          Clear
        </button>
        <button
          onClick={handleIncrementClick}
          style={{
            flex: 1,
            padding: "6px 8px",
            backgroundColor: "#28a745",
            color: "white",
            border: "none",
            borderRadius: "4px",
            cursor: "pointer",
            fontSize: "12px",
            fontWeight: "600",
          }}
          onMouseEnter={(e) =>
            (e.currentTarget.style.backgroundColor = "#218838")
          }
          onMouseLeave={(e) =>
            (e.currentTarget.style.backgroundColor = "#28a745")
          }
        >
          +
        </button>
      </div>
    </div>
  );
};

export default memo(CounterNode);
