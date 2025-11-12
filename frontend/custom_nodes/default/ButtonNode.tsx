import { memo } from "react";
import CustomNode from "../../src/nodes/CustomNode";

const ButtonNode: CustomNode = ({ data, sendSignal }) => {
  function onClick() {
    sendSignal("button_pressed", "");
  }

  return <button onClick={onClick}>{data["button_label"]}</button>;
};

export default memo(ButtonNode);
