"""Collects all Revit LangChain tools into a single importable list."""
from __future__ import annotations

from langchain_core.tools import BaseTool

from app.tools.elements import get_element_by_id, get_elements_by_category
from app.tools.levels import list_grids, list_levels
from app.tools.model_info import get_model_info, get_rooms_summary, list_warnings
from app.tools.parameters import get_element_parameters, set_element_parameter
from app.tools.views import get_active_view, list_views

ALL_REVIT_TOOLS: list[BaseTool] = [
    # Element queries
    get_elements_by_category,
    get_element_by_id,
    # Parameters
    get_element_parameters,
    set_element_parameter,
    # Views
    list_views,
    get_active_view,
    # Levels & grids
    list_levels,
    list_grids,
    # Model health & rooms
    get_model_info,
    list_warnings,
    get_rooms_summary,
]

__all__ = ["ALL_REVIT_TOOLS"]
