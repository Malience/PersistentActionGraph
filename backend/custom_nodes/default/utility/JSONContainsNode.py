from nodes.CustomNode import CustomNode
from nodes.NodeState import NodeState
from FlowEngine import FlowEngine
import json


class JSONContainsNode(CustomNode):
    def __init__(self, _engine: FlowEngine, _id: str, _nodetype: str):
        super().__init__(_engine, _id, _nodetype, "JSON Contains")
        
        # Input slots for JSON object and key
        self.add_slot("input", "json", "any")
        self.add_slot("input", "key", "string")
        
        # Output slot for boolean result
        self.add_slot("output", "contains", "boolean")
        
        # Default data with key (for frontend fallback)
        self.data = {
            "key": "",
        }
    
    @staticmethod
    def route() -> str:
        return "utility/json_contains"
    
    async def data_pulled(self, slot):
        if slot == "contains":
            json_input = await self.pull_data("json")
            key_input = await self.pull_data("key")
            
            # Get key from input slot or fall back to frontend data
            if key_input is not None:
                key = key_input
            else:
                # Use frontend value as fallback
                key = self.data.get("key", "")
            
            # Handle JSON input - could be dict or JSON string
            if json_input is None:
                await self.set_state(NodeState.DONE)
                return False
            
            # Try to parse as JSON if it's a string
            if isinstance(json_input, str):
                try:
                    json_input = json.loads(json_input)
                except json.JSONDecodeError:
                    await self.set_state(NodeState.DONE)
                    return False
            
            # Check if it's a dictionary
            if not isinstance(json_input, dict):
                await self.set_state(NodeState.DONE)
                return False
            
            # Check if key exists in JSON object
            contains = key in json_input
            await self.set_state(NodeState.DONE)
            return contains