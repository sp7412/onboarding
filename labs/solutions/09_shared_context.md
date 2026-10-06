# Lab 09 Solution Sketch

Give availability facts a time-to-live when they're proposed, and let reads ignore expired
facts. `ContextLedger.get()` already skips a fact whose `expires_at` has passed.

```python
ledger = ContextLedger()
ledger.propose("voice_agent", "J-1", "callback_window", "today_only", 0.9,
               evidence="I can only do today", ttl=3)
ledger.verify("J-1", "callback_window", evidence="caller said it directly")
assert ledger.view("J-1")["callback_window"] == "today_only"

ledger.tick(5)                     # time passes; the window is no longer valid
assert "callback_window" not in ledger.view("J-1")
```

Verification copies `expires_at` from the proposed fact, so promoting a fact never extends
its life. Choose TTLs per key: availability expires within hours; a job type doesn't expire.
