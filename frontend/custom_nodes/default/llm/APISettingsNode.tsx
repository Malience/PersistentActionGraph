import { memo } from "react";
import CustomNode from "../../../src/nodes/CustomNode";
import NumberComponent from "../../../src/components/NumberComponent";

const APISettingsNode: CustomNode = ({ data, sync }) => {
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
        dataField="temperature"
        label="Temperature"
        step="0.5"
        min="0"
        max="5"
      />

      <NumberComponent
        data={data}
        sync={sync}
        dataField="top_k"
        label="Top K"
        step="1"
        min="1"
        max="200"
      />

      <NumberComponent
        data={data}
        sync={sync}
        dataField="top_p"
        label="Top P"
        step="0.1"
        min="0"
        max="1"
      />

      <NumberComponent
        data={data}
        sync={sync}
        dataField="typical"
        label="Typical"
        step="0.1"
        min="0"
        max="1"
      />

      <NumberComponent
        data={data}
        sync={sync}
        dataField="top_a"
        label="Top A"
        step="0.1"
        min="0"
        max="1"
      />

      <NumberComponent
        data={data}
        sync={sync}
        dataField="tfs"
        label="TFS"
        step="0.1"
        min="0"
        max="1"
      />

      <NumberComponent
        data={data}
        sync={sync}
        dataField="rep_pen"
        label="Rep Pen"
        step="0.1"
        min="1"
        max="3"
      />

      <NumberComponent
        data={data}
        sync={sync}
        dataField="rep_pen_range"
        label="Rep Pen Range"
        step="1"
        min="-1"
        max="524288"
      />

      <NumberComponent
        data={data}
        sync={sync}
        dataField="rep_pen_slope"
        label="Rep Pen Slope"
        step="0.1"
        min="0"
        max="5"
      />
    </div>
  );
};

export default memo(APISettingsNode);
