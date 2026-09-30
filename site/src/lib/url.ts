const BASE = import.meta.env.BASE_URL;

/** Join an internal path to Astro's configured base without changing suffixes. */
export function url(path: string): string {
  if (/^(?:[a-z][a-z\d+.-]*:|\/\/)/i.test(path) || path.startsWith("#")) return path;
  const [pathname, suffix = ""] = path.split(/([?#].*)/, 2);
  const base = BASE.endsWith("/") ? BASE.slice(0, -1) : BASE;
  const cleanPath = pathname.replace(/^\/+/, "");
  return `${base}/${cleanPath}${suffix}`;
}
