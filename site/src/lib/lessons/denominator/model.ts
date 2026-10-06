export type DenominatorMode = "all-calls" | "bookable";

export interface CallCounts {
  allCalls: number;
  bookableCalls: number;
  bookedCalls: number;
}

function validate(counts: CallCounts): void {
  const values = Object.values(counts);
  if (values.some((value) => !Number.isFinite(value) || value < 0 || !Number.isInteger(value))) {
    throw new Error("call counts must be non-negative integers");
  }
  if (counts.bookableCalls > counts.allCalls) throw new Error("bookable calls cannot exceed all calls");
  if (counts.bookedCalls > counts.bookableCalls) throw new Error("booked calls cannot exceed bookable calls");
}

export function denominator(counts: CallCounts, mode: DenominatorMode): number {
  validate(counts);
  return mode === "all-calls" ? counts.allCalls : counts.bookableCalls;
}

export function bookingRate(counts: CallCounts, mode: DenominatorMode): number {
  const base = denominator(counts, mode);
  return base === 0 ? 0 : counts.bookedCalls / base;
}

export function percent(counts: CallCounts, mode: DenominatorMode): number {
  return bookingRate(counts, mode) * 100;
}

export function rateSummary(counts: CallCounts, mode: DenominatorMode): string {
  const label = mode === "all-calls" ? "all calls" : "bookable calls";
  return `${counts.bookedCalls} booked / ${denominator(counts, mode)} ${label} = ${percent(counts, mode).toFixed(1)}%`;
}
