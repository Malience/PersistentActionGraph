from nodes.NodeState import NodeState
from nodes.CustomNode import CustomNode
from nodes.SlotType import ACTION_PARAM
from FlowEngine import FlowEngine


class PullNode(CustomNode):
    def __init__(self, _engine: FlowEngine, _id: str, _nodetype: str):
        super().__init__(_engine, _id, _nodetype, "Pull")

        # Input slots
        self.add_slot("input", "activate", ACTION_PARAM)
        self.add_slot("input", "in", "any")
        
        # Output slot
        self.add_slot("output", "out", ACTION_PARAM)
        self.data = {}
    
    @staticmethod
    def route() -> str:
        return "utility/pull"
    
    async def slot_activated(self, slot: str, params) -> None:
        if slot == "activate":
            await self.pull_and_activate(params)
    
    async def pull_and_activate(self, params=None):
        """Pull data from input slot and activate output slot with the data."""
        await self.set_state(NodeState.PROCESSING)
        
        try:
            # Pull data from the "in" slot
            input_data = await self.pull_data("in")
            
            # Activate the output slot with the pulled data
            await self.activate_slot("out", input_data)
            
            await self.set_state(NodeState.DONE)
            
        except Exception as e:
            print(f"ERROR in PullNode: {e}")
            await self.set_state(NodeState.ERROR)