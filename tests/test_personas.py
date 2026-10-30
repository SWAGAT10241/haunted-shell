"""
Tests for haunted-shell personas and registry.
"""

import unittest

from haunted_shell.personas import (
    available_persona_names,
    get_persona,
    register_persona,
)
from haunted_shell.personas.base import BasePersona
from haunted_shell.personas.calavera import CalaveraPersona
from haunted_shell.personas.poltergeist import PoltergeistPersona
from haunted_shell.personas.unix_elder import UnixElderPersona


class CustomPersona(BasePersona):
    name = "phantom-test"
    title = "Test Phantom"
    color_name = "cyan"
    prompt_symbol = "🔮"
    system_prompt = "You are a test phantom."

    def generate_commentary(self, cmd, exit_code=0, context=None):
        return f"Echo {cmd}"

    def converse(self, utterance):
        return "Converse test"


class TestPersonas(unittest.TestCase):
    def test_poltergeist(self):
        p = PoltergeistPersona()
        self.assertEqual(p.name, "poltergeist")
        self.assertEqual(p.prompt_symbol, "👻")
        comment = p.generate_commentary("rm old_file.txt", exit_code=0)
        self.assertTrue(len(comment) > 0)
        farewell = p.get_farewell()
        self.assertIn("swap", farewell)

    def test_calavera(self):
        p = CalaveraPersona()
        self.assertEqual(p.name, "calavera")
        self.assertEqual(p.prompt_symbol, "💀")
        comment = p.generate_commentary("git commit -m 'feat'", exit_code=0)
        self.assertTrue(len(comment) > 0)
        err_comment = p.generate_commentary("rm nonexistent", exit_code=1)
        self.assertTrue(len(err_comment) > 0)
        rm_comment = p.generate_commentary("rm file.txt", exit_code=0)
        self.assertTrue(len(rm_comment) > 0)
        who_comment = p.generate_commentary("whoami", exit_code=0)
        self.assertTrue(len(who_comment) > 0)
        empty_comment = p.generate_commentary("", exit_code=0)
        self.assertTrue(len(empty_comment) > 0)
        conv = p.converse("hello")
        self.assertTrue(len(conv) > 0)
        self.assertIn("cempasúchil", p.get_farewell())

    def test_unix_elder(self):
        p = UnixElderPersona()
        self.assertEqual(p.name, "unix-elder")
        self.assertEqual(p.prompt_symbol, "#")
        comment = p.generate_commentary("cat file.txt", exit_code=0)
        self.assertTrue(len(comment) > 0)
        err_comment = p.generate_commentary("make", exit_code=2)
        self.assertTrue(len(err_comment) > 0)
        rm_comment = p.generate_commentary("rm file.txt", exit_code=0)
        self.assertTrue(len(rm_comment) > 0)
        who_comment = p.generate_commentary("whoami", exit_code=0)
        self.assertTrue(len(who_comment) > 0)
        empty_comment = p.generate_commentary("", exit_code=0)
        self.assertTrue(len(empty_comment) > 0)
        conv = p.converse("status")
        self.assertTrue(len(conv) > 0)
        self.assertIn("Teletype", p.get_farewell())

    def test_registry(self):
        names = available_persona_names()
        self.assertIn("poltergeist", names)
        self.assertIn("calavera", names)
        self.assertIn("unix-elder", names)

        p = get_persona("calavera")
        self.assertEqual(p.name, "calavera")

        # Unknown name falls back to poltergeist
        fallback = get_persona("non-existent-spirit")
        self.assertEqual(fallback.name, "poltergeist")

    def test_custom_persona_registration(self):
        custom = CustomPersona()
        register_persona(custom)
        names = available_persona_names()
        self.assertIn("phantom-test", names)
        retrieved = get_persona("phantom-test")
        self.assertEqual(retrieved.title, "Test Phantom")
        self.assertEqual(retrieved.generate_commentary("ls"), "Echo ls")
