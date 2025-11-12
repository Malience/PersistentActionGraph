import enum

class NodeState(enum.Enum):
    NEUTRAL = 0
    DONE = 1
    PROCESSING = 2
    ERROR = 3