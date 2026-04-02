"""Collects all Revit LangChain tools into a single importable list."""
from __future__ import annotations

from langchain_core.tools import BaseTool

# ── Core element queries ───────────────────────────────────────────────────────
from app.tools.elements import (
    find_elements_by_parameter_value,
    get_element_bounding_box,
    get_element_by_id,
    get_element_host,
    get_element_location,
    get_elements_by_category,
    get_elements_by_level,
    get_elements_in_bounding_box,
    get_elements_in_room,
    get_elements_in_view,
    get_hosted_elements,
    get_selected_elements,
    search_elements,
)

# ── Families & types ───────────────────────────────────────────────────────────
from app.tools.families_types import (
    change_element_type,
    get_family_info,
    get_type_properties,
    list_element_types,
    list_loaded_families,
    set_type_parameter,
)

# ── Parameters ─────────────────────────────────────────────────────────────────
from app.tools.parameters import (
    add_global_parameter,
    # add_project_parameter,  # DISABLED – too complex for plugin side
    bulk_set_parameter,
    get_element_parameters,
    list_project_parameters,
    list_shared_parameters,
    set_element_parameter,
)

# ── Structural ─────────────────────────────────────────────────────────────────
from app.tools.structural import (
    add_isolated_foundation,
    add_wall_foundation,
    get_analytical_model,
    list_rebar,
    list_structural_columns,
    list_structural_foundations,
    list_structural_framing,
)

# ── Views ──────────────────────────────────────────────────────────────────────
from app.tools.views import (
    get_active_view,
    hide_category_in_view,
    hide_elements_in_view,
    isolate_category_in_view,
    isolate_elements_in_view,
    list_views,
    set_view_display_settings,
    tab_open_views,
    tile_open_views,
    unhide_elements_in_view,
    create_section_view,
)

# ── Sheets & view management ───────────────────────────────────────────────────
from app.tools.sheets import (
    add_schedule_to_sheet,
    add_view_to_sheet,
    apply_view_template,
    create_drafting_view,
    create_schedule_view,
    create_sheet,
    get_sheet_views,
    list_sheets,
    list_view_filters,
    list_view_templates,
    set_active_view,
    set_view_property,
)

# ── Levels & grids ─────────────────────────────────────────────────────────────
from app.tools.levels import create_grid, create_level, list_grids, list_levels

# ── Rooms & areas ──────────────────────────────────────────────────────────────
from app.tools.rooms_areas import (
    get_areas_in_plan,
    get_room_adjacency,
    get_room_boundaries,
    get_room_detail,
    list_area_plans,
)

# ── Model health & summary ─────────────────────────────────────────────────────
from app.tools.model_info import get_model_info, get_rooms_summary, list_warnings

# ── MEP ────────────────────────────────────────────────────────────────────────
from app.tools.mep import (
    get_electrical_system_info,
    get_hvac_system_info,
    get_plumbing_system_info,
    list_air_terminals,
    list_circuits,
    list_ducts,
    list_electrical_equipment,
    list_electrical_systems,
    list_hvac_systems,
    list_lighting_fixtures,
    list_mechanical_equipment,
    list_pipes,
    list_plumbing_fixtures,
    list_plumbing_systems,
)

# ── Annotations ────────────────────────────────────────────────────────────────
from app.tools.annotations import (
    add_aligned_dimension,
    # add_angular_dimension,    # DISABLED – too complex for plugin side
    # add_arc_length_dimension, # DISABLED – too complex for plugin side
    # add_diameter_dimension,   # DISABLED – too complex for plugin side
    # add_linear_dimension,     # DISABLED – too complex for plugin side
    # add_radial_dimension,     # DISABLED – too complex for plugin side
    # add_spot_coordinate,      # DISABLED – too complex for plugin side
    # add_spot_elevation,       # DISABLED – too complex for plugin side
    list_dimensions,
    list_keynotes,
    list_revision_clouds,
    list_tags,
    list_text_notes,
    tag_by_category,
    tag_element,
)

# ── Materials ──────────────────────────────────────────────────────────────────
from app.tools.materials import (
    get_element_materials,
    get_material_info,
    list_materials,
    set_element_material,
)

# ── Schedules ──────────────────────────────────────────────────────────────────
from app.tools.schedules import get_schedule_data, get_schedule_fields, list_schedules

# ── Worksets & phases ──────────────────────────────────────────────────────────
from app.tools.worksets_phases import (
    # create_phase,         # DISABLED – too complex for plugin side
    get_element_phase_info,
    get_element_workset,
    list_phases,
    list_worksets,
    set_element_phase_created,
    set_element_workset,
)

# ── Links & groups ─────────────────────────────────────────────────────────────
from app.tools.links_groups import (
    get_group_instances,
    list_cad_links,
    list_design_options,
    list_groups,
    list_rvt_links,
)

# ── Site ───────────────────────────────────────────────────────────────────────
from app.tools.site import get_project_location, get_toposurface_info, list_site_components

# ── Revisions ──────────────────────────────────────────────────────────────────
from app.tools.revisions import (
    get_revision_clouds_for_element,
    get_sheet_revisions,
    list_revisions,
)

# ── Modify / write operations ──────────────────────────────────────────────────
from app.tools.modify import (
    add_door,
    add_window,
    # align_elements,       # DISABLED – too complex for plugin side
    array_element_linear,
    array_element_radial,
    copy_element,
    create_floor,
    create_room,
    create_wall,
    delete_element,
    join_geometry,
    load_family_from_file,
    mirror_element,
    move_element,
    offset_element,
    pin_element,
    place_component_in_room,
    place_family_instance,
    replace_element,
    rotate_element,
    # scale_element,        # DISABLED – too complex for plugin side
    # split_element,        # DISABLED – too complex for plugin side
    # trim_extend_elements, # DISABLED – too complex for plugin side
    unpin_element,
    unjoin_geometry,
)

# ── Drafting ──────────────────────────────────────────────────────────────────
from app.tools.drafting import (
    # add_color_fill_legend, # DISABLED – too complex for plugin side
    add_detail_line,
    # add_filled_region,     # DISABLED – too complex for plugin side
    # add_masking_region,    # DISABLED – too complex for plugin side
    add_model_line,
    add_model_text,
    add_symbol,
    check_spelling,
    create_text_note,
    edit_text_note,
    find_replace_text,
)

# ── Selection ─────────────────────────────────────────────────────────────────
from app.tools.selection import (
    filter_selection_by_category,
    invert_selection,
    select_all_of_same_type,
    select_connected_elements,
    select_elements_by_category,
    select_elements_by_parameter_filter,
    select_elements_by_type,
    select_elements_in_room,
    select_elements_on_level,
    select_exterior_walls,
)

# ── Export & output ───────────────────────────────────────────────────────────
from app.tools.export import (
    export_to_dwg,
    export_to_ifc,
    export_to_nwc,
    export_to_pdf,
    print_sheets,
    save_model,
    save_model_as,
    synchronize_with_central,
)

# ── Full tool list (kept for reference / testing) ────────────────────────────
ALL_REVIT_TOOLS: list[BaseTool] = [
    # ── Element queries ──────────────────────────────────────────────────────
    get_selected_elements,
    get_elements_by_category,
    get_element_by_id,
    get_elements_in_view,
    get_elements_by_level,
    get_elements_in_room,
    search_elements,
    find_elements_by_parameter_value,
    get_element_location,
    get_element_bounding_box,
    get_element_host,
    get_hosted_elements,
    get_elements_in_bounding_box,
    # ── Parameters ───────────────────────────────────────────────────────────
    get_element_parameters,
    set_element_parameter,
    bulk_set_parameter,
    list_project_parameters,
    list_shared_parameters,
    # add_project_parameter,  # DISABLED
    add_global_parameter,
    # ── Families & types ─────────────────────────────────────────────────────
    list_element_types,
    get_type_properties,
    set_type_parameter,
    list_loaded_families,
    get_family_info,
    change_element_type,
    load_family_from_file,
    # ── Views ────────────────────────────────────────────────────────────────
    list_views,
    get_active_view,
    hide_elements_in_view,
    hide_category_in_view,
    isolate_elements_in_view,
    isolate_category_in_view,
    unhide_elements_in_view,
    set_view_display_settings,
    create_section_view,
    tile_open_views,
    tab_open_views,
    # ── Sheets & view management ─────────────────────────────────────────────
    list_sheets,
    get_sheet_views,
    set_view_property,
    list_view_filters,
    list_view_templates,
    apply_view_template,
    set_active_view,
    create_sheet,
    add_view_to_sheet,
    add_schedule_to_sheet,
    create_drafting_view,
    create_schedule_view,
    # ── Levels & grids ───────────────────────────────────────────────────────
    list_levels,
    list_grids,
    create_level,
    create_grid,
    # ── Rooms & areas ────────────────────────────────────────────────────────
    get_rooms_summary,
    get_room_detail,
    get_room_boundaries,
    get_room_adjacency,
    list_area_plans,
    get_areas_in_plan,
    # ── Model health ─────────────────────────────────────────────────────────
    get_model_info,
    list_warnings,
    # ── Structural ───────────────────────────────────────────────────────────
    list_structural_columns,
    list_structural_framing,
    list_structural_foundations,
    get_analytical_model,
    list_rebar,
    add_wall_foundation,
    add_isolated_foundation,
    # ── MEP – Mechanical ─────────────────────────────────────────────────────
    list_hvac_systems,
    get_hvac_system_info,
    list_ducts,
    list_air_terminals,
    list_mechanical_equipment,
    # ── MEP – Electrical ─────────────────────────────────────────────────────
    list_electrical_systems,
    get_electrical_system_info,
    list_electrical_equipment,
    list_lighting_fixtures,
    list_circuits,
    # ── MEP – Plumbing ───────────────────────────────────────────────────────
    list_plumbing_systems,
    get_plumbing_system_info,
    list_pipes,
    list_plumbing_fixtures,
    # ── Annotations ──────────────────────────────────────────────────────────
    list_dimensions,
    list_text_notes,
    list_tags,
    list_keynotes,
    list_revision_clouds,
    tag_element,
    tag_by_category,
    add_aligned_dimension,
    # add_linear_dimension,     # DISABLED
    # add_radial_dimension,     # DISABLED
    # add_diameter_dimension,   # DISABLED
    # add_angular_dimension,    # DISABLED
    # add_arc_length_dimension, # DISABLED
    # add_spot_elevation,       # DISABLED
    # add_spot_coordinate,      # DISABLED
    # ── Drafting ─────────────────────────────────────────────────────────────
    add_model_text,
    add_model_line,
    add_detail_line,
    create_text_note,
    edit_text_note,
    find_replace_text,
    check_spelling,
    # add_masking_region,      # DISABLED
    # add_filled_region,        # DISABLED
    add_symbol,
    # add_color_fill_legend,    # DISABLED
    # ── Materials ────────────────────────────────────────────────────────────
    list_materials,
    get_material_info,
    get_element_materials,
    set_element_material,
    # ── Schedules ────────────────────────────────────────────────────────────
    list_schedules,
    get_schedule_data,
    get_schedule_fields,
    # ── Worksets & phases ────────────────────────────────────────────────────
    list_worksets,
    get_element_workset,
    set_element_workset,
    list_phases,
    get_element_phase_info,
    # create_phase,         # DISABLED
    set_element_phase_created,
    # ── Links & groups ───────────────────────────────────────────────────────
    list_rvt_links,
    list_cad_links,
    list_groups,
    get_group_instances,
    list_design_options,
    # ── Site ─────────────────────────────────────────────────────────────────
    get_toposurface_info,
    list_site_components,
    get_project_location,
    # ── Revisions ────────────────────────────────────────────────────────────
    list_revisions,
    get_sheet_revisions,
    get_revision_clouds_for_element,
    # ── Modify / write ───────────────────────────────────────────────────────
    move_element,
    rotate_element,
    copy_element,
    mirror_element,
    delete_element,
    create_wall,
    create_floor,
    place_family_instance,
    create_room,
    pin_element,
    unpin_element,
    replace_element,
    add_door,
    add_window,
    # trim_extend_elements, # DISABLED
    offset_element,
    # scale_element,        # DISABLED
    array_element_linear,
    array_element_radial,
    join_geometry,
    unjoin_geometry,
    # split_element,        # DISABLED
    # align_elements,       # DISABLED
    place_component_in_room,
    # ── Advanced selection ───────────────────────────────────────────────────
    select_elements_by_category,
    select_elements_by_parameter_filter,
    select_elements_by_type,
    select_exterior_walls,
    select_elements_on_level,
    select_elements_in_room,
    filter_selection_by_category,
    invert_selection,
    select_all_of_same_type,
    select_connected_elements,
    # ── Export & output ──────────────────────────────────────────────────────
    export_to_pdf,
    export_to_dwg,
    export_to_ifc,
    export_to_nwc,
    print_sheets,
    save_model,
    save_model_as,
    synchronize_with_central,
]

# ── Core tools always sent to the LLM (~33 tools) ────────────────────────────
# These cover the most common operations and keep the baseline well under the
# OpenAI 128-tool limit, leaving headroom for category expansions.
CORE_TOOLS: list[BaseTool] = [
    # Element queries
    get_selected_elements,
    get_elements_by_category,
    get_element_by_id,
    search_elements,
    get_elements_in_view,
    get_elements_by_level,
    get_elements_in_room,
    get_element_location,
    # Parameters
    get_element_parameters,
    set_element_parameter,
    # Families & types
    list_element_types,
    get_type_properties,
    change_element_type,
    list_loaded_families,
    get_family_info,
    # Views
    list_views,
    get_active_view,
    set_active_view,
    # Sheets / levels
    list_sheets,
    list_levels,
    # Model info
    get_model_info,
    get_rooms_summary,
    list_warnings,
    # Modify basics
    move_element,
    rotate_element,
    copy_element,
    delete_element,
    create_wall,
    place_family_instance,
    create_room,
    add_door,
    add_window,
    # Persist
    save_model,
]

# ── Per-category tool pools ───────────────────────────────────────────────────
_CATEGORY_TOOLS: dict[str, list[BaseTool]] = {
    "element_details": [
        find_elements_by_parameter_value,
        get_element_bounding_box,
        get_element_host,
        get_hosted_elements,
        get_elements_in_bounding_box,
    ],
    "parameters": [
        bulk_set_parameter,
        list_project_parameters,
        list_shared_parameters,
        # add_project_parameter,  # DISABLED
        add_global_parameter,
    ],
    "families": [
        set_type_parameter,
        load_family_from_file,
    ],
    "views": [
        hide_elements_in_view,
        hide_category_in_view,
        isolate_elements_in_view,
        isolate_category_in_view,
        unhide_elements_in_view,
        set_view_display_settings,
        create_section_view,
        tile_open_views,
        tab_open_views,
    ],
    "sheets": [
        get_sheet_views,
        set_view_property,
        list_view_filters,
        list_view_templates,
        apply_view_template,
        create_sheet,
        add_view_to_sheet,
        add_schedule_to_sheet,
        create_drafting_view,
        create_schedule_view,
    ],
    "levels_grids": [
        list_grids,
        create_level,
        create_grid,
    ],
    "rooms_areas": [
        get_room_detail,
        get_room_boundaries,
        get_room_adjacency,
        list_area_plans,
        get_areas_in_plan,
    ],
    "structural": [
        list_structural_columns,
        list_structural_framing,
        list_structural_foundations,
        get_analytical_model,
        list_rebar,
        add_wall_foundation,
        add_isolated_foundation,
    ],
    "mep": [
        list_hvac_systems,
        get_hvac_system_info,
        list_ducts,
        list_air_terminals,
        list_mechanical_equipment,
        list_electrical_systems,
        get_electrical_system_info,
        list_electrical_equipment,
        list_lighting_fixtures,
        list_circuits,
        list_plumbing_systems,
        get_plumbing_system_info,
        list_pipes,
        list_plumbing_fixtures,
    ],
    "annotations": [
        list_dimensions,
        list_text_notes,
        list_tags,
        list_keynotes,
        list_revision_clouds,
        tag_element,
        tag_by_category,
        add_aligned_dimension,
        # add_linear_dimension,     # DISABLED
        # add_radial_dimension,     # DISABLED
        # add_diameter_dimension,   # DISABLED
        # add_angular_dimension,    # DISABLED
        # add_arc_length_dimension, # DISABLED
        # add_spot_elevation,       # DISABLED
        # add_spot_coordinate,      # DISABLED
    ],
    "drafting": [
        add_model_text,
        add_model_line,
        add_detail_line,
        create_text_note,
        edit_text_note,
        find_replace_text,
        check_spelling,
        # add_masking_region,    # DISABLED
        # add_filled_region,     # DISABLED
        add_symbol,
        # add_color_fill_legend, # DISABLED
    ],
    "materials": [
        list_materials,
        get_material_info,
        get_element_materials,
        set_element_material,
    ],
    "schedules": [
        list_schedules,
        get_schedule_data,
        get_schedule_fields,
    ],
    "worksets_phases": [
        list_worksets,
        get_element_workset,
        set_element_workset,
        list_phases,
        get_element_phase_info,
        # create_phase,         # DISABLED
        set_element_phase_created,
    ],
    "links_groups": [
        list_rvt_links,
        list_cad_links,
        list_groups,
        get_group_instances,
        list_design_options,
    ],
    "site": [
        get_toposurface_info,
        list_site_components,
        get_project_location,
    ],
    "revisions": [
        list_revisions,
        get_sheet_revisions,
        get_revision_clouds_for_element,
    ],
    "modify_advanced": [
        create_floor,
        mirror_element,
        pin_element,
        unpin_element,
        replace_element,
        # trim_extend_elements, # DISABLED
        offset_element,
        # scale_element,        # DISABLED
        array_element_linear,
        array_element_radial,
        join_geometry,
        unjoin_geometry,
        # split_element,        # DISABLED
        # align_elements,       # DISABLED
        place_component_in_room,
    ],
    "selection": [
        select_elements_by_category,
        select_elements_by_parameter_filter,
        select_elements_by_type,
        select_exterior_walls,
        select_elements_on_level,
        select_elements_in_room,
        filter_selection_by_category,
        invert_selection,
        select_all_of_same_type,
        select_connected_elements,
    ],
    "export": [
        export_to_pdf,
        export_to_dwg,
        export_to_ifc,
        export_to_nwc,
        print_sheets,
        save_model_as,
        synchronize_with_central,
    ],
}

# ── Keyword → category mapping ────────────────────────────────────────────────
_CATEGORY_KEYWORDS: dict[str, list[str]] = {
    "element_details": ["bounding box", "hosted", "host element", "elements in box"],
    "parameters": [
        "parameter", "param", "shared parameter", "project parameter", "global parameter",
        "bulk set", "add parameter",
    ],
    "families": ["load family", "family file", "set type parameter", "type parameter"],
    "views": [
        "view", "hide", "isolate", "visibility", "section view", "camera",
        "tile", "tab open", "display settings",
    ],
    "sheets": [
        "sheet", "drawing", "title block", "viewport", "view template", "view filter",
        "drafting view", "schedule view", "add to sheet",
    ],
    "levels_grids": ["level", "grid", "story", "floor level"],
    "rooms_areas": ["room", "area", "space", "boundary", "adjacen", "area plan"],
    "structural": [
        "structural", "column", "beam", "framing", "foundation", "rebar",
        "analytical", "wall foundation", "isolated foundation",
    ],
    "mep": [
        "mep", "mechanical", "electrical", "plumbing", "duct", "pipe",
        "hvac", "circuit", "wiring", "light", "air terminal", "equipment",
        "electrical system", "plumbing system", "hvac system",
    ],
    "annotations": [
        "dimension", "tag", "annotation", "keynote", "revision cloud",
        "text note", "spot elevation", "spot coordinate", "radial", "angular",
    ],
    "drafting": [
        "detail line", "model line", "model text", "drafting", "masking region",
        "filled region", "color fill", "spell", "find replace", "text note",
    ],
    "materials": ["material", "finish", "texture", "surface material"],
    "schedules": ["schedule", "quantity take-off", "count table"],
    "worksets_phases": ["workset", "phase", "phasing", "demolish", "new construction", "existing"],
    "links_groups": ["link", "rvt link", "cad link", "group", "design option"],
    "site": ["site", "topograph", "toposurface", "project location", "solar", "coordinate"],
    "revisions": ["revision", "revision cloud", "issue date"],
    "modify_advanced": [
        "floor", "trim", "extend", "offset", "scale element", "array",
        "join geometry", "split", "align", "mirror", "pin", "unpin", "replace element",
        "place component",
    ],
    "selection": [
        "select all", "select by", "filter selection", "exterior wall",
        "same type", "connected element", "invert selection",
    ],
    "export": [
        "export", "pdf", "dwg", "ifc", "naviswork", "nwc", "print sheet",
        "save as", "synchronize", "sync with central",
    ],
}

_MAX_TOOLS = 128


def select_tools(message: str) -> list[BaseTool]:
    """
    Return a tool subset tailored to *message*, always staying ≤ _MAX_TOOLS.

    Strategy:
    1. Start with CORE_TOOLS (the ~33 most universally needed tools).
    2. Scan the message for category keywords and append matching category
       pools in priority order (most specific first).
    3. Hard-cap the result at _MAX_TOOLS to satisfy the OpenAI API limit.
    """
    msg_lower = message.lower()
    selected: list[BaseTool] = list(CORE_TOOLS)
    seen: set[str] = {t.name for t in selected}

    for category, keywords in _CATEGORY_KEYWORDS.items():
        if any(kw in msg_lower for kw in keywords):
            for tool in _CATEGORY_TOOLS[category]:
                if tool.name not in seen:
                    if len(selected) >= _MAX_TOOLS:
                        break
                    selected.append(tool)
                    seen.add(tool.name)
            if len(selected) >= _MAX_TOOLS:
                break

    return selected


__all__ = ["ALL_REVIT_TOOLS", "CORE_TOOLS", "select_tools"]
