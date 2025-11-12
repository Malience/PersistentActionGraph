from nodes.CustomNode import CustomNode
from nodes.SlotType import ACTION, ACTION_PARAM
from FlowEngine import FlowEngine


class SlotActivatedNode(CustomNode):
    def __init__(self, _engine: FlowEngine, _id: str, _nodetype: str):
        super().__init__(_engine, _id, _nodetype, "Slot Activated")

        # Input slot of type ACTION_PARAM for the slot activation
        self.add_slot("input", "in", ACTION_PARAM)
        
        # Output slots in the specified order:
        self.add_slot("output", "pre", ACTION)
        self.add_slot("output", "out", ACTION_PARAM)
        self.add_slot("output", "post", ACTION)
    
    @staticmethod
    def route() -> str:
        return "logic/slot_activated"
    
    async def slot_activated(self, slot: str, params):
        # When the input slot is activated, trigger the sequence
        if slot == "in":
            # First trigger preSlotActivated action
            await self.activate_slot("pre")
            
            # Then activate the output slot with the same parameters
            await self.activate_slot("out", params)
            
            # Finally trigger postSlotActivated action
            await self.activate_slot("post")