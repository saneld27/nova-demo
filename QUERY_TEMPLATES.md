# Nova – Query Templates

Pre-filled input templates for the Nova plugin. Click any template to load it into the input field, then adjust the highlighted placeholders (marked with `#`) before submitting.

**Placeholder convention:** Every `#placeholder_name` is a value you should replace before sending. When a template targets something inherently specific (e.g. a real plumbing fixture or a known Revit phase), real values are used directly.

---

## 🏗️ A — Architectural Design & Layout *(Drawing, Modeling, Geometry)*

> These templates drive the most powerful multi-step modeling workflows: creating geometry, placing hosted families, arraying elements, and managing building layout directly in the model.

**A-01.** Create a straight wall and immediately tag it
```
Create a #wall_type_name wall from (#start_x_mm, #start_y_mm) to (#end_x_mm, #end_y_mm) on level #level_name at #height_mm tall, then tag it in the current view.
```

**A-02.** Build a rectangular room shell (4 walls) and place a room inside it
```
Draw four walls to form a #length_mm × #width_mm rectangle with its bottom-left corner at (#origin_x_mm, #origin_y_mm) on level #level_name using #wall_type_name at #height_mm height, then place a room inside it named "#room_name" with number "#room_number".
```

**A-03.** Create a floor slab whose boundary matches an existing room
```
Get the boundary segments of room #room_id, then create a floor using those exact boundary points on level #level_name with floor type #floor_type_name at an offset of #offset_mm.
```

**A-04.** Add a door to a wall and tag it
```
Place a #door_family_name door of type #door_type_name on wall #wall_id at #position_along_wall_mm from the start end on level #level_name, then tag it in the active view.
```

**A-05.** Add a window to a wall and tag it
```
Place a #window_family_name window of type #window_type_name on wall #wall_id at #position_along_wall_mm with a sill height of #sill_height_mm on level #level_name, then tag it in the current view.
```

**A-06.** Split a wall at a point and insert a door in the resulting gap
```
Split wall #wall_id at position (#split_x_mm, #split_y_mm, #split_z_mm), then place a #door_family_name door of type #door_type_name at that split location on level #level_name.
```

**A-07.** Create a new level with a floor plan, then copy all elements of a specific category from the level below
```
Create a new level at #elevation_mm named "#new_level_name" with a floor plan view, then get all #category elements on level "#source_level_name" and copy each one upward by the elevation difference.
```

**A-08.** Create a structural grid intersection and place a column there
```
Create a horizontal grid line from (0, #y_mm) to (#grid_length_mm, #y_mm) named "#h_grid_label", create a vertical grid line from (#x_mm, 0) to (#x_mm, #grid_length_mm) named "#v_grid_label", then place a #column_family_name column of type #column_type_name at (#x_mm, #y_mm) on level #level_name.
```

**A-09.** Create a linear array of a family instance along an axis
```
Place a #family_name #type_name at (#x_mm, #y_mm, #z_mm) on level #level_name, then create a linear array of #count total instances spaced #spacing_mm apart along the #axis axis.
```

**A-10.** Create a radial array of a family instance around a centre point
```
Place a #family_name #type_name at (#start_x_mm, #start_y_mm, 0) on level #level_name, then create a radial array of #count instances centered at (#centre_x_mm, #centre_y_mm) spanning #total_angle_degrees degrees.
```

**A-11.** Load a custom family from disk, then place an instance at a specific location
```
Load the family from "#file_path", then place an instance of type "#type_name" at (#x_mm, #y_mm, #z_mm) on level #level_name rotated #rotation_degrees degrees.
```

**A-12.** Offset a wall to create a parallel partition and change its type
```
Offset wall #wall_id by #offset_mm to create a parallel copy, then change the new wall's type to #new_wall_type_name.
```

**A-13.** Mirror a wall (or set of walls) for a symmetric wing and join geometry at the new corner
```
Mirror wall #wall_id_a across the #mirror_axis axis at coordinate #axis_coordinate_mm, then join the geometry of the mirrored wall with wall #adjacent_wall_id.
```

**A-14.** Place a component family at the centre of a specific room with rotation
```
Get the detail for room #room_id to locate its centroid, then place a #family_name #type_name at the room centre offset (#offset_x_mm, #offset_y_mm) rotated #rotation_degrees degrees on level #level_name.
```

**A-15.** Create a complete corridor: spine wall, room, and equally-spaced doors
```
Create a wall from (0, 0) to (#corridor_length_mm, 0) on level #level_name using #wall_type_name at #height_mm height, place a room along it named "Corridor", then place #door_count doors of type #door_type_name evenly spaced along the wall.
```

**A-16.** Create a stairwell enclosure: four walls + room + door
```
Draw four walls forming a #width_mm × #depth_mm enclosure at (#origin_x_mm, #origin_y_mm) on level #level_name using #wall_type_name at #height_mm height, place a room inside named "Stair Core", then add a #door_family_name door of type #door_type_name on the south-facing wall.
```

**A-17.** Align all windows on a wall to a uniform sill height, then tag all of them at once
```
Find all windows hosted by wall #wall_id, align them to the face of wall #reference_wall_id, then tag all windows in the current view using tag family #tag_family_name.
```

**A-18.** Create a double-skin facade: draw an exterior curtain wall, offset it inward, then place the structure wall behind
```
Create a #curtain_wall_type_name wall from (#start_x_mm, #start_y_mm) to (#end_x_mm, #end_y_mm) on level #level_name at #height_mm height, then offset it #cavity_depth_mm inward and create a second #structural_wall_type_name wall at the offset position.
```

**A-19.** Create an open-plan office bay: floor slab + perimeter walls + room + furniture array
```
Create a floor from boundary points (#x1,#y1), (#x2,#y2), (#x3,#y3), (#x4,#y4) on level #level_name using #floor_type_name, draw four perimeter walls at #height_mm using #wall_type_name, place a room named "Open Office", then create a linear array of #desk_family_name #desk_type_name desks — #count items spaced #spacing_mm apart.
```

**A-20.** Create a bathroom pod: enclosure walls + room + place standard fixtures
```
Draw four walls to form a #width_mm × #depth_mm bathroom at (#origin_x_mm, #origin_y_mm) on level #level_name using #wall_type_name at #height_mm height, place a room named "Bathroom" inside, place a #toilet_family_name toilet at (#toilet_x_mm, #toilet_y_mm), and place a #sink_family_name sink at (#sink_x_mm, #sink_y_mm).
```

**A-21.** Rotate an element to a target orientation and then pin it to prevent accidental moves
```
Rotate element #element_id by #angle_degrees degrees around the Z axis, then pin it in place.
```

**A-22.** Scale an element uniformly about a centre point, then move it to snap to a grid
```
Scale element #element_id by a factor of #scale_factor about origin (#origin_x_mm, #origin_y_mm, #origin_z_mm), then move it by (#delta_x_mm, #delta_y_mm, 0) to align it to the nearest grid.
```

**A-23.** Create an isolated footing grid: columns on every grid intersection + pad footings under each
```
List all structural columns on level "#foundation_level_name", then place an isolated #footing_family_name #footing_type_name footing beneath each one at a depth of #depth_below_column_mm.
```

**A-24.** Create a complete parking row: linear array of parking boundary families + dimension the row
```
Place a #parking_family_name parking space at (#x_mm, #y_mm) on level #level_name, create a linear array of #count spaces spaced #stall_width_mm apart along the X axis, then add a linear dimension across the full row.
```

**A-25.** Place a radial array of seats/chairs around a table and tag each instance
```
Place a #chair_family_name #chair_type_name at (#start_x_mm, #start_y_mm) on level #level_name, create a radial array of #count instances centered on (#table_centre_x_mm, #table_centre_y_mm) spanning 360 degrees, then tag all instances in the current view.
```

**A-26.** Replace all instances of an outdated wall type with a new type while preserving geometry
```
Find all elements of category "Walls" where the parameter "Type Name" equals "#old_type_name", then change each one to type #new_type_id.
```

**A-27.** Create a section cut through a new wall and set it as the active view
```
Create a section view named "#section_name" with its origin at (#origin_x_mm, #origin_y_mm, #origin_z_mm) facing direction (#direction_x, #direction_y), with width #width_mm, height #height_mm, and depth #depth_mm, then set it as the active view.
```

**A-28.** Join geometry between all overlapping walls and columns on a level
```
List all structural columns on level "#level_name", then join the geometry of each column with any adjacent wall whose bounding box intersects it.
```

**A-29.** Add continuous wall footings under all load-bearing walls on the ground floor
```
List all walls on level "Ground Floor" where the structural parameter indicates load-bearing, then add a continuous wall foundation of type #foundation_type_name beneath each.
```

**A-30.** Create a new phase, move existing elements into it, and add a new wall representing a future extension
```
Create a new construction phase named "#new_phase_name" inserted after "#existing_phase_name", move elements #element_ids into that phase, then create a #wall_type_name wall from (#start_x_mm, #start_y_mm) to (#end_x_mm, #end_y_mm) on level #level_name with Phase Created set to "#new_phase_name".
```

---

## 🏠 B — Space Planning & Room Management

**B-01.** Get full room details and list all elements inside a specific room
```
Get the full detail for room with number "101", then list all elements inside it filtered to category #category.
```

**B-02.** Find all rooms missing a required parameter value and flag them
```
List all rooms in the model using get_rooms_summary, then find all room elements where the parameter "#parameter_name" has no value (is empty), and report each with its name, number, and level.
```

**B-03.** Get adjacent rooms to a room and show their names, numbers, and areas
```
Get the room detail for room #room_id to confirm its name, then get all rooms directly adjacent to it and show each one's name, number, level, and area.
```

**B-04.** Place a family component at the centre of every room on a level
```
Get the room summary for all rooms on level "#level_name", then place a #family_name #type_name at the centre of each room.
```

**B-05.** Bulk-assign a department name parameter to all rooms in a zone
```
Find all room elements where the parameter "Level" equals "#level_name", then set the parameter "#department_parameter_name" to "#department_value" on all of them at once.
```

**B-06.** Get room boundary segments and create detail lines tracing the boundary in a view
```
Get the boundary segments for room #room_id, then add a detail line in the current view along each boundary segment using line style "#line_style".
```

**B-07.** List all area plans and show the areas contained within a specific plan
```
List all area plans in the project, then get all area elements inside the area plan named "#area_plan_name".
```

**B-08.** Get a room's boundaries and add a filled region representing occupancy colour in the view
```
Get the boundary points for room #room_id, then add a filled region using those boundary points with fill pattern "#fill_pattern_name" in the current view.
```

**B-09.** Select all elements inside a room and bulk-set a workset for them
```
Select all elements inside room #room_id filtered to category "#category", then move all of them to workset "#workset_name".
```

**B-10.** Create rooms for every enclosed space on a level and number them sequentially
```
Get the model info to confirm the active document, list all levels to find "#level_name", then place rooms at (#x1_mm, #y1_mm), (#x2_mm, #y2_mm), and (#x3_mm, #y3_mm) on that level with numbers "101", "102", "103" and names "#room_name_1", "#room_name_2", "#room_name_3".
```

---

## 🔍 C — Element Discovery & Analysis

**C-01.** Find all elements of a category in a view and report their key parameters
```
Get all #category elements visible in view #view_id, then for the first #limit results retrieve each element's parameters and summarize: ID, type name, level, and the value of "#key_parameter_name".
```

**C-02.** Search for elements by a parameter value and show their locations
```
Find all elements where the parameter "#parameter_name" equals "#value", then get the location (coordinates) of each result and present them as a list.
```

**C-03.** Get the host of a hosted element and then get all other elements hosted by the same host
```
Get the host element for element #element_id, then list all elements hosted by that host filtered to category "#category".
```

**C-04.** Get an element's bounding box and find all other elements whose bounding box intersects that region
```
Get the bounding box of element #element_id, then find all "#category" elements that intersect that bounding box region.
```

**C-05.** Find all elements of a category on a level and check each one for a missing required parameter
```
Get all "#category" elements on level "#level_name", then get parameters for each and report any element where "#required_parameter_name" is empty or null.
```

**C-06.** Select all elements of a type and report any that belong to the wrong workset
```
Select all instances of type "#type_name" in the model, then check each element's workset and flag any that are not assigned to "#expected_workset_name".
```

**C-07.** Perform a full-text search and then get the complete parameter set for each match
```
Search the model for "#query" across element names, type names, and parameter values limited to category "#category", then retrieve the full parameter list for each match.
```

**C-08.** Find elements by a parameter value and then get their bounding boxes to understand their spatial distribution
```
Find all elements where "#parameter_name" contains "#value", then get the bounding box for each to map their locations across the model.
```

**C-09.** Get all elements in a room and compare them to a programme requirement list
```
Get all elements inside room #room_id (category "Furniture"), then list the type names of each and compare to the required furniture list: #required_item_1, #required_item_2, #required_item_3.
```

---

## ⚙️ D — Parameter Management & Bulk Operations

**D-01.** Add a new project parameter bound to a category and then populate it on all existing instances
```
Add a new project parameter named "#parameter_name" of data type "#data_type" in group "#group_name" bound to category "#category" as an instance parameter, then bulk-set its value to "#default_value" on all existing elements of that category.
```

**D-02.** Copy a type parameter value from one family type to all other types in the same family
```
Get the type properties for type #source_type_id to read the value of "#parameter_name", then set that same parameter to the same value on type IDs #type_id_1, #type_id_2, and #type_id_3.
```

**D-03.** Find elements where a parameter exceeds a threshold and flag them in a text note
```
Find all "#category" elements where parameter "#parameter_name" is greater than #threshold_value, select them to highlight them in the UI, then create a text note in the current view at (#note_x_mm, #note_y_mm) listing the count of non-compliant elements.
```

**D-04.** Create a global parameter and apply its value across multiple element parameters
```
Create a global parameter named "#global_parameter_name" of type "#data_type" with value #value, then set the parameter "#local_parameter_name" on elements #element_id_1, #element_id_2, and #element_id_3 to match that value.
```

**D-05.** List all shared parameters, then bulk-tag every element of a category with the correct value
```
List all shared parameters currently loaded in the project to confirm "#shared_parameter_name" exists, then bulk-set that parameter to "#value" on all "#category" elements in the model.
```

**D-06.** Find all elements without a required parameter populated and set a fallback value on all of them
```
Find all "#category" elements where the parameter "#parameter_name" equals "" (empty), then bulk-set "#parameter_name" to "#fallback_value" on every result.
```

**D-07.** Compare parameter values between two elements and report differences
```
Get all parameters for element #element_id_a and element #element_id_b, then compare the values side by side and list every parameter where the two elements differ.
```

**D-08.** Retrieve a schedule's data and update element parameters to match corrected values from the schedule
```
Get the data from schedule #schedule_id, then for each row where the column "#check_column" differs from "#expected_value", set the parameter "#parameter_name" on the corresponding element to "#corrected_value".
```

---

## 📐 E — Documentation & Annotation

**E-01.** Tag all untagged elements of a category in the active view and then list any that still lack a tag
```
Tag all untagged "#category" elements in the current view using tag family "#tag_family_name" without leaders, then list any remaining elements of that category that still have no tag.
```

**E-02.** Add an aligned dimension across the faces of a row of structural elements in a view
```
Get all structural columns in view #view_id to collect their element IDs, then add an aligned dimension across all of them with the dimension line positioned at y = #dimension_line_y_mm.
```

**E-03.** Add a spot elevation on a floor element and a text note explaining the design intent
```
Add a spot elevation annotation on element #element_id with the leader origin at (#leader_origin_x_mm, #leader_origin_y_mm) and the leader end at (#leader_end_x_mm, #leader_end_y_mm) in view #view_id, then create a text note at (#note_x_mm, #note_y_mm) reading "#note_text".
```

**E-04.** Add a linear dimension between two walls and then set the dimension type to match the project standard
```
Get the locations of wall #wall_id_a and wall #wall_id_b to obtain their coordinates, then add a horizontal linear dimension from (#start_x_mm, #start_y_mm) to (#end_x_mm, #end_y_mm) with the dimension line at y = #line_y_mm in the current view.
```

**E-05.** Check spelling in all text notes in the model and report suspected misspellings
```
Check spelling across all text notes and model text in the entire model, then list every suspected misspelling together with the element ID and current text content.
```

**E-06.** Find and replace a string across all text notes in a view after a revision
```
Find all text notes in the current view containing "#old_text", then replace every occurrence of "#old_text" with "#new_text" (whole-word match, case-sensitive).
```

**E-07.** Add a radial dimension to an arc wall and then tag the element
```
Add a radial dimension on arc element #arc_element_id with the leader end at (#leader_end_x_mm, #leader_end_y_mm) in the current view, then tag element #arc_element_id using tag family "#tag_family_name".
```

**E-08.** Add an angular dimension between two walls meeting at a corner and annotate the angle with a text note
```
Add an angular dimension between wall #element_id_a and wall #element_id_b with the arc position at (#arc_position_x_mm, #arc_position_y_mm) in the current view, then create a text note at (#note_x_mm, #note_y_mm) reading "Interior angle: see dimension".
```

**E-09.** Place a filled region highlighting a zone and add a colour fill legend
```
Add a filled region in the current view using boundary points (#x1,#y1), (#x2,#y2), (#x3,#y3), (#x4,#y4) with fill pattern "#fill_pattern_name" and colour RGB (#r, #g, #b), then add a colour fill legend at (#legend_x_mm, #legend_y_mm).
```

**E-10.** Add model text as a 3-D building identifier visible in the 3-D view
```
Add model text reading "#sign_text" at position (#x_mm, #y_mm, #z_mm) on level "#level_name" at font size #font_size_mm, depth #depth_mm, horizontally centred, then switch the active view to the default 3D view to confirm placement.
```

**E-11.** Draw detail lines tracing the perimeter of a room and add dimension annotations on each side
```
Get the boundary segments for room #room_id, add a detail line in view #view_id along each segment using line style "#line_style", then add a linear dimension annotating the length of each side.
```

---

## 📋 F — Sheet Composition & Publishing

**F-01.** Create a new sheet, add a floor plan view to it, and place a schedule on the same sheet
```
Create a new sheet numbered "#sheet_number" named "#sheet_name" using title block "#title_block_family_name", add view #floor_plan_view_id centred at (#viewport_x_mm, #viewport_y_mm), then place schedule #schedule_id at (#schedule_origin_x_mm, #schedule_origin_y_mm) on the same sheet.
```

**F-02.** List all sheets in a discipline and add a revision to each sheet that is missing one
```
List all sheets filtered to discipline "#discipline", then for each sheet that has no revisions from get_sheet_revisions, get the list of revisions in the project and report which sheets are missing revision "#revision_sequence_number".
```

**F-03.** Apply a view template to all floor plan views and then tile them to compare results
```
List all views of type "FloorPlan" in the project, apply view template #template_id to each one, then tile all open view windows to compare the results side by side.
```

**F-04.** Get all viewports on a sheet and update the view scale for each one
```
Get all viewports placed on sheet #sheet_id, then for each view set the view scale property to "#scale_value".
```

**F-05.** Create a new room schedule view then place it on a sheet
```
Create a new schedule view for category "Rooms" named "#schedule_name" with fields "Number", "Name", "Level", "Area", and "Occupancy", then create a sheet numbered "#sheet_number" named "#sheet_name" with title block "#title_block_family_name" and place the new schedule at (50, 50).
```

**F-06.** Create a section view through a key building element, set display settings, and add it to a sheet
```
Create a section view named "#section_name" through origin (#origin_x_mm, #origin_y_mm, #origin_z_mm) facing direction (#direction_x, #direction_y), then set it to show shadows on and far clip active with offset #far_clip_offset_mm, and place it on sheet #sheet_id centred at (#viewport_x_mm, #viewport_y_mm).
```

**F-07.** List sheets by discipline, identify those not yet issued for construction, and add the latest revision cloud count as a text note
```
List all sheets with discipline "#discipline", get sheet revisions for each, then for any sheet where revision sequence #revision_sequence is not present, create a text note on that sheet reading "Revision #revision_sequence pending".
```

**F-08.** Create a drafting view, populate it with detail lines and text notes, then place it on a sheet
```
Create a drafting view named "#drafting_view_name" at scale #scale, add a detail line in that view from (#x1,#y1) to (#x2,#y2) using line style "#line_style", add a text note at (#note_x_mm, #note_y_mm) reading "#note_text", then place the view on sheet #sheet_id centred at (#viewport_x_mm, #viewport_y_mm).
```

---

## 🔧 G — MEP Systems

**G-01.** List all HVAC systems and show detailed info — including connected equipment — for underperforming ones
```
List all HVAC systems in the model, then get detailed info for any system where the name contains "#system_name_filter" to review its connected equipment, duct layout, and airflow values.
```

**G-02.** List ducts on a level and find any with no system assigned
```
List all ducts on level "#level_name", then find all duct elements where the parameter "System Name" is empty and report their IDs, sizes, and locations.
```

**G-03.** List air terminals on a level and tag all of them in the floor plan view
```
List all air terminals on level "#level_name", then tag all untagged air terminals in the floor plan view for that level using tag family "#tag_family_name".
```

**G-04.** List all electrical panels and get the full circuit load info for a specific panel
```
List all electrical equipment to identify all panels, then get detailed electrical system info for panel #panel_id to review load calculations, circuit assignments, and wire sizing.
```

**G-05.** Find all lighting fixtures on a level not yet assigned to a circuit
```
List all lighting fixtures on level "Level 2", then filter to those where the parameter "Circuit Number" is empty and report each one's ID, type name, and location.
```

**G-06.** List all plumbing systems and show detailed fixture counts and flow values for the sanitary system
```
List all plumbing systems in the model, then get detailed info for the system named "Sanitary" to review connected fixtures, pipe layout, and fixture unit totals.
```

**G-07.** List all pipes on a level and find those exceeding a maximum allowed diameter
```
List all pipes on level "#level_name" filtered to system "#system_name", then find all elements where the parameter "Diameter" is greater than #max_diameter_mm and report them with their locations and system assignments.
```

**G-08.** Get all lighting fixtures on a circuit and bulk-update their wattage parameter
```
List all circuits from panel #panel_id, then list all lighting fixtures assigned to circuit "#circuit_name" and bulk-set their "#wattage_parameter_name" parameter to #wattage_value.
```

**G-09.** List mechanical equipment on a level and tag each piece in the associated floor plan view
```
List all mechanical equipment on level "#level_name", then tag all instances in the floor plan view for that level using tag family "#tag_family_name".
```

**G-10.** Find all plumbing fixtures in a specific room and confirm each is assigned to the correct plumbing system
```
Get all elements inside room #room_id filtered to category "Plumbing Fixtures", then for each fixture check that the parameter "System Name" equals "#expected_system_name" and report any mismatches.
```

---

## 🏛️ H — Structural Engineering

**H-01.** List all structural columns on a level and add isolated footings beneath every one
```
List all structural columns on level "#foundation_level_name", then place an isolated #footing_family_name #footing_type_name footing beneath each column at a depth of #depth_below_column_mm.
```

**H-02.** List structural framing members and find any beams missing an analytical model
```
List all structural framing members of type "Beam" on level "#level_name", then get the analytical model for each and report any beam where the analytical model data is absent or incomplete.
```

**H-03.** List all rebar hosted by a specific concrete element and report its total count and type distribution
```
List all rebar elements hosted by element #host_element_id, then group the results by type name and report the count of each rebar type.
```

**H-04.** Add wall foundations beneath all exterior walls on the ground level
```
Select all exterior walls on level "Ground Floor", then add a continuous wall foundation of type "#foundation_type_name" beneath each one.
```

**H-05.** List all structural columns and bulk-set the fire rating parameter
```
List all structural columns in the model, then bulk-set the parameter "#fire_rating_parameter_name" to "#fire_rating_value" on all of them.
```

**H-06.** Get the analytical model for a beam and then find all other beams with the same span
```
Get the analytical model properties for element #element_id to read its span length, then find all structural framing elements where the parameter "Length" equals that same span length.
```

---

## 👁️ I — View & Visibility Management

**I-01.** Isolate a category in the active view and set the visual style to a specific display mode
```
Isolate category "#category" in the current view permanently, then set the view's visual style property to "#visual_style" (e.g. Shaded, Realistic, Wireframe).
```

**I-02.** Apply a view template and then override the visibility of a specific category
```
Apply view template #template_id to view #view_id, then hide category "#category" in that view permanently.
```

**I-03.** List all view filters on a view and remove elements violating a rule from visibility
```
List all view filters applied to view #view_id with their current override settings, then hide all elements of category "#category" where the parameter "#parameter_name" equals "#exclude_value".
```

**I-04.** Create a section cut, set its crop and far clip, then add it to a sheet
```
Create a section view named "#section_name" at origin (#x_mm, #y_mm, #z_mm) facing (#direction_x, #direction_y) with width #width_mm / height #height_mm / depth #depth_mm, set far clip active at #far_clip_offset_mm and show the crop region, then add the view to sheet #sheet_id at (#viewport_x_mm, #viewport_y_mm).
```

**I-05.** Unhide all previously hidden elements in a view and reset temporary overrides
```
Unhide all elements and categories in view #view_id and reset all temporary display overrides, then set the view detail level to "#detail_level" (Coarse, Medium, or Fine) and visual style to "#visual_style".
```

**I-06.** List all view templates and apply a specific one to all views of a given type
```
List all view templates in the project, then list all views of type "#view_type" and apply template #template_id to every one of them.
```

**I-07.** Isolate selected structural columns in the 3-D view and switch the active view to it
```
Select all structural columns on level "#level_name", isolate those elements in the default 3D view (permanently), then set the 3D view as the active view.
```

**I-08.** Set display settings for an underlay in a floor plan, then tile views to compare floors
```
Set the view display settings for view #view_id to use underlay orientation "#underlay_orientation" and enable crop region, then tile all open view windows to compare the floor plans side by side.
```

---

## 🩺 J — Project Health & QA

**J-01.** Get model warnings and cross-reference them against the affected elements to prioritise fixes
```
Get all model integrity warnings from the active document, then for each warning that mentions element ID #element_id_pattern retrieve the element detail to understand the element type, level, and parameters — and report a prioritised list of warnings to address.
```

**J-02.** Get model info and list all warnings, then report a summary health score
```
Get the high-level model info (title, version, element count, last saved), then list all current warnings, and summarise: total warnings, count by warning type, and any critical issues.
```

**J-03.** Detect duplicate room numbers by comparing the rooms summary against itself
```
Get the rooms summary for the entire model, then identify any room numbers that appear more than once across all levels and list each duplicate with its room ID, name, and level.
```

**J-04.** Check if all sheets have a matching PDF export path and flag any sheets with no current revision
```
List all sheets in the project, then for each sheet get its revisions and flag any sheet that has zero revisions — reporting sheet number, name, and discipline.
```

**J-05.** Find all elements that are pinned and report them to confirm intentional placement
```
Find all "#category" elements where the parameter "Pinned" equals true across the entire model and list each one with its ID, type, level, and location.
```

**J-06.** Verify all doors in the model have a fire rating parameter populated
```
Get all elements of category "Doors" in the model, then get the parameters for each and report any door where the parameter "Fire Rating" is empty, listing door ID, type name, host wall, and level.
```

**J-07.** Find all rooms with zero area and investigate whether they are unenclosed
```
Get the rooms summary to find all rooms where area equals 0 or is null, then get the boundary segments for each such room to determine whether it has valid enclosing walls.
```

**J-08.** Get all model warnings and bulk-pin all affected elements to prevent further accidental changes
```
List all model warnings, extract all unique element IDs mentioned in the warnings, then pin each of those elements to protect them while the warnings are being investigated.
```

---

## 🧱 K — Families, Types & Materials

**K-01.** List all loaded families of a category and get detailed type info for a specific one
```
List all loaded families of category "#category", then get detailed info for the family named "#family_name" including all its types and their type-level parameters.
```

**K-02.** Change all instances of an outdated type to a new approved type
```
Find all "#category" elements where the parameter "Type Name" equals "#old_type_name", then change every one of them to new type #new_type_id.
```

**K-03.** Get the materials applied to an element and then find all other elements using the same primary material
```
Get the materials (and compound layers) applied to element #element_id to identify the primary material, then list all elements in category "#category" that have the same material assigned.
```

**K-04.** Get detailed material properties and bulk-apply it to all elements of a category
```
Get the full properties for material #material_id (render, physical, thermal), then set the material on all "#category" elements at layer index #layer_index to that material.
```

**K-05.** List all element types for a category and set a shared type parameter across all types
```
List all element types for category "#category" filtered to family "#family_name", then set the type parameter "#parameter_name" to "#value" on every type returned.
```

**K-06.** Search for elements by material name and tag them in the current view
```
Find all elements in category "#category" where the parameter "Material" contains "#material_name", then tag all of them in the current view using tag family "#tag_family_name".
```

**K-07.** Load a new family from file, inspect its type parameters, and place one instance
```
Load the family from "#file_path", get the family info for "#family_name" to inspect all available types and their parameters, then place an instance of type "#type_name" at (#x_mm, #y_mm, #z_mm) on level "#level_name".
```

---

## 🔄 L — Phases, Worksets & Coordination

**L-01.** List all phases, identify elements created in a specific phase, and move them to a new phase
```
List all construction phases in the project to confirm the phase sequence, then find all "#category" elements where Phase Created equals "#source_phase_name" and move them to phase "#target_phase_name".
```

**L-02.** Get an element's phase info and set its phase demolished to mark it for removal
```
Get the phase created and phase demolished values for element #element_id to confirm its current phase assignment, then set its Phase Demolished to "#demolish_phase_name".
```

**L-03.** List all worksets, check which workset an element belongs to, and move it to the correct one
```
List all worksets in the workshared model, get the workset for element #element_id, and if it is not on workset "#target_workset_name" then move it there.
```

**L-04.** Bulk-move all elements of a category on a level to a specific workset
```
Select all elements of category "#category" on level "#level_name", then move all of them to workset "#workset_name".
```

**L-05.** Create a new phase and add a revision cloud to mark the affected area in the drawing
```
Create a new phase named "#phase_name" inserted after "#previous_phase_name", then list revision clouds in the active view to determine which cloud corresponds to this change phase.
```

**L-06.** List all RVT links, check a linked element's information, and report its phase and workset
```
List all Revit linked files in the model, then get element by ID #element_id (from the link) and get its workset and phase information to verify coordination status.
```

**L-07.** Get phase info for all elements on a level and report those still in an early phase
```
Get all elements of category "#category" on level "#level_name", then get the phase info for each and list any element where Phase Created is still "#early_phase_name" and Phase Demolished is empty.
```

---

## 📤 M — Export & Deliverables

**M-01.** List all sheets in a discipline, filter to those with a specific revision, and export them all to PDF
```
List all sheets filtered to discipline "#discipline", then get revisions for each and collect IDs of all sheets that include revision sequence #revision_sequence, then export those sheets to PDF at path "#export_path" combined into one file.
```

**M-02.** Get all sheets for a package, export them to DWG, and save the model
```
List all sheets where the sheet name contains "#package_name", export those sheets to DWG at path "#export_path" using DWG version "#dwg_version" with shared coordinates enabled, then save the model to its current path.
```

**M-03.** Export the full model to IFC with base quantities and then synchronise with central
```
Export the model to IFC at path "#export_path" using IFC version "IFC4" with base quantities enabled and space boundaries level 2, then synchronise with the central file with comment "#sync_comment" and relinquish all checked-out elements.
```

**M-04.** Export selected sheets to PDF and print the same sheets on a named printer
```
List all sheets where the discipline equals "#discipline", export them to PDF at "#export_path" with colour mode "#color_mode" and orientation "#orientation", then print the same sheets on printer "#printer_name" as #copies copies.
```

**M-05.** Save the model as a new milestone copy and then export a Navisworks NWC for clash detection
```
Save a copy of the model to "#milestone_file_path" without making it central, then export the model to Navisworks NWC at "#nwc_export_path" with element properties converted.
```

**M-06.** List all views of a type, export them to DWG for consultant issue, and log the sheets exported
```
List all views of type "#view_type", export all of them to DWG at path "#export_path" using version "R2018", then get the model info to confirm the model title and last-saved timestamp for the issue record.
```

---

## 📊 N — Schedules & Data Extraction

**N-01.** Create a new schedule for a category with custom fields, then place it on a sheet
```
Create a schedule view for category "#category" named "#schedule_name" with fields "#field_1", "#field_2", "#field_3", and "#field_4", filter by parameter "#filter_parameter" equals "#filter_value", then place it on sheet #sheet_id at origin (#origin_x_mm, #origin_y_mm).
```

**N-02.** Pull data from an existing schedule and bulk-update the corresponding element parameters
```
Get all data rows from schedule #schedule_id, then for each row find the element by ID and set parameter "#parameter_name" to the value in column "#column_name".
```

**N-03.** List all schedules and extract data from the door schedule to cross-check fire ratings
```
List all schedules in the project to find a schedule containing "Door", then get its data and check every row where column "Fire Rating" is empty — report each door's mark, type, and host wall.
```

**N-04.** Get a schedule's field definitions and add a missing calculated-value field by creating a project parameter and refreshing the schedule
```
Get the field definitions for schedule #schedule_id to confirm the current columns, then add a new project parameter named "#new_parameter_name" of type "#data_type" bound to category "#category", and report that the schedule can now be updated to include it.
```

**N-05.** Extract room schedule data and export a summary of total area per level as a text note in a view
```
Get all data from the room schedule #schedule_id, sum the area column grouped by Level, then create a text note in view #view_id at (#note_x_mm, #note_y_mm) listing the total area per level as a summary table.
```

---

## 🔗 O — Links, Groups & Design Options

**O-01.** List all RVT links and all CAD imports, then report any CAD files that should be linked rather than imported
```
List all Revit linked files in the model and all imported/linked CAD files, then identify any CAD elements that appear to be directly imported (not linked) and report them by name and category for review.
```

**O-02.** List all groups and get the instances of a specific group to understand where it is placed
```
List all model groups in the project with their instance counts, then get all placed instances of group named "#group_name" with their locations and host levels.
```

**O-03.** List all design options and show the elements that differ between two options
```
List all design option sets and their options, then get all "#category" elements in the active view and find elements where the parameter "Design Option" differs between option "#option_a_name" and option "#option_b_name".
```

---

*Template count: **80+ unique multi-tool templates** across **15 sections***.  
*Each `#placeholder` is intended to be editable inline before submission.*
