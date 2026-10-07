from typing import List

from orchestration.models import RAGResult, Source


class ResponseSynthesizer:

    async def synthesize(
        self,
        user_query: str,
        results: List[RAGResult]
    ) -> tuple[str, List[Source]]:

        successful_results = [
            result
            for result in results
            if result.success
        ]

        if not successful_results:
            return (
                "I was unable to retrieve information for your request.",
                []
            )

        response_parts = []
        sources = []

        for result in successful_results:

            response_parts.append(
                f"**{result.domain}:** {result.answer}"
            )

            sources.extend(result.sources)

        final_answer = "\n\n".join(response_parts)

        return final_answer, sources
