from app.agent.constants import (
    MAX_RETRY_COUNT,
)


def route_after_planner(
    state,
):

    if state.get(
        "error"
    ):
        return "error"

    if state.get(
        "clarification_needed"
    ):
        return "clarification"

    return "tool_executor"


def route_after_clarification(
    state,
):

    return "__end__"


def route_after_tool_executor(
    state,
):

    if state.get(
        "error"
    ):
        return "error"

    return "reflection"


def route_after_reflection(
    state,
):

    if state.get(
        "error"
    ):
        return "error"

    reflection = (
        state.get(
            "metadata",
            {}
        )
        .get(
            "reflection",
            {}
        )
    )

    if reflection.get(
        "needs_clarification"
    ):
        return "clarification"

    if reflection.get(
        "needs_retry"
    ):

        retry_count = (
            state.get(
                "metadata",
                {}
            )
            .get(
                "retry_count",
                0
            )
        )

        if retry_count >= (
            MAX_RETRY_COUNT
        ):
            return "error"

        metadata = state.get(
            "metadata",
            {}
        )

        metadata[
            "retry_count"
        ] = retry_count + 1

        state[
            "metadata"
        ] = metadata

        return "tool_executor"

    return "memory"


def route_after_memory(
    state,
):

    if state.get(
        "error"
    ):
        return "error"

    return "response"


def route_after_response(
    state,
):

    return "__end__"


def route_after_error(
    state,
):

    return "__end__"