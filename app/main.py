from app.agent.graph import agent_graph

result = agent_graph.invoke(
    {
        "user_query": "چند تسک باز داریم؟"
    }
)

print(result["final_answer"])