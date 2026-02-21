"""Nova API routes."""
from __future__ import annotations

import json
import logging
from typing import Annotated

from fastapi import APIRouter, Depends
from sse_starlette.sse import EventSourceResponse

from app.agents.revit_agent import run_agent_stream
from app.auth.dependencies import CurrentUser
from app.config import Settings, get_settings
from app.models.schemas import ChatRequest, StreamChunk, ToolResultRequest
from app.session import session_manager

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["nova"])


# ── Health ───────────────────────────────────────────────────────────────────


@router.get("/health", include_in_schema=False)
async def health() -> dict[str, str]:
    return {"status": "ok"}


# ── Chat (streaming) ─────────────────────────────────────────────────────────


@router.post("/chat/stream")
async def chat_stream(
    request: ChatRequest,
    current_user: CurrentUser,
    settings: Annotated[Settings, Depends(get_settings)],
) -> EventSourceResponse:
    """
    Start a streaming agentic conversation with the Revit AI agent.

    The response is a Server-Sent Events (SSE) stream.  Each event has:
    - ``event``: chunk type ("token" | "tool_call" | "tool_result" | "done" | "error")
    - ``data``:  JSON-encoded ``StreamChunk``

    The Revit plugin should consume this stream and render tokens progressively.
    """
    logger.info("Chat request from sub=%s session=%s", current_user.sub, request.session_id)

    async def event_generator():
        async for chunk in run_agent_stream(
            message=request.message,
            context=request.context,
            settings=settings,
            session_id=request.session_id,
        ):
            yield {
                "event": chunk.type,
                "data": json.dumps(chunk.model_dump(exclude_none=True)),
            }

    return EventSourceResponse(event_generator())


# ── Tool result (plugin → backend) ──────────────────────────────────────────


@router.post("/chat/{session_id}/tool_result", status_code=200)
async def submit_tool_result(
    session_id: str,
    payload: ToolResultRequest,
    current_user: CurrentUser,  # noqa: ARG001
) -> dict[str, str]:
    """
    Called by the Revit plugin after it has executed a tool call in Revit.

    The plugin must supply the ``call_id`` it received in the ``tool_call``
    SSE event, plus the JSON ``result`` produced by Revit.
    """
    session = session_manager.get(session_id)
    if session is None:
        from fastapi import HTTPException, status
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")

    resolved = session.resolve_call(payload.call_id, payload.result)
    if not resolved:
        from fastapi import HTTPException, status
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unknown or already-resolved call_id")

    return {"status": "ok"}


# ── Tools introspection ───────────────────────────────────────────────────────


@router.get("/tools")
async def list_tools(
    current_user: CurrentUser,  # noqa: ARG001
) -> list[dict[str, str]]:
    """Return the list of Revit tools available to the agent."""
    from app.tools import ALL_REVIT_TOOLS

    return [
        {
            "name": t.name,
            "description": (t.description or "").strip().split("\n")[0],
        }
        for t in ALL_REVIT_TOOLS
    ]
