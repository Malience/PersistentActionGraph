from nodes.CustomNode import CustomNode
from nodes.NodeState import NodeState
from FlowEngine import FlowEngine


class IntArithmeticNode(CustomNode):
    def __init__(self, _engine: FlowEngine, _id: str, _nodetype: str):
        super().__init__(_engine, _id, _nodetype, "Int Arithmetic")
        
        # Input slots for two integers
        self.add_slot("input", "A", "int")
        self.add_slot("input", "B", "int")
        
        # Output slot for integer result
        self.add_slot("output", "result", "int")
        
        # Default data with arithmetic operation
        self.data = {
            "operation": "add",
        }
    
    @staticmethod
    def route() -> str:
        return "logic/int_arithmetic"
    
    async def data_pulled(self, slot):
        if slot == "result":
            a = await self.pull_data("A")
            if a is None: a = 0

            b = await self.pull_data("B")
            if b is None: b = 0

            operation = self.data.get("operation", "add")
            
            # Perform the arithmetic operation based on the selected operation
            result = self._perform_arithmetic(a, b, operation)
            
            await self.set_state(NodeState.DONE)
            return result
    
    def _perform_arithmetic(self, a: int, b: int, operation: str) -> int:
        """Perform the arithmetic operation between two integers."""
        if operation == "add":
            return a + b
        elif operation == "subtract":
            return a - b
        elif operation == "multiply":
            return a * b
        elif operation == "divide":
            # Handle division by zero
            if b == 0:
                return 0
            return a // b  # Integer division
        elif operation == "modulo":
            # Handle modulo by zero
            if b == 0:
                return 0
            return a % b
        elif operation == "power":
            return a ** b
        elif operation == "min":
            return min(a, b)
        elif operation == "max":
            return max(a, b)
        else:
            # Default to addition if operation is unknown
            return a + b