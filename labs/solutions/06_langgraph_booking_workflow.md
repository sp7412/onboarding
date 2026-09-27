# Lab 06 Solution Sketch

Represent an unclear answer explicitly rather than treating it as yes. Route it to a
second confirmation node with a counter, then route a second unclear answer to
`escalate`. The graph should have no edge from an unclear state to `book`.

The general rule is structural: if a policy must always hold, make the illegal path
unrepresentable in the graph and retain a tool-level check at commit time.
