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

    def test_rejects_missing_control_section(self):
        raw = "# MASVS-STORAGE-1\n\n## Description\n\nBad input without a control section.\n"
        with self.assertRaises(ValueError) as ctx:
            parse_upstream_control(raw)
        self.assertIn("## Control", str(ctx.exception))


class TestComposeFrontmatter(unittest.TestCase):
    def test_defaults_for_fresh_file(self):
        from extract_masvs_sections import compose_frontmatter

        parsed = {
            "control_id": "MASVS-STORAGE-1",
            "group": "MASVS-STORAGE",
            "summary": "Sensitive data is stored securely.",
            "description": "...",
        }
        fm = compose_frontmatter(parsed, existing=None)
        self.assertEqual(fm["title"], "MASVS-STORAGE-1: Sensitive data is stored securely.")
        self.assertEqual(fm["masvs_group"], "MASVS-STORAGE")
        self.assertEqual(fm["masvs_control"], "MASVS-STORAGE-1")
        self.assertEqual(fm["summary"], "Sensitive data is stored securely.")
        self.assertEqual(fm["platforms"], ["android", "ios"])
        self.assertEqual(fm["when_to_use"], [])
        self.assertEqual(fm["threats"], [])
        self.assertEqual(fm["mastg_tests"], [])
        self.assertEqual(fm["static_signals"], {"android": [], "ios": []})
        self.assertEqual(fm["resilience_static_only"], False)
        self.assertEqual(fm["static_only"], False)

    def test_resilience_group_defaults_static_only_true(self):
        from extract_masvs_sections import compose_frontmatter

        parsed = {
            "control_id": "MASVS-RESILIENCE-1",
            "group": "MASVS-RESILIENCE",
            "summary": "App detects tampering.",
            "description": "...",
        }
        fm = compose_frontmatter(parsed, existing=None)
        self.assertTrue(fm["resilience_static_only"])

    def test_preserves_enrichment_from_existing(self):
        from extract_masvs_sections import compose_frontmatter

        parsed = {
            "control_id": "MASVS-STORAGE-1",
            "group": "MASVS-STORAGE",
            "summary": "NEW upstream summary",
            "description": "...",
        }
        existing = {
            "title": "OLD title that should be overwritten",
            "masvs_group": "MASVS-STORAGE",
            "masvs_control": "MASVS-STORAGE-1",
            "summary": "OLD summary",
            "platforms": ["android", "ios"],
            "when_to_use": ["reviewing data storage"],
            "threats": ["data leakage"],
            "mastg_tests": ["MASTG-TEST-0001"],
            "static_signals": {"android": ["SharedPreferences"], "ios": ["NSUserDefaults"]},
            "resilience_static_only": False,
            "static_only": False,
        }
        fm = compose_frontmatter(parsed, existing=existing)
        self.assertEqual(fm["title"], "MASVS-STORAGE-1: NEW upstream summary")
        self.assertEqual(fm["summary"], "NEW upstream summary")
        self.assertEqual(fm["when_to_use"], ["reviewing data storage"])
        self.assertEqual(fm["threats"], ["data leakage"])
        self.assertEqual(fm["mastg_tests"], ["MASTG-TEST-0001"])
        self.assertEqual(
            fm["static_signals"], {"android": ["SharedPreferences"], "ios": ["NSUserDefaults"]}
        )


class TestRenderOutput(unittest.TestCase):
    def test_produces_valid_yaml_then_body(self):
        import yaml
        from extract_masvs_sections import render_output

        parsed = {
            "control_id": "MASVS-AUTH-1",
            "group": "MASVS-AUTH",
            "summary": "Secure auth.",
            "description": "Most apps...",
        }
        frontmatter = {
            "title": "MASVS-AUTH-1: Secure auth.",
            "masvs_group": "MASVS-AUTH",
            "masvs_control": "MASVS-AUTH-1",
            "summary": "Secure auth.",
            "platforms": ["android", "ios"],
            "when_to_use": [],
            "threats": [],
            "mastg_tests": [],
            "static_signals": {"android": [], "ios": []},
            "resilience_static_only": False,
            "static_only": False,
        }
        out = render_output(frontmatter, parsed)
        self.assertTrue(out.startswith("---\n"))
        parts = out.split("---\n", 2)
        self.assertEqual(len(parts), 3)
        loaded = yaml.safe_load(parts[1])
        self.assertEqual(loaded["masvs_control"], "MASVS-AUTH-1")
        body = parts[2]
        self.assertIn("# MASVS-AUTH-1", body)
        self.assertIn("## Control", body)
        self.assertIn("## Description", body)
        self.assertTrue(out.endswith("\n"))


if __name__ == "__main__":
    unittest.main()
