# Lab 05 Solution Sketch

The `wrap_tool_call` middleware should reject a `create_job` call when its `slot_id` is
not in `request.state["offered_slot_ids"]`, the caller is not identified, or the service
address lacks a grounded confirmation. The model can still propose the call, but the handler
returns a structured `ToolMessage` and the model receives no authority to override the result.
Keep the same checks in the backend/tool boundary as defense in depth.
