from nodes.CustomNode import CustomNode
from nodes.NodeState import NodeState
from nodes.SlotType import ACTION_PARAM
from FlowEngine import FlowEngine


class ForEachNode(CustomNode):
    def __init__(self, _engine: FlowEngine, _id: str, _nodetype: str):
        super().__init__(_engine, _id, _nodetype, "For Each")

        # Input slots
        self.add_slot("input", "activate", ACTION_PARAM)
        self.add_slot("input", "array", "any")
        
        # Output slots
        self.add_slot("output", "act", ACTION_PARAM)
        self.add_slot("output", "element", "any")
        
        # Initialize data with default values
        self.data = {
            "_current_element": None
        }

    
    @staticmethod
    def route() -> str:
        return "logic/for_each"
    
    async def slot_activated(self, slot: str, params) -> None:
        if slot == "activate":
            await self.activate(params)
    
    async def data_pulled(self, slot):
        if slot == "element":
            return self.data["_current_element"]
    
    async def activate(self, params=None):
        await self.set_state(NodeState.PROCESSING)
        
        # Get array from input slot or fall back to params
        array_input = await self.pull_data("array")
        
        if array_input is not None:
            array = array_input
        else:
            # Use params as fallback
            array = params
        
        # Validate that we have an array
        if not isinstance(array, list):
            print(f"ERROR: Invalid array input: {array}")
            await self.set_state(NodeState.ERROR)
            return
        
        length = len(array)
        # Execute the loop through each element
        for i in range(length):
            element = array[i]

            # Set current element
            self.data["_current_element"] = element

            if i == length - 1:
                # Set state to DONE before the last activation
                await self.set_state(NodeState.DONE)
            
            # Activate the output slot with current element as params
            await self.activate_slot("act", element)
        