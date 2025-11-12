from nodes.NodeState import NodeState
from nodes.CustomNode import CustomNode
from FlowEngine import FlowEngine


def _extract_value(data, key_path):
    """Extract value from nested JSON using dot notation or direct key access."""
    if not isinstance(data, dict):
        return None
    
    # Handle dot notation for nested keys
    if '.' in key_path:
        keys = key_path.split('.')
        current = data
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return None
        return current
    else:
        # Direct key access
        return data.get(key_path)


class GetJSONNode(CustomNode):
    def __init__(self, _engine: FlowEngine, _id: str, _nodetype: str):
        super().__init__(_engine, _id, _nodetype, "Get JSON")

        # Input slot for JSON
        self.add_slot("input", "json", "json")
        
        # Output slot for the extracted value
        self.add_slot("output", "value", "any")
        
        # Initialize data with default key
        self.data = {"key": ""}
    
    @staticmethod
    def route() -> str:
        return "utility/get_json"
    
    async def data_pulled(self, slot):
        if slot == "value":
            await self.set_state(NodeState.DONE)
            
            # Get input data
            json_input = await self.pull_data("json")
            key = self.data.get("key", "")
            
            # If no JSON input or key is empty, return None
            if json_input is None or not key:
                return None
            
            # Ensure json_input is a dictionary
            if not isinstance(json_input, dict):
                return None
            
            # Get the value from the JSON using the key with nested support
            value = _extract_value(json_input, key)
            
            return value