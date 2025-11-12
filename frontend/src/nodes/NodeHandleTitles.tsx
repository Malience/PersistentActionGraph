/* eslint-disable @typescript-eslint/no-explicit-any */
import { memo } from "react";
import type { Slot } from "./NodeContainer";
import { useConnection } from "@xyflow/react";
import {
  check_handle,
  get_source_handle,
  type ConnProps,
} from "./ConnectionContext";

type NHProps = {
  nodeid: string;
  input_slots: Slot[];
  output_slots: Slot[];
};

const enabled_color = "#999999";
const disabled_color = "#646464";

const input_enabled_style = { marginBottom: "5px", color: enabled_color };
const input_disabled_style = { marginBottom: "5px", color: disabled_color };

const output_enabled_style = {
  marginBottom: "5px",
  marginRight: "15px",
  color: enabled_color,
};
const output_disabled_style = {
  marginBottom: "5px",
  marginRight: "15px",
  color: disabled_color,
};

function NodeHandleTitles(props: NHProps) {
  const nodeid: string = props.nodeid;
  const input_slots: Slot[] = props.input_slots;
  const output_slots: Slot[] = props.output_slots;
  const disabled_slots = new Set();

  const connection = useConnection();

  const validate_slot = (slot: Slot, type: string, connContext: any) => {
    const conn: ConnProps = {
      nodeid: nodeid,
      handleid: slot.id,
      type: type,
      datatype: slot.datatype,
    };
    const connection_check = check_handle(connContext, conn);
    if (!connection_check) {
      disabled_slots.add(slot.id);
    }
  };

  if (connection.inProgress) {
    const source_handle = get_source_handle(connection) as ConnProps;
    for (const slot of input_slots) {
      validate_slot(slot, "target", source_handle);
    }
    for (const slot of output_slots) {
      validate_slot(slot, "source", source_handle);
    }
  } else {
    disabled_slots.clear();
  }

  return (
    <div
      style={{
        display: "grid",
        gridTemplateColumns: "1fr 1fr",
        gap: "12px",
        width: "100%",
        padding: "12px 8px",
      }}
    >
      <div style={{ textAlign: "left" }}>
        {input_slots.map((slot: Slot) => (
          <div
            key={slot.id}
            style={
              disabled_slots.has(slot.id)
                ? input_disabled_style
                : input_enabled_style
            }
          >
            {slot.id}
          </div>
        ))}
      </div>
      <div style={{ textAlign: "right" }}>
        {output_slots.map((slot: Slot) => (
          <div
            key={slot.id}
            style={
              disabled_slots.has(slot.id)
                ? output_disabled_style
                : output_enabled_style
            }
          >
            {slot.id}
          </div>
        ))}
      </div>
    </div>
  );
}

export default memo(NodeHandleTitles);
