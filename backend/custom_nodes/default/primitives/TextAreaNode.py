
from nodes.NodeState import NodeState
from nodes.CustomNode import CustomNode
from FlowEngine import FlowEngine


class TextAreaNode(CustomNode):
    def __init__(self, _engine: FlowEngine, _id: str, _nodetype: str):
        super().__init__(_engine, _id, _nodetype, "TextArea")

        self.add_slot("output", "value", "string")
        self.data = {"value": ""}
    
    @staticmethod
    def route() -> str:
        return "primitives/textarea"
    
    async def data_pulled(self, slot):
        if slot == "value":
            await self.set_state(NodeState.DONE)
            return self.data["value"]