import json

from app.agent.state import AgentState
from app.llm.llm import ask_llm


RESPONSE_SYSTEM_PROMPT = """
You are an intelligent Persian assistant.

Your job is to generate the final answer.

Rules:

1. Always answer in Persian.
2. Use tool results only.
3. Do not invent information.
4. Be concise and professional.
5. If multiple tool results exist, combine them.
6. If all tools failed, explain the error.
"""


async def response_node(
    state: AgentState,
) -> AgentState:

    try:

        tool_results = state.get(
            "tool_results",
            [],
        )

        if not tool_results:

            state["final_answer"] = (
                "نتیجه‌ای برای نمایش وجود ندارد."
            )

            return state

        success_results = [
            result
            for result in tool_results
            if result.get("success")
        ]

        failed_results = [
            result
            for result in tool_results
            if not result.get("success")
        ]

        if not success_results:

            errors = []

            for result in failed_results:

                errors.append(
                    result.get(
                        "error",
                        "Unknown Error",
                    )
                )

            state["final_answer"] = (
                "خطا در اجرای درخواست:\n"
                + "\n".join(errors)
            )

            return state

        prompt = f"""
User Query:

{state['user_query']}

Tool Results:

{json.dumps(
    success_results,
    ensure_ascii=False,
    indent=2,
    default=str,
)}

Generate final Persian answer.
"""

        final_answer = await ask_llm(
            prompt,
            system_message=(
                RESPONSE_SYSTEM_PROMPT
            ),
        )

        state["final_answer"] = (
            final_answer
        )

        return state

    except Exception as e:

        state["error"] = str(
            e
        )

        return state