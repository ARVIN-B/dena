from app.agent.graph import build_graph
from app.agent.session_store import SessionStore


graph = build_graph()


async def run_turn(
    message,
    conversation_id=None,
):

    state = SessionStore.load(
        conversation_id
    )

    state["user_query"] = message

    result = await graph.ainvoke(
        state
    )

    conversation_id = SessionStore.save(
        state.get("conversation_id"),
        result,
    )

    result["conversation_id"] = conversation_id

    return result
