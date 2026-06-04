from app.agent.state import AgentState


async def clarification_node(
    state: AgentState,
) -> AgentState:

    if not state.get(
        "clarification_needed",
        False,
    ):
        return state

    question = state.get(
        "clarification_question"
    )

    if not question:

        question = (
            "لطفاً درخواست خود را واضح‌تر بیان کنید."
        )

    metadata = state.get(
        "metadata",
        {}
    )

    clarification_history = metadata.get(
        "clarification_history",
        []
    )

    clarification_history.append(
        {
            "user_query": state.get(
                "user_query"
            ),
            "question": question,
            "context": state.get(
                "clarification_context",
                {},
            ),
        }
    )

    metadata[
        "clarification_history"
    ] = clarification_history

    state[
        "metadata"
    ] = metadata

    state[
        "final_answer"
    ] = question

    return state