from nodes.CustomNode import CustomNode
from nodes.SlotType import ACTION_PARAM
from FlowEngine import FlowEngine
from nodes.NodeState import NodeState


class SequentialActivationNode(CustomNode):
    def __init__(self, _engine: FlowEngine, _id: str, _nodetype: str):
        super().__init__(_engine, _id, _nodetype, "Sequential Activation")
        
        # Input slot: action trigger
        self.add_slot("input", "action", ACTION_PARAM)
        
        # Output slots: three sequential actions
        self.add_slot("output", "out1", ACTION_PARAM)
        self.add_slot("output", "out2", ACTION_PARAM)
        self.add_slot("output", "out3", ACTION_PARAM)
    
    @staticmethod
    def route() -> str:
        return "logic/sequential_activation"
    
    async def slot_activated(self, slot: str, params):
        if slot == "action":
            await self.set_state(NodeState.DONE)

            # Activate outputs in order: first, then second, then third
            await self.activate_slot("out1", params)

            await self.activate_slot("out2", params)
            await self.activate_slot("out3", params)
