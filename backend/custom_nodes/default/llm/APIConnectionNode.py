from nodes.NodeState import NodeState
from nodes.CustomNode import CustomNode
from FlowEngine import FlowEngine


class APIConnectionNode(CustomNode):
    def __init__(self, _engine: FlowEngine, _id: str, _nodetype: str):
        super().__init__(_engine, _id, _nodetype, "API Connection")

        # Output slot for API connection
        self.add_slot("output", "connection", "api_connection")
        
        # Initialize data with default API URL matching the TypeScript version
        self.data = {
            "api_url": "http://127.0.0.1:5001/v1/chat/completions"
            # "api_url": "http://127.0.0.1:5001/api/v1/generate"
        }
    
    @staticmethod
    def route() -> str:
        return "llm/api_connection"
    
    async def data_pulled(self, slot):
        if slot == "connection":
            await self.set_state(NodeState.DONE)
            return self.data