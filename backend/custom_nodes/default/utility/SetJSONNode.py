from nodes.NodeState import NodeState
from nodes.CustomNode import CustomNode
from FlowEngine import FlowEngine


class SetJSONNode(CustomNode):
    def __init__(self, _engine: FlowEngine, _id: str, _nodetype: str):
        super().__init__(_engine, _id, _nodetype, "Set JSON")

        # Input slots
        self.add_slot("input", "json", "json")
        self.add_slot("input", "value", "any")
        
        # Output slot
        self.add_slot("output", "output", "json")
        
        # Initialize data with default key
        self.data = {"key": ""}
    
    @staticmethod
    def route() -> str:
        return "utility/set_json"
    
    async def data_pulled(self, slot):
        if slot == "output":
            await self.set_state(NodeState.DONE)
            
            # Get input data
            json_input = await self.pull_data("json")
            value_input = await self.pull_data("value")
            key = self.data.get("key", "")
            
            # If no JSON input, create a new empty dict
            if json_input is None:
                json_input = {}
            
            # Ensure json_input is a dictionary
            if not isinstance(json_input, dict):
                json_input = {}
            
            # If key is empty, return the original JSON
            if not key:
                return json_input
            
            # Set the value in the JSON using the key
            json_input[key] = value_input
            
            return json_input