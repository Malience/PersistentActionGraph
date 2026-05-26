from nodes.CustomNode import CustomNode
from nodes.NodeState import NodeState
from nodes.SlotType import ACTION_PARAM
from FlowEngine import FlowEngine
import aiohttp
import json


class HTTPRequestNode(CustomNode):
    def __init__(self, _engine: FlowEngine, _id: str, _nodetype: str):
        super().__init__(_engine, _id, _nodetype, "HTTP Request")

        # Input slots
        self.add_slot("input", "activate", ACTION_PARAM)
        self.add_slot("input", "body", "any")
        
        # Output slots
        self.add_slot("output", "done", ACTION_PARAM)
        self.add_slot("output", "response", "any")
        
        # Initialize data with default values
        self.data = {
            "url": "",
            "method": "GET",
            "content_type": "",
            "body_text": "",
            "_response": None
        }
    
    @staticmethod
    def route() -> str:
        return "networking/http_request"
    
    async def slot_activated(self, slot: str, params) -> None:
        if slot == "activate":
            await self.activate(params)
    
    async def receive_signal(self, signal: str, params):
        if signal == "activate":
            await self.activate(params)
    
    async def data_pulled(self, slot):
        if slot == "response":
            return self.data["_response"]
    
    async def activate(self, params=None):
        await self.set_state(NodeState.PROCESSING)
        
        # Get input data from connected slots
        body_from_slot = await self.pull_data("body")
        
        # Use body from slot if connected, otherwise use the textarea input
        body = body_from_slot if body_from_slot is not None else self.data["body_text"]
        
        url = self.data["url"]
        if not url:
            print("ERROR: Missing required input (url)")
            await self.set_state(NodeState.ERROR)
            return
        
        method = self.data["method"]
        content_type = self.data["content_type"]
        
        headers = {}
        if content_type:
            headers['Content-Type'] = content_type
        
        try:
            # Make the HTTP request
            async with aiohttp.ClientSession() as session:
                if method == "GET":
                    async with session.get(url, data=body, headers=headers) as response:
                        response_text = await response.text()
                        self.data["_response"] = response_text
                        
                elif method == "POST":
                    async with session.post(url, data=body, headers=headers) as response:
                        response_text = await response.text()
                        self.data["_response"] = response_text
                        
                elif method == "PUT":
                    async with session.put(url, data=body, headers=headers) as response:
                        response_text = await response.text()
                        self.data["_response"] = response_text
                        
                elif method == "DELETE":
                    async with session.delete(url, data=body, headers=headers) as response:
                        response_text = await response.text()
                        self.data["_response"] = response_text
                
                # Set to DONE before activating the next slot
                await self.set_state(NodeState.DONE)
                
                # Trigger the done output slot with the response
                await self.activate_slot("done", self.data["_response"])
                
        except Exception as e:
            print(f"ERROR in HTTPRequestNode: {e}")
            self.data["_response"] = f"Error: {str(e)}"
            await self.set_state(NodeState.ERROR)