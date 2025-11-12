from nodes.NodeState import NodeState
from nodes.CustomNode import CustomNode
from FlowEngine import FlowEngine


class ArrayMergeNode(CustomNode):
    def __init__(self, _engine: FlowEngine, _id: str, _nodetype: str):
        super().__init__(_engine, _id, _nodetype, "Array Merge")

        # Input slots for two arrays to merge
        self.add_slot("input", "array1", "any")
        self.add_slot("input", "array2", "any")
        
        # Output slot for merged array
        self.add_slot("output", "merged", "any")
        self.data = {}
    
    @staticmethod
    def route() -> str:
        return "utility/array_merge"
    
    async def data_pulled(self, slot):
        if slot == "merged":
            await self.set_state(NodeState.DONE)
            
            # Get input arrays
            array1 = await self.pull_data("array1")
            array2 = await self.pull_data("array2")
            
            # Handle None inputs
            if array1 is None:
                array1 = []
            if array2 is None:
                array2 = []
            
            # Ensure inputs are arrays
            if not isinstance(array1, list):
                array1 = [array1]
            if not isinstance(array2, list):
                array2 = [array2]
            
            # Merge arrays
            merged_array = array1 + array2
            return merged_array