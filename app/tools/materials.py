"""Revit materials tools – delegates execution to the Revit plugin."""
from __future__ import annotations

from typing import Any

from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool

from app.tools.elements import _delegate


@tool
async def list_materials(
    config: RunnableConfig,
    search: str | None = None,
) -> list[dict[str, Any]]:
    """
    Return all materials defined in the project, with optional name filter.

    Args:
        search: Optional substring match against material name.

    Returns:
        List of {material_id, name, material_class, shading_color_rgb,
                 has_render_appearance, has_physical_properties,
                 thermal_conductivity_wpmk}.
    """
    return await _delegate(config, "list_materials", {"search": search})


@tool
async def get_material_info(material_id: str, config: RunnableConfig) -> dict[str, Any]:
    """
    Return detailed properties of a material including its render appearance,
    physical properties (structural), and thermal properties.

    Args:
        material_id: Revit element ID of the material.

    Returns:
        {material_id, name, material_class, shading_color_rgb,
         physical: {density_kgpm3, youngs_modulus_mpa, poissons_ratio, thermal_expansion},
         thermal: {conductivity_wpmk, specific_heat_jpkgk, emissivity},
         render_appearance_name}.
    """
    return await _delegate(config, "get_material_info", {"material_id": material_id})


@tool
async def get_element_materials(element_id: str, config: RunnableConfig) -> list[dict[str, Any]]:
    """
    Return the materials (and paint overrides) applied to an element,
    broken down by compound layer if applicable (e.g. wall layers).

    Args:
        element_id: Revit element ID.

    Returns:
        List of {layer_index, function, material_id, material_name,
                 thickness_mm, area_sqm, volume_m3, is_paint}.
    """
    return await _delegate(config, "get_element_materials", {"element_id": element_id})


@tool
async def set_element_material(
    config: RunnableConfig,
    element_id: str,
    material_name: str,
    layer_index: int = 0,
) -> dict[str, Any]:
    """
    Assign a material to an element or a specific layer of a compound element
    (wall, floor, roof).

    Args:
        element_id: Revit element ID.
        material_name: Name of the material to assign (must already be loaded).
        layer_index: Compound layer index (0-based). Use 0 for simple elements.

    Returns:
        {success: bool, message: str}.
    """
    return await _delegate(config, "set_element_material", {
        "element_id": element_id, "material_name": material_name, "layer_index": layer_index,
    })
