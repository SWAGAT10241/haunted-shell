"""
Configuration management for haunted-shell.
Supports config file (XDG compliant), environment variables, and CLI overrides.
"""

import json
import os
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

CONFIG_DIR_NAME = "haunted-shell"
CONFIG_FILE_NAME = "config.json"


@dataclass
class HauntedConfig:
    """Application configuration for haunted-shell."""

    persona: str = "poltergeist"
    model: str = "gemma2:2b"
    offline: bool = False
    ollama_url: str = "http://localhost:11434"
    glitch_intensity: int = 1
    typewriter_speed: float = 0.015
    no_color: bool = False
    debug: bool = False
    ollama_timeout: float = 1.5
    history_file: str = field(default_factory=lambda: str(Path.home() / ".haunted_history"))
    modifiers: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return asdict(self)


def get_default_config_path() -> Path:
    """Return standard XDG configuration path."""
    custom_path = os.environ.get("HAUNTED_CONFIG_PATH")
    if custom_path:
        return Path(custom_path).expanduser().resolve()

    xdg_config_home = os.environ.get("XDG_CONFIG_HOME")
    if xdg_config_home:
        base = Path(xdg_config_home).expanduser()
    else:
        base = Path.home() / ".config"

    return base / CONFIG_DIR_NAME / CONFIG_FILE_NAME


def load_config(config_path: Optional[Path] = None, **cli_overrides: Any) -> HauntedConfig:
    """
    Load configuration with precedence:
    CLI overrides > Environment variables > Config file > Defaults
    """
    cfg = HauntedConfig()
    path = config_path or get_default_config_path()

    # 1. Load from file if present
    if path.is_file():
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    for k, v in data.items():
                        if hasattr(cfg, k) and v is not None:
                            setattr(cfg, k, v)
        except (json.JSONDecodeError, OSError):
            pass

    # 2. Environment variable overrides
    if "HAUNTED_PERSONA" in os.environ:
        cfg.persona = os.environ["HAUNTED_PERSONA"].lower()
    if "HAUNTED_MODEL" in os.environ:
        cfg.model = os.environ["HAUNTED_MODEL"]
    if "HAUNTED_OFFLINE" in os.environ:
        cfg.offline = os.environ["HAUNTED_OFFLINE"].lower() in {"1", "true", "yes"}
    if "HAUNTED_OLLAMA_URL" in os.environ:
        cfg.ollama_url = os.environ["HAUNTED_OLLAMA_URL"]
    if "HAUNTED_GLITCH" in os.environ:
        try:
            cfg.glitch_intensity = int(os.environ["HAUNTED_GLITCH"])
        except ValueError:
            pass
    if "HAUNTED_NO_COLOR" in os.environ or "NO_COLOR" in os.environ:
        cfg.no_color = True
    if "HAUNTED_DEBUG" in os.environ:
        cfg.debug = os.environ["HAUNTED_DEBUG"].lower() in {"1", "true", "yes"}

    # 3. CLI explicit overrides (only apply non-None values)
    for k, v in cli_overrides.items():
        if hasattr(cfg, k) and v is not None:
            setattr(cfg, k, v)

    # Sanitize bounds
    cfg.glitch_intensity = max(0, min(3, cfg.glitch_intensity))
    cfg.persona = cfg.persona.lower()

    return cfg


def save_config(config: HauntedConfig, path: Optional[Path] = None) -> Path:
    """Save configuration to JSON file."""
    target_path = path or get_default_config_path()
    target_path.parent.mkdir(parents=True, exist_ok=True)
    with open(target_path, "w", encoding="utf-8") as f:
        json.dump(config.to_dict(), f, indent=2)
    return target_path
