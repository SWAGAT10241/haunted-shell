"""
Tests for system diagnostics doctor tool.
"""

import json
import unittest
from unittest.mock import MagicMock, patch

from haunted_shell.config import HauntedConfig
from haunted_shell.doctor import run_doctor


class TestDoctor(unittest.TestCase):
    def test_run_doctor_offline(self):
        cfg = HauntedConfig(offline=True)
        res = run_doctor(cfg)
        self.assertIn("python_version", res)
        self.assertIn("os", res)
        self.assertFalse(res["ollama_reachable"])

    @patch("urllib.request.urlopen")
    def test_run_doctor_online_success(self, mock_urlopen):
        mock_resp = MagicMock()
        mock_resp.status = 200
        mock_resp.read.return_value = json.dumps({"models": [{"name": "gemma2:2b"}]}).encode(
            "utf-8"
        )
        mock_urlopen.return_value.__enter__.return_value = mock_resp

        cfg = HauntedConfig(offline=False)
        res = run_doctor(cfg)
        self.assertTrue(res["ollama_reachable"])
        self.assertIn("gemma2:2b", res["ollama_models"])
