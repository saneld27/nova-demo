"""Revit views and sheets tools – delegates execution to the Revit plugin."""
from __future__ import annotations

from typing import Any

from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool

from app.tools.elements import _delegate


@tool
async def list_views(config: RunnableConfig, view_type: str | None = None) -> list[dict[str, Any]]:
    """
    List views (and optionally filter by type) in the active Revit document.

    Args:
        view_type: Optional filter – "FloorPlan", "Section", "Elevation",
                   "3D", "Sheet", etc.  Pass None to return all views.

    Returns:
        List of {id, name, view_type, level, scale}.
    """
    return await _delegate(config, "list_views", {"view_type": view_type})


@tool
async def get_active_view(config: RunnableConfig) -> dict[str, Any]:
    """
    Return information about the currently active view in the Revit session.

    Returns:
        {id, name, view_type, level, scale}
    """
    return await _delegate(config, "get_active_view", {})
