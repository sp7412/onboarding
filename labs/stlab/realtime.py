"""Connect to the real Realtime API or the offline simulator with one interface.

    conn = await connect(live=None)   # None = live if OPENAI_API_KEY is set
    await conn.send({...}); ev = await conn.recv(); async for ev in conn: ...
"""
from __future__ import annotations

import json
import os
import time

from .fake_realtime import FakeRealtime

REALTIME_URL = "wss://api.openai.com/v1/realtime?model={model}"


class LiveRealtime:
    """Thin JSON wrapper around a websocket to the OpenAI Realtime API."""

    def __init__(self, model: str):
        self.model = model
        self.ws = None

    async def __aenter__(self):
        import websockets  # pip install websockets
        self.ws = await websockets.connect(
            REALTIME_URL.format(model=self.model),
            additional_headers={"Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}"},
            max_size=None,
        )
        return self

    async def __aexit__(self, *exc):
        if self.ws:
            await self.ws.close()

    async def close(self):
        await self.__aexit__(None, None, None)

    async def send(self, ev: dict):
        await self.ws.send(json.dumps(ev))

    async def recv(self, timeout: float | None = None) -> dict:
        import asyncio
        return json.loads(await asyncio.wait_for(self.ws.recv(), timeout))

    def __aiter__(self):
        return self

    async def __anext__(self):
        return json.loads(await self.ws.recv())


async def connect(live: bool | None = None, model: str = "gpt-realtime-2", speed: float = 1.0):
    if live is None:
        live = bool(os.environ.get("OPENAI_API_KEY"))
    conn = LiveRealtime(model) if live else FakeRealtime(speed=speed)
    await conn.__aenter__()
    conn.is_live = live
    return conn


class EventPrinter:
    """Compact, timestamped event log. Collapses streaming deltas into one line."""

    QUIET = {"response.output_audio.delta", "response.function_call_arguments.delta", "rate_limits.updated",
             "response.content_part.added", "response.content_part.done", "conversation.item.done"}

    def __init__(self, show_quiet: bool = False):
        self.t0 = time.perf_counter()
        self.show_quiet = show_quiet
        self._delta_open = False
        self.events: list[tuple[float, dict]] = []

    def __call__(self, ev: dict):
        t = (time.perf_counter() - self.t0) * 1000
        self.events.append((t, ev))
        typ = ev.get("type", "?")
        if typ.endswith("text.delta") or typ.endswith("transcript.delta"):
            if not self._delta_open:
                print(f"{t:8.0f} ms  {typ:<44} ", end="")
                self._delta_open = True
            print(ev.get("delta", ""), end="", flush=True)
            return
        if self._delta_open:
            print()
            self._delta_open = False
        if typ in self.QUIET and not self.show_quiet:
            return
        print(f"{t:8.0f} ms  {typ:<44} {self._detail(ev)}")

    @staticmethod
    def _detail(ev):
        typ = ev.get("type", "")
        if typ == "response.function_call_arguments.done":
            return f"{ev.get('name')}({ev.get('arguments')})  call_id={ev.get('call_id')}"
        if typ == "response.done":
            r = ev.get("response", {})
            return f"status={r.get('status')} {r.get('status_details') or ''}"
        if typ == "conversation.item.added":
            it = ev.get("item", {})
            return f"{it.get('type')}/{it.get('role', it.get('name', ''))} id={it.get('id')}"
        if typ == "conversation.item.input_audio_transcription.completed":
            return repr(ev.get("transcript"))
        if typ == "error":
            return str(ev.get("error", {}).get("message"))
        return ""

    def first(self, typ: str, after_ms: float = 0.0):
        return next((t for t, e in self.events if e.get("type") == typ and t >= after_ms), None)
