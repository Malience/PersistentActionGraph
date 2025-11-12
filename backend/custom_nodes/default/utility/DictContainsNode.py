from nodes.CustomNode import CustomNode
from nodes.NodeState import NodeState
from FlowEngine import FlowEngine


class DictContainsNode(CustomNode):
    def __init__(self, _engine: FlowEngine, _id: str, _nodetype: str):
        super().__init__(_engine, _id, _nodetype, "Dict Contains")
        
        # Input slots for dictionary and key
        self.add_slot("input", "dict", "any")
        self.add_slot("input", "key", "any")
        
        # Output slot for boolean result
        self.add_slot("output", "contains", "bool")
        
        # Default data with key (for frontend fallback)
        self.data = {
            "key": "",
        }
    
    @staticmethod
    def route() -> str:
        return "utility/dict_contains"
    
    async def data_pulled(self, slot):
        if slot == "contains":
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
                return False
            
            # Check if key exists in dictionary
            contains = key in dict_input
            await self.set_state(NodeState.DONE)
            return contains