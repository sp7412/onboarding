# Lab 03 Solution Sketch

For the included phone-number timeline, sweep the fixed delays and inspect
`score_turns`. The shortest acceptable delay is the first row with
`premature_cutoffs == 0`; the cost is the response gap after a genuinely complete
utterance. A semantic detector can reduce that tradeoff but adds its own errors and
latency.
