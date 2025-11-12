from nodes.CustomNode import CustomNode
from nodes.NodeState import NodeState
from nodes.SlotType import ACTION, ACTION_PARAM
from FlowEngine import FlowEngine
from typing import Any, Dict
import shortuuid


class DictNode(CustomNode):
    def __init__(self, _engine: FlowEngine, _id: str, _nodetype: str):
        super().__init__(_engine, _id, _nodetype, "Dictionary")

        # Input slots
        self.add_slot("input", "clear", ACTION)
        self.add_slot("input", "set", ACTION_PARAM)
        self.add_slot("input", "remove", ACTION_PARAM)
        self.add_slot("input", "insert", ACTION)
        self.add_slot("input", "key", "any")
        self.add_slot("input", "value", "any")
        
        # Output slots
        self.add_slot("output", "on_update", ACTION)
        self.add_slot("output", "dict", "any")
        self.add_slot("output", "count", "int")
        
        # Initialize data with empty dictionary
        self.data = {
            "dict": {},
            "count": 0
        }
    
    @staticmethod
    def route() -> str:
        return "utility/dict"
    
    async def slot_activated(self, slot: str, params) -> None:
        if slot == "clear":
            await self.clear_dict()
        elif slot == "set":
            await self.set_dict(params)
        elif slot == "remove":
            await self.remove_key(params)
        elif slot == "insert":
            await self.insert_element()
    
    async def data_pulled(self, slot: str) -> Any:
        if slot == "dict":
            await self.set_state(NodeState.DONE)
            return self.data["dict"]
        elif slot == "count":
            await self.set_state(NodeState.DONE)
            return self.data["count"]
    
    async def receive_signal(self, signal: str, params):
        if signal == "clear":
            await self.clear_dict()
    
    async def clear_dict(self) -> None:
        await self.set_state(NodeState.PROCESSING)
        
        # Clear all elements
        self.data["dict"] = {}
        self.data["count"] = 0
        
        await self.set_state(NodeState.DONE)
        
        # Sync the cleared data to frontend
        await self.sync()
        
        # Trigger the on_update output
        await self.activate_slot("on_update")
    
    async def set_dict(self, new_dict: Any) -> None:
        await self.set_state(NodeState.PROCESSING)
        
        # Validate that we have a dictionary
        if not isinstance(new_dict, dict):
            print(f"ERROR: Invalid dictionary input: {new_dict}")
            await self.set_state(NodeState.ERROR)
            return
        
        # Set the new dictionary
        self.data["dict"] = new_dict
        self.data["count"] = len(new_dict)
        
        await self.set_state(NodeState.DONE)
        
        # Sync the updated data to frontend
        await self.sync()
        
        # Trigger the on_update output
        await self.activate_slot("on_update")
    
    async def remove_key(self, key: Any) -> None:
        await self.set_state(NodeState.PROCESSING)
        
        # Check if the key exists
        if key not in self.data["dict"]:
            print(f"WARNING: Key '{key}' not found in dictionary")
            await self.set_state(NodeState.DONE)
            return
        
        # Remove the key
        del self.data["dict"][key]
        self.data["count"] = len(self.data["dict"])
        
        await self.set_state(NodeState.DONE)
        
        # Sync the updated data to frontend
        await self.sync()
        
        # Trigger the on_update output
        await self.activate_slot("on_update")
    
    async def insert_element(self) -> None:
        await self.set_state(NodeState.PROCESSING)
        
        # Get key and value from input slots
        key = await self.pull_data("key")
        value = await self.pull_data("value")
        
        # Generate a short UUID if no key is provided
        if key is None:
            key = shortuuid.uuid()[:8]  # Use first 8 characters for brevity
        
        # Insert the key-value pair
        self.data["dict"][key] = value
        self.data["count"] = len(self.data["dict"])
        
        await self.set_state(NodeState.DONE)
        
        # Sync the updated data to frontend
        await self.sync()
        
        # Trigger the on_update output
        await self.activate_slot("on_update")