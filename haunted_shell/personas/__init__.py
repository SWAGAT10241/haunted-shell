"""
Personas for the haunted-shell possession engine.
"""

from .poltergeist import PoltergeistPersona
from .calavera import CalaveraPersona
from .unix_elder import UnixElderPersona

PERSONAS = {
    "poltergeist": PoltergeistPersona(),
    "calavera": CalaveraPersona(),
    "unix-elder": UnixElderPersona(),
}

def get_persona(name: str):
    return PERSONAS.get(name, PERSONAS["poltergeist"])
