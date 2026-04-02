"""Revit levels and grids tools – delegates execution to the Revit plugin."""
from __future__ import annotations

from typing import Any

from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool

from app.tools.elements import _delegate


@tool
async def list_levels(config: RunnableConfig) -> list[dict[str, Any]]:
    """
    Return all levels defined in the active Revit document.

    Returns:
        List of {id, name, elevation_mm, is_building_story}.
    """
    return await _delegate(config, "list_levels", {})


@tool
async def list_grids(config: RunnableConfig) -> list[dict[str, Any]]:
    """
    Return all grid lines in the active Revit document.

    Returns:
        List of {id, name, is_curved}.
    """
    return await _delegate(config, "list_grids", {})


@tool
async def create_level(
    config: RunnableConfig,
    elevation_mm: float,
    name: str | None = None,
    create_floor_plan: bool = True,
) -> dict[str, Any]:
    """
    Create a new level at the specified elevation above the project base point.

    Args:
        elevation_mm: Elevation of the new level in project coordinates (mm).
        name: Optional name for the level (e.g. "Level 3", "Roof").
              If omitted, Revit auto-names the level.
        create_floor_plan: If True (default), automatically generate an associated
                           floor plan view for the new level.

    Returns:
        {success: bool, level_id: str, name: str, elevation_mm: float,
         floor_plan_view_id: str | None, message: str}.
    """
    return await _delegate(config, "create_level", {
        "elevation_mm": elevation_mm,
        "name": name,
        "create_floor_plan": create_floor_plan,
    })


@tool
async def create_grid(
    config: RunnableConfig,
    start_x_mm: float,
    start_y_mm: float,
    end_x_mm: float,
    end_y_mm: float,
    name: str | None = None,
    bubble_end: str = "end",
) -> dict[str, Any]:
    """
    Create a straight grid line between two XY points in the model.

    Args:
        start_x_mm: X of the start point (mm).
        start_y_mm: Y of the start point (mm).
        end_x_mm: X of the end point (mm).
        end_y_mm: Y of the end point (mm).
        name: Optional grid label (e.g. "A", "1", "A2"). Auto-named if omitted.
        bubble_end: Which end shows the grid bubble – "start", "end" (default), or "both".

    Returns:
        {success: bool, grid_id: str, name: str, message: str}.
    """
    return await _delegate(config, "create_grid", {
        "start_x_mm": start_x_mm,
        "start_y_mm": start_y_mm,
        "end_x_mm": end_x_mm,
        "end_y_mm": end_y_mm,
        "name": name,
        "bubble_end": bubble_end,
    })
