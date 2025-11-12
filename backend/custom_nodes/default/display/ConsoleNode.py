
from nodes.CustomNode import CustomNode
from nodes.NodeState import NodeState
from nodes.SlotType import ACTION_PARAM
from FlowEngine import FlowEngine


class ConsoleNode(CustomNode):
    def __init__(self, _engine: FlowEngine, _id: str, _nodetype: str):
        super().__init__(_engine, _id, _nodetype, "Console")

        self.add_slot("input", "trigger", ACTION_PARAM)
        self.add_slot("input", "input", "any")
        

    @staticmethod
    def route() -> str:
        return "display/console"
    
    async def slot_activated(self, slot: str, params) -> None:
        if slot == "trigger":
            await self.set_state(NodeState.PROCESSING)
            
            # First try to get text from the dedicated "text" slot
            input = await self.pull_data("input")
            
            # If no text from slot, check if params contains a string
            if input is None and params:
                input = params
            
            if input is not None:
                print(f"Console: {input}")
                await self.send_signal("console", input)
            
            await self.set_state(NodeState.DONE)