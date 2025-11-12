from nodes.NodeState import NodeState
from nodes.CustomNode import CustomNode
from FlowEngine import FlowEngine


class ArraySliceNode(CustomNode):
    def __init__(self, _engine: FlowEngine, _id: str, _nodetype: str):
        super().__init__(_engine, _id, _nodetype, "Array Slice")

        # Input slot for the array to slice
        self.add_slot("input", "array", "any")
        
        # Output slot for the sliced array
        self.add_slot("output", "sliced", "any")
        
        # Initialize data with default slice parameters
        self.data = {
            "start": None,
            "stop": None,
            "step": None
        }
    
    @staticmethod
    def route() -> str:
        return "utility/array_slice"
    
    async def data_pulled(self, slot):
        if slot == "sliced":
            await self.set_state(NodeState.DONE)
            
            # Get input array
            array_data = await self.pull_data("array")
            
            # Check if input is an array
            if array_data is None or not isinstance(array_data, list):
                return None
            
            # Get slice parameters from data
            start = self.data.get("start")
            stop = self.data.get("stop")
            step = self.data.get("step")
            
            # Convert empty strings to None for Python slice behavior
            if start == "":
                start = None
            if stop == "":
                stop = None
            if step == "":
                step = None
            
            # Convert string numbers to integers if provided
            if start is not None and start != "":
                try:
                    start = int(start)
                except (ValueError, TypeError):
                    start = None
            
            if stop is not None and stop != "":
                try:
                    stop = int(stop)
                except (ValueError, TypeError):
                    stop = None
            
            if step is not None and step != "":
                try:
                    step = int(step)
                except (ValueError, TypeError):
                    step = None
            
            # Create slice object and apply it
            try:
                slice_obj = slice(start, stop, step)
                sliced_array = array_data[slice_obj]
                return sliced_array
            except (ValueError, TypeError, IndexError):
                # Return none if slice parameters are invalid
                return None