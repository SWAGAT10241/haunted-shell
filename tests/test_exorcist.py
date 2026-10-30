"""
Tests for Exorcist: process census and safety guards.
"""

import os
import unittest

from haunted_shell.exorcist import Exorcist


class TestExorcist(unittest.TestCase):

    def setUp(self):
        self.exorcist = Exorcist()

    def test_protected_pids(self):
        # PID 0 and 1 are protected
        blocked_0, reason_0 = self.exorcist.is_protected(0)
        self.assertTrue(blocked_0)
        self.assertIn("root kernel/init", reason_0)

        blocked_1, reason_1 = self.exorcist.is_protected(1)
        self.assertTrue(blocked_1)
        self.assertIn("root kernel/init", reason_1)

        # Self PID is protected (suicide guard)
        blocked_self, reason_self = self.exorcist.is_protected(os.getpid())
        self.assertTrue(blocked_self)
        self.assertIn("suicide averted", reason_self)

        # Parent PID is protected
        blocked_ppid, reason_ppid = self.exorcist.is_protected(os.getppid())
        self.assertTrue(blocked_ppid)
        self.assertIn("terminal shell", reason_ppid)

        # launchd/systemd protected
        blocked_sys, reason_sys = self.exorcist.is_protected(99999, name="launchd")
        self.assertTrue(blocked_sys)

        # Regular process is not protected
        blocked_reg, _ = self.exorcist.is_protected(99999, name="my_app")
        self.assertFalse(blocked_reg)

    def test_exorcise_protected_blocked(self):
        success, msg = self.exorcist.exorcise(1)
        self.assertFalse(success)
        self.assertIn("root kernel/init", msg)

    def test_exorcise_non_existent(self):
        # PID 999999 is unlikely to exist
        success, msg = self.exorcist.exorcise(999999)
        self.assertFalse(success)
        self.assertIn("no longer exists", msg)

    def test_scan_spirits(self):
        spirits = self.exorcist.scan_spirits(limit=5)
        self.assertIsInstance(spirits, list)
        self.assertLessEqual(len(spirits), 5)
        for s in spirits:
            self.assertIn("pid", s)
            self.assertIn("name", s)
            self.assertIn("type", s)
            self.assertIn("epitaph", s)

    def test_render_spectral_report_empty(self):
        # Should not raise exception
        self.exorcist.render_spectral_report([])
