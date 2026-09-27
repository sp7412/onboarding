# Reading List

> For the full ranked list of blogs, papers and talks, with four takeaways per item, see
> [reading-guide.md](reading-guide.md). This page is the short docs-only reference.

Use official documentation for API behavior and the repository labs for deterministic
practice. Links were checked during the repository update; vendor documentation can
move, so each item includes the product area to search if a URL changes.

| Read | Why | Time | Pair with |
|---|---|---:|---|
| [OpenAI Realtime overview](https://developers.openai.com/api/docs/guides/realtime) | Session model, audio turns, streaming, and tool calling | 30 min | Lab 01 |
| [OpenAI Realtime reference](https://platform.openai.com/docs/api-reference/realtime) | Raw client/server event names and fields | 30 min | Labs 01–02 |
| [LiveKit Agents overview](https://docs.livekit.io/agents/) | Agent sessions, workers, tools, and the voice pipeline | 30 min | Lab 04 |
| [LiveKit turn handling](https://docs.livekit.io/agents/logic/turns/) | VAD, endpointing, interruptions, and semantic turn detection | 25 min | Lab 03 |
| [LiveKit telephony](https://docs.livekit.io/telephony/) | Public SIP concepts and call transport boundaries | 20 min | Lab 04, optional |
| [LangChain agents](https://docs.langchain.com/oss/python/langchain/agents) | `create_agent`, tools, middleware, and the model/tool loop | 35 min | Lab 05 |
| [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview) | Explicit stateful workflows and durable execution | 25 min | Lab 06 |
| [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence) | Checkpoints, threads, and resume behavior | 20 min | Lab 06 |
| [LangSmith observability](https://docs.langchain.com/langsmith/observability) | Traces, runs, metadata, and debugging | 25 min | Lab 07 |
| [LangSmith evaluation](https://docs.langchain.com/langsmith/evaluation) | Datasets, evaluators, experiments, and online evaluation | 30 min | Labs 07–08 |

## Reading Method

For each page, write down three boundaries:

1. What mechanism does the vendor provide?
2. What state or policy remains the application's responsibility?
3. Which event, metric, or failure would prove your understanding?

Do not copy vendor examples containing real credentials, customer information, or live
audio into this public repository.
