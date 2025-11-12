from nodes.NodeState import NodeState
from nodes.CustomNode import CustomNode
from FlowEngine import FlowEngine


class AppendArrayNode(CustomNode):
    def __init__(self, _engine: FlowEngine, _id: str, _nodetype: str):
        super().__init__(_engine, _id, _nodetype, "Append Array")

        self.add_slot("input", "array", "any")
        self.add_slot("input", "item", "any")
        self.add_slot("output", "output", "any")
        self.data = {}
    
    @staticmethod
    def route() -> str:
        return "utility/append_array"
    
    async def data_pulled(self, slot):
        if slot == "output":
            await self.set_state(NodeState.DONE)
            array_data = await self.pull_data("array")
            item_data = await self.pull_data("item")
            
            # Handle array input
            if array_data is None:
                # If no array provided, create new array with the item
                return [item_data] if item_data is not None else []
            elif isinstance(array_data, list):
                # If array is provided, append the item
                if item_data is not None:
                    return array_data + [item_data]
                else:
                    return array_data
            else:
                # If array is not a list, create new array with both values
                if item_data is not None:
                    return [array_data, item_data]
                else:
                    return [array_data]