import asyncio

from app.agent.runtime import (
    run_turn,
)


async def main():

    result = await run_turn(
        "چند تسک باز داریم؟"
    )

    print(
        result.get("final_answer")
    )


if __name__ == "__main__":

    asyncio.run(
        main()
    )
