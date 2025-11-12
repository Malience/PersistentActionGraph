from nodes.CustomNode import CustomNode
from nodes.NodeState import NodeState
from nodes.SlotType import ACTION_PARAM
from nodes.Message import Message, MessageRole, create_message, validate_message
from FlowEngine import FlowEngine


class MessageInputNode(CustomNode):
    def __init__(self, _engine: FlowEngine, _id: str, _nodetype: str):
        super().__init__(_engine, _id, _nodetype, "Message Input")

        # Output slots
        self.add_slot("output", "submit", ACTION_PARAM)
        self.add_slot("output", "message", "message")
        
        # Initialize data with default values
        self.data = {
            "text": "",
            "_output": "",
            "placeholder": "Type a message...",
            "role": MessageRole.USER.value,
            "cached_message": None
        }
    
    @staticmethod
    def route() -> str:
        return "chat/message_input"
    
    async def receive_signal(self, signal: str, params):
        if signal == "submit":
            await self.set_state(NodeState.PROCESSING)

            # Get the current text
            text = self.data["text"]
            
            if not text:
                print("ERROR: No text to submit")
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
                self.data["_output"] = text
                
                # Clear the input after submission
                self.data["text"] = ""
                await self.sync()

                await self.set_state(NodeState.DONE)
                
                # Output the message and trigger submit action
                await self.activate_slot("submit", message)
                
            except ValueError as e:
                print(f"ERROR creating message: {e}")
                await self.set_state(NodeState.ERROR)
    
    async def data_pulled(self, slot):
        if slot == "message":
            await self.set_state(NodeState.DONE)
            return self.data["cached_message"]