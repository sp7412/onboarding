# Content-First Audit

**Audit date:** October 19, 2026

## Scope and method

This pass prioritized factual precision, teaching contracts, production-safety boundaries, and
source quality in guides, whitepaper chapters, labs, solutions, and public-product evidence.
It intentionally did not spend effort on visual navigation unless it prevented a reader from
using content. Official LiveKit, MCP, OpenAI Agents SDK, ServiceTitan, Apple, and ServiceTitan
press sources were compared where accessible. Some OpenAI developer-model pages remained
bot-blocked in this environment, so volatile model facts were not expanded from memory.

## Findings and Changes

| ID | Severity | Status | Change |
|---|---|---|---|
| CONTENT-01 | P1 | Fixed | Removed the unsafe all-party-state list from the recording-consent chapter. The guide now requires a counsel-maintained jurisdiction matrix rather than treating a generic list as implementation guidance. |
| CONTENT-02 | P1 | Fixed | Replaced the ungrounded Lab 05 address-confirmation transition with quoted, affirmative caller evidence. The tool and middleware now both reject ungrounded booking preconditions. |
| CONTENT-03 | P1 | Fixed | Added the missing transcript and emergency hooks to Lab 04's cascaded LiveKit session so the shared booking tools retain their grounding and emergency-state inputs. |
| CONTENT-04 | P2 | Fixed | Corrected Lab 16's real-transport commands to use the actual `mcp_demo/server.py` path and documented the Inspector's Node/npx prerequisite. |
| CONTENT-05 | P2 | Fixed | Replaced Lab 17's unrelated Census/revenue assessment with decision-contract questions and an offline fallback exercise. |
| CONTENT-06 | P2 | Fixed | Added an authorization fact group to the CallFacts teaching contract. Identity/account matching no longer implies authority to read or mutate an existing appointment. |
| CONTENT-07 | P2 | Fixed | Corrected whitepaper economics wording: revenue/GTV is a derived comparison, not proof of a share-of-wallet growth mechanism. |
| CONTENT-08 | P2 | Fixed | Added missing bibliography entries for sources cited in whitepaper chapter 09. |
| CONTENT-09 | P2 | Fixed | Clarified that input guardrails may run in parallel and cannot replace deterministic write authorization; HITL approval is now shown as a request, not a cancellation commit. |
| CONTENT-10 | P2 | Fixed | Reframed MCP's cited revision and added an explicit per-request context and operation-ID rule. |
| CONTENT-11 | P2 | Fixed | Added evaluation questions for channel/configuration/cohort comparability and rollback ownership to public Voice Intelligence evidence. |

## Deferred Content Work

- The full-duplex build guide needs a larger redesign before it can safely demonstrate stable
  transcript assembly, operation revisions, cancellation before a side effect, and
  heard-versus-generated state. Its present compact router is explicitly instructional; do not
  promote it to production code.
- The capstone rubric asks for an audit artifact not emitted directly by labs 07–08. A focused
  follow-up should add a redacted offline audit-report harness rather than weaken the rubric.
- Volatile OpenAI model identifiers, limits, prices, and API snippets should be migrated to a
  dated verification record or visibly downgraded when the primary model pages cannot be read.
- Promotion math needs an explicit non-independent-call, delayed-label, and change-reset policy.

## Validation

The notebook sources were rebuilt and labs 04, 05, 16, and 17 passed offline. Repository
hygiene, generated-notebook consistency, unit tests, site tests/build/internal links, and the
external-link checker were also run. The external checker completed with zero hard failures;
documented bot-protected primary sources are reported separately as retained records.
