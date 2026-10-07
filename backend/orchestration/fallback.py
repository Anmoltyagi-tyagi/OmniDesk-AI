from orchestration.models import RoutingResult


class FallbackHandler:

    def create_clarification(
        self,
        routing: RoutingResult
    ) -> str:

        if routing.clarification_question:
            return routing.clarification_question

        return (
            "I'm not sure which department can best handle "
            "your request. Could you provide a little more detail?"
        )

    def create_failure_message(self, domain: str) -> str:

        return (
            f"I couldn't retrieve information from the {domain} "
            "knowledge system right now. Please try again later "
            "or contact the appropriate support team."
        )
