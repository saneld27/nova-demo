"""
Revit modification tools – write operations that change the model.

Every tool here triggers a write transaction in Revit.  The agent should
confirm intent with the user before calling these unless the user has
explicitly said to just do it.
"""
from __future__ import annotations

from typing import Any

from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool

from app.tools.elements import _delegate


@tool
async def move_element(
    config: RunnableConfig,
    element_id: str,
    delta_x_mm: float,
    delta_y_mm: float,
    delta_z_mm: float = 0.0,
) -> dict[str, Any]:
    """
    Move an element by a translation vector (delta in mm).

    Args:
        element_id: Revit element ID to move.
        delta_x_mm: Translation in the X direction (mm).
        delta_y_mm: Translation in the Y direction (mm).
        delta_z_mm: Translation in the Z direction (mm, default 0).

    Returns:
        {success: bool, message: str, new_location: {x, y, z}}.
    """
    return await _delegate(config, "move_element", {
        "element_id": element_id, "delta_x_mm": delta_x_mm,
        "delta_y_mm": delta_y_mm, "delta_z_mm": delta_z_mm,
    })


@tool
async def rotate_element(
    config: RunnableConfig,
    element_id: str,
    angle_degrees: float,
    axis: str = "Z",
) -> dict[str, Any]:
    """
    Rotate an element around a specified axis through its own origin.

    Args:
        element_id: Revit element ID.
        angle_degrees: Rotation angle in degrees (positive = counter-clockwise).
        axis: Rotation axis – "X", "Y", or "Z" (default "Z" for plan rotation).

    Returns:
        {success: bool, message: str}.
    """
    return await _delegate(config, "rotate_element", {
        "element_id": element_id, "angle_degrees": angle_degrees, "axis": axis,
    })


@tool
async def copy_element(
    config: RunnableConfig,
    element_id: str,
    delta_x_mm: float,
    delta_y_mm: float,
    delta_z_mm: float = 0.0,
) -> dict[str, Any]:
    """
    Copy an element and place the copy at an offset from the original.

    Args:
        element_id: Revit element ID to copy.
        delta_x_mm: X offset for the copy (mm).
        delta_y_mm: Y offset for the copy (mm).
        delta_z_mm: Z offset for the copy (mm, default 0).

    Returns:
        {success: bool, new_element_id: str, message: str}.
    """
    return await _delegate(config, "copy_element", {
        "element_id": element_id, "delta_x_mm": delta_x_mm,
        "delta_y_mm": delta_y_mm, "delta_z_mm": delta_z_mm,
    })


@tool
async def mirror_element(
    config: RunnableConfig,
    element_id: str,
    mirror_axis: str,
    axis_coordinate_mm: float,
) -> dict[str, Any]:
    """
    Mirror an element across a plane parallel to a world axis.

    Args:
        element_id: Revit element ID to mirror.
        mirror_axis: Plane normal axis – "X" (YZ plane) or "Y" (XZ plane).
        axis_coordinate_mm: Position of the mirror plane along the axis (mm).

    Returns:
        {success: bool, new_element_id: str, message: str}.
    """
    return await _delegate(config, "mirror_element", {
        "element_id": element_id, "mirror_axis": mirror_axis,
        "axis_coordinate_mm": axis_coordinate_mm,
    })


@tool
async def delete_element(
    config: RunnableConfig,
    element_id: str,
) -> dict[str, Any]:
    """
    Delete an element from the model.  This is irreversible without an undo.
    Confirm with the user before calling.

    Args:
        element_id: Revit element ID to delete.

    Returns:
        {success: bool, message: str, also_deleted: [element_id]}.
    """
    return await _delegate(config, "delete_element", {"element_id": element_id})


@tool
async def create_wall(
    config: RunnableConfig,
    start_x_mm: float,
    start_y_mm: float,
    end_x_mm: float,
    end_y_mm: float,
    level_name: str,
    wall_type_name: str,
    height_mm: float,
    base_offset_mm: float = 0.0,
) -> dict[str, Any]:
    """
    Create a straight wall between two XY points at the given level.
    Use list_element_types("Walls") to find valid wall_type_name values.

    Args:
        start_x_mm: Start point X in project coordinates (mm).
        start_y_mm: Start point Y in project coordinates (mm).
        end_x_mm: End point X (mm).
        end_y_mm: End point Y (mm).
        level_name: Name of the base level (e.g. "Level 1").
        wall_type_name: Exact wall type name.
        height_mm: Unconnected wall height (mm).
        base_offset_mm: Offset from the base level (mm, default 0).

    Returns:
        {success: bool, element_id: str, message: str}.
    """
    return await _delegate(config, "create_wall", {
        "start_x_mm": start_x_mm, "start_y_mm": start_y_mm,
        "end_x_mm": end_x_mm, "end_y_mm": end_y_mm,
        "level_name": level_name, "wall_type_name": wall_type_name,
        "height_mm": height_mm, "base_offset_mm": base_offset_mm,
    })


@tool
async def create_floor(
    config: RunnableConfig,
    boundary_points: list[dict[str, float]],
    level_name: str,
    floor_type_name: str,
    offset_mm: float = 0.0,
) -> dict[str, Any]:
    """
    Create a floor from a closed boundary polygon.
    Use list_element_types("Floors") to find valid floor_type_name values.

    Args:
        boundary_points: Ordered list of XY points forming a closed loop,
                         e.g. [{"x": 0, "y": 0}, {"x": 5000, "y": 0}, ...] (mm).
        level_name: Name of the level (e.g. "Level 1").
        floor_type_name: Exact floor type name.
        offset_mm: Height offset from the level (mm, default 0).

    Returns:
        {success: bool, element_id: str, area_sqm: float, message: str}.
    """
    return await _delegate(config, "create_floor", {
        "boundary_points": boundary_points, "level_name": level_name,
        "floor_type_name": floor_type_name, "offset_mm": offset_mm,
    })


@tool
async def place_family_instance(
    config: RunnableConfig,
    family_name: str,
    type_name: str,
    x_mm: float,
    y_mm: float,
    z_mm: float,
    level_name: str,
    rotation_degrees: float = 0.0,
) -> dict[str, Any]:
    """
    Place a family instance (of any category) at the given coordinates.
    For hosted families (wall-based, ceiling-based), the nearest suitable host
    will be used automatically.
    Use list_loaded_families() or list_element_types() to find valid names.

    Args:
        family_name: Loaded family name (e.g. "Single-Flush").
        type_name: Type within the family (e.g. "36\" x 84\"").
        x_mm: X coordinate in project coordinates (mm).
        y_mm: Y coordinate (mm).
        z_mm: Z coordinate (mm).
        level_name: Base level name.
        rotation_degrees: Rotation about Z axis (default 0).

    Returns:
        {success: bool, element_id: str, message: str}.
    """
    return await _delegate(config, "place_family_instance", {
        "family_name": family_name, "type_name": type_name,
        "x_mm": x_mm, "y_mm": y_mm, "z_mm": z_mm,
        "level_name": level_name, "rotation_degrees": rotation_degrees,
    })


@tool
async def create_room(
    config: RunnableConfig,
    x_mm: float,
    y_mm: float,
    level_name: str,
    name: str | None = None,
    number: str | None = None,
) -> dict[str, Any]:
    """
    Place a room at the given XY point on a level.  Revit will use existing
    room-bounding elements to determine the room boundaries automatically.

    Args:
        x_mm: X coordinate inside the desired room boundary (mm).
        y_mm: Y coordinate inside the desired room boundary (mm).
        level_name: Level name.
        name: Optional room name to assign.
        number: Optional room number to assign.

    Returns:
        {success: bool, element_id: str, name: str, number: str,
         area_sqm: float, message: str}.
    """
    return await _delegate(config, "create_room", {
        "x_mm": x_mm, "y_mm": y_mm, "level_name": level_name,
        "name": name, "number": number,
    })


@tool
async def pin_element(element_id: str, config: RunnableConfig) -> dict[str, Any]:
    """
    Pin an element to prevent accidental moves or deletions.

    Args:
        element_id: Revit element ID.

    Returns:
        {success: bool, message: str}.
    """
    return await _delegate(config, "pin_element", {"element_id": element_id})


@tool
async def unpin_element(element_id: str, config: RunnableConfig) -> dict[str, Any]:
    """
    Unpin a previously pinned element, allowing it to be moved or deleted.

    Args:
        element_id: Revit element ID.

    Returns:
        {success: bool, message: str}.
    """
    return await _delegate(config, "unpin_element", {"element_id": element_id})


@tool
async def replace_element(
    config: RunnableConfig,
    element_id: str,
    new_family_name: str,
    new_type_name: str,
) -> dict[str, Any]:
    """
    Replace an element with a different family/type while preserving its location,
    level, host, and parameter values where parameter names match.
    Use list_loaded_families() or list_element_types() to find valid names.

    Args:
        element_id: Revit element ID to replace.
        new_family_name: Name of the family to place (e.g. "Single-Flush").
        new_type_name: Type name within the family (e.g. '36" x 84"').

    Returns:
        {success: bool, old_element_id: str, new_element_id: str, message: str}.
    """
    return await _delegate(config, "replace_element", {
        "element_id": element_id,
        "new_family_name": new_family_name,
        "new_type_name": new_type_name,
    })


@tool
async def add_door(
    config: RunnableConfig,
    wall_id: str,
    family_name: str,
    type_name: str,
    position_along_wall_mm: float,
    level_name: str,
    from_wall_end: str = "start",
    flip_hand: bool = False,
    flip_facing: bool = False,
) -> dict[str, Any]:
    """
    Place a door instance on an existing wall at a specified position.
    Use list_element_types("Doors") to discover available door types.

    Args:
        wall_id: Element ID of the host wall.
        family_name: Door family name (e.g. "Single-Flush").
        type_name: Door type name (e.g. '36" x 84"').
        position_along_wall_mm: Distance from the wall reference end to the door centre (mm).
        level_name: Base level name.
        from_wall_end: Reference end – "start" (default) or "end".
        flip_hand: Flip the hand of the door (default False).
        flip_facing: Flip the facing of the door (default False).

    Returns:
        {success: bool, element_id: str, message: str}.
    """
    return await _delegate(config, "add_door", {
        "wall_id": wall_id,
        "family_name": family_name,
        "type_name": type_name,
        "position_along_wall_mm": position_along_wall_mm,
        "level_name": level_name,
        "from_wall_end": from_wall_end,
        "flip_hand": flip_hand,
        "flip_facing": flip_facing,
    })


@tool
async def add_window(
    config: RunnableConfig,
    host_id: str,
    family_name: str,
    type_name: str,
    position_along_host_mm: float,
    sill_height_mm: float,
    level_name: str,
    from_host_end: str = "start",
    flip_hand: bool = False,
    flip_facing: bool = False,
) -> dict[str, Any]:
    """
    Place a window instance on an existing wall or roof at a specified position.
    Use list_element_types("Windows") to discover available window types.

    Args:
        host_id: Element ID of the host wall or roof.
        family_name: Window family name (e.g. "Fixed").
        type_name: Window type name (e.g. '24" x 48"').
        position_along_host_mm: Distance from the host reference end to the window centre (mm).
        sill_height_mm: Height of the window sill from the base level (mm).
        level_name: Base level name.
        from_host_end: Reference end – "start" (default) or "end".
        flip_hand: Flip the hand orientation (default False).
        flip_facing: Flip the facing orientation (default False).

    Returns:
        {success: bool, element_id: str, message: str}.
    """
    return await _delegate(config, "add_window", {
        "host_id": host_id,
        "family_name": family_name,
        "type_name": type_name,
        "position_along_host_mm": position_along_host_mm,
        "sill_height_mm": sill_height_mm,
        "level_name": level_name,
        "from_host_end": from_host_end,
        "flip_hand": flip_hand,
        "flip_facing": flip_facing,
    })


# DISABLED – too complex for plugin side
@tool
async def trim_extend_elements(
    config: RunnableConfig,
    element_id: str,
    reference_id: str,
    trim_or_extend: str = "trim",
) -> dict[str, Any]:
    """
    Trim or extend a linear element (wall, line, beam) to meet a reference element.
    Equivalent to Revit's Trim/Extend command.

    Args:
        element_id: Element to trim or extend.
        reference_id: Reference element defining the boundary.
        trim_or_extend: "trim" (default) to shorten, or "extend" to lengthen.

    Returns:
        {success: bool, message: str}.
    """
    return await _delegate(config, "trim_extend_elements", {
        "element_id": element_id,
        "reference_id": reference_id,
        "trim_or_extend": trim_or_extend,
    })


@tool
async def offset_element(
    config: RunnableConfig,
    element_id: str,
    offset_mm: float,
    copy: bool = True,
) -> dict[str, Any]:
    """
    Offset a wall, line, beam, or other linear/planar element by a distance.
    Positive offset is to the right of the element's direction vector.

    Args:
        element_id: Element to offset.
        offset_mm: Perpendicular offset distance (mm). Positive = right, negative = left.
        copy: If True (default) retain original and create offset copy; if False move in place.

    Returns:
        {success: bool, new_element_id: str | None, message: str}.
    """
    return await _delegate(config, "offset_element", {
        "element_id": element_id,
        "offset_mm": offset_mm,
        "copy": copy,
    })


# DISABLED – too complex for plugin side
@tool
async def scale_element(
    config: RunnableConfig,
    element_id: str,
    scale_factor: float,
    origin_x_mm: float | None = None,
    origin_y_mm: float | None = None,
    origin_z_mm: float | None = None,
) -> dict[str, Any]:
    """
    Scale an element uniformly about an optional origin point.
    If no origin is provided the element's own centre is used.
    Note: scale applies only to elements that support scaling (family instances, detail items, etc.).

    Args:
        element_id: Element to scale.
        scale_factor: Uniform scale factor (e.g. 2.0 = double size, 0.5 = half size).
        origin_x_mm: X of the scale origin in project coordinates (mm). Defaults to element centre.
        origin_y_mm: Y of the scale origin (mm).
        origin_z_mm: Z of the scale origin (mm).

    Returns:
        {success: bool, message: str}.
    """
    return await _delegate(config, "scale_element", {
        "element_id": element_id,
        "scale_factor": scale_factor,
        "origin_x_mm": origin_x_mm,
        "origin_y_mm": origin_y_mm,
        "origin_z_mm": origin_z_mm,
    })


@tool
async def array_element_linear(
    config: RunnableConfig,
    element_id: str,
    count: int,
    delta_x_mm: float,
    delta_y_mm: float,
    delta_z_mm: float = 0.0,
    group_array: bool = False,
) -> dict[str, Any]:
    """
    Create a linear array of an element by repeating it at regular intervals.

    Args:
        element_id: Source element to array.
        count: Total number of instances including the original.
        delta_x_mm: X spacing between instances (mm).
        delta_y_mm: Y spacing between instances (mm).
        delta_z_mm: Z spacing between instances (mm, default 0).
        group_array: Whether to group the array result (default False).

    Returns:
        {success: bool, new_element_ids: [str], message: str}.
    """
    return await _delegate(config, "array_element_linear", {
        "element_id": element_id,
        "count": count,
        "delta_x_mm": delta_x_mm,
        "delta_y_mm": delta_y_mm,
        "delta_z_mm": delta_z_mm,
        "group_array": group_array,
    })


@tool
async def array_element_radial(
    config: RunnableConfig,
    element_id: str,
    count: int,
    centre_x_mm: float,
    centre_y_mm: float,
    total_angle_degrees: float = 360.0,
    group_array: bool = False,
) -> dict[str, Any]:
    """
    Create a radial (circular) array of an element around a centre point.

    Args:
        element_id: Source element to array.
        count: Total number of instances including the original.
        centre_x_mm: X coordinate of the rotation centre (mm).
        centre_y_mm: Y coordinate of the rotation centre (mm).
        total_angle_degrees: Total angular span of the array in degrees (default 360 = full circle).
        group_array: Whether to group the array result (default False).

    Returns:
        {success: bool, new_element_ids: [str], message: str}.
    """
    return await _delegate(config, "array_element_radial", {
        "element_id": element_id,
        "count": count,
        "centre_x_mm": centre_x_mm,
        "centre_y_mm": centre_y_mm,
        "total_angle_degrees": total_angle_degrees,
        "group_array": group_array,
    })


@tool
async def join_geometry(
    config: RunnableConfig,
    element_id_a: str,
    element_id_b: str,
) -> dict[str, Any]:
    """
    Join the geometry of two overlapping elements so Revit computes their
    boolean intersection (e.g. wall and column, wall and beam).

    Args:
        element_id_a: First element (e.g. a wall).
        element_id_b: Second element (e.g. a column or beam overlapping the first).

    Returns:
        {success: bool, message: str}.
    """
    return await _delegate(config, "join_geometry", {
        "element_id_a": element_id_a,
        "element_id_b": element_id_b,
    })


@tool
async def unjoin_geometry(
    config: RunnableConfig,
    element_id_a: str,
    element_id_b: str,
) -> dict[str, Any]:
    """
    Remove the geometry join between two previously joined elements.

    Args:
        element_id_a: First element.
        element_id_b: Second element.

    Returns:
        {success: bool, message: str}.
    """
    return await _delegate(config, "unjoin_geometry", {
        "element_id_a": element_id_a,
        "element_id_b": element_id_b,
    })


# DISABLED – too complex for plugin side
@tool
async def split_element(
    config: RunnableConfig,
    element_id: str,
    split_point_x_mm: float,
    split_point_y_mm: float,
    split_point_z_mm: float = 0.0,
    delete_segment: str | None = None,
) -> dict[str, Any]:
    """
    Split a wall, line, or beam at a specified point into two separate elements.

    Args:
        element_id: Element to split (wall, model line, structural framing).
        split_point_x_mm: X coordinate of the split point (mm).
        split_point_y_mm: Y coordinate of the split point (mm).
        split_point_z_mm: Z coordinate of the split point (mm, default 0).
        delete_segment: Optional – after splitting, delete one segment: "first", "second", or None.

    Returns:
        {success: bool, segment_ids: [str, str], message: str}.
    """
    return await _delegate(config, "split_element", {
        "element_id": element_id,
        "split_point_x_mm": split_point_x_mm,
        "split_point_y_mm": split_point_y_mm,
        "split_point_z_mm": split_point_z_mm,
        "delete_segment": delete_segment,
    })


# DISABLED – too complex for plugin side
@tool
async def align_elements(
    config: RunnableConfig,
    reference_element_id: str,
    element_ids_to_align: list[str],
    alignment_type: str,
    prefer_closest: bool = True,
) -> dict[str, Any]:
    """
    Align one or more elements to a reference element's face or axis.
    Equivalent to the Revit Align command.

    Args:
        reference_element_id: Element whose face/axis is used as the alignment target.
        element_ids_to_align: List of element IDs to align to the reference.
        alignment_type: Which reference geometry to use –
            "left_face", "right_face", "top_face", "bottom_face",
            "front_face", "back_face", "centre_x", "centre_y", "centre_z".
        prefer_closest: When multiple faces qualify, use the closest one (default True).

    Returns:
        {success: bool, aligned_count: int, message: str}.
    """
    return await _delegate(config, "align_elements", {
        "reference_element_id": reference_element_id,
        "element_ids_to_align": element_ids_to_align,
        "alignment_type": alignment_type,
        "prefer_closest": prefer_closest,
    })


@tool
async def place_component_in_room(
    config: RunnableConfig,
    room_id: str,
    family_name: str,
    type_name: str,
    offset_from_centre_x_mm: float = 0.0,
    offset_from_centre_y_mm: float = 0.0,
    rotation_degrees: float = 0.0,
) -> dict[str, Any]:
    """
    Place a family instance (furniture, equipment, etc.) inside a room, automatically
    snapping to the room's centre point plus an optional offset.
    Use list_element_types() to find valid family/type names.

    Args:
        room_id: Element ID of the target room.
        family_name: Family name to place (e.g. "Desk").
        type_name: Type name (e.g. "60\" x 30\"").
        offset_from_centre_x_mm: X offset from the room centre (mm, default 0).
        offset_from_centre_y_mm: Y offset from the room centre (mm, default 0).
        rotation_degrees: Rotation about Z axis (default 0).

    Returns:
        {success: bool, element_id: str, placed_at: {x, y, z}, message: str}.
    """
    return await _delegate(config, "place_component_in_room", {
        "room_id": room_id,
        "family_name": family_name,
        "type_name": type_name,
        "offset_from_centre_x_mm": offset_from_centre_x_mm,
        "offset_from_centre_y_mm": offset_from_centre_y_mm,
        "rotation_degrees": rotation_degrees,
    })


@tool
async def load_family_from_file(
    config: RunnableConfig,
    file_path: str,
    overwrite_existing: bool = False,
) -> dict[str, Any]:
    """
    Load a Revit family (.rfa) from a local or network file path into the active model.
    Note: Loading from Autodesk's online cloud library is not supported via the Revit API;
    use this tool with a path to a locally saved .rfa file instead.

    Args:
        file_path: Full path to the .rfa file (e.g. "C:\\Families\\Desk.rfa").
        overwrite_existing: If True, overwrite a family with the same name that is
                            already loaded (default False).

    Returns:
        {success: bool, family_name: str, types_loaded: [str], message: str}.
    """
    return await _delegate(config, "load_family_from_file", {
        "file_path": file_path,
        "overwrite_existing": overwrite_existing,
    })
