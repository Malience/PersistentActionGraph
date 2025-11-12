from nodes.NodeState import NodeState
from nodes.CustomNode import CustomNode
from FlowEngine import FlowEngine


class ToArrayNode(CustomNode):
    def __init__(self, _engine: FlowEngine, _id: str, _nodetype: str):
        super().__init__(_engine, _id, _nodetype, "To Array")

        self.add_slot("input", "input", "any")
        self.add_slot("output", "output", "any")
        self.data = {}
    
    @staticmethod
    def route() -> str:
        return "utility/to_array"
    
    async def data_pulled(self, slot):
        if slot == "output":
            await self.set_state(NodeState.DONE)
            input_data = await self.pull_data("input")
            
            # Convert input to array
            if input_data is None:
                return None
            elif isinstance(input_data, list):
                return input_data
            else:
                return [input_data]