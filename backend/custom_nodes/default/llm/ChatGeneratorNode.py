from nodes.CustomNode import CustomNode
from nodes.NodeState import NodeState
from nodes.SlotType import ACTION, ACTION_PARAM
from nodes.Message import Message, validate_message, create_message, MessageRole
from FlowEngine import FlowEngine
import aiohttp
import json


class ChatGeneratorNode(CustomNode):
    def __init__(self, _engine: FlowEngine, _id: str, _nodetype: str):
        super().__init__(_engine, _id, _nodetype, "Chat Generator")

        # Input slots
        self.add_slot("input", "activate", ACTION_PARAM)
        self.add_slot("input", "api_connection", "api_connection")
        self.add_slot("input", "settings", "json")
        self.add_slot("input", "messages", "message[]")
        
        # Output slots
        self.add_slot("output", "done", ACTION_PARAM)
        self.add_slot("output", "output", "message")
        
        # Initialize data with default values
        self.data = {
            "max_length": 128,
            "max_context_length": 2048,
            "_output": None
        }
    
    @staticmethod
    def route() -> str:
        return "llm/chat_generator"
    
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
        messages = await self.pull_data("messages")
        
        # If no messages from slot, check if params contains messages
        if not messages and params and isinstance(params, list):
            messages = params
        
        if not conn:
            print("ERROR: Missing required input (api_connection)")
            await self.set_state(NodeState.ERROR)
            return
        
        if not messages or not isinstance(messages, list):
            print("ERROR: Missing required input (messages) - no message array found in messages slot or params")
            await self.set_state(NodeState.ERROR)
            return
        
        # Validate all messages in the array
        for i, message in enumerate(messages):
            if not validate_message(message):
                print(f"ERROR: Invalid message at index {i}: {message}")
                await self.set_state(NodeState.ERROR)
                return
        
        # Prepare settings for the API request
        settings = {
            "max_context_length": self.data["max_context_length"],
            "max_completion_tokens": self.data["max_length"],
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
                    
                    # Extract the generated text and create a message
                    generated_text = json_response["choices"][0]["message"]["content"]
                    generated_message = create_message(MessageRole.ASSISTANT, generated_text)
                    self.data["_output"] = generated_message
                    
                    # Set to DONE before activating the next slot
                    await self.set_state(NodeState.DONE)
                    
                    # Trigger the done output slot with the generated message
                    await self.activate_slot("done", generated_message)
                    
        except Exception as e:
            print(f"ERROR in ChatGeneratorNode: {e}")
            self.data["_output"] = create_message(MessageRole.ASSISTANT, f"Error: {str(e)}")
            await self.set_state(NodeState.ERROR)