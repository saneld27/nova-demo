"""Revit rooms, spaces, and area tools – delegates execution to the Revit plugin."""
from __future__ import annotations

from typing import Any

from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool

from app.tools.elements import _delegate


@tool
async def get_room_detail(
    config: RunnableConfig,
    room_id: str | None = None,
    name: str | None = None,
    number: str | None = None,
) -> dict[str, Any]:
    """
    Return full detail for a specific room, looked up by ID, name, or number.

    Args:
        room_id: Revit element ID (preferred).
        name: Room name substring match (e.g. "Conference").
        number: Room number exact match (e.g. "101").

    Returns:
        {id, name, number, level, area_sqm, perimeter_mm, height_mm, occupancy,
         department, comments, phase, bounding_box}.
    """
    return await _delegate(config, "get_room_detail", {
        "room_id": room_id, "name": name, "number": number,
    })


@tool
async def get_room_boundaries(room_id: str, config: RunnableConfig) -> dict[str, Any]:
    """
    Return the boundary segments of a room, including the hosting elements
    (walls, floors, etc.) that form each segment.  Useful for understanding
    room geometry and adjacency.

    Args:
        room_id: Revit element ID of the room.

    Returns:
        {room_id, boundary_loops: [[{element_id, element_category, length_mm,
         start: {x,y}, end: {x,y}}]]}.
    """
    return await _delegate(config, "get_room_boundaries", {"room_id": room_id})


@tool
async def get_room_adjacency(room_id: str, config: RunnableConfig) -> list[dict[str, Any]]:
    """
    Return rooms that are directly adjacent to the given room (share a boundary
    segment).  Useful for egress analysis, acoustic zone checks, etc.

    Args:
        room_id: Revit element ID of the room.

    Returns:
        List of {room_id, name, number, level, shared_boundary_length_mm, separating_element_id}.
    """
    return await _delegate(config, "get_room_adjacency", {"room_id": room_id})


@tool
async def list_area_plans(config: RunnableConfig) -> list[dict[str, Any]]:
    """
    Return all area plans in the project.

    Returns:
        List of {view_id, name, area_scheme_name, level}.
    """
    return await _delegate(config, "list_area_plans", {})


@tool
async def get_areas_in_plan(area_plan_id: str, config: RunnableConfig) -> list[dict[str, Any]]:
    """
    Return all area elements placed in a specific area plan view.

    Args:
        area_plan_id: Revit element ID of the area plan view.

    Returns:
        List of {id, name, number, area_sqm, area_type, perimeter_mm, level}.
    """
    return await _delegate(config, "get_areas_in_plan", {"area_plan_id": area_plan_id})
