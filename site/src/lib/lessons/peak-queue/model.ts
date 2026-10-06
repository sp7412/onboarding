export interface QueueMetrics {
  utilization: number;
  probabilityOfWaiting: number;
  expectedWaitMinutes: number;
}

/** Erlang C for a lossless M/M/c queue: Poisson arrivals, exponential service. */
export function erlangC(arrivalsPerHour: number, serviceMinutes: number, staff: number): QueueMetrics {
  if (arrivalsPerHour < 0 || serviceMinutes <= 0 || !Number.isInteger(staff) || staff < 1) {
    throw new Error("invalid queue inputs");
  }

  const serviceRate = 60 / serviceMinutes;
  const offeredLoad = arrivalsPerHour / serviceRate;
  const utilization = offeredLoad / staff;
  if (utilization >= 1) {
    return { utilization, probabilityOfWaiting: 1, expectedWaitMinutes: Infinity };
  }

  let sum = 0;
  for (let n = 0; n < staff; n += 1) sum += offeredLoad ** n / factorial(n);
  const tail = offeredLoad ** staff / (factorial(staff) * (1 - utilization));
  const probabilityOfWaiting = tail / (sum + tail);
  const expectedWaitMinutes = probabilityOfWaiting / (staff * serviceRate - arrivalsPerHour) * 60;
  return { utilization, probabilityOfWaiting, expectedWaitMinutes };
}

function factorial(value: number): number {
  let result = 1;
  for (let n = 2; n <= value; n += 1) result *= n;
  return result;
}
