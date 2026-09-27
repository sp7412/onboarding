# 90-Day Retro

## What I shipped (with measured impact)
## What I learned
## What surprised me
## What I'd do differently
## What I'll own next quarter
## Feedback I received and what I'm doing about it

## Fictional example

- **What I shipped:** A regression evaluator and tool-boundary guard for an invented
  booking flow.
- **Measured impact:** Unsafe bookings fell from 2/40 to 0/40 in the fictional suite;
  this is not a production claim.
- **What I learned:** A clear denominator and reviewed failure cases mattered more than
  a larger prompt.
- **What surprised me:** Most perceived latency came from endpointing and the second
  model turn, not only backend time.
- **What I'd do differently:** Establish the transport metric schema before changing
  prompts.
- **What I'll own next quarter:** Expand the regression slices and document rollback.
- **Feedback and response:** A peer asked for smaller diffs, so I will split future
  changes into independently reviewable behavior and measurement commits.
