export const lessons = [
  { slug: "pass-k", title: "The eight-step booking call", aha: "Reliability compounds: 90% per step becomes about 43% across eight steps.", related: "Lab 07", time: "8 min" },
  { slug: "latency-tail", title: "The caller feels the tail", aha: "Typical stage times do not predict the slow calls a caller remembers.", related: "Lab 08", time: "8 min" },
  { slug: "rare-alarms", title: "The rare emergency alarm", aha: "Rare emergencies make false alarms dominate, so threshold is a cost decision.", related: "Lab 02", time: "7 min" },
  { slug: "endpointing", title: "When is the caller done?", aha: "One silence timer cannot fit both yes and a phone number.", related: "Lab 03", time: "7 min" },
  { slug: "claims-vs-state", title: "Words versus the record", aha: "The system of record and the agent's words are separate timelines.", related: "Labs 02 and 07", time: "7 min" },
  { slug: "heard-vs-generated", title: "What did the caller hear?", aha: "After barge-in, memory must match heard audio, not generated audio.", related: "Lab 01 section 4", time: "6 min" },
  { slug: "peak-queue", title: "The hot-day queue", aha: "Wait times explode as call volume nears capacity.", related: "Whitepaper chapters 02 and 04", time: "8 min" },
  { slug: "denominator", title: "The denominator changes the rate", aha: "Booking rate depends on whether unbookable calls count.", related: "Whitepaper chapter 11", time: "6 min" },
  { slug: "duplex-channels", title: "Thinking is not speaking", aha: "In full duplex, only verified results belong in commentary.", related: "GPT-Live-1", time: "7 min" },
  { slug: "worth-it", title: "When does the agent pay off?", aha: "Recovered booking value must exceed call cost plus mistake cost.", related: "Whitepaper chapter 11", time: "7 min" },
  { slug: "earned-autonomy", title: "When has the agent earned it?", aha: "Zero errors in 48 calls doesn't prove under 5%: promote on the upper bound, demote on the lower.", related: "Labs 13–14", time: "8 min" },
] as const;
