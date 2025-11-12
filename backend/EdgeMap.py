
from dataclasses import dataclass
from typing import Dict, List, Optional, Set


@dataclass
class Edge():
    id: str
    src_id: str
    src_slot: str
    dst_id: str
    dst_slot: str

    def serialize(self):
        return {
            "edgeid": self.id,
            "src_id": self.src_id,
            "src_slot": self.src_slot,
            "dst_id": self.dst_id,
            "dst_slot": self.dst_slot,
        }


class EdgeMap():
    def __init__(self):
        # Primary storage by edge ID
        self.edges: Dict[str, Edge] = {}
        
        # Index by source node+slot -> set of edge IDs
        self.src_index: Dict[str, Set[str]] = {}
        
        # Index by destination node+slot -> set of edge IDs  
        self.dst_index: Dict[str, Set[str]] = {}
        
        # Index by node ID -> set of edge IDs (for both src and dst)
        self.node_index: Dict[str, Set[str]] = {}

    def add(self, edge: Edge) -> None:
        """Add an edge to the map with all necessary indexing"""
        if edge.id in self.edges:
            raise ValueError(f"Edge with id {edge.id} already exists")
        
        self.edges[edge.id] = edge
        
        # Index by source
        src_key = f"{edge.src_id}_{edge.src_slot}"
        if src_key not in self.src_index:
            self.src_index[src_key] = set()
        self.src_index[src_key].add(edge.id)
        
        # Index by destination
        dst_key = f"{edge.dst_id}_{edge.dst_slot}"
        if dst_key not in self.dst_index:
            self.dst_index[dst_key] = set()
        self.dst_index[dst_key].add(edge.id)
        
        # Index by nodes (both src and dst)
        for node_id in [edge.src_id, edge.dst_id]:
            if node_id not in self.node_index:
                self.node_index[node_id] = set()
            self.node_index[node_id].add(edge.id)

    def remove(self, id: str) -> Optional[Edge]:
        """Remove an edge by ID"""
        if id not in self.edges:
            return None
            
        edge = self.edges[id]
        
        # Remove from all indexes
        src_key = f"{edge.src_id}_{edge.src_slot}"
        dst_key = f"{edge.dst_id}_{edge.dst_slot}"
        
        if src_key in self.src_index:
            self.src_index[src_key].discard(id)
            if not self.src_index[src_key]:
                del self.src_index[src_key]
        
        if dst_key in self.dst_index:
            self.dst_index[dst_key].discard(id)
            if not self.dst_index[dst_key]:
                del self.dst_index[dst_key]
        
        # Remove from node index
        for node_id in [edge.src_id, edge.dst_id]:
            if node_id in self.node_index:
                self.node_index[node_id].discard(id)
                if not self.node_index[node_id]:
                    del self.node_index[node_id]
        
        # Remove from primary storage
        return self.edges.pop(id)

    def remove_edges_by_node(self, node_id: str) -> List[Edge]:
        """Remove all edges connected to a node (as src or dst)"""
        if node_id not in self.node_index:
            return []
            
        # Get all edge IDs for this node
        edge_ids = list(self.node_index[node_id])
        removed_edges = []
        
        # Remove each edge (this will handle index cleanup)
        for edge_id in edge_ids:
            if edge_id in self.edges:  # Double check it still exists
                removed_edges.append(self.remove(edge_id))
        
        return removed_edges

    def get(self, id: str) -> Optional[Edge]:
        """Get an edge by ID"""
        return self.edges.get(id)

    def from_src(self, node_id: str, slot: str) -> List[Edge]:
        """Get all edges from a specific source node and slot"""
        key = f"{node_id}_{slot}"
        if key not in self.src_index:
            return []
        
        return [self.edges[edge_id] for edge_id in self.src_index[key] if edge_id in self.edges]

    def from_dst(self, node_id: str, slot: str) -> List[Edge]:
        """Get all edges to a specific destination node and slot"""
        key = f"{node_id}_{slot}"
        if key not in self.dst_index:
            return []
        
        return [self.edges[edge_id] for edge_id in self.dst_index[key] if edge_id in self.edges]

    def get_edges_by_node(self, node_id: str) -> List[Edge]:
        """Get all edges connected to a node (as src or dst)"""
        if node_id not in self.node_index:
            return []
        
        return [self.edges[edge_id] for edge_id in self.node_index[node_id] if edge_id in self.edges]

    def clear(self) -> None:
        """Clear all edges"""
        self.edges.clear()
        self.src_index.clear()
        self.dst_index.clear()
        self.node_index.clear()

    def __len__(self) -> int:
        return len(self.edges)

    def __contains__(self, id: str) -> bool:
        return id in self.edges

    def serialize(self):
        """Serialize all edges in the map"""
        return [edge.serialize() for edge in self.edges.values()]
