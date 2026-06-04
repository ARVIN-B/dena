import asyncio

from app.agent.graph import (
    build_graph,
)


graph = build_graph()


async def chat():

    while True:

        query = input(
            "\nUser: "
        )

        if query.lower() in [
            "exit",
            "quit",
        ]:
            break

        result = await graph.ainvoke(
            {
                "user_query": query,
            }
        )

        print(
            "\nAssistant:",
            result.get(
                "final_answer"
            ),
        )


if __name__ == "__main__":

    asyncio.run(
        chat()
    )