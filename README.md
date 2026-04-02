# Nova Demo

An agentic AI backend for Revit automation, powered by **FastAPI**, **LangGraph** (ReAct agent), and **OpenAI GPT-4o**.  
Designed to be called from a Revit plugin; every request must carry an **Auth0 JWT** that includes a Revit-provider claim.

---

## Architecture

```
Revit Plugin
  │  HTTP POST /api/v1/chat/stream
  │  Authorization: Bearer <Auth0 JWT>
  ▼
Nova FastAPI Backend
  ├── JWT Validation (Auth0 RS256 + provider claim check)
  ├── LangGraph ReAct Agent
  │     └── OpenAI GPT-4o (streaming)
  │           └── Tool calls ──► Revit Tools (170+ tools)
  │                               ↕ JSON RPC
  │                              Revit Plugin (local bridge)
  └── SSE Stream → Revit Plugin UI
```

### Tool set

Tools are organised into modules under `app/tools/`.  **170+ tools** are registered and available to the agent.

#### 🔍 Element Querying (`elements.py`)

| Tool | Description |
|------|-------------|
| `get_selected_elements` | Return elements currently selected in the Revit UI |
| `get_elements_by_category` | List elements by Revit category |
| `get_element_by_id` | Fetch a single element by ID |
| `get_elements_in_view` | Return elements visible in a view |
| `get_elements_by_level` | Return elements associated with a level |
| `get_elements_in_room` | Return elements spatially inside a room |
| `search_elements` | Full-text search across names, types, and parameter values |
| `find_elements_by_parameter_value` | Find elements where a parameter equals a given value |
| `get_element_location` | Return the geometric location (point or curve) of an element |
| `get_element_bounding_box` | Return the 3-D axis-aligned bounding box of an element |
| `get_element_host` | Return the host of a hosted element |
| `get_hosted_elements` | Return all elements hosted by a given element |
| `get_elements_in_bounding_box` | Return elements whose bounding box intersects a 3-D region |

#### ⚙️ Parameters (`parameters.py`)

| Tool | Description |
|------|-------------|
| `get_element_parameters` | Read all parameters of an element |
| `set_element_parameter` | Write a parameter value on an element |
| `bulk_set_parameter` | Set the same parameter on multiple elements at once |
| `list_project_parameters` | Return all project parameters defined in the document |
| `list_shared_parameters` | Return all shared parameters loaded in the project |
| `add_project_parameter` | Add a new project parameter bound to one or more categories |
| `add_global_parameter` | Add or update a global parameter |

#### ✏️ Modify & Create (`modify.py`)

| Tool | Description |
|------|-------------|
| `move_element` | Move an element by a translation vector |
| `rotate_element` | Rotate an element around an axis |
| `copy_element` | Copy an element with an offset |
| `mirror_element` | Mirror an element across a plane |
| `delete_element` | Delete an element from the model |
| `create_wall` | Create a straight wall between two points |
| `create_floor` | Create a floor from a closed boundary polygon |
| `place_family_instance` | Place any loaded family instance at coordinates |
| `create_room` | Place a room at an XY point on a level |
| `pin_element` | Pin an element to prevent accidental changes |
| `unpin_element` | Unpin a pinned element |
| `replace_element` | Replace an element with a different family/type |
| `add_door` | Place a door on an existing wall |
| `add_window` | Place a window on an existing wall or roof |
| `trim_extend_elements` | Trim or extend a linear element to a reference |
| `offset_element` | Offset a wall, line, or beam by a distance |
| `scale_element` | Scale an element uniformly about an origin point |
| `array_element_linear` | Create a linear array of an element |
| `array_element_radial` | Create a radial (circular) array of an element |
| `join_geometry` | Join geometry of two overlapping elements |
| `unjoin_geometry` | Remove a geometry join between two elements |
| `split_element` | Split a wall, beam, or line at a specified point |
| `align_elements` | Align elements to a reference face or axis |
| `place_component_in_room` | Place a family instance centred inside a room |
| `load_family_from_file` | Load a Revit family (.rfa) from a file path |

#### 👁️ Views & Display (`views.py`)

| Tool | Description |
|------|-------------|
| `list_views` | List all views with optional type filter |
| `get_active_view` | Return the currently active view |
| `hide_elements_in_view` | Hide specific elements in a view |
| `hide_category_in_view` | Hide all elements of a category in a view |
| `isolate_elements_in_view` | Isolate specific elements, hiding everything else |
| `isolate_category_in_view` | Isolate all elements of a category |
| `unhide_elements_in_view` | Unhide elements/categories or reset all overrides |
| `set_view_display_settings` | Toggle shadows, crop, far clip, underlay, and more |
| `create_section_view` | Create a section or elevation view from a cut plane |
| `tile_open_views` | Tile all open view windows side-by-side |
| `tab_open_views` | Arrange open view windows as tabs |

#### 📋 Sheets & Compositions (`sheets.py`)

| Tool | Description |
|------|-------------|
| `list_sheets` | List sheets with optional discipline or search filter |
| `get_sheet_views` | Return viewports placed on a sheet |
| `set_view_property` | Set a property on a view (scale, detail level, etc.) |
| `list_view_filters` | Return filters applied to a view with override settings |
| `list_view_templates` | Return all view templates in the project |
| `apply_view_template` | Apply a view template to a view |
| `set_active_view` | Switch the Revit UI to a specific view |
| `create_sheet` | Create a new sheet with a title block |
| `add_view_to_sheet` | Place a viewport on a sheet |
| `add_schedule_to_sheet` | Place a schedule on a sheet |
| `create_drafting_view` | Create a blank drafting view for 2-D detail work |
| `create_schedule_view` | Create a new element schedule view |

#### 📐 Annotations (`annotations.py`)

| Tool | Description |
|------|-------------|
| `list_dimensions` | Return dimension annotations in a view |
| `list_text_notes` | Return text note annotations in a view |
| `list_tags` | Return tag annotations, optionally filtered by category |
| `list_keynotes` | Return keynote annotations in a view |
| `list_revision_clouds` | Return revision cloud elements |
| `tag_element` | Place a tag annotation on an element |
| `tag_by_category` | Tag all untagged elements of a category in a view |
| `add_aligned_dimension` | Add an aligned dimension across two or more elements |
| `add_linear_dimension` | Add a linear (horizontal/vertical) dimension between two points |
| `add_radial_dimension` | Add a radial dimension to a circular arc element |
| `add_diameter_dimension` | Add a diameter (⌀) dimension to a circular arc element |
| `add_angular_dimension` | Add an angular dimension between two linear elements |
| `add_arc_length_dimension` | Add an arc length dimension to a curved element |
| `add_spot_elevation` | Add a spot elevation annotation |
| `add_spot_coordinate` | Add a spot coordinate annotation |

#### ✍️ Drafting (`drafting.py`)

| Tool | Description |
|------|-------------|
| `add_model_text` | Add a 3-D model text element visible in all views |
| `add_model_line` | Add a straight model line between two 3-D points |
| `create_text_note` | Create a 2-D annotation text note in a view |
| `edit_text_note` | Edit the content of an existing text note |
| `find_replace_text` | Find and replace text across notes in a view or the entire model |
| `check_spelling` | Spell-check text notes and model text |
| `add_masking_region` | Add a masking region to blank out content in a view |
| `add_filled_region` | Add a filled region with a drafting fill pattern |
| `add_symbol` | Place an annotation symbol or detail component in a view |
| `add_detail_line` | Add a 2-D detail line (view-specific) |
| `add_color_fill_legend` | Add a color fill legend to a view |

#### 🏠 Rooms & Areas (`rooms_areas.py`)

| Tool | Description |
|------|-------------|
| `get_rooms_summary` | Return a summary of all rooms in the model |
| `get_room_detail` | Return full detail for a room by ID, name, or number |
| `get_room_boundaries` | Return boundary segments and hosting elements of a room |
| `get_room_adjacency` | Return rooms directly adjacent to a given room |
| `list_area_plans` | Return all area plans in the project |
| `get_areas_in_plan` | Return area elements inside a specific area plan |

#### 🏗️ Families & Types (`families_types.py`)

| Tool | Description |
|------|-------------|
| `list_element_types` | Return all types (family symbols) for a category |
| `get_type_properties` | Return type-level parameters for a family symbol |
| `set_type_parameter` | Set a type parameter on a family symbol |
| `list_loaded_families` | Return all families loaded in the project |
| `get_family_info` | Return detailed info about a family and its types |
| `change_element_type` | Change an element to a different type |

#### 🧱 Materials (`materials.py`)

| Tool | Description |
|------|-------------|
| `list_materials` | Return all materials with optional name filter |
| `get_material_info` | Return detailed render, physical, and thermal properties |
| `get_element_materials` | Return materials applied to an element by compound layer |
| `set_element_material` | Assign a material to an element or compound layer |

#### 📏 Levels & Grids (`levels.py`)

| Tool | Description |
|------|-------------|
| `list_levels` | Return all levels in the document |
| `list_grids` | Return all grid lines |
| `create_level` | Create a new level with an optional floor plan view |
| `create_grid` | Create a straight grid line between two XY points |

#### 🏛️ Structural (`structural.py`)

| Tool | Description |
|------|-------------|
| `list_structural_columns` | Return structural columns |
| `list_structural_framing` | Return beams, braces, trusses, and girders |
| `list_structural_foundations` | Return isolated, wall, and slab foundation elements |
| `get_analytical_model` | Return analytical model properties of a structural element |
| `list_rebar` | Return rebar elements, optionally filtered by host |
| `add_wall_foundation` | Add continuous wall footings beneath walls |
| `add_isolated_foundation` | Place pad footings beneath structural columns |

#### 🔧 MEP (`mep.py`)

| Tool | Description |
|------|-------------|
| `list_hvac_systems` | Return all HVAC/mechanical systems |
| `get_hvac_system_info` | Return detailed info for an HVAC system |
| `list_ducts` | Return duct segments with flow and size data |
| `list_air_terminals` | Return supply/return diffusers with flow data |
| `list_mechanical_equipment` | Return AHUs, VAVs, fans, and other mechanical equipment |
| `list_electrical_systems` | Return all electrical circuits and systems |
| `get_electrical_system_info` | Return detailed electrical circuit info |
| `list_electrical_equipment` | Return panels, boards, and switchgear |
| `list_lighting_fixtures` | Return lighting fixtures with circuit and load data |
| `list_circuits` | Return circuits, optionally filtered by panel |
| `list_plumbing_systems` | Return all plumbing systems |
| `get_plumbing_system_info` | Return detailed info for a plumbing system |
| `list_pipes` | Return pipe segments with size, flow, and system data |
| `list_plumbing_fixtures` | Return plumbing fixtures with system connections |

#### 📊 Schedules (`schedules.py`)

| Tool | Description |
|------|-------------|
| `list_schedules` | Return all schedules in the project |
| `get_schedule_data` | Return tabular data rows from a schedule |
| `get_schedule_fields` | Return field definitions (columns) of a schedule |

#### 🔄 Worksets & Phases (`worksets_phases.py`)

| Tool | Description |
|------|-------------|
| `list_worksets` | Return all user worksets in a workshared model |
| `get_element_workset` | Return the workset an element belongs to |
| `set_element_workset` | Move an element to a different workset |
| `list_phases` | Return all construction phases in sequence order |
| `get_element_phase_info` | Return phase created/demolished for an element |
| `create_phase` | Create a new construction phase |
| `set_element_phase_created` | Assign or change the phase of one or more elements |

#### 🔗 Links, Groups & Design Options (`links_groups.py`)

| Tool | Description |
|------|-------------|
| `list_rvt_links` | Return all Revit linked file references |
| `list_cad_links` | Return all imported/linked CAD files |
| `list_groups` | Return all model and detail group types |
| `get_group_instances` | Return placed instances of a named group |
| `list_design_options` | Return all design option sets and their options |

#### 📅 Revisions (`revisions.py`)

| Tool | Description |
|------|-------------|
| `list_revisions` | Return all project revisions |
| `get_sheet_revisions` | Return revisions appearing in a sheet's revision block |
| `get_revision_clouds_for_element` | Return revision clouds that reference a specific element |

#### 🔎 Selection (`selection.py`)

| Tool | Description |
|------|-------------|
| `select_elements_by_category` | Select all elements of a category |
| `select_elements_by_parameter_filter` | Select elements matching a parameter condition |
| `select_elements_by_type` | Select all instances of a specific type |
| `select_exterior_walls` | Identify and select exterior walls |
| `select_elements_on_level` | Select elements on a level |
| `select_elements_in_room` | Select elements inside a room |
| `filter_selection_by_category` | Filter an element list to a specific category |
| `invert_selection` | Invert the current Revit UI selection |
| `select_all_of_same_type` | Select all instances of the same type as an element |
| `select_connected_elements` | Select elements connected or hosted by a given element |

#### 📤 Export & File Management (`export.py`)

| Tool | Description |
|------|-------------|
| `export_to_pdf` | Export sheets or views to PDF |
| `export_to_dwg` | Export views or sheets to DWG |
| `export_to_ifc` | Export the model to IFC |
| `export_to_nwc` | Export the model to Navisworks NWC |
| `print_sheets` | Send sheets to a printer |
| `save_model` | Save the active document |
| `save_model_as` | Save the document as a new file |
| `synchronize_with_central` | Synchronize with the central file (workshared models) |

#### 🗺️ Site & Location (`site.py`)

| Tool | Description |
|------|-------------|
| `get_toposurface_info` | Return topographic surface elements with elevation data |
| `list_site_components` | Return site components (planting, parking, furniture) |
| `get_project_location` | Return geographic location, true north, and coordinate system |

#### 🩺 Model Info & Health (`model_info.py`)

| Tool | Description |
|------|-------------|
| `get_model_info` | Return high-level document info (title, version, element count) |
| `list_warnings` | Return model integrity warnings |

---

## Quick Start

### 1. Prerequisites

- Python ≥ 3.11
- [uv](https://docs.astral.sh/uv/) installed (`pip install uv` or `brew install uv`)
- An Auth0 tenant with an API audience configured

### 2. Install dependencies

```bash
cd nova_demo
uv venv
uv pip install -e ".[dev]"
```

### 3. Configure environment

```bash
cp .env.example .env
# Edit .env with your Auth0 domain, audience, and OpenAI API key
```

### 4. Run the server

```bash
uv run uvicorn app.main:app --reload --port 8000
```

Open [http://localhost:8000/docs](http://localhost:8000/docs) for the interactive Swagger UI.

---

## Auth0 Setup

1. Create an **API** in Auth0 with audience `https://nova-demo-api`.
2. In your Revit plugin's Auth0 application, add a custom claim to the access token (via Auth0 Actions or Rules):

```js
// Auth0 Action – add-revit-provider-claim
exports.onExecutePostLogin = async (event, api) => {
  api.accessToken.setCustomClaim("https://nova-demo/provider", "revit-plugin");
};
```

3. The backend validates:
   - Signature (RS256 via JWKS)
   - Audience & Issuer
   - `https://nova-demo/provider == "revit-plugin"`

---

## Consuming the SSE Stream (Revit Plugin)

```csharp
// Pseudo-code – C# Revit plugin
using var client = new HttpClient();
client.DefaultRequestHeaders.Authorization =
    new AuthenticationHeaderValue("Bearer", accessToken);

var request = new { message = "List all walls on Level 1", context = new { } };
using var response = await client.PostAsJsonAsync(
    "http://localhost:8000/api/v1/chat/stream", request);

await foreach (var sseEvent in response.ReadServerSentEventsAsync())
{
    var chunk = JsonSerializer.Deserialize<StreamChunk>(sseEvent.Data);
    switch (chunk.Type)
    {
        case "token":       AppendToUI(chunk.Content); break;
        case "tool_call":   ShowToolSpinner(chunk.Data["tool"]); break;
        case "tool_result": HideToolSpinner(); break;
        case "done":        FinaliseUI(chunk.Content); break;
        case "error":       ShowError(chunk.Content); break;
    }
}
```

---

## Extending with New Revit Tools

1. Add a new `@tool` function in `app/tools/your_module.py`.
2. Import and append it to `ALL_REVIT_TOOLS` in `app/tools/__init__.py`.
3. The agent picks it up automatically on next restart.

---

## Project Structure

```
nova_demo/
├── app/
│   ├── main.py                  # FastAPI app, CORS, lifespan
│   ├── config.py                # Pydantic Settings (env vars)
│   ├── auth/
│   │   ├── jwt_validator.py     # Auth0 RS256 + provider claim validation
│   │   └── dependencies.py     # get_current_user FastAPI dependency
│   ├── agents/
│   │   ├── revit_agent.py       # LangGraph ReAct agent + SSE streaming
│   │   └── prompts.py           # System prompt
│   ├── tools/
│   │   ├── __init__.py          # ALL_REVIT_TOOLS registry
│   │   ├── annotations.py       # Dimensions, tags, text notes, revision clouds
│   │   ├── drafting.py          # Model text, detail lines, filled regions
│   │   ├── elements.py          # Element querying and spatial lookups
│   │   ├── export.py            # PDF, DWG, IFC, NWC, print, save
│   │   ├── families_types.py    # Family and type management
│   │   ├── levels.py            # Levels and grids
│   │   ├── links_groups.py      # RVT links, CAD links, groups, design options
│   │   ├── materials.py         # Material properties and assignments
│   │   ├── mep.py               # HVAC, electrical, and plumbing tools
│   │   ├── model_info.py        # Model health, warnings, rooms summary
│   │   ├── modify.py            # Create, move, copy, array, join, etc.
│   │   ├── parameters.py        # Read and write element parameters
│   │   ├── revisions.py         # Revision management
│   │   ├── rooms_areas.py       # Room details, boundaries, adjacency, areas
│   │   ├── schedules.py         # Schedule data extraction
│   │   ├── selection.py         # Advanced element selection and filtering
│   │   ├── sheets.py            # Sheet and view management
│   │   ├── site.py              # Topography and project location
│   │   ├── structural.py        # Columns, framing, foundations, rebar
│   │   ├── views.py             # View display, visibility, section creation
│   │   └── worksets_phases.py   # Workset and phase management
│   ├── api/
│   │   └── routes.py            # /chat/stream, /tools, /health
│   └── models/
│       └── schemas.py           # Pydantic request/response models
├── pyproject.toml
├── .env.example
└── README.md
```

---

## Roadmap

- [ ] Real Revit plugin RPC bridge (WebSocket / named pipe)
- [ ] Multi-agent supervisor for complex multi-step Revit workflows
- [ ] Session memory / conversation history (Redis or in-memory)
- [ ] Element geometry & BIM data tools
- [ ] Transaction management (undo/redo support)
- [ ] Auth0 user-level RBAC (read-only vs. write permissions)
