from nodes.CustomNode import CustomNode
from nodes.NodeState import NodeState
from nodes.SlotType import ACTION, ACTION_PARAM
from nodes.Message import Message, validate_message
from FlowEngine import FlowEngine
from typing import List, Any


class MessageDatabaseNode(CustomNode):
    def __init__(self, _engine: FlowEngine, _id: str, _nodetype: str):
        super().__init__(_engine, _id, _nodetype, "Message Database")

        # Input slots
        self.add_slot("input", "add_message", ACTION_PARAM)
        self.add_slot("input", "clear_database", ACTION)
        
        # Output slots
        self.add_slot("output", "on_update", ACTION)
        self.add_slot("output", "messages", "message[]")
        self.add_slot("output", "message_count", "int")

        # Initialize data with empty message list
        self.data = {
            "messages": [],
            "message_count": 0
        }
    
    @staticmethod
    def route() -> str:
        return "chat/message_database"
    
    async def slot_activated(self, slot: str, params) -> None:
        if slot == "add_message":
            await self.add_message_to_database(params)
        elif slot == "clear_database":
            await self.clear_database()
    
    async def data_pulled(self, slot: str) -> Any:
        if slot == "messages":
            await self.set_state(NodeState.DONE)
            return self.data["messages"]
        elif slot == "message_count":
            await self.set_state(NodeState.DONE)
            return self.data["message_count"]
    
    async def receive_signal(self, signal: str, params):
        if signal == "clear_database":
            await self.clear_database()
        elif signal == "delete_last_message":
            await self.delete_last_message()
    
    async def add_message_to_database(self, message_data: Any) -> None:
        await self.set_state(NodeState.PROCESSING)
        
        # Validate the incoming message
        if not validate_message(message_data):
            print(f"ERROR: Invalid message structure received: {message_data}")
            await self.set_state(NodeState.ERROR)
            return
        
        # Add the validated message to the database
        self.data["messages"].append(message_data)
        self.data["message_count"] = len(self.data["messages"])
        
        await self.set_state(NodeState.DONE)
        
        # Sync the updated data to frontend
        await self.sync()
        
        # Trigger the on_update output
        await self.activate_slot("on_update")
    
    async def clear_database(self) -> None:
        await self.set_state(NodeState.PROCESSING)
        
        # Clear all messages
        self.data["messages"] = []
        self.data["message_count"] = 0
        
        await self.set_state(NodeState.DONE)
        
        # Sync the cleared data to frontend
        await self.sync()
        
        # Trigger the on_update output
        await self.activate_slot("on_update")
    
    async def delete_last_message(self) -> None:
        await self.set_state(NodeState.PROCESSING)
        
        # Check if there are messages to delete
        if len(self.data["messages"]) == 0:
            await self.set_state(NodeState.DONE)
            return
        
        # Remove the last message
        self.data["messages"].pop()
        self.data["message_count"] = len(self.data["messages"])
        
        await self.set_state(NodeState.DONE)
        
        # Sync the updated data to frontend
        await self.sync()
        
        # Trigger the on_update output
        await self.activate_slot("on_update")