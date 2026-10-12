# Full-Duplex Voice Model Evaluation: PersonaPlex vs GPT-Live

**Facts checked: October 11, 2026 · Status: desk research; no comparative load test run**

## Recommendation

Keep **OpenAI GPT-Live-1 as the production-shaped baseline** and evaluate NVIDIA
PersonaPlex-7B as a self-hosted challenger. Do not select a winner from the published
latency numbers alone, and do not assume one H100 supports 80 concurrent calls: the
public benchmark figures do not establish that capacity.

For the onboarding scheduling agent, compare complete task outcomes—not just the
voice model. The model must sit behind the same mock scheduling tools and authorization
control plane, and the tests must include barge-in, tool errors, confirmation, and safe
handoff.

## What the public evidence says

| Dimension | NVIDIA PersonaPlex-7B-v1 | OpenAI GPT-Live-1 |
|---|---|---|
| Interaction | Native full-duplex speech-to-speech; listens while speaking | Native full-duplex voice layer; listens and speaks concurrently |
| Published turn-taking latency | 170 ms on NVIDIA's FullDuplexBench results | OpenAI reports 0.798 s; its announcement describes a 30-point improvement over GPT-Realtime-2.1 on Full Duplex Bench |
| Published interruption latency | 240 ms on NVIDIA's FullDuplexBench results | No directly comparable interruption-latency number found in the cited launch material |
| Deployment | Self-hostable on supported NVIDIA GPUs; reference implementation uses PyTorch/Moshi | Managed API; backend reasoning and tools can be delegated |
| Cost model | GPU, hosting, operations, redundancy, and integration costs | $0.05 per active voice-session minute; backend model and tool use billed separately |
| Scope / caveat | Model card documents English speech input and English speech output. Model quality and tool execution need application-level evaluation. | Voice layer is not the whole agent: backend reasoning, tools, telephony, and observability still need to be budgeted. |

Sources:
- NVIDIA model card and reported benchmark: https://huggingface.co/nvidia/personaplex-7b-v1
- NVIDIA implementation: https://github.com/NVIDIA/personaplex
- OpenAI GPT-Live-1 announcement: https://openai.com/index/introducing-gpt-live-1-in-the-api/
- OpenAI model docs and pricing: https://developers.openai.com/api/docs/models/gpt-live-1 and https://developers.openai.com/api/docs/pricing

### How to read the latency claims

NVIDIA's 170 ms and 240 ms values are reported benchmark results, not an
end-to-end phone-call SLA. The model card defines turn-taking latency as user
end-of-speech to assistant speech onset, and interruption latency as the time
from a user interrupting the assistant to the assistant stopping. Those are
different measurements. Network, media transport, buffering, orchestration,
tool calls, and telephony can add latency.

I could not verify the quoted **1.1-second median acknowledgement** as a fair
like-for-like result for GPT-Live-1. OpenAI's current GPT-Live-1 launch material
reports 0.798-second turn-taking latency, while older GPT-Realtime-2.1 results
are a different model/version. Treat any comparison with 1.1 seconds as
unverified until the benchmark version, task mix, network, hardware, and metric
are known. Do not compare a pause/turn-taking result with acknowledgement time
unless the definitions match.

The model card's benchmark results also do not prove production task accuracy,
tool correctness, or a particular concurrent-session capacity. The cited public
materials do not substantiate **80 concurrent PersonaPlex sessions per H100**.
Capacity must be measured on the chosen serving stack with a realistic mix of
speaking, listening, silence, and interruptions.

## Workload and cost sanity check

Assume 100,000 calls per month and a 3–5 minute **billable voice-session**
duration per call:

| Estimate | 3-minute average | 5-minute average |
|---|---:|---:|
| Voice-session minutes/month | 300,000 | 500,000 |
| GPT-Live-1 voice-layer cost at $0.05/min | $15,000 | $25,000 |
| Average concurrent sessions over a 30-day month | 6.9 | 11.6 |

Average concurrency is total session-hours divided by 720 hours/month. It is
not a peak-load estimate. Use actual hourly arrival patterns, call duration
distribution, retries, and service-level targets to size peak capacity. The
GPT-Live-1 estimate excludes backend model and tool charges, telephony, and
other infrastructure. For PersonaPlex, compare a measured all-in cost per
completed call, including GPU reservation/utilization, redundancy, deployment,
monitoring, and engineering operations—not just GPU rental.

## Licensing and deployment caveat

PersonaPlex's repository code is MIT-licensed, but the model weights are governed
by the NVIDIA Open Model License. Call it **open-weight and self-hostable**, not
unqualified "fully open-source." Review the model license and any deployment,
redistribution, and use restrictions before adopting it commercially. Self-hosting
can reduce per-minute vendor fees and network dependence, but it transfers
availability, security, scaling, patching, and GPU-utilization responsibilities
to the operator.

## Focused evaluation plan

Run this as an optional experiment alongside [the LiveKit hands-on track](livekit-hands-on.md).
Keep the fictional `labs/stlab` backend and authorization rules identical for both
models; do not connect the experiment to real company systems or data.

1. **Pin versions and conditions.** Record model/version, SDK, GPU and driver,
   serving configuration, region, audio codec/sample rate, transport, prompt,
   tool schema, and backend model. Use the same scripted caller audio and
   network path where possible.
2. **Measure voice behavior.** Capture p50/p95 end-of-user-speech to first audio,
   interrupt-to-audio-stop, false interruption rate, missed barge-ins, pause
   handling, and recovery after packet loss. Include actual phone/SIP media if
   telephony is in scope.
3. **Measure scheduling correctness.** Reuse the same fictional scenarios:
   lookup, offered-slot selection, reschedule, explicit cancellation confirmation,
   same-day refusal, cross-customer access denial, emergency transfer, and tool
   timeout. Score backend state and audit evidence, not what the assistant says.
4. **Load test before sizing.** Ramp concurrent sessions gradually and sustain
   target load. Record GPU memory/utilization, real-time factor, dropped/late audio,
   queueing, p95/p99 latency, and task success. Test peak arrival bursts and
   failure/restart behavior. Derive safe capacity from an agreed SLO and headroom;
   do not extrapolate from parameter count or a single-session latency test.
5. **Compare economics and quality.** Report cost per completed successful call,
   transfer rate, task completion, confirmation/claim violations, interruption
   quality, and latency by scenario. Include backend/tool costs for GPT-Live and
   idle/reserved GPU plus operations for PersonaPlex.

### Decision rule

- Prefer **GPT-Live-1** if task success, reliability, and engineering time dominate
  and its managed voice-layer cost meets budget.
- Prefer **PersonaPlex** only if its measured quality clears the same task-safety
  bar and its all-in self-hosted cost, data-control benefits, or deployment
  constraints justify operating the model.
- Keep the scheduling control plane model-independent either way. The model may
  propose a tool call; the application validates authorization, confirmation,
  idempotency, and the durable result.

## Source limitations

This is a source-based comparison, not an independent reproduction. Vendor benchmark
scores are not directly comparable unless they use the same benchmark version,
scoring protocol, and runtime conditions. Revisit this page after a reproducible
side-by-side test; do not present the reported latencies or the workload estimate as
measured results from this repository.
