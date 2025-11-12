from nodes.CustomNode import CustomNode
from nodes.NodeState import NodeState
from nodes.SlotType import ACTION, ACTION_PARAM
from FlowEngine import FlowEngine
from typing import Any, List


class ArrayNode(CustomNode):
    def __init__(self, _engine: FlowEngine, _id: str, _nodetype: str):
        super().__init__(_engine, _id, _nodetype, "Array")

        # Input slots
        self.add_slot("input", "clear", ACTION)
        self.add_slot("input", "set", ACTION_PARAM)
        self.add_slot("input", "push", ACTION_PARAM)
        self.add_slot("input", "pop", ACTION)
        self.add_slot("input", "dequeue", ACTION)
        
        # Output slots
        self.add_slot("output", "on_change", ACTION)
        self.add_slot("output", "pop_out", ACTION_PARAM)
        self.add_slot("output", "dequeue_out", ACTION_PARAM)
        self.add_slot("output", "elements", "any")
        self.add_slot("output", "length", "int")
        
        # Initialize data with empty array
        self.data = {
            "elements": [],
            "length": 0
        }
    
    @staticmethod
    def route() -> str:
        return "utility/array"
    
    async def slot_activated(self, slot: str, params) -> None:
        if slot == "clear":
            await self.clear_array()
        elif slot == "set":
            await self.set_array(params)
        elif slot == "push":
            await self.push_element(params)
        elif slot == "pop":
            await self.pop_element()
        elif slot == "dequeue":
            await self.dequeue_element()
    
    async def data_pulled(self, slot: str) -> Any:
        if slot == "elements":
            await self.set_state(NodeState.DONE)
            return self.data["elements"]
        elif slot == "length":
            await self.set_state(NodeState.DONE)
            return self.data["length"]
    
    async def receive_signal(self, signal: str, params):
        if signal == "clear":
            await self.clear_array()
        elif signal == "pop":
            await self.pop_element()
        elif signal == "dequeue":
            await self.dequeue_element()
    
    async def clear_array(self) -> None:
        await self.set_state(NodeState.PROCESSING)
        
        # Clear all elements
        self.data["elements"] = []
        self.data["length"] = 0
        
        await self.set_state(NodeState.DONE)
        
        # Sync the cleared data to frontend
        await self.sync()
        
        # Trigger the on_change output
        await self.activate_slot("on_change")
    
    async def set_array(self, new_array: Any) -> None:
        await self.set_state(NodeState.PROCESSING)
        
        # Validate that we have an array
        if not isinstance(new_array, list):
            print(f"ERROR: Invalid array input: {new_array}")
            await self.set_state(NodeState.ERROR)
            return
        
        # Set the new array
        self.data["elements"] = new_array
        self.data["length"] = len(new_array)
        
        await self.set_state(NodeState.DONE)
        
        # Sync the updated data to frontend
        await self.sync()
        
        # Trigger the on_change output
        await self.activate_slot("on_change")
    
    async def push_element(self, element: Any) -> None:
        await self.set_state(NodeState.PROCESSING)
        
        # Add element to the end of the array
        self.data["elements"].append(element)
        self.data["length"] = len(self.data["elements"])
        
        await self.set_state(NodeState.DONE)
        
        # Sync the updated data to frontend
        await self.sync()
        
        # Trigger the on_change output
        await self.activate_slot("on_change")
    
    async def pop_element(self) -> None:
        await self.set_state(NodeState.PROCESSING)
        
        # Check if there are elements to pop
        if len(self.data["elements"]) == 0:
            await self.set_state(NodeState.DONE)
            return
        
        # Remove and get the last element
        popped_element = self.data["elements"].pop()
        self.data["length"] = len(self.data["elements"])
        
        await self.set_state(NodeState.DONE)
        
        # Sync the updated data to frontend
        await self.sync()
        
        # Trigger the on_change output
        await self.activate_slot("on_change")
        
        # Trigger the pop_out output with the popped element
        await self.activate_slot("pop_out", popped_element)
    
    async def dequeue_element(self) -> None:
        await self.set_state(NodeState.PROCESSING)
        
        # Check if there are elements to dequeue
        if len(self.data["elements"]) == 0:
            await self.set_state(NodeState.DONE)
            return
        
        # Remove and get the first element
        dequeued_element = self.data["elements"].pop(0)
        self.data["length"] = len(self.data["elements"])
        
        await self.set_state(NodeState.DONE)
        
        # Sync the updated data to frontend
        await self.sync()
        
        # Trigger the on_change output
        await self.activate_slot("on_change")
        
        # Trigger the dequeue_out output with the dequeued element
        await self.activate_slot("dequeue_out", dequeued_element)