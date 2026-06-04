import asyncio

from app.agent.graph import (
    build_graph,
)


graph = build_graph()


async def main():

    print("Agent Ready")
    print("type exit to quit")

    while True:

        query = input(
            "\nUser: "
        )

        if query.lower() == "exit":
            break

        result = await graph.ainvoke(
            {
                "user_query": query,
                "memory_context": [],
                "execution_history": [],
                "metadata": {},
            }
        )

        print(
            "\nAssistant:"
        )

        print(
            result.get(
                "final_answer"
            )
        )

        print(
            "\nState:"
        )

        print(result)


if __name__ == "__main__":

    asyncio.run(
        main()
    )