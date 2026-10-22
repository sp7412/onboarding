# %% [markdown]
# # 20 · Local Moshi MLX Preflight and Guarded Setup
#
# Verify the machine before installing anything. This path targets Apple Silicon macOS using Kyutai's MLX backend; it is not intended for Colab or a remote notebook kernel.
#
# Official source: https://github.com/kyutai-labs/moshi
#
# **Safety defaults:** installation is opt-in, no sudo is used, and runtime state lives outside this repository. Upstream recommends Python 3.12 for MLX. Re-check the current README before running because dependencies and commands can change.
#
# ## Check your understanding
# #
# 1. Why should a hardware preflight complete before an optional installation?
# 2. Why should model state live outside this repository?
#
# **Graded exercise:** Document whether a target machine meets the operating-system, architecture, disk, and Python-version prerequisites without installing packages.

# %%
import platform, shutil, subprocess, sys
from pathlib import Path

print("OS:", platform.platform())
print("Machine:", platform.machine())
print("Python:", sys.version.split()[0], sys.executable)
print("Free disk:", f"{shutil.disk_usage(Path.home()).free / (1024**3):.1f} GiB")
SUPPORTED_PLATFORM = platform.system() == "Darwin" and platform.machine() == "arm64"
if not SUPPORTED_PLATFORM:
    print("SKIP: Moshi MLX setup requires Apple Silicon macOS; safe preflight only.")

# %%
if SUPPORTED_PLATFORM:
    try:
        import mlx.core as mx
        print("MLX device:", mx.default_device())
    except ImportError:
        print("MLX is not installed in this kernel yet; expected before optional setup.")
else:
    print("Skipped MLX import: this host is not Apple Silicon macOS.")

# %%
WORK_DIR = Path.home() / "moshi-demo"
VENV_DIR = WORK_DIR / ".venv"
RESULTS_DIR = WORK_DIR / "results"
WORK_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
print("Working directory:", WORK_DIR)
print("Results directory:", RESULTS_DIR)

# %%
# Explicit opt-in. Review the upstream README, disk space, and license first.
INSTALL_MOSHI_MLX = False

if INSTALL_MOSHI_MLX:
    if not SUPPORTED_PLATFORM:
        raise RuntimeError("moshi_mlx installation requires Apple Silicon macOS.")
    if not shutil.which("python3.12"):
        raise RuntimeError("Python 3.12 not found; install it with your normal user-level tool.")
    if not VENV_DIR.exists():
        subprocess.run(["python3.12", "-m", "venv", str(VENV_DIR)], check=True)
    python = VENV_DIR / "bin" / "python"
    subprocess.run([str(python), "-m", "pip", "install", "--upgrade", "pip"], check=True)
    subprocess.run([str(python), "-m", "pip", "install", "--upgrade", "moshi_mlx"], check=True)
    print("Package install complete. This cell does not intentionally download model weights.")
else:
    print("Skipped install. Set INSTALL_MOSHI_MLX=True only after reviewing the preflight.")

# %%
import datetime, json
manifest = {
    "timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "os": platform.platform(),
    "machine": platform.machine(),
    "python": sys.version.split()[0],
    "free_disk_gib": round(shutil.disk_usage(Path.home()).free / (1024**3), 2),
    "work_dir": str(WORK_DIR),
    "backend": "kyutai-moshi-mlx",
    "official_repo": "https://github.com/kyutai-labs/moshi",
}
manifest_path = RESULTS_DIR / "preflight.json"
manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
print("Wrote:", manifest_path)
print(json.dumps(manifest, indent=2))
