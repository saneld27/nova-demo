"""
Revit export, print, and file management tools.

These tools cover operations in Revit's File tab: exporting to PDF, DWG, IFC, NWC,
printing sheets/views, saving the current document, and saving as a new file.
All tools delegate execution to the Revit plugin.
"""
from __future__ import annotations

from typing import Any

from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool

from app.tools.elements import _delegate


@tool
async def export_to_pdf(
    config: RunnableConfig,
    export_path: str,
    sheet_ids: list[str] | None = None,
    view_ids: list[str] | None = None,
    combine_into_one_file: bool = True,
    paper_size: str = "A1",
    orientation: str = "Landscape",
    color_mode: str = "Color",
    raster_quality: str = "High",
    zoom_percent: int = 100,
) -> dict[str, Any]:
    """
    Export one or more sheets or views to PDF.
    Requires Revit 2022+ (native PDF export via Revit API).
    Provide either sheet_ids or view_ids; sheets are preferred for printed documentation.

    Args:
        export_path: Full output folder path (e.g. "C:\\Exports\\") or full file path
                     when combine_into_one_file is True (e.g. "C:\\Exports\\Project.pdf").
        sheet_ids: List of sheet element IDs to export. Mutually exclusive with view_ids.
        view_ids: List of view element IDs to export (when not using sheets).
        combine_into_one_file: If True (default), merge all pages into a single PDF.
        paper_size: Paper size string (e.g. "A0", "A1", "A3", "Letter"). Default "A1".
        orientation: "Portrait" or "Landscape" (default).
        color_mode: "Color" (default), "GrayScale", or "BlackAndWhite".
        raster_quality: "Draft", "Low", "Medium", "High" (default), or "Presentation".
        zoom_percent: Zoom factor as a percentage (default 100).

    Returns:
        {success: bool, output_files: [str], page_count: int, message: str}.
    """
    return await _delegate(config, "export_to_pdf", {
        "export_path": export_path,
        "sheet_ids": sheet_ids,
        "view_ids": view_ids,
        "combine_into_one_file": combine_into_one_file,
        "paper_size": paper_size,
        "orientation": orientation,
        "color_mode": color_mode,
        "raster_quality": raster_quality,
        "zoom_percent": zoom_percent,
    })


@tool
async def export_to_dwg(
    config: RunnableConfig,
    export_path: str,
    view_ids: list[str] | None = None,
    sheet_ids: list[str] | None = None,
    dwg_version: str = "R2018",
    export_rooms_as_polylines: bool = False,
    shared_coordinates: bool = True,
) -> dict[str, Any]:
    """
    Export views or sheets to DWG (AutoCAD) format.

    Args:
        export_path: Full output folder path. Each view/sheet becomes a separate DWG file
                     named after the view name / sheet number.
        view_ids: List of view element IDs to export.
        sheet_ids: List of sheet element IDs to export (exported at full sheet scale).
        dwg_version: AutoCAD version format – "R2018" (default), "R2013", "R2010",
                     "R2007", "R2004", "R2000", "R14".
        export_rooms_as_polylines: Include room boundary polylines in the DWG (default False).
        shared_coordinates: Use shared (survey) coordinates instead of project coordinates
                            (default True).

    Returns:
        {success: bool, output_files: [str], message: str}.
    """
    return await _delegate(config, "export_to_dwg", {
        "export_path": export_path,
        "view_ids": view_ids,
        "sheet_ids": sheet_ids,
        "dwg_version": dwg_version,
        "export_rooms_as_polylines": export_rooms_as_polylines,
        "shared_coordinates": shared_coordinates,
    })


@tool
async def export_to_ifc(
    config: RunnableConfig,
    export_path: str,
    ifc_version: str = "IFC4",
    include_linked_files: bool = False,
    export_base_quantities: bool = True,
    space_boundaries: int = 1,
) -> dict[str, Any]:
    """
    Export the entire Revit model to IFC (Industry Foundation Classes) format.
    Useful for BIM interoperability with structural, MEP, and construction software.

    Args:
        export_path: Full output file path (e.g. "C:\\Exports\\Project.ifc").
        ifc_version: IFC schema version – "IFC4" (default), "IFC2x3", "IFCSG".
        include_linked_files: Export linked Revit models as separate IFC files (default False).
        export_base_quantities: Include quantity takeoff data (default True).
        space_boundaries: Level of space boundary export – 0 (none), 1 (default), or 2 (detailed).

    Returns:
        {success: bool, output_file: str, element_count: int, message: str}.
    """
    return await _delegate(config, "export_to_ifc", {
        "export_path": export_path,
        "ifc_version": ifc_version,
        "include_linked_files": include_linked_files,
        "export_base_quantities": export_base_quantities,
        "space_boundaries": space_boundaries,
    })


@tool
async def export_to_nwc(
    config: RunnableConfig,
    export_path: str,
    convert_element_properties: bool = True,
    export_urls: bool = False,
    find_missing_materials: bool = False,
    divided_view_export: bool = False,
) -> dict[str, Any]:
    """
    Export the Revit model to Navisworks NWC format for coordination and clash detection.
    Requires the Navisworks NWC exporter add-in to be installed in Revit.

    Args:
        export_path: Full output file path (e.g. "C:\\Exports\\Project.nwc").
        convert_element_properties: Export Revit element parameters as Navisworks
                                    properties (default True).
        export_urls: Embed URL links for elements that have them (default False).
        find_missing_materials: Attempt to resolve missing material assets (default False).
        divided_view_export: Export using divided/sectioned view approach for large models
                             (default False).

    Returns:
        {success: bool, output_file: str, message: str}.
    """
    return await _delegate(config, "export_to_nwc", {
        "export_path": export_path,
        "convert_element_properties": convert_element_properties,
        "export_urls": export_urls,
        "find_missing_materials": find_missing_materials,
        "divided_view_export": divided_view_export,
    })


@tool
async def print_sheets(
    config: RunnableConfig,
    sheet_ids: list[str] | None = None,
    printer_name: str | None = None,
    paper_size: str = "A1",
    orientation: str = "Landscape",
    copies: int = 1,
    color_mode: str = "Color",
) -> dict[str, Any]:
    """
    Send one or more sheets to a printer.
    If no sheet_ids are provided, prints the currently active sheet/view.
    Confirm with the user before calling this tool to avoid unintended printing.

    Args:
        sheet_ids: List of sheet element IDs to print. Defaults to the active view.
        printer_name: Name of the printer/plotter as shown in Windows. Defaults to
                      the system default printer.
        paper_size: Paper size (e.g. "A1", "A3", "Letter"). Default "A1".
        orientation: "Portrait" or "Landscape" (default).
        copies: Number of copies to print (default 1).
        color_mode: "Color" (default), "GrayScale", or "BlackAndWhite".

    Returns:
        {success: bool, sheets_sent: int, message: str}.
    """
    return await _delegate(config, "print_sheets", {
        "sheet_ids": sheet_ids,
        "printer_name": printer_name,
        "paper_size": paper_size,
        "orientation": orientation,
        "copies": copies,
        "color_mode": color_mode,
    })


@tool
async def save_model(config: RunnableConfig) -> dict[str, Any]:
    """
    Save the active Revit document to its current file path (Ctrl+S equivalent).
    If the model is a central file in a workshared project, this performs a
    standard local save (not a Synchronize with Central).
    Confirm with the user before calling to avoid unexpected saves.

    Returns:
        {success: bool, file_path: str, message: str}.
    """
    return await _delegate(config, "save_model", {})


@tool
async def save_model_as(
    config: RunnableConfig,
    file_path: str,
    overwrite: bool = False,
    make_central: bool = False,
    compact: bool = False,
) -> dict[str, Any]:
    """
    Save the active Revit document as a new file (File → Save As equivalent).
    Confirm with the user before calling.

    Args:
        file_path: Full path for the new file (e.g. "C:\\Projects\\Project_v2.rvt").
        overwrite: If True, overwrite an existing file at that path (default False).
        make_central: If True, save as a new central file for worksharing (default False).
        compact: If True, compact the Revit file to reduce its size (default False).
                 Compacting takes longer but reduces file size significantly.

    Returns:
        {success: bool, file_path: str, file_size_mb: float, message: str}.
    """
    return await _delegate(config, "save_model_as", {
        "file_path": file_path,
        "overwrite": overwrite,
        "make_central": make_central,
        "compact": compact,
    })


@tool
async def synchronize_with_central(
    config: RunnableConfig,
    comment: str = "",
    relinquish_checked_out_elements: bool = True,
    compact_central: bool = False,
) -> dict[str, Any]:
    """
    Synchronize the local Revit model with the central file (workshared models only).
    Equivalent to Collaborate → Synchronize with Central.
    Should only be used in workshared projects. Confirm with the user first.

    Args:
        comment: Optional synchronization comment / change note.
        relinquish_checked_out_elements: Release borrowed/checked-out elements after sync
                                         (default True).
        compact_central: Compact the central file during synchronization (default False).

    Returns:
        {success: bool, message: str}.
    """
    return await _delegate(config, "synchronize_with_central", {
        "comment": comment,
        "relinquish_checked_out_elements": relinquish_checked_out_elements,
        "compact_central": compact_central,
    })
