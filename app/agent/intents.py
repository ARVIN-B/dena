from enum import Enum


class Intent(str, Enum):

    STATS = "stats"
    SEARCH = "search"
    ANALYTICS = "analytics"
    ACTION = "action"
    MULTI_STEP = "multi_step"
    CLARIFICATION = "clarification"
    UNKNOWN = "unknown"