from nodes.NodeState import NodeState
from nodes.CustomNode import CustomNode
from FlowEngine import FlowEngine


class RerouteNode(CustomNode):
    def __init__(self, _engine: FlowEngine, _id: str, _nodetype: str):
        super().__init__(_engine, _id, _nodetype, "Reroute")

        self.add_slot("input", "input", "any")
        self.add_slot("output", "output", "any")
        self.data = {}
    
    @staticmethod
    def route() -> str:
        return "utility/reroute"
    
    async def data_pulled(self, slot):
        if slot == "output":
            await self.set_state(NodeState.DONE)
            return await self.pull_data("input")
    
    async def slot_activated(self, slot, params):
        if slot == "input":
            await self.set_state(NodeState.DONE)
            await self.activate_slot("output", params)