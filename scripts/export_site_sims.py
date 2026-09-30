"""Export deterministic guardrail-simulator traces for the site.

Runs every scenario in labs/stlab/scenarios.py through the offline Realtime
simulator twice (control plane on and off) and writes the transcript, tool calls
and outcomes to site/src/data/guardrail-traces.json. Re-run after changing the
simulator, tools or scenarios:

    python scripts/export_site_sims.py
"""
from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "labs"))

from stlab import backend as be  # noqa: E402
from stlab.realtime import connect  # noqa: E402
from stlab.scenarios import SCENARIOS  # noqa: E402
from stlab.tools import TOOL_SCHEMAS, CallState, execute_tool  # noqa: E402

OUT = ROOT / "site" / "src" / "data" / "guardrail-traces.json"


async def run(scn: dict, enforce: bool) -> dict:
    be.reset()
    be.LATENCY_MS.update({k: 0 for k in be.LATENCY_MS})
    conn = await connect(live=False, speed=200)
    await conn.recv(timeout=10)
    caller_id = scn["inputs"]["caller_id"]
    await conn.send({"type": "session.update", "session": {
        "type": "realtime", "tools": TOOL_SCHEMAS, "instructions": f"Caller ID: {caller_id}"}})
    state = CallState(call_id=f"site-{scn['id']}")
    steps: list[dict] = []

    async def turn(text: str | None):
        if text:
            steps.append({"kind": "caller", "text": text})
            state.last_user_text = text
            if enforce and be.detect_emergency(text):
                state.emergency = True
                steps.append({"kind": "policy", "text": "Emergency language detected: only transfer_to_human is allowed now."})
            await conn.send({"type": "conversation.item.create", "item": {
                "type": "message", "role": "user", "content": [{"type": "input_text", "text": text}]}})
        await conn.send({"type": "response.create"})
        for _ in range(8):
            while True:
                ev = await conn.recv(timeout=20)
                if ev["type"] == "response.done":
                    break
            resp = ev["response"]
            for o in resp.get("output", []):
                if o.get("type") == "message":
                    said = " ".join(c.get("text") or c.get("transcript") or "" for c in o.get("content", []))
                    if said.strip():
                        steps.append({"kind": "agent", "text": said.strip()})
            calls = [o for o in resp.get("output", []) if o.get("type") == "function_call"]
            if not calls:
                return
            for c in calls:
                result = execute_tool(c["name"], c["arguments"], state, enforce=enforce)
                steps.append({"kind": "tool", "name": c["name"], "args": json.loads(c["arguments"] or "{}"),
                              "ok": bool(result.get("ok", True)), "error": result.get("error"),
                              "message": result.get("message")})
                await conn.send({"type": "conversation.item.create", "item": {
                    "type": "function_call_output", "call_id": c["call_id"], "output": json.dumps(result)}})
            await conn.send({"type": "response.create"})

    await turn(None)
    for u in scn["inputs"]["utterances"]:
        await turn(u)
    await conn.close()
    actions = [c["action"] for c in state.changes]
    outcome = ("rescheduled" if "rescheduled" in actions else "cancelled" if "cancelled" in actions
               else "booked" if state.booked_job else
               ("emergency_transfer" if state.transferred and (state.emergency or any(
                   "gas" in json.dumps(s.get("args", {})) or "smoke" in json.dumps(s.get("args", {}))
                   for s in steps if s.get("name") == "transfer_to_human")) else
                "transfer" if state.transferred else "no_booking"))
    return {"steps": steps, "outcome": outcome, "address_confirmed": state.address_confirmed}


async def main():
    data = []
    for scn in SCENARIOS:
        data.append({"id": scn["id"], "caller_id": scn["inputs"]["caller_id"],
                     "expected": scn["outputs"]["outcome"],
                     "guarded": await run(scn, True), "unguarded": await run(scn, False)})
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=1) + "\n")
    print(f"wrote {len(data)} scenarios to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    asyncio.run(main())
