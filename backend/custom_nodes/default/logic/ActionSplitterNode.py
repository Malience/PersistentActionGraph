from nodes.CustomNode import CustomNode
from nodes.SlotType import ACTION_PARAM
from FlowEngine import FlowEngine


class ActionSplitterNode(CustomNode):
    def __init__(self, _engine: FlowEngine, _id: str, _nodetype: str):
        super().__init__(_engine, _id, _nodetype, "Action Splitter")

        # Input slot of type ACTION_PARAM
        self.add_slot("input", "in", ACTION_PARAM)
        
        # Three output slots of type ACTION_PARAM
        self.add_slot("output", "out1", ACTION_PARAM)
        self.add_slot("output", "out2", ACTION_PARAM)
        self.add_slot("output", "out3", ACTION_PARAM)
    
    @staticmethod
    def route() -> str:
        return "logic/action_splitter"
    
    async def slot_activated(self, slot: str, params):
        # When the input slot is activated, activate all three output slots
        if slot == "in":
            await self.activate_slot("out1", params)
            await self.activate_slot("out2", params)
            await self.activate_slot("out3", params)