/* eslint-disable @typescript-eslint/no-explicit-any */
import { memo } from "react";
import CustomNode from "../../../src/nodes/CustomNode";
import DropdownComponent from "../../../src/components/DropdownComponent";
import TextComponent from "../../../src/components/TextComponent";

const HTTPEndpointNode: CustomNode = ({ data, sync, sendSignal }) => {
  const httpMethods = [
    { value: "GET", label: "GET" },
    { value: "POST", label: "POST" },
    { value: "PUT", label: "PUT" },
    { value: "DELETE", label: "DELETE" },
  ];

  const responseTypes = [
    { value: "File", label: "File" },
    { value: "HTML", label: "HTML" },
    { value: "JSON", label: "JSON" },
    { value: "Plain Text", label: "Plain Text" },
  ];

  const handleSetEndpointClick = () => {
    sendSignal("set_endpoint", null);
    sendSignal("sync", null);
  };

  const handleDataChange = (data: any) => {
    sync(data);
    // Remove the last endpoint if the data changes
    // sendSignal("remove_endpoint", null);
    // Hacky way to get the indicator to update
    sendSignal("sync", null);
  };

  const isEndpointSet =
    data?._endpoint !== undefined && data?._endpoint !== null;

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        gap: "8px",
        padding: "8px",
      }}
    >
      {/* Path Input */}
      <TextComponent
        data={data}
        sync={handleDataChange}
        dataField="path"
        label="Path"
        placeholder=""
        multiline={false}
      />

      {/* HTTP Method Dropdown */}
      <DropdownComponent
        data={data}
        sync={handleDataChange}
        dataField="method"
        label="Method"
        options={httpMethods}
      />

      {/* Response Type Dropdown */}
      <DropdownComponent
        data={data}
        sync={handleDataChange}
        dataField="response_type"
        label="Response Type"
        options={responseTypes}
      />

      {/* Status Display */}
      <div
        style={{
          padding: "4px 8px",
          borderRadius: "4px",
          backgroundColor: isEndpointSet ? "#d4edda" : "#f8d7da",
          color: isEndpointSet ? "#155724" : "#721c24",
          fontSize: "12px",
          fontWeight: "bold",
        }}
      >
        {isEndpointSet ? "✓ Endpoint Active" : "✗ Endpoint Not Set"}
      </div>

      {/* Set/Remove Endpoint Buttons */}
      <div style={{ display: "flex", gap: "8px" }}>
        <button
          onClick={handleSetEndpointClick}
          style={{
            flex: 1,
            backgroundColor: "#007bff",
            color: "white",
            border: "none",
            padding: "6px 12px",
            borderRadius: "4px",
            cursor: "pointer",
          }}
        >
          Set Endpoint
        </button>
      </div>

      {/* Endpoint URL Display */}
      {isEndpointSet && (
        <div
          style={{
            padding: "8px",
            backgroundColor: "#f8f9fa",
            borderRadius: "4px",
            fontSize: "12px",
            border: "1px solid #dee2e6",
          }}
        >
          <div style={{ fontWeight: "bold", marginBottom: "4px" }}>
            Active Endpoint:
          </div>
          <div style={{ fontFamily: "monospace" }}>
            {data?.method || "GET"} {data?._endpoint || ""}
          </div>
          <div style={{ fontSize: "10px", color: "#6c757d", marginTop: "4px" }}>
            Access at: http://localhost:8000{data?._endpoint || ""}
          </div>
        </div>
      )}
    </div>
  );
};

export default memo(HTTPEndpointNode);
