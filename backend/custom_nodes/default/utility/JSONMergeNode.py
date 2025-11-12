from nodes.NodeState import NodeState
from nodes.CustomNode import CustomNode
from FlowEngine import FlowEngine


class JSONMergeNode(CustomNode):
    def __init__(self, _engine: FlowEngine, _id: str, _nodetype: str):
        super().__init__(_engine, _id, _nodetype, "JSON Merge")

        # Input slots for two JSON objects to merge
        self.add_slot("input", "json1", "json")
        self.add_slot("input", "json2", "json")
        
        # Output slot for merged JSON
        self.add_slot("output", "merged", "json")
        self.data = {}
    
    @staticmethod
    def route() -> str:
        return "utility/json_merge"
    
    async def data_pulled(self, slot):
        if slot == "merged":
            await self.set_state(NodeState.DONE)
            
            # Get input JSON objects
            json1 = await self.pull_data("json1")
            json2 = await self.pull_data("json2")
            
            # Handle None inputs
            if json1 is None:
                json1 = {}
            if json2 is None:
                json2 = {}
            
            # Ensure inputs are dictionaries
            if not isinstance(json1, dict):
                json1 = {}
            if not isinstance(json2, dict):
                json2 = {}
            
            # Merge JSON objects (json2 takes precedence for conflicts)
            merged_json = {**json1, **json2}
            return merged_json