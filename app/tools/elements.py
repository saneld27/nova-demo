"""
Revit element querying tools.

Each tool delegates execution to the Revit plugin:
  1. Emits a ``tool_call`` event into the session SSE queue
  2. Awaits the Future that will be resolved when the plugin POSTs back
     the result to POST /api/v1/chat/{session_id}/tool_result
"""
from __future__ import annotations

import uuid
from typing import Any

from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool

from app.session import session_manager

TOOL_TIMEOUT = 60.0  # seconds to wait for plugin response


async def _delegate(config: RunnableConfig, tool_name: str, args: dict[str, Any]) -> Any:
    """Emit a tool_call to the plugin and await the result."""
    session_id: str = config["configurable"]["session_id"]
    session = session_manager.get(session_id)
    if session is None:
        raise RuntimeError(f"No active session for session_id={session_id!r}")

    call_id = str(uuid.uuid4())
    fut = session.register_call(call_id)
    await session.emit({"type": "tool_call", "call_id": call_id, "tool": tool_name, "args": args})

    import asyncio
    return await asyncio.wait_for(fut, timeout=TOOL_TIMEOUT)


@tool
async def get_elements_by_category(
    category: str,
    config: RunnableConfig,
    limit: int = 50,
) -> list[dict[str, Any]]:
    """
    Return a list of Revit elements that belong to *category* (e.g.
    "Walls", "Doors", "Windows", "Floors", "Columns").

    Args:
        category: Revit built-in category name (case-insensitive).
        limit: Maximum number of elements to return (default 50).

    Returns:
        List of element summaries: [{id, name, category, level, type_name}, ...]
    """
    return await _delegate(config, "get_elements_by_category", {"category": category, "limit": limit})


@tool
async def get_element_by_id(element_id: str, config: RunnableConfig) -> dict[str, Any]:
    """
    Retrieve detailed information about a single Revit element by its
    integer element ID.

    Args:
        element_id: Revit element ID as a string.

    Returns:
        Dict with keys: id, name, category, level, type_name, parameters.
    """
    return await _delegate(config, "get_element_by_id", {"element_id": element_id})
