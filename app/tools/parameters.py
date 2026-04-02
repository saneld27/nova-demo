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


@tool
async def bulk_set_parameter(
    config: RunnableConfig,
    element_ids: list[str],
    parameter_name: str,
    value: str,
) -> dict[str, Any]:
    """
    Set the same parameter to the same value on multiple elements at once.
    Much more efficient than calling set_element_parameter repeatedly.
    Use this for batch workflows, e.g. marking all selected walls as a specific
    fire rating or assigning a phase to many elements.

    Args:
        element_ids: List of Revit element IDs to update.
        parameter_name: Parameter name (case-sensitive).
        value: New value string.

    Returns:
        {updated_count: int, failed: [{element_id, reason}]}.
    """
    return await _delegate(config, "bulk_set_parameter", {
        "element_ids": element_ids, "parameter_name": parameter_name, "value": value,
    })


@tool
async def list_project_parameters(config: RunnableConfig) -> list[dict[str, Any]]:
    """
    Return all project parameters defined in the active Revit document.
    Useful for discovering what custom parameters are available before
    querying or setting them.

    Returns:
        List of {name, data_type, group, is_shared, categories}.
    """
    return await _delegate(config, "list_project_parameters", {})


@tool
async def list_shared_parameters(config: RunnableConfig) -> list[dict[str, Any]]:
    """
    Return all shared parameters currently loaded in the project, including
    their GUID, group, and data type.

    Returns:
        List of {name, guid, group, data_type, description}.
    """
    return await _delegate(config, "list_shared_parameters", {})


# DISABLED – too complex for plugin side
@tool
async def add_project_parameter(
    config: RunnableConfig,
    parameter_name: str,
    data_type: str,
    group_name: str,
    categories: list[str],
    is_instance: bool = True,
    is_shared: bool = False,
    description: str = "",
) -> dict[str, Any]:
    """
    Add a new project parameter to the active Revit document.
    Project parameters exist only in this document (not shared across projects).
    For a cross-project shared parameter, use add_shared_parameter instead.

    Args:
        parameter_name: Name of the new parameter.
        data_type: Data type string – "Text", "Integer", "Number", "Length", "Area",
                   "Volume", "YesNo", "URL", "Material", "FamilyType".
        group_name: Parameter group in the Properties palette – e.g. "General",
                    "Identity Data", "Dimensions", "Text".
        categories: List of category names to bind the parameter to
                    (e.g. ["Walls", "Floors"]). Use ["All"] to bind to all categories.
        is_instance: True (default) for an instance parameter; False for a type parameter.
        is_shared: If True the parameter is created as a shared parameter
                   (requires a shared parameter file to be set up in Revit).
        description: Optional tooltip description for the parameter.

    Returns:
        {success: bool, parameter_name: str, is_shared: bool, bound_categories: [str], message: str}.
    """
    return await _delegate(config, "add_project_parameter", {
        "parameter_name": parameter_name,
        "data_type": data_type,
        "group_name": group_name,
        "categories": categories,
        "is_instance": is_instance,
        "is_shared": is_shared,
        "description": description,
    })


@tool
async def add_global_parameter(
    config: RunnableConfig,
    parameter_name: str,
    data_type: str,
    value: str | float | int | bool | None = None,
    report_parameter: bool = False,
) -> dict[str, Any]:
    """
    Add (or update) a global parameter in the active Revit document.
    Global parameters can drive dimensions and be referenced from multiple places.

    Args:
        parameter_name: Name of the global parameter.
        data_type: Data type – "Length", "Number", "Integer", "Text", "YesNo".
        value: Initial value. Omit to create the parameter without a value.
        report_parameter: If True, this global parameter reports a measured value
                          from a dimension (it cannot then be freely set).

    Returns:
        {success: bool, global_parameter_id: str, parameter_name: str, message: str}.
    """
    return await _delegate(config, "add_global_parameter", {
        "parameter_name": parameter_name,
        "data_type": data_type,
        "value": value,
        "report_parameter": report_parameter,
    })
