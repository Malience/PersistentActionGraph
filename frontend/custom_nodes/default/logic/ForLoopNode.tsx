import { memo } from "react";
import CustomNode from "../../../src/nodes/CustomNode";
import NumberComponent from "../../../src/components/NumberComponent";

const ForLoopNode: CustomNode = ({ data, sync }) => {
  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        gap: "8px",
        padding: "8px",
        minWidth: "200px",
      }}
    >
      {/* Loop Count Input */}
      <NumberComponent
        data={data}
        sync={sync}
        dataField="loops"
        label="Loop Count"
        min="0"
        step="1"
        placeholder="Enter number of loops..."
      />
    </div>
  );
};

export default memo(ForLoopNode);
