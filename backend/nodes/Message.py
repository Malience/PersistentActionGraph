from enum import Enum
from typing import TypedDict


class MessageRole(Enum):
    USER = "user"
    SYSTEM = "system"
    ASSISTANT = "assistant"


class Message(TypedDict):
    role: str
    content: str


def create_message(role: MessageRole, content: str) -> Message:
    """Create a validated message structure."""
    if not isinstance(content, str):
        raise ValueError("Message content must be a string")
    
    if role not in MessageRole:
        raise ValueError(f"Invalid role: {role}. Must be one of {[r.value for r in MessageRole]}")
    
    return {
        "role": role.value,
        "content": content
    }


def validate_message(message: dict) -> bool:
    """Validate that a dictionary conforms to the Message structure."""
    if not isinstance(message, dict):
        return False
    
    if "role" not in message or "content" not in message:
        return False
    
    if not isinstance(message["role"], str) or not isinstance(message["content"], str):
        return False
    
    valid_roles = [role.value for role in MessageRole]
    return message["role"] in valid_roles