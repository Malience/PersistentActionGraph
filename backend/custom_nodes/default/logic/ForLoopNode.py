from nodes.CustomNode import CustomNode
from nodes.NodeState import NodeState
from nodes.SlotType import ACTION, ACTION_PARAM
from FlowEngine import FlowEngine


class ForLoopNode(CustomNode):
    def __init__(self, _engine: FlowEngine, _id: str, _nodetype: str):
        super().__init__(_engine, _id, _nodetype, "For Loop")

        # Input slots
        self.add_slot("input", "activate", ACTION)
        self.add_slot("input", "loops", "int")
        
        # Output slots
        self.add_slot("output", "act", ACTION)
        self.add_slot("output", "index", "int")
        
        # Initialize data with default values
        self.data = {
            "loops": 1,
            "_current_index": 0
        }
    
    @staticmethod
    def route() -> str:
        return "logic/for_loop"
    
    async def slot_activated(self, slot: str, params) -> None:
        if slot == "activate":
            await self.activate(params)
    
    async def data_pulled(self, slot):
        if slot == "index":
            return self.data["_current_index"]
    
    async def activate(self, params=None):
        await self.set_state(NodeState.PROCESSING)
        
        # Get loop count from input slot or fall back to frontend data
        loops_input = await self.pull_data("loops")
        
        if loops_input is not None:
            loops = loops_input
        else:
            # Use frontend value as fallback
            loops = self.data.get("loops", 1)
        
        # Validate loops count
        if not isinstance(loops, int) or loops < 0:
            print(f"ERROR: Invalid loop count: {loops}")
            await self.set_state(NodeState.ERROR)
            return
        
        # Execute the loop
        for i in range(loops):
            # Set current index
            self.data["_current_index"] = i
            
            if i == loops -1:
                # Set state to DONE before the last activation
                await self.set_state(NodeState.DONE)

            # Activate the output slot with current index
            await self.activate_slot("act", i)
        