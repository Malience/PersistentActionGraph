
from abc import abstractmethod
from typing import Any

from FlowEngine import Dimension, FlowEngine, Position
from nodes.NodeState import NodeState

#TODO: Dirty checking
class CustomNode:

    def __init__(self, _engine: FlowEngine, _id: str, _nodetype: str, label: str):
        self._engine: FlowEngine = _engine
        self._id = _id
        self._nodetype = _nodetype
        self._state: NodeState = NodeState.NEUTRAL
        self._input_slots = {}
        self._output_slots = {}

        self._pos: Position = None
        self._size: Dimension = None

        self.label = label
        self.data = {}

    # Should return the nodes 'route' ie. the string used for the context menu
    @staticmethod
    @abstractmethod
    def route() -> str:
        pass

    async def data_pulled(self, slot: str) -> Any:
        pass

    async def slot_activated(self, slot: str, params) -> None:
        pass
    
    async def receive_signal(self, signal: str, params):
        pass
    
    async def set_state(self, state: NodeState) -> None:
        await self._engine.set_node_state(self._id, state)

    async def sync(self) -> None:
        await self._engine.sync(self._id, self.data)
    
    async def send_signal(self, signal: str, params) -> None:
        await self._engine.send_signal(self._id, signal, params)
    
    async def _sync_data(self, data: dict) -> None:
        self.data = data

    # TODO: Deal with type I guess
    async def pull_data(self, slot: str, expected_type: type = Any, single_output: bool = True) -> Any:
        out = await self._engine.pull_data(self._id, slot)
        if out is None:
            return out
        if single_output and len(out) == 1:
            out = out[0]
        return out

    async def activate_slot(self, slot: str, params: dict = None) -> None:
        await self._engine.activate_slot(self._id, slot, params)

    def add_slot(self, direction: str, id: str, datatype: str) -> None:
        if direction != "input" and direction != "output":
            print(f"ERROR: Added slot with invalid direction: {direction}")
            return
        
        if direction == "input":
            self._input_slots[id] = datatype
        elif direction == "output":
            self._output_slots[id] = datatype
        
    def serialize(self) -> dict:
        input_slots = []
        output_slots = []

        for k,v in self._input_slots.items():
            input_slots.append({"id": k, "datatype": v})

        for k,v in self._output_slots.items():
            output_slots.append({"id": k, "datatype": v})


        output = {}

        output["id"] = self._id
        output["nodetype"] = self._nodetype
        output["input_slots"] = input_slots
        output["output_slots"] = output_slots

        if self._pos is not None: output["pos"] = {"x": self._pos.x, "y": self._pos.y}
        if self._size is not None: output["size"] = {"width": self._size.width, "height": self._size.height}

        output["label"] = self.label
        output["data"] = self.data

        return output