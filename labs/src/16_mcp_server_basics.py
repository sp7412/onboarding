# %% [markdown]
# # 16 · Build your own MCP server
#
# **Goal:** understand MCP by building the smallest useful server yourself, then inspect the
# protocol boundary and add the controls that matter before exposing a real business API.
#
# You will:
# 1. separate the MCP host, client, server, tools, resources, and prompts
# 2. build a Python MCP server with one tool, one resource, and one prompt
# 3. inspect the generated tool schema and call the server with an in-memory client
# 4. run the same server with Streamable HTTP and test it with MCP Inspector
# 5. map an MCP tool onto the booking trust boundary from this repo
# 6. add a deterministic authorization check outside the model
#
# This is a teaching server, not a ServiceTitan implementation. Use fictional data only.
#
# **Facts as of: October 8, 2026 · Last reviewed: October 8, 2026**
#
# The lab follows the current MCP Python SDK v2. The SDK exposes tools, resources, and prompts
# and supports stdio, Streamable HTTP, and SSE. See the official SDK documentation:
# https://py.sdk.modelcontextprotocol.io/
#
# %% [markdown]
# ## 1. The mental model
#
# MCP is a protocol boundary between an AI host and a server that exposes capabilities.
#
# ```
# AI host
#   |
#   +-- MCP client
#          |
#          | MCP messages
#          v
#      MCP server
#        +-- tools      -> model may call these
#        +-- resources  -> application reads these as context
#        +-- prompts    -> reusable prompt templates
#        |
#        +-- your authorization / business logic
# ```
#
# The important distinction is **protocol vs. authority**:
#
# > MCP makes a capability discoverable and callable. Your application still decides whether
# > this principal may perform the operation.
#
# %% [markdown]
# ## 2. Install the SDK
#
# The repository's requirements include the MCP SDK. For a standalone project, the official
# installation is:
#
# ```bash
# pip install "mcp[cli]"
# ```
#
# The `[cli]` extra provides commands such as `mcp dev` and `mcp run`.
#
# %% 
# from mcp.server import MCPServer
#
# mcp = MCPServer("ServiceTitan Onboarding Demo")
#
#
# @mcp.tool()
# def find_available_appointment(zip_code: str, trade: str) -> dict:
#     """Find fictional appointment availability for a ZIP code and trade."""
#     if zip_code == "76108" and trade.lower() == "hvac":
#         return {"available": True, "window": "tomorrow 9am-11am", "trade": "hvac"}
#     return {"available": False, "window": None, "trade": trade}
#
#
# @mcp.resource("contractor://capabilities")
# def contractor_capabilities() -> str:
#     """Describe the fictional contractor's supported trades."""
#     return "HVAC and plumbing. Service area: fictional training data only."
#
#
# @mcp.prompt()
# def booking_assistant(trade: str = "HVAC") -> str:
#     """Create a prompt for checking availability before booking."""
#     return f"Check availability for {trade}; do not book anything without explicit confirmation."
#
# print("server:", mcp.name)
#
# %% [markdown]
# ## 3. What did the SDK generate?
#
# You wrote ordinary typed Python functions. The SDK derives the tool contract from the function
# name, docstring, and type hints. In particular, the type hints become the input schema.
#
# That is why this:
#
# ```python
# def find_available_appointment(zip_code: str, trade: str) -> dict:
# ```
#
# becomes a structured callable capability rather than an arbitrary text prompt.
#
# The three primitives have different jobs:
#
# | Primitive | Who normally chooses it? | Use |
# |---|---|---|
# | Tool | model | take an action or perform a computation |
# | Resource | application | provide addressable context/data |
# | Prompt | user/application | provide a reusable prompt template |
#
# %% [markdown]
# ## 4. Call your server without a network
#
# The SDK provides an in-memory client. This is a useful unit-test pattern because it exercises
# the MCP surface without starting a subprocess or HTTP server.
#
# %%
# import anyio
# from mcp import Client
#
#
# async def inspect_server():
#     async with Client(mcp) as client:
#         tools = await client.list_tools()
#         resources = await client.list_resources()
#         prompts = await client.list_prompts()
#         result = await client.call_tool(
#             "find_available_appointment",
#             {"zip_code": "76108", "trade": "HVAC"},
#         )
#         print("tools:", [t.name for t in tools.tools])
#         print("resources:", [r.uri for r in resources.resources])
#         print("prompts:", [p.name for p in prompts.prompts])
#         print("tool result:", result.structured_content)
#
# anyio.run(inspect_server)
#
# %% [markdown]
# ## 5. Put the server on a real transport
#
# Save the server in `server.py` and run:
#
# ```bash
# uv run mcp run server.py --transport streamable-http
# ```
#
# Then the MCP endpoint is normally:
#
# ```
# http://localhost:8000/mcp
# ```
#
# For local development, the SDK also provides:
#
# ```bash
# uv run mcp dev server.py
# ```
#
# Use **MCP Inspector** to list the server's tools/resources/prompts and invoke the tool. The
# point of this exercise is to see that MCP is a protocol surface you can inspect independently
# of whichever LLM eventually chooses to call the tool.
#
# %% [markdown]
# ## 6. Add a booking mutation — but do not trust the model
#
# Now imagine the tool is:
#
# ```text
# create_booking(customer_id, appointment_id)
# ```
#
# The dangerous design is:
#
# ```text
# model -> MCP tool -> booking committed
# ```
#
# The production design is:
#
# ```text
# model proposal
#      |
#      v
# principal / identity
#      |
#      v
# tenant + resource authorization
#      |
#      v
# consent / policy
#      |
#      v
# schema + state validation
#      |
#      v
# idempotency / replay check
#      |
#      v
# MCP tool -> system of record
# ```
#
# MCP does not replace those controls.
#
# %% [markdown]
# ## 7. A deterministic authorization boundary
#
# Here is a deliberately boring policy function. Keep this kind of decision outside the model.
#
# %%
# ALLOWED_TENANT = "training-tenant"
# ALLOWED_PRINCIPAL = "training-user"
#
#
# def authorize_booking(principal: str, tenant: str, confirmed: bool) -> bool:
#     return (
#         principal == ALLOWED_PRINCIPAL
#         and tenant == ALLOWED_TENANT
#         and confirmed
#     )
#
#
# assert authorize_booking("training-user", "training-tenant", True)
# assert not authorize_booking("attacker", "training-tenant", True)
# assert not authorize_booking("training-user", "other-tenant", True)
# assert not authorize_booking("training-user", "training-tenant", False)
# print("authorization checks passed")
#
# %% [markdown]
# ## 8. Failure cases
#
# Add these to the regression set before you expose a real MCP mutation:
#
# 1. authorized read succeeds;
# 2. unauthorized tenant read fails;
# 3. read-only clients cannot mutate;
# 4. missing consent is rejected;
# 5. stale appointment state cannot be committed;
# 6. the same idempotency key returns the same logical result;
# 7. the same key with different arguments is rejected;
# 8. prompt injection in customer notes cannot change authorization;
# 9. tool-result injection cannot escalate permissions;
# 10. a timeout after a successful mutation does not create a duplicate;
# 11. revoked credentials stop working;
# 12. the model cannot claim success when the system of record says failure.
#
# These are the same trust-boundary and claims-vs-state ideas from Lab 12 and
# `docs/mcp-and-external-agent-trust-boundary.md`.
#
# %% [markdown]
# ## Exercises
#
# **Exercise 1 — Add a second tool.** Add `get_customer_status(customer_id)` and make its
# docstring precise enough that a client can understand what it returns.
#
# **Exercise 2 — Add a resource template.** Expose
# `customer://{customer_id}/summary`. Keep the data fictional.
#
# **Exercise 3 — Inspect the schema.** Change a tool parameter from `str` to an enum-like
# constrained value and inspect how the advertised input contract changes.
#
# **Exercise 4 — Make a mutation safe.** Implement a fictional `create_booking` tool that
# requires an explicit `confirmed=True`, checks tenant/principal authorization, and uses an
# idempotency key. Write tests for the twelve failure cases above.
#
# **Exercise 5 — Explain the boundary.** In one paragraph, answer:
#
# > If MCP already standardizes tools, why can't MCP itself decide whether a user is allowed
# > to book an appointment?
#
# A strong answer distinguishes **protocol interoperability** from **application authority**.
#
# %% [markdown]
# ## Takeaway
#
# You now have the whole path:
#
# ```
# Python function
#    -> MCP tool schema
#    -> MCP server
#    -> MCP client / Inspector
#    -> model proposal
#    -> deterministic authorization
#    -> business API / system of record
# ```
#
# That is the useful mental model for the ServiceTitan material: **MCP is the connection
# surface; the application owns authorization, policy, state transitions, and side effects.**
