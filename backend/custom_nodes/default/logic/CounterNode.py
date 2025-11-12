from nodes.CustomNode import CustomNode
from nodes.NodeState import NodeState
from nodes.SlotType import ACTION, ACTION_PARAM
from FlowEngine import FlowEngine


class CounterNode(CustomNode):
    def __init__(self, _engine: FlowEngine, _id: str, _nodetype: str):
        super().__init__(_engine, _id, _nodetype, "Counter")

        # Input slots
        self.add_slot("input", "increment", ACTION)
        self.add_slot("input", "decrement", ACTION)
        self.add_slot("input", "set", ACTION_PARAM)
        self.add_slot("input", "clear", ACTION)
        
        # Output slots
        self.add_slot("output", "on_update", ACTION_PARAM)
        self.add_slot("output", "value", "int")
        
        # Initialize data with default values
        self.data = {
            "current_value": 0,
            "min": 0,
            "max": 100,
            "step": 1,
            "looping": False
        }
    
    @staticmethod
    def route() -> str:
        return "logic/counter"
    
    async def slot_activated(self, slot: str, params) -> None:
        if slot == "increment":
            await self.increment()
        elif slot == "decrement":
            await self.decrement()
        elif slot == "set":
            await self.set_value(params)
        elif slot == "clear":
            await self.clear()
    
    async def data_pulled(self, slot: str):
        if slot == "value":
            await self.set_state(NodeState.DONE)
            return self.data["current_value"]
    
    async def receive_signal(self, signal: str, params):
        if signal == "increment":
            await self.increment()
        elif signal == "decrement":
            await self.decrement()
        elif signal == "clear":
            await self.clear()
    
    async def increment(self) -> None:
        await self.set_state(NodeState.PROCESSING)
        
        current_value = self.data["current_value"]
        step = self.data.get("step", 1)
        min_value = self.data.get("min", 0)
        max_value = self.data.get("max", 100)
        looping = self.data.get("looping", False)
        
        # Calculate new value
        new_value = current_value + step
        
        # Handle bounds with looping if enabled
        if looping:
            if max_value is not None and new_value > max_value:
                # Loop back to min value
                new_value = min_value
            elif min_value is not None and new_value < min_value:
                # Loop back to max value
                new_value = max_value
        else:
            # Standard bounds checking
            if max_value is not None:
                new_value = min(new_value, max_value)
            if min_value is not None:
                new_value = max(new_value, min_value)
        
        self.data["current_value"] = new_value
        
        await self.set_state(NodeState.DONE)
        
        # Sync the updated data to frontend
        await self.sync()
        
        # Trigger the on_update output with the new value
        await self.activate_slot("on_update", new_value)
    
    async def decrement(self) -> None:
        await self.set_state(NodeState.PROCESSING)
        
        current_value = self.data["current_value"]
        step = self.data.get("step", 1)
        min_value = self.data.get("min", 0)
        max_value = self.data.get("max", 100)
        looping = self.data.get("looping", False)
        
        # Calculate new value
        new_value = current_value - step
        
        # Handle bounds with looping if enabled
        if looping:
            if min_value is not None and new_value < min_value:
                # Loop back to max value
                new_value = max_value
            elif max_value is not None and new_value > max_value:
                # Loop back to min value
                new_value = min_value
        else:
            # Standard bounds checking
            if min_value is not None:
                new_value = max(new_value, min_value)
            if max_value is not None:
                new_value = min(new_value, max_value)
        
        self.data["current_value"] = new_value
        
        await self.set_state(NodeState.DONE)
        
        # Sync the updated data to frontend
        await self.sync()
        
        # Trigger the on_update output with the new value
        await self.activate_slot("on_update", new_value)
    
    async def set_value(self, new_value: int) -> None:
        await self.set_state(NodeState.PROCESSING)
        
        # Validate that we have an integer
        if not isinstance(new_value, int):
            print(f"ERROR: Invalid value input: {new_value}")
            await self.set_state(NodeState.ERROR)
            return
        
        min_value = self.data.get("min", 0)
        max_value = self.data.get("max", 100)
        
        # Apply bounds checking
        if min_value is not None:
            new_value = max(new_value, min_value)
        if max_value is not None:
            new_value = min(new_value, max_value)
        
        self.data["current_value"] = new_value
        
        await self.set_state(NodeState.DONE)
        
        # Sync the updated data to frontend
        await self.sync()
        
        # Trigger the on_update output with the new value
        await self.activate_slot("on_update", new_value)
    
    async def clear(self) -> None:
        await self.set_state(NodeState.PROCESSING)
        
        # Reset to default value (respecting min bound)
        min_value = self.data.get("min", 0)
        self.data["current_value"] = min_value
        
        await self.set_state(NodeState.DONE)
        
        # Sync the updated data to frontend
        await self.sync()
        
        # Trigger the on_update output with the new value
        await self.activate_slot("on_update", self.data["current_value"])