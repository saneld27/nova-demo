"""Revit site and project location tools – delegates execution to the Revit plugin."""
from __future__ import annotations

from typing import Any

from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool

from app.tools.elements import _delegate


@tool
async def get_toposurface_info(config: RunnableConfig) -> list[dict[str, Any]]:
    """
    Return topographic surface elements in the model, including their elevation
    range, area, and sub-region count.

    Returns:
        List of {id, name, min_elevation_mm, max_elevation_mm, area_sqm,
                 sub_region_count, point_count}.
    """
    return await _delegate(config, "get_toposurface_info", {})


@tool
async def list_site_components(
    config: RunnableConfig,
    limit: int = 200,
) -> list[dict[str, Any]]:
    """
    Return site component elements (planting, site furniture, parking, etc.)
    placed in the model.

    Args:
        limit: Maximum number to return.

    Returns:
        List of {id, family_name, type_name, category, location: {x, y, z}}.
    """
    return await _delegate(config, "list_site_components", {"limit": limit})


@tool
async def get_project_location(config: RunnableConfig) -> dict[str, Any]:
    """
    Return the project's geographic location, coordinate system settings,
    and true north offset.  Useful for solar analysis, orientation checks,
    and georeferencing workflows.

    Returns:
        {place_name, latitude_deg, longitude_deg, elevation_m,
         time_zone, true_north_offset_deg, project_north_offset_deg,
         survey_point: {x,y,z}, project_base_point: {x,y,z}}.
    """
    return await _delegate(config, "get_project_location", {})
