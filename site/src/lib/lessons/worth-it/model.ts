export interface WorthItInputs {
  costPerMinute: number;
  callLengthMinutes: number;
  bookingLift: number;
  jobValue: number;
  errorCost: number;
}

export interface WorthItResult {
  callCost: number;
  incrementalJobValue: number;
  expectedErrorCost: number;
  netValue: number;
  isWorthIt: boolean;
}

function assertFiniteNonNegative(value: number, name: string): void {
  if (!Number.isFinite(value) || value < 0) throw new Error(`${name} must be finite and non-negative`);
}

export function calculateWorthIt(inputs: WorthItInputs): WorthItResult {
  Object.entries(inputs).forEach(([name, value]) => assertFiniteNonNegative(value, name));

  const callCost = inputs.costPerMinute * inputs.callLengthMinutes;
  const incrementalJobValue = inputs.bookingLift * inputs.jobValue;
  const expectedErrorCost = inputs.errorCost;
  const netValue = incrementalJobValue - expectedErrorCost - callCost;

  return { callCost, incrementalJobValue, expectedErrorCost, netValue, isWorthIt: netValue >= 0 };
}

export function formatDollars(value: number): string {
  return `$${value.toFixed(2)}`;
}
