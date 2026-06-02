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
        self.assertEqual(fm["mastg_tests"], [])
        # Dropped fields must not appear
        self.assertNotIn("when_to_use", fm)
        self.assertNotIn("threats", fm)
        self.assertNotIn("static_signals", fm)
        self.assertNotIn("coverage", fm)
        self.assertNotIn("platforms", fm)

    def test_mastg_tests_derived_from_index(self):
        """mastg_tests comes from the supplied index, not existing or default."""
        from extract_masvs_sections import compose_frontmatter

        parsed = {
            "control_id": "MASVS-STORAGE-1",
            "group": "MASVS-STORAGE",
            "summary": "...",
            "description": "...",
        }
        index = {"MASVS-STORAGE-1": ["MASTG-TEST-0200", "MASTG-TEST-0201"]}
        fm = compose_frontmatter(parsed, existing=None, mastg_index=index)
        self.assertEqual(fm["mastg_tests"], ["MASTG-TEST-0200", "MASTG-TEST-0201"])

    def test_mastg_tests_empty_when_no_match_in_index(self):
        from extract_masvs_sections import compose_frontmatter

        parsed = {
            "control_id": "MASVS-CODE-1",
            "group": "MASVS-CODE",
            "summary": "...",
            "description": "...",
        }
        index = {"MASVS-STORAGE-1": ["MASTG-TEST-0200"]}  # CODE-1 not in index
        fm = compose_frontmatter(parsed, existing=None, mastg_index=index)
        self.assertEqual(fm["mastg_tests"], [])

    def test_mastg_tests_index_overrides_existing(self):
        from extract_masvs_sections import compose_frontmatter

        parsed = {
            "control_id": "MASVS-STORAGE-1",
            "group": "MASVS-STORAGE",
            "summary": "...",
            "description": "...",
        }
        existing = {"mastg_tests": ["MASTG-TEST-OLD"]}
        index = {"MASVS-STORAGE-1": ["MASTG-TEST-NEW"]}
        fm = compose_frontmatter(parsed, existing=existing, mastg_index=index)
        self.assertEqual(fm["mastg_tests"], ["MASTG-TEST-NEW"])

    def test_mastg_tests_preserves_existing_when_index_absent(self):
        from extract_masvs_sections import compose_frontmatter

        parsed = {
            "control_id": "MASVS-STORAGE-1",
            "group": "MASVS-STORAGE",
            "summary": "...",
            "description": "...",
        }
        existing = {"mastg_tests": ["MASTG-TEST-PRESERVED"]}
        fm = compose_frontmatter(parsed, existing=existing, mastg_index=None)
        self.assertEqual(fm["mastg_tests"], ["MASTG-TEST-PRESERVED"])


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
            "mastg_tests": [],
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


class TestRoundTrip(unittest.TestCase):
    def test_read_existing_frontmatter(self):
        import tempfile
        from extract_masvs_sections import read_existing_frontmatter

        sample = (
            "---\n"
            "title: \"OLD title\"\n"
            "masvs_group: MASVS-STORAGE\n"
            "masvs_control: MASVS-STORAGE-1\n"
            "summary: \"OLD summary\"\n"
            "mastg_tests:\n"
            "  - MASTG-TEST-0001\n"
            "---\n\n"
            "# MASVS-STORAGE-1\n"
        )
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
            f.write(sample)
            path = Path(f.name)
        try:
            existing = read_existing_frontmatter(path)
            self.assertEqual(existing["mastg_tests"], ["MASTG-TEST-0001"])
        finally:
            path.unlink()

    def test_read_existing_returns_none_when_file_missing(self):
        from extract_masvs_sections import read_existing_frontmatter

        self.assertIsNone(read_existing_frontmatter(Path("/nonexistent/path.md")))

    def test_full_round_trip_preserves_enrichment(self):
        """Write file, then re-render with same upstream — mastg_tests preserved without index."""
        import tempfile
        from extract_masvs_sections import (
            compose_frontmatter,
            parse_upstream_control,
            read_existing_frontmatter,
            render_output,
        )

        raw_v1 = (
            "# MASVS-STORAGE-1\n\n"
            "## Control\n\nOriginal summary.\n\n"
            "## Description\n\nOriginal description.\n"
        )
        raw_v2 = (
            "# MASVS-STORAGE-1\n\n"
            "## Control\n\nUpdated summary in v2.\n\n"
            "## Description\n\nUpdated description in v2.\n"
        )

        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
            path = Path(f.name)
        try:
            parsed = parse_upstream_control(raw_v1)
            fm = compose_frontmatter(parsed, existing=None)
            fm["mastg_tests"] = ["MASTG-TEST-0200"]
            path.write_text(render_output(fm, parsed))

            existing = read_existing_frontmatter(path)
            parsed2 = parse_upstream_control(raw_v2)
            fm2 = compose_frontmatter(parsed2, existing=existing, mastg_index=None)

            self.assertEqual(fm2["summary"], "Updated summary in v2.")
            self.assertEqual(fm2["title"], "MASVS-STORAGE-1: Updated summary in v2.")
            self.assertEqual(fm2["mastg_tests"], ["MASTG-TEST-0200"])
        finally:
            path.unlink()


class TestExtractAll(unittest.TestCase):
    def test_processes_multiple_upstream_files(self):
        import tempfile
        from extract_masvs_sections import extract_all

        with tempfile.TemporaryDirectory() as src, tempfile.TemporaryDirectory() as dst:
            src_dir, dst_dir = Path(src), Path(dst)
            (src_dir / "MASVS-AUTH-1.md").write_text(
                "# MASVS-AUTH-1\n\n## Control\n\nA.\n\n## Description\n\nB.\n"
            )
            (src_dir / "MASVS-STORAGE-1.md").write_text(
                "# MASVS-STORAGE-1\n\n## Control\n\nC.\n\n## Description\n\nD.\n"
            )
            (src_dir / "README.md").write_text("not a control")  # should be ignored
            written = extract_all(src_dir, dst_dir)
            self.assertEqual(len(written), 2)
            self.assertTrue((dst_dir / "MASVS-AUTH-1.md").exists())
            self.assertTrue((dst_dir / "MASVS-STORAGE-1.md").exists())
            self.assertFalse((dst_dir / "README.md").exists())


if __name__ == "__main__":
    unittest.main()
