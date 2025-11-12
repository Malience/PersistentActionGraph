
from nodes.NodeState import NodeState
from nodes.CustomNode import CustomNode
from FlowEngine import FlowEngine


class FloatNode(CustomNode):
    def __init__(self, _engine: FlowEngine, _id: str, _nodetype: str):
        super().__init__(_engine, _id, _nodetype, "Float")

        self.add_slot("output", "value", "float")
        self.data = {"value": 0.0}
    
    @staticmethod
    def route() -> str:
        return "primitives/float"
    
    async def data_pulled(self, slot):
        if slot == "value":
            await self.set_state(NodeState.DONE)
            return self.data["value"]