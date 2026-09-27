"""stlab: shared helpers for the ServiceTitan voice-agent tutorial notebooks.

Everything here is a teaching fixture: a mock home-services backend, an offline
Realtime API simulator, a scripted LangChain chat model, and a turn-taking
simulator. Nothing here talks to real ServiceTitan systems.
"""
from .env import load_env, have, status  # noqa: F401
