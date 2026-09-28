# 14 - Implications And Open Questions

**Estimated reading time:** 6 minutes

## Five Takeaways

1. The strongest leverage is an evidence chain from utterance to committed state.
2. Evaluation should combine OOD, turn-taking, tool, policy, and outcome slices.
3. Safe fallbacks are product behavior, not an afterthought.
4. Public research supports hypotheses and questions, not internal assumptions.
5. Authorized validation is the next step for every private boundary.

## Implications For An ML Engineer

The domain suggests a layered evaluation harness: speech and turn quality; structured
entity extraction; policy eligibility; availability correctness; mutation idempotency;
spoken confirmation; transfer context; and later outcome. The repository's fictional labs
can exercise these concepts offline, but they do not represent production data or
architecture.

The useful artifacts are a failure taxonomy, slice definitions, labeled traces, and a
small set of release-blocking invariants. A model improvement should not ship if it raises
incorrect bookings or unsafe non-escalation even while increasing containment.

## Questions For Validation

- Which workflow states and mutations are authoritative?
- What is the permission and identity model for each tool?
- Which outcomes are release-blocking?
- What is the transfer contract and fallback when no human answers?
- Which data may be retained, redacted, or used for evaluation?
- How are customer results attributed and reviewed?
- What are the actual latency, reliability, cost, and deployment constraints?

## Closing Analysis

The public record supports a coherent engineering thesis: voice automation in the trades
is valuable where it reaches a real workflow, and risky where it makes an unsupported
claim about state. The design response is not to remove conversational flexibility. It is
to constrain authority, expose evidence, measure denominators, and make human recovery
reliable.

## Sources

1. LiveKit Agents overview: <https://docs.livekit.io/agents/>
2. LangSmith evaluation: <https://docs.langchain.com/langsmith/evaluation>
3. ServiceTitan Contact Center Pro: <https://www.servicetitan.com/features/pro/contact-center>
