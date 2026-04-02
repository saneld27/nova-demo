"""Revit schedule tools – delegates execution to the Revit plugin."""
from __future__ import annotations

from typing import Any

from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool

from app.tools.elements import _delegate


@tool
async def list_schedules(config: RunnableConfig) -> list[dict[str, Any]]:
    """
    Return all schedules (and key schedules) defined in the project.

    Returns:
        List of {schedule_id, name, category, field_count, row_count,
                 is_key_schedule, on_sheets: [sheet_number]}.
    """
    return await _delegate(config, "list_schedules", {})


@tool
async def get_schedule_data(
    config: RunnableConfig,
    schedule_id: str,
    limit: int = 500,
) -> dict[str, Any]:
    """
    Return the tabular data from a schedule as a list of rows.  This is the
    most powerful data-extraction tool – use it to answer quantity, area,
    count, or parameter-aggregation questions.

    Args:
        schedule_id: Revit element ID of the schedule view.
        limit: Maximum number of data rows to return.

    Returns:
        {schedule_name, headers: [str], rows: [[value, ...]], total_rows: int}.
    """
    return await _delegate(config, "get_schedule_data", {"schedule_id": schedule_id, "limit": limit})


@tool
async def get_schedule_fields(schedule_id: str, config: RunnableConfig) -> list[dict[str, Any]]:
    """
    Return the field definitions (columns) of a schedule view.

    Args:
        schedule_id: Revit element ID of the schedule view.

    Returns:
        List of {field_index, field_name, parameter_name, data_type,
                 is_calculated, formula, is_hidden, unit_type}.
    """
    return await _delegate(config, "get_schedule_fields", {"schedule_id": schedule_id})
