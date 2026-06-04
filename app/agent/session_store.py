from copy import deepcopy
from uuid import uuid4


DEFAULT_SESSION_STATE = {
    "memory_context": [],
    "execution_history": [],
    "metadata": {},
}


class SessionStore:

    _sessions = {}

    @classmethod
    def normalize_conversation_id(
        cls,
        conversation_id=None,
    ):

        if conversation_id:
            return str(conversation_id)

        return str(
            uuid4()
        )

    @classmethod
    def load(
        cls,
        conversation_id=None,
    ):

        conversation_id = cls.normalize_conversation_id(
            conversation_id
        )

        session = deepcopy(
            cls._sessions.get(
                conversation_id,
                DEFAULT_SESSION_STATE,
            )
        )

        return {
            "conversation_id": conversation_id,
            "memory_context": session.get(
                "memory_context",
                [],
            ),
            "execution_history": session.get(
                "execution_history",
                [],
            ),
            "metadata": session.get(
                "metadata",
                {},
            ),
        }

    @classmethod
    def save(
        cls,
        conversation_id,
        state,
    ):

        conversation_id = cls.normalize_conversation_id(
            conversation_id
        )

        cls._sessions[conversation_id] = {
            "memory_context": deepcopy(
                state.get(
                    "memory_context",
                    [],
                )
            ),
            "execution_history": deepcopy(
                state.get(
                    "execution_history",
                    [],
                )
            ),
            "metadata": deepcopy(
                state.get(
                    "metadata",
                    {},
                )
            ),
        }

        return conversation_id
