"""
Unit tests for the custom modifier system in haunted-shell.
"""

import os
import unittest
from haunted_shell.modifiers.text_modifiers import (
    modify_cursed,
    modify_matrix,
    modify_morse,
    modify_vaporwave,
    modify_whisper,
    modify_zalgo,
)
from haunted_shell.modifiers.tone_modifiers import TONE_MODIFIERS
from haunted_shell.modifiers.custom_rules import CustomRuleEngine
from haunted_shell.modifiers import apply_all_modifiers
from haunted_shell.ghost import GhostEngine


class TestModifierSystem(unittest.TestCase):

    def test_text_modifiers(self):
        sample = "Ghost in the Machine"
        self.assertNotEqual(modify_cursed(sample), sample)
        self.assertIn("...", modify_whisper(sample))
        self.assertIn("📡", modify_morse(sample))
        self.assertTrue(len(modify_vaporwave(sample)) >= len(sample))
        self.assertTrue(len(modify_matrix(sample)) >= len(sample))
        self.assertTrue(len(modify_zalgo(sample)) >= len(sample))

    def test_tone_modifiers(self):
        sample = "Memory leak in heap."
        for name, tone in TONE_MODIFIERS.items():
            modified = tone.apply(sample)
            self.assertIn("Memory leak", modified)

    def test_custom_command_rules(self):
        engine = CustomRuleEngine()
        hit = engine.match("docker run -d redis")
        self.assertIsNotNone(hit)
        self.assertTrue(any(w in hit.lower() for w in ["container", "layer", "cgroup", "daemon"]))

        hit_npm = engine.match("npm install lodash")
        self.assertIsNotNone(hit_npm)
        self.assertTrue(any(w in hit_npm.lower() for w in ["strangers", "node_modules", "black hole", "registry"]))

    def test_ghost_engine_with_modifiers(self):
        engine = GhostEngine(force_offline=True, modifiers=["vaporwave", "sarcastic"])
        whisper = engine.haunt_command("whoami")
        self.assertTrue(len(whisper) > 0)


if __name__ == "__main__":
    unittest.main()
