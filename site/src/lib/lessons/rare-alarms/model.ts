// Aha: When an alarm is rare, even a sensitive detector can produce mostly false alarms; prevalence and the threshold set the operational cost.
export interface AlarmRates {
  truePositives: number;
  falseNegatives: number;
  falsePositives: number;
  trueNegatives: number;
}

export interface ThresholdMetrics {
  sensitivity: number;
  specificity: number;
}

function probability(value: number, name: string): number {
  if (!Number.isFinite(value) || value < 0 || value > 1) throw new Error(`${name} must be between 0 and 1`);
  return value;
}

function positiveInteger(value: number, name: string): number {
  if (!Number.isInteger(value) || value <= 0) throw new Error(`${name} must be a positive integer`);
  return value;
}

export function thresholdMetrics(threshold: number): ThresholdMetrics {
  probability(threshold, "threshold");
  return { sensitivity: 1 - 0.45 * threshold, specificity: 0.5 + 0.49 * threshold };
}

export function alarmRates(prevalence: number, sensitivity: number, specificity: number, population = 1000): AlarmRates {
  probability(prevalence, "prevalence");
  probability(sensitivity, "sensitivity");
  probability(specificity, "specificity");
  positiveInteger(population, "population");
  const affected = population * prevalence;
  const unaffected = population - affected;
  return {
    truePositives: affected * sensitivity,
    falseNegatives: affected * (1 - sensitivity),
    falsePositives: unaffected * (1 - specificity),
    trueNegatives: unaffected * specificity,
  };
}

export function positivePredictiveValue(prevalence: number, sensitivity: number, specificity: number): number {
  const rates = alarmRates(prevalence, sensitivity, specificity);
  const alarms = rates.truePositives + rates.falsePositives;
  return alarms === 0 ? 0 : rates.truePositives / alarms;
}

export function weightedAlarmCost(
  prevalence: number,
  sensitivity: number,
  specificity: number,
  falsePositiveCost: number,
  falseNegativeCost: number,
  population = 1000,
): number {
  if (!Number.isFinite(falsePositiveCost) || falsePositiveCost < 0) throw new Error("falsePositiveCost must be non-negative");
  if (!Number.isFinite(falseNegativeCost) || falseNegativeCost < 0) throw new Error("falseNegativeCost must be non-negative");
  const rates = alarmRates(prevalence, sensitivity, specificity, population);
  return rates.falsePositives * falsePositiveCost + rates.falseNegatives * falseNegativeCost;
}
