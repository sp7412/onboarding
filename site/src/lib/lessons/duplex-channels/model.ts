export type ConversationMode = "turn-based" | "full-duplex";
export type Channel = "instructions" | "thinking" | "commentary";

export interface ChannelResult {
  accepted: boolean;
  spoken: boolean;
  reason: string;
}

export function modeSummary(mode: ConversationMode): string {
  return mode === "turn-based"
    ? "The caller and agent take turns. Endpointing decides when the next turn can begin."
    : "The live model can listen while speaking, so interruptions and backchannels can overlap."
}

export function channelResult(channel: Channel, verified: boolean): ChannelResult {
  if (channel === "thinking") {
    return { accepted: true, spoken: false, reason: "Useful progress stays quiet and gives the live model context." };
  }
  if (channel === "commentary") {
    return verified
      ? { accepted: true, spoken: true, reason: "Verified results can be paraphrased aloud." }
      : { accepted: false, spoken: false, reason: "Do not speak an unverified result, especially a booking confirmation." };
  }
  return { accepted: true, spoken: false, reason: "Instructions change the model's direction; they are not a spoken reply." };
}

export function challengeMessage(channel: Channel, verified: boolean): string {
  const result = channelResult(channel, verified);
  return result.accepted
    ? result.spoken ? "Safe to say aloud: the backend has committed the result." : "Accepted as quiet control-plane context."
    : "Blocked: keep this update in thinking until the backend verifies it.";
}
