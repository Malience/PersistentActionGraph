import { memo } from "react";
import CustomNode from "../../../src/nodes/CustomNode";
import TextComponent from "../../../src/components/TextComponent";

const DiceRollerNode: CustomNode = ({ data, sync, sendSignal }) => {
  const lastResult = data?._result || 0;

  const handleRollClick = () => {
    // Send signal to backend to roll the dice
    sendSignal("roll", "");
  };

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        gap: "8px",
        padding: "12px",
        minWidth: "64px",
      }}
    >
      {/* Dice String Input */}
      <TextComponent
        data={data}
        sync={sync}
        dataField="dice_string"
        label="Dice String"
        multiline={false}
        placeholder="e.g., 1d6, 2d10+1d4+3"
      />

      {/* Roll Button */}
      <button
        onClick={handleRollClick}
        style={{
          padding: "8px 12px",
          backgroundColor: "#007bff",
          color: "white",
          border: "none",
          borderRadius: "4px",
          cursor: "pointer",
          fontSize: "12px",
          fontWeight: "600",
        }}
        onMouseEnter={(e) =>
          (e.currentTarget.style.backgroundColor = "#0056b3")
        }
        onMouseLeave={(e) =>
          (e.currentTarget.style.backgroundColor = "#007bff")
        }
      >
        Roll Dice
      </button>

      {/* Last Roll Display */}
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
        <div style={{ fontSize: "12px", fontWeight: "600" }}>Last Roll</div>
        <div style={{ fontSize: "11px" }}>
          <strong>{lastResult}</strong>
        </div>
      </div>
    </div>
  );
};

export default memo(DiceRollerNode);
