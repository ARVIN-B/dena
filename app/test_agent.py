import asyncio

from app.agent.runtime import (
    run_turn,
)


async def main():

    print("Agent Ready")
    print("type exit to quit")

    conversation_id = None

    while True:

        query = input(
            "\nUser: "
        )

        if query.lower() == "exit":
            break

        result = await run_turn(
            query,
            conversation_id=conversation_id,
        )

        conversation_id = result.get(
            "conversation_id"
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
