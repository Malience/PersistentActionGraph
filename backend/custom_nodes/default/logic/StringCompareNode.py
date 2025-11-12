from nodes.CustomNode import CustomNode
from nodes.NodeState import NodeState
from FlowEngine import FlowEngine


class StringCompareNode(CustomNode):
    def __init__(self, _engine: FlowEngine, _id: str, _nodetype: str):
        super().__init__(_engine, _id, _nodetype, "String Compare")
        
        # Input slots for two strings
        self.add_slot("input", "A", "string")
        self.add_slot("input", "B", "string")
        
        # Output slot for boolean result
        self.add_slot("output", "result", "bool")
    
    @staticmethod
    def route() -> str:
        return "logic/string_compare"
    
    async def data_pulled(self, slot):
        if slot == "result":
            a = await self.pull_data("A")
            if a is None: a = ""

            b = await self.pull_data("B")
            if b is None: b = ""

            # Perform string comparison
            result = a == b
            
            await self.set_state(NodeState.DONE)
            return result