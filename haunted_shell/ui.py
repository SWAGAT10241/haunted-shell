"""
UI utilities for haunted-shell: ANSI colors, glitch/zalgo text, ASCII specters, and typewriter animations.
Supports NO_COLOR standard, non-interactive streams, and dynamic terminal resizing.
"""

import os
import random
import re
import shutil
import sys
import time
from typing import List, Optional


def supports_color() -> bool:
    """Check if the current terminal environment supports ANSI color codes."""
    if "NO_COLOR" in os.environ:
        return False
    if os.environ.get("TERM", "").lower() == "dumb":
        return False
    if not hasattr(sys.stdout, "isatty") or not sys.stdout.isatty():
        return False
    return True


# ANSI formatting codes
class Palette:
    def __init__(self, enabled: bool = True):
        self.enabled = enabled

    @property
    def RESET(self) -> str:
        return "\033[0m" if self.enabled else ""

    @property
    def BOLD(self) -> str:
        return "\033[1m" if self.enabled else ""

    @property
    def DIM(self) -> str:
        return "\033[2m" if self.enabled else ""

    @property
    def ITALIC(self) -> str:
        return "\033[3m" if self.enabled else ""

    @property
    def GHOST_PURPLE(self) -> str:
        return "\033[38;5;99m" if self.enabled else ""

    @property
    def SPECTRAL_CYAN(self) -> str:
        return "\033[38;5;51m" if self.enabled else ""

    @property
    def BLOOD_RED(self) -> str:
        return "\033[38;5;196m" if self.enabled else ""

    @property
    def SLIME_GREEN(self) -> str:
        return "\033[38;5;82m" if self.enabled else ""

    @property
    def MARIGOLD_AMBER(self) -> str:
        return "\033[38;5;214m" if self.enabled else ""

    @property
    def DEATH_GRAY(self) -> str:
        return "\033[38;5;242m" if self.enabled else ""

    @property
    def BONE_WHITE(self) -> str:
        return "\033[38;5;255m" if self.enabled else ""


_PALETTE = Palette(enabled=supports_color())

RESET = _PALETTE.RESET
BOLD = _PALETTE.BOLD
DIM = _PALETTE.DIM
ITALIC = _PALETTE.ITALIC
GHOST_PURPLE = _PALETTE.GHOST_PURPLE
SPECTRAL_CYAN = _PALETTE.SPECTRAL_CYAN
BLOOD_RED = _PALETTE.BLOOD_RED
SLIME_GREEN = _PALETTE.SLIME_GREEN
MARIGOLD_AMBER = _PALETTE.MARIGOLD_AMBER
DEATH_GRAY = _PALETTE.DEATH_GRAY
BONE_WHITE = _PALETTE.BONE_WHITE


def set_color_enabled(enabled: bool) -> None:
    """Globally toggle color palette output."""
    global RESET, BOLD, DIM, ITALIC, GHOST_PURPLE, SPECTRAL_CYAN
    global BLOOD_RED, SLIME_GREEN, MARIGOLD_AMBER, DEATH_GRAY, BONE_WHITE, _PALETTE
    _PALETTE = Palette(enabled=enabled)
    RESET = _PALETTE.RESET
    BOLD = _PALETTE.BOLD
    DIM = _PALETTE.DIM
    ITALIC = _PALETTE.ITALIC
    GHOST_PURPLE = _PALETTE.GHOST_PURPLE
    SPECTRAL_CYAN = _PALETTE.SPECTRAL_CYAN
    BLOOD_RED = _PALETTE.BLOOD_RED
    SLIME_GREEN = _PALETTE.SLIME_GREEN
    MARIGOLD_AMBER = _PALETTE.MARIGOLD_AMBER
    DEATH_GRAY = _PALETTE.DEATH_GRAY
    BONE_WHITE = _PALETTE.BONE_WHITE


# Glitch / Zalgo combining characters
ZALGO_UP = [
    '\u030d', '\u030e', '\u0304', '\u0305', '\u033f', '\u0311', '\u0306', '\u0310',
    '\u0352', '\u0357', '\u0351', '\u0307', '\u0308', '\u030a', '\u0342', '\u0343'
]
ZALGO_MID = [
    '\u0315', '\u031b', '\u0340', '\u0341', '\u0358', '\u0321', '\u0322', '\u0327',
    '\u0328', '\u0334', '\u0335', '\u0336', '\u0337', '\u0338'
]
ZALGO_DOWN = [
    '\u0316', '\u0317', '\u0318', '\u0319', '\u031c', '\u031d', '\u031e', '\u031f',
    '\u0320', '\u0324', '\u0325', '\u0326', '\u0329', '\u032a', '\u032b', '\u032c'
]


def strip_ansi(text: str) -> str:
    """Remove ANSI escape sequences for accurate visual length measurement."""
    return re.sub(r'\x1B\[[0-?]*[ -/]*[@-~]', '', text)


def zalgo(text: str, intensity: int = 1, seed: Optional[int] = None) -> str:
    """Inject subtle or heavy zalgo glitches into text."""
    if intensity <= 0:
        return text

    rng = random.Random(seed) if seed is not None else random
    result = []
    for ch in text:
        result.append(ch)
        if ch.isalnum() and rng.random() < 0.25 * intensity:
            num_glitches = rng.randint(1, min(3, intensity))
            for _ in range(num_glitches):
                category = rng.choice([ZALGO_UP, ZALGO_MID, ZALGO_DOWN])
                result.append(rng.choice(category))
    return "".join(result)


def typewriter(
    text: str,
    delay: float = 0.015,
    color: str = "",
    end: str = "\n",
    stream=None
) -> None:
    """Typewriter print with eerie rhythmic pauses and interrupt resilience."""
    out = stream if stream is not None else sys.stdout
    use_color = color or GHOST_PURPLE
    try:
        out.write(use_color)
        for char in text:
            out.write(char)
            out.flush()
            if char in {'.', '!', '?'}:
                time.sleep(delay * 4)
            elif char in {',', ':', ';'}:
                time.sleep(delay * 2)
            else:
                time.sleep(delay * random.uniform(0.7, 1.3))
        out.write(RESET + end)
        out.flush()
    except KeyboardInterrupt:
        out.write(RESET + end)
        out.flush()


def spectral_box(
    title: str,
    lines: List[str],
    color: str = "",
    border_color: str = "",
    stream=None
) -> None:
    """Draw an eerie formatted box with dynamic terminal width constraints."""
    out = stream if stream is not None else sys.stdout
    box_color = color or GHOST_PURPLE
    border = border_color or DEATH_GRAY

    # Determine terminal width (default 80 if unavailable)
    term_cols = shutil.get_terminal_size(fallback=(80, 24)).columns
    max_box_width = min(term_cols - 2, 90)

    # Calculate content width
    clean_title_len = len(strip_ansi(title))
    content_max = clean_title_len + 6
    for item in lines:
        content_max = max(content_max, len(strip_ansi(item)))

    max_len = max(min(content_max, max_box_width - 4), 48)

    top = f"{border}┌─[ {box_color}{BOLD}{title}{RESET}{border} ]" + "─" * max(0, max_len - clean_title_len - 5) + f"┐{RESET}"
    bottom = f"{border}└" + "─" * max_len + f"┘{RESET}"

    out.write(top + "\n")
    for line in lines:
        clean_len = len(strip_ansi(line))
        pad = max(0, max_len - clean_len - 2)
        out.write(f"{border}│{RESET} {line}" + " " * pad + f" {border}│{RESET}\n")
    out.write(bottom + "\n")
    out.flush()


def get_banner(persona: str = "poltergeist") -> str:
    """Return stylized ASCII banner for persona."""
    banners = {
        "poltergeist": f"""{GHOST_PURPLE}
      .-.
     (o o) boo!
     | O \\
      \\   \\      G H O S T   I N   T H E   M A C H I N E
       `~~~'     [ The terminal is possessed. Open-source local spirit online. ]
{RESET}""",
        "calavera": f"""{MARIGOLD_AMBER}
      .-''''-.
     / _    _ \\     D Í A   D E   L O S   M U E R T O S
    | (o)  (o) |    [ Honor the past. Transience in the shell. ]
    |   <__>   |    [ Cempasúchil petals fall upon your memory... ]
     \\  .__.  /
      `------'
{RESET}""",
        "unix-elder": f"""{SLIME_GREEN}
     .--------------------------------------------------------.
     | [PDP-11 DAEMON - 1971] PID 0xDEADBEEF AWAKENED        |
     | "In the old days, we had 4KB and we liked it."          |
     '--------------------------------------------------------'
{RESET}"""
    }
    return banners.get(persona.lower(), banners["poltergeist"])
