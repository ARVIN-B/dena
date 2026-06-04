from typing import Optional, Any, List
from typing_extensions import TypedDict


class AgentState(TypedDict, total=False):

    conversation_id: str
    user_query: str
    intent: str
    plan: list[dict]
    current_step: int
    tool_calls: list[dict]
    tool_results: list[Any]
    clarification_needed: bool
    clarification_question: str
    clarification_context: dict
    final_answer: str
    error: str
    execution_history: list
    memory_context: list
    metadata: dict
