# References

Every external source cited anywhere in this repo, in one place, grouped by topic.
All links were checked on Oct 7, 2026. For *what to read first and why*, use the ranked
[reading guide](reading-guide.md); this page is the complete bibliography.

Video summaries are collected in [video notes](video-notes.md).

**Where each is cited:** RG = [reading guide](reading-guide.md) item number ·
RL = [reading guide](reading-guide.md) · 101 = [ServiceTitan 101](servicetitan-101.md) ·
PP = [podcast prompts](podcast-prompts.md) episode number · WP = [whitepaper](whitepaper/README.md) chapter.

## ServiceTitan (company and products)

| Source | Type | Cited in |
|---|---|---|
| [AI Voice Agent / AI Virtual Agent product page](https://www.servicetitan.com/features/pro/virtual-agent) | Product page | RG 1, 101, PP 1 |
| [Webinar recap: AI Virtual Agents for call booking](https://www.servicetitan.com/blog/webinar-recap-ai-virtual-agents-call-booking) (the reading guide uses the older slug, which redirects) | Blog | RG 2, PP 1 |
| [Pantheon 2025 press release: Atlas and the AI suite](https://www.servicetitan.com/press/servicetitan-introducing-the-next-evolution-of-ai-at-pantheon-2025-keynote) | Press release | RG 3, PP 1 |
| [Pantheon 2025 keynote recap: Atlas](https://www.servicetitan.com/blog/pantheon-2025-vahe-keynote-atlas) | Blog | RG 3, PP 1 |
| [Contact Center Pro](https://www.servicetitan.com/features/pro/contact-center) | Product page | 101, WP 04-05, 06-07, 11-12, 14 |
| [Scheduling Pro](https://www.servicetitan.com/features/pro/scheduling) | Product page | 101, WP 03, 05, 06-07 |
| [Dispatch Pro](https://www.servicetitan.com/features/pro/dispatch) | Product page | 101, WP 03, 05, 06, 11-12 |
| [Atlas](https://www.servicetitan.com/features/atlas) | Product page | 101, WP 06, 13 |
| [Company overview](https://www.servicetitan.com/company) | Company page | 101, WP 00-01 |
| [Features overview](https://www.servicetitan.com/features) | Product index | 101, WP 06 |
| [Industries served](https://www.servicetitan.com/industries) | Product index | 101, WP 02 |
| [Products overview](https://www.servicetitan.com/products) | Product index | 101, WP 01, 06, 11 |
| [Conduit](https://www.servicetitan.com/products/conduit) | Product page | WP 01 |

## Voice-agent fundamentals

| Source | Type | Cited in |
|---|---|---|
| [Voice AI & Voice Agents: An Illustrated Primer](https://voiceaiandvoiceagents.com/) | Long-form guide | RG 4, PP 2 |
| [Building Effective Voice Agents (OpenAI, AI Engineer 2025)](https://www.youtube.com/watch?v=-OXiljTJxQU) | Talk | RG 5, PP 3 |
| [Designing Voice Agents for Real Conversations (AWS, AI Engineer 2026)](https://www.youtube.com/watch?v=hMlLw1LeIK8) | Talk | RG 10, PP 2 |
| [Engineering voice agents: latency, quality, and scale (Together AI)](https://www.youtube.com/watch?v=N7b1PJc7SFc) | Talk | RG 23 |
| [Building AI Voice Agents for Production (DeepLearning.AI × LiveKit)](https://www.deeplearning.ai/courses/building-ai-voice-agents-for-production) | Course | RG 25 |
| [ITU-T G.114: One-way transmission time](https://www.itu.int/rec/T-REC-G.114) | Standard | Architecture explorer |

## OpenAI Realtime

| Source | Type | Cited in |
|---|---|---|
| [Advancing voice intelligence with new models in the API (gpt-realtime-2)](https://openai.com/index/advancing-voice-intelligence-with-new-models-in-the-api/) | Announcement | RG 7, PP 3 |
| [Voice agents guide](https://developers.openai.com/api/docs/guides/voice-agents) | Docs | RG 8, PP 3 |
| [Realtime API guide](https://developers.openai.com/api/docs/guides/realtime) (also linked at its older [platform.openai.com address](https://platform.openai.com/docs/guides/realtime), which redirects) | Docs | RG 13, RL, PP 3 |
| [WebSockets guide, GPT-Live section](https://developers.openai.com/api/docs/guides/voice-websockets?api=live) | Docs | Build your own voice agent |
| [Agents SDK (Python): voice pipeline](https://openai.github.io/openai-agents-python/voice/pipeline/) | Docs | Build your own voice agent |
| [Guardrails and human review](https://developers.openai.com/api/docs/guides/agents/guardrails-approvals) | Docs | Tools and guardrails |
| [Agents SDK (Python): tools](https://openai.github.io/openai-agents-python/tools/) | Docs | Tools and guardrails |
| [Build more natural voice experiences with GPT-Live-1 in the API](https://openai.com/index/introducing-gpt-live-1-in-the-api/) | Announcement | RG 7A, PP 3, GPT-Live doc |
| [Getting started with GPT-Live](https://developers.openai.com/api/docs/guides/live) | Docs | RG 7A, GPT-Live doc |
| [Delegation and tools in GPT-Live](https://developers.openai.com/api/docs/guides/live-delegation) | Docs | RG 7A, PP 3, GPT-Live doc |
| [Voice cost optimization, Realtime tab (audio tokens per second, session context)](https://developers.openai.com/api/docs/guides/voice-latency-cost?voice-api=realtime) | Docs | Architecture explorer |
| [GPT-6 Luna model page](https://developers.openai.com/api/docs/models/gpt-6-luna) | Model docs | Architecture explorer |
| [GPT-6 Astra model page](https://developers.openai.com/api/docs/models/gpt-6-astra) | Model docs | Architecture explorer |
| [GPT-4o Mini TTS model page (marked deprecated)](https://developers.openai.com/api/docs/models/gpt-4o-mini-tts) | Model docs | Architecture explorer |
| [Community estimates of TTS cost per minute (users, not OpenAI)](https://community.openai.com/t/new-tts-api-pricing-and-gotchas/1150616) | Forum | Architecture explorer |
| [GPT-Live 1 model page](https://developers.openai.com/api/docs/models/gpt-live-1) | Model docs | GPT-Live doc, speech-to-speech doc |
| [Prompting GPT-Live](https://developers.openai.com/api/docs/guides/live-prompting) | Docs | GPT-Live doc |
| [Managing GPT-Live sessions](https://developers.openai.com/api/docs/guides/live-conversations) | Docs | GPT-Live doc |
| [Migrate to GPT-Live](https://developers.openai.com/api/docs/guides/live-migration) | Docs | GPT-Live doc |
| [GPT-Live partner integrations](https://developers.openai.com/api/docs/guides/live-partner-integrations) | Docs | GPT-Live doc |
| [GPT-Realtime-2.1 model page](https://developers.openai.com/api/docs/models/gpt-realtime-2.1) | Model docs | Speech-to-speech doc |
| [GPT-Realtime-2.1 Mini model page](https://developers.openai.com/api/docs/models/gpt-realtime-2.1-mini) | Model docs | Speech-to-speech doc |
| [GPT-Realtime-2 model page](https://developers.openai.com/api/docs/models/gpt-realtime-2) | Model docs | Speech-to-speech doc |
| [GPT-Realtime-Whisper model page](https://developers.openai.com/api/docs/models/gpt-realtime-whisper) | Model docs | Speech-to-speech doc |
| [GPT-Live-Transcribe model page](https://developers.openai.com/api/docs/models/gpt-live-transcribe) | Model docs | Speech-to-speech doc |
| [Realtime transcription guide](https://developers.openai.com/api/docs/guides/realtime-transcription) | Docs | Speech-to-speech doc |
| [Realtime conversations guide](https://developers.openai.com/api/docs/guides/realtime-conversations) | Docs | Speech-to-speech doc |
| [GPT-Live-Transcribe and GPT-Transcribe: Two New Transcription Models in the API](https://community.openai.com/t/gpt-live-transcribe-and-gpt-transcribe-two-new-transcription-models-in-the-api/1388318) | Announcement | Speech-to-speech doc |
| [DataCamp: GPT-Live-1 API tutorial](https://www.datacamp.com/tutorial/gpt-live-1-api) | Tutorial (third-party) | GPT-Live doc |
| [DataCamp: GPT-Realtime-2 API tutorial](https://www.datacamp.com/tutorial/gpt-realtime-2-api) | Tutorial (third-party) | Speech-to-speech doc |
| [DataCamp: GPT Live Transcribe API tutorial](https://www.datacamp.com/tutorial/gpt-live-transcribe-api) | Tutorial (third-party) | Speech-to-speech doc |
| [GPT-Realtime-Translate model page](https://developers.openai.com/api/docs/models/gpt-realtime-translate) | Model docs | Speech-to-speech doc |
| [gpt-realtime-2.1 release announcement](https://community.openai.com/t/new-realtime-models-on-the-api-gpt-realtime-2-1-and-gpt-realtime-2-1-mini/1385896) | Announcement | Speech-to-speech doc |
| [OpenAI API changelog](https://developers.openai.com/api/docs/changelog) | Changelog | Speech-to-speech doc |
| [Hello GPT-4o](https://openai.com/index/hello-gpt-4o/) | Announcement | Speech-to-speech doc |
| [Realtime API reference](https://developers.openai.com/api/reference/resources/realtime) | API reference | RL |
| [Realtime prompting guide](https://developers.openai.com/cookbook/examples/realtime_prompting_guide) | Cookbook | RG 14, PP 3 |

## LiveKit

| Source | Type | Cited in |
|---|---|---|
| [Agents framework](https://docs.livekit.io/agents/) | Docs | RG 11, RL |
| [Agent Builder](https://docs.livekit.io/agents/start/builder/) | Docs | LiveKit hands-on |
| [Agent Builder product page](https://livekit.com/products/agent-builder) | Product page | LiveKit hands-on |
| [Turn-taking tuning (endpointing defaults)](https://docs.livekit.io/agents/logic/turns/tuning/) | Docs | Architecture explorer |
| [Voice AI quickstart](https://docs.livekit.io/agents/start/voice-ai/) | Docs | LiveKit hands-on |
| [agent-starter-python](https://github.com/livekit-examples/agent-starter-python) | Template repo | LiveKit hands-on |
| [uv (Python package manager)](https://docs.astral.sh/uv/) | Docs | LiveKit hands-on |
| [Turns overview](https://docs.livekit.io/agents/logic/turns/) | Docs | RG 11, RL, PP 2 |
| [Telephony](https://docs.livekit.io/telephony/) | Docs | RL |
| [Using a transformer to improve end-of-turn detection](https://livekit.com/blog/using-a-transformer-to-improve-end-of-turn-detection) | Blog | RG 12, PP 2 |
| [Build Production-Ready Voice AI Agents (LiveKit)](https://www.youtube.com/watch?v=Axg9TNZ5038) | Video (LiveKit 101) | PP 10 |
| [Give Your Voice AI Personality and Failover Protection (LiveKit)](https://www.youtube.com/watch?v=Hj3cZIeB1nc) | Video (LiveKit 101) | PP 10 |
| [LiveKit CLI install script](https://get.livekit.io/cli) | Install script | LiveKit hands-on |
| [LiveKit 101: Build Production-Ready Voice AI Agents](https://www.youtube.com/playlist?list=PLWx-Xa8RhJxXuv8fu2Qz9rj2MPb4qgXir) | Official video course playlist | RG 11A, PP 10 |
| [Voice Agent Pipeline Explained: VAD, STT, LLM & TTS (LiveKit)](https://www.youtube.com/watch?v=SPB2T-eLrOg) | Talk (video 2 of LiveKit 101) | RG 11B, PP 10 |
| [Fix AI Voice Interruptions with Semantic Turn Detection (LiveKit)](https://www.youtube.com/watch?v=XbrlOY4Z-Ow) | Video (LiveKit 101) | RG 11C |
| [Deploy Voice AI Agents to Production with Full Observability (LiveKit)](https://www.youtube.com/watch?v=KENbu2e7myY) | Video (LiveKit 101) | RG 11C |
| [Production Voice AI Workflows: Consent and Escalations (LiveKit)](https://www.youtube.com/watch?v=bc9kI5TRhX4) | Video (LiveKit 101) | RG 11C |
| [Connect Voice Agents to External Services with MCP (LiveKit)](https://www.youtube.com/watch?v=lOACxaBLwSI) | Video (LiveKit 101) | RG 11C |

## Agents and orchestration (LangChain / LangGraph)

| Source | Type | Cited in |
|---|---|---|
| [Building Effective Agents (Anthropic)](https://www.anthropic.com/engineering/building-effective-agents) | Essay | RG 9, PP 4 |
| [LangChain and LangGraph 1.0](https://blog.langchain.com/langchain-langgraph-1dot0/) | Blog | RG 18, PP 4 |
| [LangChain agents](https://docs.langchain.com/oss/python/langchain/agents) | Docs | RL |
| [LangChain middleware](https://docs.langchain.com/oss/python/langchain/middleware) | Docs | RG 19, PP 4 |
| [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview) | Docs | RL |
| [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence) | Docs | RL |
| [LangGraph durable execution (Checkpointers: durability modes)](https://docs.langchain.com/oss/python/langgraph/checkpointers#durability-modes) | Docs | RG 20, PP 4 |
| [LangGraph interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts) | Docs | RG 20, PP 4 |

## Evaluation and observability

| Source | Type | Cited in |
|---|---|---|
| [Your AI Product Needs Evals (Hamel Husain)](https://hamel.dev/blog/posts/evals/) | Blog | RG 6, PP 5 |
| [A Field Guide to Rapidly Improving AI Products (Hamel Husain)](https://hamel.dev/blog/posts/field-guide/) | Blog | RG 15, PP 5 |
| [Using LLM-as-a-Judge (Hamel Husain)](https://hamel.dev/blog/posts/llm-judge/) | Blog | RG 22, PP 5 |
| [LangSmith evaluation concepts](https://docs.langchain.com/langsmith/evaluation-concepts) | Docs | RG 21, PP 5 |
| [LangSmith evaluation](https://docs.langchain.com/langsmith/evaluation) | Docs | RL, WP 08, 14 |
| [LangSmith observability concepts](https://docs.langchain.com/langsmith/observability-concepts) | Docs | RG 21, PP 5 |
| [What Is LangSmith? Explained in 5 Minutes (LangChain)](https://www.youtube.com/watch?v=kYtnLaJeia8) | Video | RG 14A |
| [Getting Started with LangSmith (1/8): Tracing](https://www.youtube.com/watch?v=fA9b4D8IsPQ) | Video | RG 14A, PP 5 |
| [Getting Started with LangSmith (2/8): Types of Runs](https://www.youtube.com/watch?v=WplpUxEyl9o) | Video | RG 14A |
| [Getting Started with LangSmith (3/8): Debugging with Studio](https://www.youtube.com/watch?v=NJXu-4nDo50) | Video | RG 14A (optional) |
| [Getting Started with LangSmith (4/8): Playground & Prompts](https://www.youtube.com/watch?v=h4f6bIWGkog) | Video | RG 14A (optional) |
| [Getting Started with LangSmith (5/8): Datasets & Evaluations](https://www.youtube.com/watch?v=iEgjJyk3aTw) | Video | RG 14A, PP 5 |
| [Getting Started with LangSmith (6/8): Annotation Queues](https://www.youtube.com/watch?v=rxKYHA-2KS0) | Video | RG 14A (optional) |
| [Getting Started with LangSmith (7/8): Automations & Online Evaluation](https://www.youtube.com/watch?v=z69cBXTJFZ0) | Video | RG 14A |
| [Getting Started with LangSmith (8/8): Dashboards](https://www.youtube.com/watch?v=VxsIvf9NdxI) | Video | RG 14A (optional) |
| [LangSmith observability](https://docs.langchain.com/langsmith/observability) | Docs | RL |
| [Patterns for Building LLM-based Systems & Products (Eugene Yan)](https://eugeneyan.com/writing/llm-patterns/) | Essay | RG 24 |

## Research papers

| Source | Type | Cited in |
|---|---|---|
| [τ-bench: tool-agent-user interaction in real-world domains](https://arxiv.org/abs/2406.12045) ([PDF](https://arxiv.org/pdf/2406.12045)) | Paper (2024) | RG 16, PP 5 |
| [τ²-bench: conversational agents in a dual-control environment](https://arxiv.org/abs/2506.07982) ([PDF](https://arxiv.org/pdf/2506.07982)) | Paper (2025) | RG 17, PP 5 |
| [Moshi: a speech-text foundation model for real-time dialogue](https://arxiv.org/abs/2410.00037) | Paper (2024) | RG 26 |

## Regulation and public safety

| Source | Type | Cited in |
|---|---|---|
| [EPA Section 608](https://www.epa.gov/section608) | Government | WP 10, 12, Appendix A |
| [PCI DSS](https://www.pcisecuritystandards.org/standards/pci-dss/) | Standard overview | WP 10, 12 |
| [California DOJ CCPA FAQ](https://oag.ca.gov/privacy/ccpa) | Government FAQ | WP 10, 12 |

## Background

| Source | Type | Cited in |
|---|---|---|
| [Software Is Changing (Again) (Andrej Karpathy)](https://www.youtube.com/watch?v=LCEmiRjPEtQ) | Talk | RG 27 |

## Background whitepaper (primary and secondary sources)

| Source | Type | Cited in |
|---|---|---|
| <https://buildops.com/> | Company page | Whitepaper |
| <https://docs.fcc.gov/public/attachments/FCC-24-17A1.pdf> | Regulator | Whitepaper |
| <https://en.wikipedia.org/wiki/ServiceTitan> | Press / analyst | Whitepaper |
| <https://fieldedge.com/> | Company page | Whitepaper |
| <https://finance.yahoo.com/news/servicetitan-q4-earnings-call-highlights-031828218.html> | Press / analyst | Whitepaper |
| <https://infobytes.orrick.com/2025-04-25/utah-enacts-ai-disclosure-law-for-consumer-transactions> | Legal analysis | Whitepaper |
| <https://investors.servicetitan.com/news-releases/news-release-details/servicetitan-announces-fiscal-fourth-quarter-and-full-year> | Company page | Whitepaper |
| <https://servicetitan.com/press/servicetitan-announces-ipo-pricing> | Company page | Whitepaper |
| <https://viirtue.com/call-recording-consent-laws-by-state-2026-guide/> | Legal analysis | Whitepaper |
| <https://wsgr.com/en/insights/fcc-rules-ai-generated-voices-are-artificial-under-the-tcpa.html> | Legal analysis | Whitepaper |
| <https://www.avoca.ai/> | Company page | Whitepaper |
| <https://www.bls.gov/ooh/construction-and-extraction/plumbers-pipefitters-and-steamfitters.htm> | Government data | Whitepaper |
| <https://www.bls.gov/ooh/installation-maintenance-and-repair/heating-air-conditioning-and-refrigeration-mechanics-and-installers.htm> | Government data | Whitepaper |
| <https://www.cnbc.com/2024/12/12/servicetitan-starts-trading-on-nasdaq-after-ipo.html> | Press / analyst | Whitepaper |
| <https://www.fool.com/earnings/call-transcripts/2026/03/12/servicetitan-ttan-q4-2026-earnings-transcript/> | Press / analyst | Whitepaper |
| <https://www.fortune.com/2026/04/27/avoca-ai-agents-missed-calls-hvac-plumbing-roofing-kleiner-perkins-chen-shrivastava-braswell/> | Press / analyst | Whitepaper |
| <https://www.housecallpro.com/> | Company page | Whitepaper |
| <https://www.investing.com/news/company-news/servicetitan-q4-fy26-slides-21-revenue-growth-path-to-25-margins-93CH-4558725> | Press / analyst | Whitepaper |
| <https://www.jobnimbus.com/> | Company page | Whitepaper |
| <https://www.justia.com/50-state-surveys/recording-phone-calls-and-conversations/> | Legal analysis | Whitepaper |
| <https://www.kleinerperkins.com/perspectives/avoca-bringing-ai-to-the-backbone-of-the-real-economy/> | Company page | Whitepaper |
| <https://www.sec.gov/Archives/edgar/data/0001638826/000163882626000044/ttan-ex99_1.htm> | SEC filing | Whitepaper |
| <https://www.sec.gov/Archives/edgar/data/1638826/000119312524277099/d577298d424b4.htm> | SEC filing | Whitepaper |
| <https://www.sec.gov/Archives/edgar/data/1638826/000163882626000009/ttan-ex99_1.htm> | SEC filing | Whitepaper |
| <https://www.sec.gov/Archives/edgar/data/1638826/000163882626000028/ttan-20260131.htm> | SEC filing | Whitepaper |
| <https://www.sec.gov/Archives/edgar/data/1638826/000163882626000093/ttan-ex99_1.htm> | SEC filing | Whitepaper |
| <https://www.twilio.com/docs/messaging/compliance/a2p-10dlc> | Company page | Whitepaper |

## Books

| Source | Type | Cited in |
|---|---|---|
| Michael D. Watkins, *The First 90 Days, Updated and Expanded* (Harvard Business Review Press, 2013; ISBN 9781422188613) | Book | First 90 days playbook |
| Camille Fournier, *The Manager's Path* (O'Reilly, 2017) | Book | Manager guide |

## Pantheon 2026

| Source | Type | Cited in |
|---|---|---|
| [ServiceTitan Announcing New and Expanded Capabilities at Pantheon 2026](https://www.globenewswire.com/news-release/2026/10/06/3375320/0/en/servicetitan-announcing-new-and-expanded-capabilities-at-pantheon-2026.html) | Press release | RG 7B, Pantheon brief |
| [ServiceTitan at Pantheon 2026 (keynote summary and transcript)](https://www.investing.com/news/transcripts/servicetitan-at-pantheon-2026-ai-push-aims-to-make-trades-selfrunning-93CH-4934737) | Transcript | RG 7B, Pantheon brief |
| [Pantheon 2026: Live coverage from ServiceTitan](https://www.servicetitan.com/blog/pantheon-2026-live-coverage) | Live blog | Pantheon brief |
| [Get ready for Voice Intelligence with ServiceTitan Calls](https://help.servicetitan.com/release-hub/docs/coming-soon-get-ready-for-voice-intelligence-in-servicetitan-core) | Help center (company claim) | Hypothesis map, business metrics, claims ledger |
| [Book jobs from your website with Webchat in Virtual Agent](https://help.servicetitan.com/release-hub/docs/book-jobs-from-your-website-with-webchat-in-virtual-agent) | Help center (company claim) | Hypothesis map, claims ledger |
| [An introduction to ServiceTitan Max: what it is and why it matters](https://help.servicetitan.com/docs/an-introduction-to-servicetitan-max-what-it-is-and-why-it-matters) | Help center (company claim) | Hypothesis map, claims ledger |

## Working with your manager

| Source | Type | Cited in |
|---|---|---|
| [Questions for our first 1:1 (Lara Hogan)](https://larahogan.me/blog/first-one-on-one-questions/) | Essay | RG 14B, PP 6, manager guide |
| [Get your work recognized: write a brag document (Julia Evans)](https://jvns.ca/blog/brag-documents/) | Essay | RG 14C, manager guide, brag template |
| [Staying aligned with authority (Will Larson)](https://staffeng.com/guides/staying-aligned-with-authority/) | Essay | RG 14D, PP 6, manager guide |
| [Work on what matters (Will Larson)](https://staffeng.com/guides/work-on-what-matters/) | Essay | RG 14E, manager guide |
| [When your manager isn't supporting you, build a Voltron (Lara Hogan)](https://larahogan.me/blog/manager-voltron/) | Essay | RG 14F, manager guide |
| [Radical Candor: our approach (Kim Scott)](https://www.radicalcandor.com/our-approach/) | Web page | Manager guide |

## Explainer series

| Source | Type | Cited in |
|---|---|---|
| [Voice Agents from First Principles release](https://github.com/sp7412/onboarding/releases/tag/explainer-series) | Original local explainer series | Reading guide item 0 |
| [Interactive Educator](https://github.com/Wamikmk/interactive-educator) | Pedagogy inspiration, CC BY 4.0 | Interactive lessons |

## Onboarding practice

| Source | Type | Cited in |
|---|---|---|
| [Setting Goals With Your New Manager](https://raw.githubusercontent.com/sp7412/onboarding/main/docs/manager-alignment.md) | Repo guide | PP 6 |
| [Path to Integration, this repo's published site](https://sp7412.github.io/onboarding/) (including the [earned-autonomy lesson](https://sp7412.github.io/onboarding/lessons/earned-autonomy/) and [value calculator](https://sp7412.github.io/onboarding/value-calculator/)) | Companion site | README, checklist, earning autonomy, business metrics |
| [notebooklm-mcp-cli (`nlm`, unofficial)](https://github.com/jacob-bd/notebooklm-mcp-cli) | Open-source CLI | Podcast prompts |

## Agentic orchestration

| Source | Type | Cited in |
|---|---|---|
| [Agentforce Multi-Agent Orchestration](https://www.salesforce.com/agentforce/multi-agent-orchestration/) | Vendor architecture | Whitepaper 15 |
| [Salesforce SOMA, MOMA, MCP, A2A and Agent Gateway](https://help.salesforce.com/s/articleView?id=005317683&language=en_US&type=1) | Vendor architecture/docs | Whitepaper 15 |
| [Microsoft Agent Framework](https://github.com/microsoft/agent-framework) | Open-source framework | Whitepaper 15 |
| [Microsoft Agent Framework overview (agents vs. workflows)](https://learn.microsoft.com/agent-framework/overview/) | Microsoft documentation | Whitepaper 15 |
| [Workflow orchestrations in Agent Framework](https://learn.microsoft.com/agent-framework/workflows/orchestrations) | Microsoft documentation | Whitepaper 15 |
| [LangGraph](https://github.com/langchain-ai/langgraph) | Open-source framework | Whitepaper 15 |
| [Microsoft Agent Framework: agent harness](https://learn.microsoft.com/en-us/agent-framework/concepts/harness) | Microsoft documentation | Comparative architectures, agent harness |
| [Microsoft Agent Framework overview (en-us path)](https://learn.microsoft.com/en-us/agent-framework/overview/) | Microsoft documentation | Comparative architectures, agent harness |
| [Microsoft Agent Framework: evaluation](https://learn.microsoft.com/agent-framework/agents/evaluation) | Microsoft documentation | Comparative architectures, design by evaluation |
| [OpenAI Agents SDK (Python): tracing](https://openai.github.io/openai-agents-python/tracing/) | Docs | Comparative architectures, agent harness |
| [OpenAI: evaluate agent workflows](https://developers.openai.com/api/docs/guides/agent-evals) | Docs | Comparative architectures, design by evaluation |
| [Anthropic: Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) | Engineering essay (Jan 2026) | Comparative architectures, design by evaluation |
| [Model Context Protocol specification, revision 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28) | Protocol specification | Whitepaper 15, glossary |
| [A2A (Agent2Agent) Protocol specification](https://a2a-protocol.org/latest/specification/) | Protocol specification | Whitepaper 15, glossary |
| [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview) | Documentation | Whitepaper 15 |
| [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence) | Documentation | Whitepaper 15 |
| [LangGraph durable execution (Checkpointers: durability modes)](https://docs.langchain.com/oss/python/langgraph/checkpointers#durability-modes) | Documentation | Whitepaper 15 |
| [LangGraph interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts) | Documentation | Whitepaper 15 |
| [LangChain agents](https://docs.langchain.com/oss/python/langchain/agents) | Documentation | Whitepaper 15 |
| [ServiceTitan job listing: Engineering Manager, Data Foundations](https://servicetitan.wd1.myworkdayjobs.com/en-US/ServiceTitan/job/Manager--Software-Engineering_JR114911) | Job listing (expires) | Whitepaper 15 |
| [ServiceTitan job listing on Built In: Staff Product Manager, Communications Intelligence](https://builtin.com/job/staff-product-manager-communications-intelligence/10448969) | Job listing (expires) | Whitepaper 15 |
| [ServiceTitan Help: Configure your Voice Agent settings in Contact Center Pro](https://help.servicetitan.com/docs/configure-your-voice-agent-settings) | Help center (company claim) | Whitepaper 16 |

## Maintaining this page
- Add a row whenever a new external link appears anywhere in the repo.
- Link-check before committing; never construct URLs from a site's naming pattern.
- Public sources only. No internal ServiceTitan material.
