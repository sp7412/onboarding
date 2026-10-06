import { describe, expect, it } from "vitest";
import { eventKinds, simulate } from "./model";

describe("claims versus state model", () => {
  it("keeps spoken claims separate from database state", () => {
    const result = simulate();
    expect(eventKinds(result.spoken)).toEqual(["spoken", "spoken", "spoken"]);
    expect(eventKinds(result.database)).toEqual(["database", "database"]);
    expect(result.outcome).toBe("confirmed");
  });

  it("does not commit a write after an interruption", () => {
    const result = simulate({ interrupted: true });
    expect(result.database.at(-1)?.label).toBe("Write paused");
    expect(result.outcome).toBe("uncertain");
  });

  it("makes a retried request safe when idempotent", () => {
    expect(simulate({ retry: true }).outcome).toBe("confirmed");
    expect(simulate({ retry: true }).database.at(-1)?.detail).toContain("no second appointment");
  });

  it("shows the duplicate caused by a non-idempotent retry", () => {
    const result = simulate({ retry: true, idempotent: false });
    expect(result.outcome).toBe("duplicate");
    expect(result.database).toHaveLength(3);
  });

  it("requires a claim guard before confirmation", () => {
    expect(simulate({ claimGuard: false }).outcome).toBe("uncertain");
  });
});
