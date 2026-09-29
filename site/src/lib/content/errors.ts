/**
 * One parse failure aborts the build with the file and the unmet expectation,
 * so a source-file format change can never silently drop content.
 */
export class ContentError extends Error {
  constructor(file: string, expectation: string, detail?: string) {
    super(`content parse failed in ${file}: ${expectation}${detail ? ` — ${detail}` : ""}`);
    this.name = "ContentError";
  }
}

export function fail(file: string, expectation: string, detail?: string): never {
  throw new ContentError(file, expectation, detail);
}

/** Ensure a required condition holds, or fail with file + expectation. */
export function expectCondition(
  file: string,
  expectation: string,
  condition: boolean,
  detail?: string,
): void {
  if (!condition) fail(file, expectation, detail);
}
