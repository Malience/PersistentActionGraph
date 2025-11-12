from nodes.NodeState import NodeState
from nodes.CustomNode import CustomNode
from FlowEngine import FlowEngine
import json


class JSONNode(CustomNode):
    def __init__(self, _engine: FlowEngine, _id: str, _nodetype: str):
        super().__init__(_engine, _id, _nodetype, "JSON")

        self.add_slot("output", "value", "json")
        self.data = {"value": ""}
    
    @staticmethod
    def route() -> str:
        return "primitives/json"
    
    async def data_pulled(self, slot):
        if slot == "value":
            await self.set_state(NodeState.DONE)
            try:
                # Convert text to JSON object
                if self.data["value"]:
                    return json.loads(self.data["value"])
                else:
                    return {}
            except json.JSONDecodeError:
                # Return empty object if JSON is invalid
                return {}