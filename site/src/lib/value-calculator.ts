/**
 * Illustrative value model for one contractor: a voice agent answers after-hours calls that
 * currently go unanswered. Every benefit and cost below comes from those same calls.
 *
 *   missed      = calls × after-hours share × (1 − after-hours answer rate)
 *   booked      = missed × agent booking rate
 *   false       = booked × false-booking rate          (wrong job, not bookable, no-show)
 *   completed   = (booked − false) × completion rate   (valid bookings that become paid jobs)
 *   revenue     = completed × average ticket
 *   profit      = revenue × gross margin
 *   costs       = false × wasted-roll cost + missed × agent cost per call
 *   net         = profit − costs
 */
export interface ValueInputs {
  monthlyCalls: number;
  afterHoursShare: number;
  afterHoursAnswerRate: number;
  agentBookingRate: number;
  falseBookingRate: number;
  completionRate: number;
  averageTicket: number;
  grossMargin: number;
  wastedTruckRollCost: number;
  agentCostPerCall: number;
}

export interface ValueResult {
  missedCalls: number;
  agentBookings: number;
  falseBookings: number;
  completedJobs: number;
  addedRevenue: number;
  addedGrossProfit: number;
  wastedRollCost: number;
  agentCost: number;
  netValue: number;
}

const rate = (v: number) => (Number.isFinite(v) ? Math.max(0, Math.min(1, v)) : 0);
const amount = (v: number) => (Number.isFinite(v) ? Math.max(0, v) : 0);

export function calculateValue(input: ValueInputs): ValueResult {
  const missedCalls = amount(input.monthlyCalls) * rate(input.afterHoursShare) * (1 - rate(input.afterHoursAnswerRate));
  const agentBookings = missedCalls * rate(input.agentBookingRate);
  const falseBookings = agentBookings * rate(input.falseBookingRate);
  const completedJobs = (agentBookings - falseBookings) * rate(input.completionRate);
  const addedRevenue = completedJobs * amount(input.averageTicket);
  const addedGrossProfit = addedRevenue * rate(input.grossMargin);
  const wastedRollCost = falseBookings * amount(input.wastedTruckRollCost);
  const agentCost = missedCalls * amount(input.agentCostPerCall);
  return {
    missedCalls,
    agentBookings,
    falseBookings,
    completedJobs,
    addedRevenue,
    addedGrossProfit,
    wastedRollCost,
    agentCost,
    netValue: addedGrossProfit - wastedRollCost - agentCost,
  };
}

/** Break-even false-booking rate: above this, the agent loses money on the calls it books. */
export function breakEvenFalseBookingRate(input: ValueInputs): number {
  const perBooking = rate(input.completionRate) * amount(input.averageTicket) * rate(input.grossMargin);
  const swing = perBooking + amount(input.wastedTruckRollCost);
  return swing === 0 ? 0 : rate(perBooking / swing);
}
