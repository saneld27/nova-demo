"""
Revit drafting tools – model text, model lines, text notes, filled/masking regions,
symbols, and text utilities (find/replace, spell-check).

All tools delegate execution to the Revit plugin.
"""
from __future__ import annotations

from typing import Any

from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool

from app.tools.elements import _delegate


@tool
async def add_model_text(
    config: RunnableConfig,
    text: str,
    position_x_mm: float,
    position_y_mm: float,
    position_z_mm: float,
    level_name: str,
    work_plane: str = "XY",
    depth_mm: float = 150.0,
    font_size_mm: float = 300.0,
    text_type_name: str | None = None,
    horizontal_align: str = "Center",
) -> dict[str, Any]:
    """
    Add a 3-D Model Text element to the model at a given position.
    Model Text is visible in 3-D views and sections (unlike annotation text notes).

    Args:
        text: The string content of the model text.
        position_x_mm: X of the insertion point in project coordinates (mm).
        position_y_mm: Y of the insertion point (mm).
        position_z_mm: Z of the insertion point (mm).
        level_name: Host level name (e.g. "Level 1").
        work_plane: Work plane orientation – "XY" (default, horizontal), "XZ", or "YZ".
        depth_mm: Extrusion depth of the letters (mm, default 150).
        font_size_mm: Height of the letters (mm, default 300).
        text_type_name: Optional Model Text type name. Defaults to the first available type.
        horizontal_align: Text justification – "Left", "Center" (default), or "Right".

    Returns:
        {success: bool, element_id: str, message: str}.
    """
    return await _delegate(config, "add_model_text", {
        "text": text,
        "position_x_mm": position_x_mm,
        "position_y_mm": position_y_mm,
        "position_z_mm": position_z_mm,
        "level_name": level_name,
        "work_plane": work_plane,
        "depth_mm": depth_mm,
        "font_size_mm": font_size_mm,
        "text_type_name": text_type_name,
        "horizontal_align": horizontal_align,
    })


@tool
async def add_model_line(
    config: RunnableConfig,
    start_x_mm: float,
    start_y_mm: float,
    start_z_mm: float,
    end_x_mm: float,
    end_y_mm: float,
    end_z_mm: float,
    line_style: str = "Model Lines",
    work_plane_level: str | None = None,
) -> dict[str, Any]:
    """
    Add a straight model line between two 3-D points.
    Model lines are visible in all views that intersect their plane.

    Args:
        start_x_mm: Start X in project coordinates (mm).
        start_y_mm: Start Y (mm).
        start_z_mm: Start Z (mm).
        end_x_mm: End X (mm).
        end_y_mm: End Y (mm).
        end_z_mm: End Z (mm).
        line_style: Line style name (e.g. "Model Lines", "Hidden Lines"). Default "Model Lines".
        work_plane_level: Optional level name to use as the work plane for the line.
                          If omitted, the line is placed on the plane defined by its points.

    Returns:
        {success: bool, element_id: str, message: str}.
    """
    return await _delegate(config, "add_model_line", {
        "start_x_mm": start_x_mm,
        "start_y_mm": start_y_mm,
        "start_z_mm": start_z_mm,
        "end_x_mm": end_x_mm,
        "end_y_mm": end_y_mm,
        "end_z_mm": end_z_mm,
        "line_style": line_style,
        "work_plane_level": work_plane_level,
    })


@tool
async def create_text_note(
    config: RunnableConfig,
    text: str,
    position_x_mm: float,
    position_y_mm: float,
    view_id: str | None = None,
    width_mm: float = 500.0,
    horizontal_align: str = "Left",
    text_type_name: str | None = None,
    rotation_degrees: float = 0.0,
) -> dict[str, Any]:
    """
    Create a 2-D annotation text note in the specified view at the given position.
    Text notes are view-specific annotations (not visible in 3-D by default).

    Args:
        text: The text content.
        position_x_mm: X of the text insertion point in model coordinates (mm).
        position_y_mm: Y of the text insertion point (mm).
        view_id: View in which to place the text note. Defaults to the active view.
        width_mm: Wrap width for the text box (mm, default 500).
        horizontal_align: "Left" (default), "Center", or "Right".
        text_type_name: Optional text note type name (controls font, size, etc.).
        rotation_degrees: Rotation of the text note about its insertion point (default 0).

    Returns:
        {success: bool, element_id: str, message: str}.
    """
    return await _delegate(config, "create_text_note", {
        "text": text,
        "position_x_mm": position_x_mm,
        "position_y_mm": position_y_mm,
        "view_id": view_id,
        "width_mm": width_mm,
        "horizontal_align": horizontal_align,
        "text_type_name": text_type_name,
        "rotation_degrees": rotation_degrees,
    })


@tool
async def edit_text_note(
    config: RunnableConfig,
    element_id: str,
    new_text: str,
) -> dict[str, Any]:
    """
    Edit the text content of an existing text note element.

    Args:
        element_id: Element ID of the text note to edit.
        new_text: Replacement text content.

    Returns:
        {success: bool, message: str}.
    """
    return await _delegate(config, "edit_text_note", {
        "element_id": element_id,
        "new_text": new_text,
    })


@tool
async def find_replace_text(
    config: RunnableConfig,
    find_string: str,
    replace_string: str,
    view_id: str | None = None,
    scope: str = "view",
    case_sensitive: bool = False,
    whole_word: bool = False,
) -> dict[str, Any]:
    """
    Find and replace text across text notes and model text in a view or the entire model.
    Equivalent to Revit's Find/Replace dialog on text elements.

    Args:
        find_string: The substring (or exact word if whole_word=True) to search for.
        replace_string: The replacement string.
        view_id: If scope is "view", restrict search to this view. Defaults to the active view.
        scope: "view" (default) – search the current/specified view only;
               "model" – search all text notes and model text in the entire document.
        case_sensitive: Match case (default False).
        whole_word: Match whole words only (default False).

    Returns:
        {success: bool, replaced_count: int, element_ids_modified: [str], message: str}.
    """
    return await _delegate(config, "find_replace_text", {
        "find_string": find_string,
        "replace_string": replace_string,
        "view_id": view_id,
        "scope": scope,
        "case_sensitive": case_sensitive,
        "whole_word": whole_word,
    })


@tool
async def check_spelling(
    config: RunnableConfig,
    view_id: str | None = None,
    scope: str = "view",
) -> dict[str, Any]:
    """
    Run a spell-check on text notes and model text, returning a list of
    suspected misspellings with their element IDs.
    Note: This uses Revit's built-in spell-check dictionary. Corrections must be
    made manually via edit_text_note or find_replace_text.

    Args:
        view_id: If scope is "view", restrict to this view. Defaults to active view.
        scope: "view" (default) or "model".

    Returns:
        {suspected_misspellings: [{element_id, word, context_text}], total_count: int}.
    """
    return await _delegate(config, "check_spelling", {
        "view_id": view_id,
        "scope": scope,
    })


# DISABLED – too complex for plugin side
@tool
async def add_masking_region(
    config: RunnableConfig,
    boundary_points: list[dict[str, float]],
    view_id: str | None = None,
    line_style: str = "Masking Region Lines",
) -> dict[str, Any]:
    """
    Add a masking region (white/filled area that covers underlying content) in the
    specified view. Masking regions are commonly used to blank out portions of a view.

    Args:
        boundary_points: Ordered list of XY points forming the closed boundary loop,
                         in model coordinates (mm). E.g. [{"x": 0, "y": 0}, ...].
                         Interior voids can be passed as a second sub-list if needed.
        view_id: Target view. Defaults to the active view.
        line_style: Line style name for the region boundary (default "Masking Region Lines").

    Returns:
        {success: bool, element_id: str, message: str}.
    """
    return await _delegate(config, "add_masking_region", {
        "boundary_points": boundary_points,
        "view_id": view_id,
        "line_style": line_style,
    })


# DISABLED – too complex for plugin side
@tool
async def add_filled_region(
    config: RunnableConfig,
    boundary_points: list[dict[str, float]],
    fill_pattern_name: str,
    view_id: str | None = None,
    line_style: str = "Medium Lines",
    color_rgb: list[int] | None = None,
) -> dict[str, Any]:
    """
    Add a filled region with a drafting fill pattern in the specified view.
    Filled regions are annotation elements visible only in the view they are placed in.

    Args:
        boundary_points: Ordered list of XY points forming the closed outer loop (mm).
        fill_pattern_name: Name of the fill pattern to apply (e.g. "Diagonal Crosshatch",
                           "Solid fill"). Use list_materials() to discover pattern names.
        view_id: Target view. Defaults to the active view.
        line_style: Line style for the region boundary (default "Medium Lines").
        color_rgb: Optional fill colour as [R, G, B] integers 0-255 (e.g. [255, 0, 0]).

    Returns:
        {success: bool, element_id: str, message: str}.
    """
    return await _delegate(config, "add_filled_region", {
        "boundary_points": boundary_points,
        "fill_pattern_name": fill_pattern_name,
        "view_id": view_id,
        "line_style": line_style,
        "color_rgb": color_rgb,
    })


@tool
async def add_symbol(
    config: RunnableConfig,
    family_name: str,
    type_name: str,
    position_x_mm: float,
    position_y_mm: float,
    view_id: str | None = None,
    rotation_degrees: float = 0.0,
) -> dict[str, Any]:
    """
    Place an annotation symbol (a Revit generic annotation or detail component family)
    in a view at the given model-coordinate position.
    Common symbol categories: "Generic Annotations", "Detail Items".
    Use list_element_types("Generic Annotations") to discover available symbols.

    Args:
        family_name: Annotation or detail family name (e.g. "North Arrow", "Break Line").
        type_name: Type within the family.
        position_x_mm: X placement coordinate in model space (mm).
        position_y_mm: Y placement coordinate (mm).
        view_id: Target view. Defaults to the active view.
        rotation_degrees: Rotation about Z axis (default 0).

    Returns:
        {success: bool, element_id: str, message: str}.
    """
    return await _delegate(config, "add_symbol", {
        "family_name": family_name,
        "type_name": type_name,
        "position_x_mm": position_x_mm,
        "position_y_mm": position_y_mm,
        "view_id": view_id,
        "rotation_degrees": rotation_degrees,
    })


@tool
async def add_detail_line(
    config: RunnableConfig,
    start_x_mm: float,
    start_y_mm: float,
    end_x_mm: float,
    end_y_mm: float,
    view_id: str | None = None,
    line_style: str = "Medium Lines",
) -> dict[str, Any]:
    """
    Add a 2-D detail line (view-specific drafted line) in the specified view.
    Unlike model lines, detail lines are visible only in the view they are placed in.

    Args:
        start_x_mm: Start X in model coordinates (mm).
        start_y_mm: Start Y (mm).
        end_x_mm: End X (mm).
        end_y_mm: End Y (mm).
        view_id: Target view. Defaults to the active view.
        line_style: Revit line style name (e.g. "Thin Lines", "Medium Lines",
                    "Wide Lines", "Dashed"). Default "Medium Lines".

    Returns:
        {success: bool, element_id: str, message: str}.
    """
    return await _delegate(config, "add_detail_line", {
        "start_x_mm": start_x_mm,
        "start_y_mm": start_y_mm,
        "end_x_mm": end_x_mm,
        "end_y_mm": end_y_mm,
        "view_id": view_id,
        "line_style": line_style,
    })


# DISABLED – too complex for plugin side
@tool
async def add_color_fill_legend(
    config: RunnableConfig,
    view_id: str | None = None,
    scheme_name: str | None = None,
    position_x_mm: float = 0.0,
    position_y_mm: float = 0.0,
) -> dict[str, Any]:
    """
    Add a color fill legend (room/area color fill) to a view.
    The legend displays the color key for a color scheme already applied to the view.
    Use this after a room or area color scheme has been assigned to the view.

    Args:
        view_id: Target view with color fill applied. Defaults to the active view.
        scheme_name: Optional name of the color scheme to display. If omitted, uses
                     the scheme already applied to the view.
        position_x_mm: X position of the legend on the sheet/view (mm).
        position_y_mm: Y position of the legend (mm).

    Returns:
        {success: bool, element_id: str, message: str}.
    """
    return await _delegate(config, "add_color_fill_legend", {
        "view_id": view_id,
        "scheme_name": scheme_name,
        "position_x_mm": position_x_mm,
        "position_y_mm": position_y_mm,
    })
