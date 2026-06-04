from langgraph.graph import StateGraph, END

from app.agent.state import AgentState
from app.agent.nodes import (
    planner_node,
    tool_node,
    response_node
)

from app.agent.router import route_after_planner


graph = StateGraph(AgentState)

graph.add_node("planner", planner_node)
graph.add_node("tool", tool_node)
graph.add_node("response", response_node)

graph.set_entry_point("planner")

graph.add_conditional_edges(
    "planner",
    route_after_planner,
    {
        "tool": "tool",
        "response": "response"
    }
)
graph.add_edge("tool", "response")
graph.add_edge("response", END)


agent_graph = graph.compile()