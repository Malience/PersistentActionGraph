/* eslint-disable @typescript-eslint/no-explicit-any */
import { memo } from "react";
import CustomNode from "../../../src/nodes/CustomNode";
import TextComponent from "../../../src/components/TextComponent";

const JSONSearchNode: CustomNode = ({ data, sync }) => {
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
      {/* Search Criteria Section */}
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
        <div style={{ fontSize: "12px", fontWeight: "600" }}>
          Search Criteria
        </div>

        {/* Search Key Input */}
        <TextComponent
          data={data}
          sync={sync}
          dataField="search_key"
          label="Search Key"
          multiline={false}
          placeholder="Enter key to search for..."
        />

        {/* Search Value Input */}
        <TextComponent
          data={data}
          sync={sync}
          dataField="search_value"
          label="Search Value"
          multiline={false}
          placeholder="Enter value to match..."
        />
      </div>
    </div>
  );
};

export default memo(JSONSearchNode);
