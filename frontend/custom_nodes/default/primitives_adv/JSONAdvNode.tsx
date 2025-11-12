import { memo, useState, useEffect } from "react";
import CustomNode from "../../../src/nodes/CustomNode";
import TextComponent from "../../../src/components/TextComponent";

const JSONAdvNode: CustomNode = ({ data, sync }) => {
  const [isValidJSON, setIsValidJSON] = useState(true);

  useEffect(() => {
    // Validate JSON whenever the value changes
    if (data.value) {
      try {
        JSON.parse(data.value);
        setIsValidJSON(true);
      } catch {
        setIsValidJSON(false);
      }
    } else {
      // Empty string is considered valid (will output empty object)
      setIsValidJSON(true);
    }
  }, [data.value]);

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        gap: "4px",
        padding: "8px",
      }}
    >
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: "8px",
          marginBottom: "4px",
        }}
      >
        <span style={{ fontSize: "12px", fontWeight: "bold" }}>
          JSON Valid:
        </span>
        <div
          style={{
            width: "12px",
            height: "12px",
            borderRadius: "50%",
            backgroundColor: isValidJSON ? "#4CAF50" : "#F44336",
            border: "1px solid #ccc",
            flexShrink: 0,
          }}
          title={isValidJSON ? "Valid JSON" : "Invalid JSON"}
        />
        <span
          style={{
            fontSize: "10px",
            color: isValidJSON ? "#4CAF50" : "#F44336",
          }}
        >
          {isValidJSON ? "Valid" : "Invalid"}
        </span>
      </div>
      <TextComponent
        data={data}
        sync={sync}
        dataField="value"
        label="JSON"
        multiline={true}
        rows={6}
      />
    </div>
  );
};

export default memo(JSONAdvNode);
