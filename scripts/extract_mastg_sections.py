#!/usr/bin/env python3
"""
Extract OWASP MASTG tests (V2 preferred via V1 deprecation chain, V1 fallback
with notice otherwise) into per-test markdown files under data/mastg/.

V1 translation rule:
  For each MASVS control X:
    - Walk every V1 test in tests/**/*.md whose masvs_v2_id contains X.
    - If V1 test is deprecated AND covered_by is non-empty:
        -> Extract each V2 successor in covered_by from tests-beta/.
    - If V1 test is deprecated AND covered_by is empty:
        -> Extract V1 with upstream_version: v1-fallback + status_note.
    - If V1 test is active:
        -> Extract V1 as upstream_version: v1.

PRIVACY directory fallback:
  V1 predated PRIVACY, so no V1 tests declare masvs_v2_id: MASVS-PRIVACY-*.
  For PRIVACY: walk tests-beta/{android,ios}/MASVS-PRIVACY/ and attach
  those tests with covers_masvs: [<PRIVACY group only -- no per-control>].

Usage:
    extract_mastg_sections.py <upstream-mastg-root> [<output-dir>]
"""
import re
import sys
from pathlib import Path

import yaml

FRONTMATTER_RE = re.compile(r"\A---\n(.+?)\n---\n", re.DOTALL)
TEST_ID_RE = re.compile(r"(MASTG-TEST-\d+)")

OUTPUT_KEYS_V1 = ("id", "title", "upstream_version", "upstream_path",
                  "upstream_tag", "platform", "covers_masvs",
                  "masvs_v1_id", "masvs_v2_id", "status_note")
OUTPUT_KEYS_V2 = ("id", "title", "upstream_version", "upstream_path",
                  "upstream_tag", "platform", "type", "weakness",
                  "profiles", "covers_masvs")


def parse_test_frontmatter(raw: str) -> tuple[dict, str]:
    """Parse a MASTG test markdown file into (frontmatter_dict, body_string)."""
    m = FRONTMATTER_RE.match(raw)
    if not m:
        return {}, raw
    fm = yaml.safe_load(m.group(1)) or {}
    body = raw[m.end():]
    return fm, body


def classify_test(test_id: str, fm: dict) -> dict:
    """Return classification: which action to take for this V1 test."""
    status = fm.get("status", "active")
    covered_by = fm.get("covered_by") or []
    if status == "deprecated" and covered_by:
        return {"action": "use_v2_successors", "successor_ids": list(covered_by)}
    if status == "deprecated" and not covered_by:
        return {"action": "use_v1_fallback", "test_id": test_id}
    return {"action": "use_v1", "test_id": test_id}


def resolve_masvs_to_tests(masvs_control: str,
                            v1_tests: dict,
                            v2_tests: dict) -> list[dict]:
    """For one MASVS control, return the list of test records to extract.

    Each record is {"id": ..., "upstream_version": ..., "fm": ..., "predecessor": ...}.
    """
    out: list[dict] = []
    seen: set[str] = set()

    for v1_id, fm in v1_tests.items():
        if masvs_control not in (fm.get("masvs_v2_id") or []):
            continue
        cls = classify_test(v1_id, fm)
        if cls["action"] == "use_v2_successors":
            for succ_id in cls["successor_ids"]:
                if succ_id in seen:
                    continue
                if succ_id not in v2_tests:
                    # Successor declared but not present upstream -- skip with warning
                    print(f"WARN: V1 {v1_id} cites successor {succ_id} not found in tests-beta/",
                          file=sys.stderr)
                    continue
                seen.add(succ_id)
                out.append({
                    "id": succ_id,
                    "upstream_version": "v2",
                    "fm": v2_tests[succ_id],
                    "predecessor": v1_id,
                })
        elif cls["action"] == "use_v1_fallback":
            if v1_id in seen:
                continue
            seen.add(v1_id)
            out.append({
                "id": v1_id,
                "upstream_version": "v1-fallback",
                "fm": fm,
                "predecessor": None,
            })
        elif cls["action"] == "use_v1":
            if v1_id in seen:
                continue
            seen.add(v1_id)
            out.append({
                "id": v1_id,
                "upstream_version": "v1",
                "fm": fm,
                "predecessor": None,
            })

    # Sort for idempotency
    out.sort(key=lambda r: r["id"])
    return out


def build_output_frontmatter(*, test_id: str,
                              upstream_fm: dict,
                              upstream_path: str,
                              upstream_tag: str,
                              upstream_version: str,
                              covers_masvs: list[str]) -> dict:
    """Build the canonical output frontmatter dict for a single MASTG test."""
    fm: dict = {
        "id": test_id,
        "title": upstream_fm.get("title", ""),
        "upstream_version": upstream_version,
        "upstream_path": upstream_path,
        "upstream_tag": upstream_tag,
        "platform": upstream_fm.get("platform"),
        "covers_masvs": sorted(covers_masvs),
    }
    if upstream_version == "v2":
        if "type" in upstream_fm:
            fm["type"] = upstream_fm["type"]
        if "weakness" in upstream_fm:
            fm["weakness"] = upstream_fm["weakness"]
        if "profiles" in upstream_fm:
            fm["profiles"] = upstream_fm["profiles"]
    else:
        # v1 or v1-fallback: carry the v1 mapping fields
        if "masvs_v1_id" in upstream_fm:
            fm["masvs_v1_id"] = upstream_fm["masvs_v1_id"]
        if "masvs_v2_id" in upstream_fm:
            fm["masvs_v2_id"] = upstream_fm["masvs_v2_id"]
        if upstream_version == "v1-fallback":
            fm["status_note"] = "V1 test; no V2 successor authored upstream yet — content may be outdated"
    return fm


def walk_v1_tests(mastg_root: Path) -> dict[str, dict]:
    """Walk upstream tests/**/*.md -> {MASTG-TEST-ID: frontmatter_dict}."""
    tests: dict[str, dict] = {}
    for p in sorted((mastg_root / "tests").rglob("*.md")):
        if p.name == "index.md":
            continue
        m = TEST_ID_RE.search(p.name)
        if not m:
            continue
        raw = p.read_text(encoding="utf-8")
        fm, _ = parse_test_frontmatter(raw)
        tests[m.group(1)] = fm
    return tests


def walk_v2_tests(mastg_root: Path) -> dict[str, dict]:
    """Walk upstream tests-beta/**/*.md -> {MASTG-TEST-ID: frontmatter_dict}."""
    tests: dict[str, dict] = {}
    for p in sorted((mastg_root / "tests-beta").rglob("*.md")):
        if p.name == "index.md":
            continue
        m = TEST_ID_RE.search(p.name)
        if not m:
            continue
        raw = p.read_text(encoding="utf-8")
        fm, _ = parse_test_frontmatter(raw)
        if "id" not in fm:
            fm["id"] = m.group(1)
        tests[m.group(1)] = fm
    return tests


def get_v1_path(mastg_root: Path, test_id: str) -> Path | None:
    matches = list((mastg_root / "tests").rglob(f"{test_id}.md"))
    return matches[0] if matches else None


def get_v2_path(mastg_root: Path, test_id: str) -> Path | None:
    matches = list((mastg_root / "tests-beta").rglob(f"{test_id}.md"))
    return matches[0] if matches else None


def render_output_file(record: dict, mastg_root: Path, upstream_tag: str,
                       covers_masvs: list[str]) -> tuple[str, str]:
    """Return (filename, file_content) for one extracted test."""
    test_id = record["id"]
    version = record["upstream_version"]
    if version == "v2":
        src = get_v2_path(mastg_root, test_id)
    else:
        src = get_v1_path(mastg_root, test_id)
    if src is None:
        raise FileNotFoundError(f"{test_id} not found in upstream for version={version}")

    raw = src.read_text(encoding="utf-8")
    _, body = parse_test_frontmatter(raw)
    rel_path = src.relative_to(mastg_root).as_posix()

    fm = build_output_frontmatter(
        test_id=test_id,
        upstream_fm=record["fm"],
        upstream_path=rel_path,
        upstream_tag=upstream_tag,
        upstream_version=version,
        covers_masvs=covers_masvs,
    )
    yaml_text = yaml.safe_dump(fm, sort_keys=False, allow_unicode=True)
    return f"{test_id}.md", f"---\n{yaml_text}---\n{body}"


def collect_privacy_v2_tests(mastg_root: Path,
                              v2_tests: dict[str, dict]) -> dict[str, list[str]]:
    """For MASVS-PRIVACY group fallback: find V2 tests under tests-beta/*/MASVS-PRIVACY/.

    Returns {test_id: [list of MASVS-PRIVACY group strings -- typically just ['MASVS-PRIVACY']]}
    so the caller can attach them to PRIVACY at group level.
    """
    privacy_tests: dict[str, list[str]] = {}
    for test_id, fm in v2_tests.items():
        path = get_v2_path(mastg_root, test_id)
        if path and "/MASVS-PRIVACY/" in path.as_posix():
            privacy_tests[test_id] = ["MASVS-PRIVACY"]
    return privacy_tests


def extract_all(mastg_root: Path, dest_dir: Path, upstream_tag: str) -> dict[str, list[str]]:
    """Run the full extraction. Returns {MASVS-control-id: [test_id, ...]} reverse index."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    v1_tests = walk_v1_tests(mastg_root)
    v2_tests = walk_v2_tests(mastg_root)

    # Discover MASVS controls referenced anywhere in V1 masvs_v2_id frontmatter
    masvs_controls: set[str] = set()
    for fm in v1_tests.values():
        for ctrl in fm.get("masvs_v2_id") or []:
            masvs_controls.add(ctrl)

    written: dict[str, dict] = {}  # test_id -> resolved record dict
    reverse_index: dict[str, list[str]] = {}

    for ctrl in sorted(masvs_controls):
        records = resolve_masvs_to_tests(ctrl, v1_tests, v2_tests)
        for rec in records:
            reverse_index.setdefault(ctrl, []).append(rec["id"])
            if rec["id"] in written:
                # Test already resolved for another control -- skip re-storing the record
                continue
            written[rec["id"]] = rec

    # Pass 2: accumulate covers_masvs across all controls before writing
    test_covers: dict[str, set[str]] = {}
    for ctrl in sorted(masvs_controls):
        for rec in resolve_masvs_to_tests(ctrl, v1_tests, v2_tests):
            test_covers.setdefault(rec["id"], set()).add(ctrl)

    # PRIVACY directory fallback (V1 has no PRIVACY tests)
    privacy_tests = collect_privacy_v2_tests(mastg_root, v2_tests)
    for tid, groups in privacy_tests.items():
        test_covers.setdefault(tid, set()).update(groups)
        reverse_index.setdefault("MASVS-PRIVACY", []).append(tid)

    # Write each test once with the union of its MASVS controls
    for tid, rec in written.items():
        covers = sorted(test_covers.get(tid, set()))
        filename, content = render_output_file(rec, mastg_root, upstream_tag, covers)
        (dest_dir / filename).write_text(content, encoding="utf-8")

    # Also write PRIVACY-fallback V2 tests if not already written
    for tid in privacy_tests:
        if tid in written:
            continue
        # Build a synthetic v2 record
        rec = {"id": tid, "upstream_version": "v2", "fm": v2_tests[tid], "predecessor": None}
        covers = sorted(test_covers.get(tid, set()))
        filename, content = render_output_file(rec, mastg_root, upstream_tag, covers)
        (dest_dir / filename).write_text(content, encoding="utf-8")

    # Deduplicate and sort the reverse index
    for ctrl in reverse_index:
        reverse_index[ctrl] = sorted(set(reverse_index[ctrl]))
    return reverse_index


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: extract_mastg_sections.py <upstream-mastg-root> [<output-dir>] [<upstream-tag>]",
              file=sys.stderr)
        sys.exit(1)
    mastg_root = Path(sys.argv[1]).resolve()
    dest_dir = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else Path("data/mastg").resolve()
    upstream_tag = sys.argv[3] if len(sys.argv) > 3 else "master"
    reverse_index = extract_all(mastg_root, dest_dir, upstream_tag)
    n_files = len(list(dest_dir.glob("MASTG-TEST-*.md")))
    print(f"Wrote {n_files} test file(s) to {dest_dir}", file=sys.stderr)
    print(f"Reverse index covers {len(reverse_index)} MASVS controls/groups", file=sys.stderr)


if __name__ == "__main__":
    main()
