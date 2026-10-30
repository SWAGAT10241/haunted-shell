"""
Visual and text modifiers for haunted-shell.
Transforms spectral output into different aesthetic and glitch formats.
"""

import random
from typing import Dict, Callable

from ..ui import zalgo

UPSIDE_DOWN_MAP = {
    'a': 'ɐ', 'b': 'q', 'c': 'ɔ', 'd': 'p', 'e': 'ǝ', 'f': 'ɟ', 'g': 'ƃ', 'h': 'ɥ',
    'i': 'ᴉ', 'j': 'ɾ', 'k': 'ʞ', 'l': 'l', 'm': 'ɯ', 'n': 'u', 'o': 'o', 'p': 'd',
    'q': 'b', 'r': 'ɹ', 's': 's', 't': 'ʇ', 'u': 'n', 'v': 'ʌ', 'w': 'ʍ', 'x': 'x',
    'y': 'ʎ', 'z': 'z', 'A': '∀', 'B': 'ᗺ', 'C': 'Ɔ', 'D': 'ᗡ', 'E': 'Ǝ', 'F': 'Ⅎ',
    'G': '⅁', 'H': 'H', 'I': 'I', 'J': 'ſ', 'K': 'ʞ', 'L': '˥', 'M': 'W', 'N': 'N',
    'O': 'O', 'P': 'Ԁ', 'Q': 'Ό', 'R': 'ᴚ', 'S': 'S', 'T': '⊥', 'U': '∩', 'V': 'Λ',
    'W': 'M', 'X': 'X', 'Y': '⅄', 'Z': 'Z', '?': '¿', '!': '¡', '.': '˙', ',': "'"
}

MORSE_CODE = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..', '0': '-----', '1': '.----', '2': '..---',
    '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...',
    '8': '---..', '9': '----.'
}

MATRIX_GLYPHS = ["0", "1", "0x00", "0xFF", "ｦ", "ｱ", "ｳ", "ｴ", "ｵ", "ｶ", "ｷ", "ｹ", "ｺ", "ｻ", "ｼ", "ｽ", "ｾ", "ｿ"]


def modify_zalgo(text: str, intensity: int = 2) -> str:
    """Standard zalgo glitch combining mark injection."""
    return zalgo(text, intensity=intensity)


def modify_cursed(text: str, **kwargs) -> str:
    """Invert characters upside-down to look like unholy incantations."""
    res = []
    for char in text:
        res.append(UPSIDE_DOWN_MAP.get(char, char))
    return "".join(reversed(res))


def modify_matrix(text: str, **kwargs) -> str:
    """Inject digital rain binary and phosphor glyphs into text."""
    words = text.split()
    res = []
    for word in words:
        if random.random() < 0.25:
            res.append(f"{random.choice(MATRIX_GLYPHS)}{word}")
        else:
            res.append(word)
    return " ".join(res)


def modify_whisper(text: str, **kwargs) -> str:
    """Lowers case, adds wide spacing and breathing ellipses."""
    cleaned = text.lower().replace("\n", " ")
    spaced = " ".join(cleaned)
    return f"... {spaced} ..."


def modify_vaporwave(text: str, **kwargs) -> str:
    """Transform text into fullwidth aesthetic characters."""
    res = []
    for char in text:
        code = ord(char)
        if 0x21 <= code <= 0x7E:
            res.append(chr(code + 0xFEE0))
        elif code == 0x20:
            res.append("\u3000")
        else:
            res.append(char)
    return "".join(res)


def modify_morse(text: str, **kwargs) -> str:
    """Appends an ominous telegraphic morse code cipher."""
    first_word = text.strip().split()[0].upper() if text.strip() else "DEAD"
    morse_trans = " ".join(MORSE_CODE.get(ch, "") for ch in first_word if ch in MORSE_CODE)
    return f"{text} [📡 {morse_trans}]"


TEXT_MODIFIERS: Dict[str, Callable[[str], str]] = {
    "zalgo": modify_zalgo,
    "cursed": modify_cursed,
    "matrix": modify_matrix,
    "whisper": modify_whisper,
    "vaporwave": modify_vaporwave,
    "morse": modify_morse,
}
