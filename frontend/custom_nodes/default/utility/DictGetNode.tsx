import { memo } from "react";
import CustomNode from "../../../src/nodes/CustomNode";
import TextComponent from "../../../src/components/TextComponent";

const DictGetNode: CustomNode = ({ data, sync }) => {
  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        gap: "8px",
        padding: "8px",
      }}
    >
      {/* Key input for frontend fallback */}
      <TextComponent
        data={data}
        sync={sync}
        dataField="key"
        label="Key"
        multiline={false}
        placeholder="Enter dictionary key..."
      />
    </div>
  );
};

export default memo(DictGetNode);
