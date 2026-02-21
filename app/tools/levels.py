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
