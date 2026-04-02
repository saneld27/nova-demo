"""Revit annotation and documentation tools – delegates execution to the Revit plugin."""
from __future__ import annotations

from typing import Any

from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool

from app.tools.elements import _delegate


@tool
async def list_dimensions(
    config: RunnableConfig,
    view_id: str | None = None,
    limit: int = 200,
) -> list[dict[str, Any]]:
    """
    Return dimension annotations in a view (defaults to the active view).

    Args:
        view_id: Revit view element ID. Defaults to the active view.
        limit: Maximum number to return.

    Returns:
        List of {id, dimension_type, value_mm, value_text, segment_count,
                 references: [{element_id, reference_type}]}.
    """
    return await _delegate(config, "list_dimensions", {"view_id": view_id, "limit": limit})


@tool
async def list_text_notes(
    config: RunnableConfig,
    view_id: str | None = None,
    search: str | None = None,
    limit: int = 200,
) -> list[dict[str, Any]]:
    """
    Return text note annotations in a view, with optional text content search.

    Args:
        view_id: Revit view element ID. Defaults to the active view.
        search: Optional substring to filter text content.
        limit: Maximum number to return.

    Returns:
        List of {id, text, type_name, position: {x, y}, width_mm}.
    """
    return await _delegate(config, "list_text_notes", {"view_id": view_id, "search": search, "limit": limit})


@tool
async def list_tags(
    config: RunnableConfig,
    view_id: str | None = None,
    category: str | None = None,
    limit: int = 300,
) -> list[dict[str, Any]]:
    """
    Return tag annotations in a view, optionally filtered by the category of
    the tagged element (e.g. "Rooms", "Doors", "Walls").

    Args:
        view_id: Revit view element ID. Defaults to the active view.
        category: Optional category of the element being tagged.
        limit: Maximum number to return.

    Returns:
        List of {tag_id, tag_family, tagged_element_id, tagged_element_category,
                 tag_text, has_leader, position: {x, y}}.
    """
    return await _delegate(config, "list_tags", {"view_id": view_id, "category": category, "limit": limit})


@tool
async def list_keynotes(
    config: RunnableConfig,
    view_id: str | None = None,
    limit: int = 200,
) -> list[dict[str, Any]]:
    """
    Return keynote annotations in a view, including their keynote value and
    the elements they reference.

    Args:
        view_id: Revit view element ID. Defaults to the active view.
        limit: Maximum number to return.

    Returns:
        List of {id, keynote_value, keynote_text, tagged_element_id, position: {x,y}}.
    """
    return await _delegate(config, "list_keynotes", {"view_id": view_id, "limit": limit})


@tool
async def list_revision_clouds(
    config: RunnableConfig,
    view_id: str | None = None,
    revision_sequence: int | None = None,
) -> list[dict[str, Any]]:
    """
    Return revision cloud elements, optionally filtered by view or revision
    sequence number.

    Args:
        view_id: Revit view element ID. Pass None to get clouds across all views.
        revision_sequence: Optional revision sequence number filter.

    Returns:
        List of {id, revision_sequence, revision_date, revision_description,
                 view_id, view_name, area_sqmm, comments}.
    """
    return await _delegate(config, "list_revision_clouds", {
        "view_id": view_id, "revision_sequence": revision_sequence,
    })


@tool
async def tag_element(
    config: RunnableConfig,
    element_id: str,
    view_id: str | None = None,
    tag_family_name: str | None = None,
    leader: bool = False,
) -> dict[str, Any]:
    """
    Place a tag annotation on an element in the specified view.  The tag
    family is auto-selected if not specified.

    Args:
        element_id: Revit element ID to tag.
        view_id: View in which to place the tag. Defaults to the active view.
        tag_family_name: Specific tag family to use. Auto-selected if None.
        leader: Whether to add a leader line from tag to element.

    Returns:
        {success: bool, tag_id: str, message: str}.
    """
    return await _delegate(config, "tag_element", {
        "element_id": element_id,
        "view_id": view_id,
        "tag_family_name": tag_family_name,
        "leader": leader,
    })


@tool
async def tag_by_category(
    config: RunnableConfig,
    category: str,
    view_id: str | None = None,
    tag_family_name: str | None = None,
    leader: bool = False,
    skip_already_tagged: bool = True,
) -> dict[str, Any]:
    """
    Tag all elements of a given category in a view at once (Tag All Not Tagged).
    Commonly used to bulk-tag doors, windows, rooms, structural members, etc.

    Args:
        category: Category name to tag (e.g. "Doors", "Windows", "Rooms", "Walls").
        view_id: View in which to place tags. Defaults to the active view.
        tag_family_name: Specific tag family to use. Auto-selected if None.
        leader: Whether to add leader lines (default False).
        skip_already_tagged: Skip elements that already have a tag (default True).

    Returns:
        {success: bool, tagged_count: int, skipped_count: int, message: str}.
    """
    return await _delegate(config, "tag_by_category", {
        "category": category,
        "view_id": view_id,
        "tag_family_name": tag_family_name,
        "leader": leader,
        "skip_already_tagged": skip_already_tagged,
    })


@tool
async def add_aligned_dimension(
    config: RunnableConfig,
    reference_element_ids: list[str],
    dimension_line_x_mm: float,
    dimension_line_y_mm: float,
    view_id: str | None = None,
    dimension_type_name: str | None = None,
) -> dict[str, Any]:
    """
    Add an aligned dimension annotation across two or more elements (e.g. walls, columns,
    reference planes). The dimension line is placed at the specified coordinate.
    The references are the faces/axes that define the dimension segments.

    Args:
        reference_element_ids: Ordered list of element IDs whose
                               auto-detected faces/axes form the dimension references.
                               Minimum 2 elements.
        dimension_line_x_mm: X coordinate of the dimension line offset position (mm).
        dimension_line_y_mm: Y coordinate of the dimension line offset position (mm).
        view_id: View in which to place the dimension. Defaults to active view.
        dimension_type_name: Specific dimension type (e.g. "Linear - 3mm Arial").

    Returns:
        {success: bool, dimension_id: str, value_mm: float, message: str}.
    """
    return await _delegate(config, "add_aligned_dimension", {
        "reference_element_ids": reference_element_ids,
        "dimension_line_x_mm": dimension_line_x_mm,
        "dimension_line_y_mm": dimension_line_y_mm,
        "view_id": view_id,
        "dimension_type_name": dimension_type_name,
    })


# DISABLED – too complex for plugin side
@tool
async def add_linear_dimension(
    config: RunnableConfig,
    start_x_mm: float,
    start_y_mm: float,
    end_x_mm: float,
    end_y_mm: float,
    line_position_x_mm: float,
    line_position_y_mm: float,
    view_id: str | None = None,
    orientation: str = "horizontal",
    dimension_type_name: str | None = None,
) -> dict[str, Any]:
    """
    Add a linear (horizontal or vertical) dimension between two explicit points.

    Args:
        start_x_mm: X of the first reference point (mm).
        start_y_mm: Y of the first reference point (mm).
        end_x_mm: X of the second reference point (mm).
        end_y_mm: Y of the second reference point (mm).
        line_position_x_mm: X coordinate where the dimension line is drawn (mm).
        line_position_y_mm: Y coordinate where the dimension line is drawn (mm).
        view_id: View in which to place the dimension. Defaults to active view.
        orientation: "horizontal" (default) measures horizontal distance;
                     "vertical" measures vertical distance;
                     "aligned" measures true distance.
        dimension_type_name: Optional dimension type name.

    Returns:
        {success: bool, dimension_id: str, value_mm: float, message: str}.
    """
    return await _delegate(config, "add_linear_dimension", {
        "start_x_mm": start_x_mm,
        "start_y_mm": start_y_mm,
        "end_x_mm": end_x_mm,
        "end_y_mm": end_y_mm,
        "line_position_x_mm": line_position_x_mm,
        "line_position_y_mm": line_position_y_mm,
        "view_id": view_id,
        "orientation": orientation,
        "dimension_type_name": dimension_type_name,
    })


# DISABLED – too complex for plugin side (returns error due to missing API method)
@tool
async def add_radial_dimension(
    config: RunnableConfig,
    arc_element_id: str,
    leader_end_x_mm: float,
    leader_end_y_mm: float,
    view_id: str | None = None,
    dimension_type_name: str | None = None,
) -> dict[str, Any]:
    """
    Add a radial dimension to a circular arc element (curved wall, arc model line, etc.)
    showing its radius with a leader line to the arc centre.

    Args:
        arc_element_id: Element ID of the arc-shaped element to dimension.
        leader_end_x_mm: X position for the free end of the dimension leader (mm).
        leader_end_y_mm: Y position for the free end of the dimension leader (mm).
        view_id: View in which to place the dimension. Defaults to active view.
        dimension_type_name: Optional dimension type name.

    Returns:
        {success: bool, dimension_id: str, radius_mm: float, message: str}.
    """
    return await _delegate(config, "add_radial_dimension", {
        "arc_element_id": arc_element_id,
        "leader_end_x_mm": leader_end_x_mm,
        "leader_end_y_mm": leader_end_y_mm,
        "view_id": view_id,
        "dimension_type_name": dimension_type_name,
    })


# DISABLED – too complex for plugin side (returns error due to missing API method)
@tool
async def add_diameter_dimension(
    config: RunnableConfig,
    arc_element_id: str,
    leader_end_x_mm: float,
    leader_end_y_mm: float,
    view_id: str | None = None,
    dimension_type_name: str | None = None,
) -> dict[str, Any]:
    """
    Add a diameter dimension (⌀) to a circular arc element.

    Args:
        arc_element_id: Element ID of the arc-shaped element.
        leader_end_x_mm: X position for the end of the dimension leader (mm).
        leader_end_y_mm: Y position for the end of the dimension leader (mm).
        view_id: View in which to place the dimension. Defaults to active view.
        dimension_type_name: Optional dimension type name.

    Returns:
        {success: bool, dimension_id: str, diameter_mm: float, message: str}.
    """
    return await _delegate(config, "add_diameter_dimension", {
        "arc_element_id": arc_element_id,
        "leader_end_x_mm": leader_end_x_mm,
        "leader_end_y_mm": leader_end_y_mm,
        "view_id": view_id,
        "dimension_type_name": dimension_type_name,
    })


# DISABLED – too complex for plugin side
@tool
async def add_angular_dimension(
    config: RunnableConfig,
    element_id_a: str,
    element_id_b: str,
    arc_position_x_mm: float,
    arc_position_y_mm: float,
    view_id: str | None = None,
    dimension_type_name: str | None = None,
) -> dict[str, Any]:
    """
    Add an angular dimension between two linear elements (walls, lines, beams)
    showing the angle between them.

    Args:
        element_id_a: First linear element ID.
        element_id_b: Second linear element ID.
        arc_position_x_mm: X near the desired arc position for the dimension (mm).
        arc_position_y_mm: Y near the desired arc position for the dimension (mm).
        view_id: View in which to place the dimension. Defaults to active view.
        dimension_type_name: Optional dimension type name.

    Returns:
        {success: bool, dimension_id: str, angle_degrees: float, message: str}.
    """
    return await _delegate(config, "add_angular_dimension", {
        "element_id_a": element_id_a,
        "element_id_b": element_id_b,
        "arc_position_x_mm": arc_position_x_mm,
        "arc_position_y_mm": arc_position_y_mm,
        "view_id": view_id,
        "dimension_type_name": dimension_type_name,
    })


# DISABLED – too complex for plugin side
@tool
async def add_arc_length_dimension(
    config: RunnableConfig,
    arc_element_id: str,
    leader_end_x_mm: float,
    leader_end_y_mm: float,
    view_id: str | None = None,
    dimension_type_name: str | None = None,
) -> dict[str, Any]:
    """
    Add an arc length dimension to a curved element (arc wall, arc model line, etc.)
    showing the length along the curve.

    Args:
        arc_element_id: Element ID of the arc element.
        leader_end_x_mm: X position for the dimension text / leader end (mm).
        leader_end_y_mm: Y position for the dimension text / leader end (mm).
        view_id: View in which to place the dimension. Defaults to active view.
        dimension_type_name: Optional dimension type name.

    Returns:
        {success: bool, dimension_id: str, arc_length_mm: float, message: str}.
    """
    return await _delegate(config, "add_arc_length_dimension", {
        "arc_element_id": arc_element_id,
        "leader_end_x_mm": leader_end_x_mm,
        "leader_end_y_mm": leader_end_y_mm,
        "view_id": view_id,
        "dimension_type_name": dimension_type_name,
    })


# DISABLED – too complex for plugin side
@tool
async def add_spot_elevation(
    config: RunnableConfig,
    element_id: str,
    leader_origin_x_mm: float,
    leader_origin_y_mm: float,
    leader_end_x_mm: float,
    leader_end_y_mm: float,
    view_id: str | None = None,
    spot_type_name: str | None = None,
) -> dict[str, Any]:
    """
    Add a spot elevation annotation showing the absolute elevation of a point on
    a floor, slab, roof, or topography surface.

    Args:
        element_id: Element whose surface defines the elevation reference point.
        leader_origin_x_mm: X of the point on the element surface (mm).
        leader_origin_y_mm: Y of the point on the element surface (mm).
        leader_end_x_mm: X of the leader shoulder / text position (mm).
        leader_end_y_mm: Y of the leader shoulder / text position (mm).
        view_id: View in which to place the annotation. Defaults to active view.
        spot_type_name: Optional spot elevation type name.

    Returns:
        {success: bool, annotation_id: str, elevation_mm: float, message: str}.
    """
    return await _delegate(config, "add_spot_elevation", {
        "element_id": element_id,
        "leader_origin_x_mm": leader_origin_x_mm,
        "leader_origin_y_mm": leader_origin_y_mm,
        "leader_end_x_mm": leader_end_x_mm,
        "leader_end_y_mm": leader_end_y_mm,
        "view_id": view_id,
        "spot_type_name": spot_type_name,
    })


# DISABLED – too complex for plugin side
@tool
async def add_spot_coordinate(
    config: RunnableConfig,
    element_id: str,
    leader_origin_x_mm: float,
    leader_origin_y_mm: float,
    leader_end_x_mm: float,
    leader_end_y_mm: float,
    view_id: str | None = None,
    spot_type_name: str | None = None,
) -> dict[str, Any]:
    """
    Add a spot coordinate annotation showing the North/East (Y/X) survey coordinates
    of a point on an element.

    Args:
        element_id: Element whose surface defines the coordinate reference point.
        leader_origin_x_mm: X of the point on the element surface (mm).
        leader_origin_y_mm: Y of the point on the element surface (mm).
        leader_end_x_mm: X of the leader shoulder / text position (mm).
        leader_end_y_mm: Y of the leader shoulder / text position (mm).
        view_id: View in which to place the annotation. Defaults to active view.
        spot_type_name: Optional spot coordinate type name.

    Returns:
        {success: bool, annotation_id: str, north_mm: float, east_mm: float, message: str}.
    """
    return await _delegate(config, "add_spot_coordinate", {
        "element_id": element_id,
        "leader_origin_x_mm": leader_origin_x_mm,
        "leader_origin_y_mm": leader_origin_y_mm,
        "leader_end_x_mm": leader_end_x_mm,
        "leader_end_y_mm": leader_end_y_mm,
        "view_id": view_id,
        "spot_type_name": spot_type_name,
    })
