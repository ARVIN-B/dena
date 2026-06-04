class HumanFeedback:

    @staticmethod
    def requires_feedback(
        state,
    ):

        if state.get(
            "clarification_needed"
        ):
            return True

        return False