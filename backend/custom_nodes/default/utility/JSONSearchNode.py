from nodes.CustomNode import CustomNode
from nodes.NodeState import NodeState
from nodes.SlotType import ACTION, ACTION_PARAM
from FlowEngine import FlowEngine
from typing import Any, Dict, List
import json


class JSONSearchNode(CustomNode):
    def __init__(self, _engine: FlowEngine, _id: str, _nodetype: str):
        super().__init__(_engine, _id, _nodetype, "JSON Search")

        # Input slots
        self.add_slot("input", "activate", ACTION_PARAM)
        self.add_slot("input", "dict", "any")
        
        # Output slots
        self.add_slot("output", "found", ACTION)
        self.add_slot("output", "keys", "any")
        self.add_slot("output", "values", "any")
        self.add_slot("output", "count", "int")
        
        # Initialize data with search criteria
        self.data = {
            "search_key": "",
            "search_value": "",
            "_found_keys": [],
            "_found_values": [],
            "_found_count": 0
        }
    
    @staticmethod
    def route() -> str:
        return "utility/json_search"
    
    async def slot_activated(self, slot: str, params) -> None:
        if slot == "activate":
            await self.search(params)
    
    async def data_pulled(self, slot: str) -> Any:
        if slot == "keys":
            await self.set_state(NodeState.DONE)
            return self.data["_found_keys"]
        elif slot == "values":
            await self.set_state(NodeState.DONE)
            return self.data["_found_values"]
        elif slot == "count":
            await self.set_state(NodeState.DONE)
            return self.data["_found_count"]
    
    async def search(self, params=None):
        await self.set_state(NodeState.PROCESSING)
        
        # Get dictionary from input slot
        dict_input = await self.pull_data("dict")
        
        # Validate that we have a dictionary
        if not isinstance(dict_input, dict):
            print(f"ERROR: Invalid dictionary input: {dict_input}")
            await self.set_state(NodeState.ERROR)
            return
        
        # Get search criteria from frontend data
        search_key = self.data.get("search_key", "")
        search_value = self.data.get("search_value", "")
        
        # Initialize results
        found_keys = []
        found_values = []
        
        # Search through the dictionary
        for key, value in dict_input.items():
            # Try to parse value as JSON if it's a string
            parsed_value = value
            if isinstance(value, str):
                try:
                    parsed_value = json.loads(value)
                except json.JSONDecodeError:
                    continue
            
            # Skip if parsed value is a dictionary (nested)
            if isinstance(parsed_value, dict):
                # Check if the current element contains the search key and matches the search value
                if search_key in parsed_value and str(parsed_value[search_key]) == search_value:
                    found_keys.append(key)
                    found_values.append(value)
        
        # Update output caches
        self.data["_found_keys"] = found_keys
        self.data["_found_values"] = found_values
        self.data["_found_count"] = len(found_keys)
        
        await self.set_state(NodeState.DONE)
        
        # Trigger the found output
        await self.activate_slot("found")