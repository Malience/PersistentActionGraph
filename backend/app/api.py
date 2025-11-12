from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import os
import shutil
import mimetypes
from typing import List


from FlowEngine import Dimension, FlowEngine, Position

CUSTOM_FRONTENT_NODES_DIR = "./frontend/custom_nodes"
CUSTOM_BACKEND_NODES_DIR = "./backend/custom_nodes"

engine: FlowEngine = None

def get_files(dir, filetype):
    out = []

    for root, dirs, files in os.walk(dir):
        for file in files:
            if file.endswith(filetype):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, dir)

                out.append(rel_path)
    return out

def setup_engine():
    global engine
    engine = FlowEngine()
    engine.load_nodes()


# Application
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    setup_engine()
    yield
    # Cleanup

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:3000",
    "localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
async def read_root() -> dict:
    data = engine.serialize()
    print(data)
    return data


@app.get("/custom_nodes")
async def custom_nodes() -> dict:
    frontend_nodes = {}

    frontend_files = get_files(CUSTOM_FRONTENT_NODES_DIR, ".tsx")
    for file in frontend_files:
        filename_ext = os.path.basename(file)
        filename = os.path.splitext(filename_ext)[0]
        frontend_nodes[filename] = file




    return {
        "frontend_nodes": frontend_nodes,
        "routes": engine.routes,
    }

@app.get("/graph_state")
async def graph_state() -> dict:
    pass

@app.post("/add_node/{nodetype}")
async def add_node(nodetype: str, pos: Position) -> dict:
    node = engine.create_node(nodetype)
    engine.move_node(node["id"], pos)
    return node

@app.delete("/remove_node/{nodeid}")
async def remove_node(nodeid: str) -> dict:
    result = engine.remove_node(nodeid)
    return {"result": result}

@app.put("/move_node/{nodeid}")
async def move_node(nodeid: str, pos: Position) -> dict:
    engine.move_node(nodeid, pos)
    return {}

@app.put("/resize_node/{nodeid}")
async def resize_node(nodeid: str, dim: Dimension) -> dict:
    engine.resize_node(nodeid, dim)
    return {}


@app.post("/load_graph")
async def add_node(data: dict) -> dict:
    engine.load_graph(data)
    return {}

@app.delete("/remove_edge/{edgeid}")
async def remove_edge(edgeid: str) -> dict:
    result = engine.remove_edge(edgeid)
    return {"result": result}

@app.post("/add_edge")
async def add_edge(data: dict) -> dict:
    engine.add_edge(data["edgeid"], data["src_id"], data["src_slot"], data["dst_id"], data["dst_slot"])
    return {}

@app.post("/clear_graph")
async def clear_graph() -> dict:
    engine.clear()
    return {}

@app.post("/get_subgraph")
async def get_subgraph(node_ids: dict) -> dict:
    """Get a subgraph containing the specified nodes and edges between them"""
    if "node_ids" not in node_ids:
        raise HTTPException(status_code=400, detail="Missing 'node_ids' field")
    
    selected_nodes = node_ids["node_ids"]
    if not isinstance(selected_nodes, list):
        raise HTTPException(status_code=400, detail="'node_ids' must be a list")
    
    # Get nodes
    subgraph_nodes = []
    for node_id in selected_nodes:
        if node_id in engine.nodes:
            subgraph_nodes.append(engine.nodes[node_id].serialize())
    
    # Get edges between selected nodes
    subgraph_edges = []
    for edge in engine.edges.edges.values():
        if edge.src_id in selected_nodes and edge.dst_id in selected_nodes:
            subgraph_edges.append(edge.serialize())
    
    return {
        "nodes": subgraph_nodes,
        "edges": subgraph_edges
    }

@app.post("/add_subgraph")
async def add_subgraph(data: dict) -> dict:
    """Add a subgraph to the current graph, generating new IDs for all elements"""
    subgraph = data.get("subgraph", data)  # Support both old and new format
    if "nodes" not in subgraph or "edges" not in subgraph:
        raise HTTPException(status_code=400, detail="Missing 'nodes' or 'edges' field")
    
    # Get position offset if provided
    position_offset = data.get("position_offset", {"x": 0, "y": 0})
    
    import shortuuid
    
    # Create mapping from old IDs to new IDs
    id_mapping = {}
    new_nodes = []
    new_edges = []
    
    # Add nodes with new IDs
    for node_data in subgraph["nodes"]:
        old_id = node_data["id"]
        new_id = str(shortuuid.uuid())
        id_mapping[old_id] = new_id
        
        # Create new node data with updated ID
        new_node_data = node_data.copy()
        new_node_data["id"] = new_id
        
        # Apply simple position offset if provided
        if "pos" in new_node_data and (position_offset["x"] != 0 or position_offset["y"] != 0):
            new_node_data["pos"]["x"] += position_offset["x"]
            new_node_data["pos"]["y"] += position_offset["y"]
        
        # Add the node to the engine
        engine.add_node(new_node_data)
        new_nodes.append(engine.nodes[new_id].serialize())
    
    # Add edges with new IDs and updated node references
    for edge_data in subgraph["edges"]:
        old_src_id = edge_data["src_id"]
        old_dst_id = edge_data["dst_id"]
        
        # Skip edges where nodes weren't copied (shouldn't happen in our case)
        if old_src_id not in id_mapping or old_dst_id not in id_mapping:
            continue
            
        new_src_id = id_mapping[old_src_id]
        new_dst_id = id_mapping[old_dst_id]
        new_edge_id = f"edge_{new_src_id}-{edge_data['src_slot']}_{new_dst_id}-{edge_data['dst_slot']}"
        
        # Add the edge to the engine
        engine.add_edge(
            new_edge_id,
            new_src_id,
            edge_data["src_slot"],
            new_dst_id,
            edge_data["dst_slot"]
        )
        new_edges.append(engine.edges.get(new_edge_id).serialize())
    
    return {
        "new_nodes": new_nodes,
        "new_edges": new_edges,
        "new_node_ids": list(id_mapping.values())
    }

@app.websocket("/current_node")
async def current_node(websocket: WebSocket):
    await engine.current_node_socket.manage_websocket(websocket)

@app.websocket("/node_socket")
async def current_node(websocket: WebSocket):
    await engine.node_socket.manage_websocket(websocket)