from nodes.CustomNode import CustomNode
from nodes.NodeState import NodeState
from nodes.SlotType import ACTION_PARAM
from nodes.Message import Message, MessageRole, create_message, validate_message
from FlowEngine import FlowEngine


class ChatMessageNode(CustomNode):
    def __init__(self, _engine: FlowEngine, _id: str, _nodetype: str):
        super().__init__(_engine, _id, _nodetype, "Chat Message")

        # Input slots
        self.add_slot("input", "activate", ACTION_PARAM)
        self.add_slot("input", "text", "string")
        
        # Output slots
        self.add_slot("output", "message_output", ACTION_PARAM)
        self.add_slot("output", "cached_message", "message")
        self.add_slot("output", "pull_message", "message")
        
        # Initialize data with default values
        self.data = {
            "role": MessageRole.USER.value,
            "cached_message": None
        }
    
    @staticmethod
    def route() -> str:
        return "chat/message"
    
    async def slot_activated(self, slot: str, params) -> None:
        if slot == "activate":
            await self.create_message(params)
    
    async def data_pulled(self, slot):
        if slot == "cached_message":
            await self.set_state(NodeState.DONE)
            return self.data["cached_message"]
        elif slot == "pull_message":
            await self.set_state(NodeState.PROCESSING)

            text = await self.pull_data("text")
            if text is None:
                print("ERROR: No text found in text slot or params")
                await self.set_state(NodeState.ERROR)
                return
            
            # Get the selected role from data
            role_str = self.data.get("role", MessageRole.USER.value)

            try:
                # Convert string role to MessageRole enum
                role = MessageRole(role_str)
                
                # Create the message structure
                message = create_message(role, text)
                
                
                await self.set_state(NodeState.DONE)
                # Cache the message
                self.data["cached_message"] = message
                return self.data["cached_message"]
            
            except ValueError as e:
                print(f"ERROR creating message: {e}")
                await self.set_state(NodeState.ERROR)
    
    async def create_message(self, params=None):
        await self.set_state(NodeState.PROCESSING)

        # First try to get text from the dedicated "text" slot
        text = await self.pull_data("text")
        
        # If no text from slot, check if params contains a string
        if text is None and params and isinstance(params, str):
            text = params
        
        if text is None:
            print("ERROR: No text found in text slot or params")
            await self.set_state(NodeState.ERROR)
            return
        
        # Get the selected role from data
        role_str = self.data.get("role", MessageRole.USER.value)
        
        try:
            # Convert string role to MessageRole enum
            role = MessageRole(role_str)
            
            # Create the message structure
            message = create_message(role, text)
            
            # Cache the message
            self.data["cached_message"] = message
            
            await self.set_state(NodeState.DONE)
            
            # Trigger the message output with the created message
            await self.activate_slot("message_output", message)
            
        except ValueError as e:
            print(f"ERROR creating message: {e}")
            await self.set_state(NodeState.ERROR)