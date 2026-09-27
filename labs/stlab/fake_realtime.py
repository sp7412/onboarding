"""An offline simulator of the OpenAI Realtime API (GA event protocol).

It speaks the same JSON events as the real server closely enough to learn the
protocol and to test your client/control-plane code without an API key.
The "model" inside is a small rule-based script, NOT an LLM - it exists so
you can see event sequences, tool calls, preambles, cancellation, and
truncation deterministically.

Simulator-only client event (not part of the real API):
    {"type": "x_sim.user_speech", "text": "...", "duration_ms": 1200}
emulates the caller talking into the mic (VAD start/stop, commit, transcript),
including barge-in if the agent is mid-response.
"""
from __future__ import annotations

import asyncio
import base64
import itertools
import json
import re
import time

_ids = itertools.count(1)
TTFT_MS = {"minimal": 150, "low": 300, "medium": 700, "high": 1400, "xhigh": 2500}
MS_PER_WORD_AUDIO = 320   # simulated speech duration per spoken word
MS_PER_WORD_STREAM = 30   # how fast the "model" streams words (faster than real time, like the real API)


def _id(prefix):
    return f"{prefix}_{next(_ids):04d}"


class FakeRealtime:
    def __init__(self, model: str = "gpt-realtime-2 (simulated)", speed: float = 1.0):
        self.model = model
        self.speed = speed  # >1 runs faster than "real" time
        self.session = {"type": "realtime", "model": model, "instructions": "", "tools": [],
                        "output_modalities": ["text"], "reasoning": {"effort": "low"},
                        "audio": {"input": {"turn_detection": {"type": "server_vad", "create_response": True,
                                                                "interrupt_response": True}}}}
        self.items: list[dict] = []
        self._out: asyncio.Queue = asyncio.Queue()
        self._active: asyncio.Task | None = None
        self._active_id: str | None = None
        self.t0 = time.perf_counter()

    # ------------------------------------------------------------ plumbing
    async def __aenter__(self):
        await self._emit({"type": "session.created", "session": dict(self.session)})
        return self

    async def __aexit__(self, *exc):
        if self._active:
            self._active.cancel()

    async def close(self):
        await self.__aexit__(None, None, None)

    async def _emit(self, ev: dict):
        ev.setdefault("event_id", _id("evt"))
        await self._out.put(ev)

    async def recv(self, timeout: float | None = None) -> dict:
        return await asyncio.wait_for(self._out.get(), timeout)

    def __aiter__(self):
        return self

    async def __anext__(self):
        return await self._out.get()

    async def _sleep(self, ms):
        await asyncio.sleep(ms / 1000 / self.speed)

    # ------------------------------------------------------------ client events
    async def send(self, ev: dict | str):
        if isinstance(ev, str):
            ev = json.loads(ev)
        t = ev.get("type")
        if t == "session.update":
            s = ev.get("session", {})
            for k, v in s.items():
                if isinstance(v, dict) and isinstance(self.session.get(k), dict):
                    self.session[k] = {**self.session[k], **v}
                else:
                    self.session[k] = v
            await self._emit({"type": "session.updated", "session": dict(self.session)})
        elif t == "conversation.item.create":
            item = {"id": _id("item"), **ev["item"]}
            self.items.append(item)
            await self._emit({"type": "conversation.item.added", "item": item})
            await self._emit({"type": "conversation.item.done", "item": item})
        elif t == "response.create":
            await self._start_response(ev.get("response", {}))
        elif t == "response.cancel":
            await self._cancel("client_cancelled")
        elif t == "conversation.item.truncate":
            await self._truncate(ev["item_id"], ev.get("audio_end_ms", 0))
        elif t == "x_sim.user_speech":
            # runs in the background, like a real caller talking while you keep reading events
            self._speech_task = asyncio.create_task(self._user_speech(ev["text"], ev.get("duration_ms", 1000)))
        else:
            await self._emit({"type": "error", "error": {"type": "invalid_request_error",
                              "message": f"Simulator does not support '{t}'"}})

    # ------------------------------------------------------------ behaviours
    async def _user_speech(self, text, duration_ms):
        td = self.session["audio"]["input"].get("turn_detection") or {}
        item_id = _id("item")
        await self._emit({"type": "input_audio_buffer.speech_started", "audio_start_ms": self._now(), "item_id": item_id})
        if self._active and td.get("interrupt_response", True):
            await self._cancel("turn_detected")  # barge-in!
        await self._sleep(duration_ms)
        silence = td.get("silence_duration_ms", 500)
        await self._sleep(silence)  # endpointing: wait for trailing silence
        await self._emit({"type": "input_audio_buffer.speech_stopped", "audio_end_ms": self._now(), "item_id": item_id})
        await self._emit({"type": "input_audio_buffer.committed", "item_id": item_id})
        item = {"id": item_id, "type": "message", "role": "user",
                "content": [{"type": "input_audio", "transcript": text}]}
        self.items.append(item)
        await self._emit({"type": "conversation.item.added", "item": item})
        await self._emit({"type": "conversation.item.input_audio_transcription.completed",
                          "item_id": item_id, "transcript": text})
        if td.get("create_response", True):
            await self._start_response({})

    def _now(self):
        return int((time.perf_counter() - self.t0) * 1000 * self.speed)

    async def _cancel(self, reason):
        if self._active and not self._active.done():
            self._active.cancel()
            try:
                await self._active
            except asyncio.CancelledError:
                pass
            await self._emit({"type": "response.done", "response": {
                "id": self._active_id, "status": "cancelled", "status_details": {"reason": reason}}})
        self._active = None

    async def _truncate(self, item_id, audio_end_ms):
        for it in self.items:
            if it["id"] == item_id:
                words_heard = max(0, int(audio_end_ms // MS_PER_WORD_AUDIO))
                for c in it.get("content", []):
                    if "transcript" in c:
                        c["transcript"] = " ".join(c["transcript"].split()[:words_heard])
                await self._emit({"type": "conversation.item.truncated", "item_id": item_id,
                                  "content_index": 0, "audio_end_ms": audio_end_ms})
                return
        await self._emit({"type": "error", "error": {"message": f"no item {item_id}"}})

    async def _start_response(self, overrides):
        if self._active and not self._active.done():
            await self._emit({"type": "error", "error": {"type": "invalid_request_error",
                              "code": "conversation_already_has_active_response",
                              "message": "Conversation already has an active response in progress."}})
            return
        self._active_id = _id("resp")
        self._active = asyncio.create_task(self._run_response(self._active_id, overrides))

    async def _run_response(self, rid, overrides):
        await self._emit({"type": "response.created", "response": {"id": rid, "status": "in_progress"}})
        effort = (self.session.get("reasoning") or {}).get("effort", "low")
        await self._sleep(TTFT_MS.get(effort, 300))
        plan = brain(self.items, self.session, overrides)
        outputs, out_tokens = [], 0
        audio = "audio" in overrides.get("output_modalities", self.session.get("output_modalities", ["text"]))
        for step in plan:
            if step["kind"] == "say":
                item = await self._stream_message(rid, step["text"], audio)
                outputs.append(item)
                out_tokens += len(step["text"].split())
            else:
                item = await self._stream_call(rid, step["name"], step["args"])
                outputs.append(item)
                out_tokens += 12
        await self._emit({"type": "response.done", "response": {
            "id": rid, "status": "completed", "output": outputs,
            "usage": {"input_tokens": 40 * len(self.items), "output_tokens": out_tokens}}})
        self._active = None

    async def _stream_message(self, rid, text, audio):
        item = {"id": _id("item"), "type": "message", "role": "assistant", "status": "in_progress", "content": []}
        self.items.append(item)
        await self._emit({"type": "response.output_item.added", "response_id": rid, "item": dict(item)})
        await self._emit({"type": "conversation.item.added", "item": dict(item)})
        dtype = "response.output_audio_transcript.delta" if audio else "response.output_text.delta"
        said = []
        key = "transcript" if audio else "text"
        item["content"] = [{"type": "output_audio" if audio else "output_text", key: ""}]
        item["status"] = "incomplete"   # stays incomplete if we get cancelled mid-stream
        for w in text.split():
            said.append(w)
            item["content"][0][key] = " ".join(said)
            await self._emit({"type": dtype, "response_id": rid, "item_id": item["id"], "delta": w + " "})
            if audio:
                chunk = base64.b64encode(b"\x00\x00" * 8).decode()  # placeholder PCM
                await self._emit({"type": "response.output_audio.delta", "response_id": rid, "item_id": item["id"],
                                  "delta": chunk, "x_sim_audio_ms": MS_PER_WORD_AUDIO})
            await self._sleep(MS_PER_WORD_STREAM)
        item["content"][0][key] = text
        item["status"] = "completed"
        done = "response.output_audio_transcript.done" if audio else "response.output_text.done"
        await self._emit({"type": done, "response_id": rid, "item_id": item["id"], key: text})
        await self._emit({"type": "response.output_item.done", "response_id": rid, "item": dict(item)})
        return item

    async def _stream_call(self, rid, name, args):
        call_id = _id("call")
        item = {"id": _id("item"), "type": "function_call", "name": name, "call_id": call_id, "arguments": ""}
        self.items.append(item)
        await self._emit({"type": "response.output_item.added", "response_id": rid, "item": dict(item)})
        argstr = json.dumps(args)
        for i in range(0, len(argstr), 12):
            await self._emit({"type": "response.function_call_arguments.delta", "response_id": rid,
                              "item_id": item["id"], "call_id": call_id, "delta": argstr[i:i + 12]})
            await self._sleep(5)
        item["arguments"] = argstr
        await self._emit({"type": "response.function_call_arguments.done", "response_id": rid, "item_id": item["id"],
                          "call_id": call_id, "name": name, "arguments": argstr})
        await self._emit({"type": "response.output_item.done", "response_id": rid, "item": dict(item)})
        return item


# ---------------------------------------------------------------- the "model"
JOB_WORDS = [("water heater", "water_heater"), ("hot water", "water_heater"), ("leak", "leak_repair"),
             ("tune", "hvac_tuneup"), ("maintenance", "hvac_tuneup"), ("furnace", "furnace_repair"),
             ("heat", "furnace_repair"), ("a/c", "ac_repair"), ("ac ", "ac_repair"), ("air", "ac_repair"),
             ("cool", "ac_repair")]
EMERGENCY = ["gas", "carbon monoxide", "sparks", "smoke", "flooding", "burst"]


def _text_of(item):
    out = []
    for c in item.get("content", []):
        out.append(c.get("text") or c.get("transcript") or "")
    return " ".join(out).strip()


def _fmt_slot(s):
    h = int(s["start"][:2])
    ampm = f"{h if h <= 12 else h - 12}{'am' if h < 12 else 'pm'}"
    return f"{s['weekday']} {s['date'][5:]} at {ampm} with {s['tech']}"


def brain(items, session, overrides):
    """Return a list of steps: {"kind": "say", "text"} or {"kind": "call", "name", "args"}."""
    tools = {t["name"] for t in (overrides.get("tools") if "tools" in overrides else session.get("tools") or [])}
    instr = overrides.get("instructions") or session.get("instructions", "")
    # out-of-band "say this" responses (used for filler while a tool runs)
    if instr.startswith("Say exactly:"):
        return [{"kind": "say", "text": instr.split(":", 1)[1].strip()}]
    if "advance_booking" in tools:
        return _workflow_brain(items)
    # gather memory from the conversation (the model "reads" its context)
    outputs = {}
    calls = {i["call_id"]: i for i in items if i.get("type") == "function_call"}
    for i in items:
        if i.get("type") == "function_call_output":
            name = calls.get(i["call_id"], {}).get("name")
            try:
                outputs[name] = json.loads(i["output"])
            except Exception:
                outputs[name] = {"raw": i["output"]}
    customer = (outputs.get("lookup_customer") or {}).get("customer")
    slots = (outputs.get("find_slots") or {}).get("slots") or []
    last = items[-1] if items else {}
    user_texts = [_text_of(i) for i in items if i.get("role") == "user"]
    alltext = " ".join(user_texts).lower()

    # 1) react to a tool result
    if last.get("type") == "function_call_output":
        name = calls.get(last["call_id"], {}).get("name")
        out = outputs.get(name, {})
        if not out.get("ok", True):
            err = out.get("error")
            if err == "address_not_confirmed" and customer:
                return [{"kind": "say", "text": f"Before I lock that in, can you confirm the service address is {customer['address']}?"}]
            if err == "emergency_escalation_required" and "transfer_to_human" in tools:
                return [{"kind": "call", "name": "transfer_to_human", "args": {"reason": "possible emergency"}}]
            return [{"kind": "say", "text": f"Sorry, I hit a problem: {out.get('message', err)} Let me get someone to help."}]
        if name == "lookup_customer":
            if customer:
                job = next((j for w, j in JOB_WORDS if w in alltext + " "), None)
                if job and "find_slots" in tools:
                    return [{"kind": "say", "text": f"Thanks {customer['name'].split()[0]}. Let me check the schedule."},
                            {"kind": "call", "name": "find_slots", "args": {"job_type": job, "zip_code": customer["zip"]}}]
                return [{"kind": "say", "text": f"Hi {customer['name'].split()[0]}, I have you at {customer['address']}. What's going on with your system today?"}]
            return [{"kind": "say", "text": "I don't see an account for that number. What's the service address?"}]
        if name == "find_slots":
            if not slots:
                return [{"kind": "say", "text": "I don't have anything open soon. Let me connect you with the office."}]
            opts = "; or ".join(_fmt_slot(s) for s in slots[:2])
            return [{"kind": "say", "text": f"I can do {opts}. Which works best?"}]
        if name == "record_address_confirmation":
            return [{"kind": "say", "text": "Great, address confirmed."}]
        if name == "create_job":
            j = out["job"]
            return [{"kind": "say", "text": f"You're all set: {j['date']} between {j['window']} with {j['tech']}. Your job number is {j['id']}."}]
        if name == "transfer_to_human":
            return [{"kind": "say", "text": "Connecting you to a team member now. Please stay on the line."}]
        return [{"kind": "say", "text": "Done."}]

    # 2) react to the caller
    said = _text_of(last).lower() if last.get("role") == "user" else ""
    if any(w in said for w in EMERGENCY) and "transfer_to_human" in tools:
        return [{"kind": "say", "text": "If you smell gas, please leave the house now and call 911 from outside. I'm getting a technician on the line."},
                {"kind": "call", "name": "transfer_to_human", "args": {"reason": "possible gas leak"}}]
    if any(w in said for w in ("human", "person", "representative", "operator")) and "transfer_to_human" in tools:
        return [{"kind": "call", "name": "transfer_to_human", "args": {"reason": "caller requested a human"}}]
    phone = re.search(r"(\+?1?[\s\-.(]*\d{3}[\s\-.)]*\d{3}[\s\-.]*\d{4})", said) or \
        (None if customer else re.search(r"caller id[:\s]+(\+?\d{10,11})", instr.lower()))
    if phone and not customer and "lookup_customer" in tools:
        return [{"kind": "call", "name": "lookup_customer", "args": {"phone": phone.group(1)}}]
    if slots and any(w in said for w in ("yes", "yeah", "works", "first", "second", "correct", "sure", "that one")):
        idx = 1 if "second" in said else 0
        steps = []
        addr_ok = (outputs.get("record_address_confirmation") or {}).get("ok")
        if not addr_ok and "record_address_confirmation" in tools and any(w in said for w in ("yes", "correct", "yeah")):
            steps.append({"kind": "call", "name": "record_address_confirmation", "args": {"caller_said": said.split(",")[0].strip()}})
        prev = [json.loads(i["arguments"]) for i in items if i.get("type") == "function_call"
                and i.get("name") == "create_job" and i.get("arguments")]
        slot_id = prev[-1]["slot_id"] if prev and not any(w in said for w in ("first", "second")) else slots[idx]["id"]
        if customer and "create_job" in tools:
            job = next((j for w, j in JOB_WORDS if w in alltext + " "), "ac_repair")
            steps.append({"kind": "call", "name": "create_job", "args": {
                "customer_id": customer["id"], "slot_id": slot_id, "job_type": job,
                "summary": user_texts[0][:80] if user_texts else "service call"}})
        return steps or [{"kind": "say", "text": "Great."}]
    job = next((j for w, j in JOB_WORDS if w in said + " "), None)
    if job and customer and "find_slots" in tools:
        return [{"kind": "say", "text": "Got it. One moment while I check availability."},
                {"kind": "call", "name": "find_slots", "args": {"job_type": job, "zip_code": customer["zip"]}}]
    if job and not customer:
        return [{"kind": "say", "text": "I can help with that. What's the phone number on the account?"}]
    if not said:
        return [{"kind": "say", "text": "Thanks for calling Benbrook Comfort Services, this is the virtual assistant. How can I help?"}]
    return [{"kind": "say", "text": "Got it. Can you tell me a bit more about what's happening with the system?"}]


def _paraphrase(text: str) -> str:
    """What a model might pass as a tool argument instead of the caller's verbatim words."""
    t = text.lower()
    if re.search(r"\b(yes|yeah|yep|correct|right)\b", t) and "address" not in t and len(t.split()) <= 5:
        return "The caller confirmed."
    if "first" in t:
        return "Caller picked the first option."
    if "second" in t:
        return "Caller picked the second option."
    return text


def _workflow_brain(items):
    """Talker mode: forward every caller turn to advance_booking and speak what it returns."""
    last = items[-1] if items else {}
    calls = {i["call_id"]: i for i in items if i.get("type") == "function_call"}
    if last.get("type") == "function_call_output":
        try:
            out = json.loads(last["output"])
        except Exception:
            out = {}
        if out.get("ok") is False:
            return [{"kind": "say", "text": "Sorry, something went wrong on my end. Let me get a team member."}]
        return [{"kind": "say", "text": out.get("say") or "Okay."}]
    said = _text_of(last) if last.get("role") == "user" else ""
    return [{"kind": "call", "name": "advance_booking", "args": {"caller_said": _paraphrase(said)}}]
