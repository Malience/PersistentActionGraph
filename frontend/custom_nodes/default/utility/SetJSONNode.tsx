import { memo } from "react";
import CustomNode from "../../../src/nodes/CustomNode";
import TextComponent from "../../../src/components/TextComponent";

const SetJSONNode: CustomNode = ({ data, sync }) => {
  return (
    <TextComponent
      data={data}
      sync={sync}
      dataField="key"
      label="Key"
      placeholder="Enter key..."
      multiline={false}
    />
  );
};

export default memo(SetJSONNode);
