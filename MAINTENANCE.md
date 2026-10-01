# Maintenance

This repository is public research and teaching material, not a source of internal system
truth. Keep the public-safe rule in `AGENTS.md` in force.

## Monthly review

1. **Models and APIs:** review the official OpenAI, LiveKit, LangChain, LangGraph, and
   LangSmith documentation linked in `docs/references.md`. Re-check model names, event names,
   imports, prices, limits, and examples. Update the claims ledger when a factual claim changes.
2. **Company facts:** check the latest public SEC filing and public product pages before
   repeating customer counts, revenue, GTV, retention, product names, or product claims.
3. **Regulations:** revisit the regulator or standards source for TCPA, recording consent,
   CCPA, EPA Section 608, PCI DSS, and messaging rules. Label legal interpretation as
   `Analysis:` and do not present this repo as legal advice.
4. **Links:** run the scheduled link workflow or run the site build and link checker locally.
   Replace dead URLs only after finding and verifying the actual destination; never infer a
   URL from a naming pattern.
5. **Learning path:** confirm dates, time estimates, prerequisites, lab order, and capstone
   evidence still agree across README, plan, labs, docs, and the site.

## Before changing facts

- Prefer a primary source. Record the source and date in `docs/whitepaper/claims-ledger.md`.
- Add or update the bibliography row in `docs/references.md`.
- Add `Facts as of` and `Last reviewed` metadata to factual documents you materially revise.
- Mark inaccessible or unverified sources explicitly; do not fill gaps from memory.
- Run the repository and site checks in `AGENTS.md`. Never run live notebook paths in CI.

## Scheduled checks

The weekly link workflow checks tracked Markdown/HTML source URLs and builds the site before
running the generated-site checker. It does not deploy. A failure means a maintainer should
   inspect the first broken URL, verify the replacement manually, update the bibliography if
   needed, and rerun the workflow. `BOT-BLOCKED-BUT-VERIFIED` means the URL is retained in the
   public references/claims records but the configured proxy prevented an automated HTTP check;
   it is not a hard failure.
