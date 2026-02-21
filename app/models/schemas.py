from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


# ── Request / Response schemas ───────────────────────────────────────────────


class ChatRequest(BaseModel):
    """Payload sent by the Revit plugin to start an agent run."""

    message: str = Field(..., description="Natural-language instruction for the Revit agent.")
    session_id: str | None = Field(None, description="Optional session identifier for context.")
    context: dict[str, Any] = Field(
        default_factory=dict,
        description="Optional Revit context (active document info, selected elements, etc.).",
    )


class StreamChunk(BaseModel):
    """A single server-sent event chunk."""

    type: str  # "token" | "tool_call" | "tool_result" | "done" | "error"
    content: str | None = None
    data: dict[str, Any] | None = None


class ToolResultRequest(BaseModel):
    """Payload the Revit plugin sends after executing a tool call."""

    call_id: str = Field(..., description="The call_id from the tool_call SSE event.")
    result: Any = Field(..., description="The JSON result returned by Revit.")


# ── JWT / Auth schemas ───────────────────────────────────────────────────────


class TokenClaims(BaseModel):
    """Validated claims extracted from the Auth0 JWT."""

    sub: str
    email: str | None = None
    provider: str  # must equal settings.revit_provider_claim_value
    raw: dict[str, Any] = Field(default_factory=dict, exclude=True)
