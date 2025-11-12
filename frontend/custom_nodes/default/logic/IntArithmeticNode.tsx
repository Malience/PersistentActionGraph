import { memo } from "react";
import CustomNode from "../../../src/nodes/CustomNode";
import DropdownComponent from "../../../src/components/DropdownComponent";

const IntArithmeticNode: CustomNode = ({ data, sync }) => {
  // Arithmetic operation options
  const arithmeticOptions = [
    { value: "add", label: "A + B" },
    { value: "subtract", label: "A - B" },
    { value: "multiply", label: "A × B" },
    { value: "divide", label: "A ÷ B" },
    { value: "modulo", label: "A % B" },
    { value: "power", label: "A ^ B" },
    { value: "min", label: "min(A, B)" },
    { value: "max", label: "max(A, B)" },
  ];

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        gap: "8px",
        padding: "8px",
      }}
    >
      {/* Arithmetic operation dropdown */}
      <DropdownComponent
        data={data}
        sync={sync}
        dataField="operation"
        label="Operation"
        options={arithmeticOptions}
      />
    </div>
  );
};

export default memo(IntArithmeticNode);
