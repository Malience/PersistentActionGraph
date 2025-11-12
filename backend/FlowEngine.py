import os
import shortuuid
import importlib.util as imp
from pydantic import BaseModel

from EdgeMap import EdgeMap, Edge
from sockets.TextSocket import TextSocket
from sockets.JsonSocket import JsonSocket
from nodes.NodeState import NodeState

CUSTOM_BACKEND_NODES_DIR = "./backend/custom_nodes"

class Position(BaseModel):
    x: float
    y: float

class Dimension(BaseModel):
    width: float
    height: float

class FlowEngine:
    def __init__(self):
        self.custom_nodes = {}
        self.routes = {}

        self.nodes = {}
        self.edges: EdgeMap = EdgeMap()
        self.current_node_socket: TextSocket = TextSocket("current_node")
        self.node_socket: JsonSocket = JsonSocket("node_socket")
        self.data_socket: JsonSocket = JsonSocket("data")

        self.node_socket.add_callback("main", self.receive_node_socket)
        
        # State tracking
        self.last_done_node_id: str = None

    DEBUG = False
    def load_nodes(self):
        full_paths = []
        rel_paths = []
        abs_paths = []

        # TODO: Find something to get rid of all of the pylance and the __init__ nonsense
        for root, dirs, files in os.walk(CUSTOM_BACKEND_NODES_DIR):
            for file in files:
                if file.endswith(".py"):
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, CUSTOM_BACKEND_NODES_DIR)
                    abs_path = os.path.abspath(full_path)

                    full_paths.append(full_path)
                    rel_paths.append(rel_path)
                    abs_paths.append(abs_path)

        self.custom_nodes = {}
        for path in abs_paths:
            try:
                classname = os.path.splitext(os.path.basename(path))[0]
                
                if self.DEBUG:
                    print(f"DEBUG: Attempting to load node: {classname} from {path}")
                
                spec = imp.spec_from_file_location(path, path)
                module = imp.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                if self.DEBUG:
                    print(f"DEBUG: Module loaded successfully: {module}")
                    print(f"DEBUG: Module attributes: {dir(module)}")
                
                classdef = getattr(module, classname)
                
                if self.DEBUG:
                    print(f"DEBUG: Class definition found: {classdef}")
                    print(f"DEBUG: Class type: {type(classdef)}")
                
                if isinstance(classdef, type):
                    if self.DEBUG:
                        print(f"DEBUG: Valid class found, adding to custom_nodes: {classname}")
                    
                    self.custom_nodes[classname] = classdef

                    route = self.custom_nodes[classname].route()
                    self.routes[classname] = route
                    
                    if self.DEBUG:
                        print(f"DEBUG: Route registered: {classname} -> {route}")
                else:
                    if self.DEBUG:
                        print(f"DEBUG: {classname} is not a class, skipping")
                    continue
            except Exception as e:
                print(f"ERROR: Custom Node could not be loaded: {classname}")
                print(f"DEBUG: Exception details: {e}")
                import traceback
                traceback.print_exc()
        
        print(self.custom_nodes)

    def add_node(self, data: dict) -> None:
        if "id" not in data or "nodetype" not in data:
            print(f"ERROR: Could not add node. Data was not formatted correctly: {data}")

        id = data["id"]
        nodetype = data["nodetype"]
        

        if nodetype not in self.custom_nodes:
            print(f"ERROR: Nodetype not found: {nodetype}")
            return
        
        self.nodes[id] = self.custom_nodes[nodetype](self, id, nodetype)

        node = self.nodes[id]
        if "data" in data: node.data = data["data"]
        if "pos" in data: 
            pos = data["pos"]
            self.move_node(id, Position(x=pos["x"], y=pos["y"]))
        if "size" in data: 
            size = data["size"]
            self.resize_node(id, Dimension(width=size["width"], height=size["height"]))
        


    def create_node(self, nodetype: str, id: str = None) -> dict:
        if nodetype not in self.custom_nodes:
            print(f"ERROR: Nodetype not found: {nodetype}")
            return
        
        if id is not None and id in self.nodes:
            print(f"ERROR: ID already in use: {id}")
            return
        
        if id is None:
            id = str(shortuuid.uuid())

        self.nodes[id] = self.custom_nodes[nodetype](self, id, nodetype)

        print(f"NODE ADDED: {id}")
        print(self.nodes)

        return self.nodes[id].serialize()

    def remove_node(self, nodeid: str) -> bool:
        if nodeid not in self.nodes:
            print(f"ERROR: ID does not exist: {nodeid}")
            return False
        
        del self.nodes[nodeid]
        self.edges.remove_edges_by_node(nodeid)

        print(f"NODE REMOVED: {nodeid}")
        print(self.nodes)

        return True

    def move_node(self, nodeid: str, pos: Position):
        if nodeid not in self.nodes:
            print(f"ERROR: ID does not exist: {nodeid}")
            return False    
        
        self.nodes[nodeid]._pos = pos

        print(self.nodes[nodeid].serialize())

    def resize_node(self, nodeid: str, dim: Dimension):
        if nodeid not in self.nodes:
            print(f"ERROR: ID does not exist: {nodeid}")
            return False

        self.nodes[nodeid]._size = dim
        print(self.nodes[nodeid].serialize())


    def serialize(self) -> dict:
        output = {}

        nodes = []
        for k in self.nodes:
            nodes.append(self.nodes[k].serialize())
        output["nodes"] = nodes
        output["edges"] = self.edges.serialize()

        return output

    def clear(self) -> None:
        self.nodes.clear()
        self.edges.clear()

    def add_edge(self, edgeid: str, src_id: str, src_slot: str, dst_id: str, dst_slot: str) -> None:
        print("ADD EDGE " + edgeid)

        edge = Edge(
            id=edgeid,
            src_id=src_id,
            src_slot=src_slot,
            dst_id=dst_id,
            dst_slot=dst_slot
        )
        self.edges.add(edge)

    def remove_edge(self, edgeid: str) -> None:
        print("REMOVE EDGE " + edgeid)
        removed_edge = self.edges.remove(edgeid)
        if removed_edge is None:
            print("ERROR: Edge does not exist: " + edgeid)

    def load_graph(self, graph: dict) -> None:
        self.clear()

        nodes = graph["nodes"]
        for node in nodes:
            self.add_node(node)

        edges = graph["edges"]
        for edge in edges:
            self.add_edge(edge["edgeid"], edge["src_id"], edge["src_slot"], edge["dst_id"], edge["dst_slot"])

    # TODO: Ultimately this whole system needs to be overhauled to use a stack based system that can visualize the processing in a more sane way
    # Activates all nodes connected to the corresponding slot. Note: Only works if the slot is a 'src'
    async def activate_slot(self, nodeid: str, slot: str, params) -> None:
        if nodeid not in self.nodes:
            print(f"ERROR: Couldn't find original node: {nodeid}")
            return
        
        edges = self.edges.from_src(nodeid, slot)

        for e in edges:
            node = self.nodes[e.dst_id]
            await node.slot_activated(e.dst_slot, params)
    
    async def pull_data(self, nodeid: str, slot: str):
        if nodeid not in self.nodes:
            print(f"ERROR: Couldn't find original node: {nodeid}")
            return
        
        edges = self.edges.from_dst(nodeid, slot)
        data = []

        # If there are no nodes connected
        if len(edges) == 0:
            return None

        for e in edges:
            

            node = self.nodes[e.src_id]
            res = await node.data_pulled(e.src_slot)
            data.append(res)
        
        return data
    
    async def send_node_message(self, nodeid: str, type: str, data: dict):
        packet = {
            "nodeid": nodeid,
            "data": {
                "type": type,
                "data": data,
                }
        }
        await self.node_socket.send(packet)

    async def sync(self, nodeid: str, data: dict):
        await self.send_node_message(nodeid, "sync", data)

    async def send_signal(self, nodeid: str, signal: str, params) -> None:
        if nodeid not in self.nodes:
            print(f"ERROR: Couldn't find original node: {nodeid}")
            return
        
        data = {
            "signal": signal,
            "params": params,
        }
        
        await self.send_node_message(nodeid, "signal", data)

    async def receive_signal(self, nodeid: str, data: any):
        if nodeid not in self.nodes:
            print(f"ERROR: Couldn't find node to receive signal: {nodeid}")
            return

        signal = data["signal"]
        params = data["params"]

        await self.nodes[nodeid].receive_signal(signal, params)
    
    async def receive_sync(self, nodeid: str, data: any):
        await self.nodes[nodeid]._sync_data(data) 
        
    async def set_node_state(self, nodeid: str, state: NodeState) -> None:
        """Set the state of a node and handle state transitions"""
        if nodeid not in self.nodes:
            print(f"ERROR: Node not found: {nodeid}")
            return
        
        # Handle DONE state special logic - only one node can be in DONE state at a time
        if state == NodeState.DONE:
            # Reset the previous DONE node if it exists and is different
            if self.last_done_node_id and self.last_done_node_id != nodeid:
                await self._send_state_message(self.last_done_node_id, NodeState.NEUTRAL)
            
            # Update the last DONE node
            self.last_done_node_id = nodeid
        
        # Send state message to frontend
        await self._send_state_message(nodeid, state)
    
    async def _send_state_message(self, nodeid: str, state: NodeState) -> None:
        """Send a state message to the frontend"""
        packet = {
            "nodeid": nodeid,
            "data": {
                "type": "state",
                "data": {
                    "state": state.value
                }
            }
        }
        await self.node_socket.send(packet)

    async def receive_node_socket(self, data: any):
        nodeid = data["nodeid"]
        packet = data["data"]
        t = packet["type"]
        d = packet["data"]

        match t:
            case "signal":
                await self.receive_signal(nodeid, d)
            case "sync":
                await self.receive_sync(nodeid, d)


