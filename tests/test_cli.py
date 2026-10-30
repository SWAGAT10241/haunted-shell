"""
Tests for Click CLI commands and entry points.
"""

import unittest

from click.testing import CliRunner

from haunted_shell.cli import cli


class TestCLI(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    def test_version(self):
        result = self.runner.invoke(cli, ["--version"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("haunted-shell", result.output)

    def test_whisper(self):
        result = self.runner.invoke(cli, ["--offline", "whisper", "ls -la"])
        self.assertEqual(result.exit_code, 0)
        self.assertTrue(len(result.output.strip()) > 0)

    def test_whisper_exit_code(self):
        result = self.runner.invoke(cli, ["--offline", "whisper", "make build", "-e", "1"])
        self.assertEqual(result.exit_code, 0)
        self.assertTrue(len(result.output.strip()) > 0)

    def test_whisper_with_debug_and_no_color(self):
        result = self.runner.invoke(
            cli, ["--debug", "--no-color", "--offline", "whisper", "git status"]
        )
        self.assertEqual(result.exit_code, 0)

    def test_hook_zsh(self):
        result = self.runner.invoke(cli, ["hook", "zsh"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("add-zsh-hook", result.output)

    def test_hook_bash(self):
        result = self.runner.invoke(cli, ["hook", "bash"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("PROMPT_COMMAND", result.output)

    def test_hook_fish(self):
        result = self.runner.invoke(cli, ["hook", "fish"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("fish_postexec", result.output)

    def test_airgap(self):
        result = self.runner.invoke(cli, ["--offline", "airgap"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("AIR-GAP & PRIVACY AUDIT", result.output)

    def test_doctor(self):
        result = self.runner.invoke(cli, ["--offline", "doctor"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("SYSTEM DIAGNOSTICS", result.output)

    def test_persona_list(self):
        result = self.runner.invoke(cli, ["persona", "list"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("poltergeist", result.output)
        self.assertIn("calavera", result.output)
        self.assertIn("unix-elder", result.output)

    def test_persona_show(self):
        result = self.runner.invoke(cli, ["persona", "show", "calavera"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("CALAVERA", result.output)
        self.assertIn("Día de los Muertos", result.output)

    def test_exorcise_scan(self):
        result = self.runner.invoke(cli, ["exorcise"])
        self.assertEqual(result.exit_code, 0)

    def test_exorcise_banish_protected(self):
        result = self.runner.invoke(cli, ["exorcise", "--banish", "1"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("cannot be banished", result.output)

    def test_config_show(self):
        result = self.runner.invoke(cli, ["config", "show"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("CURRENT CONFIGURATION", result.output)

    def test_config_path(self):
        result = self.runner.invoke(cli, ["config", "path"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("config.json", result.output)

    def test_config_init(self):
        import os
        import tempfile
        from pathlib import Path
        from unittest.mock import patch

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_cfg = Path(tmpdir) / "test_config.json"
            with patch.dict(os.environ, {"HAUNTED_CONFIG_PATH": str(tmp_cfg)}):
                result = self.runner.invoke(cli, ["config", "init"])
                self.assertEqual(result.exit_code, 0)
                self.assertIn("Default configuration written", result.output)
                self.assertTrue(tmp_cfg.is_file())

    def test_seance_dialogue(self):
        # Provide dialogue inputs: a question then "farewell"
        inputs = "What is the meaning of swap?\nfarewell\n"
        result = self.runner.invoke(cli, ["--offline", "seance"], input=inputs)
        self.assertEqual(result.exit_code, 0)
        self.assertIn("SÉANCE CHAMBER", result.output)
        self.assertIn("Spirit:", result.output)
