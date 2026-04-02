"""Revit revision management tools – delegates execution to the Revit plugin."""
from __future__ import annotations

from typing import Any

from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool

from app.tools.elements import _delegate


@tool
async def list_revisions(config: RunnableConfig) -> list[dict[str, Any]]:
    """
    Return all project revisions defined in the revision table.

    Returns:
        List of {revision_id, sequence, date, description, issued_by,
                 issued_to, visibility, numbering_type}.
    """
    return await _delegate(config, "list_revisions", {})


@tool
async def get_sheet_revisions(sheet_id: str, config: RunnableConfig) -> list[dict[str, Any]]:
    """
    Return all revisions that appear in the revision block of a specific sheet,
    both from clouds placed on views and manually assigned revisions.

    Args:
        sheet_id: Revit element ID of the sheet.

    Returns:
        List of {revision_id, sequence, date, description, cloud_count}.
    """
    return await _delegate(config, "get_sheet_revisions", {"sheet_id": sheet_id})


@tool
async def get_revision_clouds_for_element(
    element_id: str,
    config: RunnableConfig,
) -> list[dict[str, Any]]:
    """
    Return revision clouds that reference or enclose a specific element.
    Useful for finding which revisions affected a particular wall, room, etc.

    Args:
        element_id: Revit element ID to check.

    Returns:
        List of {cloud_id, revision_sequence, revision_date, revision_description,
                 view_id, view_name, comments}.
    """
    return await _delegate(config, "get_revision_clouds_for_element", {"element_id": element_id})
