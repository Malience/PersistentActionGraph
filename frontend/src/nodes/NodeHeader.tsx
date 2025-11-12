/* eslint-disable @typescript-eslint/no-explicit-any */
import { memo } from "react";

type HeaderProps = {
  color: any;
  label: string;
};

function NodeHeader(props: HeaderProps) {
  return (
    <div
      style={{
        backgroundColor: props.color,
        height: "20px",
        borderTopLeftRadius: "2px",
        borderTopRightRadius: "2px",
        boxShadow: "0px 0px 1px rgba(0, 0, 0, 0.5)",
      }}
    >
      <div
        style={{
          height: "100%",
          width: "100%",
          margin: "auto",
          paddingTop: "2px",
          paddingLeft: "15px",
          textAlign: "left",
          color: "#999999",
        }}
      >
        {props.label}
      </div>
    </div>
  );
}

export default memo(NodeHeader);
