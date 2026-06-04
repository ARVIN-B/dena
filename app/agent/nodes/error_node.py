from datetime import datetime

from app.agent.state import AgentState


async def error_node(
    state: AgentState,
) -> AgentState:

    error_message = (
        state.get("error")
        or "Unknown Error"
    )

    metadata = state.get(
        "metadata",
        {}
    )

    execution_history = (
        metadata.get(
            "execution_history",
            []
        )
    )

    execution_history.append(
        {
            "timestamp": datetime.utcnow().isoformat(),
            "error": error_message,
            "query": state.get(
                "user_query"
            ),
        }
    )

    metadata[
        "execution_history"
    ] = execution_history

    state[
        "metadata"
    ] = metadata

    planner_error_keywords = [
        "Unknown tool",
        "Invalid source",
        "Invalid metric",
    ]

    llm_error_keywords = [
        "OpenAI",
        "LLM",
        "Model",
        "Token",
        "Rate limit",
        "API",
    ]

    tool_error_keywords = [
        "KeyError",
        "ValueError",
        "TypeError",
        "AttributeError",
        "IndexError",
    ]

    if any(
        keyword.lower()
        in error_message.lower()
        for keyword in planner_error_keywords
    ):

        state["final_answer"] = (
            "در تفسیر درخواست مشکل به وجود آمد. "
            "لطفاً درخواست را واضح‌تر بیان کنید."
        )

        return state

    if any(
        keyword.lower()
        in error_message.lower()
        for keyword in llm_error_keywords
    ):

        state["final_answer"] = (
            "در ارتباط با مدل زبانی مشکلی رخ داد. "
            "لطفاً مجدداً تلاش کنید."
        )

        return state

    if any(
        keyword.lower()
        in error_message.lower()
        for keyword in tool_error_keywords
    ):

        state["final_answer"] = (
            "در اجرای عملیات درخواستی خطایی رخ داد."
        )

        return state

    state["final_answer"] = (
        "خطایی در پردازش درخواست رخ داد."
    )

    return state