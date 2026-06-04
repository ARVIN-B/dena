from app.agent.state import AgentState
from app.agent.tool_registry import TOOLS


async def tool_executor_node(
    state: AgentState,
) -> AgentState:

    try:

        plan = state.get(
            "plan",
            []
        )

        tool_calls = []
        tool_results = []

        for index, step in enumerate(plan):

            tool_name = step.get(
                "tool"
            )

            params = step.get(
                "params",
                {}
            )
            effective_params = dict(
                params
            )

            if (
                tool_name == "create_task"
                and not effective_params.get("assignee_id")
                and not effective_params.get("assignee_name")
            ):

                for previous_result in reversed(
                    tool_results
                ):

                    if not previous_result.get(
                        "success"
                    ):
                        continue

                    if previous_result.get(
                        "tool"
                    ) != "search":
                        continue

                    search_result = previous_result.get(
                        "result",
                        [],
                    )

                    if (
                        isinstance(
                            search_result,
                            list,
                        )
                        and len(search_result) == 1
                        and isinstance(
                            search_result[0],
                            dict,
                        )
                        and search_result[0].get("id") is not None
                    ):
                        effective_params[
                            "assignee_id"
                        ] = search_result[0]["id"]
                        break

            if tool_name not in TOOLS:

                tool_results.append(
                    {
                        "step": index,
                        "tool": tool_name,
                        "success": False,
                        "error": (
                            f"Unknown tool: "
                            f"{tool_name}"
                        ),
                    }
                )

                continue

            tool = TOOLS[
                tool_name
            ]

            try:

                result = tool(
                    **effective_params
                )

                tool_calls.append(
                    {
                        "step": index,
                        "tool": tool_name,
                        "params": effective_params,
                    }
                )

                tool_results.append(
                    {
                        "step": index,
                        "tool": tool_name,
                        "success": True,
                        "result": result,
                    }
                )

            except Exception as e:

                tool_results.append(
                    {
                        "step": index,
                        "tool": tool_name,
                        "success": False,
                        "error": str(e),
                    }
                )

        state["tool_calls"] = (
            tool_calls
        )

        state["tool_results"] = (
            tool_results
        )

        state["current_step"] = (
            len(plan)
        )

        return state

    except Exception as e:

        state["error"] = str(
            e
        )

        return state
