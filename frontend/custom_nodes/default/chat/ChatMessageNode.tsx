import { memo } from "react";
import CustomNode from "../../../src/nodes/CustomNode";
import DropdownComponent from "../../../src/components/DropdownComponent";

const ChatMessageNode: CustomNode = ({ data, sync }) => {
  const roleOptions = [
    { value: "user", label: "User" },
    { value: "system", label: "System" },
    { value: "assistant", label: "Assistant" },
  ];

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        gap: "4px",
        padding: "8px",
      }}
    >
      <DropdownComponent
        data={data}
        sync={sync}
        dataField="role"
        label="Role"
        options={roleOptions}
        placeholder="Select role..."
      />
    </div>
  );
};

export default memo(ChatMessageNode);
