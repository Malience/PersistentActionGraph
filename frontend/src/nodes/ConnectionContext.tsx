import type { ConnectionState } from "@xyflow/react";
import { createContext } from "react";
import type { Slot } from "./NodeContainer";

export interface ConnProps {
  nodeid: string;
  handleid: string;
  type: string;
  datatype: string;
}

export const blankConn: ConnProps = {
  nodeid: "",
  handleid: "",
  type: "",
  datatype: "",
};

export const ConnectionContext = createContext<ConnProps>(blankConn);

export function get_source_handle(conn: ConnectionState) {
  const node = conn.fromNode;

  if (!node || !conn.fromHandle) {
    return null;
  }
  const type = conn.fromHandle.type;

  let slots: Slot[] = [];
  if (type == "source") {
    slots = conn.fromNode.data["output_slots"] as Slot[];
  } else if (type == "target") {
    slots = conn.fromNode.data["input_slots"] as Slot[];
  } else {
    console.log("Something went wrong.");
    return null;
  }

  const handleid = conn.fromHandle.id as string;

  let datatype = "";
  for (let i = 0; i < slots.length; i++) {
    if (slots[i].id == handleid) {
      datatype = slots[i].datatype;
    }
  }

  if (datatype == "") {
    console.log("Something wrong");
    return null;
  }

  const handle: ConnProps = {
    nodeid: node.id,
    handleid: handleid,
    type: type,
    datatype: datatype,
  };

  return handle;
}

export function check_handle(src_handle: ConnProps, tgt_handle: ConnProps) {
  // Target handle should always have non blank props
  if (tgt_handle == blankConn) {
    console.log("Target handle gave blank props: ", tgt_handle);
    return false;
  }

  // If there is no active connection then it is always available
  if (src_handle == blankConn) {
    return true;
  }

  // If it's the same handle
  if (
    src_handle.nodeid == tgt_handle.nodeid &&
    src_handle.handleid == tgt_handle.handleid
  ) {
    return true;
  }

  // Disable all other handles on the node to prevent recursion
  if (src_handle.nodeid == tgt_handle.nodeid) {
    return false;
  }

  // I don't want to deal with unknown handle types
  if (src_handle.type != "source" && src_handle.type != "target") {
    console.log("Unknown type on handle: ", src_handle);
    return false;
  }

  // Disable nodes of the same type, source => target only
  if (src_handle.type == tgt_handle.type) {
    return false;
  }

  // Handles must have the same datatype
  if (src_handle.datatype == tgt_handle.datatype) {
    return true;
  }

  // Exception for action types
  if (
    (src_handle.datatype == "action" ||
      src_handle.datatype == "action_param") &&
    (tgt_handle.datatype == "action" || tgt_handle.datatype == "action_param")
  ) {
    return true;
  }

  // Exception for any type
  if (src_handle.datatype == "any" || tgt_handle.datatype == "any") {
    return true;
  }

  return false;
}
