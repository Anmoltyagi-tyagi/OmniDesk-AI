import asyncio
from orchestration.models import Intent, RAGResult, Source


class DomainExecutor:

    def __init__(self):
        self.supported_domains = {
            "IT",
            "HR",
            "Finance",
            "Facilities"
        }

    async def execute(self, intent: Intent) -> RAGResult:
        """
        Execute the RAG corresponding to the requested domain.

        Later, replace the mock implementation with calls
        to the actual domain RAG services.
        """

        if intent.domain not in self.supported_domains:
            return RAGResult(
                domain=intent.domain,
                answer="Unsupported domain.",
                success=False,
                error=f"Domain '{intent.domain}' is not supported."
            )

        try:
            # Simulates an external RAG/API call
            await asyncio.sleep(0.1)

            return await self._mock_rag(intent)

        except Exception as exc:
            return RAGResult(
                domain=intent.domain,
                answer="Unable to retrieve information.",
                success=False,
                error=str(exc)
            )

    async def _mock_rag(self, intent: Intent) -> RAGResult:

        if intent.domain == "IT":
            return RAGResult(
                domain="IT",
                answer=(
                    "For VPN problems, restart the VPN client, "
                    "verify your credentials, and reconnect."
                ),
                sources=[
                    Source(
                        title="VPN Troubleshooting Guide",
                        page=4
                    )
                ],
                confidence=0.91
            )

        if intent.domain == "Finance":
            return RAGResult(
                domain="Finance",
                answer=(
                    "Travel reimbursement generally requires "
                    "submission of the expense claim along with "
                    "the required receipts."
                ),
                sources=[
                    Source(
                        title="Travel Reimbursement Policy",
                        page=7
                    )
                ],
                confidence=0.89
            )

        if intent.domain == "HR":
            return RAGResult(
                domain="HR",
                answer="HR policy information was retrieved.",
                sources=[
                    Source(title="Employee Handbook", page=12)
                ],
                confidence=0.88
            )

        if intent.domain == "Facilities":
            return RAGResult(
                domain="Facilities",
                answer="Facilities information was retrieved.",
                sources=[
                    Source(title="Facilities Guide", page=3)
                ],
                confidence=0.87
            )

        raise ValueError("Unknown domain")
