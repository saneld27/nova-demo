# Nova Tools Reference – V2 (New Tools)

All **new** tools added in the second expansion pass, grouped by module.  
For the original 97 tools see [TOOLS.md](TOOLS.md).

> **Total new tools: 68**  
> Grand total (v1 + v2): **165 tools**

---

## Modify – Extensions (`modify.py`)

| Tool | Description | Key Arguments |
|------|-------------|---------------|
| `replace_element` | Replace an element with a different family/type while preserving location, level, host, and matching parameters. | `element_id`; `new_family_name`; `new_type_name` |
| `add_door` | Place a door on an existing wall at a measured position. | `wall_id`; `family_name`; `type_name`; `position_along_wall_mm`; `level_name`; `from_wall_end` *(default "start")*; `flip_hand`; `flip_facing` |
| `add_window` | Place a window on a wall or roof at a measured position. | `host_id`; `family_name`; `type_name`; `position_along_host_mm`; `sill_height_mm`; `level_name`; `from_host_end`; `flip_hand`; `flip_facing` |
| `trim_extend_elements` | Trim or extend a linear element to meet a reference element. | `element_id`; `reference_id`; `trim_or_extend` *(default "trim")* |
| `offset_element` | Offset a wall, line, or beam by a perpendicular distance; optionally copy. | `element_id`; `offset_mm`; `copy` *(default True)* |
| `scale_element` | Scale an element uniformly about an optional origin. | `element_id`; `scale_factor`; `origin_x_mm`; `origin_y_mm`; `origin_z_mm` |
| `array_element_linear` | Linear array: repeat an element at regular spacing. | `element_id`; `count`; `delta_x_mm`; `delta_y_mm`; `delta_z_mm`; `group_array` |
| `array_element_radial` | Radial array: repeat an element around a centre point. | `element_id`; `count`; `centre_x_mm`; `centre_y_mm`; `total_angle_degrees` *(default 360)*; `group_array` |
| `join_geometry` | Join two overlapping element geometries (boolean cut). | `element_id_a`; `element_id_b` |
| `unjoin_geometry` | Remove an existing geometry join between two elements. | `element_id_a`; `element_id_b` |
| `split_element` | Split a wall, line, or beam at a given point into two segments. | `element_id`; `split_point_x_mm`; `split_point_y_mm`; `split_point_z_mm`; `delete_segment` *(optional: "first"/"second")* |
| `align_elements` | Align elements to a reference element's face or axis (Revit Align command). | `reference_element_id`; `element_ids_to_align`; `alignment_type` – e.g. `"left_face"`, `"centre_x"`; `prefer_closest` |
| `place_component_in_room` | Place a family instance at the centre of a room with an optional offset. | `room_id`; `family_name`; `type_name`; `offset_from_centre_x_mm`; `offset_from_centre_y_mm`; `rotation_degrees` |
| `load_family_from_file` | Load an .rfa family from a local file path into the active model. | `file_path`; `overwrite_existing` *(default False)* – *Note: cloud library access is not supported by the Revit API.* |

---

## Views – Visibility & Display (`views.py`)

| Tool | Description | Key Arguments |
|------|-------------|---------------|
| `hide_elements_in_view` | Hide specific elements in a view (temporary or permanent). | `element_ids`; `view_id` *(optional)*; `permanent` *(default False)* |
| `hide_category_in_view` | Hide all elements of a category in a view. | `category`; `view_id` *(optional)*; `permanent` *(default False)* |
| `isolate_elements_in_view` | Isolate elements in a view, hiding everything else. | `element_ids`; `view_id` *(optional)*; `isolate_mode` *("temporary" default or "permanent")* |
| `isolate_category_in_view` | Isolate all elements of a category in a view. | `category`; `view_id` *(optional)*; `isolate_mode` |
| `unhide_elements_in_view` | Unhide elements/categories or reset all temporary view overrides. | `element_ids` *(optional)*; `category` *(optional)*; `reset_all` *(default False)*; `view_id` |
| `set_view_display_settings` | Toggle shadows, reveal hidden elements, crop region, far clip, underlay. | `view_id` *(optional)*; `show_shadows`; `reveal_hidden_elements`; `show_crop_region`; `show_annotation_crop`; `underlay_orientation`; `far_clip_active`; `far_clip_offset_mm` |
| `create_section_view` | Cut a new section or elevation view through the model. | `section_name`; `origin_x/y/z_mm`; `direction_x`; `direction_y`; `width_mm`; `height_mm`; `depth_mm`; `view_type` *("Section" default or "Elevation")* |
| `tile_open_views` | Tile all open view windows side-by-side (View → Windows → Tile). | *(none)* |
| `tab_open_views` | Arrange open views as tabs (View → Windows → Tab Views). | *(none)* |

---

## Sheets & View Management Extensions (`sheets.py`)

| Tool | Description | Key Arguments |
|------|-------------|---------------|
| `create_sheet` | Create a new sheet with a specified title block. | `sheet_number`; `sheet_name`; `title_block_family_name`; `title_block_type_name` *(optional)* |
| `add_view_to_sheet` | Place a viewport for a view onto a sheet at sheet coordinates. | `sheet_id`; `view_id`; `centre_x_mm`; `centre_y_mm`; `viewport_type_name` *(optional)* |
| `add_schedule_to_sheet` | Place a schedule view on a sheet. | `sheet_id`; `schedule_id`; `origin_x_mm`; `origin_y_mm` |
| `create_drafting_view` | Create a blank drafting view for 2-D detail work. | `view_name`; `scale` *(default 100)* |
| `create_schedule_view` | Generate a new element schedule for a category with optional column fields and a row filter. | `category`; `schedule_name`; `fields` *(optional list)*; `filter_parameter`; `filter_value` |

---

## Levels & Grids Extensions (`levels.py`)

| Tool | Description | Key Arguments |
|------|-------------|---------------|
| `create_level` | Create a new level at a given elevation, optionally auto-generating a floor plan view. | `elevation_mm`; `name` *(optional)*; `create_floor_plan` *(default True)* |
| `create_grid` | Create a straight grid line between two XY points. | `start_x/y_mm`; `end_x/y_mm`; `name` *(optional)*; `bubble_end` *("end" default, "start", "both")* |

---

## Structural Extensions (`structural.py`)

| Tool | Description | Key Arguments |
|------|-------------|---------------|
| `add_wall_foundation` | Add a continuous footing beneath one or more walls. | `wall_ids`; `foundation_type_name` |
| `add_isolated_foundation` | Place isolated pad footings beneath structural columns. | `column_ids`; `foundation_family_name`; `foundation_type_name`; `depth_below_column_mm` *(default 0)* |

---

## Annotations Extensions (`annotations.py`)

| Tool | Description | Key Arguments |
|------|-------------|---------------|
| `tag_by_category` | Tag all elements of a category in a view at once (Tag All Not Tagged). | `category`; `view_id` *(optional)*; `tag_family_name` *(optional)*; `leader` *(default False)*; `skip_already_tagged` *(default True)* |
| `add_aligned_dimension` | Aligned dimension across 2+ element faces/axes. | `reference_element_ids`; `dimension_line_x/y_mm`; `view_id` *(optional)*; `dimension_type_name` *(optional)* |
| `add_linear_dimension` | Linear (H/V/aligned) dimension between two explicit points. | `start/end_x/y_mm`; `line_position_x/y_mm`; `view_id` *(optional)*; `orientation` *("horizontal" default, "vertical", "aligned")* |
| `add_radial_dimension` | Radial dimension showing the radius of an arc element. | `arc_element_id`; `leader_end_x/y_mm`; `view_id` *(optional)* |
| `add_diameter_dimension` | Diameter dimension (⌀) on a circular arc element. | `arc_element_id`; `leader_end_x/y_mm`; `view_id` *(optional)* |
| `add_angular_dimension` | Angle between two linear elements. | `element_id_a`; `element_id_b`; `arc_position_x/y_mm`; `view_id` *(optional)* |
| `add_arc_length_dimension` | Arc length dimension on a curved element. | `arc_element_id`; `leader_end_x/y_mm`; `view_id` *(optional)* |
| `add_spot_elevation` | Spot elevation annotation on a surface point. | `element_id`; `leader_origin_x/y_mm`; `leader_end_x/y_mm`; `view_id` *(optional)* |
| `add_spot_coordinate` | Spot coordinate (N/E) annotation on a surface point. | `element_id`; `leader_origin_x/y_mm`; `leader_end_x/y_mm`; `view_id` *(optional)* |

---

## Drafting & Text (`drafting.py`) *(new module)*

| Tool | Description | Key Arguments |
|------|-------------|---------------|
| `add_model_text` | Place 3-D extruded model text visible in all views. | `text`; `position_x/y/z_mm`; `level_name`; `work_plane` *(default "XY")*; `depth_mm`; `font_size_mm`; `text_type_name`; `horizontal_align` |
| `add_model_line` | Add a 3-D model line between two points. | `start/end_x/y/z_mm`; `line_style` *(default "Model Lines")*; `work_plane_level` *(optional)* |
| `add_detail_line` | Add a 2-D detail line (view-specific) in a view. | `start/end_x/y_mm`; `view_id` *(optional)*; `line_style` *(default "Medium Lines")* |
| `create_text_note` | Create a 2-D annotation text note in a view. | `text`; `position_x/y_mm`; `view_id` *(optional)*; `width_mm`; `horizontal_align`; `text_type_name`; `rotation_degrees` |
| `edit_text_note` | Edit the content of an existing text note. | `element_id`; `new_text` |
| `find_replace_text` | Find and replace text across text notes in a view or model. | `find_string`; `replace_string`; `view_id` *(optional)*; `scope` *("view" default or "model")*; `case_sensitive`; `whole_word` |
| `check_spelling` | Return suspected misspellings in text notes/model text. | `view_id` *(optional)*; `scope` *("view" default or "model")* |
| `add_masking_region` | Add a masking region (white coverage area) in a view. | `boundary_points` – list of `{x,y}` mm; `view_id` *(optional)*; `line_style` |
| `add_filled_region` | Add a hatch/solid fill annotation region in a view. | `boundary_points`; `fill_pattern_name`; `view_id` *(optional)*; `line_style`; `color_rgb` *(optional)* |
| `add_symbol` | Place an annotation or detail component symbol (north arrow, break line, etc.). | `family_name`; `type_name`; `position_x/y_mm`; `view_id` *(optional)*; `rotation_degrees` |
| `add_color_fill_legend` | Add a color fill legend for a room/area color scheme in a view. | `view_id` *(optional)*; `scheme_name` *(optional)*; `position_x/y_mm` |

---

## Phases & Worksets Extensions (`worksets_phases.py`)

| Tool | Description | Key Arguments |
|------|-------------|---------------|
| `create_phase` | Create a new construction phase, optionally inserted after an existing phase. | `phase_name`; `insert_after_phase` *(optional)* |
| `set_element_phase_created` | Move elements to a different Phase Created (and optionally Phase Demolished). | `element_ids`; `phase_created`; `phase_demolished` *(optional)* |

---

## Parameters Extensions (`parameters.py`)

| Tool | Description | Key Arguments |
|------|-------------|---------------|
| `add_project_parameter` | Add a new project parameter bound to specified categories. | `parameter_name`; `data_type`; `group_name`; `categories`; `is_instance` *(default True)*; `is_shared` *(default False)*; `description` |
| `add_global_parameter` | Create or update a model-level global parameter for driving dimensions. | `parameter_name`; `data_type`; `value` *(optional)*; `report_parameter` *(default False)* |

---

## Advanced Selection (`selection.py`) *(new module)*

| Tool | Description | Key Arguments |
|------|-------------|---------------|
| `select_elements_by_category` | Select all elements of a category in the model or view, updating the Revit UI selection. | `category`; `scope` *("model" default or "view")*; `view_id` *(optional)*; `set_ui_selection` |
| `select_elements_by_parameter_filter` | Rule-based selection by parameter name + operator + value (e.g. Fire Rating > 60). | `parameter_name`; `operator` – "equals", "greater_than", "contains", etc.; `value`; `category` *(optional)*; `scope`; `view_id` |
| `select_elements_by_type` | Select all instances of a specific element type across the model. | `type_name`; `family_name` *(optional)*; `category` *(optional)*; `set_ui_selection` |
| `select_exterior_walls` | Identify and select all exterior walls (Function = Exterior or no interior room on one side). | `level_name` *(optional)*; `set_ui_selection` |
| `select_elements_on_level` | Select all elements on a given level, with optional category filter. | `level_name`; `category` *(optional)*; `set_ui_selection` |
| `select_elements_in_room` | Select all elements inside a room (by ID, name, or number), with optional category filter. | `room_id` *(optional)*; `room_name` *(optional)*; `room_number` *(optional)*; `category` *(optional)* |
| `filter_selection_by_category` | From a list of element IDs, return only those in a specific category. | `category`; `element_ids`; `set_ui_selection` |
| `invert_selection` | Invert the current Revit selection (relative to view or model). | `scope` *("view" default or "model")*; `view_id` *(optional)* |
| `select_all_of_same_type` | Select all instances of the same type as a given element. | `element_id`; `scope` *("model" default or "view")* |
| `select_connected_elements` | Select elements connected to a given element (hosted children, host, MEP system, structural). | `element_id`; `connection_type` – "hosted", "host", "mep_system", "structural_connected" |

---

## Export & Output (`export.py`) *(new module)*

> ⚠️ Confirm with the user before calling any of these tools.

| Tool | Description | Key Arguments |
|------|-------------|---------------|
| `export_to_pdf` | Export sheets or views to PDF (Revit 2022+). Supports combined multi-page files. | `export_path`; `sheet_ids` or `view_ids`; `combine_into_one_file` *(default True)*; `paper_size`; `orientation`; `color_mode`; `raster_quality`; `zoom_percent` |
| `export_to_dwg` | Export views or sheets to DWG (AutoCAD) format. | `export_path`; `view_ids` or `sheet_ids`; `dwg_version` *(default "R2018")*; `export_rooms_as_polylines`; `shared_coordinates` |
| `export_to_ifc` | Export the entire model to IFC for BIM interoperability. | `export_path`; `ifc_version` *("IFC4" default)*; `include_linked_files`; `export_base_quantities`; `space_boundaries` |
| `export_to_nwc` | Export to Navisworks NWC (requires NWC exporter add-in). | `export_path`; `convert_element_properties`; `export_urls`; `find_missing_materials` |
| `print_sheets` | Send sheets to a printer. | `sheet_ids` *(optional)*; `printer_name` *(optional)*; `paper_size`; `orientation`; `copies`; `color_mode` |
| `save_model` | Save the active document to its current path (Ctrl+S). | *(none)* |
| `save_model_as` | Save a copy to a new file path with optional compact and make-central options. | `file_path`; `overwrite` *(default False)*; `make_central` *(default False)*; `compact` *(default False)* |
| `synchronize_with_central` | Sync a workshared local file with the central file. | `comment`; `relinquish_checked_out_elements` *(default True)*; `compact_central` |

---

## Notes on Cloud Families

The Revit API does **not** provide a way to browse or download families from Autodesk's online content library (BIM 360 / ACC family browser) programmatically.  
Use `load_family_from_file` with an `.rfa` file saved locally or on a network share.

---

## Example Complex Workflows

### 1. Create a sheet and place a floor plan on it
```
1. list_element_types("Title Blocks")  → find title block name
2. create_sheet(sheet_number="A-101", sheet_name="Ground Floor", title_block_family_name="...")
3. list_views(view_type="FloorPlan")   → find view_id of "Level 1 Floor Plan"
4. add_view_to_sheet(sheet_id, view_id, centre_x_mm=594, centre_y_mm=420)
```

### 2. Tag all doors in the active view
```
1. get_active_view()  → get view_id
2. tag_by_category(category="Doors", view_id=...)
```

### 3. Add pad footings under all columns on Level 1
```
1. list_structural_columns(level_name="Level 1")  → get column IDs
2. list_element_types("Structural Foundations")   → pick footing type
3. add_isolated_foundation(column_ids=[...], foundation_family_name="...", foundation_type_name="...")
```

### 4. Export all sheets to a single PDF
```
1. list_sheets()   → collect all sheet_ids
2. export_to_pdf(export_path="C:\\Output\\Project.pdf", sheet_ids=[...], combine_into_one_file=True)
```

### 5. Select all fire-rated doors and tag them
```
1. select_elements_by_parameter_filter(parameter_name="Fire Rating", operator="greater_than",
       value=0, category="Doors")  → element_ids
2. tag_element(element_id=...) for each id  (or use tag_by_category for the whole view)
```

### 6. Move a project into a new phase
```
1. list_phases()           → confirm existing phase names
2. create_phase("Phase 3 – Fit-Out", insert_after_phase="Phase 2 – Structure")
3. select_elements_by_category("Furniture", scope="model")  → element_ids
4. set_element_phase_created(element_ids=[...], phase_created="Phase 3 – Fit-Out")
```

---

*Total new tools in V2: **68**.  Grand total: **165 tools** across 20 modules.*
