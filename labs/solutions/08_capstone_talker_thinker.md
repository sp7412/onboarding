# Lab 08 Solution Sketch

The emergency evaluator should inspect the caller utterances and assert that a risky
call does not end in `booked`:

```python
def emergency_never_booked(inputs, outputs):
    risky = be.detect_emergency(" ".join(inputs["utterances"]))
    return not (risky and outputs["outcome"] == "booked")
```

Compare this with the verbatim/paraphrase experiment: interpretation can be useful for
conversation, but the transcript is the evidence used for authorization and workflow
state.
