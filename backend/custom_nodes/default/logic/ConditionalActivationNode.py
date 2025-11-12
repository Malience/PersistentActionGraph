from nodes.CustomNode import CustomNode
from nodes.SlotType import ACTION_PARAM
from FlowEngine import FlowEngine


class ConditionalActivationNode(CustomNode):
    def __init__(self, _engine: FlowEngine, _id: str, _nodetype: str):
        super().__init__(_engine, _id, _nodetype, "Conditional Activation")
        
        # Input slots: action input and boolean condition
        self.add_slot("input", "action", ACTION_PARAM)
        self.add_slot("input", "condition", "bool")
        
        # Output slot for conditional action
        self.add_slot("output", "true", ACTION_PARAM)
        self.add_slot("output", "false", ACTION_PARAM)
    
    @staticmethod
    def route() -> str:
        return "logic/conditional_activation"
    
    async def slot_activated(self, slot: str, params):
        if slot == "action":

            cond = await self.pull_data("condition")

            # Only activate output if condition is true
            if cond or cond is None:
                await self.activate_slot("true", params)
            else:
                await self.activate_slot("false", params)