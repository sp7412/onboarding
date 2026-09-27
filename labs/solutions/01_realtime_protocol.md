# Lab 01 Solution Sketch

After cancellation, truncate the assistant item using the audio duration actually sent
to the speaker, not the number of deltas received. A self-check can be as small as:

```python
words_heard = max(0, played_ms // MS_PER_WORD_AUDIO)
assert len(item["content"][0]["transcript"].split()) <= words_heard
```

The important invariant is that conversation history matches what the caller could
actually have heard.
