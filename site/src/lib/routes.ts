export interface Route {
  key: string;
  label: string;
  path: string;
  built: boolean;
}

export const routes: Route[] = [
  { key: "journey", label: "Journey", path: "/", built: true },
  { key: "checklist", label: "Checklist", path: "/checklist", built: false },
  { key: "reading", label: "Reading", path: "/reading", built: false },
  { key: "podcasts", label: "Podcasts", path: "/podcasts", built: false },
  { key: "whitepaper", label: "Whitepaper", path: "/whitepaper", built: false },
  { key: "architecture", label: "Architecture", path: "/architecture", built: false },
  { key: "simulations", label: "Simulations", path: "/simulations/turn-taking", built: false },
  { key: "glossary", label: "Glossary", path: "/glossary", built: false },
  { key: "labs", label: "Labs", path: "/labs", built: false },
  { key: "templates", label: "Templates", path: "/templates", built: false },
  { key: "achievements", label: "Achievements", path: "/achievements", built: false },
  { key: "about", label: "About", path: "/about", built: true },
];

export const routeByKey = (key: string) => routes.find((route) => route.key === key);
