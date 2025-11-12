from nodes.CustomNode import CustomNode
from nodes.NodeState import NodeState
from FlowEngine import FlowEngine


class BooleanLogicNode(CustomNode):
    def __init__(self, _engine: FlowEngine, _id: str, _nodetype: str):
        super().__init__(_engine, _id, _nodetype, "Boolean Logic")
        
        # Input slots for two boolean values
        self.add_slot("input", "A", "bool")
        self.add_slot("input", "B", "bool")
        
        # Output slot for boolean result
        self.add_slot("output", "result", "bool")
        
        # Default data with logic operation
        self.data = {
            "operation": "and",
        }
    
    @staticmethod
    def route() -> str:
        return "logic/boolean_logic"
    
    async def data_pulled(self, slot):
        if slot == "result":
            a = await self.pull_data("A")
            if a is None: a = False

            b = await self.pull_data("B")
            if b is None: b = False

            operation = self.data.get("operation", "and")
            
            # Perform the logic operation based on the selected operation
            result = self._perform_logic(a, b, operation)
            
            await self.set_state(NodeState.DONE)
            return result
    
    def _perform_logic(self, a: bool, b: bool, operation: str) -> bool:
        """Perform the logic operation between two boolean values."""
        if operation == "and":
            return a and b
        elif operation == "or":
            return a or b
        elif operation == "xor":
            return a != b  # Exclusive OR
        elif operation == "nand":
            return not (a and b)
        elif operation == "nor":
            return not (a or b)
        elif operation == "xnor":
            return a == b  # Exclusive NOR (equivalence)
        elif operation == "not_a":
            return not a
        elif operation == "not_b":
            return not b
        elif operation == "implies":
            return (not a) or b  # A implies B
        elif operation == "a_only":
            return a and not b
        elif operation == "b_only":
            return not a and b
        elif operation == "true":
            return True
        elif operation == "false":
            return False
        else:
            # Default to AND if operation is unknown
            return False