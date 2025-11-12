/* eslint-disable @typescript-eslint/no-explicit-any */
import { memo } from "react";
import type { ChangeEvent } from "react";

export interface DropdownComponentProps {
  data: any;
  sync: (data: any) => void;
  dataField: string;
  label?: string;
  options: Array<{ value: string; label: string }>;
  placeholder?: string;
}

const DropdownComponent: React.FC<DropdownComponentProps> = ({
  data,
  sync,
  dataField,
  label = "Select",
  options,
  placeholder,
}) => {
  function onChange(event: ChangeEvent<HTMLSelectElement>) {
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
      <select
        value={data[dataField] || ""}
        onChange={onChange}
        style={{
          width: "100%",
          background: "#222222",
          border: "1px solid #111",
          borderRadius: "4px",
          fontSize: "12px",
          color: "#ddd",
          padding: "2px 4px",
        }}
      >
        {placeholder && (
          <option value="" disabled>
            {placeholder}
          </option>
        )}
        {options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
    </div>
  );
};

export default memo(DropdownComponent);
