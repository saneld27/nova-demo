"""
Revit MEP (Mechanical / Electrical / Plumbing) discipline tools.

These tools expose system-topology and network-level queries that cannot be
answered with the generic get_elements_by_category tool alone, because MEP
systems in Revit carry connectivity and load/flow data beyond normal parameters.
"""
from __future__ import annotations

from typing import Any

from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool

from app.tools.elements import _delegate


# ── MECHANICAL ─────────────────────────────────────────────────────────────────

@tool
async def list_hvac_systems(config: RunnableConfig) -> list[dict[str, Any]]:
    """
    Return all mechanical (HVAC) systems defined in the model.

    Returns:
        List of {system_id, name, system_type, flow_cfm, static_pressure_pa,
                 equipment_count, terminal_count}.
    """
    return await _delegate(config, "list_hvac_systems", {})


@tool
async def get_hvac_system_info(system_id: str, config: RunnableConfig) -> dict[str, Any]:
    """
    Return detailed information about a specific HVAC system including its
    served equipment, connected ducts, and calculated flow/pressure values.

    Args:
        system_id: Revit element ID of the mechanical system.

    Returns:
        {system_id, name, system_type, flow_cfm, static_pressure_pa,
         equipment: [{id, name}], terminals: [{id, name, flow_cfm}],
         duct_segments: [{id, size, length_mm}]}.
    """
    return await _delegate(config, "get_hvac_system_info", {"system_id": system_id})


@tool
async def list_ducts(
    config: RunnableConfig,
    system_name: str | None = None,
    level_name: str | None = None,
    limit: int = 200,
) -> list[dict[str, Any]]:
    """
    Return duct segments in the model.  Unlike the generic element query, this
    returns duct-specific data: size, system, insulation, flow values.

    Args:
        system_name: Optional mechanical system name filter.
        level_name: Optional level filter.
        limit: Maximum number of ducts to return.

    Returns:
        List of {id, type_name, system_name, width_mm, height_mm, diameter_mm,
                 length_mm, level, flow_cfm, velocity_ms, insulation_type,
                 insulation_thickness_mm}.
    """
    return await _delegate(config, "list_ducts", {
        "system_name": system_name, "level_name": level_name, "limit": limit,
    })


@tool
async def list_air_terminals(
    config: RunnableConfig,
    system_name: str | None = None,
    level_name: str | None = None,
    limit: int = 200,
) -> list[dict[str, Any]]:
    """
    Return air terminal elements (supply/return diffusers, grilles, registers)
    with their flow assignments.

    Args:
        system_name: Optional HVAC system name filter.
        level_name: Optional level filter.
        limit: Maximum number to return.

    Returns:
        List of {id, family_name, type_name, system_name, level, flow_cfm,
                 face_size, hosted_on}.
    """
    return await _delegate(config, "list_air_terminals", {
        "system_name": system_name, "level_name": level_name, "limit": limit,
    })


@tool
async def list_mechanical_equipment(
    config: RunnableConfig,
    level_name: str | None = None,
    limit: int = 100,
) -> list[dict[str, Any]]:
    """
    Return mechanical equipment elements (AHUs, VAVs, fans, chillers, etc.)
    with their system connections and key performance parameters.

    Args:
        level_name: Optional level filter.
        limit: Maximum number to return.

    Returns:
        List of {id, family_name, type_name, level, systems_served: [name],
                 supply_flow_cfm, return_flow_cfm, electrical_load_kw}.
    """
    return await _delegate(config, "list_mechanical_equipment", {"level_name": level_name, "limit": limit})


# ── ELECTRICAL ─────────────────────────────────────────────────────────────────

@tool
async def list_electrical_systems(config: RunnableConfig) -> list[dict[str, Any]]:
    """
    Return all electrical systems (power circuits, data circuits, etc.)
    defined in the model.

    Returns:
        List of {system_id, name, system_type, panel_name, circuit_number,
                 load_va, voltage, phase_count, wire_size}.
    """
    return await _delegate(config, "list_electrical_systems", {})


@tool
async def get_electrical_system_info(system_id: str, config: RunnableConfig) -> dict[str, Any]:
    """
    Return detailed info for an electrical circuit/system including connected
    equipment, load calculations, panel board assignments, and wire sizing.

    Args:
        system_id: Revit element ID of the electrical system.

    Returns:
        {system_id, name, system_type, panel_name, circuit_number,
         load_va, apparent_load_va, voltage, phase_count, wire_size,
         elements: [{id, name, load_va}]}.
    """
    return await _delegate(config, "get_electrical_system_info", {"system_id": system_id})


@tool
async def list_electrical_equipment(
    config: RunnableConfig,
    level_name: str | None = None,
    limit: int = 100,
) -> list[dict[str, Any]]:
    """
    Return electrical equipment (distribution boards, panels, switchgear,
    transformers, UPS units) with their load and circuit summary data.

    Args:
        level_name: Optional level filter.
        limit: Maximum number to return.

    Returns:
        List of {id, family_name, type_name, level, panel_name, voltage,
                 main_breaker_rating_a, load_va, circuit_count}.
    """
    return await _delegate(config, "list_electrical_equipment", {"level_name": level_name, "limit": limit})


@tool
async def list_lighting_fixtures(
    config: RunnableConfig,
    level_name: str | None = None,
    circuit_name: str | None = None,
    limit: int = 300,
) -> list[dict[str, Any]]:
    """
    Return lighting fixtures with their circuit assignment, load, and location.
    Useful for lighting layout reviews and circuit load calculations.

    Args:
        level_name: Optional level filter.
        circuit_name: Optional circuit filter (e.g. "L1A").
        limit: Maximum number to return.

    Returns:
        List of {id, family_name, type_name, level, room_name, circuit_name,
                 load_watts, lamp_type, mounting_height_mm}.
    """
    return await _delegate(config, "list_lighting_fixtures", {
        "level_name": level_name, "circuit_name": circuit_name, "limit": limit,
    })


@tool
async def list_circuits(
    config: RunnableConfig,
    panel_id: str | None = None,
) -> list[dict[str, Any]]:
    """
    Return circuits, optionally filtered to those originating from a specific
    panel.  Each circuit entry includes its connected loads.

    Args:
        panel_id: Optional Revit element ID of an electrical panel (equipment).

    Returns:
        List of {system_id, circuit_number, panel_name, load_va, voltage,
                 phase_count, wire_size, breaker_rating_a,
                 element_count, element_ids}.
    """
    return await _delegate(config, "list_circuits", {"panel_id": panel_id})


# ── PLUMBING ───────────────────────────────────────────────────────────────────

@tool
async def list_plumbing_systems(config: RunnableConfig) -> list[dict[str, Any]]:
    """
    Return all plumbing systems defined in the model (domestic hot water,
    cold water, sanitary, fire protection, etc.).

    Returns:
        List of {system_id, name, system_type, flow_lps, pipe_segment_count,
                 fixture_count}.
    """
    return await _delegate(config, "list_plumbing_systems", {})


@tool
async def get_plumbing_system_info(system_id: str, config: RunnableConfig) -> dict[str, Any]:
    """
    Return detailed info for a plumbing system including connected fixtures,
    pipes, and calculated flow values.

    Args:
        system_id: Revit element ID of the plumbing system.

    Returns:
        {system_id, name, system_type, flow_lps, fixtures: [{id, name, fu}],
         pipes: [{id, size_mm, length_mm}]}.
    """
    return await _delegate(config, "get_plumbing_system_info", {"system_id": system_id})


@tool
async def list_pipes(
    config: RunnableConfig,
    system_name: str | None = None,
    level_name: str | None = None,
    limit: int = 300,
) -> list[dict[str, Any]]:
    """
    Return pipe segments with size, material, system, and flow data – going
    beyond what get_elements_by_category returns for plumbing analysis.

    Args:
        system_name: Optional plumbing system name filter.
        level_name: Optional level filter.
        limit: Maximum number to return.

    Returns:
        List of {id, type_name, system_name, system_type, diameter_mm,
                 length_mm, level, slope, insulation_type,
                 insulation_thickness_mm, flow_lps, velocity_ms}.
    """
    return await _delegate(config, "list_pipes", {
        "system_name": system_name, "level_name": level_name, "limit": limit,
    })


@tool
async def list_plumbing_fixtures(
    config: RunnableConfig,
    level_name: str | None = None,
    system_name: str | None = None,
    limit: int = 200,
) -> list[dict[str, Any]]:
    """
    Return plumbing fixtures (sinks, toilets, showers, etc.) with their system
    connections and fixture unit values.

    Args:
        level_name: Optional level filter.
        system_name: Optional connected plumbing system name filter.
        limit: Maximum number to return.

    Returns:
        List of {id, family_name, type_name, level, room_name,
                 systems: [name], cold_water_fu, hot_water_fu, sanitary_fu}.
    """
    return await _delegate(config, "list_plumbing_fixtures", {
        "level_name": level_name, "system_name": system_name, "limit": limit,
    })
