from nodes.CustomNode import CustomNode
from nodes.NodeState import NodeState
from nodes.SlotType import ACTION
from FlowEngine import FlowEngine
from typing import Any, List


class ChatDisplayNode(CustomNode):
    def __init__(self, _engine: FlowEngine, _id: str, _nodetype: str):
        super().__init__(_engine, _id, _nodetype, "Chat Display")

        # Input slots
        self.add_slot("input", "update", ACTION)
        self.add_slot("input", "messages", "message[]")

        # Initialize data with empty message list
        self.data = {
            "messages": [],
            "message_count": 0,
            "auto_scroll": True,
        }
    
    @staticmethod
    def route() -> str:
        return "chat/display"
    
    async def slot_activated(self, slot: str, params) -> None:
        if slot == "update":
            await self.update_display()
    
    async def update_display(self) -> None:
        await self.set_state(NodeState.PROCESSING)
        
        # Pull the latest messages from the input slot
        messages = await self.pull_data("messages")
        
        if messages is not None:
            self.data["messages"] = messages
            self.data["message_count"] = len(messages)
        
        await self.set_state(NodeState.DONE)
        await self.sync()