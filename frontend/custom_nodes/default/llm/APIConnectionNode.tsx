import { memo } from "react";
import CustomNode from "../../../src/nodes/CustomNode";
import TextComponent from "../../../src/components/TextComponent";

const APIConnectionNode: CustomNode = ({ data, sync }) => {
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
        dataField="api_url"
        label="API URL"
        placeholder="Enter API URL..."
        multiline={false}
      />
      <TextComponent
        data={data}
        sync={sync}
        dataField="api_key"
        label="API Key"
        placeholder="Enter API Key..."
        multiline={false}
      />
      <TextComponent
        data={data}
        sync={sync}
        dataField="model"
        label="Model"
        placeholder="Enter Model Name..."
        multiline={false}
      />
    </div>
  );
};

export default memo(APIConnectionNode);
