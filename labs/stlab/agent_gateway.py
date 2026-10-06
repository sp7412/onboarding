"""A booking API for *other companies' AI agents* (teaching model, lab 12).

When a homeowner's assistant books a visit, there's no human caller on the line, so the
gateway has to establish everything the phone flow got from people and the transport:
who the client is (authentication), what it may do (scopes), that the request wasn't
altered or replayed (signatures, timestamps, nonces), that retries don't double-book
(idempotency), that slots were really offered (quotes), and that free-text fields can't
change behavior (untrusted content). It also must not leak whether a phone number is a
customer (enumeration).

Generic pattern, not any company's API. Uses the mock backend in `backend.py`.
"""
from __future__ import annotations

import hashlib
import hmac
import json
import secrets
from dataclasses import dataclass, field

from . import backend as be

REPLAY_WINDOW_S = 300
QUOTE_TTL_S = 600


def sign(secret: str, method: str, path: str, ts: int, nonce: str, body: dict) -> str:
    """HMAC-SHA256 over a canonical string. Clients and the gateway compute the same thing."""
    canonical = "\n".join([method, path, str(ts), nonce, json.dumps(body, sort_keys=True, separators=(",", ":"))])
    return hmac.new(secret.encode(), canonical.encode(), hashlib.sha256).hexdigest()


@dataclass
class Client:
    client_id: str
    secret: str
    scopes: set[str]
    rate_per_minute: int = 30


@dataclass
class Request:
    client_id: str
    method: str
    path: str
    ts: int
    nonce: str
    body: dict
    signature: str
    idempotency_key: str | None = None


@dataclass
class Gateway:
    clients: dict[str, Client] = field(default_factory=dict)
    now: int = 1_800_000_000                      # fixed clock for deterministic labs
    seen_nonces: set[tuple[str, str]] = field(default_factory=set)
    idem: dict[tuple[str, str], tuple[str, dict]] = field(default_factory=dict)
    quotes: dict[str, dict] = field(default_factory=dict)
    calls: dict[tuple[str, int], int] = field(default_factory=dict)
    bookings: dict[str, dict] = field(default_factory=dict)
    audit: list[dict] = field(default_factory=list)

    def register(self, client_id: str, scopes: set[str], rate_per_minute: int = 30) -> Client:
        c = Client(client_id, secrets.token_hex(16), set(scopes), rate_per_minute)
        self.clients[client_id] = c
        return c

    # ---- the pipeline ------------------------------------------------------------------
    def handle(self, req: Request) -> tuple[int, dict]:
        status, resp = self._handle(req)
        self.audit.append({"client": req.client_id, "path": req.path, "status": status,
                           "error": resp.get("error")})
        return status, resp

    def _handle(self, req: Request) -> tuple[int, dict]:
        client = self.clients.get(req.client_id)
        if client is None:
            return 401, {"error": "unknown_client"}
        expected = sign(client.secret, req.method, req.path, req.ts, req.nonce, req.body)
        if not hmac.compare_digest(expected, req.signature):
            return 401, {"error": "bad_signature"}
        if abs(self.now - req.ts) > REPLAY_WINDOW_S:
            return 401, {"error": "stale_request"}
        # idempotent retries are answered before nonce checks, so a safe retry with the same
        # key (and a fresh nonce) returns the original result
        if req.idempotency_key:
            prior = self.idem.get((client.client_id, req.idempotency_key))
            if prior:
                body_hash, resp = prior
                if body_hash != _hash(req.body):
                    return 409, {"error": "idempotency_key_reused_with_different_body"}
                return 200, {**resp, "replayed": True}
        if (client.client_id, req.nonce) in self.seen_nonces:
            return 401, {"error": "replayed_nonce"}
        self.seen_nonces.add((client.client_id, req.nonce))
        minute = (client.client_id, self.now // 60)
        self.calls[minute] = self.calls.get(minute, 0) + 1
        if self.calls[minute] > client.rate_per_minute:
            return 429, {"error": "rate_limited"}

        route = {("POST", "/availability"): ("availability:read", self._availability),
                 ("POST", "/bookings"): ("booking:create", self._book)}.get((req.method, req.path))
        if route is None:
            return 404, {"error": "no_such_endpoint"}
        scope, fn = route
        if scope not in client.scopes:
            return 403, {"error": "missing_scope", "needs": scope}
        status, resp = fn(client, req.body)
        if req.idempotency_key and status == 200:
            self.idem[(client.client_id, req.idempotency_key)] = (_hash(req.body), resp)
        return status, resp

    # ---- endpoints ---------------------------------------------------------------------
    def _availability(self, client: Client, body: dict) -> tuple[int, dict]:
        job_type, zip_code = body.get("job_type"), body.get("zip_code")
        if job_type not in be.JOB_TYPES or not isinstance(zip_code, str):
            return 400, {"error": "invalid_request"}
        try:
            slots = be.find_slots(job_type, zip_code)
        except be.PolicyError as e:
            return 422, {"error": e.code}
        quote_id = "Q-" + secrets.token_hex(4)
        self.quotes[quote_id] = {"client": client.client_id, "job_type": job_type, "zip_code": zip_code,
                                 "slot_ids": [s["id"] for s in slots], "expires": self.now + QUOTE_TTL_S}
        # windows only: no technician names, no customer data
        return 200, {"quote_id": quote_id,
                     "windows": [{"slot_id": s["id"], "date": s["date"], "window": f"{s['start']}-{s['end']}"} for s in slots]}

    def _book(self, client: Client, body: dict) -> tuple[int, dict]:
        quote = self.quotes.get(body.get("quote_id", ""))
        if quote is None or quote["client"] != client.client_id:
            return 422, {"error": "unknown_quote"}
        if self.now > quote["expires"]:
            return 422, {"error": "quote_expired"}
        if body.get("slot_id") not in quote["slot_ids"]:
            return 422, {"error": "slot_not_quoted"}
        contact = body.get("homeowner", {})
        if not contact.get("name") or not contact.get("phone"):
            return 400, {"error": "invalid_request"}
        booking_id = "B-" + secrets.token_hex(4)
        # Every agent-made booking waits for the homeowner to confirm by text. The response is
        # the same whether or not the phone matches an existing customer (no enumeration).
        self.bookings[booking_id] = {
            "client": client.client_id, "slot_id": body["slot_id"], "job_type": quote["job_type"],
            "contact": contact, "zip_code": quote["zip_code"], "status": "pending_homeowner_confirmation",
            "notes_untrusted": str(body.get("notes", ""))[:500],
        }
        return 200, {"booking_id": booking_id, "status": "pending_homeowner_confirmation"}

    def homeowner_confirms(self, booking_id: str, code_ok: bool) -> dict:
        """The homeowner replies to a confirmation text. Only then is the job created."""
        b = self.bookings[booking_id]
        if b["status"] != "pending_homeowner_confirmation":
            return b
        if not code_ok:
            b["status"] = "declined"
            return b
        customer_id = be.register_external_contact(b["contact"]["name"], b["contact"]["phone"], b["zip_code"])
        try:
            job = be.create_job(customer_id=customer_id, slot_id=b["slot_id"], job_type=b["job_type"],
                                summary="Booked by an external assistant; see untrusted notes",
                                idempotency_key=booking_id)
        except be.PolicyError as e:
            b["status"] = "slot_taken" if e.code == "slot_unavailable" else f"failed:{e.code}"
            return b
        b["status"], b["job_id"] = "confirmed", job["id"]
        return b


def _hash(body: dict) -> str:
    return hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest()


def make_request(client: Client, method: str, path: str, body: dict, ts: int,
                 nonce: str | None = None, idempotency_key: str | None = None) -> Request:
    nonce = nonce or secrets.token_hex(8)
    return Request(client.client_id, method, path, ts, nonce, body,
                   sign(client.secret, method, path, ts, nonce, body), idempotency_key)
