"""Revit workset and phase management tools – delegates execution to the Revit plugin."""
from __future__ import annotations

from typing import Any

from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool

from app.tools.elements import _delegate


@tool
async def list_worksets(config: RunnableConfig) -> list[dict[str, Any]]:
    """
    Return all user-created worksets in the workshared model.
    Returns an empty list for non-workshared models.

    Returns:
        List of {workset_id, name, kind, is_open, is_editable, owner, borrowers}.
    """
    return await _delegate(config, "list_worksets", {})


@tool
async def get_element_workset(element_id: str, config: RunnableConfig) -> dict[str, Any]:
    """
    Return the workset that the given element belongs to.

    Args:
        element_id: Revit element ID.

    Returns:
        {workset_id, workset_name, is_editable}.
    """
    return await _delegate(config, "get_element_workset", {"element_id": element_id})


@tool
async def set_element_workset(
    config: RunnableConfig,
    element_id: str,
    workset_name: str,
) -> dict[str, Any]:
    """
    Move an element to a different workset.  The workset must already exist.
    Use list_worksets to discover available workset names first.

    Args:
        element_id: Revit element ID.
        workset_name: Name of the target workset.

    Returns:
        {success: bool, message: str, previous_workset: str}.
    """
    return await _delegate(config, "set_element_workset", {
        "element_id": element_id, "workset_name": workset_name,
    })


@tool
async def list_phases(config: RunnableConfig) -> list[dict[str, Any]]:
    """
    Return all construction phases defined in the project, in sequence order.

    Returns:
        List of {phase_id, name, sequence_number, description}.
    """
    return await _delegate(config, "list_phases", {})


@tool
async def get_element_phase_info(element_id: str, config: RunnableConfig) -> dict[str, Any]:
    """
    Return the phase created and phase demolished values for an element,
    along with its status in the currently active phase filter.

    Args:
        element_id: Revit element ID.

    Returns:
        {element_id, phase_created: str, phase_demolished: str | null,
         status_in_active_phase: "New"|"Existing"|"Demolished"|"Temporary"}.
    """
    return await _delegate(config, "get_element_phase_info", {"element_id": element_id})


# DISABLED – too complex for plugin side
@tool
async def create_phase(
    config: RunnableConfig,
    phase_name: str,
    insert_after_phase: str | None = None,
) -> dict[str, Any]:
    """
    Create a new construction phase in the project's phase table.
    Use list_phases() first to see existing phases and their order.

    Args:
        phase_name: Name for the new phase (e.g. "Phase 3 - Fit-Out").
        insert_after_phase: Name of an existing phase after which to insert this new phase.
                            If omitted, the new phase is appended at the end.

    Returns:
        {success: bool, phase_id: str, phase_name: str, sequence: int, message: str}.
    """
    return await _delegate(config, "create_phase", {
        "phase_name": phase_name,
        "insert_after_phase": insert_after_phase,
    })


@tool
async def set_element_phase_created(
    config: RunnableConfig,
    element_ids: list[str],
    phase_created: str,
    phase_demolished: str | None = None,
) -> dict[str, Any]:
    """
    Assign or change the Phase Created (and optionally Phase Demolished) of one or
    more elements. This effectively moves an element into a different construction phase.
    Use list_phases() to get valid phase names.

    Args:
        element_ids: List of element IDs to update.
        phase_created: Name of the phase in which the elements should appear as new.
        phase_demolished: Optional name of the phase in which the elements are demolished.
                          Pass None (default) to clear any demolish phase.

    Returns:
        {success: bool, updated_count: int, message: str}.
    """
    return await _delegate(config, "set_element_phase_created", {
        "element_ids": element_ids,
        "phase_created": phase_created,
        "phase_demolished": phase_demolished,
    })
