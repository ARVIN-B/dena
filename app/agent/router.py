from app.agent.state import AgentState


def route_after_planner(state: AgentState):
    if state.get("selected_tool"):
        return "tool"
    return "response"