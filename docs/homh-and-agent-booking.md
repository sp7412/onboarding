# Homh and AI-Agent Booking

**Facts as of: October 6, 2026 · Last reviewed: October 6, 2026**

Public sources only. At Pantheon 2026, ServiceTitan announced **Homh**, a consumer demand
generation platform that makes selected contractors discoverable and bookable where
homeowners—or their AI agents—are searching. Homh was described as available via ChatGPT,
Google Gemini, and Claude, with real-time availability, performance signals, and confirmed
appointment booking into ServiceTitan. The release also says ServiceTitan *intends* to extend
Homh into consumer LLMs and AI advertising platforms; treat that as forward-looking, not
shipped. [1][2]

This note is for a voice-agent engineer joining the team. It does not describe internal
Homh architecture, authentication, APIs, or credentials. It lists the **new trust surfaces**
that matter when a consumer's AI assistant is part of the discovery/booking path.

**Scope correction:** the public announcement establishes AI-agent-assisted discovery and
booking; it does *not* establish that Homh is a direct agent-to-agent protocol. Treat protocol,
authentication, idempotency, and authorization details below as questions to validate after
joining, not facts about the product.

## What changed for booking

Homh adds a distinct discovery/booking surface where:

- Discovery happens inside a consumer AI assistant.
- Availability and performance signals are part of the selection experience.
- A confirmed booking is written into ServiceTitan.

The voice agent remains one booking path among several. The announcement explicitly names
AI assistants as a discovery surface; Pantheon also frames booking inside a broader coordination
system involving shared context and coordinated action. [1][3]

## Trust model questions (public-safe)

These questions deliberately avoid asserting an internal protocol. The useful senior-engineer
move is to identify the trust boundary and then ask where the authoritative check lives.

Write them down before you start; validate them only after joining, through normal team
channels. They are questions, not answers:

### Identity and authorization

- How is the requesting agent (or platform) authenticated?
- How is the homeowner's authority to book for an address established?
- What prevents one agent from booking on behalf of another household?

### Consent and disclosure

- What disclosures apply when no human is on the line?
- How is recording or transcript retention handled for agent-originated bookings?
- Where does "AI is assisting" disclosure live when the consumer already opened an AI app?

### Idempotency and double-booking

- What is the idempotency key for a Homh-originated booking request?
- How are retries from an assistant distinguished from a second distinct request?
- Who wins if phone and Homh both attempt the same slot?

### Capacity and policy

- Do Homh bookings use the same Adaptive Capacity rules as first-party voice/chat agents?
- Which job types or membership rules can an external agent never override?
- What is the escalation path when capacity is full or the request is out of policy?

### Abuse and quality

- How are spam or automated probing requests detected?
- What rate limits or reputation signals apply per platform or per agent identity?
- How are failed or cancelled Homh bookings attributed in demand metrics?

## Control-plane implications

The same pattern as phone voice still applies:

**The model (or external agent) proposes → the application controls → the source of truth verifies.**

External agents increase the cost of weak control:

- A free-form "book me Tuesday" string is insufficient; the system needs structured slot ids,
  policy checks, and a durable commit.
- Spoken or chat confirmation language must not run ahead of the source of truth.
- Shared context written for dispatch must be verified, not merely echoed from the requester.

See [Call facts contract](call-facts-contract.md) for a teaching schema of what to capture,
and [lab 12](../labs/README.md) for an offline, generic agent-to-agent booking exercise (a
teaching model, not Homh's design).

## Questions to bring to the team

- How are Homh bookings authenticated and validated today?
- What is shared vs different between phone voice booking and Homh booking in the control plane?
- How does Adaptive Capacity for AI CSRs interact with Homh? The public announcement says
  Adaptive Capacity is being made available to AI CSRs; it does not document the internal
  interaction between that capability and Homh. [1]
- Which metrics treat Homh bookings as the same denominator as phone bookings?

## Related material

- [Pantheon 2026 AI roadmap brief](pantheon-2026-ai-roadmap.md)
- [Call facts contract](call-facts-contract.md)
- [Labs 09–12](../labs/README.md)
- [Tools and guardrails](tools-and-guardrails.md)

## Sources

1. ServiceTitan press release, Pantheon 2026 (October 6, 2026):
   <https://www.globenewswire.com/news-release/2026/10/06/3375320/0/en/servicetitan-announcing-new-and-expanded-capabilities-at-pantheon-2026.html>
2. ServiceTitan, Pantheon 2026 live coverage:
   <https://www.servicetitan.com/blog/pantheon-2026-live-coverage>
3. Investing.com, ServiceTitan Pantheon 2026 keynote summary and transcript (October 6, 2026):
   <https://www.investing.com/news/transcripts/servicetitan-at-pantheon-2026-ai-push-aims-to-make-trades-selfrunning-93CH-4934737>
