from nodes.CustomNode import CustomNode
from nodes.NodeState import NodeState
from FlowEngine import FlowEngine


class DictGetNode(CustomNode):
    def __init__(self, _engine: FlowEngine, _id: str, _nodetype: str):
        super().__init__(_engine, _id, _nodetype, "Dict Get")
        
        # Input slots for dictionary and key
        self.add_slot("input", "dict", "any")
        self.add_slot("input", "key", "any")
        
        # Output slot for the value
        self.add_slot("output", "value", "any")
        
        # Default data with key (for frontend fallback)
        self.data = {
            "key": "",
        }
    
    @staticmethod
    def route() -> str:
        return "utility/dict_get"
    
    async def data_pulled(self, slot):
        if slot == "value":
            dict_input = await self.pull_data("dict")
            key_input = await self.pull_data("key")
            
            # Get key from input slot or fall back to frontend data
            if key_input is not None:
                key = key_input
            else:
                # Use frontend value as fallback
                key = self.data.get("key", "")
            
            # Handle dictionary input
            if dict_input is None or not isinstance(dict_input, dict):
                await self.set_state(NodeState.DONE)
                return None
            
            # Check if key exists in dictionary
            if key in dict_input:
                await self.set_state(NodeState.DONE)
                return dict_input[key]
            else:
                # Key not found
                await self.set_state(NodeState.DONE)
                return None