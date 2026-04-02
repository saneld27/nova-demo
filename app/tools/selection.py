"""
Advanced element selection and filtering tools for Revit.

These tools enable the agent to find and select elements using criteria that
are not available directly within the standard Revit UI, such as filtering by
multiple parameters, spatial relationships, or custom logic.  All selection
operations set the Revit UI selection so the user can see and act on results.
"""
from __future__ import annotations

from typing import Any

from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool

from app.tools.elements import _delegate


@tool
async def select_elements_by_category(
    config: RunnableConfig,
    category: str,
    scope: str = "model",
    view_id: str | None = None,
    set_ui_selection: bool = True,
) -> dict[str, Any]:
    """
    Select all elements of a given category in the model or in a specific view,
    and optionally set Revit's UI selection to show a highlight.

    Args:
        category: Category name (e.g. "Walls", "Doors", "Structural Columns").
        scope: "model" (default) – entire document; "view" – limit to a specific view.
        view_id: Required when scope is "view". Defaults to the active view.
        set_ui_selection: If True (default), update the Revit UI selection to highlight
                          the matching elements.

    Returns:
        {element_ids: [str], count: int, category: str, message: str}.
    """
    return await _delegate(config, "select_elements_by_category", {
        "category": category,
        "scope": scope,
        "view_id": view_id,
        "set_ui_selection": set_ui_selection,
    })


@tool
async def select_elements_by_parameter_filter(
    config: RunnableConfig,
    parameter_name: str,
    operator: str,
    value: str | float | int | bool,
    category: str | None = None,
    scope: str = "model",
    view_id: str | None = None,
    set_ui_selection: bool = True,
) -> dict[str, Any]:
    """
    Select elements where a specific parameter satisfies a condition.
    Examples: fire-rated doors (Fire Rating > 60), rooms larger than 20 m²,
    walls of a specific type, etc.

    Args:
        parameter_name: Name of the parameter to filter by (e.g. "Fire Rating", "Area").
        operator: Comparison operator –
            "equals", "not_equals",
            "greater_than", "greater_or_equal",
            "less_than", "less_or_equal",
            "contains", "not_contains",
            "begins_with", "ends_with".
        value: The value to compare against (e.g. 60, "Concrete", True).
        category: Optional category name to restrict the search (e.g. "Doors").
        scope: "model" (default) or "view".
        view_id: Required when scope is "view".
        set_ui_selection: Update Revit UI selection (default True).

    Returns:
        {element_ids: [str], count: int, message: str}.
    """
    return await _delegate(config, "select_elements_by_parameter_filter", {
        "parameter_name": parameter_name,
        "operator": operator,
        "value": value,
        "category": category,
        "scope": scope,
        "view_id": view_id,
        "set_ui_selection": set_ui_selection,
    })


@tool
async def select_elements_by_type(
    config: RunnableConfig,
    type_name: str,
    family_name: str | None = None,
    category: str | None = None,
    set_ui_selection: bool = True,
) -> dict[str, Any]:
    """
    Select all instances of a specific element type (and optionally family) in the model.
    Useful for "select all instances of this door type" or "select all Generic 200mm walls".

    Args:
        type_name: Exact type name to match (e.g. "Generic - 200mm", '36" x 84"').
        family_name: Optional family name to narrow the match (e.g. "Single-Flush").
        category: Optional category to restrict the search (e.g. "Doors", "Walls").
        set_ui_selection: Update Revit UI selection (default True).

    Returns:
        {element_ids: [str], count: int, type_name: str, message: str}.
    """
    return await _delegate(config, "select_elements_by_type", {
        "type_name": type_name,
        "family_name": family_name,
        "category": category,
        "set_ui_selection": set_ui_selection,
    })


@tool
async def select_exterior_walls(
    config: RunnableConfig,
    level_name: str | None = None,
    set_ui_selection: bool = True,
) -> dict[str, Any]:
    """
    Identify and select all exterior walls in the model (or on a specific level).
    A wall is classified as exterior if its "Function" parameter is "Exterior"
    or if it has no interior room on one side (spatial boundary analysis).

    Args:
        level_name: Optional level filter (e.g. "Level 1").
        set_ui_selection: Update Revit UI selection (default True).

    Returns:
        {element_ids: [str], count: int, message: str}.
    """
    return await _delegate(config, "select_exterior_walls", {
        "level_name": level_name,
        "set_ui_selection": set_ui_selection,
    })


@tool
async def select_elements_on_level(
    config: RunnableConfig,
    level_name: str,
    category: str | None = None,
    set_ui_selection: bool = True,
) -> dict[str, Any]:
    """
    Select all elements associated with a given level, optionally filtered
    to a specific category.

    Args:
        level_name: Name of the level (e.g. "Level 2").
        category: Optional category filter (e.g. "Walls", "Floors", "Furniture").
        set_ui_selection: Update Revit UI selection (default True).

    Returns:
        {element_ids: [str], count: int, level_name: str, message: str}.
    """
    return await _delegate(config, "select_elements_on_level", {
        "level_name": level_name,
        "category": category,
        "set_ui_selection": set_ui_selection,
    })


@tool
async def select_elements_in_room(
    config: RunnableConfig,
    room_id: str | None = None,
    room_name: str | None = None,
    room_number: str | None = None,
    category: str | None = None,
    set_ui_selection: bool = True,
) -> dict[str, Any]:
    """
    Select all elements spatially located inside a room, optionally filtered
    by category.  Room can be identified by ID, name, or room number.

    Args:
        room_id: Element ID of the room (preferred).
        room_name: Room name to look up if ID is unknown.
        room_number: Room number to look up if ID is unknown.
        category: Optional category filter (e.g. "Furniture", "Lighting Fixtures").
        set_ui_selection: Update Revit UI selection (default True).

    Returns:
        {element_ids: [str], count: int, room_name: str, message: str}.
    """
    return await _delegate(config, "select_elements_in_room_advanced", {
        "room_id": room_id,
        "room_name": room_name,
        "room_number": room_number,
        "category": category,
        "set_ui_selection": set_ui_selection,
    })


@tool
async def filter_selection_by_category(
    config: RunnableConfig,
    category: str,
    element_ids: list[str],
    set_ui_selection: bool = True,
) -> dict[str, Any]:
    """
    From an existing list of element IDs (e.g. from the current selection),
    return only those belonging to a specific category.
    Useful for narrowing down a mixed selection.

    Args:
        category: Category to keep (e.g. "Walls").
        element_ids: List of element IDs to filter.
        set_ui_selection: If True, update the Revit UI to show filtered selection.

    Returns:
        {element_ids: [str], count: int, message: str}.
    """
    return await _delegate(config, "filter_selection_by_category", {
        "category": category,
        "element_ids": element_ids,
        "set_ui_selection": set_ui_selection,
    })


@tool
async def invert_selection(
    config: RunnableConfig,
    scope: str = "view",
    view_id: str | None = None,
) -> dict[str, Any]:
    """
    Invert the current Revit UI selection so that previously selected elements
    are deselected and all other visible elements become selected.

    Args:
        scope: "view" (default) – invert relative to elements visible in the view;
               "model" – invert relative to all elements in the document.
        view_id: Reference view for "view" scope. Defaults to the active view.

    Returns:
        {element_ids: [str], count: int, message: str}.
    """
    return await _delegate(config, "invert_selection", {
        "scope": scope,
        "view_id": view_id,
    })


@tool
async def select_all_of_same_type(
    config: RunnableConfig,
    element_id: str,
    scope: str = "model",
    set_ui_selection: bool = True,
) -> dict[str, Any]:
    """
    Select all instances of the same type as the given element (equivalent to
    Revit's "Select All Instances → In Entire Project / Visible in View").

    Args:
        element_id: Source element whose type is used as the selection criterion.
        scope: "model" (default) – entire project; "view" – visible in active view.
        set_ui_selection: Update Revit UI selection (default True).

    Returns:
        {element_ids: [str], count: int, type_name: str, message: str}.
    """
    return await _delegate(config, "select_all_of_same_type", {
        "element_id": element_id,
        "scope": scope,
        "set_ui_selection": set_ui_selection,
    })


@tool
async def select_connected_elements(
    config: RunnableConfig,
    element_id: str,
    connection_type: str = "hosted",
    set_ui_selection: bool = True,
) -> dict[str, Any]:
    """
    Select elements that are connected or related to a given element.
    Useful for "select all doors on this wall" or "select all elements in this MEP system".

    Args:
        element_id: The source element.
        connection_type: How to define "connected" –
            "hosted"   – elements hosted by this element (doors/windows on a wall);
            "host"     – the host of this element;
            "mep_system" – elements in the same MEP system;
            "structural_connected" – structurally connected framing members or columns.
        set_ui_selection: Update Revit UI selection (default True).

    Returns:
        {element_ids: [str], count: int, message: str}.
    """
    return await _delegate(config, "select_connected_elements", {
        "element_id": element_id,
        "connection_type": connection_type,
        "set_ui_selection": set_ui_selection,
    })
