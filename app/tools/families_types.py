"""Revit family and type management tools – delegates execution to the Revit plugin."""
from __future__ import annotations

from typing import Any

from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool

from app.tools.elements import _delegate


@tool
async def list_element_types(
    config: RunnableConfig,
    category: str,
    family_name: str | None = None,
) -> list[dict[str, Any]]:
    """
    Return all element types (family symbols) available for a given category.
    Useful for discovering what wall types, door types, beam types etc. are
    loaded in the project before placing or changing elements.

    Args:
        category: Revit category name (e.g. "Walls", "Doors", "Structural Framing").
        family_name: Optional family name filter to narrow results.

    Returns:
        List of {type_id, family_name, type_name, category}.
    """
    return await _delegate(config, "list_element_types", {"category": category, "family_name": family_name})


@tool
async def get_type_properties(type_id: str, config: RunnableConfig) -> dict[str, Any]:
    """
    Return all type-level parameters for a family type (symbol).
    Complements get_element_parameters which returns instance parameters.

    Args:
        type_id: Revit element ID of the type/symbol.

    Returns:
        {family_name, type_name, category, parameters: {name: {value, units, is_read_only}}}.
    """
    return await _delegate(config, "get_type_properties", {"type_id": type_id})


@tool
async def set_type_parameter(
    config: RunnableConfig,
    type_id: str,
    parameter_name: str,
    value: str,
) -> dict[str, Any]:
    """
    Set a writable type parameter on a family symbol.  Note: this affects ALL
    existing and future instances of that type.  Use with caution.

    Args:
        type_id: Revit element ID of the family type.
        parameter_name: Type parameter name (case-sensitive).
        value: New value as a string.

    Returns:
        {success: bool, message: str, affected_instance_count: int}.
    """
    return await _delegate(config, "set_type_parameter", {
        "type_id": type_id, "parameter_name": parameter_name, "value": value,
    })


@tool
async def list_loaded_families(
    config: RunnableConfig,
    category: str | None = None,
) -> list[dict[str, Any]]:
    """
    Return all families loaded in the project, optionally filtered by category.
    Each family can have multiple types.

    Args:
        category: Optional category filter (e.g. "Furniture", "Plumbing Fixtures").

    Returns:
        List of {family_name, category, type_count, is_system_family, is_in_place}.
    """
    return await _delegate(config, "list_loaded_families", {"category": category})


@tool
async def get_family_info(config: RunnableConfig, family_name: str) -> dict[str, Any]:
    """
    Return detailed information about a loaded family including all its types
    and the parameters exposed at type level.

    Args:
        family_name: Exact family name (case-sensitive).

    Returns:
        {family_name, category, types: [{type_id, type_name, key_params}], is_system_family}.
    """
    return await _delegate(config, "get_family_info", {"family_name": family_name})


@tool
async def change_element_type(
    config: RunnableConfig,
    element_id: str,
    new_type_id: str,
) -> dict[str, Any]:
    """
    Change an existing element to a different type within the same family or
    a compatible family (e.g. swap a wall type, swap a door type).

    Args:
        element_id: Revit element ID of the instance to change.
        new_type_id: Revit element ID of the target type.

    Returns:
        {success: bool, message: str, old_type_name: str, new_type_name: str}.
    """
    return await _delegate(config, "change_element_type", {
        "element_id": element_id, "new_type_id": new_type_id,
    })
