from nodes.NodeState import NodeState
from nodes.CustomNode import CustomNode
from FlowEngine import FlowEngine
import json


class ToStringNode(CustomNode):
    def __init__(self, _engine: FlowEngine, _id: str, _nodetype: str):
        super().__init__(_engine, _id, _nodetype, "To String")

        self.add_slot("input", "input", "any")
        self.add_slot("output", "output", "string")
        self.data = {}
    
    @staticmethod
    def route() -> str:
        return "utility/to_string"
    
    async def data_pulled(self, slot):
        if slot == "output":
            await self.set_state(NodeState.DONE)
            input_data = await self.pull_data("input")
            
            # Convert input to string
            if input_data is None:
                return None
            elif isinstance(input_data, str):
                return input_data
            else:
                # For any other type, convert to string
                try:
                    # Try to convert to JSON string for complex objects
                    return json.dumps(input_data)
                except:
                    # Fall back to regular string conversion
                    return str(input_data)