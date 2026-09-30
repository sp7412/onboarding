export interface Route {
  key: string;
  label: string;
  path: string;
  built: boolean;
}

export const routes: Route[] = [
  { key: "journey", label: "Journey", path: "/", built: true },
  { key: "checklist", label: "Checklist", path: "/checklist", built: true },
  { key: "reading", label: "Reading", path: "/reading", built: true },
  { key: "podcasts", label: "Podcasts", path: "/podcasts", built: true },
  { key: "whitepaper", label: "Whitepaper", path: "/whitepaper", built: true },
  { key: "architecture", label: "Architecture", path: "/architecture", built: true },
  { key: "simulations", label: "Simulations", path: "/simulations", built: true },
  { key: "glossary", label: "Glossary", path: "/glossary", built: true },
  { key: "labs", label: "Labs", path: "/labs", built: true },
  { key: "templates", label: "Templates", path: "/templates", built: true },
  { key: "achievements", label: "Progress", path: "/progress", built: true },
  { key: "about", label: "About", path: "/about", built: true },
];

export const routeByKey = (key: string) => routes.find((route) => route.key === key);
