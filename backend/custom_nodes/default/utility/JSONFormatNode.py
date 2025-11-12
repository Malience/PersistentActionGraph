from nodes.NodeState import NodeState
from nodes.CustomNode import CustomNode
from FlowEngine import FlowEngine
import re
import json


def _extract_value(data, key_path):
    """Extract value from nested JSON using dot notation or direct key access."""
    if not isinstance(data, dict):
        return None
    
    # Handle dot notation for nested keys
    if '.' in key_path:
        keys = key_path.split('.')
        current = data
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return None
        return current
    else:
        # Direct key access
        return data.get(key_path)
    
def _format_value(value):
    """Convert any value to string for formatting."""
    if value is None:
        return ""
    elif isinstance(value, (dict, list)):
        # Convert complex objects to JSON string
        try:
            return json.dumps(value)
        except:
            return str(value)
    else:
        return str(value)

class JSONFormatNode(CustomNode):
    def __init__(self, _engine: FlowEngine, _id: str, _nodetype: str):
        super().__init__(_engine, _id, _nodetype, "JSON Format")

        self.add_slot("input", "json_data", "json")
        self.add_slot("input", "template", "string")
        self.add_slot("output", "formatted", "string")
        self.data = {}
    
    @staticmethod
    def route() -> str:
        return "utility/json_format"
    
    async def data_pulled(self, slot):
        if slot == "formatted":
            await self.set_state(NodeState.DONE)
            json_data = await self.pull_data("json_data")
            template = await self.pull_data("template")
            
            if template is None:
                return None
            
            if json_data is None:
                json_data = {}
            
            # Use regex to find all {{key}} patterns
            pattern = r'\{\{([^}]+)\}\}'
            
            def replace_match(match):
                key = match.group(1).strip()
                value = _extract_value(json_data, key)
                if value is None:
                    # Return the original placeholder if key not found
                    return match.group(0)
                return _format_value(value)
            
            # Replace all matches in the template
            formatted_string = re.sub(pattern, replace_match, template)
            
            return formatted_string