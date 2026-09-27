"""A minimal Realtime "tool loop": the piece of the control plane that sits
between the model and your backend. Same code works live or simulated."""
from __future__ import annotations

import asyncio
import json

from .tools import CallState, execute_tool


async def run_until_idle(conn, state: CallState, on_event=print, *, enforce: bool = True,
                         idle_timeout: float = 20.0, max_tool_rounds: int = 6) -> list[dict]:
    """Consume events until a response finishes with no pending tool calls.

    Returns the list of all events seen. Tool calls are executed through
    `execute_tool` (policy layer), and their outputs are sent back followed by
    a new `response.create`, exactly like a production loop would.
    """
    seen, rounds = [], 0
    while True:
        ev = await conn.recv(timeout=idle_timeout)
        seen.append(ev)
        on_event(ev)
        typ = ev.get("type")
        if typ == "conversation.item.input_audio_transcription.completed":
            state.last_user_text = ev.get("transcript", "")
        if typ == "error":
            continue
        if typ != "response.done":
            continue
        resp = ev["response"]
        if resp.get("status") != "completed":
            # cancelled (barge-in) or failed; caller's next turn will drive things
            return seen
        calls = [o for o in resp.get("output", []) if o.get("type") == "function_call"]
        if not calls:
            return seen
        rounds += 1
        if rounds > max_tool_rounds:
            raise RuntimeError("Too many tool rounds - possible loop")
        for c in calls:  # execute sequentially, in the order the model emitted them
            result = await asyncio.to_thread(execute_tool, c["name"], c["arguments"], state, enforce=enforce)
            await conn.send({"type": "conversation.item.create", "item": {
                "type": "function_call_output", "call_id": c["call_id"], "output": json.dumps(result)}})
        await conn.send({"type": "response.create"})


async def user_says(conn, state: CallState, text: str, *, typed: bool = True, **kw):
    """Send a caller turn (typed text, or simulated speech on the fake server) and run to idle."""
    state.last_user_text = text
    if typed:
        await conn.send({"type": "conversation.item.create", "item": {
            "type": "message", "role": "user", "content": [{"type": "input_text", "text": text}]}})
        await conn.send({"type": "response.create"})
    else:
        await conn.send({"type": "x_sim.user_speech", "text": text, "duration_ms": 300 * len(text.split())})
    return await run_until_idle(conn, state, **kw)
