import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const DEFAULT_BASE = "/onboarding/";

function collectHtmlFiles(root) {
  const files = [];
  const walk = (dir) => {
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      const full = path.join(dir, entry.name);
      if (entry.isDirectory()) walk(full);
      else if (entry.name.endsWith(".html")) files.push(full);
    }
  };
  walk(root);
  return files;
}

function resolveTarget(value, from, dist, base) {
  const [pathname, hash] = value.split("#", 2);
  const clean = pathname.split("?", 1)[0];
  let file;
  if (clean === base || clean === base.slice(0, -1) || clean === "") {
    file = path.join(dist, "index.html");
  } else if (clean.startsWith(base)) {
    const relative = clean.slice(base.length);
    file = relative.endsWith("/")
      ? path.join(dist, relative, "index.html")
      : path.join(dist, relative);
    if (fs.existsSync(file) && fs.statSync(file).isDirectory()) {
      file = path.join(file, "index.html");
    }
    if (!fs.existsSync(file) && fs.existsSync(`${file}.html`)) {
      file = `${file}.html`;
    }
    if (!fs.existsSync(file) && fs.existsSync(path.join(file, "index.html"))) {
      file = path.join(file, "index.html");
    }
  } else {
    return null;
  }
  return hash ? { file, hash } : { file };
}

export async function checkLinks({
  dist = path.resolve("dist"),
  base = DEFAULT_BASE,
  checkExternal = false,
} = {}) {
  const htmlFiles = collectHtmlFiles(dist);
  const idsByFile = new Map();
  for (const file of htmlFiles) {
    const html = fs.readFileSync(file, "utf8");
    idsByFile.set(
      file,
      new Set([...html.matchAll(/\bid=["']([^"']+)["']/g)].map((m) => m[1])),
    );
  }

  let checked = 0;
  const broken = [];
  for (const file of htmlFiles) {
    const html = fs.readFileSync(file, "utf8");
    for (const match of html.matchAll(/\b(?:href|src)=["']([^"']+)["']/g)) {
      const value = match[1];
      if (/^(?:[a-z][a-z\d+.-]*:|\/\/|data:|mailto:|javascript:)/i.test(value)) {
        if (checkExternal && /^https?:\/\//i.test(value)) {
          try {
            const response = await fetch(value, { method: "HEAD" });
            if (!response.ok) broken.push(`${file}: ${value} (${response.status})`);
          } catch (error) {
            broken.push(`${file}: ${value} (${error.message})`);
          }
        }
        continue;
      }
      checked += 1;
      const target = value.startsWith("#")
        ? { file, hash: value.slice(1) }
        : resolveTarget(value, file, dist, base);
      if (!target) {
        broken.push(`${file}: ${value} (missing ${base} base path)`);
      } else if (!fs.existsSync(target.file)) {
        broken.push(`${file}: ${value} (missing ${target.file})`);
      } else if (
        target.hash &&
        (!idsByFile.has(target.file) || !idsByFile.get(target.file).has(target.hash))
      ) {
        broken.push(`${file}: ${value} (missing anchor #${target.hash})`);
      }
    }
  }
  return { pages: htmlFiles.length, checked, broken };
}

const isCli = process.argv[1] &&
  path.resolve(process.argv[1]) === fileURLToPath(import.meta.url);
if (isCli) {
  const result = await checkLinks({ checkExternal: process.argv.includes("--external") });
  console.log(
    `Scanned ${result.pages} HTML pages; checked ${result.checked} internal links; broken = ${result.broken.length}.`,
  );
  if (result.broken.length) {
    for (const item of result.broken) console.error(item);
    process.exitCode = 1;
  }
}
