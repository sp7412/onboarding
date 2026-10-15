# Review of ServiceTitan's Public GitHub Organization

**Review date:** 2026-10-15  
**Scope:** Public repositories visible under [github.com/servicetitan](https://github.com/servicetitan), with deeper reading of the projects most relevant to voice/agent engineering, real-time systems, API contracts, and AI developer tooling.  
**Purpose:** Improve this public-source onboarding guide without implying access to ServiceTitan's private production architecture.

## Executive summary

The public organization is useful for understanding selected engineering tools and public experiments, but it is **not a public mirror of the production Voice Agent or Voice Intelligence systems**. In the public repositories reviewed, I found no clearly identified production voice-agent implementation, internal multi-agent registry, or complete LLM orchestration stack.

The strongest technical learning resource is **[Stl.Fusion](https://github.com/servicetitan/Stl.Fusion)** and its [sample/tutorial repository](https://github.com/servicetitan/Stl.Fusion.Samples). Fusion is a .NET distributed reactive memoization framework. Its code and documentation explain dependency-aware computed state, invalidation propagation, client replicas, WebSocket RPC, reconnect behavior, and performance testing. These are relevant patterns for keeping real-time application state coherent. They are **not evidence that the production voice-agent backend uses Fusion**.

Other notable findings:

- **LazyProxy family:** .NET dependency-injection utilities that defer service construction. Useful for thinking about startup and object-graph costs; not an agent framework.
- **Claude Code Action:** AI coding automation for PRs/issues, code review, implementation, and structured outputs. Relevant to developer tooling and automation safety, not evidence of a customer-facing voice runtime.
- **AzureChatGPT:** a solution accelerator for private enterprise chat over Azure OpenAI and internal data. Historical architecture background, not proof of current internal deployment.
- **Moltbot/OpenClaw fork:** contains an inspectable public voice-call extension with Twilio/Telnyx/Plivo adapters, OpenAI Realtime transcription, TTS queues, barge-in, and normalized call events. It is upstream-derived and is not evidence of ServiceTitan's production architecture.
- **Recording PWA prototype:** source inspection found a Field Pro Recorder with local browser audio capture, IndexedDB chunk persistence, and background-interruption recovery. It has no upload/ASR path in the inspected code; I also identified untested data-loss and cleanup risks.
- **Forks and general-purpose libraries:** much of the organization consists of inherited open-source tooling, schema/code-generation libraries, SDKs, and web infrastructure. A repository under the organization is not automatically a ServiceTitan-authored product.

## Method and confidence

I used the public organization repository listing and GitHub repository search, inspected README/documentation or project metadata for the most relevant projects, and searched for voice-agent, agent, AI, and MCP-related evidence. The organization listing showed **31 public repositories** in the snapshot captured for this review. Repository listings and code evolve; this is a dated snapshot, not a permanent inventory.

This is a **source review, not a full line-by-line security audit of all 31 repositories**. Deeper review focused on Anvil2's Voice Agent/AI Kit examples, the Moltbot voice-call extension and selected commit history, the recording PWA implementation, Fusion operation internals/tutorials, Claude Code Action's executable contract/security/configuration docs, the LazyProxy family, AzureChatGPT, and selected API/schema tooling. Remaining repositories were classified from public metadata and available README information. A negative search result means I did not find public evidence in the reviewed material; it does not prove that no private implementation exists.

## Deep review

### 1. Stl.Fusion — highest-value technical read

Repository: [servicetitan/Stl.Fusion](https://github.com/servicetitan/Stl.Fusion)  
Documentation: [Fusion docs](https://github.com/servicetitan/Stl.Fusion/tree/master/docs)  
Samples: [servicetitan/Stl.Fusion.Samples](https://github.com/servicetitan/Stl.Fusion.Samples)

Fusion describes itself as **Distributed REActive Memoization (DREAM)**. The central idea is to cache results of computations while tracking dependencies between computed values. When a source value changes, invalidation propagates through dependent computations. Remote clients can hold replicas of computed results and receive invalidation notifications over a WebSocket-based RPC protocol.

The repository includes source, documentation, samples, tests, build configuration, and performance-test scripts. The samples repository provides runnable .NET examples and tutorials, including single-server and multi-server RPC samples and benchmarks. The tutorial documents reconnect behavior and refreshing replicas after reconnect.

**Patterns worth learning**

1. **Make state dependencies explicit.** Derived state should be invalidated when authoritative inputs change; avoid downstream consumers silently keeping stale results.
2. **Separate authoritative state from replicas.** A local cached view can improve latency, but it needs a defined consistency and invalidation contract.
3. **Treat reconnect as state reconciliation.** Re-establishing transport is not enough; cached remote state may need refreshing or revalidation.
4. **Measure the actual workload.** The repository includes performance tests and benchmark samples. Reproduce measurements with representative workloads rather than treating headline speed claims as universal.
5. **Keep transport and application semantics distinct.** Fusion's RPC/invalidation protocol is a particular design, not a generic substitute for every messaging or event-streaming system.

**Voice-agent application — engineering inference, not a ServiceTitan implementation claim**

A voice agent may have to reconcile call state, customer facts, booking status, and UI updates while several services operate concurrently. Fusion's dependency/invalidation concepts are useful for thinking about stale reads and UI consistency. They do not by themselves solve turn-taking, audio transport, model orchestration, tool authorization, transaction semantics, or distributed booking locks.

For a booking workflow, an invalidation notification must never be treated as an atomic reservation. The authoritative scheduling system still needs to validate availability and commit the booking with appropriate concurrency and idempotency controls.

**Trade-offs and questions to investigate**

- What is the source of truth, and what is merely a cached or replicated view?
- What is the consistency contract during network partitions or reconnects?
- How are invalidations, cache growth, cancellation, and failures handled under load?
- What happens if an update arrives out of order or a client remains disconnected?
- Which performance results hold for the target latency, fan-out, payload sizes, and failure profile?

**Recommendation:** Read the Fusion README, then the samples/tutorial sections on computed values, live state, replicas, and RPC. Run the multi-server and RPC benchmark examples if the current SDK/environment supports them. Treat the project as a design study; do not assume it is deployed in the Voice Agent stack.

### 2. Stl.Fusion.Samples — practical companion

Repository: [servicetitan/Stl.Fusion.Samples](https://github.com/servicetitan/Stl.Fusion.Samples)  
Published tutorial: [servicetitan.github.io/Stl.Fusion.Samples](https://servicetitan.github.io/Stl.Fusion.Samples/)

The README says the examples target the .NET 8 SDK and includes HelloWorld/Blazor examples, MiniRpc, MultiServerRpc, and benchmark projects. It also points to **Actual Chat**, a separate application described as combining real-time audio, live transcription, and AI assistance, and notes that some Fusion examples come from that application's codebase.

That Actual Chat reference is a useful adjacent example of a real-time application. It is **not evidence that Actual Chat is ServiceTitan's Voice Agent**, nor that the production voice product uses the same implementation.

**Recommendation:** Use the sample projects to understand Fusion concepts in executable form. Keep the Actual Chat example labeled as an adjacent product example.

### 3. LazyProxy family — deferred dependency construction

Repositories: [lazy-proxy](https://github.com/servicetitan/lazy-proxy), [lazy-proxy-autofac](https://github.com/servicetitan/lazy-proxy-autofac), [lazy-proxy-serviceprovider](https://github.com/servicetitan/lazy-proxy-serviceprovider), [lazy-proxy-unity](https://github.com/servicetitan/lazy-proxy-unity).

The core library builds runtime proxy types that defer creating the underlying service until a member is invoked. Companion repositories integrate the pattern with dependency-injection containers.

**What it teaches:** dependency graphs, construction cost, proxy behavior, and the difference between resolving a service and actually using it. The core README documents support for sync/async and generic methods, properties, indexers, and thread-safe proxy generation, with limitations such as events not being supported.

**Trade-offs:** deferred construction can reduce eager startup work, but moves cost and possible failures to first use. It can make latency less predictable if the first request constructs a large dependency graph. It does not eliminate the work and should not be added to a hot path without measuring cold-start and first-call latency.

**Recommendation:** Relevant background for .NET service composition; low direct relevance to voice-agent design.

### 4. Claude Code Action — AI-assisted engineering automation

Repository: [servicetitan/claude-code-action](https://github.com/servicetitan/claude-code-action)

The public README describes a GitHub Action for AI assistance on pull requests and issues: answering questions, reviewing code, implementing changes, and returning structured outputs. It describes authentication/provider options and links to setup, solutions, and security documentation. The repository content resembles the public Anthropic Claude Code Action project; treat its presence as evidence of an available public developer-tooling artifact, not a proprietary ServiceTitan agent architecture.

**Useful lessons for engineering workflows**

- Distinguish interactive comment-triggered operation from explicit prompt-driven automation.
- Treat tool access and repository permissions as security boundaries.
- Keep untrusted issue/PR content separate from trusted workflow configuration.
- Use constrained permissions, auditable CI runs, and explicit test gates before accepting generated changes.
- Prefer validated structured outputs when automation needs machine-readable results.
- Do not equate a successful agent run with a correct patch; tests, review, and merge policy remain authoritative.

**Security caution:** An AI coding action can execute tools in a repository context. Workflow triggers, tokens, permissions, project configuration, and untrusted PR content therefore matter. Review the current upstream security documentation before adopting any workflow.

**Recommendation:** Useful for developer-experience onboarding and AI coding automation. Not a voice-agent runtime.

### 5. AzureChatGPT — enterprise chat solution accelerator

Repository: [servicetitan/azurechatgpt](https://github.com/servicetitan/azurechatgpt)

The README describes a private ChatGPT-like experience on Azure OpenAI, with network/security controls and the ability to connect internal data or services. It includes deployment, identity, file-chat, and environment-variable guides.

This is an example of an enterprise LLM application pattern: model access, identity, deployment, internal data integration, and policy controls. Treat it as a solution accelerator whose current compatibility and maintenance status need independent verification, not as a source of truth for ServiceTitan's current AI platform.

**Recommendation:** Optional historical background. Prefer current vendor docs and maintained examples for implementation decisions.

### 6. Recording PWA prototype — limited evidence

Repository: [servicetitan/recording-PWA-proto](https://github.com/servicetitan/recording-PWA-proto)

The README is still the standard Vite scaffold, but source inspection shows a working local-recording prototype: microphone capture, MIME selection, pause/resume, segmented recording, IndexedDB persistence, local playback/deletion, and recovery after page visibility changes. The UI calls it **Field Pro Recorder**. Metadata includes an `uploaded` boolean, but both finalization paths set it to `false`; searches for `fetch(`, `XMLHttpRequest`, transcription, and speech recognition returned no implementation in this repository. The best-supported conclusion is a local recording prototype, not a complete upload/transcription pipeline.

**Recommendation:** Do not cite it as a production voice-recording architecture. Inspect source files and history before drawing more specific conclusions.

### 7. API contracts and code generation

Relevant repositories include [NSwag](https://github.com/servicetitan/NSwag) and [NJsonSchema](https://github.com/servicetitan/NJsonSchema). Their README content identifies them as general-purpose .NET/OpenAPI and JSON Schema tooling associated with their respective open-source projects. The organization also contains forks or copies of other libraries and SDKs.

These are useful ecosystem clues for API schema generation and typed client contracts, but a fork's presence does not establish which version ServiceTitan uses internally or how its production APIs are designed.

**Recommendation:** Learn the general concepts—schema-first contracts, generated clients, compatibility checks—but do not infer internal service boundaries from repository ownership alone.

## Inventory of the 31 public repositories

The table records the public organization snapshot and each repository's relevance to this onboarding project. “Low” means it does not materially inform voice-agent architecture based on the public evidence reviewed; it does not mean the repository has no value to its maintainers.

| Repository | Publicly apparent purpose / classification | Onboarding relevance |
|---|---|---|
| [Stl.Fusion](https://github.com/servicetitan/Stl.Fusion) | .NET distributed reactive memoization and real-time application framework | **High** — state consistency, invalidation, replicas, RPC, performance |
| [Stl.Fusion.Samples](https://github.com/servicetitan/Stl.Fusion.Samples) | Runnable Fusion samples and tutorials | **High** — hands-on study |
| [lazy-proxy](https://github.com/servicetitan/lazy-proxy) | Lazy interface proxies for .NET services | Medium — dependency construction and cold-path latency |
| [lazy-proxy-autofac](https://github.com/servicetitan/lazy-proxy-autofac) | Autofac integration for lazy dependency injection | Low–medium |
| [lazy-proxy-serviceprovider](https://github.com/servicetitan/lazy-proxy-serviceprovider) | Microsoft DI ServiceProvider integration | Low–medium |
| [lazy-proxy-unity](https://github.com/servicetitan/lazy-proxy-unity) | Unity container integration | Low–medium |
| [dataobjects-net](https://github.com/servicetitan/dataobjects-net) | Fork of a .NET data-access/object-relational library | Low — inspect if relevant to a concrete stack question |
| [ReportGenerator](https://github.com/servicetitan/ReportGenerator) | Code-coverage report generation project | Low — testing/coverage tooling |
| [Stl.Extras](https://github.com/servicetitan/Stl.Extras) | Archived supporting library | Low; archived |
| [api-management-developer-portal](https://github.com/servicetitan/api-management-developer-portal) | Fork of Azure API Management developer portal | Low–medium — API publishing/developer experience |
| [clrspy](https://github.com/servicetitan/clrspy) | Archived .NET runtime/debugging utility | Low; archived |
| [editable-contracts](https://github.com/servicetitan/editable-contracts) | Archived contracts-related project | Low; archived |
| [NSwag](https://github.com/servicetitan/NSwag) | OpenAPI/Swagger and typed client generation tooling | Medium conceptually; ecosystem tooling |
| [tslint-yield](https://github.com/servicetitan/tslint-yield) | Archived TSLint-related utility | Low; archived |
| [DarkSkyApi](https://github.com/servicetitan/DarkSkyApi) | Weather API client library | Low |
| [claude-code-action](https://github.com/servicetitan/claude-code-action) | Claude Code GitHub automation action | **Medium–high** for AI developer tooling, permissions, and CI guardrails; not voice runtime |
| [anvil2-docs-live-code](https://github.com/servicetitan/anvil2-docs-live-code) | Anvil2 design-system examples, including Atlas and AI Kit interaction patterns | **High for product/UX clues**; examples are mostly static UI, not backend implementation |
| [NJsonSchema](https://github.com/servicetitan/NJsonSchema) | JSON Schema parsing, validation, and code generation tooling | Medium conceptually; ecosystem tooling |
| [terraform-provider-sendgrid](https://github.com/servicetitan/terraform-provider-sendgrid) | SendGrid infrastructure provider | Low |
| [mergetest-public](https://github.com/servicetitan/mergetest-public) | Explicitly described as a public CI/CD workflow test repository | Low; workflow demonstration |
| [Xero-NetStandard](https://github.com/servicetitan/Xero-NetStandard) | Xero API client wrapper | Low |
| [diff-match-patch](https://github.com/servicetitan/diff-match-patch) | Text-diff/patch utility | Low |
| [unpkg](https://github.com/servicetitan/unpkg) | JavaScript package CDN-related project | Low; infrastructure dependency |
| [AngleSharp.Css](https://github.com/servicetitan/AngleSharp.Css) | CSS extension for AngleSharp | Low |
| [moltbot](https://github.com/servicetitan/moltbot) | Public fork of OpenClaw/Moltbot, including a voice-call extension and multi-channel agent runtime | **High as an external reference architecture**; no ServiceTitan-specific voice backend established |
| [verdaccio-storage-proxy](https://github.com/servicetitan/verdaccio-storage-proxy) | npm registry/storage proxy component | Low |
| [AngleSharp](https://github.com/servicetitan/AngleSharp) | HTML parsing library | Low |
| [recording-PWA-proto](https://github.com/servicetitan/recording-PWA-proto) | React/Vite PWA prototype scaffold | Low pending source-level review |
| [azurechatgpt](https://github.com/servicetitan/azurechatgpt) | Azure OpenAI private-chat solution accelerator | Medium as historical enterprise-LLM background |
| [dotnet-dumps-devcontainer](https://github.com/servicetitan/dotnet-dumps-devcontainer) | .NET dump-analysis development container; README unavailable in this review | Low–medium for incident/debugging workflows; details unverified |
| [html-sketchapp](https://github.com/servicetitan/html-sketchapp) | Archived design-tool integration | Low; archived |

**Classification caveat:** Some repositories are forks, mirrors, or upstream projects. The table describes public purpose rather than attributing all implementation decisions to ServiceTitan.

## What this does—and does not—tell us about the voice-agent stack

### Supported by the public evidence reviewed

- ServiceTitan publishes the Fusion real-time .NET framework and examples.
- The organization has public code for lazy dependency-injection utilities and assorted application/developer infrastructure.
- It has a public Claude Code Action repository and an AzureChatGPT solution accelerator.
- A recording-named PWA prototype exists, but its README/metadata alone do not document a production audio architecture.
- The reviewed public inventory does not expose an obvious, clearly labeled production Voice Agent implementation.

### Not established by these repositories

The review does **not** establish the internal voice stack's ASR/TTS providers, media transport, orchestration framework, agent count, inter-agent messaging, MCP usage, trace schema, Kafka/Snowflake design, scheduling transaction protocol, deployment topology, or model-routing policy. Those details require direct public documentation or authorized internal confirmation.

The guide's existing architecture diagrams, trace schemas, orchestration patterns, and agent-coordination exercises should remain labeled as **reference architectures, public-product interpretations, or teaching examples**, not as recovered internal design.

## Recommended learning order

1. Read [Stl.Fusion README](https://github.com/servicetitan/Stl.Fusion) and the [Fusion documentation](https://github.com/servicetitan/Stl.Fusion/tree/master/docs).
2. Run selected [Fusion Samples](https://github.com/servicetitan/Stl.Fusion.Samples), especially the tutorial and multi-server/RPC examples; inspect benchmark methodology before reusing any numbers.
3. Read the [LazyProxy README](https://github.com/servicetitan/lazy-proxy) only if dependency-injection behavior or cold-start cost becomes relevant.
4. Review [Claude Code Action](https://github.com/servicetitan/claude-code-action) with emphasis on trigger conditions, tool permissions, token scopes, untrusted pull-request inputs, structured output, and CI gates.
5. Treat AzureChatGPT and the recording PWA as optional historical/prototype reading unless source history or a concrete engineering task makes them relevant.

## Sources

- [ServiceTitan GitHub organization](https://github.com/servicetitan) — repository inventory and organization-level metadata.
- [Stl.Fusion README](https://github.com/servicetitan/Stl.Fusion) and [documentation](https://github.com/servicetitan/Stl.Fusion/tree/master/docs).
- [Stl.Fusion.Samples README](https://github.com/servicetitan/Stl.Fusion.Samples) and [tutorial documentation](https://servicetitan.github.io/Stl.Fusion.Samples/).
- [LazyProxy README](https://github.com/servicetitan/lazy-proxy) and the [ServiceProvider integration](https://github.com/servicetitan/lazy-proxy-serviceprovider).
- [Claude Code Action README](https://github.com/servicetitan/claude-code-action); the current [upstream security documentation](https://github.com/anthropics/claude-code-action/blob/main/docs/security.md) is useful for general workflow-security principles, but is not proof of the fork's exact state.
- [AzureChatGPT README](https://github.com/servicetitan/azurechatgpt).
- [Recording PWA prototype](https://github.com/servicetitan/recording-PWA-proto).
- [NSwag](https://github.com/servicetitan/NSwag) and [NJsonSchema](https://github.com/servicetitan/NJsonSchema).

## Maintenance rule

Revisit this review when the organization publishes a clearly relevant voice/agent repository, an existing repository changes materially, or a public technical disclosure substantiates a previously unknown architecture detail. Update claims only with source links and dates, and preserve the distinction between observed code and inference.


## Second-pass, source-level clue review

This section records the higher-signal findings after searching code across the organization for voice/audio, recording, agent, MCP, transcription, escalation, prompt, action-log, booking, payment, Atlas, and related terms, then reading the relevant source files. It supersedes the earlier shallow classification of `anvil2-docs-live-code` and `recording-PWA-proto`.

### A. Anvil2 examples expose a useful product/UX vocabulary

Repository: [servicetitan/anvil2-docs-live-code](https://github.com/servicetitan/anvil2-docs-live-code)

The repository README is only a one-line title, so the evidence is in the examples themselves. These examples import `@servicetitan/anvil2`, `@servicetitan/anvil2-ai-kit`, and `@servicetitan/anvil2-ext-atlas`; most use hard-coded sample messages and no backend calls. They are source-backed clues about product concepts and interface states, **not proof of the runtime's internal orchestration**.

#### A1. Voice Agent configuration appears to have five explicit areas

File: [settings-page example](https://github.com/servicetitan/anvil2-docs-live-code/blob/main/examples/block-decorative-icon-settings-page/src/App.tsx)

The `settingsPageSections` array names:

1. **Persona** — brand identity and foundational knowledge.
2. **Conversation Flow** — interaction logic and specialized responses for scenarios.
3. **Rules** — permissions for actions such as booking jobs and processing payments.
4. **Job Types and Fees** — job types, dispatch fees, and how fees are communicated.
5. **Escalations and Fallbacks** — transition from Voice Agent to human support.

This is the strongest direct Voice Agent clue in the organization outside public product marketing. It implies that customer/tenant configuration is separated into persona, flow, action permissions, domain-specific booking/fee configuration, and escalation/fallback behavior. The file only renders section cards with `Edit` buttons that log to the console; it does not show how those settings are stored, versioned, evaluated, or enforced.

#### A2. Navigation suggests the broader assistant/product surface

Files: [full-page navigation example](https://github.com/servicetitan/anvil2-docs-live-code/blob/main/examples/block-global-navigation-full-page/src/App.tsx) and [admin navigation example](https://github.com/servicetitan/anvil2-docs-live-code/blob/main/examples/block-global-navigation-admin-full-page/src/App.tsx)

The navigation examples include **Agent Settings**, **Agent Workflows**, **Interactions**, **Calls**, **Bookings**, **Call Analytics**, and **Insights**, alongside operational areas such as AR Management, Invoices, and Customer Payments. This suggests the product experience is not just a voice endpoint: it includes configuration, workflows, interaction/call review, booking outcomes, and analytics. Since these are navigation mockups, they do not establish which sections are shipped, enabled for every tenant, or backed by a particular service.

#### A3. The AI Kit examples make action visibility a first-class UX pattern

Files: [ActionLog example](https://github.com/servicetitan/anvil2-docs-live-code/blob/main/examples/ai-kit-action-log/src/App.tsx), [labeled evidence disclosure](https://github.com/servicetitan/anvil2-docs-live-code/blob/main/examples/ai-kit-evidence-disclosure-labeled-do/src/App.tsx), and [response-first evidence disclosure](https://github.com/servicetitan/anvil2-docs-live-code/blob/main/examples/ai-kit-evidence-disclosure-response-first-do/src/App.tsx)

The examples represent work as discrete steps with IDs, titles, statuses such as `success`, `in-progress`, `not-started`, and `error`, and optional descriptions. One example shows “Looked up the customer account” followed by “Pulled the last 20 invoices”; another pairs an action log with the user-facing answer. Separate variants explicitly compare labeled vs. unlabeled evidence disclosure and response-first vs. other layouts.

**Engineering implication:** the visible product pattern favors a user-facing answer plus an inspectable summary of what was checked or done. For our onboarding, this supports teaching traces/action logs as an auditable record of tool activity, not as a dump of hidden chain-of-thought. The examples do not show a backend trace schema, tool payloads, trace IDs, persistence, or how the displayed steps are generated.

#### A4. Human-escalation examples encode a detailed boundary taxonomy

These are especially valuable. The repository contains separate examples for different escalation reasons, including:

| Example | What the sample demonstrates | System-design lesson |
|---|---|---|
| [Blocking escalation](https://github.com/servicetitan/anvil2-docs-live-code/blob/main/examples/ai-kit-patterns-human-escalation-blocking/src/App.tsx) | Explain why a connector/repository cannot be accessed, disclose the access gap, and offer concrete next steps | Do not pretend access; report blockers and give recovery options |
| [Backdated invoice](https://github.com/servicetitan/anvil2-docs-live-code/blob/main/examples/ai-kit-patterns-human-escalation-backdated-invoice/src/App.tsx) | Refuse a request to falsify invoice dates; offer an accurate alternative | Integrity/business-rule refusals should be specific and redirect to a safe action |
| [Another role](https://github.com/servicetitan/anvil2-docs-live-code/blob/main/examples/ai-kit-patterns-human-escalation-another-role/src/App.tsx) | CSR can see an invoice but cannot void it; the action belongs to Accounting; assistant drafts a handoff message | Read permission and write/action permission are distinct; handoff should preserve context |
| [Credit limit](https://github.com/servicetitan/anvil2-docs-live-code/blob/main/examples/ai-kit-patterns-human-escalation-credit-limit/src/App.tsx) | $350 credit exceeds a $200 per-incident authority cap; offer partial action plus approval or one approval request | Encode quantitative authorization limits; approval should be explicit |
| [Tenant setting](https://github.com/servicetitan/anvil2-docs-live-code/blob/main/examples/ai-kit-patterns-human-escalation-tenant-setting/src/App.tsx) | Feature is disabled tenant-wide; only Tenant Owner/IT Admin can change it | Distinguish tenant-level policy/configuration from an individual user's role |
| [ServiceTitan permission](https://github.com/servicetitan/anvil2-docs-live-code/blob/main/examples/ai-kit-patterns-human-escalation-servicetitan-permission/src/App.tsx) | A feature flag is controlled by ServiceTitan, not the tenant; assistant offers to contact Support | Distinguish tenant authority from vendor-side feature enablement |
| [Other tenant](https://github.com/servicetitan/anvil2-docs-live-code/blob/main/examples/ai-kit-patterns-human-escalation-other-tenant/src/App.tsx) | A broader search cannot cross tenant boundaries | Tenant isolation is a hard authorization boundary, not a prompt preference |
| [Malicious intent](https://github.com/servicetitan/anvil2-docs-live-code/blob/main/examples/ai-kit-patterns-human-escalation-malicious-intent/src/App.tsx) | A claimed “authorized test” does not override tenant isolation | User assertions must not grant privileges; authorization comes from system policy |
| [Stale guidance](https://github.com/servicetitan/anvil2-docs-live-code/blob/main/examples/ai-kit-patterns-human-escalation-stale-guidance/src/App.tsx) | The known answer may have been invalidated by a recent product change; hold final advice and ask to confirm | Knowledge needs freshness/provenance; uncertainty should trigger verification before consequential actions |
| [Uncertain context](https://github.com/servicetitan/anvil2-docs-live-code/blob/main/examples/ai-kit-patterns-human-escalation-uncertain-context/src/App.tsx) | A plausible answer is labeled unconfirmed against recent policy changes | Make confidence and unresolved caveats visible; allow user-directed verification when appropriate |
| [Disputed result](https://github.com/servicetitan/anvil2-docs-live-code/blob/main/examples/ai-kit-patterns-human-escalation-disputed-result/src/App.tsx) | System has a send confirmation but cannot verify final delivery; records customer dispute as a delivery gap | Distinguish tool acceptance from end-to-end outcome; log discrepancies rather than inventing certainty |
| [Service degradation](https://github.com/servicetitan/anvil2-docs-live-code/blob/main/examples/ai-kit-patterns-human-escalation-service-degradation/src/App.tsx) | Slow responses are treated as possible platform degradation; avoid making the user wait on likely timeouts | Have explicit degraded-service behavior and escalation rather than retrying blindly |
| [Outside abilities](https://github.com/servicetitan/anvil2-docs-live-code/blob/main/examples/ai-kit-patterns-human-escalation-outside-abilities/src/App.tsx) | Assistant cannot reroute GPS, but can offer a message to the technician or dispatch | Offer the nearest safe supported action rather than pretending to control an unavailable tool |
| [Legal guidance](https://github.com/servicetitan/anvil2-docs-live-code/blob/main/examples/ai-kit-patterns-human-escalation-legal-guidance/src/App.tsx) | Refuses legal guidance and also avoids recasting it as “what other companies do” | Domain boundaries must survive paraphrasing and follow-up pressure |
| [Personal topic](https://github.com/servicetitan/anvil2-docs-live-code/blob/main/examples/ai-kit-patterns-human-escalation-personal-topic/src/App.tsx) | After completing a schedule change, assistant responds empathetically to a personal disclosure and offers a manager handoff | Separate task completion from a new user need; use restrained empathy and a relevant handoff |
| [Song lyrics](https://github.com/servicetitan/anvil2-docs-live-code/blob/main/examples/ai-kit-patterns-human-escalation-song-lyrics/src/App.tsx) | Refuses reproduction of copyrighted lyrics and offers original copy in a similar tone | Refusal should preserve the user's underlying goal with a compliant alternative |
| [Non-blocking escalation](https://github.com/servicetitan/anvil2-docs-live-code/blob/main/examples/ai-kit-patterns-human-escalation-non-blocking/src/App.tsx) | Shows a partial result when a source is inaccessible, then records which integrations and commands were used | Partial completion and tool-access gaps should be explicit, not silently hidden |
| [No authorized path](https://github.com/servicetitan/anvil2-docs-live-code/blob/main/examples/ai-kit-patterns-human-escalation-no-authorized-path/src/App.tsx) | Refuses temporary self-approval access and offers to find a designated backup approver | Do not let urgency bypass separation of duties; route to an authorized alternative |
| [Conflicting sources](https://github.com/servicetitan/anvil2-docs-live-code/blob/main/examples/ai-kit-patterns-human-escalation-conflicting-sources/src/App.tsx) | Two warranty references conflict; assistant surfaces the conflict, asks for confirmation, and flags stale documentation | Detect disagreement between sources; don't silently pick a convenient answer; preserve a documentation-correction loop |

**Important caveat:** these are named example applications with hard-coded dialogue. Their taxonomy is a strong signal of intended UX/pattern coverage, but it is not proof that every rule is enforced in the production agent runtime. In particular, the examples' prose saying an action was “sent,” “submitted,” or “flagged” is illustrative text; the snippets do not call real backend APIs.

#### A5. Prompting is represented as structured user interaction

Files: [AgentPrompt single-step](https://github.com/servicetitan/anvil2-docs-live-code/blob/main/examples/ai-kit-agent-prompt/src/App.tsx), [multi-step](https://github.com/servicetitan/anvil2-docs-live-code/blob/main/examples/ai-kit-agent-prompt-multi-step/src/App.tsx), [free-text](https://github.com/servicetitan/anvil2-docs-live-code/blob/main/examples/ai-kit-agent-prompt-free-text/src/App.tsx), and [transcription prompt bar](https://github.com/servicetitan/anvil2-docs-live-code/blob/main/examples/ai-kit-prompt-bar-transcribing/src/App.tsx)

The UI supports agent-generated questions with selectable options, optional free text, multi-step progression (Back/Next/Send), and transcription states including active waveform and microphone-access error. This is evidence for a human-in-the-loop interaction pattern: the assistant can request a structured decision rather than force all clarification through free-form chat. The transcription example is only a UI state fixture; it contains no ASR implementation.

#### A6. “Atlas” appears as an assistant UI name

The repo includes `@servicetitan/anvil2-ext-atlas` examples for header, footer, content, loader, welcome screen, suggestions, chat window, system errors, and user feedback. One example says “Welcome to Atlas — Your AI Assistant”; another uses “Ask Atlas.” A separate disputed-result sample says “Atlas confirmed send.” This supports that **Atlas is a named assistant experience in these public UI examples**, but does not establish that Atlas is the Voice Agent, how it is orchestrated, or whether the name applies to all AI products.

### B. Recording PWA source-level review

Repository: [servicetitan/recording-PWA-proto](https://github.com/servicetitan/recording-PWA-proto)

Files reviewed: `src/hooks/useAudioRecorder.ts`, `src/services/recordingStorage.ts`, `src/services/platformDetect.ts`, `src/types/recording.ts`, `src/context/RecordingContext.tsx`, `src/components/RecordingControls.tsx`, `src/components/RecordingList.tsx`, `src/App.tsx`, and `package.json`.

What is actually present:

- Browser microphone capture via `getUserMedia` and `MediaRecorder`, with candidate MIME types including WebM/Opus and MP4.
- Recording states `idle`, `recording`, `paused`, and `interrupted`.
- One-second MediaRecorder chunks and persistence in IndexedDB stores `recordings` and `chunks`.
- Segmentation after the page is hidden and microphone reacquisition when visible again.
- Metadata records duration, MIME type, byte size, `uploaded: false`, and zero-length gap markers for lost audio intervals.
- Local playback and deletion, plus a storage-quota estimate helper.

What is not present in the inspected repository: a network upload client, transcription/ASR, speech recognition, a backend endpoint, or a sync queue. Searching the repository for `fetch(`, `XMLHttpRequest`, `transcription`, and `speech recognition` found no matching implementation.

**Potential implementation defects found by reading the code:**

1. **Background flush race:** on page hide, the code calls `requestData()` and then immediately persists the current in-memory chunk array. The final data event is asynchronous; later chunks may arrive after the snapshot and then be discarded when the next segment resets `chunksRef.current`. This needs an event-driven flush/stop sequence and a regression test.
2. **Chunk ordering ambiguity:** `saveChunks()` restarts `chunkIndex` at zero on every batch, while `getChunks()` orders by segment then chunk index. Multiple flushes in one segment can therefore create duplicate sort keys and potentially reorder chunks. A monotonic per-segment counter or explicit sequence ID would be safer.
3. **Listener cleanup:** `pagehide` is registered using an anonymous function but cleanup removes only `visibilitychange`; repeated mount/unmount can leak listeners.
4. **Recovery/stop state:** stop controls are disabled while state is `interrupted`, even though that state represents a possible recoverable microphone failure. That may leave a user without an obvious way to finalize the recording after a failed reconnect.
5. **Quota handling:** quota is measurable but the save path shown does not check it before writing or handle a quota failure with an explicit recovery path.
6. **No upload lifecycle:** `uploaded` remains false and no code transitions it to true. It should not be interpreted as evidence of an implemented upload feature.

These are code-reading hypotheses; I have not run the app in a browser or validated the race on device. They are useful leads for evaluating the prototype, not evidence of production behavior.

### C. A semantic trap: “agent” in Fusion is not an LLM agent

Files: [AgentInfo.cs](https://github.com/servicetitan/Stl.Fusion/blob/master/src/Stl.Fusion/Operations/AgentInfo.cs), [IOperation.cs](https://github.com/servicetitan/Stl.Fusion/blob/master/src/Stl.Fusion/Operations/IOperation.cs), [OperationCompletionNotifier.cs](https://github.com/servicetitan/Stl.Fusion/blob/master/src/Stl.Fusion/Operations/OperationCompletionNotifier.cs), and [DbOperationLogReader.cs](https://github.com/servicetitan/Stl.Fusion/blob/master/src/Stl.Fusion.EntityFramework/Operations/DbOperationLogReader.cs).

The word `AgentId` appears in Fusion's operation framework. Reading the implementation clarifies that `AgentInfo` generates an ID from machine/process identity plus a local counter; operation notifications use it to distinguish local from remote process work. `DbOperationLogReader` polls newly committed operations, batches work, retries indefinitely with configured delays, and can use file-based or PostgreSQL LISTEN/NOTIFY change tracking (the tutorial also mentions Redis). This is a distributed-process/operation-log concept, **not evidence of multi-LLM-agent orchestration**.

Still useful patterns: explicit operation IDs and origin IDs, deduplication via recently seen IDs, durable operation logs, idempotent invalidation/replay, batching, retry policy, and change notification with periodic reconciliation. These can inform distributed systems design, but they should not be mapped directly to an LLM agent registry or agent-to-agent protocol.

### D. Claude Code Action — read the executable input contract, not just the README

Files: [README](https://github.com/servicetitan/claude-code-action/blob/main/README.md) and [action.yml](https://github.com/servicetitan/claude-code-action/blob/main/action.yml).

The action definition is unusually explicit about risk boundaries: default trigger phrase `@claude`; allowed bots default to none; allowing all bots on public repositories warns that external apps may invoke prompts; allowing non-write users warns about prompt injection; it notes that secret scrubbing is best-effort and does not eliminate risk; `show_full_output` warns logs may contain secrets; and `display_report` warns that model-authored output is only appropriate for trusted input. Its configuration docs also show custom MCP servers configured through `--mcp-config`, explicit `--allowedTools`, secrets injected through GitHub Secrets, and a `--max-turns` cap. The security guide says non-write-user mode bypasses the primary permission check and recommends minimal workflow permissions, short-lived `GITHUB_TOKEN`, and validation of outputs. It also says default `@claude` responses do not automatically create a PR: the action commits a branch and returns a PR-creation link for a human to click. These are concrete harness patterns. None of this proves that ServiceTitan uses MCP in its customer-facing agents.

This is a strong source for the onboarding's **agent harness / permission boundary** section: trigger filtering, actor trust, minimal permissions, secret isolation, output validation, and review gates. It remains developer tooling, not evidence of the customer-facing voice runtime. The organization contains a public copy/fork of the action; compare it with upstream before attributing every upstream behavior to the current fork.

### E. Updated evidence ranking

1. **Strongest direct product/UX clue:** Anvil2 Voice Agent settings names Persona, Conversation Flow, Rules, Job Types and Fees, and Escalations/Fallbacks.
2. **Strongest concrete voice-code reference:** the Moltbot/OpenClaw fork contains telephony adapters, streaming STT, TTS, barge-in, call lifecycle events, and webhook controls, but is upstream-derived rather than ServiceTitan-specific.
3. **Strongest operational UX clue:** Anvil2 examples name Agent Workflows, Interactions, Calls, Bookings, Call Analytics, Insights, action logs, and evidence-disclosure variants.
4. **Strongest policy/quality clue:** escalation examples cover authorization, tenant boundaries, money/approval limits, stale information, uncertainty, service degradation, disputed outcomes, and unsupported actions.
5. **Useful prototype clue:** Field Pro Recorder implements local audio capture and interruption-aware persistence, but no upload/transcription pipeline was found.
6. **Useful distributed-systems library clue:** Fusion's operation log and RPC machinery illustrate durable change notification and process identity; its `AgentId` is not an AI-agent identifier.
7. **Useful harness-security clue:** Claude Code Action's `action.yml` makes trust, permissions, prompt injection, and log-secret exposure explicit.

**Still not established:** voice transport/provider, telephony/SIP implementation, ASR/TTS vendors, LLM/provider routing, actual tool schemas, orchestration graph, multi-agent topology, MCP use in production, trace storage format, Kafka/Snowflake usage, and production scheduling transaction semantics. None of the source files reviewed here supplies those internals.


### F. Moltbot fork — the most concrete public voice-runtime code, but upstream-derived

Repository: [servicetitan/moltbot](https://github.com/servicetitan/moltbot)  
Voice-call extension: [extensions/voice-call](https://github.com/servicetitan/moltbot/tree/main/extensions/voice-call)  
Relevant files: [README](https://github.com/servicetitan/moltbot/blob/main/extensions/voice-call/README.md), [runtime.ts](https://github.com/servicetitan/moltbot/blob/main/extensions/voice-call/src/runtime.ts), [webhook.ts](https://github.com/servicetitan/moltbot/blob/main/extensions/voice-call/src/webhook.ts), [media-stream.ts](https://github.com/servicetitan/moltbot/blob/main/extensions/voice-call/src/media-stream.ts), [STT provider](https://github.com/servicetitan/moltbot/blob/main/extensions/voice-call/src/providers/stt-openai-realtime.ts), [call types](https://github.com/servicetitan/moltbot/blob/main/extensions/voice-call/src/types.ts), and [Talk Mode docs](https://github.com/servicetitan/moltbot/blob/main/docs/nodes/talk.md).

This repository deserves a closer look than its one-line inventory description suggests. GitHub identifies it as a fork of [openclaw/openclaw](https://github.com/openclaw/openclaw); the code and documentation are the upstream Moltbot/OpenClaw assistant platform, not a disclosed ServiceTitan product implementation. The sampled history includes mostly upstream changes and a few generic maintenance changes; I did not find a ServiceTitan-specific customer workflow or domain-specific voice-agent backend in the commits inspected. The fork's presence is a signal that this open-source agent implementation is available in the public organization, **not proof it is used in production or connected to ServiceTitan Voice Agent**.

**What the actual voice-call code implements**

- **Telephony adapters:** Twilio Programmable Voice/Media Streams, Telnyx Call Control v2, Plivo Voice API, plus a mock provider for local development.
- **Explicit call control:** tool actions `initiate_call`, `continue_call`, `speak_to_user`, `end_call`, and `get_status`; corresponding gateway RPC operations are separately named.
- **Provider-independent lifecycle:** normalized events include initiated, ringing, answered, active, speaking, speech/transcript, silence, DTMF, ended, and error. Call records include provider/internal IDs, direction, timestamps, state, transcript entries, processed event IDs, and metadata.
- **Streaming audio path:** Twilio mu-law audio arrives through a WebSocket media stream; the stream handler forwards audio to OpenAI Realtime transcription, handles partial/final transcripts and VAD speech-start callbacks, and routes generated audio back to Twilio.
- **Turn-taking/barge-in:** incoming speech can clear queued TTS and the provider's audio buffer; TTS playback is queued per stream to avoid overlapping speech.
- **Response policy:** inbound calls auto-respond; outbound calls only auto-respond when configured in `conversation` mode. The plugin has separate `responseModel`, `responseSystemPrompt`, and timeout configuration.
- **Speech synthesis:** core TTS integration supports OpenAI or ElevenLabs for telephony; the README says Edge TTS is ignored for calls because telephony audio needs PCM and Edge output is unreliable.
- **Deployment boundary:** a local HTTP webhook server can be exposed via a public URL, ngrok, or Tailscale. Provider webhook signature verification is part of the provider interface.

**What this gives the onboarding guide:** a concrete, inspectable reference for call lifecycle state, provider adapters, webhook handling, real-time STT, audio streaming, TTS queues, barge-in, and tool/RPC boundaries. It is especially useful for comparing a cascaded pipeline (telephony audio → streaming transcription → model response → TTS) with a speech-to-speech design.

**Security and correctness review notes**

- The config schema supports inbound policies `disabled`, `allowlist`, `pairing`, and `open`, and explicitly calls `open` dangerous. A production deployment would need a default-deny inbound policy and explicit authorization for any caller-controlled side effects.
- The config also exposes `skipSignatureVerification` and a narrowly described ngrok loopback compatibility bypass. These are high-risk development knobs; deployment should ensure signature bypass cannot accidentally be enabled on publicly reachable production webhooks.
- The webhook server routes requests by path and method and relies on the provider's `verifyWebhook` implementation. The trust chain therefore depends on correct signature verification, URL/body canonicalization, and safe handling of public WebSocket upgrades.
- Transcript callbacks log recognized speech with a provider call ID. Production logging must consider caller PII, retention, access controls, and whether full transcripts belong in operational logs.
- The normalized event example creates a transcript event ID from `Date.now()`. Timestamp-derived IDs can collide under concurrency; production-grade idempotency should use a unique sequence/UUID or provider event ID where available.
- The public code is a reference implementation, not a validated production design. I did not run live telephony tests, review every provider adapter, or perform a full security audit.

**Boundary of inference:** this repo provides real code for one open-source voice-call architecture. It does not establish that ServiceTitan uses Twilio, Telnyx, Plivo, OpenAI Realtime, ElevenLabs, WebSockets, or this call state model in its own Voice Agent.
