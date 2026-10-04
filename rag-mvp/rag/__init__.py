"""OmniDesk-AI RAG module.

Public contract (the only thing other modules should import):

    from rag import retrieve
    chunks = retrieve(domain="IT", query="...", top_k=5)   # -> list[RetrievedChunk]
"""
from .models import Chunk, RetrievedChunk
from .retriever import retrieve

__all__ = ["retrieve", "RetrievedChunk", "Chunk"]
