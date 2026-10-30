"""
Doctor: System diagnostics and environment inspection tool for haunted-shell.
Verifies system health, local AI reachability, terminal capabilities, and configuration.
"""

import json
import platform
import shutil
import sys
import urllib.error
import urllib.request
from typing import Any, Dict

from .config import HauntedConfig, get_default_config_path
from .ui import (
    BLOOD_RED,
    BOLD,
    DIM,
    MARIGOLD_AMBER,
    RESET,
    SLIME_GREEN,
    SPECTRAL_CYAN,
    spectral_box,
    supports_color,
)


def run_doctor(config: HauntedConfig) -> Dict[str, Any]:
    """Perform diagnostic health check and print formatted report."""
    results: Dict[str, Any] = {}

    # 1. System environment
    py_ver = platform.python_version()
    os_desc = f"{platform.system()} {platform.release()} ({platform.machine()})"
    is_tty = sys.stdout.isatty()
    term_cols, term_rows = shutil.get_terminal_size(fallback=(80, 24))
    has_color = supports_color()

    # 2. Config check
    cfg_path = get_default_config_path()
    cfg_exists = cfg_path.is_file()

    # 3. Ollama / Local Model probe
    ollama_ok = False
    ollama_models = []
    ollama_error = ""

    if not config.offline:
        try:
            req = urllib.request.Request(
                f"{config.ollama_url.rstrip('/')}/api/tags",
                headers={"User-Agent": "haunted-shell/1.0.0"}
            )
            with urllib.request.urlopen(req, timeout=0.8) as resp:
                if resp.status == 200:
                    data = json.loads(resp.read().decode("utf-8"))
                    ollama_models = [m.get("name", "") for m in data.get("models", [])]
                    ollama_ok = True
        except Exception as exc:
            ollama_error = str(exc)

    results["python_version"] = py_ver
    results["os"] = os_desc
    results["tty"] = is_tty
    results["color_supported"] = has_color
    results["config_path"] = str(cfg_path)
    results["config_exists"] = cfg_exists
    results["ollama_reachable"] = ollama_ok
    results["ollama_models"] = ollama_models

    # Render report
    lines = [
        f"Platform: {BOLD}{os_desc}{RESET}",
        f"Python:   {BOLD}{py_ver}{RESET} ({'✓ Supported' if sys.version_info >= (3, 9) else '✗ Unsupported'})",
        f"Terminal: {'Interactive TTY' if is_tty else 'Piped/Non-TTY'} | Colors: {'✓ Enabled' if has_color else '✗ Disabled'} | Size: {term_cols}x{term_rows}",
        "",
        f"Active Persona:  {BOLD}{config.persona}{RESET}",
        f"Configured Model: {BOLD}{config.model}{RESET}",
        f"Config File:      {cfg_path} ({'Found' if cfg_exists else 'Using Defaults'})",
        "",
        f"Local AI Server ({config.ollama_url}):"
    ]

    if config.offline:
        lines.append(f"  {MARIGOLD_AMBER}• Forced Offline Mode Active (Zero Local/Remote AI Calls){RESET}")
    elif ollama_ok:
        lines.append(f"  {SLIME_GREEN}✓ Ollama reachable ({len(ollama_models)} model(s) available){RESET}")
        if ollama_models:
            models_sample = ", ".join(ollama_models[:3])
            lines.append(f"    Available: {DIM}{models_sample}{RESET}")
    else:
        lines.append(f"  {BLOOD_RED}✗ Not responding: {ollama_error or 'Connection refused'}{RESET}")
        lines.append(f"    {DIM}haunted-shell gracefully defaults to 100% offline rule-based neural persona.{RESET}")

    spectral_box("HAUNTED-SHELL SYSTEM DIAGNOSTICS", lines, color=SPECTRAL_CYAN)
    return results
