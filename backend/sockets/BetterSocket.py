

from enum import Enum
from typing import List

from fastapi import WebSocket
import asyncio

class Mode(Enum):
    TEXT = 1
    BINARY = 2
    JSON = 3

class BetterSocket:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def _connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def _disconnect(self, websocket: WebSocket) -> None:
        self.active_connections.remove(websocket)
    
    # async def manage_websocket(self, websocket: WebSocket) -> None:
        # await self._connect(websocket)
        # try:
        #     while True:
        #         await websocket.receive()
                # TOODO: Finish this function and then add in callbacks for when the servers respond, i gtg


    # async def _broadcast(self, data) -> None:
    #     for connection in self.active_connections:
    #         await connection.send(data)
    
    # async def _broadcast_bytes(self, bytes: bytes) -> None:
    #     for connection in self.active_connections:
    #         await connection.send_bytes(bytes)
    
    # async def _broadcast_json(self, json: any) -> None:
    #     for connection in self.active_connections:
    #         await connection.send_json(json)

    def send(self, data) -> None:
        asyncio.run(self._broadcast(data))

    # def send_text(self, text: str) -> None:
    #     asyncio.run(self._broadcast_text(text))

    # def send_bytes(self, bytes: bytes) -> None:
    #     asyncio.run(self._broadcast_bytes(bytes))

    # def send_json(self, json: any) -> None:
    #     asyncio.run(self._broadcast_json(json))


# async def _broadcast(self, text: str) -> None:
#         for connection in self.active_connections:
#             await connection.send_text(text)

# class ConnectionManager:
#     def __init__(self):
#         self.active_connections: List[WebSocket] = []

#     async def connect(self, websocket: WebSocket):
#         await websocket.accept()
#         self.active_connections.append(websocket)

#     def disconnect(self, websocket: WebSocket):
#         self.active_connections.remove(websocket)

#     async def broadcast(self, message: str):
#         for connection in self.active_connections:
#             await connection.send_text(message)

# manager = ConnectionManager()

# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await manager.connect(websocket)
#     try:
#         while True:
#             data = await websocket.receive_text()
#             await manager.broadcast(f"Client says: {data}")
#     except WebSocketDisconnect:
#         manager.disconnect(websocket)
#         await manager.broadcast("A client disconnected.")