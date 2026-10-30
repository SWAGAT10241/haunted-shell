"""
UI utilities for haunted-shell: ANSI colors, glitch/zalgo text, ASCII specters, and typewriter animations.
"""

import sys
import time
import random

# ANSI Color Codes
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
ITALIC = "\033[3m"

# Spectral Palette
GHOST_PURPLE = "\033[38;5;99m"
SPECTRAL_CYAN = "\033[38;5;51m"
BLOOD_RED = "\033[38;5;196m"
SLIME_GREEN = "\033[38;5;82m"
MARIGOLD_AMBER = "\033[38;5;214m"
DEATH_GRAY = "\033[38;5;242m"
BONE_WHITE = "\033[38;5;255m"

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

GHOST_BANNERS = {
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


def zalgo(text: str, intensity: int = 1) -> str:
    """Inject subtle or heavy zalgo glitches into text."""
    if intensity <= 0:
        return text
    result = []
    for ch in text:
        result.append(ch)
        if ch.isalnum() and random.random() < 0.25 * intensity:
            num_glitches = random.randint(1, min(3, intensity))
            for _ in range(num_glitches):
                category = random.choice([ZALGO_UP, ZALGO_MID, ZALGO_DOWN])
                result.append(random.choice(category))
    return "".join(result)


def typewriter(text: str, delay: float = 0.015, color: str = GHOST_PURPLE, end: str = "\n"):
    """Typewriter print with eerie rhythmic pauses."""
    sys.stdout.write(color)
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        if char in {'.', '!', '?'}:
            time.sleep(delay * 6)
        elif char in {',', ':', ';'}:
            time.sleep(delay * 3)
        else:
            time.sleep(delay * random.uniform(0.7, 1.3))
    sys.stdout.write(RESET + end)
    sys.stdout.flush()


def spectral_box(title: str, lines: list, color: str = GHOST_PURPLE, border_color: str = DEATH_GRAY):
    """Draw an eerie formatted box in the terminal."""
    max_len = max([len(title) + 4] + [len(l) for l in lines] + [48])
    top = f"{border_color}┌─[ {color}{BOLD}{title}{RESET}{border_color} ]" + "─" * (max_len - len(title) - 5) + "┐"
    bottom = f"{border_color}└" + "─" * max_len + f"┘{RESET}"

    print(top)
    for line in lines:
        pad = max_len - len(line) - 2
        print(f"{border_color}│{RESET} {line}" + " " * max(0, pad) + f" {border_color}│{RESET}")
    print(bottom)


def get_banner(persona: str = "poltergeist") -> str:
    return GHOST_BANNERS.get(persona, GHOST_BANNERS["poltergeist"])
