"""Tests for extract_masvs_sections.py — run via: python scripts/test_extract_masvs_sections.py -v"""
import sys
import textwrap
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from extract_masvs_sections import parse_upstream_control


class TestParseUpstreamControl(unittest.TestCase):
    def test_parses_basic_control(self):
        raw = textwrap.dedent("""\
            # MASVS-AUTH-1

            ## Control

            The app uses secure authentication and authorization protocols and follows the relevant best practices.

            ## Description

            Most apps connecting to a remote endpoint require user authentication.
            """)
        result = parse_upstream_control(raw)
        self.assertEqual(result["control_id"], "MASVS-AUTH-1")
        self.assertEqual(result["group"], "MASVS-AUTH")
        self.assertEqual(
            result["summary"],
            "The app uses secure authentication and authorization protocols and follows the relevant best practices.",
        )
        self.assertIn("Most apps connecting to a remote endpoint", result["description"])

    def test_strips_extra_whitespace(self):
        raw = "# MASVS-CODE-2  \n\n## Control\n\n  Foo bar.  \n\n## Description\n\nBaz.\n"
        result = parse_upstream_control(raw)
        self.assertEqual(result["control_id"], "MASVS-CODE-2")
        self.assertEqual(result["summary"], "Foo bar.")
        self.assertEqual(result["description"], "Baz.")

    def test_rejects_malformed_input(self):
        with self.assertRaises(ValueError):
            parse_upstream_control("# Not a MASVS control\n\n## Whatever\n\nNope.\n")


if __name__ == "__main__":
    unittest.main()
