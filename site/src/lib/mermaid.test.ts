import { describe, expect, it } from "vitest";
import { renderMermaidSvg } from "./mermaid";

describe("renderMermaidSvg", () => {
  it("renders labelled flowchart edges and decision nodes as accessible SVG", () => {
    const svg = renderMermaidSvg(
      [
        "flowchart LR",
        "A[Call arrives] --> B{Safe to book?}",
        "B -- yes --> C[Book appointment]",
        "B -- no --> D[Transfer to a person]",
      ].join("\n"),
      "contractor-flow",
    );

    expect(svg).not.toBeNull();
    expect(svg).toContain("<svg");
    expect(svg).toContain('role="img"');
    expect(svg).toContain("Call arrives");
    expect(svg).toContain("Safe to book?");
    expect(svg).toContain(">yes</text>");
    expect(svg).toContain(">no</text>");
    expect(svg).toContain("<polygon");
    expect(svg).toContain("marker-end");
  });

  it("uses authored node fill colors when provided", () => {
    const svg = renderMermaidSvg(
      "flowchart LR\nA[Start] --> B[Done]\nstyle B fill:#e8f7ed",
      "styled-flow",
    );

    expect(svg).toContain("--node-fill:#e8f7ed");
  });

  it("returns null for syntax outside the supported flowchart subset", () => {
    expect(renderMermaidSvg("sequenceDiagram\nA->>B: hello", "unsupported")).toBeNull();
  });
});
