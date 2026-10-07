from typing import List, Optional
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    session_id: str
    message: str


class Intent(BaseModel):
    domain: str
    query: str
    confidence: float = Field(ge=0.0, le=1.0)


class RoutingResult(BaseModel):
    intents: List[Intent]
    requires_clarification: bool = False
    clarification_question: Optional[str] = None


class Source(BaseModel):
    title: str
    page: Optional[int] = None
    url: Optional[str] = None


class RAGResult(BaseModel):
    domain: str
    answer: str
    sources: List[Source] = []
    confidence: float = 0.0
    success: bool = True
    error: Optional[str] = None


class FinalResponse(BaseModel):
    answer: str
    domains: List[str]
    sources: List[Source]
    status: str
