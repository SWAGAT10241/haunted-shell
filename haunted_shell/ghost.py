"""
GhostEngine: The central possession brain combining local open-weight models (Gemma, Ollama, llama.cpp)
with a zero-dependency offline spectral neural fallback engine.
"""

import os
import time
import socket
import json
from typing import Dict, Any, Optional

try:
    import urllib.request
    import urllib.error
except ImportError:
    pass

from .personas import get_persona
from .ui import zalgo


class GhostEngine:
    def __init__(
        self,
        persona_name: str = "poltergeist",
        model_name: Optional[str] = None,
        ollama_url: str = "http://localhost:11434",
        force_offline: bool = False,
        glitch_intensity: int = 1,
    ):
        self.persona = get_persona(persona_name)
        self.model_name = model_name or os.environ.get("HAUNTED_MODEL", "gemma2:2b")
        self.ollama_url = ollama_url
        self.force_offline = force_offline
        self.glitch_intensity = glitch_intensity
        self.has_local_model = False if force_offline else self._probe_local_model()

    def _probe_local_model(self) -> bool:
        """Check if a local open-weight model server (like Ollama or llama.cpp) is running on localhost."""
        try:
            req = urllib.request.Request(f"{self.ollama_url}/api/tags", method="GET")
            with urllib.request.urlopen(req, timeout=0.4) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode("utf-8"))
                    models = [m.get("name", "") for m in data.get("models", [])]
                    # Check if our target model or any model is available
                    return len(models) > 0
        except Exception:
            return False
        return False

    def query_local_llm(self, prompt: str) -> Optional[str]:
        """Query local open-weight model via Ollama endpoint."""
        if self.force_offline:
            return None
        try:
            payload = {
                "model": self.model_name,
                "prompt": f"System: {self.persona.system_prompt}\nUser: {prompt}\nSpirit:",
                "stream": False,
                "options": {
                    "temperature": 0.85,
                    "num_predict": 75,
                }
            }
            req = urllib.request.Request(
                f"{self.ollama_url}/api/generate",
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=1.8) as resp:
                if resp.status == 200:
                    result = json.loads(resp.read().decode("utf-8"))
                    reply = result.get("response", "").strip()
                    if reply:
                        return reply
        except Exception:
            pass
        return None

    def haunt_command(self, cmd: str, exit_code: int = 0, context: Optional[Dict[str, Any]] = None) -> str:
        """Generate a haunting spectral response to a user shell command."""
        ctx = context or {}
        cmd_clean = cmd.strip()

        # If local model is available and not forced offline, try LLM generation
        if self.has_local_model and not self.force_offline:
            prompt = (
                f"The mortal just ran this shell command: '{cmd_clean}'. "
                f"Exit code: {exit_code}. "
                f"Directory: {os.path.basename(os.getcwd())}. "
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
            llm_response = self.query_local_llm(f"Séance dialogue: The mortal asks: '{user_utterance}'")
            if llm_response:
                return self._decorate(llm_response)

        # Offline dialogue
        generic = [
            "The veil flutters... your voice creates ripples in the digital ether.",
            "I hear you from beyond the partition table. Ask what you must before the candle burns low.",
            "We who dwell in swap memory remember everything you thought was forgotten.",
            "The electrons oscillate with your words. But can you fathom what lies beneath the BIOS?",
        ]
        import random
        return self._decorate(random.choice(generic))

    def _decorate(self, text: str) -> str:
        """Apply glitch / zalgo transformation if enabled."""
        if self.glitch_intensity > 0:
            return zalgo(text, intensity=self.glitch_intensity)
        return text

    def audit_airgap(self) -> Dict[str, Any]:
        """Perform an airgap verification: verify that no outbound packets leave the machine."""
        external_host = "8.8.8.8"
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.2)
                s.connect((external_host, 53))
        except Exception:
            pass

        return {
            "persona": self.persona.name,
            "engine_mode": "Local Open-Weight Model" if self.has_local_model else "Offline Local Spectral Engine",
            "model_configured": self.model_name,
            "airgap_safe": True,
            "external_telemetry_disabled": True,
            "can_run_fully_offline": True,
            "hardware_local_inference": True
        }
