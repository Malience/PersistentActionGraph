from nodes.CustomNode import CustomNode
from nodes.NodeState import NodeState
from nodes.SlotType import ACTION, ACTION_PARAM
from FlowEngine import FlowEngine
import random
import re


class DiceRollerNode(CustomNode):
    def __init__(self, _engine: FlowEngine, _id: str, _nodetype: str):
        super().__init__(_engine, _id, _nodetype, "Dice Roller")
        
        # Input slots
        self.add_slot("input", "roll", ACTION)
        self.add_slot("input", "dice_string", "string")
        
        # Output slots
        self.add_slot("output", "rolled", ACTION_PARAM)
        self.add_slot("output", "result", "int")
        
        # Default data with dice string
        self.data = {
            "dice_string": "1d6",
            "_result": 0
        }
    
    @staticmethod
    def route() -> str:
        return "utility/dice_roller"
    
    async def slot_activated(self, slot: str, params) -> None:
        if slot == "roll":
            await self.roll_dice(params)
    
    async def data_pulled(self, slot):
        if slot == "result":
            await self.set_state(NodeState.DONE)
            return self.data["_result"]
    
    async def receive_signal(self, signal: str, params):
        if signal == "roll":
            await self.roll_dice()
    
    async def roll_dice(self, params=None):
        await self.set_state(NodeState.PROCESSING)
        
        # Get dice string - prioritize input slot over frontend data
        input_dice_string = await self.pull_data("dice_string")
        if input_dice_string is not None:
            dice_string = input_dice_string
        else:
            dice_string = self.data.get("dice_string", "1d6")
        
        # Parse and roll the dice
        result = self._parse_and_roll_dice(dice_string)
        
        # Update data with roll results
        self.data["_result"] = result
        
        await self.set_state(NodeState.DONE)
        
        # Sync the updated data to frontend
        await self.sync()
        
        # Trigger the rolled output with the result
        await self.activate_slot("rolled", result)
    
    def _parse_and_roll_dice(self, dice_string: str) -> int:
        """Parse a D&D-style dice string and roll the dice."""
        try:
            # Remove whitespace and convert to lowercase
            dice_string = dice_string.replace(" ", "").lower()
            
            # Use regex to split by + and - while keeping the operators
            import re
            parts = re.split(r'([+-])', dice_string)
            
            # If no operators found, treat as single part
            if len(parts) == 1:
                parts = [parts[0]]
            
            total = 0
            current_operator = '+'
            
            for part in parts:
                if part in ['+', '-']:
                    current_operator = part
                    continue
                
                # Check if it's a dice expression (contains 'd')
                if 'd' in part:
                    # Split into count and sides
                    count_str, sides_str = part.split('d', 1)
                    
                    # Handle empty count (default to 1)
                    count = int(count_str) if count_str else 1
                    sides = int(sides_str)
                    
                    # Roll the dice
                    dice_total = 0
                    for _ in range(count):
                        dice_total += random.randint(1, sides)
                    
                    # Apply the operator
                    if current_operator == '+':
                        total += dice_total
                    else:  # current_operator == '-'
                        total -= dice_total
                else:
                    # It's a static modifier
                    modifier = int(part)
                    
                    # Apply the operator
                    if current_operator == '+':
                        total += modifier
                    else:  # current_operator == '-'
                        total -= modifier
            
            return total
            
        except (ValueError, IndexError):
            # If parsing fails, return a simple d6 roll
            print(f"ERROR: Invalid dice string format: {dice_string}")
            return random.randint(1, 6)