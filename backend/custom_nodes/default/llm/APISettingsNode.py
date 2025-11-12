from nodes.NodeState import NodeState
from nodes.CustomNode import CustomNode
from FlowEngine import FlowEngine


class APISettingsNode(CustomNode):
    def __init__(self, _engine: FlowEngine, _id: str, _nodetype: str):
        super().__init__(_engine, _id, _nodetype, "API Settings")

        # Output slot for settings JSON
        self.add_slot("output", "settings", "json")
        
        # Initialize data with default values matching the TypeScript version
        self.data = {
            "temperature": 0.7,
            "top_k": 0,
            "top_p": 1.0,
            "typical": 1.0,
            "top_a": 0.0,
            "tfs": 1.0,
            "rep_pen": 1.05,
            "rep_pen_range": 4096,
            "rep_pen_slope": 1.0
        }
    
    @staticmethod
    def route() -> str:
        return "llm/api_settings"
    
    async def data_pulled(self, slot):
        if slot == "settings":
            await self.set_state(NodeState.DONE)
            return self.data