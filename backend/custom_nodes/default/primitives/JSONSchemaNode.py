from nodes.NodeState import NodeState
from nodes.CustomNode import CustomNode
from FlowEngine import FlowEngine
import json


class JSONSchemaNode(CustomNode):
    def __init__(self, _engine: FlowEngine, _id: str, _nodetype: str):
        super().__init__(_engine, _id, _nodetype, "JSON Schema")

        self.add_slot("input", "properties", "json_schema[]")

        self.add_slot("output", "schema", "json_schema")
        self.data = {
            "name": "",
            "description": "",
            "properties": "[]",
            "required": "",
        }
    
    @staticmethod
    def route() -> str:
        return "primitives/json_schema"
    
    async def data_pulled(self, slot):
        if slot == "schema":
            await self.set_state(NodeState.DONE)

            external_props = await self.pull_data("properties")

            try:
                # Build the JSON schema from the data
                schema = {
                    "name": self.data["name"],
                    "type": "object",
                }

                if self.data["description"]: schema["description"] = self.data["description"],
                
                # Parse properties array
                properties = {}
                if self.data["properties"]:
                    try:
                        properties_list = json.loads(self.data["properties"])
                        for prop in properties_list:
                            if prop.get("name") and prop.get("type"):
                                prop_schema = {"type": prop["type"]}
                                
                                # Add description if provided
                                if prop.get("description"):
                                    prop_schema["description"] = prop["description"]
                                
                                # Add custom options if provided
                                if prop.get("custom"):
                                    try:
                                        custom_options = json.loads(prop["custom"])
                                        prop_schema.update(custom_options)
                                    except json.JSONDecodeError:
                                        # Ignore invalid custom options
                                        pass
                                
                                properties[prop["name"]] = prop_schema
                    except json.JSONDecodeError:
                        # Return nothing if properties JSON is invalid
                        return None
                
                if external_props:
                    for prop in external_props:
                        name = prop["name"]
                        del prop["name"]
                        p = {
                            name: prop
                        }
                        properties.update(p)

                print(properties)
                schema["properties"] = properties
                
                # Parse required fields
                if self.data["required"]:
                    required_list = [name.strip() for name in self.data["required"].split(",") if name.strip()]
                    schema["required"] = required_list
                
                return schema
            except Exception:
                # Return empty schema on any error
                return None
        
        return None