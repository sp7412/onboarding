# %% [markdown]
# # Lab 21 — Start and verify the local Moshi browser demo
#
# This notebook starts the official local MLX web UI on Apple Silicon macOS. It cannot grant microphone permissions or automate a real conversation; those checks must happen in your browser.
#
# Upstream documents the command python -m moshi_mlx.local_web and the local UI at http://localhost:8998: https://github.com/kyutai-labs/moshi
#
# **Important:** enabling the server can trigger model-weight downloads. Confirm disk space, the current model/weight license, and upstream behavior first. Keep the server on localhost; do not create a public tunnel. The notebook defaults to not starting the server.

# %%
import os, platform, shutil, subprocess, time
from pathlib import Path

WORK_DIR = Path.home() / "moshi-demo"
VENV_PYTHON = WORK_DIR / ".venv" / "bin" / "python"
RESULTS_DIR = WORK_DIR / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
SUPPORTED_PLATFORM = platform.system() == "Darwin" and platform.machine() == "arm64"
print("Free disk:", f"{shutil.disk_usage(Path.home()).free / (1024**3):.1f} GiB")
print("Official command: python -m moshi_mlx.local_web")
if not SUPPORTED_PLATFORM:
    print("SKIP: live Moshi MLX server requires Apple Silicon macOS.")
elif not VENV_PYTHON.exists():
    print(f"Environment missing at {VENV_PYTHON}; complete Lab 18 before starting the server.")

# %%
# This may download weights. Re-check upstream documentation and disk first.
START_SERVER = False
SERVER_LOG = RESULTS_DIR / "moshi-server.log"
server = None

if START_SERVER:
    if not SUPPORTED_PLATFORM:
        raise RuntimeError("Starting the Moshi MLX server requires Apple Silicon macOS.")
    if not VENV_PYTHON.exists():
        raise RuntimeError(f"Environment missing at {VENV_PYTHON}; complete Lab 18 first.")
    log_file = SERVER_LOG.open("w")
    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"
    server = subprocess.Popen(
        [str(VENV_PYTHON), "-m", "moshi_mlx.local_web"],
        cwd=WORK_DIR, env=env, stdout=log_file,
        stderr=subprocess.STDOUT, start_new_session=True,
    )
    time.sleep(5)
    print("Server PID:", server.pid, "log:", SERVER_LOG)
    if server.poll() is not None:
        print(SERVER_LOG.read_text(errors="replace")[-6000:])
    else:
        print("Open http://localhost:8998 in a browser on this Mac.")
else:
    print("Not started. Set START_SERVER=True after reviewing upstream requirements.")

# %%
import urllib.request
from urllib.error import URLError

try:
    with urllib.request.urlopen("http://localhost:8998", timeout=2) as response:
        print("HTTP status:", response.status)
        print("Content type:", response.headers.get("Content-Type"))
except (URLError, TimeoutError, OSError) as exc:
    print("Local UI not reachable (expected if server is stopped):", repr(exc))

# %%
# Mark an item true only after observing it in the browser.
checks = {
    "page loads at localhost:8998": False,
    "microphone permission granted": False,
    "basic prompt produces audible, intelligible speech": False,
    "user can speak while assistant is speaking": False,
    "barge-in stops or changes assistant speech": False,
    "natural pause does not cause pathological turn splitting": False,
    "no public tunnel/listener enabled": True,
}
print("\n".join(f"[{'x' if done else ' '}] {name}" for name, done in checks.items()))
print("Record observations in the evaluation notebook; do not claim a pass until tested.")

# %%
STOP_SERVER = False
if STOP_SERVER and server is not None and server.poll() is None:
    server.terminate()
    try:
        server.wait(timeout=10)
    except subprocess.TimeoutExpired:
        server.kill()
        server.wait(timeout=5)
    print("Server stopped.")
else:
    print("Server left unchanged. Set STOP_SERVER=True to stop this notebook's process.")

