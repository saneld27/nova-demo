"""
LangGraph ReAct agent for Revit automation.

Correct execution flow
─────────────────────
1.  Plugin  →  POST /api/v1/chat/stream  (message + session_id)
2.  Backend →  starts agent in background task; opens SSE response
3.  Agent   →  reasons, decides to call a tool
4.  Tool    →  emits  ``tool_call``  event to session queue  (plugin sees it)
              →  awaits Future until plugin responds
5.  Plugin  →  executes the tool in Revit
              →  POST /api/v1/chat/{session_id}/tool_result
6.  Backend →  resolves Future with the result
7.  Tool    →  returns result to agent
8.  Agent   →  continues reasoning; emits ``token`` / ``done`` events
9.  Plugin  →  displays final answer

The backend never touches Revit.  It only orchestrates the LLM and relays
tool calls/results between the agent and the plugin.
"""
from __future__ import annotations

import asyncio
import json
import logging
from collections.abc import AsyncGenerator
from typing import Any

from langchain_core.messages import AIMessageChunk, BaseMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from app.agents.prompts import REVIT_AGENT_SYSTEM_PROMPT
from app.config import Settings
from app.models.schemas import StreamChunk
from app.session import RevitSession, session_manager
from app.tools import ALL_REVIT_TOOLS

logger = logging.getLogger(__name__)


def build_agent(settings: Settings):  # type: ignore[return]
    """Construct and return a LangGraph ReAct agent bound to all Revit tools."""
    llm = ChatOpenAI(
        model=settings.openai_model,
        api_key=settings.openai_api_key,
        streaming=True,
        temperature=0,
    )
    return create_react_agent(model=llm, tools=ALL_REVIT_TOOLS)


def _build_messages(message: str, context: dict[str, Any]) -> list[BaseMessage]:
    messages: list[BaseMessage] = [SystemMessage(content=REVIT_AGENT_SYSTEM_PROMPT)]
    if context:
        messages.append(HumanMessage(content="Current Revit context:\n" + json.dumps(context, indent=2)))
    messages.append(HumanMessage(content=message))
    return messages


async def _run_agent_task(
    session: RevitSession,
    message: str,
    context: dict[str, Any],
    settings: Settings,
) -> None:
    """
    Background task: runs the agent and funnels all events into the session
    SSE queue.  Tools block inside this task waiting for plugin responses.
    """
    agent = build_agent(settings)
    initial_state = {"messages": _build_messages(message, context)}
    # Pass session_id via RunnableConfig so every tool can access the session
    run_config = {"configurable": {"session_id": session.session_id}}

    try:
        async for event in agent.astream_events(initial_state, config=run_config, version="v2"):
            event_name: str = event["event"]
            event_data: dict[str, Any] = event.get("data", {})

            # ── Streaming tokens ────────────────────────────────────────────
            if event_name == "on_chat_model_stream":
                chunk: AIMessageChunk = event_data.get("chunk")  # type: ignore[assignment]
                if chunk and chunk.content:
                    await session.emit(
                        StreamChunk(type="token", content=str(chunk.content)).model_dump(exclude_none=True)
                    )

            # ── Tool returned a result (agent processed it) ─────────────────
            elif event_name == "on_tool_end":
                tool_name = event.get("name", "unknown_tool")
                tool_output = event_data.get("output")
                output_val = tool_output.content if hasattr(tool_output, "content") else str(tool_output)
                await session.emit(
                    StreamChunk(
                        type="tool_result",
                        data={"tool": tool_name, "output": output_val},
                    ).model_dump(exclude_none=True)
                )

            # ── Final answer ────────────────────────────────────────────────
            elif event_name == "on_chain_end" and event.get("name") == "LangGraph":
                output_messages: list[BaseMessage] = (
                    event_data.get("output", {}).get("messages", [])
                )
                if output_messages:
                    final = output_messages[-1]
                    await session.emit(
                        StreamChunk(type="done", content=str(final.content)).model_dump(exclude_none=True)
                    )

    except asyncio.CancelledError:
        logger.info("Agent task cancelled for session %s", session.session_id)
    except Exception as exc:
        logger.exception("Agent error in session %s", session.session_id)
        await session.emit(StreamChunk(type="error", content=str(exc)).model_dump(exclude_none=True))
    finally:
        await session.close()


async def run_agent_stream(
    message: str,
    context: dict[str, Any],
    settings: Settings,
    session_id: str | None = None,
) -> AsyncGenerator[StreamChunk, None]:
    """
    Create (or resume) a session, launch the agent as a background task,
    and yield StreamChunk objects read from the session's SSE queue.
    """
    session = session_manager.get_or_create(session_id)

    # Launch agent concurrently so the SSE generator can drain the queue
    # while the agent is blocked waiting for tool results from the plugin
    asyncio.create_task(
        _run_agent_task(session, message, context, settings),
        name=f"agent-{session.session_id}",
    )

    try:
        while True:
            event = await session.sse_queue.get()
            if event is session.done_sentinel:
                break
            # event is already a dict (model_dump output) – wrap in StreamChunk
            yield StreamChunk(**event)
    finally:
        session_manager.remove(session.session_id)
