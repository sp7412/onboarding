# 12 - Risks And Failure Modes

**Estimated reading time:** 7 minutes

## Five Takeaways

1. Severity and likelihood values below are engineering analysis, not statistics.
2. Wrong state changes can be more harmful than awkward language.
3. Safety-sensitive and restricted requests need explicit escalation.
4. Detection, containment, review, and rollback should be designed together.
5. Public sources do not establish private incident history or risk acceptance.

## Risk Matrix

| Failure | Severity reasoning | Controls |
|---|---|---|
| Wrong or duplicate booking | Operational disruption and trust loss | Recheck, confirmation, idempotency, audit |
| Hallucinated confirmation | Caller acts on false state | Speak only from tool result |
| Unsafe technical guidance | Possible physical harm | OOD detection, transfer, no diagnosis claim |
| Identity or authorization error | Privacy or unauthorized action | Verification and scoped tools |
| Stale availability | Conflict and rework | Commit-time validation |
| Outage or tool timeout | Unresolved customer request | Explicit pending state and fallback |
| Transcript or payment exposure | Privacy and security harm | Minimize context, isolate payment, retention |

EPA Section 608 is a concrete example of why trade-specific work can have obligations that
are not answered by general conversation. [1] PCI DSS and CCPA provide additional public
examples of payment-data and privacy concerns. [2][3]

## Testing And Monitoring

Offline tests should cover adversarial phrasing, noise, interruption, conflicting facts,
unavailable slots, retries, and backend failures. Online monitors should sample tool/state
agreement, transfer correctness, latency, error rates, and human corrections. A rollback
must be possible for model, prompt, policy, and configuration changes independently where
the system permits it.

## Sources

1. U.S. EPA Section 608: <https://www.epa.gov/section608>
2. PCI DSS: <https://www.pcisecuritystandards.org/standards/pci-dss/>
3. California DOJ CCPA: <https://oag.ca.gov/privacy/ccpa>
