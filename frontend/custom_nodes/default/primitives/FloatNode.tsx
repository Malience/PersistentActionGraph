import { memo } from "react";
import CustomNode from "../../../src/nodes/CustomNode";
import NumberComponent from "../../../src/components/NumberComponent";

const FloatNode: CustomNode = ({ data, sync }) => {
  return (
    <NumberComponent
      data={data}
      sync={sync}
      dataField="value"
      label="Value"
      step="0.1"
      min="-999999999"
      max="999999999"
    />
  );
};

export default memo(FloatNode);
