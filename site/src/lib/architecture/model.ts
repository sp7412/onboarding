/**
 * Data for the drill-down architecture explorer (/architecture).
 *
 * Three ways to build the same booking call, made of blocks you can open to see what they do,
 * where their job stops, and what they typically add in latency and cost. Every figure carries
 * a basis and sources; tests in model.test.ts fail the build if one doesn't.
 *
 * Latency ranges are rough typical (p50-ish) contributions to the gap the caller hears, in ms.
 * Cost ranges are US dollars per minute of call. Neither is a benchmark of any product.
 */

export type Basis =
  | "vendor"        // a number the vendor published (pricing, their own benchmark)
  | "standard"      // a standards body or peer-reviewed paper
  | "docs"          // a documented default setting
  | "derived"       // computed from published prices with stated assumptions
  | "estimate"      // third-party or community estimate
  | "teaching"      // a value used by this repo's labs
  | "illustrative"; // a plausible range for teaching, not measured

export interface Figure {
  lo: number;
  hi: number;
  basis: Basis;
  note: string;
  sources?: string[];
}

export interface Link { label: string; href: string }

export interface ArchNode {
  id: string;
  title: string;
  summary: string;           // what it does
  stops?: string;            // where its responsibility ends
  owner: Owner;
  latency?: Figure;          // ms added to the path(s) that include this node
  cost?: Figure;             // $ per call minute
  failures?: string[];
  knobs?: string[];
  learn?: Link[];
  children?: string[];
}

export type Owner = "telephony" | "transport" | "model" | "control" | "backend" | "observe";

export const OWNER_LABEL: Record<Owner, string> = {
  telephony: "Telephony",
  transport: "Transport",
  model: "Model",
  control: "Control plane",
  backend: "Backend",
  observe: "Observe & coordinate",
};

export interface Source { label: string; url: string; kind: Basis }

export const SOURCES: Record<string, Source> = {
  g114: { label: "ITU-T G.114, One-way transmission time (2003)", url: "https://www.itu.int/rec/T-REC-G.114", kind: "standard" },
  livekitTuning: { label: "LiveKit docs: turn-taking tuning (endpointing defaults)", url: "https://docs.livekit.io/agents/logic/turns/tuning/", kind: "docs" },
  gpt4o: { label: "OpenAI, Hello GPT-4o (May 2024)", url: "https://openai.com/index/hello-gpt-4o/", kind: "vendor" },
  moshi: { label: "Défossez et al., Moshi (arXiv preprint, 2024)", url: "https://arxiv.org/abs/2410.00037", kind: "vendor" },
  liveLaunch: { label: "OpenAI, GPT-Live-1 in the API (Sept 2026)", url: "https://openai.com/index/introducing-gpt-live-1-in-the-api/", kind: "vendor" },
  liveModel: { label: "OpenAI, GPT-Live 1 model page", url: "https://developers.openai.com/api/docs/models/gpt-live-1", kind: "vendor" },
  rt21: { label: "OpenAI, GPT-Realtime-2.1 model page", url: "https://developers.openai.com/api/docs/models/gpt-realtime-2.1", kind: "vendor" },
  rt21mini: { label: "OpenAI, GPT-Realtime-2.1 Mini model page", url: "https://developers.openai.com/api/docs/models/gpt-realtime-2.1-mini", kind: "vendor" },
  realtimeCosts: { label: "OpenAI, Realtime API: managing costs", url: "https://developers.openai.com/api/docs/guides/realtime-costs", kind: "vendor" },
  liveTranscribe: { label: "OpenAI, GPT-Live-Transcribe model page", url: "https://developers.openai.com/api/docs/models/gpt-live-transcribe", kind: "vendor" },
  luna: { label: "OpenAI, GPT-6 Luna model page", url: "https://developers.openai.com/api/docs/models/gpt-6-luna", kind: "vendor" },
  astra: { label: "OpenAI, GPT-6 Astra model page", url: "https://developers.openai.com/api/docs/models/gpt-6-astra", kind: "vendor" },
  miniTts: { label: "OpenAI, GPT-4o Mini TTS model page (shows a deprecated badge)", url: "https://developers.openai.com/api/docs/models/gpt-4o-mini-tts", kind: "vendor" },
  ttsCommunity: { label: "OpenAI Developer Community: TTS pricing estimates (users, Mar 2025)", url: "https://community.openai.com/t/new-tts-api-pricing-and-gotchas/1150616", kind: "estimate" },
  labBackend: { label: "This repo: lab 08 and the teaching backend's tool latencies", url: "/labs#lab-08", kind: "teaching" },
};

/** Stated assumptions behind every "derived" cost. Shown on the page. */
export const COST_ASSUMPTIONS = [
  "A minute of call is about 30 s of caller speech and 30 s of agent speech.",
  "Cascaded: about 6 model turns per minute, each re-reading 1.5k–4k tokens of prompt, tools and history and writing 50–150 tokens.",
  "Full duplex: about 2 backend delegations per minute of the same size.",
  "Realtime audio is 1 token per 100 ms of caller audio and 1 per 50 ms of agent audio (OpenAI's costs guide).",
  "No prompt caching. Caching can cut repeated input cost substantially; the costs guide calls it best-effort.",
  "Carrier, SIP and media-server charges are not included; they depend on your providers.",
];

const L = (label: string, href: string): Link => ({ label, href });

export const NODES: Record<string, ArchNode> = {
  // ---------------------------------------------------------------- shared: telephony
  phone: {
    id: "phone", title: "Caller and phone network", owner: "telephony",
    summary: "The caller's phone, the carrier network and the SIP trunk that hands the call to your media server.",
    stops: "Carries audio. Knows nothing about the conversation or the business.",
    failures: ["Packet loss and jitter garble words, especially numbers.", "Narrowband phone audio hurts recognition of names and addresses."],
    learn: [L("Whitepaper ch. 08: technology landscape", "/whitepaper/08-technology-landscape"), L("Call anatomy", "/docs/call-anatomy")],
    children: ["netIn", "codec", "consent"],
  },
  netIn: {
    id: "netIn", title: "Network delay, caller to you", owner: "telephony",
    summary: "One-way transit time for the caller's audio to reach your servers.",
    latency: { lo: 20, hi: 150, basis: "standard", note: "ITU-T G.114 says under 150 ms one way is essentially transparent for conversation and 400 ms is the planning limit. The lower bound is illustrative.", sources: ["g114"] },
    knobs: ["Region of your media servers", "Carrier and SIP provider"],
  },
  codec: {
    id: "codec", title: "Phone audio and codecs", owner: "telephony",
    summary: "Phone calls usually arrive as narrowband audio, which loses detail that speech recognition relies on.",
    failures: ["Similar-sounding letters and digits (B/D, 15/50) get confused."],
    knobs: ["Keyword hints for names and street names", "Always read back numbers and addresses"],
    learn: [L("Lesson: when is the caller done?", "/lessons/endpointing")],
  },
  consent: {
    id: "consent", title: "Recording and AI disclosure", owner: "telephony",
    summary: "Telling callers they may be recorded and that they're talking to an AI, where the law requires it.",
    stops: "A policy decision implemented in the greeting and the control plane, not a model setting.",
    learn: [L("Whitepaper ch. 10: regulation", "/whitepaper/10-regulation-and-compliance")],
  },

  // ---------------------------------------------------------------- shared: transport
  transport: {
    id: "transport", title: "Transport (LiveKit or similar)", owner: "transport",
    summary: "Moves audio in real time, decides when the caller has finished a turn, and plays the agent's audio back.",
    stops: "Decides when a turn ends, not what to say or whether an action is allowed.",
    learn: [L("LiveKit hands-on", "/docs/livekit-hands-on"), L("Lab 04: LiveKit agents", "/labs#lab-04")],
    children: ["vad", "endpointing", "bargeIn", "playout"],
  },
  vad: {
    id: "vad", title: "Voice activity detection", owner: "transport",
    summary: "Estimates frame by frame whether someone is speaking.",
    failures: ["Background TV or a second speaker counts as the caller.", "A soft-spoken caller is missed."],
    learn: [L("Lab 03: turn-taking", "/labs#lab-03"), L("Turn-taking simulation", "/simulations#turn-taking")],
  },
  endpointing: {
    id: "endpointing", title: "Endpointing (end of turn)", owner: "transport",
    summary: "Waits for enough silence, or a semantic end-of-turn signal, before treating the caller's turn as finished.",
    stops: "Only decides when to respond. A pause inside a phone number is the classic failure.",
    latency: { lo: 500, hi: 800, basis: "docs", note: "LiveKit's default minimum endpointing delay is 0.5 s (maximum 3 s). Realtime APIs expose a similar silence setting. The upper bound is illustrative.", sources: ["livekitTuning"] },
    failures: ["Too short: cuts callers off mid-number.", "Too long: dead air after every answer."],
    knobs: ["Minimum and maximum delay", "Semantic end-of-turn model"],
    learn: [L("Lesson: when is the caller done?", "/lessons/endpointing"), L("Turn-taking simulation", "/simulations#turn-taking")],
  },
  bargeIn: {
    id: "bargeIn", title: "Barge-in and truncation", owner: "transport",
    summary: "When the caller interrupts, stop playback and cut the agent's memory back to what the caller actually heard.",
    failures: ["The model 'remembers' saying things the caller never heard."],
    learn: [L("Lesson: what did the caller hear?", "/lessons/heard-vs-generated"), L("Lab 01, section 4", "/labs#lab-01")],
  },
  playout: {
    id: "playout", title: "Network out and playout buffer", owner: "transport",
    summary: "Getting the agent's first audio frames back to the caller, through jitter buffers.",
    latency: { lo: 40, hi: 200, basis: "illustrative", note: "Return network transit (see G.114) plus playout buffering.", sources: ["g114"] },
  },

  // ---------------------------------------------------------------- cascaded
  stt: {
    id: "stt", title: "Speech-to-text", owner: "model",
    summary: "Streams the caller's audio into text: partial words as they speak, then a final transcript.",
    stops: "Produces words. Understanding them is the language model's job.",
    cost: { lo: 0.0085, hi: 0.017, basis: "derived", note: "GPT-Live-Transcribe is $0.017 per minute of audio; transcribing only the caller's half of a minute is about $0.0085.", sources: ["liveTranscribe"] },
    children: ["sttStream", "sttFinal", "keywords"],
    learn: [L("Speech-to-speech vs. cascaded", "/docs/speech-to-speech-models")],
  },
  sttStream: {
    id: "sttStream", title: "Streaming recognition", owner: "model",
    summary: "Emits partial transcripts while the caller is still speaking, so later stages can start early.",
    knobs: ["Start language-model work on stable partials (speculative)"],
  },
  sttFinal: {
    id: "sttFinal", title: "Final transcript", owner: "model",
    summary: "The settled transcript, available shortly after the turn ends.",
    latency: { lo: 50, hi: 300, basis: "illustrative", note: "Time from the end of the turn to a usable final transcript in a streaming recognizer." },
  },
  keywords: {
    id: "keywords", title: "Keyword hints", owner: "model",
    summary: "Bias recognition toward expected words: street names, product names, the company name.",
    failures: ["Hints that are too broad cause false matches."],
  },
  llm: {
    id: "llm", title: "Language model (text)", owner: "model",
    summary: "Reads the transcript, decides what to say, and proposes tool calls.",
    stops: "Proposes. Never executes tools, owns no durable state, can't unsay audio.",
    cost: { lo: 0.001, hi: 0.003, basis: "derived", note: "GPT-6 Luna at $0.10 / $0.50 per 1M input/output tokens, with the turn and context assumptions below.", sources: ["luna"] },
    children: ["context", "toolCalling", "llmTtft"],
    learn: [L("Build your own voice agent", "/docs/build-your-own-voice-agent"), L("Lab 05: create_agent", "/labs#lab-05")],
  },
  context: {
    id: "context", title: "Prompt and context", owner: "model",
    summary: "Instructions, tool definitions and the conversation so far, re-read on every turn.",
    failures: ["Context grows every turn, raising cost and latency on long calls."],
    knobs: ["Summarize old turns", "Prompt caching", "Load tools for the current phase only"],
  },
  toolCalling: {
    id: "toolCalling", title: "Tool proposals", owner: "model",
    summary: "The model asks for a tool by name with arguments. The application decides whether it runs.",
    learn: [L("Tools and guardrails", "/docs/tools-and-guardrails"), L("Lab 02", "/labs#lab-02")],
  },
  llmTtft: {
    id: "llmTtft", title: "Time to first token", owner: "model",
    summary: "How long until the model starts producing a reply.",
    latency: { lo: 150, hi: 500, basis: "illustrative", note: "A small, fast text model. Reasoning models take much longer before the first token." },
  },
  tts: {
    id: "tts", title: "Text-to-speech", owner: "model",
    summary: "Turns the reply into audio, streaming the first chunk as soon as possible.",
    stops: "Says what it's given. Can't check whether it's true.",
    cost: { lo: 0.0075, hi: 0.015, basis: "estimate", note: "About $0.015 per minute of generated audio for GPT-4o Mini TTS ($12 per 1M audio tokens), per community and third-party estimates; the agent speaks about half the call. OpenAI's model page shows a deprecated badge on it and some snapshots.", sources: ["miniTts", "ttsCommunity"] },
    children: ["ttsFirst", "voice", "pronounce"],
  },
  ttsFirst: {
    id: "ttsFirst", title: "Time to first audio", owner: "model",
    summary: "From text in to the first playable audio chunk.",
    latency: { lo: 100, hi: 400, basis: "illustrative", note: "Streaming synthesis; non-streaming is much slower." },
  },
  voice: { id: "voice", title: "Voice and style", owner: "model", summary: "Which voice, speaking rate and tone. Easy to swap in a cascaded design." },
  pronounce: {
    id: "pronounce", title: "Numbers and addresses", owner: "model",
    summary: "Reading back phone numbers, ZIP codes and times in a form the caller can check.",
    failures: ["'1500' read as 'one thousand five hundred' instead of 'fifteen hundred' or 'one five zero zero'."],
  },

  // ---------------------------------------------------------------- speech-to-speech
  s2s: {
    id: "s2s", title: "Speech-to-speech model", owner: "model",
    summary: "One model hears audio and speaks audio, with tool calling, inside a realtime session (for example gpt-realtime-2.1).",
    stops: "Proposes tool calls and speaks. Still turn-based: endpointing decides when it answers.",
    cost: { lo: 0.048, hi: 0.2, basis: "derived", note: "Floor: 300 caller audio tokens × $32/1M + 600 agent audio tokens × $64/1M per minute (gpt-realtime-2.1). Each response re-reads the session so far, so later minutes cost more; the upper bound is illustrative.", sources: ["rt21", "realtimeCosts"] },
    children: ["audioTokens", "s2sFirst", "sessionCost", "s2sTools"],
    learn: [L("Speech-to-speech models", "/docs/speech-to-speech-models"), L("Lab 01: realtime protocol", "/labs#lab-01")],
  },
  audioTokens: {
    id: "audioTokens", title: "Audio as tokens", owner: "model",
    summary: "Audio is compressed into tokens so a language model can read and write speech directly, keeping tone and timing that text drops.",
    learn: [L("How speech-to-speech works", "/docs/speech-to-speech-models")],
  },
  s2sFirst: {
    id: "s2sFirst", title: "Time to first audio", owner: "model",
    summary: "From the committed turn to the first audio the model produces.",
    latency: { lo: 250, hi: 800, basis: "illustrative", note: "No vendor publishes this for gpt-realtime-2.1. For scale: OpenAI reported GPT-4o answering audio in as little as 232 ms (320 ms average) in 2024, and the Moshi preprint reports about 200 ms. Reasoning effort and long context push it higher.", sources: ["gpt4o", "moshi"] },
  },
  sessionCost: {
    id: "sessionCost", title: "Session context and cost", owner: "model",
    summary: "Each response re-reads the whole session, so cost per minute rises as the call goes on.",
    knobs: ["Keep history unchanged to get cache hits", "Truncate or summarize old items"],
    learn: [L("OpenAI realtime costs guide", "https://developers.openai.com/api/docs/guides/realtime-costs")],
  },
  s2sTools: {
    id: "s2sTools", title: "Tool calls mid-conversation", owner: "model",
    summary: "The model emits a function call, waits for the result, then speaks again. Harder to inspect before audio plays.",
    failures: ["Speaks a confirmation before the tool result arrives."],
    learn: [L("Lesson: words versus the record", "/lessons/claims-vs-state")],
  },

  // ---------------------------------------------------------------- full duplex
  live: {
    id: "live", title: "Full-duplex voice model", owner: "model",
    summary: "Listens while it speaks and detects turns natively (for example GPT-Live-1). Delegates reasoning and tools to a backend model.",
    stops: "Handles the conversation. Doesn't reason deeply or run tools itself; it speaks what the backend sends.",
    cost: { lo: 0.05, hi: 0.05, basis: "vendor", note: "$0.05 per minute of voice session, billed per second. Backend usage is billed separately.", sources: ["liveModel", "liveLaunch"] },
    children: ["liveTurn", "backchannel", "channels"],
    learn: [L("GPT-Live-1", "/docs/gpt-live-1"), L("Build your own voice agent", "/docs/build-your-own-voice-agent")],
  },
  liveTurn: {
    id: "liveTurn", title: "Turn-taking reply", owner: "model",
    summary: "From the caller finishing to the agent starting to reply, including the model's own turn detection.",
    latency: { lo: 600, hi: 1000, basis: "vendor", note: "OpenAI reports 0.80 s average turn-taking latency on Full Duplex Bench v1 (vs 1.41 s for gpt-realtime-2.1). Measured at the model, without the phone network.", sources: ["liveLaunch"] },
  },
  backchannel: {
    id: "backchannel", title: "Listening while speaking", owner: "model",
    summary: "Hears 'uh-huh', side conversations and interruptions while talking, without stopping for every sound.",
  },
  channels: {
    id: "channels", title: "Thinking vs. commentary", owner: "control",
    summary: "The backend sends 'thinking' (context the model may paraphrase) and 'commentary' (what it should say). Only verified results belong in commentary.",
    learn: [L("Lesson: thinking is not speaking", "/lessons/duplex-channels")],
  },
  backend: {
    id: "backend", title: "Backend reasoning model", owner: "model",
    summary: "The model the voice layer delegates to: it reasons, calls tools through the control plane and sends back what to say.",
    stops: "Runs off the hot path: the caller hears the voice model meanwhile.",
    cost: { lo: 0.00035, hi: 0.00095, basis: "derived", note: "GPT-6 Luna at $0.10 / $0.50 per 1M input/output tokens for about 2 delegations a minute.", sources: ["luna"] },
    children: ["delegate", "backendThink", "commentary"],
  },
  delegate: {
    id: "delegate", title: "Delegation hand-off", owner: "control",
    summary: "Your application receives the delegation and starts the backend model.",
    latency: { lo: 20, hi: 80, basis: "illustrative", note: "An in-region network hop and request setup." },
  },
  backendThink: {
    id: "backendThink", title: "Backend thinking time", owner: "model",
    summary: "How long the backend model takes to decide what to do and say.",
    latency: { lo: 150, hi: 500, basis: "illustrative", note: "A fast model. A reasoning model can take seconds." },
  },
  commentary: {
    id: "commentary", title: "Commentary back to speech", owner: "model",
    summary: "The voice model receives the backend's answer and starts saying it at a natural point.",
    latency: { lo: 200, hi: 600, basis: "illustrative", note: "Depends on where the voice model is in its current sentence." },
  },

  // ---------------------------------------------------------------- shared: control plane and backend
  control: {
    id: "control", title: "Control plane (your application)", owner: "control",
    summary: "Owns identity, policy at the tool boundary, grounding, idempotency, escalation and what may be claimed.",
    stops: "This is where the business rules live. Models propose; this decides.",
    children: ["policy", "grounding", "idem", "emergency", "claimGuard"],
    learn: [L("Tools and guardrails", "/docs/tools-and-guardrails"), L("Guardrails simulation", "/simulations#guardrails")],
  },
  policy: {
    id: "policy", title: "Identity and policy checks", owner: "control",
    summary: "Is this the account holder? Is this slot one we offered? Is the change allowed today?",
    latency: { lo: 5, hi: 30, basis: "illustrative", note: "In-process checks against state the application already holds." },
    learn: [L("Lab 02", "/labs#lab-02")],
  },
  grounding: {
    id: "grounding", title: "Grounded confirmation", owner: "control",
    summary: "A 'yes' only counts if the caller's own words, in the transcript, contain it.",
    learn: [L("Lab 02", "/labs#lab-02")],
  },
  idem: {
    id: "idem", title: "Idempotent writes", owner: "control",
    summary: "The application owns the idempotency key, so a retried booking returns the same job instead of a second one.",
    learn: [L("Lab 06: durable workflow", "/labs#lab-06")],
  },
  emergency: {
    id: "emergency", title: "Emergency screen", owner: "control",
    summary: "Words like 'gas' or 'smoke' lock every tool except transfer, regardless of what the model thinks.",
    learn: [L("Lesson: the rare emergency alarm", "/lessons/rare-alarms"), L("Lab 13: Mini-Max", "/labs#lab-13")],
  },
  claimGuard: {
    id: "claimGuard", title: "Claim guard", owner: "control",
    summary: "Checks what's about to be said against committed state: no 'you're booked' without a booking.",
    learn: [L("Lesson: words versus the record", "/lessons/claims-vs-state"), L("Lab 07", "/labs#lab-07")],
  },
  tools: {
    id: "tools", title: "Tools and systems of record", owner: "backend",
    summary: "The schedule, customer records and jobs, reached only through the control plane.",
    stops: "The source of truth. Nothing is booked until it says so.",
    children: ["toolCall", "records"],
    learn: [L("How a contractor works", "/docs/how-a-contractor-works")],
  },
  toolCall: {
    id: "toolCall", title: "Tool round trip", owner: "backend",
    summary: "Finding open slots or creating the job: the backend call the answer depends on.",
    latency: { lo: 300, hi: 600, basis: "teaching", note: "The labs' teaching backend uses 450 ms for find_slots; lab 08 sweeps 300 ms to 3 s.", sources: ["labBackend"] },
    knobs: ["Prefetch likely slots while the caller is still talking", "Timeouts and a spoken fallback"],
    learn: [L("Lab 08: talker and thinker", "/labs#lab-08"), L("Latency simulation", "/simulations#latency")],
  },
  records: {
    id: "records", title: "Schedule, customers, jobs", owner: "backend",
    summary: "The systems that actually hold bookings, accounts and capacity.",
  },

  // ---------------------------------------------------------------- shared: orchestration
  orchestrate: {
    id: "orchestrate", title: "Orchestration (LangGraph or similar)", owner: "control",
    summary: "Runs multi-step workflows with durable state: the booking flow's steps, retries, timeouts and hand-offs to a person.",
    stops: "Sequences work and remembers where it is. Isn't the audio hot path or the system of record, and doesn't replace policy checks at the tool boundary.",
    children: ["workflowState", "retries", "humanLoop"],
    learn: [L("Lab 05: create_agent", "/labs#lab-05"), L("Lab 06: durable workflow", "/labs#lab-06"), L("Whitepaper ch. 15: agentic orchestration", "/whitepaper/15-agentic-orchestration")],
  },
  workflowState: {
    id: "workflowState", title: "Durable workflow state", owner: "control",
    summary: "Checkpoints each step so a dropped call or a crashed worker resumes instead of starting over.",
    failures: ["State held only in the model's context is lost when the session ends."],
    learn: [L("Lab 06: durable workflow", "/labs#lab-06")],
  },
  retries: {
    id: "retries", title: "Retries and timeouts", owner: "control",
    summary: "Retries a failed tool call with the same idempotency key, and gives up on a timeout with a spoken fallback.",
    failures: ["Retrying without an idempotency key books the job twice."],
  },
  humanLoop: {
    id: "humanLoop", title: "Human in the loop", owner: "control",
    summary: "Pauses the workflow for a person to approve or take over, then resumes from the saved state.",
    learn: [L("Lab 06: durable workflow", "/labs#lab-06")],
  },

  // ---------------------------------------------------------------- shared: off the hot path
  observe: {
    id: "observe", title: "Tracing and evaluation", owner: "observe",
    summary: "Records every turn, tool call and claim; scores calls offline and online.",
    stops: "Observes and scores. Enforces nothing at runtime.",
    children: ["traces", "evals"],
    learn: [L("Evaluating voice agents", "/docs/evaluating-voice-agents"), L("Lab 07", "/labs#lab-07")],
  },
  traces: { id: "traces", title: "Traces", owner: "observe", summary: "One trace per call linking audio turns, model events, tool calls and spoken claims, with personal data redacted.", learn: [L("Lab 07", "/labs#lab-07")] },
  evals: { id: "evals", title: "Evaluations", owner: "observe", summary: "Datasets and evaluators, run repeatedly, because a 95% agent fails a five-run check about one time in four.", learn: [L("Lesson: the eight-step booking call", "/lessons/pass-k")] },
  coordinate: {
    id: "coordinate", title: "Shared context and other agents", owner: "observe",
    summary: "The call's facts feed lead scoring, dispatch and a post-call bookability judge. Public Pantheon 2026 material describes this kind of coordination.",
    stops: "Other agents act on verified facts, not on the transcript.",
    children: ["facts", "judge"],
    learn: [L("Call facts contract", "/docs/call-facts-contract"), L("Pantheon 2026 brief", "/docs/pantheon-2026-ai-roadmap")],
  },
  facts: { id: "facts", title: "Call facts and the context ledger", owner: "observe", summary: "Structured facts with confidence and evidence; proposed by the voice agent, verified by the control plane.", learn: [L("Lab 09: shared context", "/labs#lab-09"), L("Lab 13: Mini-Max", "/labs#lab-13")] },
  judge: { id: "judge", title: "Bookability judge", owner: "observe", summary: "Decides after the call whether it was a real opportunity to book, which sets the denominator for every booking rate.", learn: [L("Exercise: bookability judge", "/docs/bookability-judge"), L("Lesson: the denominator", "/lessons/denominator")] },
};

// ------------------------------------------------------------------------ architectures

/** A path is a sequence of steps. A step is a node id, or parallel branches (the slowest wins). */
export type Step = string | { parallel: string[][] };

export interface Architecture {
  id: "cascaded" | "s2s" | "duplex";
  title: string;
  tagline: string;
  hotPath: string[];        // top-level blocks shown in the main lane, in call order
  background: string[];     // blocks alongside or after the call
  firstSound: Step[];       // caller stops → caller hears something
  answer: Step[];           // caller stops → caller hears the answer that needed a tool
  costNodes: string[];
  knobs: string[];
  benchmark?: { label: string; ms: number; sources: string[] };
  good: string[];
  watch: string[];
}

export const ARCHITECTURES: Architecture[] = [
  {
    id: "cascaded", title: "Cascaded", tagline: "Speech-to-text → language model → text-to-speech",
    hotPath: ["phone", "transport", "stt", "llm", "control", "tools", "tts"],
    background: ["orchestrate", "observe", "coordinate"],
    firstSound: ["netIn", "endpointing", "sttFinal", "llmTtft", "ttsFirst", "playout"],
    answer: ["netIn", "endpointing", "sttFinal", "llmTtft",
      { parallel: [["ttsFirst"], ["policy", "toolCall"]] }, "llmTtft", "ttsFirst", "playout"],
    costNodes: ["stt", "llm", "tts"],
    knobs: ["endpoint", "textModel", "toolSpeed"],
    good: ["Every stage is inspectable text: easy to log, test and guard before speech.", "Swap any vendor independently.", "Cheapest with a small text model."],
    watch: ["Each hand-off adds delay.", "Tone and hesitation are lost in transcription.", "Interruptions need careful plumbing."],
  },
  {
    id: "s2s", title: "Speech-to-speech", tagline: "One realtime model hears and speaks",
    hotPath: ["phone", "transport", "s2s", "control", "tools"],
    background: ["orchestrate", "observe", "coordinate"],
    firstSound: ["netIn", "endpointing", "s2sFirst", "playout"],
    answer: ["netIn", "endpointing", "s2sFirst", "policy", "toolCall", "s2sFirst", "playout"],
    costNodes: ["s2s"],
    knobs: ["endpoint", "s2sModel", "toolSpeed"],
    benchmark: { label: "OpenAI-reported turn-taking latency, gpt-realtime-2.1 (Full Duplex Bench v1)", ms: 1410, sources: ["liveLaunch"] },
    good: ["Fewer hand-offs, more natural prosody.", "Hears tone, not just words."],
    watch: ["Audio tokens make it the most expensive per minute.", "Less to inspect before audio plays.", "Still turn-based: endpointing still decides when it speaks."],
  },
  {
    id: "duplex", title: "Full duplex + delegation", tagline: "A live voice model talks while a backend model works",
    hotPath: ["phone", "transport", "live", "control", "tools"],
    background: ["backend", "orchestrate", "observe", "coordinate"],
    firstSound: ["netIn", "liveTurn", "playout"],
    answer: ["netIn", { parallel: [["liveTurn"], ["delegate", "backendThink", "policy", "toolCall"]] }, "commentary", "playout"],
    costNodes: ["live", "backend"],
    knobs: ["backendModel", "toolSpeed"],
    benchmark: { label: "OpenAI-reported turn-taking latency, gpt-live-1 (Full Duplex Bench v1)", ms: 798, sources: ["liveLaunch"] },
    good: ["The caller hears a natural reply while the tool runs.", "Choose backend depth per task.", "Native turn-taking and interruptions."],
    watch: ["Two models and a delegation protocol to operate.", "Only verified results may be spoken as commentary.", "Newest of the three: less tooling and history."],
  },
];

// ------------------------------------------------------------------------ knobs

export interface KnobOption {
  id: string;
  label: string;
  latency?: Record<string, Figure>;
  cost?: Record<string, Figure>;
}
export interface Knob { id: string; label: string; help: string; options: KnobOption[]; defaultId: string }

export const KNOBS: Record<string, Knob> = {
  endpoint: {
    id: "endpoint", label: "End-of-turn silence", defaultId: "default",
    help: "Shorter replies faster but cuts callers off mid-number.",
    options: [
      { id: "fast", label: "200 ms (fast, risky)", latency: { endpointing: { lo: 200, hi: 400, basis: "illustrative", note: "Aggressive silence threshold." } } },
      { id: "default", label: "500 ms (LiveKit default)" },
      { id: "cautious", label: "800 ms (cautious)", latency: { endpointing: { lo: 800, hi: 1100, basis: "illustrative", note: "Waits longer before answering." } } },
    ],
  },
  textModel: {
    id: "textModel", label: "Language model", defaultId: "luna",
    help: "A reasoning model is smarter and much slower and costlier per turn.",
    options: [
      { id: "luna", label: "Fast model (GPT-6 Luna)" },
      {
        id: "astra", label: "Reasoning model (GPT-6 Astra)",
        latency: { llmTtft: { lo: 600, hi: 2500, basis: "illustrative", note: "Reasoning before the first token." } },
        cost: { llm: { lo: 0.105, hi: 0.285, basis: "derived", note: "GPT-6 Astra at $10 / $50 per 1M input/output tokens, no caching ($1 per 1M cached input would cut this a lot).", sources: ["astra"] } },
      },
    ],
  },
  s2sModel: {
    id: "s2sModel", label: "Realtime model", defaultId: "full",
    help: "The mini model is cheaper and faster, with weaker reasoning.",
    options: [
      { id: "full", label: "gpt-realtime-2.1" },
      {
        id: "mini", label: "gpt-realtime-2.1-mini",
        latency: { s2sFirst: { lo: 200, hi: 600, basis: "illustrative", note: "Smaller model, typically faster first audio." } },
        cost: { s2s: { lo: 0.015, hi: 0.06, basis: "derived", note: "Floor: 300 × $10/1M + 600 × $20/1M audio tokens per minute; upper bound illustrative for re-read context.", sources: ["rt21mini", "realtimeCosts"] } },
      },
    ],
  },
  backendModel: {
    id: "backendModel", label: "Backend model", defaultId: "luna",
    help: "Only the answer waits for the backend. The caller hears the voice model either way.",
    options: [
      { id: "luna", label: "Fast model (GPT-6 Luna)" },
      {
        id: "astra", label: "Reasoning model (GPT-6 Astra)",
        latency: { backendThink: { lo: 800, hi: 3000, basis: "illustrative", note: "Reasoning before deciding." } },
        cost: { backend: { lo: 0.035, hi: 0.095, basis: "derived", note: "GPT-6 Astra at $10 / $50 per 1M input/output tokens for about 2 delegations a minute, no caching.", sources: ["astra"] } },
      },
    ],
  },
  toolSpeed: {
    id: "toolSpeed", label: "Backend tool speed", defaultId: "typical",
    help: "How long finding slots or booking takes in your systems.",
    options: [
      { id: "fast", label: "Fast (~150 ms)", latency: { toolCall: { lo: 100, hi: 200, basis: "teaching", note: "A cached or local lookup.", sources: ["labBackend"] } } },
      { id: "typical", label: "Typical (~450 ms)" },
      { id: "slow", label: "Slow (1–3 s)", latency: { toolCall: { lo: 1000, hi: 3000, basis: "teaching", note: "Lab 08's slow cases.", sources: ["labBackend"] } } },
    ],
  },
};

// ------------------------------------------------------------------------ calculations

export type Choices = Record<string, string>;

export function defaultChoices(): Choices {
  return Object.fromEntries(Object.values(KNOBS).map((k) => [k.id, k.defaultId]));
}

function patched(kind: "latency" | "cost", id: string, arch: Architecture, choices: Choices): Figure | undefined {
  for (const knobId of arch.knobs) {
    const knob = KNOBS[knobId];
    const opt = knob.options.find((o) => o.id === (choices[knobId] ?? knob.defaultId));
    const fig = opt?.[kind]?.[id];
    if (fig) return fig;
  }
  return NODES[id]?.[kind];
}

export function latencyOf(id: string, arch: Architecture, choices: Choices): Figure | undefined {
  return patched("latency", id, arch, choices);
}

export function costOf(id: string, arch: Architecture, choices: Choices): Figure | undefined {
  return patched("cost", id, arch, choices);
}

export interface Range { lo: number; hi: number }

export function pathRange(path: Step[], arch: Architecture, choices: Choices): Range {
  let lo = 0, hi = 0;
  for (const step of path) {
    if (typeof step === "string") {
      const f = latencyOf(step, arch, choices);
      if (f) { lo += f.lo; hi += f.hi; }
    } else {
      const branches = step.parallel.map((b) => pathRange(b, arch, choices));
      lo += Math.max(...branches.map((b) => b.lo));
      hi += Math.max(...branches.map((b) => b.hi));
    }
  }
  return { lo, hi };
}

export function costRange(arch: Architecture, choices: Choices): Range {
  return arch.costNodes.reduce((acc, id) => {
    const c = costOf(id, arch, choices);
    return c ? { lo: acc.lo + c.lo, hi: acc.hi + c.hi } : acc;
  }, { lo: 0, hi: 0 });
}

/** Every node id a path touches (including inside parallel branches). */
export function pathNodes(path: Step[]): string[] {
  return path.flatMap((s) => (typeof s === "string" ? [s] : s.parallel.flat()));
}

/** Descendants of a node, including itself. */
export function subtree(id: string): string[] {
  const n = NODES[id];
  return [id, ...(n?.children ?? []).flatMap(subtree)];
}

/** Latency a block contributes to a path: the sum of its subtree's nodes on that path (sequential view). */
export function blockLatency(blockId: string, path: Step[], arch: Architecture, choices: Choices): Range | null {
  const inBlock = new Set(subtree(blockId));
  const steps = pathNodes(path).filter((id) => inBlock.has(id));
  if (!steps.length) return null;
  return steps.reduce((acc, id) => {
    const f = latencyOf(id, arch, choices);
    return f ? { lo: acc.lo + f.lo, hi: acc.hi + f.hi } : acc;
  }, { lo: 0, hi: 0 });
}

/** Breadcrumb from a top-level block down to the node. */
export function trail(target: string, roots: string[]): string[] | null {
  for (const root of roots) {
    if (root === target) return [root];
    const below = trail(target, NODES[root]?.children ?? []);
    if (below) return [root, ...below];
  }
  return null;
}

export const fmtMs = (r: Range) => `${(r.lo / 1000).toFixed(2)}–${(r.hi / 1000).toFixed(2)} s`;
const money = (v: number) => (v === 0 ? "$0" : v < 0.01 ? `$${v.toFixed(4)}` : `$${v.toFixed(3)}`);
export const fmtCost = (r: Range) => (r.lo === r.hi ? money(r.lo) : `${money(r.lo)}–${money(r.hi)}`);
