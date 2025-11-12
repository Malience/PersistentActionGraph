/* eslint-disable @typescript-eslint/no-explicit-any */
import { Handle, useConnection, useNodeConnections } from "@xyflow/react";
import {
  check_handle,
  get_source_handle,
  type ConnProps,
} from "./ConnectionContext";

export default function CustomHandle(props: any) {
  const nodeid = props.nodeid;
  const handleid = props.id;
  const type = props.type;
  const datatype = props.datatype;

  const connections = useNodeConnections({
    handleId: handleid,
    handleType: type,
  });
  const connection = useConnection();

  const startabble: boolean =
    connections.length < props.max_connections || props.type == "source";

  let endable = startabble;
  if (connection.inProgress) {
    const conn: ConnProps = {
      nodeid: nodeid,
      handleid: handleid,
      type: type,
      datatype: datatype,
    };
    const connHandle = get_source_handle(connection) as ConnProps;
    const connection_check = check_handle(connHandle, conn);
    endable = startabble && connection_check;
  }

  return (
    <Handle
      {...props}
      isConnectableStart={startabble}
      isConnectableEnd={endable}
    />
  );
}
