// Aha: Reliability compounds: a task passed 90% of the time succeeds on all 8 tries only about 43% of the time (0.9^8), so repeat-trial success predicts production.
export function repeatedSuccess(singleTrialRate: number, attempts: number): number {
  if (singleTrialRate < 0 || singleTrialRate > 1 || attempts < 0) throw new Error("invalid probability or attempt count");
  return singleTrialRate ** attempts;
}

export function trialOutcome(singleTrialRate: number, attempts: number, random: number[]): boolean {
  if (random.length < attempts) throw new Error("not enough trial values");
  return random.slice(0, attempts).every((value) => value < singleTrialRate);
}
