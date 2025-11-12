from nodes.CustomNode import CustomNode
from nodes.SlotType import ACTION
from FlowEngine import FlowEngine


class DataPulledNode(CustomNode):
    def __init__(self, _engine: FlowEngine, _id: str, _nodetype: str):
        super().__init__(_engine, _id, _nodetype, "Data Pulled")

        # Input slot of type "any" for the data to be passed through
        self.add_slot("input", "in", "any")
        
        # Output slots in the specified order:
        self.add_slot("output", "pre", ACTION)
        self.add_slot("output", "out", "any")
        self.add_slot("output", "post", ACTION)
    
    @staticmethod
    def route() -> str:
        return "logic/data_pulled"
    
    async def data_pulled(self, slot: str):
        # When data is pulled from this node, trigger the sequence
        if slot == "out":
            # First trigger preDataPulled action
            await self.activate_slot("pre")
            
            # Then pull the actual data from the input
            data = await self.pull_data("in")
            
            # Finally trigger postDataPulled action
            await self.activate_slot("post")
            
            return data
        
        return None