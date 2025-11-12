import { memo } from "react";
import CustomNode from "../../../src/nodes/CustomNode";
import NumberComponent from "../../../src/components/NumberComponent";

const ChatGeneratorNode: CustomNode = ({ data, sync }) => {
  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        gap: "4px",
        padding: "8px",
      }}
    >
      <NumberComponent
        data={data}
        sync={sync}
        dataField="max_length"
        label="Length"
        step="1"
        min="1"
        max="4096"
      />

      <NumberComponent
        data={data}
        sync={sync}
        dataField="max_context_length"
        label="Context"
        step="1"
        min="64"
        max="32000"
      />
    </div>
  );
};

export default memo(ChatGeneratorNode);
