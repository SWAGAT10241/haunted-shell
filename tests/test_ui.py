"""
Tests for UI utilities: ANSI palettes, banners, zalgo, typewriter, and box rendering.
"""

import io
import unittest

from haunted_shell.ui import (
    get_banner,
    set_color_enabled,
    spectral_box,
    strip_ansi,
    typewriter,
    zalgo,
)


class TestUI(unittest.TestCase):

    def test_strip_ansi(self):
        colored = "\033[38;5;99mPossessed\033[0m"
        self.assertEqual(strip_ansi(colored), "Possessed")

    def test_zalgo(self):
        text = "Soul"
        # Zero intensity leaves string untouched
        self.assertEqual(zalgo(text, intensity=0), "Soul")

        # Deterministic seed produces glitch characters
        glitched = zalgo(text, intensity=2, seed=42)
        self.assertGreaterEqual(len(glitched), len(text))

    def test_typewriter(self):
        buffer = io.StringIO()
        typewriter("Boo!", delay=0.0001, stream=buffer)
        output = buffer.getvalue()
        self.assertIn("Boo!", output)

    def test_spectral_box(self):
        buffer = io.StringIO()
        spectral_box("TEST BOX", ["First line", "Second line"], stream=buffer)
        output = buffer.getvalue()
        self.assertIn("TEST BOX", output)
        self.assertIn("First line", output)
        self.assertIn("Second line", output)

    def test_banners(self):
        for p in ["poltergeist", "calavera", "unix-elder"]:
            banner = get_banner(p)
            self.assertTrue(len(banner) > 0)

    def test_toggle_color(self):
        set_color_enabled(False)
        from haunted_shell import ui
        self.assertEqual(ui.BOLD, "")
        self.assertEqual(ui.RESET, "")

        set_color_enabled(True)
        self.assertEqual(ui.BOLD, "\033[1m")
        self.assertEqual(ui.RESET, "\033[0m")
