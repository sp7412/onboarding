import { defineConfig } from "astro/config";

// GitHub Pages project site: https://sp7412.github.io/onboarding/
export default defineConfig({
  site: "https://sp7412.github.io",
  base: "/onboarding",
  trailingSlash: "always",
  output: "static",
});
