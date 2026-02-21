"""Revit element parameter tools – delegates execution to the Revit plugin."""
from __future__ import annotations

from typing import Any

from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool

from app.tools.elements import _delegate


@tool
async def get_element_parameters(element_id: str, config: RunnableConfig) -> dict[str, Any]:
    """
    Return all user-visible parameters and their values for the given element.

    Args:
        element_id: Revit element ID as a string.

    Returns:
        Dict mapping parameter name -> {value, units, is_read_only}.
    """
    return await _delegate(config, "get_element_parameters", {"element_id": element_id})


@tool
async def set_element_parameter(
    element_id: str,
    parameter_name: str,
    value: str,
    config: RunnableConfig,
) -> dict[str, Any]:
    """
    Set a writable parameter on a Revit element.

    Args:
        element_id: Revit element ID as a string.
        parameter_name: Exact parameter name (case-sensitive).
        value: New value as a string; Revit will parse it to the correct type.

    Returns:
        {success: bool, message: str}
    """
    return await _delegate(
        config,
        "set_element_parameter",
        {"element_id": element_id, "parameter_name": parameter_name, "value": value},
    )
