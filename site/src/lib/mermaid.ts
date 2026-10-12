/**
 * Small, dependency-free renderer for the flowchart subset used in repo docs.
 * It emits accessible inline SVG at build time; unsupported syntax falls back
 * to showing the original Mermaid source.
 */

function escapeXml(value: string): string {
  return value.replace(/&/g, "&amp;").replace(/</g, "&lt;")
    .replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}

interface NodeDef {
  id: string;
  label: string;
  shape: "rect" | "diamond";
  fill?: string;
}

interface EdgeDef {
  from: string;
  to: string;
  label?: string;
}

const NODE_PATTERN = /([A-Za-z][\w-]*)\s*(\[[^\]]*\]|\{[^}]*\})/g;
const EDGE_PATTERN =
  /^\s*([A-Za-z][\w-]*)(?:\s*(?:\[[^\]]*\]|\{[^}]*\}))?\s+(?:--\s*(.*?)\s*-->|-->|---)\s+([A-Za-z][\w-]*)(?:\s*(?:\[[^\]]*\]|\{[^}]*\}))?\s*$/;
const DEFAULT_FILL = "#111c33";
const DEFAULT_TEXT = "#e8eefa";

function wrapLabel(label: string, maxChars = 19): string[] {
  const words = label.replace(/<br\s*\/?>/gi, " ").split(/\s+/).filter(Boolean);
  const lines: string[] = [];
  let line = "";
  for (const word of words) {
    if (line && line.length + word.length + 1 > maxChars) {
      lines.push(line);
      line = word;
    } else {
      line = line ? line + " " + word : word;
    }
  }
  if (line) lines.push(line);
  return lines.length ? lines : [""];
}

function parseColor(line: string): { id: string; fill: string } | null {
  const match = /^\s*style\s+([A-Za-z][\w-]*)\s+.*?fill\s*:\s*(#[0-9a-f]{3,8})/i.exec(line);
  return match ? { id: match[1], fill: match[2] } : null;
}

function luminance(hex: string): number {
  const value = hex.replace("#", "");
  if (![3, 6].includes(value.length)) return 0.1;
  const full = value.length === 3 ? value.split("").map((c) => c + c).join("") : value;
  const channels = [0, 2, 4].map((i) => parseInt(full.slice(i, i + 2), 16) / 255);
  const linear = channels.map((c) => c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4);
  return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2];
}

/** Render flowchart LR/TD syntax with simple node shapes and labelled arrows. */
export function renderMermaidSvg(source: string, id: string): string | null {
  const lines = source.replace(/\r\n/g, "\n").split("\n");
  const header = lines.find((line) => line.trim() !== "")?.trim() ?? "";
  const directionMatch = /^(?:flowchart|graph)\s+(LR|RL|TB|TD|BT)\b/i.exec(header);
  if (!directionMatch) return null;

  const direction = directionMatch[1].toUpperCase();
  const nodes = new Map<string, NodeDef>();
  const edges: EdgeDef[] = [];
  const fills = new Map<string, string>();

  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed || /^(flowchart|graph)\s+/i.test(trimmed) || trimmed.startsWith("%%")) continue;
    const color = parseColor(line);
    if (color) {
      fills.set(color.id, color.fill);
      continue;
    }
    if (/^classDef\b|^class\b|^linkStyle\b/i.test(trimmed)) continue;

    for (const match of line.matchAll(NODE_PATTERN)) {
      const token = match[2];
      const label = token.slice(1, -1).trim();
      if (!nodes.has(match[1])) {
        nodes.set(match[1], {
          id: match[1],
          label,
          shape: token.startsWith("{") ? "diamond" : "rect",
        });
      }
    }

    const edge = EDGE_PATTERN.exec(line);
    if (edge) edges.push({ from: edge[1], label: edge[2]?.trim(), to: edge[3] });
  }

  for (const edge of edges) {
    for (const nodeId of [edge.from, edge.to]) {
      if (!nodes.has(nodeId)) nodes.set(nodeId, { id: nodeId, label: nodeId, shape: "rect" });
    }
  }
  if (nodes.size === 0 || edges.length === 0) return null;

  for (const node of nodes.values()) node.fill = fills.get(node.id);
  const ordered = [...nodes.values()];
  if (direction === "RL" || direction === "BT") ordered.reverse();
  const index = new Map(ordered.map((node, i) => [node.id, i]));

  const nodeWidth = 166;
  const nodeHeight = 64;
  const gap = 52;
  const left = 34;
  const centerY = 124;
  const width = left * 2 + ordered.length * nodeWidth + Math.max(0, ordered.length - 1) * gap;
  const height = 252;
  const nodeX = (nodeId: string) => left + (index.get(nodeId) ?? 0) * (nodeWidth + gap) + nodeWidth / 2;
  const titleId = id + "-title";
  const descId = id + "-description";

  const edgeMarkup = edges.map((edge) => {
    const fromIndex = index.get(edge.from);
    const toIndex = index.get(edge.to);
    if (fromIndex === undefined || toIndex === undefined) return "";
    const fromX = nodeX(edge.from);
    const toX = nodeX(edge.to);
    const forward = toIndex > fromIndex;
    const x1 = fromX + (forward ? nodeWidth / 2 : -nodeWidth / 2);
    const x2 = toX + (forward ? -nodeWidth / 2 : nodeWidth / 2);
    const routeY = forward ? 28 : 220;
    const path = Math.abs(toIndex - fromIndex) === 1
      ? "M " + x1 + " " + centerY + " L " + x2 + " " + centerY
      : "M " + x1 + " " + centerY + " C " + (x1 + (forward ? 28 : -28)) + " " + routeY + ", " +
        (x2 - (forward ? 28 : -28)) + " " + routeY + ", " + x2 + " " + centerY;
    const labelX = (x1 + x2) / 2;
    const labelY = forward ? 38 : 232;
    const label = edge.label
      ? '<text class="edge-label" x="' + labelX + '" y="' + labelY + '" text-anchor="middle">' + escapeXml(edge.label) + "</text>"
      : "";
    return '<g class="diagram-edge"><path d="' + path + '" marker-end="url(#' + id + '-arrow)" />' + label + "</g>";
  }).join("");

  const nodeMarkup = ordered.map((node) => {
    const x = nodeX(node.id);
    const fill = node.fill ?? DEFAULT_FILL;
    const textColor = node.fill && luminance(fill) > 0.38 ? "#0a1224" : DEFAULT_TEXT;
    const lines = wrapLabel(node.label);
    const lineHeight = 16;
    const startY = centerY - ((lines.length - 1) * lineHeight) / 2 + 4;
    const text = lines.map((line, i) =>
      '<tspan x="' + x + '" y="' + (startY + i * lineHeight) + '">' + escapeXml(line) + "</tspan>",
    ).join("");
    const shape = node.shape === "diamond"
      ? '<polygon points="' + x + "," + (centerY - 39) + " " + (x + nodeWidth / 2) + "," + centerY + " " +
        x + "," + (centerY + 39) + " " + (x - nodeWidth / 2) + "," + centerY + '" />'
      : '<rect x="' + (x - nodeWidth / 2) + '" y="' + (centerY - nodeHeight / 2) + '" width="' +
        nodeWidth + '" height="' + nodeHeight + '" rx="10" />';
    return '<g class="diagram-node" style="--node-fill:' + escapeXml(fill) + ";--node-text:" + textColor + '">' +
      shape + '<text text-anchor="middle">' + text + "</text></g>";
  }).join("");

  return '<svg class="mermaid-svg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ' + width + " " + height +
    '" width="' + width + '" height="' + height + '" role="img" aria-labelledby="' + titleId + " " + descId + '">' +
    '<title id="' + titleId + '">Workflow diagram</title>' +
    '<desc id="' + descId + '">A vector flowchart with connected steps and decision branches.</desc>' +
    '<defs><marker id="' + id + '-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#37e0ff" /></marker></defs>' +
    '<g class="diagram-edges">' + edgeMarkup + '</g><g class="diagram-nodes">' + nodeMarkup + '</g>' +
    '<style>.diagram-edge path{fill:none;stroke:#6682ad;stroke-width:1.8}.diagram-edge .edge-label{fill:#a8b5d1;font:600 12px system-ui,sans-serif;paint-order:stroke;stroke:#0a1224;stroke-width:4px;stroke-linejoin:round}.diagram-node rect,.diagram-node polygon{fill:var(--node-fill);stroke:#37e0ff;stroke-width:1.6}.diagram-node text{fill:var(--node-text);font:500 13px system-ui,sans-serif}</style></svg>';
}
