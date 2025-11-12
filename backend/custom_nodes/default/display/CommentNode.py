from nodes.CustomNode import CustomNode
from FlowEngine import FlowEngine


class CommentNode(CustomNode):
    def __init__(self, _engine: FlowEngine, _id: str, _nodetype: str):
        super().__init__(_engine, _id, _nodetype, "Comment")
        
        # No inputs or outputs - just a display node
        self.data = {"value": ""}
    
    @staticmethod
    def route() -> str:
        return "display/comment"