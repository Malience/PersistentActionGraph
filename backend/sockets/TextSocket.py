from typing import List, Dict, Callable

from fastapi import WebSocket, WebSocketDisconnect

class TextSocket:
    def __init__(self, name: str, verbose: bool = False):
        self.active_connections: List[WebSocket] = []
        self.name = name
        self.verbose = verbose
        self.callbacks: Dict[str, Callable[[str], None]] = {}
    
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
                text = await websocket.receive_text()
                for _,v in self.callbacks:
                    v(text)
        except WebSocketDisconnect:
            self._disconnect(websocket)
        if self.verbose: print(f"Socket-{self.name}: client disconnected!")


    async def _broadcast(self, text: str) -> None:
        for connection in self.active_connections:
            await connection.send_text(text)

    async def send(self, text: str) -> None:
        await self._broadcast(text)

    def add_callback(self, id: str, callback: Callable[[str], None]) -> None:
        self.callbacks[id] = callback
    
    def remove_callback(self, id: str) -> None:
        if id not in self.callbacks: return
        del self.callbacks[id]