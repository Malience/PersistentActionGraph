/* eslint-disable @typescript-eslint/no-explicit-any */
import { memo } from "react";
import type { ChangeEvent } from "react";

export interface NumberComponentProps {
  data: any;
  sync: (data: any) => void;
  dataField: string;
  label?: string;
  step?: number | string;
  min?: number | string;
  max?: number | string;
  placeholder?: string;
}

const NumberComponent: React.FC<NumberComponentProps> = ({
  data,
  sync,
  dataField,
  label = "Value",
  step = 1,
  min = "-999999999",
  max = "999999999",
  placeholder,
}) => {
  function onChange(event: ChangeEvent<HTMLInputElement>) {
    const value = parseFloat(event.target.value);
    if (!isNaN(value)) {
      const updatedData = { ...data, [dataField]: value };
      sync(updatedData);
    }
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
      <input
        type="number"
        value={data[dataField] || 0}
        onChange={onChange}
        step={step}
        min={min}
        max={max}
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
    </div>
  );
};

export default memo(NumberComponent);
