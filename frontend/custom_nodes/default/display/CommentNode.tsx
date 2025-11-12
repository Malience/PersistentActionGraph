/* eslint-disable @typescript-eslint/no-explicit-any */
import { memo } from "react";
import CustomNode from "../../../src/nodes/CustomNode";
import TextComponent from "../../../src/components/TextComponent";

const CommentNode: CustomNode = ({ data, sync }) => {
  return (
    <TextComponent
      data={data}
      sync={sync}
      dataField="value"
      label=""
      placeholder="Enter text..."
      multiline={true}
      rows={4}
    />
  );
};

export default memo(CommentNode);
