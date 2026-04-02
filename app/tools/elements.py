"""
Revit element querying tools.

Each tool delegates execution to the Revit plugin:
  1. Emits a ``tool_call`` event into the session SSE queue
  2. Awaits the Future that will be resolved when the plugin POSTs back
     the result to POST /api/v1/chat/{session_id}/tool_result
"""
from __future__ import annotations

import logging
import uuid
from typing import Any

from langchain_core.runnables import RunnableConfig
from langchain_core.tools import ToolException, tool

from app.session import session_manager

logger = logging.getLogger(__name__)

TOOL_TIMEOUT = 60.0  # seconds to wait for plugin response


async def _delegate(config: RunnableConfig, tool_name: str, args: dict[str, Any]) -> Any:
    """Emit a tool_call to the plugin and await the result."""
    import asyncio
    import time

    session_id: str = config["configurable"]["session_id"]
    session = session_manager.get(session_id)
    if session is None:
        raise ToolException(f"No active session for session_id={session_id!r}")

    call_id = str(uuid.uuid4())
    fut = session.register_call(call_id)
    logger.info("Dispatching tool call session=%s tool=%s call_id=%s args=%r", session_id, tool_name, call_id, args)
    await session.emit({
        "type": "tool_call",
        "data": {"call_id": call_id, "tool": tool_name, "args": args},
    })

    t0 = time.monotonic()
    try:
        result = await asyncio.wait_for(fut, timeout=TOOL_TIMEOUT)
        elapsed = time.monotonic() - t0
        logger.info(
            "Tool result received session=%s tool=%s call_id=%s elapsed=%.2fs result_preview=%r",
            session_id, tool_name, call_id, elapsed, str(result)[:300],
        )
        return result
    except asyncio.TimeoutError:
        elapsed = time.monotonic() - t0
        logger.error(
            "Tool timed out session=%s tool=%s call_id=%s elapsed=%.2fs",
            session_id, tool_name, call_id, elapsed,
        )
        raise ToolException(
            f"Tool '{tool_name}' timed out after {TOOL_TIMEOUT:.0f}s – "
            "the Revit plugin did not respond in time. "
            "Make sure the Revit plugin is running and connected."
        )


@tool
async def get_selected_elements(config: RunnableConfig) -> list[dict[str, Any]]:
    """
    Return the elements currently selected in the Revit UI.

    Use this ONLY when the user refers to 'this', 'these', 'the selected elements',
    'it', 'them', or similar pronouns AND the conversation context does not already
    contain a non-empty ``selected_elements`` list.  In multi-turn conversations the
    selection may have changed since the original request was sent, so this tool
    fetches the live selection directly from Revit.

    Returns:
        List of {id, name, category, type_name, level} for every currently selected
        element.  Returns an empty list if nothing is selected.
    """
    return await _delegate(config, "get_selected_elements", {})


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


@tool
async def get_elements_in_view(
    config: RunnableConfig,
    view_id: str | None = None,
    category: str | None = None,
    limit: int = 100,
) -> list[dict[str, Any]]:
    """
    Return elements that are visible in a specific view (or the active view if
    no view_id is given).  Optionally filter by category.

    Args:
        view_id: Revit view element ID. Defaults to the active view.
        category: Optional category name filter (e.g. "Walls", "Doors").
        limit: Maximum number of elements to return.

    Returns:
        List of {id, name, category, type_name, level}.
    """
    return await _delegate(config, "get_elements_in_view", {"view_id": view_id, "category": category, "limit": limit})


@tool
async def get_elements_by_level(
    config: RunnableConfig,
    level_name: str,
    category: str | None = None,
    limit: int = 200,
) -> list[dict[str, Any]]:
    """
    Return all elements associated with a given level, optionally filtered by
    category.  Useful for floor-by-floor audits or clash reviews.

    Args:
        level_name: Exact level name (e.g. "Level 2", "Ground Floor").
        category: Optional category filter. Pass None for all categories.
        limit: Maximum number of elements to return.

    Returns:
        List of {id, name, category, type_name}.
    """
    return await _delegate(config, "get_elements_by_level", {"level_name": level_name, "category": category, "limit": limit})


@tool
async def get_elements_in_room(
    config: RunnableConfig,
    room_id: str,
    category: str | None = None,
) -> list[dict[str, Any]]:
    """
    Return elements spatially located inside a specific room.  Optionally filter
    by category to e.g. find all furniture or lighting fixtures in a room.

    Args:
        room_id: Revit element ID of the Room.
        category: Optional category filter.

    Returns:
        List of {id, name, category, type_name}.
    """
    return await _delegate(config, "get_elements_in_room", {"room_id": room_id, "category": category})


@tool
async def search_elements(
    config: RunnableConfig,
    query: str,
    categories: list[str] | None = None,
    limit: int = 50,
) -> list[dict[str, Any]]:
    """
    Full-text search across element names, type names, and parameter values.
    Use this when the user describes an element by name or keyword rather than
    by category or ID.

    Args:
        query: Search string (case-insensitive substring match).
        categories: Optional list of category names to restrict the search.
        limit: Maximum number of matches to return.

    Returns:
        List of {id, name, category, type_name, level, matched_field}.
    """
    return await _delegate(config, "search_elements", {"query": query, "categories": categories, "limit": limit})


@tool
async def find_elements_by_parameter_value(
    config: RunnableConfig,
    parameter_name: str,
    value: str,
    category: str | None = None,
    limit: int = 100,
) -> list[dict[str, Any]]:
    """
    Find all elements where a specific parameter equals (or contains) a given value.
    Useful for queries like "find all walls with fire rating EI60" or
    "find all rooms with occupancy = Office".

    Args:
        parameter_name: Parameter name to match (case-insensitive).
        value: Value to search for (substring match on string params; exact for numbers).
        category: Optional category to limit the search.
        limit: Maximum number of results.

    Returns:
        List of {id, name, category, type_name, level, parameter_name, parameter_value}.
    """
    return await _delegate(config, "find_elements_by_parameter_value", {
        "parameter_name": parameter_name, "value": value, "category": category, "limit": limit,
    })


@tool
async def get_element_location(element_id: str, config: RunnableConfig) -> dict[str, Any]:
    """
    Return the geometric location of an element – a point (XYZ) for point-based
    families, or start/end points for linear elements (walls, beams, pipes).

    Args:
        element_id: Revit element ID.

    Returns:
        {location_type: "point"|"curve", x, y, z} or
        {location_type: "curve", start: {x,y,z}, end: {x,y,z}, length_mm}.
    """
    return await _delegate(config, "get_element_location", {"element_id": element_id})


@tool
async def get_element_bounding_box(element_id: str, config: RunnableConfig) -> dict[str, Any]:
    """
    Return the axis-aligned 3-D bounding box of an element in project coordinates.

    Args:
        element_id: Revit element ID.

    Returns:
        {min: {x,y,z}, max: {x,y,z}, width_mm, depth_mm, height_mm} (all in mm).
    """
    return await _delegate(config, "get_element_bounding_box", {"element_id": element_id})


@tool
async def get_element_host(element_id: str, config: RunnableConfig) -> dict[str, Any] | None:
    """
    Return the host element of a hosted element (e.g. the wall that hosts a door
    or window, the floor that hosts a floor-based family).

    Args:
        element_id: Revit element ID of the hosted element.

    Returns:
        {id, name, category, type_name} of the host, or null if not hosted.
    """
    return await _delegate(config, "get_element_host", {"element_id": element_id})


@tool
async def get_hosted_elements(
    config: RunnableConfig,
    host_element_id: str,
    category: str | None = None,
) -> list[dict[str, Any]]:
    """
    Return all elements hosted by the given element (e.g. all doors and windows
    in a wall, all fixtures hosted on a ceiling).

    Args:
        host_element_id: Revit element ID of the host.
        category: Optional category filter for the hosted elements.

    Returns:
        List of {id, name, category, type_name}.
    """
    return await _delegate(config, "get_hosted_elements", {"host_element_id": host_element_id, "category": category})


@tool
async def get_elements_in_bounding_box(
    config: RunnableConfig,
    min_x: float,
    min_y: float,
    min_z: float,
    max_x: float,
    max_y: float,
    max_z: float,
    category: str | None = None,
) -> list[dict[str, Any]]:
    """
    Return elements whose bounding box intersects a given 3-D region (in mm,
    project coordinates). Useful for clash detection or zone-based queries.

    Args:
        min_x/min_y/min_z: Minimum corner of the query box in mm.
        max_x/max_y/max_z: Maximum corner of the query box in mm.
        category: Optional category filter.

    Returns:
        List of {id, name, category, type_name, level}.
    """
    return await _delegate(config, "get_elements_in_bounding_box", {
        "min_x": min_x, "min_y": min_y, "min_z": min_z,
        "max_x": max_x, "max_y": max_y, "max_z": max_z,
        "category": category,
    })
