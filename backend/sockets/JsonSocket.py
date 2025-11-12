from typing import List, Dict, Callable, Any

from fastapi import WebSocket, WebSocketDisconnect

class JsonSocket:
    def __init__(self, name: str, verbose: bool = False):
        self.active_connections: List[WebSocket] = []
        self.name = name
        self.verbose = verbose
        self.callbacks: Dict[str, Callable[[Any], None]] = {}
    
    async def _connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def _disconnect(self, websocket: WebSocket) -> None:
        self.active_connections.remove(websocket)
    
    async def manage_websocket(self, websocket: WebSocket) -> None:
        await self._connect(websocket)
        if self.verbose: print(f"Socket-{self.name}: client connected!")
        try:
            while True:
                json = await websocket.receive_json()
                for _,v in self.callbacks.items():
                    await v(json)
        except WebSocketDisconnect:
            self._disconnect(websocket)
        if self.verbose: print(f"Socket-{self.name}: client disconnected!")


    async def _broadcast(self, json: any) -> None:
        for connection in self.active_connections:
            await connection.send_json(json)

    async def send(self, json: any) -> None:
        await self._broadcast(json)

    def add_callback(self, id: str, callback: Callable[[Any], None]) -> None:
        self.callbacks[id] = callback
    
    def remove_callback(self, id: str) -> None:
        if id not in self.callbacks: return
        del self.callbacks[id]