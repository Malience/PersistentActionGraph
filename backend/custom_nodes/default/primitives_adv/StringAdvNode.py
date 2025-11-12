from nodes.NodeState import NodeState
from nodes.CustomNode import CustomNode
from nodes.SlotType import ACTION, ACTION_PARAM
from FlowEngine import FlowEngine


class StringAdvNode(CustomNode):
    def __init__(self, _engine: FlowEngine, _id: str, _nodetype: str):
        super().__init__(_engine, _id, _nodetype, "String (Advanced)")

        # Input slots
        self.add_slot("input", "set", ACTION_PARAM)
        
        # Output slots
        self.add_slot("output", "value", "string")
        self.data = {"value": ""}
    
    @staticmethod
    def route() -> str:
        return "primitives_adv/string"
    
    async def slot_activated(self, slot: str, params) -> None:
        if slot == "set":
            await self.set_value(params)
        if slot == "clear":
            await self.set_value("")
    
    async def data_pulled(self, slot):
        if slot == "value":
            await self.set_state(NodeState.DONE)
            return self.data["value"]
    
    async def set_value(self, value):
        """Set the node's value from external input."""
        if isinstance(value, str):
            self.data["value"] = value
            await self.sync()
            await self.set_state(NodeState.DONE)
        else:
            print(f"ERROR: Invalid value type for StringAdvNode. Expected string, got {type(value)}")
            await self.set_state(NodeState.ERROR)