import fs from "node:fs";
import path from "node:path";
import { describe, expect, it } from "vitest";
import {
  ARCHITECTURES, KNOBS, NODES, SOURCES, costRange, defaultChoices, pathNodes, pathRange, trail,
  type Figure,
} from "./model";

const PAGES = path.resolve(__dirname, "../../pages");
const ROUTE_FILES: Record<string, string> = {
  labs: "labs.astro", simulations: "simulations.astro",
};

function figures(): [string, Figure][] {
  const out: [string, Figure][] = [];
  for (const n of Object.values(NODES)) {
    if (n.latency) out.push([`${n.id}.latency`, n.latency]);
    if (n.cost) out.push([`${n.id}.cost`, n.cost]);
  }
  for (const k of Object.values(KNOBS)) {
    for (const o of k.options) {
      for (const [id, f] of Object.entries({ ...o.latency, ...o.cost })) out.push([`${k.id}.${o.id}.${id}`, f]);
    }
  }
  return out;
}

describe("architecture model integrity", () => {
  it("has consistent ids and children that exist", () => {
    for (const [key, n] of Object.entries(NODES)) {
      expect(n.id).toBe(key);
      for (const c of n.children ?? []) expect(NODES[c], `${key} → ${c}`).toBeDefined();
    }
  });

  it("is a tree: every node has at most one parent and no cycles", () => {
    const parents = new Map<string, string>();
    for (const n of Object.values(NODES)) {
      for (const c of n.children ?? []) {
        expect(parents.has(c), `${c} has two parents`).toBe(false);
        parents.set(c, n.id);
      }
    }
    for (const id of Object.keys(NODES)) {
      const seen = new Set<string>();
      let cur: string | undefined = id;
      while (cur) {
        expect(seen.has(cur), `cycle at ${id}`).toBe(false);
        seen.add(cur);
        cur = parents.get(cur);
      }
      expect(seen.size).toBeLessThanOrEqual(4);   // drill-down depth
    }
  });

  it("gives every figure a valid range, a basis, a note, and real sources where claimed", () => {
    for (const [where, f] of figures()) {
      expect(f.lo, where).toBeGreaterThanOrEqual(0);
      expect(f.hi, where).toBeGreaterThanOrEqual(f.lo);
      expect(f.note.length, where).toBeGreaterThan(10);
      for (const s of f.sources ?? []) expect(SOURCES[s], `${where} source ${s}`).toBeDefined();
      if (["vendor", "standard", "docs", "derived", "estimate", "teaching"].includes(f.basis)) {
        expect(f.sources?.length ?? 0, `${where} (${f.basis}) needs a source`).toBeGreaterThan(0);
      }
    }
  });

  it("wires architectures to existing nodes and knobs", () => {
    for (const a of ARCHITECTURES) {
      for (const id of [...a.hotPath, ...a.background, ...a.costNodes, ...pathNodes(a.firstSound), ...pathNodes(a.answer)]) {
        expect(NODES[id], `${a.id}: ${id}`).toBeDefined();
      }
      for (const k of a.knobs) expect(KNOBS[k], `${a.id}: knob ${k}`).toBeDefined();
      for (const id of [...pathNodes(a.firstSound), ...pathNodes(a.answer)]) {
        expect(trail(id, [...a.hotPath, ...a.background]), `${a.id}: ${id} not reachable from a block`).not.toBeNull();
      }
      for (const s of a.benchmark?.sources ?? []) expect(SOURCES[s]).toBeDefined();
    }
  });

  it("has knob patches that target nodes with the same kind of figure", () => {
    for (const k of Object.values(KNOBS)) {
      expect(k.options.some((o) => o.id === k.defaultId)).toBe(true);
      for (const o of k.options) {
        for (const id of Object.keys(o.latency ?? {})) expect(NODES[id]?.latency, `${k.id}.${o.id}: ${id}`).toBeDefined();
        for (const id of Object.keys(o.cost ?? {})) expect(NODES[id]?.cost, `${k.id}.${o.id}: ${id}`).toBeDefined();
      }
    }
  });

  it("links only to site routes that exist (or external https URLs)", () => {
    const docs = fs.readFileSync(path.resolve(__dirname, "../content/repo.ts"), "utf8");
    for (const n of Object.values(NODES)) {
      for (const l of n.learn ?? []) {
        if (l.href.startsWith("https://")) continue;
        const [route] = l.href.split("#");
        const parts = route.split("/").filter(Boolean);
        if (parts[0] === "docs") expect(docs, l.href).toMatch(new RegExp(`${parts[1]}\\.md"|slug: "${parts[1]}"`));
        else if (parts[0] === "lessons") expect(fs.existsSync(path.join(PAGES, "lessons", `${parts[1]}.astro`)), l.href).toBe(true);
        else if (parts[0] === "whitepaper") expect(fs.existsSync(path.resolve(__dirname, "../../../../docs/whitepaper", `${parts[1]}.md`)), l.href).toBe(true);
        else expect(fs.existsSync(path.join(PAGES, ROUTE_FILES[parts[0]] ?? `${parts[0]}.astro`)), l.href).toBe(true);
      }
    }
  });
});

describe("architecture calculations", () => {
  const byId = Object.fromEntries(ARCHITECTURES.map((a) => [a.id, a]));
  const d = defaultChoices();

  it("sums a sequential path", () => {
    // netIn 20–150, endpointing 500–800, sttFinal 50–300, llmTtft 150–500, ttsFirst 100–400, playout 40–200
    expect(pathRange(byId.cascaded.firstSound, byId.cascaded, d)).toEqual({ lo: 860, hi: 2350 });
  });

  it("takes the slowest branch of a parallel step", () => {
    const fast = pathRange(byId.duplex.answer, byId.duplex, d);
    // netIn + max(liveTurn 600–1000, delegate+think+policy+tool 475–1210) + commentary + playout
    expect(fast).toEqual({ lo: 20 + 600 + 200 + 40, hi: 150 + 1210 + 600 + 200 });
  });

  it("applies knob choices only to architectures that use the knob", () => {
    const slow = { ...d, endpoint: "cautious" };
    expect(pathRange(byId.cascaded.firstSound, byId.cascaded, slow).lo).toBe(860 + 300);
    expect(pathRange(byId.duplex.firstSound, byId.duplex, slow)).toEqual(pathRange(byId.duplex.firstSound, byId.duplex, d));
  });

  it("keeps full-duplex first sound independent of the backend model", () => {
    const astra = { ...d, backendModel: "astra" };
    expect(pathRange(byId.duplex.firstSound, byId.duplex, astra)).toEqual(pathRange(byId.duplex.firstSound, byId.duplex, d));
    expect(pathRange(byId.duplex.answer, byId.duplex, astra).hi).toBeGreaterThan(pathRange(byId.duplex.answer, byId.duplex, d).hi);
  });

  it("orders cost per minute as the sources imply", () => {
    const cost = (id: string, c = d) => costRange(byId[id], c);
    expect(cost("cascaded").hi).toBeLessThan(cost("s2s").lo);          // small text model vs audio tokens
    expect(cost("duplex").lo).toBeGreaterThanOrEqual(0.05);            // $0.05/min voice layer
    expect(cost("cascaded", { ...d, textModel: "astra" }).lo).toBeGreaterThan(cost("cascaded").hi);
  });
});
