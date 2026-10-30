"""
Tests for haunted-shell.
"""

import unittest

from haunted_shell.exorcist import Exorcist
from haunted_shell.ghost import GhostEngine
from haunted_shell.shell_hook import generate_hook
from haunted_shell.ui import get_banner, zalgo


class TestHauntedShell(unittest.TestCase):

    def test_poltergeist_persona(self):
        engine = GhostEngine(persona_name="poltergeist", force_offline=True, glitch_intensity=0)
        whisper_rm = engine.haunt_command("rm -rf old_secrets.txt", exit_code=0)
        self.assertTrue(any(word in whisper_rm.lower() for word in ["void", "bytes", "ashes", "graveyard", "dev/null"]))

        whisper_err = engine.haunt_command("make build", exit_code=1)
        self.assertTrue(len(whisper_err) > 0)

    def test_calavera_persona(self):
        engine = GhostEngine(persona_name="calavera", force_offline=True, glitch_intensity=0)
        whisper = engine.haunt_command("git commit -m 'Initial commit'", exit_code=0)
        self.assertTrue(len(whisper) > 0)

    def test_unix_elder_persona(self):
        engine = GhostEngine(persona_name="unix-elder", force_offline=True, glitch_intensity=0)
        whisper = engine.haunt_command("git push origin main", exit_code=0)
        self.assertTrue(len(whisper) > 0)

    def test_airgap_audit(self):
        engine = GhostEngine(force_offline=True)
        audit = engine.audit_airgap()
        self.assertTrue(audit["airgap_safe"])
        self.assertTrue(audit["external_telemetry_disabled"])
        self.assertTrue(audit["can_run_fully_offline"])

    def test_exorcist_scanner(self):
        exorcist = Exorcist()
        spirits = exorcist.scan_spirits(limit=3)
        self.assertIsInstance(spirits, list)
        if spirits:
            first = spirits[0]
            self.assertIn("pid", first)
            self.assertIn("name", first)
            self.assertIn("epitaph", first)

    def test_zalgo_glitch(self):
        text = "Hello world"
        glitched = zalgo(text, intensity=2)
        # Glitched string should contain combining marks or be longer than original
        self.assertTrue(len(glitched) >= len(text))

    def test_hooks(self):
        zsh_hook = generate_hook("zsh")
        self.assertIn("add-zsh-hook", zsh_hook)
        bash_hook = generate_hook("bash")
        self.assertIn("PROMPT_COMMAND", bash_hook)

    def test_banners(self):
        for p in ["poltergeist", "calavera", "unix-elder"]:
            banner = get_banner(p)
            self.assertTrue(len(banner) > 0)


if __name__ == "__main__":
    unittest.main()
