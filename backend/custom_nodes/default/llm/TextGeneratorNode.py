from nodes.CustomNode import CustomNode
from nodes.NodeState import NodeState
from nodes.SlotType import ACTION, ACTION_PARAM
from FlowEngine import FlowEngine
import aiohttp
import json


class TextGeneratorNode(CustomNode):
    def __init__(self, _engine: FlowEngine, _id: str, _nodetype: str):
        super().__init__(_engine, _id, _nodetype, "Text Generator")

        # Input slots
        self.add_slot("input", "activate", ACTION_PARAM)
        self.add_slot("input", "api_connection", "api_connection")
        self.add_slot("input", "settings", "json")
        self.add_slot("input", "prompt", "string")
        
        # Output slots
        self.add_slot("output", "done", ACTION_PARAM)
        self.add_slot("output", "output", "string")
        
        # Initialize data with default values matching the TypeScript version
        self.data = {
            "max_length": 128,
            "max_context_length": 2048,
            "_output": ""
        }
    
    @staticmethod
    def route() -> str:
        return "llm/text_generator"
    
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
        
        # First try to get prompt from the dedicated "prompt" slot
        prompt = await self.pull_data("prompt")
        
        # If no prompt from slot, check if params contains a string
        if not prompt and params and isinstance(params, str):
            prompt = params
        
        if not conn:
            print("ERROR: Missing required input (api_connection)")
            await self.set_state(NodeState.ERROR)
            return
        
        if not prompt or not isinstance(prompt, str):
            print("ERROR: Missing required input (prompt) - no string found in prompt slot or params")
            await self.set_state(NodeState.ERROR)
            return
        
        # Prepare settings for the API request
        settings = {
            "max_context_length": self.data["max_context_length"],
            "max_length": self.data["max_length"],
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
            "prompt": prompt,
        }
        
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
                    
                    # Extract the generated text
                    # generated_text = json_response["choices"][0]["message"]["content"]
                    # This generator uses Text Completion as opposed to chat completion
                    generated_text = json_response["results"][0]["text"]
                    self.data["_output"] = generated_text
                    
                    # Set to DONE before activating the next slot
                    await self.set_state(NodeState.DONE)
                    
                    # Trigger the done output slot with the generated text
                    await self.activate_slot("done", generated_text)
                    
        except Exception as e:
            print(f"ERROR in TextGeneratorNode: {e}")
            self.data["_output"] = f"Error: {str(e)}"
            await self.set_state(NodeState.ERROR)