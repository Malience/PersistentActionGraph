
from typing import Callable, Dict, Any, Union, Optional
import asyncio
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.routing import APIWebSocketRoute


class DynamicWebsocketRouter:
    def __init__(self, app: FastAPI):
        self.sockets: Dict[str, Dict[str, Callable]] = {}
        self.active_connections: Dict[str, list] = {}

        self.root_path = "/wsapi"
        self.app = app
    
    def add_socket(self, path: str, nodeid: str, callable: Callable) -> str:
        
        path = self.root_path + path

        if path not in self.sockets:
            self.app.add_api_websocket_route(path, endpoint=self.create_socket_handler(path))
            self.sockets[path] = {}
            self.active_connections[path] = []
        
        self.sockets[path][nodeid] = callable

        return path

    def create_socket_handler(self, path: str):
        """Create a WebSocket handler for a specific path"""
        
        async def socket_handler(websocket: WebSocket):
            await websocket.accept()
            self.active_connections[path].append(websocket)
            
            try:
                while True:
                    # Try to receive as JSON first, then text
                    data = await websocket.receive_text()
                    try:
                        data = json.loads(data)
                    except:
                        pass
                    
                    # Call all registered callbacks for this path
                    for nodeid, callback in self.sockets[path].items():
                        try:
                            await callback(data)
                        except Exception as e:
                            print(f"Error in WebSocket callback for node {nodeid}: {e}")
                            
            except WebSocketDisconnect:
                self.active_connections[path].remove(websocket)
            except Exception as e:
                print(f"Error in WebSocket handler for path {path}: {e}")
                if path in self.active_connections:
                    self.active_connections[path].remove(websocket)
        
        return socket_handler
    
    async def broadcast_on_path(self, path: str, message: Union[Dict, str]):
        """Broadcasts a message through the associated WebSocket"""
        if path not in self.active_connections:
            print("ERROR: No path registered for {path}")
            return
        
        try:
            conns = self.active_connections[path]
            # Send the message
            if isinstance(message, (dict, list)):
                for c in conns:
                    await c.send_json(message)
            else:
                for c in conns:
                    await c.send_text(str(message))
            
            print(f"WebSocket message broadcast: {message}")
            
        except Exception as e:
            print(f"ERROR sending WebSocket message: {e}")

    def remove_socket(self, path: str, nodeid: str):
        if path not in self.sockets:
            print(f"Path does not exist: {path}-{nodeid}")
            return
        
        if nodeid not in self.sockets[path]:
            print(f"Path does not exist for nodeid: {path}-{nodeid}")
            return
        
        del self.sockets[path][nodeid]

        if len(self.sockets[path]) == 0:
            for conn in self.active_connections[path]:
                w_conn: WebSocket= conn
                w_conn.close()

            del self.sockets[path]
            del self.active_connections[path]

            for i in range(len(self.app.routes)):
                route = self.app.routes[i]
                if type(route) == APIWebSocketRoute and route.path == path:
                    del self.app.routes[i]
                    break

    def clear_all_endpoints(self):
        """Clear all dynamic endpoints"""
        
        for i in range(len(self.app.routes) - 1, -1, -1):
            route = self.app.routes[i]
            if type(route) == APIWebSocketRoute and route.path in self.sockets:
                del self.app.routes[i]
        
        self.sockets.clear()
        self.active_connections.clear()