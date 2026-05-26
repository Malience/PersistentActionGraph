from nodes.CustomNode import CustomNode
from nodes.NodeState import NodeState
from nodes.SlotType import ACTION_PARAM
from FlowEngine import FlowEngine
from fastapi import Request
import json

class HTTPEndpointNode(CustomNode):
    def __init__(self, _engine: FlowEngine, _id: str, _nodetype: str):
        super().__init__(_engine, _id, _nodetype, "HTTP Endpoint")

        # Input slots
        self.add_slot("input", "data", "any")

        self.add_slot("output", "request", ACTION_PARAM)
        self.add_slot("output", "body", "any")
        
        # Initialize data with default values
        self.data = {
            "path": "",
            "method": "GET",
            "response_type": "JSON",
            "_endpoint": None,
            "_method": None,
            "_body": "",
        }
    
    @staticmethod
    def route() -> str:
        return "networking/http_endpoint"
    
    async def startup(self) -> None:
        if self.data["_endpoint"] is not None:
            self.set_endpoint()
        
        self.cur_path = self.data["path"]
        self.cur_method = self.data["method"]

    async def receive_signal(self, signal: str, params):
        if signal == "sync":
            if self.cur_path != self.data["path"] or self.cur_method != self.data["method"]:
                self.remove_endpoint()

            await self.sync()
        if signal == "set_endpoint":
            self.set_endpoint()
        if signal == "remove_endpoint":
            self.remove_endpoint()
    
    async def data_pulled(self, slot):
        if slot == "body":
            return self.data["_body"]

    def set_endpoint(self):
        """Set up the HTTP endpoint using the dynamic router"""
        
        path = self.data.get("path", "").strip()
        method = self.data.get("method", "GET").upper()
        
        if not path:
            print("ERROR: Path is required for HTTP endpoint")
            return
        
        # Remove any existing endpoint for this node first
        if self.data.get("_endpoint"):
            self.remove_endpoint()
        
        # Create the endpoint handler
        async def endpoint_handler(request: Request):
            try:
                method = self.data.get("method", "GET").upper()
                if request.method != method:
                    raise Exception(f"Incorrect method - {request.method}")

                # Parse content type
                content_type = None
                if "Content-Type" in request.headers:
                    content_type = request.headers["Content-Type"]
                    
                match content_type:
                    case "text/plain":
                        body = (await request.body()).decode('utf-8')
                    case "application/json":
                        body = await request.json()
                    case _:
                        body = await request.body()

                self.data["_body"] = body

                await self.activate_slot("request", body)
                
                response_data = await self.pull_data("data")
                return response_data
                # # Handle different HTTP methods
                # if method == "GET":
                #     request_data = dict(request.query_params)
                # elif method in ["POST", "PUT", "DELETE"]:
                #     try:
                #         body = await request.body()
                #         if body:
                #             request_data = await request.json()
                #     except:
                #         # If JSON parsing fails, try form data
                #         try:
                #             request_data = await request.form()
                #             request_data = dict(request_data)
                #         except:
                #             request_data = {"raw_body": body.decode()}
                
                # # Store the request data for the node
                # self.data["_last_request"] = {
                #     "method": method,
                #     "path": path,
                #     "headers": dict(request.headers),
                #     "data": request_data
                # }
                
                # # Return response - can be customized by connected nodes
                # response_data = await self.pull_data("data")
                # if response_data is not None:
                #     return response_data
                # else:
                #     return {
                #         "status": "success",
                #         "message": f"Endpoint {path} handled by node {self._id}",
                #         "node_id": self._id,
                #         "request_data": request_data
                #     }
                    
            except Exception as e:
                print(f"ERROR in HTTP endpoint handler: {e}")
                return {
                    "status": "error",
                    "message": str(e),
                    "node_id": self._id
                }
        

        from fastapi.responses import (
            FileResponse,
            JSONResponse,
            HTMLResponse,
            PlainTextResponse
        )
        # Get response class
        response_class = JSONResponse
        match(self.data["response_type"]):
            case "File": response_class = FileResponse
            case "JSON": response_class = JSONResponse
            case "HTML": response_class = HTMLResponse
            case "Plain Text": response_class = PlainTextResponse
            case _: response_class = JSONResponse

        # Register the endpoint with the dynamic router
        res_path, res_method = self._engine.dynamic_api_router.add_endpoint(path, method, self._id, endpoint_handler, response_class=response_class)

        if not res_path:
            print("Endpoint could not be set!")
            return

        self.data["_endpoint"] = res_path
        self.data["_method"] = res_method
        self.cur_path = self.data["path"]
        self.cur_method = self.data["method"]
        
        print(f"HTTP Endpoint registered: {res_method} {res_path} for node {self._id}")
    
    def remove_endpoint(self):
        """Remove the HTTP endpoint"""
        if not self.data["_endpoint"]:
            return

        path = self.data.get("_endpoint", "").strip()
        method = self.data.get("_method", "GET").upper()
        
        if path:
            self._engine.dynamic_api_router.remove_endpoint(path, method, self._id)
            self.data["_endpoint"] = None
            self.data["_method"] = None
            print(f"HTTP Endpoint removed: {method} {path} for node {self._id}")

            self.cur_path = None
            self.cur_method = None
    
    def cleanup(self):
        """Clean up endpoint when node is removed"""
        if self.data.get("_endpoint"):
            self.remove_endpoint()