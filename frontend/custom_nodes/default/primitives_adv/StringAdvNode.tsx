import { memo } from "react";
import CustomNode from "../../../src/nodes/CustomNode";
import TextComponent from "../../../src/components/TextComponent";

const StringAdvNode: CustomNode = ({ data, sync }) => {
  return (
    <TextComponent
      data={data}
      sync={sync}
      dataField="value"
      label="String"
      placeholder="Enter string..."
    />
  );
};

export default memo(StringAdvNode);
