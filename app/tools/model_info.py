"""Revit model health, warnings, and room tools – delegates execution to the Revit plugin."""
from __future__ import annotations

from typing import Any

from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool

from app.tools.elements import _delegate


@tool
async def get_model_info(config: RunnableConfig) -> dict[str, Any]:
    """
    Return high-level information about the active Revit document.

    Returns:
        {title, path, revit_version, element_count, last_saved}.
    """
    return await _delegate(config, "get_model_info", {})


@tool
async def list_warnings(config: RunnableConfig) -> list[dict[str, Any]]:
    """
    Return model integrity warnings from the active Revit document.

    Returns:
        List of {severity, description, element_ids}.
    """
    return await _delegate(config, "list_warnings", {})


@tool
async def get_rooms_summary(config: RunnableConfig) -> list[dict[str, Any]]:
    """
    Return a summary of all rooms/spaces in the model.

    Returns:
        List of {id, name, number, level, area_sqm, occupancy}.
    """
    return await _delegate(config, "get_rooms_summary", {})
