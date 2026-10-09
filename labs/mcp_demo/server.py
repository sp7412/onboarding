"""Standalone server used by Lab 16.

Run locally with:
    uv run mcp dev server.py
or:
    uv run mcp run server.py --transport streamable-http
"""

from mcp.server import MCPServer

mcp = MCPServer("ServiceTitan Onboarding Demo")


@mcp.tool()
def find_available_appointment(zip_code: str, trade: str) -> dict:
    """Find fictional appointment availability for a ZIP code and trade."""
    if zip_code == "76108" and trade.lower() == "hvac":
        return {"available": True, "window": "tomorrow 9am-11am", "trade": "hvac"}
    return {"available": False, "window": None, "trade": trade}


@mcp.resource("contractor://capabilities")
def contractor_capabilities() -> str:
    """Describe the fictional contractor's supported trades."""
    return "HVAC and plumbing. Service area: fictional training data only."


@mcp.prompt()
def booking_assistant(trade: str = "HVAC") -> str:
    """Create a prompt for checking availability before booking."""
    return f"Check availability for {trade}; do not book anything without explicit confirmation."


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
