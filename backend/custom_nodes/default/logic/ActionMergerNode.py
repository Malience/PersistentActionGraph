from nodes.CustomNode import CustomNode
from nodes.SlotType import ACTION_PARAM
from FlowEngine import FlowEngine


class ActionMergerNode(CustomNode):
    def __init__(self, _engine: FlowEngine, _id: str, _nodetype: str):
        super().__init__(_engine, _id, _nodetype, "Action Merger")

        # Three input slots of type ACTION_PARAM
        self.add_slot("input", "in1", ACTION_PARAM)
        self.add_slot("input", "in2", ACTION_PARAM)
        self.add_slot("input", "in3", ACTION_PARAM)
        
        # One output slot of type ACTION_PARAM
        self.add_slot("output", "out", ACTION_PARAM)
    
    @staticmethod
    def route() -> str:
        return "logic/action_merger"
    
    async def slot_activated(self, slot: str, params):
        # When any of the input slots are activated, activate the output slot
        if slot in ["in1", "in2", "in3"]:
            await self.activate_slot("out", params)