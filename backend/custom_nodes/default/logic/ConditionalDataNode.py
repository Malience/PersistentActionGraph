from nodes.CustomNode import CustomNode
from nodes.NodeState import NodeState
from FlowEngine import FlowEngine


class ConditionalDataNode(CustomNode):
    def __init__(self, _engine: FlowEngine, _id: str, _nodetype: str):
        super().__init__(_engine, _id, _nodetype, "Conditional Data")
        
        # Input slots: condition, true path data, false path data
        self.add_slot("input", "condition", "bool")
        self.add_slot("input", "true", "any")
        self.add_slot("input", "false", "any")
        
        # Output slot for conditional data
        self.add_slot("output", "value", "any")
    
    @staticmethod
    def route() -> str:
        return "logic/conditional_data"
    
    async def data_pulled(self, slot: str):
        if slot == "value":
            await self.set_state(NodeState.PROCESSING)

            # Pull the condition value
            cond = await self.pull_data("condition")
            
            # Based on condition, pull data from true or false path
            if cond:
                data = await self.pull_data("true")
            else:
                data = await self.pull_data("false")
            
            await self.set_state(NodeState.DONE)
            return data
        
        return None