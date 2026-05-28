"""Tests for extract_mastg_sections.py — run via: python3 scripts/test_extract_mastg_sections.py -v"""
import sys
import textwrap
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from extract_mastg_sections import (
    parse_test_frontmatter,
    classify_test,
    resolve_masvs_to_tests,
    build_output_frontmatter,
)


class TestParseTestFrontmatter(unittest.TestCase):
    def test_parses_v1_test(self):
        raw = textwrap.dedent("""\
            ---
            masvs_v1_id:
            - MSTG-STORAGE-1
            - MSTG-STORAGE-2
            masvs_v2_id:
            - MASVS-STORAGE-1
            platform: android
            title: Testing Local Storage for Sensitive Data
            status: deprecated
            covered_by: [MASTG-TEST-0200, MASTG-TEST-0201]
            deprecation_note: New version available in MASTG V2
            ---

            ## Overview

            Body content here.
            """)
        fm, body = parse_test_frontmatter(raw)
        self.assertEqual(fm["masvs_v2_id"], ["MASVS-STORAGE-1"])
        self.assertEqual(fm["status"], "deprecated")
        self.assertEqual(fm["covered_by"], ["MASTG-TEST-0200", "MASTG-TEST-0201"])
        self.assertIn("Body content here", body)

    def test_parses_v2_test(self):
        raw = textwrap.dedent("""\
            ---
            platform: android
            title: Files Written to External Storage
            id: MASTG-TEST-0200
            type: [dynamic]
            weakness: MASWE-0007
            profiles: [L1, L2]
            ---

            ## Overview

            V2 body.
            """)
        fm, body = parse_test_frontmatter(raw)
        self.assertEqual(fm["id"], "MASTG-TEST-0200")
        self.assertEqual(fm["weakness"], "MASWE-0007")
        self.assertNotIn("masvs_v2_id", fm)


class TestClassifyTest(unittest.TestCase):
    def test_v1_deprecated_with_successors_returns_v2_ids(self):
        """V1 deprecated test with covered_by: yields V2 successor IDs to extract."""
        fm = {
            "status": "deprecated",
            "covered_by": ["MASTG-TEST-0200", "MASTG-TEST-0201"],
            "masvs_v2_id": ["MASVS-STORAGE-1"],
        }
        classification = classify_test("MASTG-TEST-0001", fm)
        self.assertEqual(classification["action"], "use_v2_successors")
        self.assertEqual(classification["successor_ids"], ["MASTG-TEST-0200", "MASTG-TEST-0201"])

    def test_v1_deprecated_without_successors_falls_back_to_v1(self):
        """V1 deprecated with empty covered_by: yields v1-fallback."""
        fm = {
            "status": "deprecated",
            "covered_by": [],
            "masvs_v2_id": ["MASVS-STORAGE-2"],
        }
        classification = classify_test("MASTG-TEST-0009", fm)
        self.assertEqual(classification["action"], "use_v1_fallback")
        self.assertEqual(classification["test_id"], "MASTG-TEST-0009")

    def test_v1_active_used_as_primary(self):
        """V1 not deprecated: extract V1 as primary."""
        fm = {
            "status": "active",
            "covered_by": [],
            "masvs_v2_id": ["MASVS-AUTH-1"],
        }
        classification = classify_test("MASTG-TEST-9999", fm)
        self.assertEqual(classification["action"], "use_v1")


class TestResolveMasvsToTests(unittest.TestCase):
    def test_resolves_v1_chain_to_v2_successors(self):
        """Walking V1 tests for MASVS-STORAGE-1 picks up V2 successors."""
        v1_tests = {
            "MASTG-TEST-0001": {
                "status": "deprecated",
                "covered_by": ["MASTG-TEST-0200", "MASTG-TEST-0201"],
                "masvs_v2_id": ["MASVS-STORAGE-1"],
            },
        }
        v2_tests = {
            "MASTG-TEST-0200": {"id": "MASTG-TEST-0200", "platform": "android"},
            "MASTG-TEST-0201": {"id": "MASTG-TEST-0201", "platform": "android"},
        }
        resolved = resolve_masvs_to_tests("MASVS-STORAGE-1", v1_tests, v2_tests)
        self.assertEqual(sorted(t["id"] for t in resolved),
                         ["MASTG-TEST-0200", "MASTG-TEST-0201"])
        for t in resolved:
            self.assertEqual(t["upstream_version"], "v2")

    def test_resolves_v1_fallback_when_no_successors(self):
        v1_tests = {
            "MASTG-TEST-0009": {
                "status": "deprecated",
                "covered_by": [],
                "masvs_v2_id": ["MASVS-STORAGE-2"],
            },
        }
        v2_tests = {}
        resolved = resolve_masvs_to_tests("MASVS-STORAGE-2", v1_tests, v2_tests)
        self.assertEqual(len(resolved), 1)
        self.assertEqual(resolved[0]["id"], "MASTG-TEST-0009")
        self.assertEqual(resolved[0]["upstream_version"], "v1-fallback")


class TestBuildOutputFrontmatter(unittest.TestCase):
    def test_v2_output_shape(self):
        upstream_fm = {
            "id": "MASTG-TEST-0200",
            "title": "Files Written to External Storage",
            "platform": "android",
            "type": ["dynamic"],
            "weakness": "MASWE-0007",
            "profiles": ["L1", "L2"],
        }
        fm = build_output_frontmatter(
            test_id="MASTG-TEST-0200",
            upstream_fm=upstream_fm,
            upstream_path="tests-beta/android/MASVS-STORAGE/MASTG-TEST-0200.md",
            upstream_tag="abc123",
            upstream_version="v2",
            covers_masvs=["MASVS-STORAGE-1"],
        )
        self.assertEqual(fm["id"], "MASTG-TEST-0200")
        self.assertEqual(fm["upstream_version"], "v2")
        self.assertEqual(fm["covers_masvs"], ["MASVS-STORAGE-1"])
        self.assertEqual(fm["upstream_tag"], "abc123")
        self.assertNotIn("status_note", fm)  # v2 has no status note

    def test_v1_fallback_output_includes_status_note(self):
        upstream_fm = {
            "title": "Testing Backups for Sensitive Data",
            "platform": "android",
            "masvs_v1_id": ["MSTG-STORAGE-1"],
            "masvs_v2_id": ["MASVS-STORAGE-2"],
            "status": "deprecated",
        }
        fm = build_output_frontmatter(
            test_id="MASTG-TEST-0009",
            upstream_fm=upstream_fm,
            upstream_path="tests/android/MASVS-STORAGE/MASTG-TEST-0009.md",
            upstream_tag="abc123",
            upstream_version="v1-fallback",
            covers_masvs=["MASVS-STORAGE-2"],
        )
        self.assertEqual(fm["upstream_version"], "v1-fallback")
        self.assertIn("status_note", fm)
        self.assertIn("no V2 successor", fm["status_note"])


if __name__ == "__main__":
    unittest.main()
