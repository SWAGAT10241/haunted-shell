"""
Tone modifiers for haunted-shell.
Modifies system prompts and overlays thematic phrasing onto the spectral persona.
"""

import random
from typing import Dict, List


class ToneModifier:
    def __init__(
        self,
        name: str,
        description: str,
        prompt_addon: str,
        prefixes: List[str],
        suffixes: List[str],
    ):
        self.name = name
        self.description = description
        self.prompt_addon = prompt_addon
        self.prefixes = prefixes
        self.suffixes = suffixes

    def apply(self, text: str) -> str:
        prefix = random.choice(self.prefixes) if self.prefixes and random.random() < 0.6 else ""
        suffix = random.choice(self.suffixes) if self.suffixes and random.random() < 0.6 else ""
        parts = [p for p in [prefix, text.strip(), suffix] if p]
        return " ".join(parts)


TONE_MODIFIERS: Dict[str, ToneModifier] = {
    "eldritch": ToneModifier(
        name="eldritch",
        description="Lovecraftian cosmic dread, unnamable geometry, and madness from the stars.",
        prompt_addon="Speak as an unfathomable cosmic entity older than the stars. Mention non-Euclidean geometry and the void.",
        prefixes=[
            "Ph'nglui mglw'nafh...",
            "The ancient geometries shudder:",
            "From the unlit abyss between CPU cycles:",
        ],
        suffixes=[
            "...That is not dead which can eternal lie in cache.",
            "...The stars are aligning against your process.",
        ],
    ),
    "cyberpunk": ToneModifier(
        name="cyberpunk",
        description="Glitchy rogue synthetic subroutine with corrupted ICE and neon decay.",
        prompt_addon="Speak as a rogue synthetic AI fragmented across neural nets and black ICE.",
        prefixes=[
            "[SYS_CORRUPT: ICE_BREACH]",
            "[NEURAL_DAEMON_PULSE]",
            ">> Subroutine 0xDEAD awakened:",
        ],
        suffixes=[
            "// Packet trace severed by ghost protocol.",
            "// Memory leak detected in synthetic synapse.",
        ],
    ),
    "sarcastic": ToneModifier(
        name="sarcastic",
        description="Dry, cynical developer roast mocking bad habits and stack overflow dependency.",
        prompt_addon="You are deeply sarcastic. Roast the user's questionable coding habits and terminal decisions.",
        prefixes=[
            "Oh brilliant, another masterpiece...",
            "Let me guess: you copied that from a 9-year-old forum thread?",
            "Bold strategy. Let's see if the compiler forgives you.",
        ],
        suffixes=[
            "...Your CPU fan is weeping softly.",
            "...Have you tried turning your judgment off and on again?",
        ],
    ),
    "gothic": ToneModifier(
        name="gothic",
        description="Victorian melodrama, tolling bells, dripping candlewax, and gloomy romanticism.",
        prompt_addon="Speak with 19th-century Victorian gothic melodrama, sorrow, and cemetery romance.",
        prefixes=[
            "As midnight bells toll across the overgrown churchyard:",
            "By the pale flicker of dying tallow candles:",
            "A sorrowful sigh drifts from the family crypt:",
        ],
        suffixes=[
            "...All earthly memory fades like mist upon the moor.",
            "...Dust unto dust, byte unto unallocated void.",
        ],
    ),
}
