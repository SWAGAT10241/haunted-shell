"""
Base abstraction for haunted-shell personas.
Defines the required interface and common fallback capabilities.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class BasePersona(ABC):
    """Abstract base class for all terminal specter personas."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Machine identifier (e.g. 'poltergeist', 'calavera', 'unix-elder')."""
        pass

    @property
    @abstractmethod
    def title(self) -> str:
        """Display title of the spirit."""
        pass

    @property
    @abstractmethod
    def color_name(self) -> str:
        """Primary color theme identifier."""
        pass

    @property
    @abstractmethod
    def prompt_symbol(self) -> str:
        """Terminal prompt glyph for this spirit (e.g. 👻, 💀, #)."""
        pass

    @property
    @abstractmethod
    def system_prompt(self) -> str:
        """System prompt instructions for local LLMs."""
        pass

    @abstractmethod
    def generate_commentary(
        self,
        cmd: str,
        exit_code: int = 0,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Generate offline commentary on a command."""
        pass

    @abstractmethod
    def converse(self, utterance: str) -> str:
        """Generate offline conversational response during a seance."""
        pass

    def get_farewell(self) -> str:
        """Spooky farewell message when the user exits the session."""
        return "The veil closes. Farewell, mortal..."
