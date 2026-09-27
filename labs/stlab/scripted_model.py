"""A scripted LangChain chat model so create_agent tutorials run with no API key.

It is NOT smart: a small rule-based policy looks at the message history and
emits tool calls / replies. Swap in `init_chat_model("openai:...")` for real use.
"""
from __future__ import annotations

import json
import re
import uuid
from typing import Any

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, ToolMessage
from langchain_core.outputs import ChatGeneration, ChatResult

JOB_WORDS = [("water heater", "water_heater"), ("leak", "leak_repair"), ("tune", "hvac_tuneup"),
             ("furnace", "furnace_repair"), ("heat", "furnace_repair"), ("ac", "ac_repair"),
             ("air", "ac_repair"), ("cool", "ac_repair")]


def _call(name, args):
    return AIMessage(content="", tool_calls=[{"name": name, "args": args, "id": "call_" + uuid.uuid4().hex[:8]}])


def booking_policy(messages: list[BaseMessage], tool_names: set[str]) -> AIMessage:
    humans = [m for m in messages if isinstance(m, HumanMessage)]
    text = " ".join(str(m.content) for m in humans).lower()
    last_h = str(humans[-1].content).lower() if humans else ""
    results = {}
    for m in messages:
        if isinstance(m, ToolMessage):
            try:
                results[m.name] = json.loads(m.content) if isinstance(m.content, str) else m.content
            except Exception:
                results[m.name] = {"raw": m.content}
    last = messages[-1]
    job = next((j for w, j in JOB_WORDS if re.search(rf"\b{w}", text)), None)
    cust = (results.get("lookup_customer") or {}).get("customer")
    slots = (results.get("find_slots") or {}).get("slots")

    if isinstance(last, ToolMessage):
        r = results.get(last.name, {})
        if isinstance(r, dict) and r.get("ok") is False:
            return AIMessage(content=f"I couldn't do that: {r.get('message')}")
        if last.name == "create_job":
            j = r["job"]
            return AIMessage(content=f"Booked! {j['date']} {j['window']} with {j['tech']} (job {j['id']}).")
    if "human" in last_h and "transfer_to_human" in tool_names:
        return _call("transfer_to_human", {"reason": "caller asked"})
    if not cust and "lookup_customer" in tool_names and "lookup_customer" not in results:
        m = re.search(r"(\d{3}\D?\d{3}\D?\d{4})", text)
        if m:
            return _call("lookup_customer", {"phone": m.group(1)})
        return AIMessage(content="What's the phone number on the account?")
    if cust and job and not slots and "find_slots" in tool_names:
        return _call("find_slots", {"job_type": job, "zip_code": cust["zip"]})
    if slots and any(w in last_h for w in ("yes", "book", "first", "works")) and "create_job" in tool_names \
            and not isinstance(last, ToolMessage):
        return _call("create_job", {"customer_id": cust["id"], "slot_id": slots[0]["id"], "job_type": job,
                                    "summary": str(humans[0].content)[:80]})
    if slots:
        s = slots[0]
        return AIMessage(content=f"The earliest opening is {s['weekday']} {s['date']} {s['start']} with {s['tech']}. Shall I book it?")
    if cust:
        return AIMessage(content=f"Hi {cust['name'].split()[0]}! What's going on with your system?")
    return AIMessage(content="How can I help?")


class ScriptedChatModel(BaseChatModel):
    policy: Any = booking_policy
    tool_names: set = set()

    @property
    def _llm_type(self) -> str:
        return "scripted"

    def bind_tools(self, tools, **kwargs):
        names = set()
        for t in tools:
            names.add(getattr(t, "name", None) or (t.get("name") if isinstance(t, dict) else getattr(t, "__name__", "")))
        return self.model_copy(update={"tool_names": names})

    def _generate(self, messages, stop=None, run_manager=None, **kwargs) -> ChatResult:
        msg = self.policy(messages, self.tool_names)
        return ChatResult(generations=[ChatGeneration(message=msg)])
