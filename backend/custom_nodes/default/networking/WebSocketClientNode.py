from nodes.CustomNode import CustomNode
from nodes.NodeState import NodeState
from nodes.SlotType import ACTION_PARAM
from FlowEngine import FlowEngine
import aiohttp
import json
import asyncio
from websockets.asyncio.client import connect
from typing import Optional


class WebSocketClientNode(CustomNode):
    def __init__(self, _engine: FlowEngine, _id: str, _nodetype: str):
        super().__init__(_engine, _id, _nodetype, "WebSocket Client")

        # Input slots
        self.add_slot("input", "send", ACTION_PARAM)
        self.add_slot("input", "message", "any")
        
        # Output slots
        self.add_slot("output", "received", ACTION_PARAM)
        self.add_slot("output", "response", "any")
        
        # Initialize data with default values
        self.data = {
            "url": "",
            "_connected": False,
            "_last_received": False,
        }

        self._session = None
        self._websocket = None
        
        # Task for receiving messages
        self.receive_task: Optional[asyncio.Task] = None
    
    @staticmethod
    def route() -> str:
        return "networking/websocket_client"
    
    async def startup(self) -> None:
        if self.data["_connected"]:
            self.data["_connected"] = False
            await self.connect()
    
    async def slot_activated(self, slot: str, params) -> None:
        if slot == "send":
            await self.send_message(params)
    
    async def receive_signal(self, signal: str, params):
        if signal == "activate":
            await self.send_message(params)
        elif signal == "connect":
            await self.connect()
        elif signal == "disconnect":
            await self.disconnect()
    
    async def data_pulled(self, slot):
        if slot == "response":
            return self.data["_last_received"]
        if slot == "connected":
            return self.data["_connected"]
    
    async def connect(self):
        """Connect to the WebSocket server"""
        url = self.data["url"]
        if not url:
            print("ERROR: URL is required for WebSocket connection")
            await self.disconnect()
            return
        
        if self.data["_connected"]:
            print("Already connected")
            return
        
        try:
            await self.set_state(NodeState.PROCESSING)
            
            # Connect to WebSocket
            session = aiohttp.ClientSession()
            websocket = await session.ws_connect(url)
            
            self._websocket = websocket
            self.data["_connected"] = True
            self._session = session
            
            # Start receiving messages
            self.receive_task = asyncio.create_task(self.receive_messages())
            
            await self.set_state(NodeState.DONE)
            await self.activate_slot("connected", None)

            await self.sync()
            
            print(f"WebSocket connected to {url}")
            
        except Exception as e:
            print(f"ERROR connecting to WebSocket: {e}")
            self.data["_connected"] = False
            await self.set_state(NodeState.ERROR)
    
    async def disconnect(self):
        """Disconnect from the WebSocket server"""
        if not self.data["_connected"]:
            return
        
        try:
            await self.set_state(NodeState.PROCESSING)
            
            # Cancel receive task
            if self.receive_task:
                self.receive_task.cancel()
                try:
                    await self.receive_task
                except asyncio.CancelledError:
                    pass
                self.receive_task = None
            
            # Close WebSocket
            if self._websocket:
                await self._websocket.close()
                self._websocket = None
            
            # Close session
            if self._session:
                await self._session.close()
                self._session = None
            
            self.data["_connected"] = False
            
            await self.set_state(NodeState.DONE)
            await self.sync()
            
            print("WebSocket disconnected")
            
        except Exception as e:
            print(f"ERROR disconnecting from WebSocket: {e}")
            await self.set_state(NodeState.ERROR)
    
    async def send_message(self, params=None):
        """Send a message through the WebSocket"""
        if not self.data["_connected"]:
            print("ERROR: Not connected to WebSocket")
            return
        
        # Get message from input slot if params is None
        message = params
        if message is None:
            message = await self.pull_data("message")
        
        if message is None:
            print("ERROR: No message to send")
            return
        
        try:
            await self.set_state(NodeState.PROCESSING)
            
            # Send the message
            if isinstance(message, (dict, list)):
                await self._websocket.send_json(message)
            else:
                await self._websocket.send_str(str(message))
            
            await self.set_state(NodeState.DONE)
            
            print(f"WebSocket message sent: {message}")
            
        except Exception as e:
            print(f"ERROR sending WebSocket message: {e}")
            await self.set_state(NodeState.ERROR)
    
    async def receive_messages(self):
        """Continuously receive messages from the WebSocket"""
        try:
            while self.data["_connected"] and self._websocket:
                msg = await self._websocket.receive()
                
                if msg.type == aiohttp.WSMsgType.TEXT:
                    data = msg.data
                    # Try to parse as JSON
                    try:
                        data = json.loads(data)
                    except:
                        pass
                    
                    self.data["_last_received"] = data
                    await self.activate_slot("received", data)
                    await self.activate_slot("response", data)
                    
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    print(f"WebSocket error: {self._websocket.exception()}")
                    break
                elif msg.type == aiohttp.WSMsgType.CLOSE:
                    print("WebSocket closed by server")
                    break
                    
        except asyncio.CancelledError:
            pass
        except Exception as e:
            print(f"ERROR receiving WebSocket messages: {e}")
    
    def cleanup(self):
        """Clean up when node is removed"""
        if self.data["_connected"]:
            # Schedule disconnect
            asyncio.create_task(self.disconnect())