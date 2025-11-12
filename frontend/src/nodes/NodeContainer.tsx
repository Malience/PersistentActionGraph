/* eslint-disable @typescript-eslint/no-unused-vars */
/* eslint-disable @typescript-eslint/no-explicit-any */
import { NodeResizeControl, Position } from "@xyflow/react";
import { memo, Suspense, useCallback, useEffect, useState } from "react";
import CustomHandle from "./CustomHandle";
import type CustomNode from "./CustomNode";
import NodeHeader from "./NodeHeader";
import NodeHandleTitles from "./NodeHandleTitles";
import { useNodeSocket } from "../sockets/useNodeSocket";

// const customComponentURL = "../../custom_nodes/default/ButtonNode.tsx";
// const CComp: CustomComponent = lazy(() => import(customComponentURL));

const controlStyle = {
  background: "transparent",
  border: "none",
};

export type Slot = {
  id: string;
  datatype: string;
};

function NodeContainer(props: any) {
  const nodetype: string = props.data.nodetype;
  const input_slots: Slot[] = props.data.input_slots;
  const output_slots: Slot[] = props.data.output_slots;

  const label: string = props.data.label;
  const [data, setData] = useState<any>(props.data.data);
  const [nodeState, setNodeState] = useState<number>(0); // 0=NEUTRAL, 1=DONE, 2=PROCESSING, 3=ERROR

  const functions: any = props.data.functions;

  const socket = useNodeSocket();

  const calculate_min_height = () => {
    const maxsl =
      input_slots.length > output_slots.length
        ? input_slots.length
        : output_slots.length;

    return 40 + maxsl * 20;
  };
  const min_height = calculate_min_height();

  const calculate_min_width = () => {
    const char_len = 4;
    const padding = 20;
    const title_length = label.length * char_len;

    const find_longest_slot = (slot_list: Slot[]) => {
      let longest = 0;
      for (let i = 0; i < slot_list.length; i++) {
        const slot: Slot = slot_list[i];
        const len = slot.id.length;
        if (len > longest) {
          longest = len;
        }
      }
      return longest;
    };

    const longest_in = find_longest_slot(input_slots);
    const longest_out = find_longest_slot(output_slots);
    const total = (longest_in + longest_out) * char_len + padding;

    return Math.max(title_length, total, 100);
  };
  const min_width = calculate_min_width();

  const check_frontend_node: (node: string) => boolean =
    functions.check_frontend_node;
  const get_frontend_node: (node: string) => CustomNode =
    functions.get_frontend_node;

  let CustomComponent: CustomNode | null = null;
  CustomComponent = null;

  if (check_frontend_node(nodetype)) {
    CustomComponent = get_frontend_node(nodetype);
  }

  const sync = useCallback(
    async (data: any) => {
      if (!socket) return;
      const packet = {
        type: "sync",
        data: data,
      };
      socket.sendMessage(props.id, packet);
      setData(data);
    },
    [props.id, socket]
  );

  const sendSignal = useCallback(
    async (signal: string, params: any) => {
      if (!socket) return;
      const packet = {
        type: "signal",
        data: {
          signal: signal,
          params: params,
        },
      };
      socket.sendMessage(props.id, packet);
    },
    [props.id, socket]
  );

  const [signalCallback, setSignalCallback] = useState<
    ((signal: string, params: any) => void) | null
  >(null);

  // Create a stable setter function that can be passed to child components
  const handleSetSignalCallback = useCallback(
    (callback: (signal: string, params: any) => void) => {
      setSignalCallback(() => callback);
    },
    []
  );

  useEffect(() => {
    const handleSocket = (data: any) => {
      const type = data.type;
      const d = data.data;

      switch (type) {
        case "signal":
          if (signalCallback) {
            const signal = d.signal;
            const params = d.params;
            signalCallback(signal, params);
          }
          break;
        case "sync":
          setData(d);
          break;
        case "state": {
          const newState = d.state;
          setNodeState(newState);
          break;
        }
      }
    };
    socket.registerNodeHandler(props.id, handleSocket);

    return () => socket.unregisterNodeHandler(props.id);
  }, [props.id, signalCallback, socket]);

  // Get border color based on node state
  const getBorderStyle = () => {
    switch (nodeState) {
      case 1: // DONE
        return { border: "2px solid #00ff00" };
      case 2: // PROCESSING
        return { border: "2px solid #ffff00" };
      case 3: // ERROR
        return { border: "2px solid #ff0000" };
      default: // NEUTRAL
        return { border: "2px solid transparent" };
    }
  };

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        // overflow: "hidden",
        borderRadius: "2px",
        backgroundColor: "#353535",
        minHeight: min_height,
        minWidth: min_width,
        ...getBorderStyle(),
        transition: "border-color 1s ease-out",
      }}
    >
      <div className="handles targets">
        {input_slots.map((slot: Slot, i: number) => (
          <CustomHandle
            nodeid={props.id}
            key={slot.id}
            id={slot.id}
            datatype={slot.datatype}
            type="target"
            position={Position.Left}
            max_connections={1}
            style={{ top: `${i * 20 + 40}px` }}
          />
        ))}
      </div>
      <div className="handles sources">
        {output_slots.map((slot: Slot, i: number) => (
          <CustomHandle
            key={slot.id}
            id={slot.id}
            datatype={slot.datatype}
            type="source"
            position={Position.Right}
            max_connections={1}
            style={{ top: `${i * 20 + 40}px` }}
          />
        ))}
      </div>
      <NodeHeader color={"#333333"} label={label} />

      <NodeHandleTitles
        nodeid={props.id}
        input_slots={input_slots}
        output_slots={output_slots}
      />

      {CustomComponent ? (
        <Suspense fallback={<div>Loading...</div>}>
          <div
            className="nodrag"
            style={{
              height: "100%",
              width: "100%",
              display: "flex",
              flexDirection: "column",
            }}
          >
            <CustomComponent
              data={data}
              sync={sync}
              sendSignal={sendSignal}
              setSignalCallback={handleSetSignalCallback}
            />
          </div>
        </Suspense>
      ) : (
        <div />
      )}
      <NodeResizeControl
        style={controlStyle}
        minWidth={min_width}
        minHeight={min_height}
      />
    </div>
    // <div style={{ justifyContent: "top", alignItems: "top" }}>
    //   {/* <div style={{ height: "50%", backgroundColor: "gray" }}>{label}</div> */}
    //   <NodeHeader color={"gray"} label={label} />

    //   <div style={{ height: "50%", backgroundColor: "green" }}>
    //     <div className="handles targets">
    //       <CustomHandle
    //         key="a"
    //         id="a"
    //         type="target"
    //         position={Position.Left}
    //         max_connections={1}
    //         style={{ top: "30%" }}
    //       />
    //       <CustomHandle
    //         key="b"
    //         id="b"
    //         type="target"
    //         position={Position.Left}
    //         max_connections={1}
    //         style={{ top: "70%" }}
    //       />
    //     </div>
    //     <div>test</div>
    //     {CustomComponent ? (
    //       <Suspense fallback={<div>Loading...</div>}>
    //         <CustomComponent
    //           data={data}
    //           updateData={updateData}
    //           sendSignal={sendSignal}
    //         />
    //       </Suspense>
    //     ) : (
    //       <div />
    //     )}

    //     <div className="handles sources">
    //       <CustomHandle
    //         key="c"
    //         id="c"
    //         type="source"
    //         position={Position.Right}
    //         max_connections={1}
    //         style={{ top: "30%" }}
    //       >
    //         Hi!
    //       </CustomHandle>
    //       <CustomHandle
    //         key="d"
    //         id="d"
    //         type="source"
    //         position={Position.Right}
    //         max_connections={1}
    //         style={{ top: "70%" }}
    //       />
    //     </div>
    //     <NodeResizeControl style={controlStyle} minWidth={100} minHeight={50} />
    //   </div>
    // </div>
  );
}

export default memo(NodeContainer);
