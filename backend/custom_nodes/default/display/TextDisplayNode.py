from nodes.CustomNode import CustomNode
from nodes.NodeState import NodeState
from nodes.SlotType import ACTION_PARAM
from FlowEngine import FlowEngine


class TextDisplayNode(CustomNode):
    def __init__(self, _engine: FlowEngine, _id: str, _nodetype: str):
        super().__init__(_engine, _id, _nodetype, "Text Display")

        self.add_slot("input", "update", ACTION_PARAM)
        self.add_slot("input", "text", "string")
        
        self.data = {"display_text": ""}

    @staticmethod
    def route() -> str:
        return "display/text"

    async def slot_activated(self, slot: str, params) -> None:
        if slot == "update":
            await self.set_state(NodeState.PROCESSING)
            
            # First try to get text from the dedicated "text" slot
            text = await self.pull_data("text")
            
            # If no text from slot, check if params contains a string
            if text is None and params and isinstance(params, str):
                text = params
            
            if text is not None:
                self.data["display_text"] = str(text)
                await self.sync()
            
            await self.set_state(NodeState.DONE)