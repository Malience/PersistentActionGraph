from nodes.CustomNode import CustomNode
from FlowEngine import FlowEngine


class PriorityDataNode(CustomNode):
    def __init__(self, _engine: FlowEngine, _id: str, _nodetype: str):
        super().__init__(_engine, _id, _nodetype, "Priority Data")

        # Three input slots of type "any" for priority-based data pulling
        self.add_slot("input", "in1", "any")
        self.add_slot("input", "in2", "any")
        self.add_slot("input", "in3", "any")
        
        # One output slot of type "any"
        self.add_slot("output", "out", "any")
    
    @staticmethod
    def route() -> str:
        return "logic/priority_data"
    
    async def data_pulled(self, slot: str):
        # When data is pulled from the output slot, try inputs in priority order
        if slot == "out":
            # Try in1 first
            data = await self.pull_data("in1")
            if data is not None:
                return data
            
            # If in1 returned None, try in2
            data = await self.pull_data("in2")
            if data is not None:
                return data
            
            # If in2 returned None, try in3
            data = await self.pull_data("in3")
            if data is not None:
                return data
            
            # If all inputs returned None, return None
            return None
        
        return None