# Claims Ledger

Checked September 27, 2026. `partial` means the source supports a narrower statement
than an unrestricted claim. Unsupported generalizations are retained here as gaps and
are not stated as facts in the chapters.

| Claim | Chapter | URL | Date checked | Supported | Notes |
|---|---:|---|---|---|---|
| Founders describe building the company to help their fathers' contracting businesses. | 01 | https://www.servicetitan.com/company | 2026-09-27 | partial | Company-authored origin story. |
| IPO prospectus describes ServiceTitan as founded in 2012. | 01 | https://www.sec.gov/Archives/edgar/data/1638826/000119312524277099/d577298d424b4.htm | 2026-09-30 | unverified | SEC returned HTTP 403 through the configured proxy; claim retained as explicitly attributed and requires direct filing review. |
| Company page states more than 11,800 trade customers. | 01 | https://www.servicetitan.com/company | 2026-09-27 | partial | Company-reported; no independent denominator on page. |
| Public product catalog presents offerings for contractors across multiple industries. | 01 | https://www.servicetitan.com/products | 2026-09-27 | yes | Public catalog positioning. |
| Public industries page lists commercial and residential contractor categories. | 02 | https://www.servicetitan.com/industries | 2026-09-27 | yes | Category list, not market-size evidence. |
| Public pages describe availability and dispatch inputs including capacity, skills, location, and drive time. | 03 | https://www.servicetitan.com/features/pro/scheduling | 2026-09-27 | partial | Product positioning; implementation boundaries unknown. |
| Contact Center Pro describes centralized, multi-location calls linked to jobs. | 04 | https://www.servicetitan.com/features/pro/contact-center | 2026-09-27 | yes | Product-page claim. |
| AI Virtual Agent is positioned for overflow/after-hours booking, confirmation, rescheduling, and escalation. | 04 | https://www.servicetitan.com/features/pro/contact-center | 2026-09-27 | yes | Product-page claim. |
| Bonney Plumbing case study reports fewer missed calls and increased bookings. | 04, 05 | https://www.servicetitan.com/features/pro/contact-center | 2026-09-27 | partial | Customer-reported/vendor-presented; not a general benchmark. |
| General call mix, CSR turnover, missed-call cost, labor shortage, and market sizes. | 02, 04, 05 | [unverified] | 2026-09-27 | no | Omitted from factual prose pending verified sources. |
| Internal architecture, owners, pricing, adoption, roadmap, and KPI SQL. | 01-05 | [unverified] | 2026-09-27 | no | Post-joining validation questions only. |
| Public catalog groups capabilities across products for commercial and residential trades. | 06 | https://www.servicetitan.com/products | 2026-09-27 | yes | Catalog positioning, not implementation boundary. |
| Atlas is publicly positioned for conversational answers and field assistance; some office capabilities are marked coming soon. | 06, 13 | https://www.servicetitan.com/features/atlas | 2026-09-27 | yes | Current public page language; not a private roadmap. |
| AI Virtual Agent is publicly positioned for capacity-aware booking, confirmation, rescheduling, and live escalation. | 07 | https://www.servicetitan.com/features/pro/virtual-agent | 2026-09-27 | yes | Product positioning; performance not independently established. |
| LiveKit documents realtime agents, tools, turn detection, handoffs, telephony, and lifecycle abstractions. | 08 | https://docs.livekit.io/agents/ | 2026-09-27 | yes | Technology documentation, not a deployment claim. |
| LangGraph documents deterministic and agentic orchestration with persistence and human-in-the-loop support. | 08 | https://docs.langchain.com/oss/python/langgraph/overview | 2026-09-27 | yes | Framework documentation. |
| LangSmith documents offline and online evaluation workflows. | 08, 14 | https://docs.langchain.com/langsmith/evaluation | 2026-09-27 | yes | Platform documentation. |
| EPA Section 608 includes certification, refrigerant, recordkeeping, and reporting material. | 10, 12 | https://www.epa.gov/section608 | 2026-09-27 | yes | General public education; legal design requires review. |
| PCI DSS provides baseline technical and operational requirements for payment account data security. | 10, 12 | https://www.pcisecuritystandards.org/standards/pci-dss/ | 2026-09-27 | yes | Scope and compliance status are organization-specific. |
| California DOJ describes CCPA consumer rights and covered-business responsibilities. | 10, 12 | https://oag.ca.gov/privacy/ccpa | 2026-09-27 | yes | General education; applicability requires legal review. |
| Complete competitor map, ranking, pricing, win/loss, and differentiation. | 09 | [unverified] | 2026-09-27 | no | Deliberately omitted pending individual source verification. |

## Research pass, September 27, 2026

Added when chapters 01, 02, 06, 07, 09, 10, 11 and Appendix A were rebuilt. Earlier `no` rows for
market size, labor shortage, recording consent, TCPA and competitors are superseded by the rows below.

| Claim | Chapter | URL | Date checked | Supported | Notes |
|---|---:|---|---|---|---|
| ~10,800 Active Customers as of Jan 31, 2026; definition (>$10k annualized billings; >97% of billings) | 01, 11 | https://www.sec.gov/Archives/edgar/data/1638826/000163882626000028/ttan-20260131.htm | 2026-09-27 | yes | 10-K Business |
| GTV $82.1B fiscal 2026 and $68.5B fiscal 2025 | 01, 11 | https://www.sec.gov/Archives/edgar/data/1638826/000163882626000028/ttan-20260131.htm | 2026-09-27 | yes | 10-K MD&A |
| Core / FinTech / Pro structure and Core workflow list | 01, 06 | https://www.sec.gov/Archives/edgar/data/1638826/000163882626000028/ttan-20260131.htm | 2026-09-27 | yes | 10-K Business |
| Gross dollar retention >95% in fiscal 2024–2026 | 01 | https://www.sec.gov/Archives/edgar/data/1638826/000163882626000028/ttan-20260131.htm | 2026-09-27 | yes |  |
| Share of wallet defined as portion of customer GTV earned | 01 | https://www.sec.gov/Archives/edgar/data/1638826/000163882626000028/ttan-20260131.htm | 2026-09-27 | yes | ~1.2% is Analysis from revenue/GTV |
| Atlas introduced in fiscal 2026 as agentic AI layer, evolution of Titan Intelligence | 01, 06 | https://www.sec.gov/Archives/edgar/data/1638826/000163882626000028/ttan-20260131.htm | 2026-09-27 | yes |  |
| Virtual Agents handle overflow and after-hours calls to book, reschedule, confirm | 06, 07 | https://www.sec.gov/Archives/edgar/data/1638826/000163882626000028/ttan-20260131.htm | 2026-09-27 | yes |  |
| Phones Pro: VoIP routing, CSR attribution, abandonment/duration KPIs, transcripts, escalation alerts | 04, 06, 11 | https://www.sec.gov/Archives/edgar/data/1638826/000163882626000028/ttan-20260131.htm | 2026-09-27 | yes |  |
| Contact Center Pro: omnichannel, multi-location, AI-powered, Universal Inbox | 06 | https://www.sec.gov/Archives/edgar/data/1638826/000163882626000028/ttan-20260131.htm | 2026-09-27 | yes |  |
| Second Chance Leads uses AI on unbooked calls | 04, 05, 06 | https://www.sec.gov/Archives/edgar/data/1638826/000163882626000028/ttan-20260131.htm | 2026-09-27 | yes |  |
| Convex and Conduit Tech descriptions | 01, 06 | https://www.sec.gov/Archives/edgar/data/1638826/000163882626000028/ttan-20260131.htm | 2026-09-27 | yes |  |
| Customers range to franchise aggregations >$1B GTV; owner is key decision maker | 01, 02 | https://www.sec.gov/Archives/edgar/data/1638826/000163882626000028/ttan-20260131.htm | 2026-09-27 | yes |  |
| Competition types and ten named example vendors | 09 | https://www.sec.gov/Archives/edgar/data/1638826/000163882626000028/ttan-20260131.htm | 2026-09-27 | yes | Vendors not assigned to types in the 10-K |
| Competitors may adopt AI faster (risk factor) | 09 | https://www.sec.gov/Archives/edgar/data/1638826/000163882626000028/ttan-20260131.htm | 2026-09-27 | yes |  |
| Demand peaks fiscal Q2 (summer); extreme weather raises demand | 02, 04, 05, 11 | https://www.sec.gov/Archives/edgar/data/1638826/000163882626000028/ttan-20260131.htm | 2026-09-27 | yes | 10-K Seasonality |
| TCPA restrictions named as regulatory risk | 01, 10 | https://www.sec.gov/Archives/edgar/data/1638826/000163882626000028/ttan-20260131.htm | 2026-09-27 | yes |  |
| Industry consolidation and labor shortages named as risk factors | 01, 02 | https://www.sec.gov/Archives/edgar/data/1638826/000163882626000028/ttan-20260131.htm | 2026-09-27 | yes |  |
| Q2 FY27: revenue $292.8M (+21%), platform $284.5M, GTV $26.8B (+17%), subscription $212.4M, usage $72.1M | 01, 02, 11 | https://www.sec.gov/Archives/edgar/data/1638826/000163882626000093/ttan-ex99_1.htm | 2026-09-27 | yes | 8-K Ex. 99.1 |
| Q2 FY27: non-GAAP op margin 15.2%, non-GAAP FCF $50.5M, GAAP op loss $27.6M, R&D $100.6M vs S&M $77.0M | 01 | https://www.sec.gov/Archives/edgar/data/1638826/000163882626000093/ttan-ex99_1.htm | 2026-09-27 | yes |  |
| FY27 guidance revenue $1,139–1,144M; non-GAAP op income $152–154M | 01 | https://www.sec.gov/Archives/edgar/data/1638826/000163882626000093/ttan-ex99_1.htm | 2026-09-27 | yes |  |
| >700 enrolled Max locations expected by FY27 end; 'Agentic Operating System' | 01, 06 | https://www.sec.gov/Archives/edgar/data/1638826/000163882626000093/ttan-ex99_1.htm | 2026-09-27 | yes |  |
| NDR >110% | 01 | https://www.sec.gov/Archives/edgar/data/1638826/000163882626000093/ttan-ex99_1.htm | 2026-09-27 | yes |  |
| Q1 FY27 GTV $21.7B | 02 | https://www.sec.gov/Archives/edgar/data/0001638826/000163882626000044/ttan-ex99_1.htm | 2026-09-27 | yes |  |
| FY26 revenue ~$961M (+24%), FCF ~$85M, Max pilot outcomes (management-reported) | 01, 11 | https://finance.yahoo.com/news/servicetitan-q4-earnings-call-highlights-031828218.html | 2026-09-27 | yes | Secondary summary of call; Max outcomes attributed to management |
| Q4 FY26 GTV slowdown partly attributed to weather and one fewer business day | 02 | https://finance.yahoo.com/news/servicetitan-q4-earnings-call-highlights-031828218.html | 2026-09-27 | yes |  |
| New CTO Abhishek Mathur; internal AI adoption | 01 | https://www.fool.com/earnings/call-transcripts/2026/03/12/servicetitan-ttan-q4-2026-earnings-transcript/ | 2026-09-27 | yes | Transcript |
| IPO: 8.8M shares at $71, priced Dec 11, trading Dec 12, 2024 as TTAN | 01, A | https://servicetitan.com/press/servicetitan-announces-ipo-pricing | 2026-09-27 | yes |  |
| First-day close $101; ~$625M raised; ~$8.9B market value | 01, A | https://www.cnbc.com/2024/12/12/servicetitan-starts-trading-on-nasdaq-after-ipo.html | 2026-09-27 | yes |  |
| ~$1.5T annual trades spend in U.S. and Canada (company estimate); trades served; FieldRoutes and Aspire | 01, 02, 06 | https://www.sec.gov/Archives/edgar/data/1638826/000119312524277099/d577298d424b4.htm | 2026-09-27 | yes | Prospectus estimate |
| ~9,500 Active Customers as of Jan 31, 2025 | 01, A | https://investors.servicetitan.com/news-releases/news-release-details/servicetitan-announces-fiscal-fourth-quarter-and-full-year | 2026-09-27 | yes | Site blocks automated fetch; content confirmed via search index |
| HVACR: +8% 2024–34, ~40,100 openings/yr, median $59,810 (May 2024) | 02, 04, 05 | https://www.bls.gov/ooh/installation-maintenance-and-repair/heating-air-conditioning-and-refrigeration-mechanics-and-installers.htm | 2026-09-27 | yes | Site blocks automated fetch; confirmed via search index |
| Plumbers: +4% 2024–34, ~44,000 openings/yr, median $62,970 (May 2024); most states require licenses | 02, 04, 05, 10 | https://www.bls.gov/ooh/construction-and-extraction/plumbers-pipefitters-and-steamfitters.htm | 2026-09-27 | yes | Site blocks automated fetch; confirmed via search index |
| FCC 24-17: AI-generated human voices are 'artificial' under TCPA; prior express consent required absent emergency/exemption; no live-agent-equivalent carve-out | 10 | https://docs.fcc.gov/public/attachments/FCC-24-17A1.pdf | 2026-09-27 | yes | Primary source read |
| One-party federal baseline; majority one-party; all-party states list and 11–13 count variance | 10 | https://viirtue.com/call-recording-consent-laws-by-state-2026-guide/ | 2026-09-27 | partial | Vendor guide; cross-checked with Justia survey |
| Reasonable-expectation nuance; courts differ on interstate choice of law | 10 | https://www.justia.com/50-state-surveys/recording-phone-calls-and-conversations/ | 2026-09-27 | yes | Site blocks automated fetch; confirmed via search index |
| Utah SB 226: disclose on clear request; safe harbor for up-front disclosure; up to $2,500 per violation; effective May 7, 2025 | 10, A | https://infobytes.orrick.com/2025-04-25/utah-enacts-ai-disclosure-law-for-consumer-transactions | 2026-09-27 | yes |  |
| A2P 10DLC brand and campaign registration | 10 | https://www.twilio.com/docs/messaging/compliance/a2p-10dlc | 2026-09-27 | yes | Vendor documentation |
| Avoca: AI agents answering calls and booking for HVAC, plumbing, electrical, roofing | 07, 09 | https://www.avoca.ai/ | 2026-09-27 | yes | Company self-description |
| Avoca described as ~$1B Kleiner Perkins-backed; founders' missed-call framing | 07, 09, 11 | https://www.fortune.com/2026/04/27/avoca-ai-agents-missed-calls-hvac-plumbing-roofing-kleiner-perkins-chen-shrivastava-braswell/ | 2026-09-27 | yes |  |
| Kleiner Perkins describes Avoca's AI workforce for service businesses | 07 | https://www.kleinerperkins.com/perspectives/avoca-bringing-ai-to-the-backbone-of-the-real-economy/ | 2026-09-27 | yes | Investor perspective |
| Virtual Agent page capability list and quoted 80–85% booking rate testimonial | 06, 07, 11 | https://www.servicetitan.com/features/pro/virtual-agent | 2026-09-27 | yes | Testimonial, not benchmark |
| Vendor self-positioning (Housecall Pro, FieldEdge, JobNimbus, BuildOps) | 09 | https://www.housecallpro.com/ | 2026-09-27 | yes | Also fieldedge.com, jobnimbus.com, buildops.com page titles |
| PE consolidation networks targeted in go-to-market | 02 | https://www.investing.com/news/company-news/servicetitan-q4-fy26-slides-21-revenue-growth-path-to-25-margins-93CH-4558725 | 2026-09-27 | partial | Secondary; site blocks automated fetch |
| Convex acquisition month (April 2024) | A | https://en.wikipedia.org/wiki/ServiceTitan | 2026-09-27 | partial | Secondary source for date only |

## Research pass 2, September 28, 2026

Added when chapters 03, 04, 05, 08, 12, 13 and 14 were rewritten.

| Claim | Chapter | URL | Date checked | Supported | Notes |
|---|---:|---|---|---|---|
| Scheduling Pro availability shaped by buffers, arrival windows, blocked dates; follows job types, zones, capacity rules | 03, 05 | https://www.servicetitan.com/features/pro/scheduling | 2026-09-28 | yes | Product page and FAQ |
| Dispatch Pro weighs technician skills, recent sales performance, location, drive time, predicted job value | 03, 05 | https://www.servicetitan.com/features/pro/dispatch | 2026-09-28 | yes | Product page FAQ |
| Pro menu lists AI Virtual Agent, Marketing Pro, Contact Center Pro, Pricebook Pro, Fleet Pro, Scheduling Pro, Dispatch Pro, Field Pro (formerly Sales Pro) | 06 | https://www.servicetitan.com/features/pro/scheduling | 2026-09-28 | yes | Site navigation |
| Technician on-the-way notifications with photo and link; Pricebook with pictures, videos, warranties; Call Booking and Recording | 03, 04 | https://www.sec.gov/Archives/edgar/data/1638826/000163882626000028/ttan-20260131.htm | 2026-09-28 | yes | 10-K Business |
| gpt-realtime-2: reasoning with configurable effort, preambles, parallel tool calls, tool-failure recovery | 08, 13 | https://openai.com/index/advancing-voice-intelligence-with-new-models-in-the-api/ | 2026-09-28 | yes | Site blocks automated fetch; verified in earlier research and community announcement |
| LiveKit turn detection, interruptions; transformer end-of-turn model | 08 | https://livekit.com/blog/using-a-transformer-to-improve-end-of-turn-detection | 2026-09-28 | yes |  |
| τ-bench checks final database state and introduces pass^k; agents less consistent across repeats | 12 | https://arxiv.org/abs/2406.12045 | 2026-09-28 | yes | Paper abstract |
| Boilerplate: 'AI for the trades'; organizational velocity; Max doubled in Q2 | 13 | https://www.sec.gov/Archives/edgar/data/1638826/000163882626000093/ttan-ex99_1.htm | 2026-09-28 | yes |  |

## Verification pass, September 30, 2026

| Claim | Chapter | URL | Date checked | Supported | Notes |
|---|---:|---|---|---|---|
| Agent Builder prototypes browser agents, supports cascaded LiveKit Inference models, and does not support realtime-model plugins | 08 | https://docs.livekit.io/agents/start/builder/ | 2026-09-30 | yes | Current public documentation; realtime work belongs in the Python SDK path. |
| LiveKit Python quickstart uses `lk agent init`, `uv sync`, `AgentSession`, and supports realtime models through the OpenAI plugin | 08 | https://docs.livekit.io/agents/start/voice-ai/ | 2026-09-30 | yes | Current public documentation; local examples checked with livekit-agents 1.8.3. |
| LiveKit turn handling supports turn-detector, realtime-model, VAD, STT endpointing, and manual modes | 08 | https://docs.livekit.io/agents/logic/turns/ | 2026-09-30 | yes | Current public documentation. |
| OpenAI realtime model names, prices, context limits, modalities, and changelog dates in the speech-to-speech note | 08 | https://developers.openai.com/api/docs/models/gpt-realtime-2.1 | 2026-09-30 | unverified | Automated proxy-backed fetch returned HTTP 403; values remain source-attributed notes and were not guessed or changed. |

## GPT-Live-1 pass, September 30, 2026

| Claim | Chapter | URL | Date checked | Supported | Notes |
|---|---:|---|---|---|---|
| GPT-Live-1 released in the API Sept 10, 2026; full duplex; delegates reasoning and tools to a backend model | GPT-Live doc | https://openai.com/index/introducing-gpt-live-1-in-the-api/ | 2026-09-30 | yes | Primary announcement read directly |
| Model ID, audio/text modalities, Jul 31 2025 cutoff, v1/live/sessions endpoint, $0.05/min billed per second, concurrent-session limits 25/50/200 | GPT-Live doc | https://developers.openai.com/api/docs/models/gpt-live-1 | 2026-09-30 | yes | Model page read directly |
| Responses vs client delegation; instructions/thinking/commentary appends (500 tokens); app owns permissions and confirmations | GPT-Live doc | https://developers.openai.com/api/docs/guides/live-delegation | 2026-09-30 | yes | Guide read directly |
| Benchmarks (Full Duplex Bench +30 pts vs Realtime-2.1; turn-taking ~0.80 s vs ~1.41 s; Tau3 86.2% vs 45.7%) | GPT-Live doc | https://openai.com/index/introducing-gpt-live-1-in-the-api/ | 2026-09-30 | yes | Vendor-reported; labeled as such |
| gpt-realtime-2.1 modalities, 128k context, 32k output, text $4/$24 and audio $32/$64 per 1M tokens | S2S doc | https://developers.openai.com/api/docs/models/gpt-realtime-2.1 | 2026-09-30 | yes | Direct fetch; supersedes the proxy 403 "unverified" row |

## Pantheon 2026 pass, October 6, 2026

| Claim | Chapter | URL | Date checked | Supported | Notes |
|---|---:|---|---|---|---|
| Max available to all residential in-home contractors; limited commercial and roofing pilot; Atlas mobile app; Homh with ChatGPT, Gemini and Claude; AI CSRs get Adaptive Capacity | Pantheon brief, 01, 06, 13 | https://www.globenewswire.com/news-release/2026/10/06/3375320/0/en/servicetitan-announcing-new-and-expanded-capabilities-at-pantheon-2026.html | 2026-10-06 | yes | Official press release; forward-looking caveats noted |
| Five-level AI maturity model; voice agent evolution and voice-intelligence booking judge; 30 agents across 18 drivers; coordination system's five capabilities; learning loop; 700 Max locations expected by fiscal year-end | Pantheon brief | https://www.investing.com/news/transcripts/servicetitan-at-pantheon-2026-ai-push-aims-to-make-trades-selfrunning-93CH-4934737 | 2026-10-06 | yes | Third-party published transcript (AI-assisted, editor-reviewed); company claims attributed |



## First-90-days system guide pass, October 6, 2026

| Claim | Chapter | URL | Date checked | Supported | Notes |
|---|---|---|---|---|---|
| Voice Intelligence assesses each call, including whether it was a real opportunity to book, backed by transcript evidence, replacing CSR-picked call categories | Pantheon brief / business metrics | https://help.servicetitan.com/release-hub/docs/coming-soon-get-ready-for-voice-intelligence-in-servicetitan-core | 2026-10-06 | yes | ServiceTitan help documentation; company claim |
| Webchat booking is brought into Virtual Agent alongside voice and text interactions | Hypothesis map | https://help.servicetitan.com/release-hub/docs/book-jobs-from-your-website-with-webchat-in-virtual-agent | 2026-10-06 | yes | ServiceTitan help documentation; company claim |
| Max is described as using shared context and data across the business so agents can act in coordination | Hypothesis map | https://help.servicetitan.com/docs/an-introduction-to-servicetitan-max-what-it-is-and-why-it-matters | 2026-10-06 | yes | ServiceTitan help documentation; company claim |

## Transcription and GPT-Live operations pass, October 6, 2026

| Claim | Chapter | URL | Date checked | Supported | Notes |
|---|---:|---|---|---|---|
| gpt-live-transcribe: low-latency live transcription, $0.017 per minute, tunable delay, context/keyword/language hints | S2S doc | https://developers.openai.com/api/docs/models/gpt-live-transcribe | 2026-10-06 | yes | Model page read directly |
| Delay levels minimal–xhigh; prompt/keywords/languages; no server VAD (turn_detection null, manual commit); match by item_id; no timestamps, speaker labels or confidence scores | S2S doc | https://developers.openai.com/api/docs/guides/realtime-transcription | 2026-10-06 | yes | Guide read directly; example uses 24 kHz PCM |
| Announced July 29, 2026 with gpt-transcribe; semantic accuracy 38.5% → 44.6% with free-form context | S2S doc | https://community.openai.com/t/gpt-live-transcribe-and-gpt-transcribe-two-new-transcription-models-in-the-api/1388318 | 2026-10-06 | yes | Vendor-reported benchmark |
| G.711 μ-law/A-law input works with gpt-live-transcribe | S2S doc | https://www.datacamp.com/tutorial/gpt-live-transcribe-api | 2026-10-06 | unverified | Third-party tutorial only; not in OpenAI guide. Labeled as unconfirmed |
| Realtime sessions max 60 minutes; voice fixed after first audio; input_audio_buffer.append max 15 MB | S2S doc | https://developers.openai.com/api/docs/guides/realtime-conversations | 2026-10-06 | yes | Guide read directly |
| GPT-Live: wait for session.started (WebSocket); muted sessions keep running; close via session.close/session.closed with usage.seconds; transcript deltas have no item ID or turn-end event; >90% of 128k context starts a replacement voice engine | GPT-Live doc | https://developers.openai.com/api/docs/guides/live-conversations | 2026-10-06 | yes | Guide read directly |
| GPT-Live delegation: speech and backend work run independently; interrupting leaves backend work running; track operation IDs and task revisions | GPT-Live doc | https://developers.openai.com/api/docs/guides/live-delegation | 2026-10-06 | yes | Guide read directly |

## Pantheon 2026 day-one keynotes pass, October 7, 2026

| Claim | Chapter | URL | Date checked | Supported | Notes |
|---|---:|---|---|---|---|
| CTPO keynote: Atlas mobile app for the office, no-code Automation Hub, MCP server connecting Claude or ChatGPT to ServiceTitan data; Pro/Max customers grew revenue twice as fast as non-Max peers | Pantheon brief | https://www.servicetitan.com/blog/pantheon-2026-live-coverage | 2026-10-07 | yes | Company live blog; summary of the keynote, not a transcript |
| Max open after Pantheon to plumbing, heating, electrical and garage-door customers with four or more technicians | Pantheon brief | https://www.servicetitan.com/blog/pantheon-2026-live-coverage | 2026-10-07 | yes | Narrower than the press release's "all residential in-home contractors"; both stated |
| Homh app plugin live on ChatGPT, Google Gemini and Claude; Atlas now a chief-of-staff-level agent; Max pilot for commercial and roofing | Pantheon brief, Homh doc | https://www.servicetitan.com/blog/pantheon-2026-live-coverage | 2026-10-07 | yes | Corrected October 7, 2026: these are the live blog's narration, not quotes from the co-founder and president; now paraphrased and attributed to the blog |
| Commercial agents (Equipment, Findings, Daily Log, Invoice); one customer's invoice prep fell from 30 to under 5 minutes | Pantheon brief | https://www.servicetitan.com/blog/pantheon-2026-live-coverage | 2026-10-07 | yes | Company-reported customer result |
| Davis AC's AI Virtual Agent reported a 98% booking rate during peak season | Pantheon brief | https://www.servicetitan.com/blog/pantheon-2026-live-coverage | 2026-10-07 | yes | Customer claim; denominator not stated |
| Average revenue realization in the room about 60%, top performers high 80s | Pantheon brief | https://www.servicetitan.com/blog/pantheon-2026-live-coverage | 2026-10-07 | yes | Attributed to a ServiceTitan SVP |

## Agentic orchestration and shared skills pass, October 7, 2026

| Claim | Chapter | URL | Date checked | Supported | Notes |
|---|---:|---|---|---|---|
| Max: 30 agents across 18 business drivers; shared context, shared judgment, coordinated action, arbitration (highest expected value at lowest expected cost), centralized supervision; command center | 15 | https://www.investing.com/news/transcripts/servicetitan-at-pantheon-2026-ai-push-aims-to-make-trades-selfrunning-93CH-4934737 | 2026-10-07 | yes | Company claims; same sources as the Pantheon brief |
| Salesforce SOMA: a primary orchestrator ("Superagent") delegates to specialized agents in one org; MOMA extends across orgs in one Data Cloud trust boundary | 15 | https://help.salesforce.com/s/articleView?id=005317683&language=en_US&type=1 | 2026-10-07 | yes | Vendor documentation |
| Salesforce Agent Gateway: governance layer for MCP and A2A connections (auth, per-agent policy, rate limits and quotas, message schema validation, session tracing) | 15 | https://help.salesforce.com/s/articleView?id=005317683&language=en_US&type=1 | 2026-10-07 | yes | Vendor documentation |
| Agentforce: a primary agent routes tasks to specialized agents; A2A support for third-party agents | 15 | https://www.salesforce.com/agentforce/multi-agent-orchestration/ | 2026-10-07 | yes | Product page; does not mention SOMA/MOMA or MCP |
| Microsoft Agent Framework orchestration patterns: sequential, concurrent, handoff, group chat, Magentic | 15 | https://learn.microsoft.com/agent-framework/workflows/orchestrations | 2026-10-07 | yes | Vendor documentation |
| Agent Framework guidance: use a workflow when steps are well defined, explicit control over execution order is needed, or multiple agents/functions coordinate; prefer a function over an agent when possible | 15 | https://learn.microsoft.com/agent-framework/overview/ | 2026-10-07 | yes | Vendor documentation; the overview mentions MCP clients but not A2A |
| ServiceTitan data platform uses Kafka (with a custom ETL agent), Snowflake and Airflow | 15 | https://servicetitan.wd1.myworkdayjobs.com/en-US/ServiceTitan/job/Manager--Software-Engineering_JR114911 | 2026-10-07 | yes | Job listing; data platform only, not the agent runtime; listings expire |
| ServiceTitan communications data: event streaming and a reporting pipeline into Snowflake serving reporting, AI systems and AgentOS | 15 | https://builtin.com/job/staff-product-manager-communications-intelligence/10448969 | 2026-10-07 | yes | Job listing on Built In; listings expire |
| A Senior Software Engineer, Data Platform listing names Kafka, Snowflake, Airflow and AI agents for operational tasks | 15 | — (Workday listing JR114910, no longer available) | 2026-10-07 | unverified | Page returned no readable description, and the listing has since been removed; not cited in the chapter |
| Voice Agent "Skills and Capabilities" settings control which scheduling actions the agent can perform; unbooked calls get AI-assigned call reasons | 16 | https://help.servicetitan.com/docs/configure-your-voice-agent-settings | 2026-10-07 | yes | Help center; "teams review unbooked calls to find capability gaps" is our inference, not stated |
| A cross-agent skills registry or marketplace exists inside Max | 16 | — | 2026-10-07 | unverified | Hypothesis only; no public evidence |
| MCP: JSON-RPC 2.0 between hosts, clients and servers; servers offer resources, prompts and tools; clients may offer elicitation; 2026-07-28 revision has stateless self-contained requests and opt-in extensions (Tasks, Skills over MCP working group, MCP Apps); tool descriptions untrusted unless from a trusted server; hosts must get consent before invoking tools; the protocol cannot enforce these principles | 15 | https://modelcontextprotocol.io/specification/2026-07-28 | 2026-10-07 | yes | Protocol specification read directly |
| A2A 1.0.0: Agent Card at /.well-known/agent-card.json; Task states incl. working, input-required, auth-required, completed, failed, canceled, rejected; Message/Part/Artifact; JSON-RPC, gRPC and HTTP+JSON bindings; streaming and webhook push notifications; auth schemes declared in the Agent Card; opaque agents | 15 | https://a2a-protocol.org/latest/specification/ | 2026-10-07 | yes | Protocol specification read directly |

## Architecture explorer figures pass, October 7, 2026

| Claim | Chapter | URL | Date checked | Supported | Notes |
|---|---:|---|---|---|---|
| GPT-6 Luna: $0.10 / $0.50 per 1M input/output tokens ($0.01 cached input) | Architecture explorer | https://developers.openai.com/api/docs/models/gpt-6-luna | 2026-10-07 | yes | Model page lists speed as "Fast"; no latency figure |
| GPT-6 Astra: $10 / $50 per 1M input/output tokens ($1 cached input); reasoning model | Architecture explorer | https://developers.openai.com/api/docs/models/gpt-6-astra | 2026-10-07 | yes | Explorer costs assume no caching |
| gpt-realtime-2.1-mini audio: $10 / $20 per 1M input/output tokens | Architecture explorer | https://developers.openai.com/api/docs/models/gpt-realtime-2.1-mini | 2026-10-07 | yes | Full model's $32 / $64 already in the speech-to-speech doc |
| Realtime audio is 1 token per 100 ms of user audio and 1 per 50 ms of assistant audio; caching is "best-effort and not guaranteed" | Architecture explorer | https://developers.openai.com/api/docs/guides/realtime-costs | 2026-10-07 | yes | Basis for the derived per-minute audio costs |
| LiveKit default endpointing delay: 0.5 s minimum, 3.0 s maximum | Architecture explorer | https://docs.livekit.io/agents/logic/turns/tuning/ | 2026-10-07 | yes | Python and Node.js docs agree |
| GPT-4o Mini TTS: $12 per 1M audio output tokens; page shows a deprecated badge | Architecture explorer | https://developers.openai.com/api/docs/models/gpt-4o-mini-tts | 2026-10-07 | partly | Deprecation status is inconsistent across snapshots; per-minute TTS cost (~$0.015) is a community estimate, not OpenAI's |
| ITU-T G.114: under 150 ms one-way delay is essentially transparent; 400 ms is the planning limit | Architecture explorer | https://www.itu.int/rec/T-REC-G.114 | 2026-10-07 | yes | Standard (2003) |
| Speech-to-speech time to first audio (250–800 ms) | Architecture explorer | https://openai.com/index/hello-gpt-4o/ | 2026-10-07 | illustrative | Anchored to GPT-4o's 232 / 320 ms (2024) and Moshi's ~200 ms preprint; no published figure for gpt-realtime-2.1 |

## Agent architectures, harness and evaluation docs, October 7, 2026

| Claim | Chapter | URL | Date checked | Supported | Notes |
|---|---:|---|---|---|---|
| Microsoft defines an agent harness as "the runtime scaffolding that turns a language model into an agent that can perform work"; components: chat client, chat pipeline, agent and context providers, middleware and decorators, application UX; looping and background agents experimental | Comparative architectures, agent harness | https://learn.microsoft.com/en-us/agent-framework/concepts/harness | 2026-10-07 | yes | Vendor documentation; `create_harness_agent` released |
| Microsoft Agent Framework evaluators include tool_selection, tool_input_accuracy, task_completion, safety evaluators, and evaluate_workflow for workflows | Design by evaluation | https://learn.microsoft.com/agent-framework/agents/evaluation | 2026-10-07 | yes | Vendor documentation |
| OpenAI: a trace is the end-to-end record of model calls, tool calls, guardrails and handoffs for one run; move from traces to datasets and eval runs | Comparative architectures, design by evaluation | https://developers.openai.com/api/docs/guides/agent-evals | 2026-10-07 | yes | Vendor documentation |
| Anthropic: transcript vs. outcome; "it's often better to grade what the agent produced, not the path it took"; read transcripts to check graders; evals make behavior changes visible before users see them | Comparative architectures, design by evaluation | https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents | 2026-10-07 | yes | Published January 9, 2026 |
| Earlier draft claimed Anthropic's contribution is trajectory evaluation and permissions/sandboxing | Comparative architectures | https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents | 2026-10-07 | no | Corrected before merge: the article recommends outcome-first grading; sandboxing was unsourced |

## Whitepaper post-Pantheon refresh, October 7, 2026

| Claim | Chapter | URL | Date checked | Supported | Notes |
|---|---:|---|---|---|---|
| CEO placed "a voice agent that answers calls and books appointments" at level 2 of a five-level AI maturity model | 07, 14 | https://www.investing.com/news/transcripts/servicetitan-at-pantheon-2026-ai-push-aims-to-make-trades-selfrunning-93CH-4934737 | 2026-10-07 | yes | Transcript; company framing |
| In-product booking rates are "very easy to game"; a voice intelligence agent reviews every call to judge whether it was a bookable lead | 07, 11, 14 | https://www.investing.com/news/transcripts/servicetitan-at-pantheon-2026-ai-push-aims-to-make-trades-selfrunning-93CH-4934737 | 2026-10-07 | yes | CEO statement in transcript |
| Voice agent "books as well as a good CSR"; some customers let it handle 100% of calls with CSRs on standby for escalations | 07, 14 | https://www.investing.com/news/transcripts/servicetitan-at-pantheon-2026-ai-push-aims-to-make-trades-selfrunning-93CH-4934737 | 2026-10-07 | yes | Company-reported; no measurement method given |
| Coordination examples: voice agent books a high-value job, dispatch agent lacking context assigns a low-level tech; ads keep spending with a full schedule; "effectiveness tax" | 07, 12 | https://www.investing.com/news/transcripts/servicetitan-at-pantheon-2026-ai-push-aims-to-make-trades-selfrunning-93CH-4934737 | 2026-10-07 | yes | CEO's illustrative examples, not incident reports |
| Customers can adopt third-party agents or build their own; contractors will need to compete in "ChatGPT ads" | 09 | https://www.investing.com/news/transcripts/servicetitan-at-pantheon-2026-ai-push-aims-to-make-trades-selfrunning-93CH-4934737 | 2026-10-07 | yes | CEO statements in transcript |
| Profit example: 10,000 leads, 60% booked, $800 ticket; +10% on each lifts revenue 33% and doubles profit | 11 | https://www.investing.com/news/transcripts/servicetitan-at-pantheon-2026-ai-push-aims-to-make-trades-selfrunning-93CH-4934737 | 2026-10-07 | yes | Illustrative; profit doubling depends on an unpublished cost structure |
| Max is "the fully loaded version of ServiceTitan's Agentic Operating System"; company describes itself as "a purpose-built agentic operating system" | 07, 09 | https://www.globenewswire.com/news-release/2026/10/06/3375320/0/en/servicetitan-announcing-new-and-expanded-capabilities-at-pantheon-2026.html | 2026-10-07 | yes | Press release (body and About section) |
| Homh connects homeowners "and their AI agents" with contractors, works with ChatGPT, Gemini and Claude, with confirmed booking into ServiceTitan; AI CSRs get Adaptive Capacity | 07, 09, 12 | https://www.globenewswire.com/news-release/2026/10/06/3375320/0/en/servicetitan-announcing-new-and-expanded-capabilities-at-pantheon-2026.html | 2026-10-07 | yes | Press release; protocol and authentication not described. curl hit an HTTP/2 stream error; content read via fetch tool |
| "We're ServiceTitan, the agentic operating system of the trades." | 09 | https://www.servicetitan.com/blog/pantheon-2026-live-coverage | 2026-10-07 | yes | In quotation marks closing the live blog's coverage of the co-founder and president's keynote; attributed by placement, no speaker tag |
| Homh app plugin live on ChatGPT, Google Gemini and Claude; MCP server connecting Claude or ChatGPT to ServiceTitan data | 07, 12 | https://www.servicetitan.com/blog/pantheon-2026-live-coverage | 2026-10-07 | yes | Live-blog narration, not a speaker quote; paraphrased and attributed to the blog |
| Davis AC credits its virtual agent with a 98% booking rate | 07, 11 | https://www.servicetitan.com/blog/pantheon-2026-live-coverage | 2026-10-07 | yes | Blog's paraphrase of a customer; denominator not stated |
| Some customers using Pro and Max grew revenue twice as fast year over year as non-Max peers | 11 | https://www.servicetitan.com/blog/pantheon-2026-live-coverage | 2026-10-07 | yes | Reported speech of the CTPO in the live blog; selection effects not addressed |
| gpt-realtime-2 announced May 7, 2026 with minimal–xhigh reasoning effort, preambles and parallel tool calls | 08, A | https://openai.com/index/advancing-voice-intelligence-with-new-models-in-the-api/ | 2026-10-07 | yes | Vendor announcement; curl returned 403 (bot protection), content read via fetch tool |
| gpt-realtime-2 and gpt-realtime-2.1: 128k context, 32k output, $4/$24 text and $32/$64 audio per 1M tokens; 2.1 improves alphanumerics, silence/noise and interruptions | 08 | https://developers.openai.com/api/docs/models/gpt-realtime-2.1 | 2026-10-07 | yes | Model pages (HTTP 200); gpt-realtime-2 page also checked |
| gpt-realtime-2.1-mini: distilled reasoning model; $0.60/$2.40 text, $10/$20 audio per 1M tokens | 08 | https://developers.openai.com/api/docs/models/gpt-realtime-2.1-mini | 2026-10-07 | yes | Model page |
| gpt-realtime-2.1 and 2.1-mini released July 6, 2026; p95 latency cut at least 25% across Realtime voice models | 08, A | https://community.openai.com/t/new-realtime-models-on-the-api-gpt-realtime-2-1-and-gpt-realtime-2-1-mini/1385896 | 2026-10-07 | yes | Vendor-reported |
| gpt-live-transcribe announced July 29, 2026; low-latency realtime speech-to-text at $0.017 per minute | 08, A | https://community.openai.com/t/gpt-live-transcribe-and-gpt-transcribe-two-new-transcription-models-in-the-api/1388318 | 2026-10-07 | yes | Price from the model page |
| GPT-Live-1 in the API September 10, 2026; full duplex; delegates reasoning and tool calls to a backend or third-party model; +30 points on Full Duplex Bench vs GPT-Realtime-2.1 | 08, A | https://openai.com/index/introducing-gpt-live-1-in-the-api/ | 2026-10-07 | yes | Vendor-reported; curl 403, read via fetch tool |
| GPT-Live-1 turn-taking latency (~0.80 s vs ~1.41 s) and Tau3 pass@1 (86.2% vs 45.7%) | 08 | https://openai.com/index/introducing-gpt-live-1-in-the-api/ | 2026-10-07 | unverified | In the GPT-Live doc since Sept 30, but the page text fetched today did not show the figures (likely chart-only); left out of chapter 08 |
| GPT-Live: application checks permissions, obtains confirmations, runs functions that access your systems; $0.05 per minute billed per second, backend billed separately | 08 | https://developers.openai.com/api/docs/guides/live | 2026-10-07 | yes | Guide and model page read |
| Chapter 15 sections 10–13 (observability, failure mining incl. the Kafka/Snowflake job-listing subsection, evaluation, canary/A-B) moved unchanged to chapter 17; earlier rows that say "15" for those topics now refer to chapter 17 | 15, 17 | — (repo edit: PR #20, https://github.com/sp7412/onboarding/pull/20) | 2026-10-07 | n/a | Editorial change to this repo, not an external claim; recorded so earlier rows citing chapter 15 can be read correctly |

## Pantheon follow-ups, October 8, 2026

| Claim | Chapter | URL | Date checked | Supported | Notes |
|---|---:|---|---|---|---|
| Oct 7 partner-ecosystem keynote: partner certification program for security and data handling; Avoca books against real capacity via an API open to certified partners; webhooks by year-end; programmatic onboarding | Pantheon brief, MCP note | https://www.servicetitan.com/blog/pantheon-2026-live-coverage | 2026-10-08 | yes | Live-blog summary; one direct Chander quote ("a choice that you can trust") |
| A ServiceTitan MCP server, described as still in development, let Claude find stale materials and offer to deactivate them | Pantheon brief, MCP note | https://www.servicetitan.com/blog/pantheon-2026-live-coverage | 2026-10-08 | yes | Live-blog narration of a demo, plus the quote "You didn't need to know what the APIs were"; availability unconfirmed |
| Atlas places capacity holds for campaigns and shows reasoning; Command Center in private preview for Max customers | Pantheon brief | https://www.servicetitan.com/blog/pantheon-2026-live-coverage | 2026-10-08 | yes | Tuesday session recap; Armour quote is direct |
| Atlas access is administered by persona | Pantheon brief, MCP note | https://help.servicetitan.com/docs/assign-atlas-access-and-personas | 2026-10-08 | yes | Help center |
| Atlas creates and updates Adaptive Capacity strategic rules from plain language | Pantheon brief, MCP note | https://help.servicetitan.com/commercial/docs/use-atlas-in-adaptive-capacity-strategic-rules-1 | 2026-10-08 | yes | Help center |
| Pantheon breakout sessions go to Academy about 4–6 weeks after the event | Pantheon brief | https://help.servicetitan.com/docs/how-can-i-access-pantheon-slides-and-video-recordings | 2026-10-08 | yes | Help center (updated April 9, 2026); Academy is a customer platform |
| A transcript or recap of "Charging Ahead with AI and Max" (Oct 7) is public | Pantheon brief | — | 2026-10-08 | no | Not found on the live blog or in news search as of this date |

