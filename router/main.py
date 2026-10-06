"""FastAPI application entry point for the OmniDesk-AI Router.

Exposes:
- POST /route: Accepts natural-language query and returns RoutingResult
- GET /health: Simple health and diagnostics check
"""
from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, HTTPException, status

from .router import get_router, route_query
from .schemas import HealthResponse, RouteRequest, RoutingResult

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("omnidesk.api")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Startup and shutdown lifecycle."""
    logger.info("Initializing OmniDesk-AI Router...")
    get_router()  # warm up classifier and vectorizer
    logger.info("Router initialization complete.")
    yield


app = FastAPI(
    title="OmniDesk-AI Routing Service",
    description="Enterprise domain and multi-intent routing engine for OmniDesk-AI RAG assistant.",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check() -> HealthResponse:
    """Return the health status of the routing service."""
    router = get_router()
    return HealthResponse(
        status="healthy",
        service="OmniDesk-AI Router",
        classifier=router.classifier.name,
        version="1.0.0",
    )


@app.post("/route", response_model=RoutingResult, tags=["Routing"])
async def route_endpoint(request: RouteRequest) -> RoutingResult:
    """Classify and route an employee natural-language query.

    Returns detected domain routes, sub-queries, and confidence scores,
    or a clarification question if the request is ambiguous or confidence is low.
    """
    clean_query = request.query.strip()
    if not clean_query:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Query string cannot be empty or blank.",
        )

    try:
        result = route_query(clean_query)
        return result
    except ValueError as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ex),
        )
    except Exception as ex:
        logger.exception("Unexpected error during query routing: %s", ex)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal error processing routing request.",
        )
