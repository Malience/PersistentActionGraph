from typing import Dict, List, Callable, Tuple
from fastapi import Request, HTTPException, FastAPI, Response
from fastapi.routing import APIRoute

class DynamicAPIRouter:
    def __init__(self, app: FastAPI):
        self.methods: Dict[str, List[str]] = {}
        self.endpoints: Dict[Tuple[str, str], Dict[str, Callable]] = {}

        self.root_path = "/api"
        self.app = app
        
    def add_endpoint(self, path: str, method: str, nodeid: str, callable: Callable, response_class: Response) -> Tuple[str, str]:
        if path[0] != '/':
            print(f"Invalid path: {path}")
            return None, None
        
        path = self.root_path + path
        method = method.upper()
        tup = (path, method)

        if tup not in self.endpoints:
            if path not in self.methods:
                self.methods[path] = [method]
                self.app.add_api_route(path, endpoint=self.endpoint_handle, methods=self.methods[path], response_class=response_class)

            else:
                self.methods[path].append(method)
                for api_route in self.app.routes:
                    if type(api_route) == APIRoute and api_route.path == path:
                        api_route.methods = self.methods[path]
                        break
            
            self.endpoints[tup] = {}
            
        self.endpoints[tup][nodeid] = callable

        return path, method

    async def endpoint_handle(self, request: Request):
        method = request.method
        path = request.url.path
        tup = (path, method)

        results = []
        for nodeid, callable in self.endpoints[tup].items():
            try:
                # Call the handler with request context
                result = await callable(request)
                results.append({
                    "nodeid": nodeid,
                    "result": result,
                    "success": True
                })
            except Exception as e:
                results.append({
                    "nodeid": nodeid,
                    "error": str(e),
                    "success": False
                })

        # Aggregate results
        if len(results) == 1:
            # Single handler - return its result directly
            if results[0]["success"]:
                return results[0]["result"]
            else:
                raise HTTPException(500, f"Handler error: {results[0]['error']}")
        else:
            # Multiple handlers - return aggregated results
            # This probably isn't the ideal output
            return results

    
    def remove_endpoint(self, path: str, method: str, nodeid: str):
        """Remove a specific node from an endpoint"""
        method = method.upper()
        tup = (path, method)

        if tup not in self.endpoints:
            print(f"Path-method combination does not exist: {tup}-{nodeid}")
            return
        
        if nodeid not in self.endpoints[tup]:
            print(f"Path-method combination does not exist for nodeid: {tup}-{nodeid}")
            return
        
        # Remove the nodes callback
        del self.endpoints[tup][nodeid]

        # Remove the instance from methods if it is empty
        if len(self.endpoints[tup]) == 0:
            del self.endpoints[tup]
            self.methods[path].remove(method)

            # Remove the method from the api
            for api_route in self.app.routes:
                if type(api_route) == APIRoute and api_route.path == path:
                    api_route.methods = self.methods[path]
                    break

            # Remove the instance from methods if it is empty
            if len(self.methods[path]) == 0:
                del self.methods[path]

                # Remove the path from the api
                # Listen, I don't know the optimal ways to remove things from lists in python and frankly
                # FastAPI should just have it's own functionality for removing endpoints
                for i in range(len(self.app.routes)):
                    route = self.app.routes[i]
                    if type(route) == APIRoute and route.path == path:
                        del self.app.routes[i]
                        break
    
    def clear_endpoints_for_node(self, nodeid: str):
        """Remove all endpoints for a specific node"""
        endpoints_to_remove = []
        
        for tup, ends in self.endpoints.items():
            if nodeid in ends:
                endpoints_to_remove.append((*tup, nodeid))
        
        for e in endpoints_to_remove:
            self.remove_endpoint(*e)
    
    def clear_all_endpoints(self):
        """Clear all dynamic endpoints"""
        
        for i in range(len(self.app.routes) - 1, -1, -1):
            route = self.app.routes[i]
            # Since methods basically holds a list of all paths we can use it to check paths
            if type(route) == APIRoute and route.path in self.methods:
                del self.app.routes[i]
        
        self.methods.clear()
        self.endpoints.clear()

