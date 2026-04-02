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
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

from app.agents.prompts import REVIT_AGENT_SYSTEM_PROMPT
from app.config import Settings
from app.models.schemas import StreamChunk
from app.session import RevitSession, session_manager
from app.tools import select_tools

logger = logging.getLogger(__name__)

# ── Conversation memory (in-process, survives across turns for the same thread_id)
# Swap this for AsyncSqliteSaver / AsyncPostgresSaver for cross-restart persistence.
_checkpointer = MemorySaver()


def build_agent(settings: Settings, message: str = ""):  # type: ignore[return]
    """
    Construct and return a LangGraph ReAct agent bound to a context-aware
    subset of Revit tools.

    ``message`` is used by :func:`~app.tools.select_tools` to pick the most
    relevant tools for the current turn while staying under the OpenAI 128-tool
    limit.  The MemorySaver checkpointer is keyed by ``thread_id``
    (== session_id from the plugin) so conversation history is preserved across
    turns even though the agent is rebuilt each turn.
    """
    tools = select_tools(message)
    logger.debug("Tool selection: %d tools selected for message_preview=%r", len(tools), message[:120])
    llm = ChatOpenAI(
        model=settings.openai_model,
        api_key=settings.openai_api_key,
        streaming=True,
        temperature=0,
    )
    return create_react_agent(
        model=llm,
        tools=tools,
        checkpointer=_checkpointer,
        prompt=SystemMessage(content=REVIT_AGENT_SYSTEM_PROMPT),
    )


def _build_messages(message: str, context: dict[str, Any]) -> list[BaseMessage]:
    """Build only the NEW turn's messages – the checkpointer supplies prior history."""
    messages: list[BaseMessage] = []
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
    agent = build_agent(settings, message)
    initial_state = {"messages": _build_messages(message, context)}
    # thread_id  → LangGraph checkpointer key (conversation memory)
    # session_id → custom key so tools can look up the active RevitSession
    run_config = {"configurable": {"thread_id": session.session_id, "session_id": session.session_id}}

    logger.info("Agent task started session=%s message_preview=%r", session.session_id, message[:120])
    tool_call_count = 0

    try:
        async for event in agent.astream_events(initial_state, config=run_config, version="v2"):
            event_name: str = event["event"]
            event_data: dict[str, Any] = event.get("data", {})

            # ── LLM decides to call a tool ──────────────────────────────────
            if event_name == "on_tool_start":
                tool_call_count += 1
                tool_input = event_data.get("input", {})
                logger.info(
                    "Tool call #%d session=%s tool=%s input=%r",
                    tool_call_count,
                    session.session_id,
                    event.get("name", "unknown"),
                    str(tool_input)[:300],
                )

            # ── Streaming tokens ────────────────────────────────────────────
            elif event_name == "on_chat_model_stream":
                chunk: AIMessageChunk = event_data.get("chunk")  # type: ignore[assignment]
                if chunk and chunk.content:
                    logger.debug("Token session=%s content=%r", session.session_id, str(chunk.content)[:80])
                    await session.emit(
                        StreamChunk(type="token", content=str(chunk.content)).model_dump(exclude_none=True)
                    )

            # ── Tool returned a result (agent processed it) ─────────────────
            elif event_name == "on_tool_end":
                tool_name = event.get("name", "unknown_tool")
                tool_output = event_data.get("output")
                output_val = tool_output.content if hasattr(tool_output, "content") else str(tool_output)
                logger.info(
                    "Tool result session=%s tool=%s output_preview=%r",
                    session.session_id,
                    tool_name,
                    output_val[:300] if isinstance(output_val, str) else str(output_val)[:300],
                )
                await session.emit(
                    StreamChunk(
                        type="tool_result",
                        data={"tool": tool_name, "output": output_val},
                    ).model_dump(exclude_none=True)
                )

            # ── LLM generates a new reasoning step ─────────────────────────
            elif event_name == "on_chat_model_start":
                logger.debug("LLM invocation session=%s", session.session_id)

            # ── Final answer ────────────────────────────────────────────────
            elif event_name == "on_chain_end" and event.get("name") == "LangGraph":
                output_messages: list[BaseMessage] = (
                    event_data.get("output", {}).get("messages", [])
                )
                if output_messages:
                    final = output_messages[-1]
                    logger.info(
                        "Agent done session=%s tool_calls=%d answer_preview=%r",
                        session.session_id,
                        tool_call_count,
                        str(final.content)[:200],
                    )
                    await session.emit(
                        StreamChunk(type="done", content=str(final.content)).model_dump(exclude_none=True)
                    )

    except asyncio.CancelledError:
        logger.info("Agent task cancelled session=%s", session.session_id)
    except Exception as exc:
        logger.exception("Agent error session=%s", session.session_id)
        await session.emit(StreamChunk(type="error", content=str(exc)).model_dump(exclude_none=True))
    finally:
        logger.info("Agent task finished session=%s tool_calls=%d", session.session_id, tool_call_count)
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
