export interface ValueInputs {
  monthlyCalls: number;
  afterHoursShare: number;
  currentAnswerRate: number;
  agentBookingRate: number;
  averageTicket: number;
  closeRate: number;
  falseBookingRate: number;
  wastedTruckRollCost: number;
}

export interface ValueResult {
  missedAfterHoursCalls: number;
  agentHandledCalls: number;
  addedBookedJobs: number;
  addedRevenue: number;
  wastedRollCost: number;
  netValue: number;
}

function clampRate(value: number): number {
  return Math.max(0, Math.min(1, value));
}

export function calculateValue(input: ValueInputs): ValueResult {
  const calls = Math.max(0, input.monthlyCalls);
  const afterHours = clampRate(input.afterHoursShare);
  const answer = clampRate(input.currentAnswerRate);
  const booking = clampRate(input.agentBookingRate);
  const close = clampRate(input.closeRate);
  const falseBooking = clampRate(input.falseBookingRate);
  const missedAfterHoursCalls = calls * afterHours * (1 - answer);
  const recovered = calls * (answer + afterHours * (1 - answer));
  const addedBookedJobs = missedAfterHoursCalls * booking;
  const agentHandledCalls = recovered;
  const addedRevenue = addedBookedJobs * close * Math.max(0, input.averageTicket);
  const agentBookedJobs = agentHandledCalls * booking;
  const wastedRollCost = agentBookedJobs * falseBooking * Math.max(0, input.wastedTruckRollCost);
  return {
    missedAfterHoursCalls,
    agentHandledCalls,
    addedBookedJobs,
    addedRevenue,
    wastedRollCost,
    netValue: addedRevenue - wastedRollCost,
  };
}
