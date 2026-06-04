from app.agent.state import AgentState

from app.agent.memory.short_term_memory import (
    ShortTermMemory,
)


async def memory_node(
    state: AgentState,
) -> AgentState:

    try:

        memory_item = {
            "query": state.get(
                "user_query"
            ),
            "intent": state.get(
                "intent"
            ),
            "plan": state.get(
                "plan"
            ),
            "tool_results": state.get(
                "tool_results"
            ),
        }

        state = (
            ShortTermMemory.save(
                state,
                memory_item,
            )
        )

        execution_history = state.get(
            "execution_history",
            []
        )

        execution_history.append(
            {
                "node": "memory",
                "status": "saved",
            }
        )

        state[
            "execution_history"
        ] = execution_history

        return state

    except Exception as e:

        state["error"] = str(e)

        return state