from nodes.CustomNode import CustomNode
from nodes.SlotType import ACTION, ACTION_PARAM
from FlowEngine import FlowEngine


class ActionDataNode(CustomNode):
    def __init__(self, _engine: FlowEngine, _id: str, _nodetype: str):
        super().__init__(_engine, _id, _nodetype, "Action Data")
        
        # Input slots: ACTION and any data
        self.add_slot("input", "action", ACTION)
        self.add_slot("input", "data", "any")
        
        # Output slot: ACTION_PARAM containing the data
        self.add_slot("output", "action_param", ACTION_PARAM)
    
    @staticmethod
    def route() -> str:
        return "utility/action_data"
    
    async def slot_activated(self, slot: str, params):
        if slot == "action":
            # When ACTION is activated, pull the data and activate ACTION_PARAM with it
            data = await self.pull_data("data")
            await self.activate_slot("action_param", data)