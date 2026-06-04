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
                    **params
                )

                tool_calls.append(
                    {
                        "step": index,
                        "tool": tool_name,
                        "params": params,
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