import { memo } from "react";
import CustomNode from "../../../src/nodes/CustomNode";
import DropdownComponent from "../../../src/components/DropdownComponent";

const IntComparisonNode: CustomNode = ({ data, sync }) => {
  // Comparison operation options
  const comparisonOptions = [
    { value: "equals", label: "A = B" },
    { value: "not_equals", label: "A ≠ B" },
    { value: "greater_than", label: "A > B" },
    { value: "less_than", label: "A < B" },
    { value: "greater_than_or_equal", label: "A ≥ B" },
    { value: "less_than_or_equal", label: "A ≤ B" },
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
      {/* Comparison operation dropdown */}
      <DropdownComponent
        data={data}
        sync={sync}
        dataField="operation"
        label="Operation"
        options={comparisonOptions}
      />
    </div>
  );
};

export default memo(IntComparisonNode);
