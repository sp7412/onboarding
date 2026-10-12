import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { checkLinks } from "./check-links.mjs";

function fixture(t) {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "site-link-check-"));
  t.after(() => fs.rmSync(root, { recursive: true, force: true }));
  fs.mkdirSync(path.join(root, "docs"), { recursive: true });
  fs.writeFileSync(
    path.join(root, "index.html"),
    '<a href="/onboarding/docs/">docs</a><a href="#top">top</a><h1 id="top">Home</h1>',
  );
  fs.writeFileSync(
    path.join(root, "docs", "index.html"),
    '<a href="/onboarding/">home</a><h2 id="8-numbered-heading">Heading</h2>',
  );
  return root;
}

test("accepts base-path links, query strings, and numeric heading anchors", async (t) => {
  const root = fixture(t);
  fs.writeFileSync(
    path.join(root, "index.html"),
    '<a href="/onboarding/docs/?view=1#8-numbered-heading">docs</a>' +
      '<a href="/onboarding/docs/#8-numbered-heading">anchor</a>',
  );
  const result = await checkLinks({ dist: root });
  assert.deepEqual(result.broken, []);
  assert.equal(result.pages, 2);
  assert.equal(result.checked, 3);
});

test("reports missing pages and missing anchors", async (t) => {
  const root = fixture(t);
  fs.writeFileSync(
    path.join(root, "index.html"),
    '<a href="/onboarding/missing/">page</a>' +
      '<a href="/onboarding/docs/#does-not-exist">anchor</a>',
  );
  const result = await checkLinks({ dist: root });
  assert.equal(result.broken.length, 2);
  assert.match(result.broken.join("\\n"), /missing/);
  assert.match(result.broken.join("\\n"), /missing anchor #does-not-exist/);
});

test("rejects internal paths that omit the configured base path", async (t) => {
  const root = fixture(t);
  fs.writeFileSync(path.join(root, "index.html"), '<a href="/docs/">docs</a>');
  const result = await checkLinks({ dist: root });
  assert.equal(result.broken.length, 1);
  assert.match(result.broken[0], /missing \/onboarding\/ base path/);
});
