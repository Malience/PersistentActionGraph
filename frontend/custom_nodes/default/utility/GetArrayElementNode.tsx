import { memo } from "react";
import CustomNode from "../../../src/nodes/CustomNode";
import NumberComponent from "../../../src/components/NumberComponent";

const GetArrayElementNode: CustomNode = ({ data, sync }) => {
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
        dataField="index"
        label="Index"
        step="1"
        min="0"
        max="1000"
      />
    </div>
  );
};

export default memo(GetArrayElementNode);
