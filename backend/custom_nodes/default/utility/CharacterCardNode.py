import json
import base64
from io import BytesIO
from PIL import Image

from nodes.NodeState import NodeState
from nodes.CustomNode import CustomNode
from nodes.SlotType import ACTION_PARAM
from FlowEngine import FlowEngine


class CharacterCardNode(CustomNode):
    def __init__(self, _engine: FlowEngine, _id: str, _nodetype: str):
        super().__init__(_engine, _id, _nodetype, "Character Card")

        # Output slots
        self.add_slot("output", "on_load", ACTION_PARAM)  # Trigger when image is loaded
        self.add_slot("output", "character_data", "json")  # Character JSON data
        
        # Initialize data
        self.data = {
            "character_data": {},
        }
    
    @staticmethod
    def route() -> str:
        return "utility/character_card"
    
    async def receive_signal(self, signal: str, params):
        if signal == "image_dropped":
            await self.process_image(params)
    
    async def process_image(self, image_data: str):
        """Process dropped image and extract character data"""
        await self.set_state(NodeState.PROCESSING)
        
        try:
            # Extract base64 data (remove data:image/png;base64, prefix if present)
            if image_data.startswith('data:image'):
                image_data = image_data.split(',', 1)[1]
            
            # Decode base64 image
            image_bytes = base64.b64decode(image_data)
            image = Image.open(BytesIO(image_bytes))

            char_data = base64.b64decode(image.info['chara'])
            character_json = json.loads(char_data)['data']
            
            if character_json:
                # Update node data
                self.data["character_data"] = character_json
                
                # Sync data to frontend
                await self.sync()
                await self.set_state(NodeState.DONE)
                
                # Trigger output slots
                await self.activate_slot("on_load", character_json)
                
            else:
                # No character data found
                self.data["character_data"] = {}
                await self.sync()
                await self.set_state(NodeState.ERROR)
                
        except Exception as e:
            print(f"ERROR in CharacterCardNode: {e}")
            self.data["character_name"] = f"Error: {str(e)}"
            await self.sync()
            await self.set_state(NodeState.ERROR)
    
    async def data_pulled(self, slot: str):
        """Handle data pulls from output slots"""
        if slot == "character_data":
            await self.set_state(NodeState.DONE)
            return self.data["character_data"]
        
        return None