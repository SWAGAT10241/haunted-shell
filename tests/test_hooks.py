"""
Tests for shell hook generation.
"""

import unittest

from haunted_shell.shell_hook import generate_hook


class TestShellHooks(unittest.TestCase):

    def test_zsh_hook(self):
        hook = generate_hook("zsh")
        self.assertIn("add-zsh-hook", hook)
        self.assertIn("haunt whisper", hook)

    def test_bash_hook(self):
        hook = generate_hook("bash")
        self.assertIn("PROMPT_COMMAND", hook)
        self.assertIn("haunt whisper", hook)

    def test_fish_hook(self):
        hook = generate_hook("fish")
        self.assertIn("fish_postexec", hook)
        self.assertIn("haunt whisper", hook)
