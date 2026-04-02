# Nova Tools Reference

All tools exposed by the Revit agent, grouped by module.

> **V1 total: 97 tools.** For the 68 new tools added in the second pass see [TOOLS_V2.md](TOOLS_V2.md).  
> **Grand total: 165 tools across 20 modules.**

---

## Annotations (`annotations.py`)

| Tool | Description | Arguments |
|------|-------------|-----------|
| `list_dimensions` | Return dimension annotations in a view. | `view_id` *(optional)* – Revit view element ID, defaults to active view; `limit` *(default 200)* – max number to return |
| `list_text_notes` | Return text note annotations in a view, with optional text content search. | `view_id` *(optional)*; `search` *(optional)* – substring filter on text content; `limit` *(default 200)* |
| `list_tags` | Return tag annotations in a view, optionally filtered by the category of the tagged element. | `view_id` *(optional)*; `category` *(optional)* – e.g. `"Rooms"`, `"Doors"`, `"Walls"`; `limit` *(default 300)* |
| `list_keynotes` | Return keynote annotations in a view, including keynote value and referenced elements. | `view_id` *(optional)*; `limit` *(default 200)* |
| `list_revision_clouds` | Return revision cloud elements, optionally filtered by view or revision sequence number. | `view_id` *(optional)*; `revision_sequence` *(optional)* – integer sequence number |
| `tag_element` | Place a tag annotation on an element in a view. | `element_id` – element to tag; `view_id` *(optional)*; `tag_family_name` *(optional)*; `leader` *(default false)* – add leader line |

---

## Elements (`elements.py`)

| Tool | Description | Arguments |
|------|-------------|-----------|
| `get_selected_elements` | Return the elements currently selected in the Revit UI. | *(none)* |
| `get_elements_by_category` | Return elements belonging to a category. | `category` – category name; `limit` *(default 50)* |
| `get_element_by_id` | Retrieve detailed information about a single element by its integer ID. | `element_id` |
| `get_elements_in_view` | Return elements visible in a specific view, optionally filtered by category. | `view_id` *(optional)*; `category` *(optional)*; `limit` *(default 100)* |
| `get_elements_by_level` | Return all elements associated with a given level, optionally filtered by category. | `level_name`; `category` *(optional)*; `limit` *(default 200)* |
| `get_elements_in_room` | Return elements spatially located inside a specific room. | `room_id`; `category` *(optional)* |
| `search_elements` | Full-text search across element names, type names, and parameter values. | `query`; `categories` *(optional)* – list of category names; `limit` *(default 50)* |
| `find_elements_by_parameter_value` | Find all elements where a specific parameter equals or contains a given value. | `parameter_name`; `value`; `category` *(optional)*; `limit` *(default 100)* |
| `get_element_location` | Return the geometric location (point or start/end) of an element in mm. | `element_id` |
| `get_element_bounding_box` | Return the axis-aligned 3-D bounding box of an element in project coordinates (mm). | `element_id` |
| `get_element_host` | Return the host element of a hosted element (e.g. wall hosting a door). | `element_id` |
| `get_hosted_elements` | Return all elements hosted by the given element. | `host_element_id`; `category` *(optional)* |
| `get_elements_in_bounding_box` | Return elements whose bounding box intersects a given 3-D region (mm). | `min_x`, `min_y`, `min_z`, `max_x`, `max_y`, `max_z` – region corners in mm; `category` *(optional)* |

---

## Families & Types (`families_types.py`)

| Tool | Description | Arguments |
|------|-------------|-----------|
| `list_element_types` | Return all element types (family symbols) available for a given category. | `category`; `family_name` *(optional)* – filter by family |
| `get_type_properties` | Return all type-level parameters for a family type (symbol). | `type_id` |
| `set_type_parameter` | Set a writable type parameter on a family symbol. Affects ALL existing and future instances. | `type_id`; `parameter_name`; `value` |
| `list_loaded_families` | Return all families loaded in the project, optionally filtered by category. | `category` *(optional)* |
| `get_family_info` | Return detailed information about a loaded family including all its types and type-level parameters. | `family_name` |
| `change_element_type` | Change an existing element to a different type within the same or compatible family. | `element_id`; `new_type_id` |

---

## Levels & Grids (`levels.py`)

| Tool | Description | Arguments |
|------|-------------|-----------|
| `list_levels` | Return all levels defined in the active Revit document. | *(none)* |
| `list_grids` | Return all grid lines in the active Revit document. | *(none)* |

---

## Links & Groups (`links_groups.py`)

| Tool | Description | Arguments |
|------|-------------|-----------|
| `list_rvt_links` | Return all Revit linked file (RVT) references in the model. | *(none)* |
| `list_cad_links` | Return all imported or linked CAD files (DWG, DXF, DGN, etc.). | *(none)* |
| `list_groups` | Return all group types and their instance counts. | `group_type` *(optional)* – `"Model"` or `"Detail"` |
| `get_group_instances` | Return all placed instances of a named group with their locations and host levels. | `group_name` |
| `list_design_options` | Return all design option sets and their options. | *(none)* |

---

## Materials (`materials.py`)

| Tool | Description | Arguments |
|------|-------------|-----------|
| `list_materials` | Return all materials defined in the project, with optional name filter. | `search` *(optional)* – name substring filter |
| `get_material_info` | Return detailed properties of a material including render, physical, and thermal properties. | `material_id` |
| `get_element_materials` | Return the materials (and paint overrides) applied to an element, broken down by compound layer. | `element_id` |
| `set_element_material` | Assign a material to an element or a specific compound layer. | `element_id`; `material_name`; `layer_index` *(default 0)* |

---

## MEP (`mep.py`)

### Mechanical

| Tool | Description | Arguments |
|------|-------------|-----------|
| `list_hvac_systems` | Return all mechanical (HVAC) systems defined in the model. | *(none)* |
| `get_hvac_system_info` | Return detailed information about a specific HVAC system. | `system_id` |
| `list_ducts` | Return duct segments with size, system, insulation, and flow values. | `system_name` *(optional)*; `level_name` *(optional)*; `limit` *(default 200)* |
| `list_air_terminals` | Return air terminal elements (diffusers, grilles, registers) with flow assignments. | `system_name` *(optional)*; `level_name` *(optional)*; `limit` *(default 200)* |
| `list_mechanical_equipment` | Return mechanical equipment (AHUs, VAVs, fans, chillers, etc.) with system connections. | `level_name` *(optional)*; `limit` *(default 100)* |

### Electrical

| Tool | Description | Arguments |
|------|-------------|-----------|
| `list_electrical_systems` | Return all electrical systems (power, data circuits, etc.) defined in the model. | *(none)* |
| `get_electrical_system_info` | Return detailed info for an electrical circuit including connected equipment, load calculations, panel assignments, and wire sizing. | `system_id` |
| `list_electrical_equipment` | Return electrical equipment (distribution boards, panels, switchgear, transformers, UPS). | `level_name` *(optional)*; `limit` *(default 100)* |
| `list_lighting_fixtures` | Return lighting fixtures with circuit assignment, load, and location. | `level_name` *(optional)*; `circuit_name` *(optional)*; `limit` *(default 300)* |
| `list_circuits` | Return circuits, optionally filtered to those from a specific panel. | `panel_id` *(optional)* |

### Plumbing

| Tool | Description | Arguments |
|------|-------------|-----------|
| `list_plumbing_systems` | Return all plumbing systems (DHW, cold water, sanitary, fire protection, etc.). | *(none)* |
| `get_plumbing_system_info` | Return detailed info for a plumbing system including connected fixtures, pipes, and flow values. | `system_id` |
| `list_pipes` | Return pipe segments with size, material, system, and flow data. | `system_name` *(optional)*; `level_name` *(optional)*; `limit` *(default 300)* |
| `list_plumbing_fixtures` | Return plumbing fixtures (sinks, toilets, showers, etc.) with system connections and fixture unit values. | `level_name` *(optional)*; `system_name` *(optional)*; `limit` *(default 200)* |

---

## Model Info (`model_info.py`)

| Tool | Description | Arguments |
|------|-------------|-----------|
| `get_model_info` | Return high-level information about the active Revit document (title, path, version, element count, last saved). | *(none)* |
| `list_warnings` | Return model integrity warnings from the active Revit document. | *(none)* |
| `get_rooms_summary` | Return a summary of all rooms/spaces in the model (id, name, number, level, area, occupancy). | *(none)* |

---

## Modify (`modify.py`)

| Tool | Description | Arguments |
|------|-------------|-----------|
| `move_element` | Move an element by a translation vector (delta in mm). | `element_id`; `delta_x_mm`; `delta_y_mm`; `delta_z_mm` *(default 0.0)* |
| `rotate_element` | Rotate an element around a specified axis through its own origin. | `element_id`; `angle_degrees`; `axis` *(default `"Z"`)* |
| `copy_element` | Copy an element and place the copy at an offset from the original. | `element_id`; `delta_x_mm`; `delta_y_mm`; `delta_z_mm` *(default 0.0)* |
| `mirror_element` | Mirror an element across a plane parallel to a world axis. | `element_id`; `mirror_axis` – `"X"`, `"Y"`, or `"Z"`; `axis_coordinate_mm` |
| `delete_element` | Delete an element from the model. Confirm with the user before calling. | `element_id` |
| `create_wall` | Create a straight wall between two XY points at a given level. | `start_x_mm`, `start_y_mm`, `end_x_mm`, `end_y_mm`; `level_name`; `wall_type_name`; `height_mm`; `base_offset_mm` *(default 0.0)* |
| `create_floor` | Create a floor from a closed boundary polygon. | `boundary_points` – list of `{x, y}` points in mm; `level_name`; `floor_type_name`; `offset_mm` *(default 0.0)* |
| `place_family_instance` | Place a family instance at given coordinates. | `family_name`; `type_name`; `x_mm`, `y_mm`, `z_mm`; `level_name`; `rotation_degrees` *(default 0.0)* |
| `create_room` | Place a room at the given XY point on a level. | `x_mm`, `y_mm`; `level_name`; `name` *(optional)*; `number` *(optional)* |
| `pin_element` | Pin an element to prevent accidental moves or deletions. | `element_id` |
| `unpin_element` | Unpin a previously pinned element, allowing it to be moved or deleted. | `element_id` |

---

## Parameters (`parameters.py`)

| Tool | Description | Arguments |
|------|-------------|-----------|
| `get_element_parameters` | Return all user-visible parameters and their values for a given element. | `element_id` |
| `set_element_parameter` | Set a writable parameter on a Revit element. | `element_id`; `parameter_name`; `value` |
| `bulk_set_parameter` | Set the same parameter to the same value on multiple elements at once. | `element_ids` – list of element IDs; `parameter_name`; `value` |
| `list_project_parameters` | Return all project parameters defined in the active Revit document. | *(none)* |
| `list_shared_parameters` | Return all shared parameters currently loaded in the project. | *(none)* |

---

## Revisions (`revisions.py`)

| Tool | Description | Arguments |
|------|-------------|-----------|
| `list_revisions` | Return all project revisions defined in the revision table. | *(none)* |
| `get_sheet_revisions` | Return all revisions that appear in the revision block of a specific sheet. | `sheet_id` |
| `get_revision_clouds_for_element` | Return revision clouds that reference or enclose a specific element. | `element_id` |

---

## Rooms & Areas (`rooms_areas.py`)

| Tool | Description | Arguments |
|------|-------------|-----------|
| `get_room_detail` | Return full detail for a specific room, looked up by ID, name, or number. | `room_id` *(optional)*; `name` *(optional)*; `number` *(optional)* |
| `get_room_boundaries` | Return the boundary segments of a room, including hosting elements for each segment. | `room_id` |
| `get_room_adjacency` | Return rooms directly adjacent to the given room (sharing a boundary segment). | `room_id` |
| `list_area_plans` | Return all area plans in the project. | *(none)* |
| `get_areas_in_plan` | Return all area elements placed in a specific area plan view. | `area_plan_id` |

---

## Schedules (`schedules.py`)

| Tool | Description | Arguments |
|------|-------------|-----------|
| `list_schedules` | Return all schedules (and key schedules) defined in the project. | *(none)* |
| `get_schedule_data` | Return the tabular data from a schedule as a list of rows. Most powerful data-extraction tool. | `schedule_id`; `limit` *(default 500)* |
| `get_schedule_fields` | Return the field definitions (columns) of a schedule view. | `schedule_id` |

---

## Sheets & Views (`sheets.py`)

| Tool | Description | Arguments |
|------|-------------|-----------|
| `list_sheets` | Return all sheets, optionally filtered by discipline or name search. | `discipline` *(optional)*; `search` *(optional)* |
| `get_sheet_views` | Return all viewports placed on a sheet. | `sheet_id` |
| `set_view_property` | Set a property on a view (scale, detail level, visual style, discipline, etc.). | `view_id`; `property_name`; `value` |
| `list_view_filters` | Return all view filters applied to a view with their visibility/override settings. | `view_id` |
| `list_view_templates` | Return all view templates defined in the project. | *(none)* |
| `apply_view_template` | Apply a view template to a view. All controlled properties will be overwritten. | `view_id`; `template_id` |
| `set_active_view` | Switch the Revit UI to display the specified view as the active view. | `view_id` |

---

## Site (`site.py`)

| Tool | Description | Arguments |
|------|-------------|-----------|
| `get_toposurface_info` | Return topographic surface elements in the model. | *(none)* |
| `list_site_components` | Return site component elements (planting, site furniture, parking, etc.). | `limit` *(default 200)* |
| `get_project_location` | Return the project's geographic location, coordinate system settings, and true north offset. | *(none)* |

---

## Structural (`structural.py`)

| Tool | Description | Arguments |
|------|-------------|-----------|
| `list_structural_columns` | Return structural columns in the model. | `level_name` *(optional)*; `limit` *(default 200)* |
| `list_structural_framing` | Return structural framing members: beams, braces, trusses, and girders. | `framing_type` *(optional)* – `"Beam"`, `"Brace"`, `"Truss"`, `"Girder"`; `level_name` *(optional)*; `limit` *(default 200)* |
| `list_structural_foundations` | Return structural foundation elements (isolated footings, wall footings, foundation slabs). | `foundation_type` *(optional)* – `"Isolated"`, `"Wall"`, `"Slab"`; `limit` *(default 200)* |
| `get_analytical_model` | Return the analytical model properties for a structural element (column, beam, brace, wall, floor). | `element_id` |
| `list_rebar` | Return rebar elements, optionally filtered to those hosted within a specific concrete element. | `host_element_id` *(optional)*; `limit` *(default 500)* |

---

## Views (`views.py`)

| Tool | Description | Arguments |
|------|-------------|-----------|
| `list_views` | List views in the active Revit document, optionally filtered by type. | `view_type` *(optional)* – `"FloorPlan"`, `"Section"`, `"Elevation"`, `"3D"`, `"Sheet"`, etc. |
| `get_active_view` | Return information about the currently active view in the Revit session. | *(none)* |

---

## Worksets & Phases (`worksets_phases.py`)

| Tool | Description | Arguments |
|------|-------------|-----------|
| `list_worksets` | Return all user-created worksets in the workshared model. Returns empty list for non-workshared models. | *(none)* |
| `get_element_workset` | Return the workset that the given element belongs to. | `element_id` |
| `set_element_workset` | Move an element to a different workset. Use `list_worksets` first to discover available names. | `element_id`; `workset_name` |
| `list_phases` | Return all construction phases defined in the project, in sequence order. | *(none)* |
| `get_element_phase_info` | Return the phase created and phase demolished values for an element. | `element_id` |
| `create_phase` | Create a new construction phase, optionally inserted after an existing one. | `phase_name`; `insert_after_phase` *(optional)* |
| `set_element_phase_created` | Move elements into a different Phase Created; optionally set Phase Demolished. | `element_ids`; `phase_created`; `phase_demolished` *(optional)* |

---

## Annotations – Extended (`annotations.py`)

New annotation tools added in V2:

| Tool | Description | Arguments |
|------|-------------|-----------|
| `tag_by_category` | Tag all elements of a category in a view at once (Tag All Not Tagged). | `category`; `view_id` *(optional)*; `tag_family_name` *(optional)*; `leader` *(default false)*; `skip_already_tagged` *(default true)* |
| `add_aligned_dimension` | Aligned dimension across 2+ element faces. | `reference_element_ids`; `dimension_line_x_mm`; `dimension_line_y_mm`; `view_id` *(optional)*; `dimension_type_name` *(optional)* |
| `add_linear_dimension` | Linear (H/V/aligned) dimension between two explicit points. | `start/end_x/y_mm`; `line_position_x/y_mm`; `orientation` *(default "horizontal")*; `view_id` *(optional)* |
| `add_radial_dimension` | Radial dimension (radius) on an arc element. | `arc_element_id`; `leader_end_x/y_mm`; `view_id` *(optional)* |
| `add_diameter_dimension` | Diameter dimension (⌀) on a circular element. | `arc_element_id`; `leader_end_x/y_mm`; `view_id` *(optional)* |
| `add_angular_dimension` | Angle dimension between two linear elements. | `element_id_a`; `element_id_b`; `arc_position_x/y_mm`; `view_id` *(optional)* |
| `add_arc_length_dimension` | Arc length dimension on a curved element. | `arc_element_id`; `leader_end_x/y_mm`; `view_id` *(optional)* |
| `add_spot_elevation` | Spot elevation annotation on a surface point. | `element_id`; `leader_origin_x/y_mm`; `leader_end_x/y_mm`; `view_id` *(optional)* |
| `add_spot_coordinate` | Spot coordinate (N/E) annotation on a surface point. | `element_id`; `leader_origin_x/y_mm`; `leader_end_x/y_mm`; `view_id` *(optional)* |

---

## Levels & Grids – Extended (`levels.py`)

| Tool | Description | Arguments |
|------|-------------|-----------|
| `create_level` | Create a new level at a given elevation, auto-generating a floor plan view if requested. | `elevation_mm`; `name` *(optional)*; `create_floor_plan` *(default true)* |
| `create_grid` | Create a straight grid line between two XY points with an optional label. | `start_x/y_mm`; `end_x/y_mm`; `name` *(optional)*; `bubble_end` *("end" default)* |

---

## Modify – Extended (`modify.py`)

New modify tools added in V2:

| Tool | Description | Arguments |
|------|-------------|-----------|
| `replace_element` | Replace element with a different family/type while preserving location and matching parameters. | `element_id`; `new_family_name`; `new_type_name` |
| `add_door` | Place a door on a wall at a measured position. | `wall_id`; `family_name`; `type_name`; `position_along_wall_mm`; `level_name`; `from_wall_end`; `flip_hand`; `flip_facing` |
| `add_window` | Place a window on a wall or roof at a measured position. | `host_id`; `family_name`; `type_name`; `position_along_host_mm`; `sill_height_mm`; `level_name`; `from_host_end`; `flip_hand`; `flip_facing` |
| `trim_extend_elements` | Trim or extend a linear element to meet a reference element. | `element_id`; `reference_id`; `trim_or_extend` *(default "trim")* |
| `offset_element` | Offset a wall/line/beam by a distance; optionally copy. | `element_id`; `offset_mm`; `copy` *(default true)* |
| `scale_element` | Scale an element uniformly about an optional origin point. | `element_id`; `scale_factor`; `origin_x/y/z_mm` *(optional)* |
| `array_element_linear` | Create a linear array with regular spacing. | `element_id`; `count`; `delta_x/y/z_mm`; `group_array` |
| `array_element_radial` | Create a radial (circular) array around a centre point. | `element_id`; `count`; `centre_x/y_mm`; `total_angle_degrees` *(default 360)*; `group_array` |
| `join_geometry` | Join geometry of two overlapping elements. | `element_id_a`; `element_id_b` |
| `unjoin_geometry` | Remove an existing geometry join. | `element_id_a`; `element_id_b` |
| `split_element` | Split a wall/line at a point into two segments. | `element_id`; `split_point_x/y/z_mm`; `delete_segment` *(optional)* |
| `align_elements` | Align elements to a reference element's face or axis. | `reference_element_id`; `element_ids_to_align`; `alignment_type`; `prefer_closest` |
| `place_component_in_room` | Place a family instance at the centre of a room with optional offset. | `room_id`; `family_name`; `type_name`; `offset_from_centre_x/y_mm`; `rotation_degrees` |
| `load_family_from_file` | Load an .rfa file from a local path into the active model. | `file_path`; `overwrite_existing` *(default false)* |

---

## Structural – Extended (`structural.py`)

| Tool | Description | Arguments |
|------|-------------|-----------|
| `add_wall_foundation` | Add a continuous footing beneath one or more walls. | `wall_ids`; `foundation_type_name` |
| `add_isolated_foundation` | Place isolated pad footings beneath structural columns. | `column_ids`; `foundation_family_name`; `foundation_type_name`; `depth_below_column_mm` *(default 0)* |

---

## Sheets & View Management – Extended (`sheets.py`)

| Tool | Description | Arguments |
|------|-------------|-----------|
| `create_sheet` | Create a new sheet with a title block. | `sheet_number`; `sheet_name`; `title_block_family_name`; `title_block_type_name` *(optional)* |
| `add_view_to_sheet` | Place a viewport on a sheet at given sheet coordinates. | `sheet_id`; `view_id`; `centre_x/y_mm`; `viewport_type_name` *(optional)* |
| `add_schedule_to_sheet` | Place a schedule view on a sheet. | `sheet_id`; `schedule_id`; `origin_x/y_mm` |
| `create_drafting_view` | Create a blank drafting view for 2-D work. | `view_name`; `scale` *(default 100)* |
| `create_schedule_view` | Generate a new element schedule for any category. | `category`; `schedule_name`; `fields` *(optional)*; `filter_parameter`; `filter_value` |

---

## Views – Extended (`views.py`)

| Tool | Description | Arguments |
|------|-------------|-----------|
| `hide_elements_in_view` | Hide specific elements in a view (temporary or permanent). | `element_ids`; `view_id` *(optional)*; `permanent` *(default false)* |
| `hide_category_in_view` | Hide all elements of a category in a view. | `category`; `view_id` *(optional)*; `permanent` *(default false)* |
| `isolate_elements_in_view` | Isolate elements in a view, hiding everything else. | `element_ids`; `view_id` *(optional)*; `isolate_mode` *("temporary" default or "permanent")* |
| `isolate_category_in_view` | Isolate a category in a view. | `category`; `view_id` *(optional)*; `isolate_mode` |
| `unhide_elements_in_view` | Unhide elements/categories or reset all temporary overrides. | `element_ids` *(optional)*; `category` *(optional)*; `reset_all` *(default false)*; `view_id` |
| `set_view_display_settings` | Toggle shadows, reveal hidden elements, crop region, far clip, underlay. | `view_id` *(optional)*; `show_shadows`; `reveal_hidden_elements`; `show_crop_region`; `far_clip_active`; `far_clip_offset_mm`; `underlay_orientation` |
| `create_section_view` | Cut a new section or elevation view. | `section_name`; `origin_x/y/z_mm`; `direction_x/y`; `width/height/depth_mm`; `view_type` |
| `tile_open_views` | Tile all open view windows (View → Windows → Tile). | *(none)* |
| `tab_open_views` | Arrange open views as tabs (View → Windows → Tab Views). | *(none)* |

---

## Parameters – Extended (`parameters.py`)

| Tool | Description | Arguments |
|------|-------------|-----------|
| `add_project_parameter` | Add a new project parameter bound to specified categories. | `parameter_name`; `data_type`; `group_name`; `categories`; `is_instance` *(default true)*; `is_shared`; `description` |
| `add_global_parameter` | Create or update a model-level global parameter. | `parameter_name`; `data_type`; `value` *(optional)*; `report_parameter` *(default false)* |

---

## Drafting & Text (`drafting.py`) *(new)*

| Tool | Description | Arguments |
|------|-------------|-----------|
| `add_model_text` | Place 3-D extruded model text visible in all views. | `text`; `position_x/y/z_mm`; `level_name`; `work_plane`; `depth_mm`; `font_size_mm`; `text_type_name`; `horizontal_align` |
| `add_model_line` | Add a 3-D model line between two points. | `start/end_x/y/z_mm`; `line_style`; `work_plane_level` *(optional)* |
| `add_detail_line` | Add a 2-D detail line in a view. | `start/end_x/y_mm`; `view_id` *(optional)*; `line_style` |
| `create_text_note` | Create a 2-D annotation text note in a view. | `text`; `position_x/y_mm`; `view_id` *(optional)*; `width_mm`; `horizontal_align`; `text_type_name`; `rotation_degrees` |
| `edit_text_note` | Edit the content of an existing text note. | `element_id`; `new_text` |
| `find_replace_text` | Find and replace text in text notes/model text in a view or model. | `find_string`; `replace_string`; `scope` *("view" default or "model")*; `view_id` *(optional)*; `case_sensitive`; `whole_word` |
| `check_spelling` | Return suspected misspellings in text notes and model text. | `view_id` *(optional)*; `scope` *("view" default or "model")* |
| `add_masking_region` | Add a masking region (white coverage) in a view. | `boundary_points`; `view_id` *(optional)*; `line_style` |
| `add_filled_region` | Add a hatch/solid fill annotation region in a view. | `boundary_points`; `fill_pattern_name`; `view_id` *(optional)*; `line_style`; `color_rgb` *(optional)* |
| `add_symbol` | Place an annotation or detail component symbol. | `family_name`; `type_name`; `position_x/y_mm`; `view_id` *(optional)*; `rotation_degrees` |
| `add_color_fill_legend` | Add a color fill legend for a room/area color scheme. | `view_id` *(optional)*; `scheme_name` *(optional)*; `position_x/y_mm` |

---

## Advanced Selection (`selection.py`) *(new)*

| Tool | Description | Arguments |
|------|-------------|-----------|
| `select_elements_by_category` | Select all elements of a category in the model or view, updating the Revit UI selection. | `category`; `scope` *("model" default or "view")*; `view_id` *(optional)* |
| `select_elements_by_parameter_filter` | Rule-based selection: filter elements where a parameter satisfies a condition. | `parameter_name`; `operator` – "equals", "greater_than", "contains", etc.; `value`; `category` *(optional)*; `scope`; `view_id` *(optional)* |
| `select_elements_by_type` | Select all instances of a specific element type. | `type_name`; `family_name` *(optional)*; `category` *(optional)* |
| `select_exterior_walls` | Identify and select all exterior walls. | `level_name` *(optional)* |
| `select_elements_on_level` | Select all elements on a given level with optional category filter. | `level_name`; `category` *(optional)* |
| `select_elements_in_room` | Select all elements inside a room (by ID, name, or number). | `room_id` *(optional)*; `room_name` *(optional)*; `room_number` *(optional)*; `category` *(optional)* |
| `filter_selection_by_category` | From a list of element IDs, return only those in a specific category. | `category`; `element_ids` |
| `invert_selection` | Invert the current Revit UI selection. | `scope` *("view" default or "model")*; `view_id` *(optional)* |
| `select_all_of_same_type` | Select all instances of the same type as a given element. | `element_id`; `scope` *("model" default or "view")* |
| `select_connected_elements` | Select elements connected to a given element (hosted, host, MEP system, structural). | `element_id`; `connection_type` – "hosted", "host", "mep_system", "structural_connected" |

---

## Export & Output (`export.py`) *(new)* ⚠️ Confirm with user before calling

| Tool | Description | Arguments |
|------|-------------|-----------|
| `export_to_pdf` | Export sheets or views to PDF (Revit 2022+). | `export_path`; `sheet_ids` or `view_ids`; `combine_into_one_file` *(default true)*; `paper_size`; `orientation`; `color_mode`; `raster_quality` |
| `export_to_dwg` | Export views or sheets to DWG (AutoCAD). | `export_path`; `view_ids` or `sheet_ids`; `dwg_version` *(default "R2018")*; `shared_coordinates` |
| `export_to_ifc` | Export the model to IFC for BIM interoperability. | `export_path`; `ifc_version` *("IFC4" default)*; `include_linked_files`; `export_base_quantities`; `space_boundaries` |
| `export_to_nwc` | Export to Navisworks NWC (requires NWC exporter add-in). | `export_path`; `convert_element_properties` |
| `print_sheets` | Send sheets to a printer. | `sheet_ids` *(optional)*; `printer_name` *(optional)*; `paper_size`; `orientation`; `copies`; `color_mode` |
| `save_model` | Save the active document to its current path. | *(none)* |
| `save_model_as` | Save a copy to a new file path. | `file_path`; `overwrite`; `make_central`; `compact` |
| `synchronize_with_central` | Sync workshared local model with the central file. | `comment`; `relinquish_checked_out_elements` *(default true)*; `compact_central` |

---

*V1 total: **97 tools** across 18 modules.  V2 additions: **68 tools** across 2 new + 10 extended modules.  Grand total: **165 tools** across 20 modules.*
