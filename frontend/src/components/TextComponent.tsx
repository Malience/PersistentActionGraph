/* eslint-disable @typescript-eslint/no-explicit-any */
import { memo } from "react";
import type { ChangeEvent } from "react";

export interface TextComponentProps {
  data: any;
  sync: (data: any) => void;
  dataField: string;
  label?: string;
  placeholder?: string;
  multiline?: boolean;
  rows?: number;
}

const TextComponent: React.FC<TextComponentProps> = ({
  data,
  sync,
  dataField,
  label = "Text",
  placeholder,
  multiline = false,
  rows = 3,
}) => {
  function onChange(
    event: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) {
    const value = event.target.value;
    const updatedData = { ...data, [dataField]: value };
    sync(updatedData);
  }

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "row",
        gap: "4px",
        padding: "4px, 8px",
      }}
    >
      <label
        style={{
          fontSize: "12px",
          fontWeight: "500",
          color: "#999999",
          alignContent: "center",
        }}
      >
        {label}
      </label>
      {multiline ? (
        <textarea
          value={data[dataField] || ""}
          onChange={onChange}
          placeholder={placeholder}
          rows={rows}
          style={{
            width: "100%",
            background: "#222222",
            border: "1px solid #111",
            borderRadius: "4px",
            fontSize: "12px",
            color: "#ddd",
            resize: "vertical",
            fontFamily: "inherit",
          }}
        />
      ) : (
        <input
          type="text"
          value={data[dataField] || ""}
          onChange={onChange}
          placeholder={placeholder}
          style={{
            width: "100%",
            background: "#222222",
            border: "1px solid #111",
            borderRadius: "4px",
            fontSize: "12px",
            color: "#ddd",
          }}
        />
      )}
    </div>
  );
};

export default memo(TextComponent);
