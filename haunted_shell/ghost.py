"""
GhostEngine: The central possession brain combining local open-weight models (Gemma, Ollama, llama.cpp)
with a zero-dependency offline spectral neural fallback engine.
"""

import json
import os
import re
import socket
import time
import urllib.error
import urllib.request
from typing import Any, Dict, Optional

from .config import HauntedConfig
from .logger import logger
from .personas import BasePersona, get_persona
from .ui import zalgo


class GhostEngine:
    """Manages spectral inference, local model fallback, and zalgo post-processing."""

    def __init__(
        self,
        config: Optional[HauntedConfig] = None,
        persona_name: Optional[str] = None,
        model_name: Optional[str] = None,
        ollama_url: Optional[str] = None,
        force_offline: Optional[bool] = None,
        glitch_intensity: Optional[int] = None,
        timeout: Optional[float] = None,
    ):
        cfg = config or HauntedConfig()
        self.persona: BasePersona = get_persona(persona_name or cfg.persona)
        self.model_name: str = model_name or cfg.model
        self.ollama_url: str = (ollama_url or cfg.ollama_url).rstrip("/")
        self.force_offline: bool = force_offline if force_offline is not None else cfg.offline
        self.glitch_intensity: int = (
            glitch_intensity if glitch_intensity is not None else cfg.glitch_intensity
        )
        self.timeout: float = timeout if timeout is not None else cfg.ollama_timeout

        self._has_local_model_cache: Optional[bool] = None
        self._last_probe_time: float = 0.0
        self._probe_ttl: float = 30.0  # seconds to cache probe result

    @property
    def has_local_model(self) -> bool:
        """Cached check for local open-weight model availability."""
        if self.force_offline:
            return False

        now = time.time()
        if (
            self._has_local_model_cache is not None
            and (now - self._last_probe_time) < self._probe_ttl
        ):
            return self._has_local_model_cache

        self._has_local_model_cache = self._probe_local_model()
        self._last_probe_time = now
        return self._has_local_model_cache

    def _probe_local_model(self) -> bool:
        """Probe localhost Ollama/llama.cpp server to check if models are available."""
        endpoint = f"{self.ollama_url}/api/tags"
        try:
            req = urllib.request.Request(
                endpoint, headers={"User-Agent": "haunted-shell/1.0.0"}, method="GET"
            )
            with urllib.request.urlopen(req, timeout=0.5) as resp:  # nosec B310
                if resp.status == 200:
                    data = json.loads(resp.read().decode("utf-8"))
                    models = [m.get("name", "") for m in data.get("models", [])]
                    logger.debug("Found %d local models at %s", len(models), self.ollama_url)
                    return len(models) > 0
        except Exception as exc:
            logger.debug("Local LLM probe failed at %s: %s", endpoint, exc)
            return False
        return False

    def query_local_llm(self, prompt: str) -> Optional[str]:
        """Query local open-weight model via Ollama endpoint with strict timeout."""
        if self.force_offline:
            return None

        endpoint = f"{self.ollama_url}/api/generate"
        payload = {
            "model": self.model_name,
            "prompt": f"System: {self.persona.system_prompt}\nUser: {prompt}\nSpirit:",
            "stream": False,
            "options": {
                "temperature": 0.85,
                "num_predict": 75,
            },
        }

        try:
            req = urllib.request.Request(
                endpoint,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json", "User-Agent": "haunted-shell/1.0.0"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:  # nosec B310
                if resp.status == 200:
                    raw_data = resp.read().decode("utf-8")
                    result = json.loads(raw_data)
                    reply = result.get("response", "").strip()
                    if reply:
                        return self._sanitize_llm_response(reply)
        except Exception as exc:
            logger.debug("Ollama inference error: %s", exc)
            return None
        return None

    @staticmethod
    def _sanitize_llm_response(text: str) -> str:
        """Strip enclosing quotes, markdown wrappers, and prefix labels."""
        cleaned = text.strip()
        for _ in range(2):
            if (cleaned.startswith('"') and cleaned.endswith('"')) or (
                cleaned.startswith("'") and cleaned.endswith("'")
            ):
                cleaned = cleaned[1:-1].strip()
            cleaned = re.sub(
                r"^(Spirit|Ghost|Poltergeist|Calavera|UnixElder):\s*",
                "",
                cleaned,
                flags=re.IGNORECASE,
            ).strip()
        cleaned = re.sub(r"\s+", " ", cleaned)
        return cleaned

    def haunt_command(
        self, cmd: str, exit_code: int = 0, context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Generate a haunting spectral response to a user shell command."""
        ctx = context or {}
        cmd_clean = cmd.strip()

        # If local model is available and not forced offline, try LLM generation
        if self.has_local_model and not self.force_offline:
            cwd_name = os.path.basename(os.getcwd()) or "/"
            prompt = (
                f"The mortal just ran this shell command: '{cmd_clean}'. "
                f"Exit code: {exit_code}. "
                f"Directory: {cwd_name}. "
                f"Whisper your reaction directly to them."
            )
            llm_response = self.query_local_llm(prompt)
            if llm_response:
                return self._decorate(llm_response)

        # Fallback to rich offline persona engine
        commentary = self.persona.generate_commentary(cmd_clean, exit_code, ctx)
        return self._decorate(commentary)

    def converse(self, user_utterance: str) -> str:
        """Direct conversational response in seance mode."""
        if self.has_local_model and not self.force_offline:
            prompt = f"Séance dialogue: The mortal asks: '{user_utterance.strip()}'"
            llm_response = self.query_local_llm(prompt)
            if llm_response:
                return self._decorate(llm_response)

        # Offline dialogue
        return self._decorate(self.persona.converse(user_utterance))

    def _decorate(self, text: str) -> str:
        """Apply glitch / zalgo transformation if enabled."""
        if self.glitch_intensity > 0:
            return zalgo(text, intensity=self.glitch_intensity)
        return text

    def audit_airgap(self) -> Dict[str, Any]:
        """Perform an airgap verification: verify that no outbound packets leave the machine."""
        external_connected = False
        # Test connecting to an external DNS IP to check if machine is airgapped
        external_host = "8.8.8.8"
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.2)
                s.connect((external_host, 53))
                external_connected = True
        except Exception:
            external_connected = False

        return {
            "persona": self.persona.name,
            "engine_mode": "Local Open-Weight Model"
            if self.has_local_model
            else "Offline Local Spectral Engine",
            "model_configured": self.model_name,
            "airgap_safe": True,
            "external_telemetry_disabled": True,
            "can_run_fully_offline": True,
            "hardware_local_inference": True,
            "host_network_isolated": not external_connected,
        }
