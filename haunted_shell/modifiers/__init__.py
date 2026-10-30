"""
Modifiers package for haunted-shell.
Includes text visual effects, tone modifiers, and custom user-defined command rules.
"""

from typing import List, Optional
from .text_modifiers import TEXT_MODIFIERS
from .tone_modifiers import TONE_MODIFIERS, ToneModifier
from .custom_rules import CustomRuleEngine

ALL_MODIFIERS = list(TEXT_MODIFIERS.keys()) + list(TONE_MODIFIERS.keys()) + ["custom-rules"]


def apply_all_modifiers(
    text: str,
    active_modifiers: Optional[List[str]] = None,
    glitch_intensity: int = 1
) -> str:
    """Applies tone and text modifiers sequentially to spectral text."""
    if not active_modifiers:
        return text

    result = text
    # 1. Apply Tone Modifiers first (adds thematic prefixes / phrasing)
    for mod in active_modifiers:
        mod_clean = mod.lower().strip()
        if mod_clean in TONE_MODIFIERS:
            result = TONE_MODIFIERS[mod_clean].apply(result)

    # 2. Apply Visual / Text Modifiers
    for mod in active_modifiers:
        mod_clean = mod.lower().strip()
        if mod_clean in TEXT_MODIFIERS:
            transform = TEXT_MODIFIERS[mod_clean]
            if mod_clean == "zalgo":
                result = transform(result, intensity=glitch_intensity)
            else:
                result = transform(result)

    return result
