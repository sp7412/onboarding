# Local full-duplex speech-to-speech experiment

**Status:** optional, hardware-dependent experiment. This is a reproducible setup and evaluation plan, not a claim that a model has been installed or tested.

## Goal

Run a self-hosted speech-to-speech model locally, talk to it through its supported demo interface, and measure real interaction behavior before integrating tools. Keep this experiment separate from the core onboarding path and from any company systems, accounts, customer data, or recordings.

## Choose a backend

- **Kyutai Moshi:** start here for the simplest baseline supported by the current official project instructions: https://github.com/kyutai-labs/moshi
- **NVIDIA PersonaPlex:** optional follow-on for role/voice conditioning: https://github.com/NVIDIA/personaplex and https://huggingface.co/nvidia/personaplex-7b-v1

Do not assume their installation commands, Python versions, model repositories, weight licenses, memory requirements, or server flags are interchangeable. Check the selected project's current README and model card before running commands.

## Hardware and preflight

Before installing anything, record OS/version, CPU architecture, Python version, available disk space, GPU model/VRAM/driver/CUDA where applicable, or Apple Silicon chip/unified memory. Also record the selected backend, model revision, quantization, expected download size, and license/terms.

Use a backend the official project supports for the detected hardware. Treat memory thresholds as estimates, not guarantees. If there is no documented supported backend for the machine, stop rather than silently falling back to CPU.

## Safe setup protocol

1. Work in a dedicated directory such as ~/moshi-demo, outside this repository.
2. Read the official README and model card at run time; do not rely on copied commands or remembered flags.
3. Create an isolated virtual environment using the project's documented Python version and package manager.
4. Resolve exact model files and revisions. Report download size and disk requirements before downloading weights; wait for approval if the download is unexpectedly large or license acceptance is required.
5. Install only project-scoped dependencies. Do not use sudo, alter system Python, or install system-wide packages without explicit approval.
6. Launch the documented local server. Prefer localhost; only configure TLS if the actual browser/device access path requires it.
7. Test server startup and model loading separately from browser microphone access and a real conversation.
8. If a step fails, capture the error, state a falsifiable hypothesis, and propose a fix before trying a materially different approach.

## Suggested local artifacts

Keep runtime artifacts in ~/moshi-demo, not in this repo:
- README.md: exact commands, versions, model revision, license notes, and known limitations.
- run.sh: a minimal launcher based on the verified official command.
- smoke_test.sh: checks the documented startup/health signal without pretending to validate live conversation quality.
- results.md: hardware, configuration, observations, and failures.

Never commit downloaded weights, credentials, recordings, or machine-specific secrets. A checked-in launcher should not invent model names or flags; create it only after official instructions have been verified on the target machine.

## Evaluation plan

Start with a tiny, repeatable manual test set. Use no customer or company data.

| Test | Observation |
|---|---|
| Basic exchange | Does audio input produce intelligible audio output? |
| Natural pause | Does the model avoid treating every pause as end of turn? |
| Barge-in | Can the user interrupt generated speech? |
| Stop latency | Time from user interruption to assistant audio stopping |
| Turn-taking | End of user speech to first assistant audio |
| False interruption | Does noise or a short pause incorrectly interrupt? |
| Recovery | Behavior after browser reconnect or simulated server restart |
| Repeatability | Same setup and test script produce comparable observations |

Report p50 and p95 only after collecting enough repeated observations; label sample size and measurement boundaries. Distinguish model-reported benchmark metrics from end-to-end measurements. A working demo is not evidence of task correctness, production reliability, or concurrent-call capacity.

## Acceptance criteria

- [ ] Hardware/backend compatibility checked against official documentation.
- [ ] Model revision, license, download size, and environment recorded.
- [ ] Server starts and model loads without errors.
- [ ] Browser microphone permission and a real conversation are manually verified.
- [ ] Interruptions and natural pauses tested with repeatable scenarios.
- [ ] Results and limitations recorded; no unsupported performance claims.
- [ ] No company data, secrets, or recordings entered into the experiment.

## Next step: guarded tool use

Only after the standalone demo passes, consider connecting a voice model to the repo's fictional scheduling backend. Keep authorization, booking state, idempotency, and escalation in the application control plane. The speech model must not be the authority for whether a booking actually happened.
