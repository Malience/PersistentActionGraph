from nodes.NodeState import NodeState
from nodes.CustomNode import CustomNode
from FlowEngine import FlowEngine
import json


class ToJSONNode(CustomNode):
    def __init__(self, _engine: FlowEngine, _id: str, _nodetype: str):
        super().__init__(_engine, _id, _nodetype, "To JSON")

        self.add_slot("input", "input", "any")
        self.add_slot("output", "output", "json")
        self.data = {}
    
    @staticmethod
    def route() -> str:
        return "utility/to_json"
    
    async def data_pulled(self, slot):
        if slot == "output":
            await self.set_state(NodeState.DONE)
            input_data = await self.pull_data("input")
            
            # Convert input to JSON
            if input_data is None:
                return None
            elif isinstance(input_data, str):
                try:
                    # If it's already a JSON string, parse it
                    return json.loads(input_data)
                except json.JSONDecodeError:
                    # If not valid JSON, return as string in JSON
                    return None
            else:
                # For any other type, return as-is (will be serialized to JSON)
                return input_data