/* eslint-disable @typescript-eslint/no-explicit-any */
import { memo } from "react";

export interface BooleanSwitchComponentProps {
  data: any;
  sync: (data: any) => void;
  dataField: string;
  label?: string;
  disabled?: boolean;
}

const BooleanSwitchComponent: React.FC<BooleanSwitchComponentProps> = ({
  data,
  sync,
  dataField,
  label = "Toggle",
  disabled = false,
}) => {
  const value = data[dataField] || false;

  const handleToggle = () => {
    if (!disabled) {
      const updatedData = { ...data, [dataField]: !value };
      sync(updatedData);
    }
  };

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "row",
        gap: "4px",
        padding: "4px, 8px",
      }}
    >
      <label
        style={{
          fontSize: "12px",
          fontWeight: "500",
          color: "#999999",
          alignContent: "center",
        }}
      >
        {label}
      </label>
      <div
        style={{
          display: "flex",
          alignItems: "center",
          cursor: disabled ? "not-allowed" : "pointer",
          opacity: disabled ? 0.6 : 1,
        }}
        onClick={handleToggle}
      >
        {/* Switch Container */}
        <div
          style={{
            width: "48px",
            height: "12px",
            borderRadius: "12px",
            backgroundColor: value ? "#007bff" : "#4a5568",
            position: "relative",
            transition: "background-color 0.2s ease",
            border: "1px solid",
            borderColor: value ? "#007bff" : "#718096",
          }}
        >
          {/* Switch Knob */}
          <div
            style={{
              width: "9px",
              height: "9px",
              borderRadius: "50%",
              backgroundColor: "white",
              position: "absolute",
              top: "2px",
              left: value ? "38px" : "2px",
              transition: "left 0.2s ease",
              boxShadow: "0 1px 3px rgba(0, 0, 0, 0.3)",
            }}
          />
        </div>
      </div>
    </div>
  );
};

export default memo(BooleanSwitchComponent);
