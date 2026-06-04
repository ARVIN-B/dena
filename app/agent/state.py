from typing import Optional
from typing_extensions import TypedDict


class AgentState(TypedDict):
    user_query: str
    selected_tool: Optional[str]
    tool_result: Optional[int]
    final_answer: Optional[str]