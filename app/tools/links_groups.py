"""Revit linked files, CAD links, groups, and design options tools."""
from __future__ import annotations

from typing import Any

from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool

from app.tools.elements import _delegate


@tool
async def list_rvt_links(config: RunnableConfig) -> list[dict[str, Any]]:
    """
    Return all Revit linked file (RVT) references in the model.

    Returns:
        List of {link_id, name, path, load_status, is_loaded, position_type,
                 element_count, disciplines: [str]}.
    """
    return await _delegate(config, "list_rvt_links", {})


@tool
async def list_cad_links(config: RunnableConfig) -> list[dict[str, Any]]:
    """
    Return all imported or linked CAD files (DWG, DXF, DGN, etc.).

    Returns:
        List of {link_id, name, path, import_type ("Imported"|"Linked"),
                 is_linked_to_view, level, category_count}.
    """
    return await _delegate(config, "list_cad_links", {})


@tool
async def list_groups(
    config: RunnableConfig,
    group_type: str | None = None,
) -> list[dict[str, Any]]:
    """
    Return all group types and their instance counts in the model.

    Args:
        group_type: Optional filter – "Model" or "Detail".

    Returns:
        List of {group_type_id, name, kind ("Model"|"Detail"),
                 instance_count, element_count_per_instance}.
    """
    return await _delegate(config, "list_groups", {"group_type": group_type})


@tool
async def get_group_instances(
    config: RunnableConfig,
    group_name: str,
) -> list[dict[str, Any]]:
    """
    Return all placed instances of a named group, with their locations and
    host levels.  Useful for inventory checks or batch-modifying grouped
    assemblies.

    Args:
        group_name: Exact group type name.

    Returns:
        List of {instance_id, group_name, level, location: {x, y, z},
                 rotation_degrees}.
    """
    return await _delegate(config, "get_group_instances", {"group_name": group_name})


@tool
async def list_design_options(config: RunnableConfig) -> list[dict[str, Any]]:
    """
    Return all design option sets and their options.  Useful for understanding
    alternate design strategies modelled in the project.

    Returns:
        List of {option_set_id, option_set_name, options: [{option_id, name,
                 is_primary}]}.
    """
    return await _delegate(config, "list_design_options", {})
