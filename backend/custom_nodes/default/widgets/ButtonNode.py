
from nodes.CustomNode import CustomNode
from nodes.NodeState import NodeState
from nodes.SlotType import ACTION
from FlowEngine import FlowEngine


class ButtonNode(CustomNode):
    def __init__(self, _engine: FlowEngine, _id: str, _nodetype: str):
        super().__init__(_engine, _id, _nodetype, "Button Node")

        self.add_slot("output", "pressed", ACTION)
        self.data = {"button_label": "Press!"}
    
    @staticmethod
    def route() -> str:
        return "widgets/button"

    async def receive_signal(self, signal: str, params):
        if signal =="button_pressed":
            await self.set_state(NodeState.DONE)
            await self.activate_slot("pressed")