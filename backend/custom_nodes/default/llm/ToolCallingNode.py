from typing import List
from nodes.CustomNode import CustomNode
from nodes.NodeState import NodeState
from nodes.SlotType import ACTION, ACTION_PARAM
import aiohttp
import json

def refine_tools(tools: List[dict]) -> List[dict]:
    """Alter the JSON Schema to work with function calling"""
    refined = []

    for tool in tools: # Look it's late, I don't even know if this copies properly
        newTool = tool
        newTool["type"] = "function"
        refined.append(newTool)
    
    return refined

def simplify_tool_calls(tool_calls: List[dict]) -> List[dict]:
    """Convert full tool calls to simplified format with just name and arguments."""
    simplified = []
    
    for tool_call in tool_calls:
        function_data = tool_call.get("function", {})
        name = function_data.get("name")
        arguments_str = function_data.get("arguments", "{}")
        
        if not name:
            continue
            
        try:
            # Parse arguments from JSON string to dict
            arguments = json.loads(arguments_str) if isinstance(arguments_str, str) else arguments_str
            simplified.append({
                "name": name,
                "args": arguments
            })
        except json.JSONDecodeError:
            continue
    
    return simplified

class ToolCallingNode(CustomNode):
    def __init__(self, _engine, _id: str, _nodetype: str):
        super().__init__(_engine, _id, _nodetype, "Tool Calling")

        # Input slots
        self.add_slot("input", "activate", ACTION)
        self.add_slot("input", "api_connection", "api_connection")
        self.add_slot("input", "settings", "json")
        self.add_slot("input", "tools", "json_schema[]")
        self.add_slot("input", "messages", "message[]")
        
        # Output slots
        self.add_slot("output", "done", ACTION_PARAM)
        self.add_slot("output", "output", "json[]")
        
        # Initialize data with default values
        self.data = {
            "max_length": 128,
            "max_context_length": 2048,
            "_output": None
        }
    
    @staticmethod
    def route() -> str:
        return "llm/tool_calling"
    
    async def slot_activated(self, slot: str, params) -> None:
        if slot == "activate":
            await self.activate(params)
    
    async def data_pulled(self, slot):
        if slot == "output":
            return self.data["_output"]
    
    async def activate(self, params=None):
        await self.set_state(NodeState.PROCESSING)
        
        # Get input data from connected slots
        conn = await self.pull_data("api_connection")
        sett = await self.pull_data("settings")
        tools_raw = await self.pull_data("tools")
        messages = await self.pull_data("messages")
        
        if not conn:
            print("ERROR: Missing required input (api_connection)")
            await self.set_state(NodeState.ERROR)
            return
        
        if not messages or not isinstance(messages, list):
            print("ERROR: Missing required input (messages) - no message array found in messages slot or params")
            await self.set_state(NodeState.ERROR)
            return
        
        # # Validate tools if provided #TODO: Redo this, we're using raw schemas now Could potentially replace the "title" with "function" for additional compat
        # if tools and not json.:
        #     print("ERROR: Invalid tools format")
        #     await self.set_state(NodeState.ERROR)
        #     return

        tools = refine_tools(tools_raw)
        # print(tools)
        
        # Prepare settings for the API request
        settings = {
            "max_context_length": self.data["max_context_length"],
            "max_completion_tokens": self.data["max_length"],
            "quiet": False
        }
        
        api_url = conn.get("api_url")
        if not api_url:
            print("ERROR: No API URL found in connection data")
            await self.set_state(NodeState.ERROR)
            return
        
        # Prepare the request body
        model = "kcpp"
        header = {
            "model": model,
            "messages": messages,
            "tool_choice": "auto"
        }
        
        # Add tools if provided
        if tools:
            header["tools"] = tools
        
        # Merge all settings together
        body_data = {**header, **settings}
        if sett:
            body_data.update(sett)
        
        body = json.dumps(body_data)
        
        try:
            # Make the API request
            async with aiohttp.ClientSession() as session:
                async with session.post(api_url, data=body, headers={'Content-Type': 'application/json'}) as response:
                    if not response.ok:
                        raise Exception(f"Response status: {response.status}")
                    
                    json_response = await response.json()
                    
                    # Extract the tool calls from the response and simplify them
                    tool_calls_raw = json_response["choices"][0]["message"].get("tool_calls", [])
                    tool_calls = simplify_tool_calls(tool_calls_raw)
                    self.data["_output"] = tool_calls
                    
                    # Set to DONE before activating the next slot
                    await self.set_state(NodeState.DONE)
                    
                    # Trigger the done output slot with the simplified tool calls
                    await self.activate_slot("done", tool_calls)
                    
        except Exception as e:
            print(f"ERROR in ToolCallNode: {e}")
            self.data["_output"] = []
            await self.set_state(NodeState.ERROR)