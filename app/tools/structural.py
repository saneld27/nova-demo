"""Revit structural discipline tools – delegates execution to the Revit plugin."""
from __future__ import annotations

from typing import Any

from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool

from app.tools.elements import _delegate


@tool
async def list_structural_columns(
    config: RunnableConfig,
    level_name: str | None = None,
    limit: int = 200,
) -> list[dict[str, Any]]:
    """
    Return structural columns in the model.  Structural columns are distinct from
    architectural columns and carry load data in the analytical model.

    Args:
        level_name: Optional level filter.
        limit: Maximum number to return.

    Returns:
        List of {id, family_name, type_name, level, base_offset_mm, top_level,
                 top_offset_mm, is_slanted, material, analytical_model_enabled}.
    """
    return await _delegate(config, "list_structural_columns", {"level_name": level_name, "limit": limit})


@tool
async def list_structural_framing(
    config: RunnableConfig,
    framing_type: str | None = None,
    level_name: str | None = None,
    limit: int = 200,
) -> list[dict[str, Any]]:
    """
    Return structural framing members: beams, braces, trusses, and girders.

    Args:
        framing_type: Optional filter – "Beam", "Brace", "Truss", "Girder".
        level_name: Optional level filter.
        limit: Maximum number to return.

    Returns:
        List of {id, family_name, type_name, framing_type, level,
                 start: {x,y,z}, end: {x,y,z}, length_mm, cut_length_mm,
                 start_level_offset_mm, end_level_offset_mm, structural_usage}.
    """
    return await _delegate(config, "list_structural_framing", {
        "framing_type": framing_type, "level_name": level_name, "limit": limit,
    })


@tool
async def list_structural_foundations(
    config: RunnableConfig,
    foundation_type: str | None = None,
    limit: int = 200,
) -> list[dict[str, Any]]:
    """
    Return structural foundation elements (isolated footings, wall footings,
    foundation slabs).

    Args:
        foundation_type: Optional filter – "Isolated", "Wall", "Slab".
        limit: Maximum number to return.

    Returns:
        List of {id, family_name, type_name, foundation_type, level,
                 bearing_level, thickness_mm, area_sqm}.
    """
    return await _delegate(config, "list_structural_foundations", {
        "foundation_type": foundation_type, "limit": limit,
    })


@tool
async def get_analytical_model(element_id: str, config: RunnableConfig) -> dict[str, Any]:
    """
    Return the analytical model properties for a structural element (column,
    beam, brace, wall, floor).  Includes analytical member type, end join
    conditions, and material assignment for structural analysis.

    Args:
        element_id: Revit element ID of the structural element.

    Returns:
        {analytical_member_type, start_release, end_release, material,
         cross_section, analytical_nodes: [{x,y,z}]}.
    """
    return await _delegate(config, "get_analytical_model", {"element_id": element_id})


@tool
async def list_rebar(
    config: RunnableConfig,
    host_element_id: str | None = None,
    limit: int = 500,
) -> list[dict[str, Any]]:
    """
    Return rebar elements in the model, optionally filtered to those hosted
    within a specific concrete element.

    Args:
        host_element_id: Optional host element ID (concrete column, beam, wall).
        limit: Maximum number of rebar elements to return.

    Returns:
        List of {id, rebar_shape, bar_type_name, diameter_mm, length_mm,
                 host_id, host_category, quantity}.
    """
    return await _delegate(config, "list_rebar", {"host_element_id": host_element_id, "limit": limit})


@tool
async def add_wall_foundation(
    config: RunnableConfig,
    wall_ids: list[str],
    foundation_type_name: str,
) -> dict[str, Any]:
    """
    Add a structural wall foundation (continuous footing) to one or more walls.
    The foundation is placed automatically beneath each wall at its base.
    Use list_element_types("Structural Foundations") to find valid type names.

    Args:
        wall_ids: List of wall element IDs to apply foundations to.
        foundation_type_name: Footing type name (e.g. "600 x 300mm" or the project-specific name).

    Returns:
        {success: bool, created_foundation_ids: [str], message: str}.
    """
    return await _delegate(config, "add_wall_foundation", {
        "wall_ids": wall_ids,
        "foundation_type_name": foundation_type_name,
    })


@tool
async def add_isolated_foundation(
    config: RunnableConfig,
    column_ids: list[str],
    foundation_family_name: str,
    foundation_type_name: str,
    depth_below_column_mm: float = 0.0,
) -> dict[str, Any]:
    """
    Place isolated (pad/spread) footing foundations beneath structural columns.
    Each foundation is centred on the column base and snapped to the structural
    foundation level automatically.
    Use list_element_types("Structural Foundations") to find valid type names.

    Args:
        column_ids: List of structural column element IDs to receive footings.
        foundation_family_name: Family name of the isolated footing
                                (e.g. "Isolated Foundation - Rectangular").
        foundation_type_name: Type name within the family (e.g. "1200 x 1200 x 500mm").
        depth_below_column_mm: Extra depth to lower the foundation below the column
                               base offset (mm, default 0).

    Returns:
        {success: bool, created_foundation_ids: [str], message: str}.
    """
    return await _delegate(config, "add_isolated_foundation", {
        "column_ids": column_ids,
        "foundation_family_name": foundation_family_name,
        "foundation_type_name": foundation_type_name,
        "depth_below_column_mm": depth_below_column_mm,
    })
