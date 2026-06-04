from app.agent.state import AgentState


async def reflection_node(
    state: AgentState,
) -> AgentState:

    try:

        tool_results = state.get(
            "tool_results",
            []
        )

        execution_history = state.get(
            "execution_history",
            []
        )

        if not tool_results:

            state["error"] = (
                "No tool results found"
            )

            return state

        failed_tools = []

        successful_tools = []

        for result in tool_results:

            if result.get(
                "success"
            ):
                successful_tools.append(
                    result
                )

            else:
                failed_tools.append(
                    result
                )

        reflection = {
            "successful_tools": len(
                successful_tools
            ),
            "failed_tools": len(
                failed_tools
            ),
            "needs_retry": False,
            "needs_clarification": False,
        }

        if (
            len(successful_tools)
            == 0
        ):

            reflection[
                "needs_retry"
            ] = True

        for failed in failed_tools:

            error = str(
                failed.get(
                    "error",
                    ""
                )
            ).lower()

            if (
                "required"
                in error
            ):

                reflection[
                    "needs_clarification"
                ] = True

        execution_history.append(
            {
                "node": "reflection",
                "reflection": reflection,
            }
        )

        state[
            "execution_history"
        ] = execution_history

        metadata = state.get(
            "metadata",
            {}
        )

        metadata[
            "reflection"
        ] = reflection

        state[
            "metadata"
        ] = metadata

        if reflection[
            "needs_clarification"
        ]:

            state[
                "clarification_needed"
            ] = True

            state[
                "clarification_question"
            ] = (
                "اطلاعات بیشتری برای انجام درخواست لازم است."
            )

        return state

    except Exception as e:

        state["error"] = str(
            e
        )

        return state