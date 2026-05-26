/* eslint-disable @typescript-eslint/no-explicit-any */
import { memo } from "react";
import CustomNode from "../../../src/nodes/CustomNode";
import DropdownComponent from "../../../src/components/DropdownComponent";
import TextComponent from "../../../src/components/TextComponent";

const HTTPRequestNode: CustomNode = ({ data, sync, sendSignal }) => {
  const httpMethods = [
    { value: "GET", label: "GET" },
    { value: "POST", label: "POST" },
    { value: "PUT", label: "PUT" },
    { value: "DELETE", label: "DELETE" },
  ];

  const contentTypes = [
    { value: "", label: "" },
    { value: "text/plain", label: "text/plain" },
    { value: "application/json", label: "application/json" },
  ];

  const handleSendClick = () => {
    sendSignal("activate", null);
  };

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        gap: "8px",
        padding: "8px",
      }}
    >
      {/* URL Input */}
      <TextComponent
        data={data}
        sync={sync}
        dataField="url"
        label="URL"
        placeholder="Enter URL..."
        multiline={false}
      />

      {/* HTTP Method Dropdown */}
      <DropdownComponent
        data={data}
        sync={sync}
        dataField="method"
        label="Method"
        options={httpMethods}
      />

      {/* Content Type Dropdown */}
      <DropdownComponent
        data={data}
        sync={sync}
        dataField="content_type"
        label="Content Type"
        options={contentTypes}
      />

      {/* Body Text Area (only used when body input slot isn't connected) */}
      <TextComponent
        data={data}
        sync={sync}
        dataField="body_text"
        label="Body"
        placeholder="Enter request body..."
        multiline={true}
        rows={6}
      />

      {/* Send Button */}
      <button onClick={handleSendClick}>Send Request</button>
    </div>
  );
};

export default memo(HTTPRequestNode);
