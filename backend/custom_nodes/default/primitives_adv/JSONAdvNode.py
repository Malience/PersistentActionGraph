import json
from nodes.NodeState import NodeState
from nodes.CustomNode import CustomNode
from nodes.SlotType import ACTION, ACTION_PARAM
from FlowEngine import FlowEngine


class JSONAdvNode(CustomNode):
    def __init__(self, _engine: FlowEngine, _id: str, _nodetype: str):
        super().__init__(_engine, _id, _nodetype, "JSON (Advanced)")

        # Input slots
        self.add_slot("input", "set", ACTION_PARAM)
        self.add_slot("input", "clear", ACTION)
        
        # Output slots
        self.add_slot("output", "value", "json")
        self.data = {"value": ""}
    
    @staticmethod
    def route() -> str:
        return "primitives_adv/json_adv"
    
    async def slot_activated(self, slot: str, params) -> None:
        if slot == "set":
            await self.set_value(params)
        if slot == "clear":
            await self.set_value("")
    
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
    
    async def set_value(self, value):
        """Set the node's JSON value from external input."""
        if isinstance(value, dict):
            self.data["value"] = json.dumps(value)
            await self.sync()
            await self.set_state(NodeState.DONE)
            
        else:
            print(f"ERROR: Invalid value type for JSONAdvNode. Expected dict, got {type(value)}")
            await self.set_state(NodeState.ERROR)