export type CallerContext = "complete" | "unfinished";

export interface EndpointInput {
  silenceMs: number;
  minSilenceMs: number;
  maxSilenceMs: number;
  context: CallerContext;
}

export interface EndpointResult {
  action: "commit" | "wait";
  waitMs: number;
  reason: "minimum-silence" | "maximum-silence" | "context" | "listening";
}

function valid(input: EndpointInput): void {
  if (input.silenceMs < 0 || input.minSilenceMs < 0 || input.maxSilenceMs < input.minSilenceMs) {
    throw new Error("invalid endpoint timing");
  }
  if (input.context !== "complete" && input.context !== "unfinished") {
    throw new Error("invalid caller context");
  }
}

/** A small teaching model: silence starts the timer; context decides whether it can finish early. */
export function endpoint(input: EndpointInput): EndpointResult {
  valid(input);
  const waitMs = Math.min(input.silenceMs, input.maxSilenceMs);
  if (input.silenceMs >= input.maxSilenceMs) {
    return { action: "commit", waitMs, reason: "maximum-silence" };
  }
  if (input.silenceMs < input.minSilenceMs) {
    return { action: "wait", waitMs, reason: "listening" };
  }
  if (input.context === "complete") {
    return { action: "commit", waitMs, reason: "minimum-silence" };
  }
  return { action: "wait", waitMs, reason: "context" };
}

export function timerProgress(silenceMs: number, maxSilenceMs: number): number {
  if (silenceMs < 0 || maxSilenceMs <= 0) throw new Error("invalid timer values");
  return Math.min(1, silenceMs / maxSilenceMs);
}
