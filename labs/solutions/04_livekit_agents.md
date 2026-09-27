# Lab 04 Solution Sketch

Three invariants that should remain outside the transport are:

1. A booking requires a verified customer and offered slot.
2. A booking requires grounded address confirmation.
3. Emergency language restricts routine tools and routes to the approved transfer.

`userdata` is useful per-call state, but durable recovery and audit records belong in an
application-owned store.
