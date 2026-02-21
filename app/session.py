"""
Session manager for Nova ↔ Revit plugin communication.

Each active chat session owns:
- ``sse_queue``    – events the backend wants to push to the plugin via SSE
- ``_pending``     – futures keyed by call_id, resolved when the plugin
                     POSTs back a tool result

Lifecycle:
  1.  Plugin opens SSE by calling POST /api/v1/chat/stream
  2.  Backend creates (or reuses) a session and launches the agent task
  3.  Agent calls a tool → tool registers a Future, emits tool_call via sse_queue
  4.  SSE generator streams tool_call to plugin
  5.  Plugin executes in Revit → POST /api/v1/chat/{session_id}/tool_result
  6.  Route resolves the Future → tool returns → agent continues
  7.  ``done`` sentinel is put in sse_queue → SSE generator closes
"""
from __future__ import annotations

import asyncio
import logging
import uuid
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)

# Sentinel that signals the SSE generator to close the stream
_STREAM_DONE = object()


@dataclass
class RevitSession:
    session_id: str
    sse_queue: asyncio.Queue = field(default_factory=asyncio.Queue)
    _pending: dict[str, asyncio.Future[Any]] = field(default_factory=dict)

    # ── Tool call registration ─────────────────────────────────────────────

    def register_call(self, call_id: str) -> asyncio.Future[Any]:
        """Create and store a Future that will be resolved by the plugin."""
        loop = asyncio.get_event_loop()
        fut: asyncio.Future[Any] = loop.create_future()
        self._pending[call_id] = fut
        return fut

    def resolve_call(self, call_id: str, result: Any) -> bool:
        """
        Called when the plugin POSTs a tool_result.
        Returns True if the call_id was found and resolved, False otherwise.
        """
        fut = self._pending.pop(call_id, None)
        if fut is None:
            logger.warning("resolve_call: unknown call_id=%r", call_id)
            return False
        if fut.done():
            logger.warning("resolve_call: future already done for call_id=%r", call_id)
            return False
        fut.set_result(result)
        return True

    def cancel_pending(self) -> None:
        """Cancel all pending futures (called on session teardown)."""
        for fut in self._pending.values():
            if not fut.done():
                fut.cancel()
        self._pending.clear()

    async def emit(self, event: dict[str, Any]) -> None:
        """Put an SSE event dict onto the queue."""
        await self.sse_queue.put(event)

    async def close(self) -> None:
        """Signal the SSE generator to finish."""
        await self.sse_queue.put(_STREAM_DONE)
        self.cancel_pending()

    @property
    def done_sentinel(self) -> object:
        return _STREAM_DONE


class SessionManager:
    """In-memory store of active RevitSessions (one per connected plugin instance)."""

    def __init__(self) -> None:
        self._sessions: dict[str, RevitSession] = {}

    def create(self, session_id: str | None = None) -> RevitSession:
        sid = session_id or str(uuid.uuid4())
        session = RevitSession(session_id=sid)
        self._sessions[sid] = session
        logger.debug("Session created: %s", sid)
        return session

    def get(self, session_id: str) -> RevitSession | None:
        return self._sessions.get(session_id)

    def get_or_create(self, session_id: str | None) -> RevitSession:
        if session_id and session_id in self._sessions:
            return self._sessions[session_id]
        return self.create(session_id)

    def remove(self, session_id: str) -> None:
        session = self._sessions.pop(session_id, None)
        if session:
            session.cancel_pending()
            logger.debug("Session removed: %s", session_id)


# Global singleton – imported by tools and routes
session_manager = SessionManager()
