import { memo } from "react";
import CustomNode from "../../../src/nodes/CustomNode";
import TextComponent from "../../../src/components/TextComponent";

const ArraySliceNode: CustomNode = ({ data, sync }) => {
  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        gap: "4px",
        padding: "8px",
      }}
    >
      <TextComponent
        data={data}
        sync={sync}
        dataField="start"
        label="Start"
        placeholder="(optional)"
      />
      <TextComponent
        data={data}
        sync={sync}
        dataField="stop"
        label="Stop"
        placeholder="(optional)"
      />
      <TextComponent
        data={data}
        sync={sync}
        dataField="step"
        label="Step"
        placeholder="(optional)"
      />
    </div>
  );
};

export default memo(ArraySliceNode);
