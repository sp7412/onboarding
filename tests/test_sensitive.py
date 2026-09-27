"""Tests for the sensitive-content scanner using fake placeholder patterns."""
from __future__ import annotations

import os
import re
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import scripts.check_sensitive as checker


class SensitivePatternTests(unittest.TestCase):
    def test_reads_patterns_from_environment(self):
        with patch.dict(os.environ, {"SENSITIVE_PATTERNS": "acme-internal,red-team-only"}):
            self.assertEqual(checker.configured_patterns(), ["acme-internal", "red-team-only"])

    def test_reads_patterns_from_local_file(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".sensitive-patterns").write_text("acme-internal\nred-team-only\n")
            with patch.object(checker, "ROOT", root), patch.dict(os.environ, {"SENSITIVE_PATTERNS": ""}):
                self.assertEqual(checker.configured_patterns(), ["acme-internal", "red-team-only"])

    def test_fake_pattern_matches_case_insensitively(self):
        self.assertIsNotNone(re.search("acme-internal", "ACME-INTERNAL", re.IGNORECASE))


if __name__ == "__main__":
    unittest.main()
