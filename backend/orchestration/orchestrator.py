import asyncio
from typing import List

from orchestration.models import (
    ChatRequest,
    FinalResponse,
    Intent,
    RAGResult,
    RoutingResult
)

from orchestration.domain_executor import DomainExecutor
from orchestration.context_manager import ContextManager
from orchestration.response_synthesizer import ResponseSynthesizer
from orchestration.fallback import FallbackHandler


class OmniOrchestrator:

    CONFIDENCE_THRESHOLD = 0.70

    def __init__(self):

        self.domain_executor = DomainExecutor()
        self.context_manager = ContextManager()
        self.synthesizer = ResponseSynthesizer()
        self.fallback = FallbackHandler()

    async def orchestrate(
        self,
        request: ChatRequest,
        routing: RoutingResult
    ) -> FinalResponse:

        # ---------------------------------------
        # 1. Store user message
        # ---------------------------------------

        self.context_manager.add_message(
            session_id=request.session_id,
            role="user",
            content=request.message
        )

        # ---------------------------------------
        # 2. Check clarification requirement
        # ---------------------------------------

        if routing.requires_clarification:

            question = self.fallback.create_clarification(
                routing
            )

            self.context_manager.add_message(
                request.session_id,
                "assistant",
                question
            )

            return FinalResponse(
                answer=question,
                domains=[],
                sources=[],
                status="clarification_required"
            )

        # ---------------------------------------
        # 3. Validate confidence
        # ---------------------------------------

        valid_intents = [
            intent
            for intent in routing.intents
            if intent.confidence >= self.CONFIDENCE_THRESHOLD
        ]

        if not valid_intents:

            question = (
                "Could you provide more details so I can "
                "route your request to the correct department?"
            )

            return FinalResponse(
                answer=question,
                domains=[],
                sources=[],
                status="clarification_required"
            )

        # ---------------------------------------
        # 4. Execute domain RAGs concurrently
        # ---------------------------------------

        tasks = [
            self.domain_executor.execute(intent)
            for intent in valid_intents
        ]

        results: List[RAGResult] = await asyncio.gather(
            *tasks
        )

        # ---------------------------------------
        # 5. Collect successful domains
        # ---------------------------------------

        domains = [
            result.domain
            for result in results
            if result.success
        ]

        # ---------------------------------------
        # 6. Generate unified response
        # ---------------------------------------

        answer, sources = await self.synthesizer.synthesize(
            user_query=request.message,
            results=results
        )

        # ---------------------------------------
        # 7. Store assistant response
        # ---------------------------------------

        self.context_manager.add_message(
            session_id=request.session_id,
            role="assistant",
            content=answer
        )

        # ---------------------------------------
        # 8. Return final response
        # ---------------------------------------

        status = (
            "resolved"
            if domains
            else "partial_failure"
        )

        return FinalResponse(
            answer=answer,
            domains=domains,
            sources=sources,
            status=status
        )
