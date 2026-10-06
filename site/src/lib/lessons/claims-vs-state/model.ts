export type EventKind = "spoken" | "database";

export interface TimelineEvent {
  kind: EventKind;
  label: string;
  detail: string;
  time: number;
}

export interface SimulationOptions {
  interrupted?: boolean;
  retry?: boolean;
  idempotent?: boolean;
  claimGuard?: boolean;
}

export interface SimulationResult {
  spoken: TimelineEvent[];
  database: TimelineEvent[];
  outcome: "confirmed" | "blocked" | "duplicate" | "uncertain";
  summary: string;
}

const claim = (label: string, detail: string, time: number): TimelineEvent => ({ kind: "spoken", label, detail, time });
const state = (label: string, detail: string, time: number): TimelineEvent => ({ kind: "database", label, detail, time });

export function simulate(options: SimulationOptions = {}): SimulationResult {
  const { interrupted = false, retry = false, idempotent = true, claimGuard = true } = options;
  const spoken: TimelineEvent[] = [claim("Caller claim", "\"Book me for Tuesday at 10.\"", 1)];
  const database: TimelineEvent[] = [state("Read availability", "Tuesday 10:00 is open", 2)];

  if (interrupted) {
    spoken.push(claim("Interruption", "Caller cuts in: \"Actually, cancel that.\"", 3));
    database.push(state("Write paused", "No booking committed", 4));
    return { spoken, database, outcome: "uncertain", summary: "The interruption changes the claim before the write. Pause and re-ground instead of treating speech as state." };
  }

  spoken.push(claim("Agent claim", "\"You are booked for Tuesday at 10.\"", 3));
  if (retry && !idempotent) {
    database.push(state("Create booking", "Appointment A-2001 created", 4), state("Retry write", "Appointment A-2002 created", 5));
    return { spoken, database, outcome: "duplicate", summary: "A retried write created two appointments. A spoken confirmation is not proof that one durable state exists." };
  }

  database.push(state("Create booking", "Appointment A-2001 created", 4));
  if (retry) database.push(state("Retry write", idempotent ? "Same request key; no second appointment" : "Duplicate appointment", 5));
  if (claimGuard) {
    spoken.push(claim("Grounded confirmation", "\"Appointment A-2001 is booked.\"", 6));
    return { spoken, database, outcome: "confirmed", summary: "The agent confirms only after reading durable state, and the idempotency key makes a retry safe." };
  }
  return { spoken, database, outcome: "uncertain", summary: "The agent speaks confidently, but without a claim guard the words remain only a claim." };
}

export function eventKinds(events: TimelineEvent[]): EventKind[] {
  return events.map(({ kind }) => kind);
}
