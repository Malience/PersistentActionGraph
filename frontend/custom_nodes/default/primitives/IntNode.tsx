import { memo } from "react";
import CustomNode from "../../../src/nodes/CustomNode";
import NumberComponent from "../../../src/components/NumberComponent";

const IntNode: CustomNode = ({ data, sync }) => {
  return (
    <NumberComponent
      data={data}
      sync={sync}
      dataField="value"
      label="Value"
      step="1"
      min="-999999999"
      max="999999999"
    />
  );
};

export default memo(IntNode);
