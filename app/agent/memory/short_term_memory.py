MAX_MEMORY_ITEMS = 20


class ShortTermMemory:

    @staticmethod
    def load(
        state,
    ):

        return state.get(
            "memory_context",
            []
        )

    @staticmethod
    def save(
        state,
        memory_item,
    ):

        memory = state.get(
            "memory_context",
            []
        )

        memory.append(
            memory_item
        )

        memory = memory[
            -MAX_MEMORY_ITEMS:
        ]

        state[
            "memory_context"
        ] = memory

        return state