from nodes.CustomNode import CustomNode
from nodes.NodeState import NodeState
from FlowEngine import FlowEngine


class IntComparisonNode(CustomNode):
    def __init__(self, _engine: FlowEngine, _id: str, _nodetype: str):
        super().__init__(_engine, _id, _nodetype, "Int Comparison")
        
        # Input slots for two integers
        self.add_slot("input", "A", "int")
        self.add_slot("input", "B", "int")
        
        # Output slot for boolean result
        self.add_slot("output", "result", "bool")
        
        # Default data with comparison operation
        self.data = {
            "operation": "equals",
        }
    
    @staticmethod
    def route() -> str:
        return "logic/int_comparison"
    
    async def data_pulled(self, slot):
        if slot == "result":
            a = await self.pull_data("A")
            if a is None: a = 0

            b = await self.pull_data("B")
            if b is None: b = 0

            operation = self.data.get("operation", "equals")
            
            # Perform the comparison based on the selected operation
            result = self._perform_comparison(a, b, operation)
            
            await self.set_state(NodeState.DONE)
            return result
    
    def _perform_comparison(self, a: int, b: int, operation: str) -> bool:
        """Perform the comparison operation between two integers."""
        if operation == "equals":
            return a == b
        elif operation == "not_equals":
            return a != b
        elif operation == "greater_than":
            return a > b
        elif operation == "less_than":
            return a < b
        elif operation == "greater_than_or_equal":
            return a >= b
        elif operation == "less_than_or_equal":
            return a <= b
        else:
            # Default to equals if operation is unknown
            return a == b