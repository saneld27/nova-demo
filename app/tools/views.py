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


@tool
async def hide_elements_in_view(
    config: RunnableConfig,
    element_ids: list[str],
    view_id: str | None = None,
    permanent: bool = False,
) -> dict[str, Any]:
    """
    Hide specific elements in a view.
    Temporary hide uses Revit's hide-in-view mechanism (can be reset by resetting temporary view properties).
    Permanent hide removes the element from visibility permanently in that view.

    Args:
        element_ids: List of element IDs to hide.
        view_id: Target view ID. Defaults to the active view.
        permanent: If True, permanently hide (Hide in View). If False (default), temporary hide.

    Returns:
        {success: bool, hidden_count: int, message: str}.
    """
    return await _delegate(config, "hide_elements_in_view", {
        "element_ids": element_ids,
        "view_id": view_id,
        "permanent": permanent,
    })


@tool
async def hide_category_in_view(
    config: RunnableConfig,
    category: str,
    view_id: str | None = None,
    permanent: bool = False,
) -> dict[str, Any]:
    """
    Hide all elements of a category in a view (e.g. hide all "Furniture" in a floor plan).

    Args:
        category: Category name to hide (e.g. "Furniture", "Doors", "Walls").
        view_id: Target view ID. Defaults to the active view.
        permanent: If True, permanently hide the category; if False, temporary.

    Returns:
        {success: bool, message: str}.
    """
    return await _delegate(config, "hide_category_in_view", {
        "category": category,
        "view_id": view_id,
        "permanent": permanent,
    })


@tool
async def isolate_elements_in_view(
    config: RunnableConfig,
    element_ids: list[str],
    view_id: str | None = None,
    isolate_mode: str = "temporary",
) -> dict[str, Any]:
    """
    Isolate specific elements in a view, hiding everything else temporarily or permanently.

    Args:
        element_ids: List of element IDs to isolate.
        view_id: Target view ID. Defaults to the active view.
        isolate_mode: "temporary" (default) – reversible temporary isolation;
                      "permanent" – permanent hide-in-view for all other elements.

    Returns:
        {success: bool, message: str}.
    """
    return await _delegate(config, "isolate_elements_in_view", {
        "element_ids": element_ids,
        "view_id": view_id,
        "isolate_mode": isolate_mode,
    })


@tool
async def isolate_category_in_view(
    config: RunnableConfig,
    category: str,
    view_id: str | None = None,
    isolate_mode: str = "temporary",
) -> dict[str, Any]:
    """
    Isolate all elements of a category in a view, hiding all other categories.

    Args:
        category: Category name to isolate.
        view_id: Target view ID. Defaults to the active view.
        isolate_mode: "temporary" (default) or "permanent".

    Returns:
        {success: bool, message: str}.
    """
    return await _delegate(config, "isolate_category_in_view", {
        "category": category,
        "view_id": view_id,
        "isolate_mode": isolate_mode,
    })


@tool
async def unhide_elements_in_view(
    config: RunnableConfig,
    element_ids: list[str] | None = None,
    category: str | None = None,
    reset_all: bool = False,
    view_id: str | None = None,
) -> dict[str, Any]:
    """
    Unhide previously hidden elements or categories in a view, or reset all
    temporary view property overrides (equivalent to clicking Reset Temporary
    Hide/Isolate in the Revit view control bar).

    Provide either element_ids, category, or set reset_all=True.

    Args:
        element_ids: Specific element IDs to unhide (optional).
        category: Category to unhide (optional).
        reset_all: If True, reset all temporary visibility overrides in the view.
        view_id: Target view ID. Defaults to the active view.

    Returns:
        {success: bool, message: str}.
    """
    return await _delegate(config, "unhide_elements_in_view", {
        "element_ids": element_ids,
        "category": category,
        "reset_all": reset_all,
        "view_id": view_id,
    })


@tool
async def set_view_display_settings(
    config: RunnableConfig,
    view_id: str | None = None,
    show_shadows: bool | None = None,
    reveal_hidden_elements: bool | None = None,
    show_crop_region: bool | None = None,
    show_annotation_crop: bool | None = None,
    underlay_orientation: str | None = None,
    far_clip_active: bool | None = None,
    far_clip_offset_mm: float | None = None,
) -> dict[str, Any]:
    """
    Toggle view display settings such as shadows, reveal hidden elements,
    crop region visibility, underlay orientation, and far clip plane.

    Pass only the properties you want to change; unspecified ones are left as-is.

    Args:
        view_id: Target view ID. Defaults to the active view.
        show_shadows: Enable or disable shadow rendering.
        reveal_hidden_elements: Toggle "Reveal Hidden Elements" mode (pink highlight).
        show_crop_region: Show or hide the view crop boundary.
        show_annotation_crop: Show or hide the annotation crop boundary.
        underlay_orientation: "Look Up" or "Look Down".
        far_clip_active: Enable or disable the far clip plane.
        far_clip_offset_mm: Distance of the far clip plane from the view origin (mm).

    Returns:
        {success: bool, applied_settings: dict, message: str}.
    """
    return await _delegate(config, "set_view_display_settings", {
        "view_id": view_id,
        "show_shadows": show_shadows,
        "reveal_hidden_elements": reveal_hidden_elements,
        "show_crop_region": show_crop_region,
        "show_annotation_crop": show_annotation_crop,
        "underlay_orientation": underlay_orientation,
        "far_clip_active": far_clip_active,
        "far_clip_offset_mm": far_clip_offset_mm,
    })


@tool
async def create_section_view(
    config: RunnableConfig,
    section_name: str,
    origin_x_mm: float,
    origin_y_mm: float,
    origin_z_mm: float,
    direction_x: float,
    direction_y: float,
    width_mm: float,
    height_mm: float,
    depth_mm: float,
    view_type: str = "Section",
) -> dict[str, Any]:
    """
    Create a new section or callout view by defining a cut plane.

    Args:
        section_name: Name to assign the new view.
        origin_x_mm: X of the section origin in project coordinates (mm).
        origin_y_mm: Y of the section origin (mm).
        origin_z_mm: Z of the section origin (the vertical mid-point) (mm).
        direction_x: X component of the section's look-direction (normalised).
        direction_y: Y component of the section's look-direction (normalised).
        width_mm: Width of the section crop box (mm).
        height_mm: Height of the section crop box (mm).
        depth_mm: Depth (far clip distance) of the section (mm).
        view_type: "Section" (default) or "Elevation".

    Returns:
        {success: bool, view_id: str, view_name: str, message: str}.
    """
    return await _delegate(config, "create_section_view", {
        "section_name": section_name,
        "origin_x_mm": origin_x_mm,
        "origin_y_mm": origin_y_mm,
        "origin_z_mm": origin_z_mm,
        "direction_x": direction_x,
        "direction_y": direction_y,
        "width_mm": width_mm,
        "height_mm": height_mm,
        "depth_mm": depth_mm,
        "view_type": view_type,
    })


@tool
async def tile_open_views(config: RunnableConfig) -> dict[str, Any]:
    """
    Tile all currently open view windows in the Revit UI side-by-side
    (equivalent to View → Windows → Tile Views).

    Returns:
        {success: bool, message: str}.
    """
    return await _delegate(config, "tile_open_views", {})


@tool
async def tab_open_views(config: RunnableConfig) -> dict[str, Any]:
    """
    Arrange all currently open view windows as tabs in the Revit UI
    (equivalent to View → Windows → Tab Views).

    Returns:
        {success: bool, message: str}.
    """
    return await _delegate(config, "tab_open_views", {})
