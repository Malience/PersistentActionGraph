from nodes.CustomNode import CustomNode
from nodes.NodeState import NodeState
from nodes.SlotType import ACTION_PARAM
from FlowEngine import FlowEngine
import json

class WebSocketServerNode(CustomNode):
    def __init__(self, _engine: FlowEngine, _id: str, _nodetype: str):
        super().__init__(_engine, _id, _nodetype, "WebSocket Server")

        # Input slots
        self.add_slot("input", "send", ACTION_PARAM)  # For sending messages to connected clients
        self.add_slot("input", "data", "any")

        self.add_slot("output", "message", ACTION_PARAM)  # Triggered when message received
        self.add_slot("output", "body", "any")  # Contains the last received message
        
        # Initialize data with default values
        self.data = {
            "path": "",
            "_socket": None,
            "_body": "",
            "_last_message": None,
            "_connected_clients": 0
        }
    
    @staticmethod
    def route() -> str:
        return "networking/websocket_server"
    
    async def startup(self) -> None:
        if self.data["_socket"] is not None:
            self.set_socket()
        
        self.cur_path = self.data["path"]

    async def receive_signal(self, signal: str, params):
        if signal == "sync":
            if self.cur_path != self.data["path"]:
                self.remove_socket()

            await self.sync()
        if signal == "set_socket":
            self.set_socket()
        if signal == "remove_socket":
            self.remove_socket()
        if signal == "send":
            await self.send_message(params)
    
    async def slot_activated(self, slot: str, params) -> None:
        if slot == "send":
            await self.send_message(params)
    
    async def data_pulled(self, slot):
        if slot == "body":
            return self.data["_body"]
        if slot == "connected_clients":
            return self.data["_connected_clients"]

    async def send_message(self, message):
        """Send a message to all connected WebSocket clients"""
        if not self.data.get("_socket"):
            print("ERROR: WebSocket not set up")
            return
        
        # Get message from input slot if params is None
        if message is None:
            message = await self.pull_data("data")
        
        if message is None:
            print("ERROR: No message to send")
            return
        
        path = self.data["_socket"]

        await self._engine.dynamic_websocket_router.broadcast_on_path(path, message)

    def set_socket(self):
        """Set up the WebSocket using the dynamic router"""
        
        path = self.data.get("path", "").strip()
        
        if not path:
            print("ERROR: Path is required for WebSockets")
            return
        
        # Remove any existing endpoint for this node first
        if self.data.get("_socket"):
            self.remove_socket()
        
        # Create the WebSocket message handler
        async def socket_handler(data):
            """Handle incoming WebSocket messages"""
            try:
                # Store the received message
                self.data["_body"] = data
                self.data["_last_message"] = data
                
                # Activate the message output slot
                await self.activate_slot("message", data)
                
            except Exception as e:
                print(f"ERROR in WebSocket handler: {e}")
        
        # Register the endpoint with the dynamic router
        res_path = self._engine.dynamic_websocket_router.add_socket(path, self._id, socket_handler)

        if not res_path:
            print("Socket could not be set!")
            return

        self.data["_socket"] = res_path
        self.cur_path = self.data["path"]
        
        print(f"WebSocket registered: {res_path} for node {self._id}")
    
    def remove_socket(self):
        """Remove the WebSocket"""
        if not self.data["_socket"]:
            return

        path = self.data.get("_socket", "").strip()
        
        if path:
            self._engine.dynamic_websocket_router.remove_socket(path, self._id)
            self.data["_socket"] = None
            print(f"WebSocket removed: {path} for node {self._id}")

            self.cur_path = None
    
    def cleanup(self):
        """Clean up endpoint when node is removed"""
        if self.data.get("_socket"):
            self.remove_socket()