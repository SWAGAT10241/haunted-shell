"""
Tests for GhostEngine: local open-weight inference and offline fallback.
"""

import json
import unittest
import urllib.error
from unittest.mock import MagicMock, patch

from haunted_shell.ghost import GhostEngine


class TestGhostEngine(unittest.TestCase):
    def test_init_defaults(self):
        engine = GhostEngine(force_offline=True, glitch_intensity=0)
        self.assertEqual(engine.persona.name, "poltergeist")
        self.assertTrue(engine.force_offline)
        self.assertFalse(engine.has_local_model)

    def test_offline_haunt_command(self):
        engine = GhostEngine(force_offline=True, glitch_intensity=0)
        res = engine.haunt_command("rm -rf node_modules", exit_code=0)
        self.assertTrue(
            any(w in res.lower() for w in ["void", "ashes", "bytes", "dev/null", "graveyard"])
        )

    def test_offline_error_command(self):
        engine = GhostEngine(force_offline=True, glitch_intensity=0)
        res = engine.haunt_command("python script.py", exit_code=1)
        self.assertTrue(len(res) > 0)

    def test_offline_converse(self):
        engine = GhostEngine(force_offline=True, glitch_intensity=0)
        reply = engine.converse("Who is there?")
        self.assertTrue(len(reply) > 0)

    def test_sanitize_llm_response(self):
        raw = '  "Spirit: The veil has been pierced."  '
        clean = GhostEngine._sanitize_llm_response(raw)
        self.assertEqual(clean, "The veil has been pierced.")

        raw2 = "Ghost: Beware of running rm -rf!"
        self.assertEqual(GhostEngine._sanitize_llm_response(raw2), "Beware of running rm -rf!")

    @patch("urllib.request.urlopen")
    def test_query_local_llm_success(self, mock_urlopen):
        mock_resp = MagicMock()
        mock_resp.status = 200
        mock_resp.read.return_value = json.dumps({"response": "The bytes tremble."}).encode("utf-8")
        mock_urlopen.return_value.__enter__.return_value = mock_resp

        engine = GhostEngine(force_offline=False, glitch_intensity=0)
        reply = engine.query_local_llm("test prompt")
        self.assertEqual(reply, "The bytes tremble.")

    @patch("urllib.request.urlopen")
    def test_query_local_llm_failure_falls_back(self, mock_urlopen):
        mock_urlopen.side_effect = urllib.error.URLError("Connection refused")

        engine = GhostEngine(force_offline=False, glitch_intensity=0)
        reply = engine.query_local_llm("test prompt")
        self.assertIsNone(reply)

    def test_audit_airgap(self):
        engine = GhostEngine(force_offline=True)
        audit = engine.audit_airgap()
        self.assertTrue(audit["airgap_safe"])
        self.assertTrue(audit["external_telemetry_disabled"])
        self.assertTrue(audit["can_run_fully_offline"])
        self.assertTrue(audit["hardware_local_inference"])
