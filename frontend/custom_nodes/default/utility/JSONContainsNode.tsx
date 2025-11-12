import { memo } from "react";
import CustomNode from "../../../src/nodes/CustomNode";
import TextComponent from "../../../src/components/TextComponent";

const JSONContainsNode: CustomNode = ({ data, sync }) => {
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
      {/* Key Input */}
      <TextComponent
        data={data}
        sync={sync}
        dataField="key"
        label="Key to Check"
        multiline={false}
        placeholder="Enter key name..."
      />
    </div>
  );
};

export default memo(JSONContainsNode);
