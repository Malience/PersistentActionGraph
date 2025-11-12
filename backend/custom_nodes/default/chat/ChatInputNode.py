from nodes.NodeState import NodeState
from nodes.CustomNode import CustomNode
from nodes.SlotType import ACTION_PARAM
from FlowEngine import FlowEngine


class ChatInputNode(CustomNode):
    def __init__(self, _engine: FlowEngine, _id: str, _nodetype: str):
        super().__init__(_engine, _id, _nodetype, "Chat Input")

        self.add_slot("output", "submit", ACTION_PARAM)
        self.add_slot("output", "text", "string")
        
        self.data = {"text": "", "_output": "", "placeholder": "Type a message..."}

    @staticmethod
    def route() -> str:
        return "chat/chat_input"

    async def receive_signal(self, signal: str, params):
        if signal == "submit":
            await self.set_state(NodeState.PROCESSING)

            # Cache the text for data pulling
            self.data["_output"] = self.data["text"]
            
            # Clear the input after submission
            self.data["text"] = ""
            await self.sync()

            await self.set_state(NodeState.DONE)
            
            # Output the current text and trigger submit action
            await self.activate_slot("submit", self.data["_output"])
    
    async def data_pulled(self, slot):
        if slot == "text":
            await self.set_state(NodeState.DONE)
            return self.data["_output"]