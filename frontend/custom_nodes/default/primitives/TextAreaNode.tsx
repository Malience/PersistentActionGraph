import { memo } from "react";
import CustomNode from "../../../src/nodes/CustomNode";
import TextComponent from "../../../src/components/TextComponent";

const TextAreaNode: CustomNode = ({ data, sync }) => {
  return (
    <TextComponent
      data={data}
      sync={sync}
      dataField="value"
      label="Text"
      placeholder="Enter text..."
      multiline={true}
      rows={4}
    />
  );
};

export default memo(TextAreaNode);
