"""
Personas registry for the haunted-shell possession engine.
"""

from typing import Dict, List, Optional

from .base import BasePersona
from .calavera import CalaveraPersona
from .poltergeist import PoltergeistPersona
from .unix_elder import UnixElderPersona

_PERSONA_REGISTRY: Dict[str, BasePersona] = {
    "poltergeist": PoltergeistPersona(),
    "calavera": CalaveraPersona(),
    "unix-elder": UnixElderPersona(),
}


def register_persona(persona: BasePersona) -> None:
    """Register a new custom persona into the runtime registry."""
    _PERSONA_REGISTRY[persona.name.lower()] = persona


def get_persona(name: Optional[str]) -> BasePersona:
    """Retrieve a persona by name; falls back safely to poltergeist if unrecognized."""
    if not name:
        return _PERSONA_REGISTRY["poltergeist"]
    return _PERSONA_REGISTRY.get(name.lower(), _PERSONA_REGISTRY["poltergeist"])


def list_personas() -> Dict[str, BasePersona]:
    """Return dictionary of all registered personas."""
    return dict(_PERSONA_REGISTRY)


def available_persona_names() -> List[str]:
    """Return sorted list of persona identifiers."""
    return sorted(_PERSONA_REGISTRY.keys())
