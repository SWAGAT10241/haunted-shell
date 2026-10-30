"""
Tests for haunted-shell configuration management.
"""

import os
import tempfile
import unittest
from pathlib import Path

from haunted_shell.config import HauntedConfig, load_config, save_config


class TestConfig(unittest.TestCase):
    def test_default_config(self):
        cfg = HauntedConfig()
        self.assertEqual(cfg.persona, "poltergeist")
        self.assertEqual(cfg.model, "gemma2:2b")
        self.assertFalse(cfg.offline)
        self.assertEqual(cfg.glitch_intensity, 1)
        self.assertEqual(cfg.ollama_url, "http://localhost:11434")

    def test_load_config_cli_overrides(self):
        cfg = load_config(
            persona="calavera",
            offline=True,
            model="llama3.2",
            glitch_intensity=2,
            no_color=True,
            debug=True,
        )
        self.assertEqual(cfg.persona, "calavera")
        self.assertTrue(cfg.offline)
        self.assertEqual(cfg.model, "llama3.2")
        self.assertEqual(cfg.glitch_intensity, 2)
        self.assertTrue(cfg.no_color)
        self.assertTrue(cfg.debug)

    def test_env_var_overrides(self):
        old_env = dict(os.environ)
        try:
            os.environ["HAUNTED_PERSONA"] = "unix-elder"
            os.environ["HAUNTED_MODEL"] = "mistral:7b"
            os.environ["HAUNTED_OFFLINE"] = "1"
            os.environ["HAUNTED_GLITCH"] = "3"
            os.environ["HAUNTED_DEBUG"] = "true"

            cfg = load_config()
            self.assertEqual(cfg.persona, "unix-elder")
            self.assertEqual(cfg.model, "mistral:7b")
            self.assertTrue(cfg.offline)
            self.assertEqual(cfg.glitch_intensity, 3)
            self.assertTrue(cfg.debug)
        finally:
            os.environ.clear()
            os.environ.update(old_env)

    def test_save_and_load_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "config.json"
            cfg = HauntedConfig(persona="calavera", model="custom-ghost", glitch_intensity=0)
            saved = save_config(cfg, path=file_path)
            self.assertTrue(saved.is_file())

            loaded = load_config(config_path=file_path)
            self.assertEqual(loaded.persona, "calavera")
            self.assertEqual(loaded.model, "custom-ghost")
            self.assertEqual(loaded.glitch_intensity, 0)

    def test_glitch_intensity_clamping(self):
        cfg1 = load_config(glitch_intensity=99)
        self.assertEqual(cfg1.glitch_intensity, 3)

        cfg2 = load_config(glitch_intensity=-5)
        self.assertEqual(cfg2.glitch_intensity, 0)
