"""Revit sheet and view management tools – delegates execution to the Revit plugin."""
from __future__ import annotations

from typing import Any

from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool

from app.tools.elements import _delegate


@tool
async def list_sheets(
    config: RunnableConfig,
    discipline: str | None = None,
    search: str | None = None,
) -> list[dict[str, Any]]:
    """
    Return all sheets in the project, optionally filtered by discipline or a
    search string matching the sheet number or name.

    Args:
        discipline: Optional discipline filter ("Architectural", "Structural",
                    "Mechanical", "Electrical", "Plumbing", etc.).
        search: Optional substring to match against sheet number or name.

    Returns:
        List of {sheet_id, sheet_number, sheet_name, discipline, revision, drawn_by}.
    """
    return await _delegate(config, "list_sheets", {"discipline": discipline, "search": search})


@tool
async def get_sheet_views(sheet_id: str, config: RunnableConfig) -> list[dict[str, Any]]:
    """
    Return all viewports (and their associated views) placed on a sheet.

    Args:
        sheet_id: Revit element ID of the sheet.

    Returns:
        List of {viewport_id, view_id, view_name, view_type, scale, center_x_mm, center_y_mm}.
    """
    return await _delegate(config, "get_sheet_views", {"sheet_id": sheet_id})


@tool
async def set_view_property(
    config: RunnableConfig,
    view_id: str,
    property_name: str,
    value: str,
) -> dict[str, Any]:
    """
    Set a property on a view such as scale, detail level, visual style, or
    discipline.  Useful for standardising views before printing/exporting.

    Args:
        view_id: Revit element ID of the view.
        property_name: Property to set – e.g. "Scale", "DetailLevel",
                       "VisualStyle", "Discipline", "ViewName".
        value: New value as a string ("1:100", "Fine", "Shaded", etc.).

    Returns:
        {success: bool, message: str}.
    """
    return await _delegate(config, "set_view_property", {
        "view_id": view_id, "property_name": property_name, "value": value,
    })


@tool
async def list_view_filters(view_id: str, config: RunnableConfig) -> list[dict[str, Any]]:
    """
    Return all view filters (parameter filters + selection filters) applied to a view,
    along with their visibility/override settings.

    Args:
        view_id: Revit element ID of the view.

    Returns:
        List of {filter_id, filter_name, is_visible, override_projection_color,
                 override_cut_color, override_halftone}.
    """
    return await _delegate(config, "list_view_filters", {"view_id": view_id})


@tool
async def list_view_templates(config: RunnableConfig) -> list[dict[str, Any]]:
    """
    Return all view templates defined in the project.

    Returns:
        List of {template_id, name, view_type, discipline, applied_count}.
    """
    return await _delegate(config, "list_view_templates", {})


@tool
async def apply_view_template(
    config: RunnableConfig,
    view_id: str,
    template_id: str,
) -> dict[str, Any]:
    """
    Apply a view template to a view.  All controlled properties will be
    overwritten by the template.

    Args:
        view_id: Revit element ID of the target view.
        template_id: Revit element ID of the view template to apply.

    Returns:
        {success: bool, message: str}.
    """
    return await _delegate(config, "apply_view_template", {
        "view_id": view_id, "template_id": template_id,
    })


@tool
async def set_active_view(view_id: str, config: RunnableConfig) -> dict[str, Any]:
    """
    Switch the Revit UI to display the specified view as the active view.

    Args:
        view_id: Revit element ID of the view to activate.

    Returns:
        {success: bool, view_name: str}.
    """
    return await _delegate(config, "set_active_view", {"view_id": view_id})


@tool
async def create_sheet(
    config: RunnableConfig,
    sheet_number: str,
    sheet_name: str,
    title_block_family_name: str,
    title_block_type_name: str | None = None,
) -> dict[str, Any]:
    """
    Create a new sheet in the project with the specified title block.
    Use list_element_types("Title Blocks") to discover available title block types.

    Args:
        sheet_number: Sheet number string (e.g. "A-101").
        sheet_name: Sheet name (e.g. "Ground Floor Plan").
        title_block_family_name: Title block family name (e.g. "A1 metric").
        title_block_type_name: Optional specific type within the title block family.

    Returns:
        {success: bool, sheet_id: str, sheet_number: str, sheet_name: str, message: str}.
    """
    return await _delegate(config, "create_sheet", {
        "sheet_number": sheet_number,
        "sheet_name": sheet_name,
        "title_block_family_name": title_block_family_name,
        "title_block_type_name": title_block_type_name,
    })


@tool
async def add_view_to_sheet(
    config: RunnableConfig,
    sheet_id: str,
    view_id: str,
    centre_x_mm: float,
    centre_y_mm: float,
    viewport_type_name: str | None = None,
) -> dict[str, Any]:
    """
    Place a viewport for the given view onto a sheet at the specified sheet coordinates.
    A view can only be placed on one sheet; this tool will error if the view is already
    on a different sheet.

    Args:
        sheet_id: Element ID of the target sheet.
        view_id: Element ID of the view to place.
        centre_x_mm: X position of the viewport centre on the sheet (mm from sheet origin).
        centre_y_mm: Y position of the viewport centre on the sheet (mm from sheet origin).
        viewport_type_name: Optional viewport type for the border style. Defaults to the
                            project default.

    Returns:
        {success: bool, viewport_id: str, message: str}.
    """
    return await _delegate(config, "add_view_to_sheet", {
        "sheet_id": sheet_id,
        "view_id": view_id,
        "centre_x_mm": centre_x_mm,
        "centre_y_mm": centre_y_mm,
        "viewport_type_name": viewport_type_name,
    })


@tool
async def add_schedule_to_sheet(
    config: RunnableConfig,
    sheet_id: str,
    schedule_id: str,
    origin_x_mm: float,
    origin_y_mm: float,
) -> dict[str, Any]:
    """
    Place a schedule view onto a sheet at the specified sheet coordinates.

    Args:
        sheet_id: Element ID of the target sheet.
        schedule_id: Element ID of the schedule view to place.
        origin_x_mm: X of the top-left corner of the schedule on the sheet (mm).
        origin_y_mm: Y of the top-left corner of the schedule on the sheet (mm).

    Returns:
        {success: bool, schedule_instance_id: str, message: str}.
    """
    return await _delegate(config, "add_schedule_to_sheet", {
        "sheet_id": sheet_id,
        "schedule_id": schedule_id,
        "origin_x_mm": origin_x_mm,
        "origin_y_mm": origin_y_mm,
    })


@tool
async def create_drafting_view(
    config: RunnableConfig,
    view_name: str,
    scale: int = 100,
) -> dict[str, Any]:
    """
    Create a new drafting view (blank view for 2D detail work with no model geometry).

    Args:
        view_name: Name of the new drafting view.
        scale: View scale denominator (e.g. 50 for 1:50, 100 for 1:100). Default 100.

    Returns:
        {success: bool, view_id: str, view_name: str, message: str}.
    """
    return await _delegate(config, "create_drafting_view", {
        "view_name": view_name,
        "scale": scale,
    })


@tool
async def create_schedule_view(
    config: RunnableConfig,
    category: str,
    schedule_name: str,
    fields: list[str] | None = None,
    filter_parameter: str | None = None,
    filter_value: str | None = None,
) -> dict[str, Any]:
    """
    Create a new element schedule for the given category.
    Optionally specify which parameter fields to add as columns, and an optional
    single filter to limit the rows.

    Args:
        category: The Revit category to schedule (e.g. "Doors", "Walls", "Rooms").
        schedule_name: Name to assign the new schedule view.
        fields: Optional list of parameter names to include as schedule columns
                (e.g. ["Family and Type", "Width", "Height", "Mark"]).
                If omitted, a default set of common parameters is used.
        filter_parameter: Optional parameter name to filter rows by.
        filter_value: Optional value to match for the filter (equality).

    Returns:
        {success: bool, schedule_id: str, schedule_name: str, field_count: int, message: str}.
    """
    return await _delegate(config, "create_schedule_view", {
        "category": category,
        "schedule_name": schedule_name,
        "fields": fields,
        "filter_parameter": filter_parameter,
        "filter_value": filter_value,
    })
