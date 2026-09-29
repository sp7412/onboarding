/**
 * Stable content IDs: a readable slug plus a short hash of the item text, so
 * localStorage progress survives small edits elsewhere in the source file but
 * changes if the item's own text changes (making stale progress visible).
 */
export function hash8(text: string): string {
  // FNV-1a 32-bit, hex-encoded, zero-padded to 8 chars.
  let h = 0x811c9dc5;
  for (let i = 0; i < text.length; i++) {
    h ^= text.charCodeAt(i);
    h = Math.imul(h, 0x01000193) >>> 0;
  }
  return h.toString(16).padStart(8, "0");
}

export function slugify(text: string): string {
  return text
    .toLowerCase()
    .normalize("NFKD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, 60);
}

/** contentId = `<prefix>-<slug>-<hash8(canonical text)>` */
export function contentId(prefix: string, slugSource: string, text: string): string {
  const slug = slugify(slugSource) || "item";
  return `${prefix}-${slug}-${hash8(text.replace(/\s+/g, " ").trim())}`;
}
