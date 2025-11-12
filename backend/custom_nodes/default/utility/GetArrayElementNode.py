from nodes.NodeState import NodeState
from nodes.CustomNode import CustomNode
from FlowEngine import FlowEngine


class GetArrayElementNode(CustomNode):
    def __init__(self, _engine: FlowEngine, _id: str, _nodetype: str):
        super().__init__(_engine, _id, _nodetype, "Get Array Element")

        self.add_slot("input", "array", "any")
        self.add_slot("input", "index", "int")
        self.add_slot("output", "element", "any")
        self.data = {
            "index": 0
        }
    
    @staticmethod
    def route() -> str:
        return "utility/get_array_element"
    
    async def data_pulled(self, slot):
        if slot == "element":
            await self.set_state(NodeState.DONE)
            array_data = await self.pull_data("array")
            
            # Get the index from input slot or fall back to frontend data
            index_input = await self.pull_data("index")
            
            if index_input is not None:
                index = index_input
            else:
                # Use frontend value as fallback
                index = self.data.get("index", 0)
            
            # Handle array input
            if array_data is None or not isinstance(array_data, list):
                return None
            
            # Check if index is within bounds
            if index < 0 or index >= len(array_data):
                return None
            
            # Return the element at the specified index
            return array_data[index]