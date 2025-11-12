import { memo } from "react";
import CustomNode from "../../../src/nodes/CustomNode";
import DropdownComponent from "../../../src/components/DropdownComponent";

const BooleanLogicNode: CustomNode = ({ data, sync }) => {
  const operationOptions = [
    { value: "and", label: "AND (A ∧ B)" },
    { value: "or", label: "OR (A ∨ B)" },
    { value: "xor", label: "XOR (A ⊕ B)" },
    { value: "nand", label: "NAND (¬(A ∧ B))" },
    { value: "nor", label: "NOR (¬(A ∨ B))" },
    { value: "xnor", label: "XNOR (A ≡ B)" },
    { value: "not_a", label: "NOT A (¬A)" },
    { value: "not_b", label: "NOT B (¬B)" },
    { value: "implies", label: "IMPLIES (A → B)" },
    { value: "a_only", label: "A ONLY (A ∧ ¬B)" },
    { value: "b_only", label: "B ONLY (¬A ∧ B)" },
    { value: "true", label: "TRUE" },
    { value: "false", label: "FALSE" },
  ];

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        gap: "8px",
        padding: "12px",
        minWidth: "200px",
      }}
    >
      {/* Operation Selection */}
      <DropdownComponent
        data={data}
        sync={sync}
        dataField="operation"
        label="Logic Operation"
        options={operationOptions}
      />
    </div>
  );
};

export default memo(BooleanLogicNode);
