#!/usr/bin/env python3
"""
Extract OWASP MASVS v2.1.0 controls from upstream (OWASP/masvs, controls/MASVS-*.md)
into per-control markdown files with YAML frontmatter under
plugins/code-security-skills/data/masvs/.

Upstream layout per file:
    # MASVS-AUTH-1
    ## Control
    <one-line statement>
    ## Description
    <body>

Output layout per file (plugins/code-security-skills/data/masvs/MASVS-AUTH-1.md):
    ---
    title: "MASVS-AUTH-1: <statement>"
    masvs_group: "MASVS-AUTH"
    masvs_control: "MASVS-AUTH-1"
    summary: "<statement>"
    mastg_tests: [...]                # derived from data/mastg/ covers_masvs
    ---

    # MASVS-AUTH-1
    ## Control
    ...
    ## Description
    ...

Re-extraction rule: UPSTREAM_KEYS (title, masvs_group, masvs_control, summary)
plus the body come from upstream verbatim. `mastg_tests:` is derived by scanning
data/mastg/ for `covers_masvs:` matches. The schema is lean — no enrichment
fields (no when_to_use, threats, static_signals, coverage, platforms); those
moved to play rules / MASTG content.

Usage:
    extract_masvs_sections.py <upstream-controls-dir> [<output-dir>] [<mastg-dir>]
"""

import re
import sys
from pathlib import Path

UPSTREAM_KEYS = ("title", "masvs_group", "masvs_control", "summary")
CONTROL_ID_RE = re.compile(r"^# (MASVS-[A-Z]+-\d+)\s*$", re.MULTILINE)
FRONTMATTER_RE = re.compile(r"\A---\n(.+?)\n---\n", re.DOTALL)


def parse_upstream_control(raw: str) -> dict[str, str]:
    """Parse one upstream MASVS control .md into {control_id, group, summary, description}."""
    m = CONTROL_ID_RE.search(raw)
    if not m:
        raise ValueError("missing '# MASVS-X-N' heading")
    control_id = m.group(1)
    group = "-".join(control_id.split("-")[:2])

    def _between(start_marker: str, end_marker: str | None) -> str:
        start = raw.find(start_marker)
        if start < 0:
            raise ValueError(f"missing section {start_marker!r}")
        start += len(start_marker)
        end = raw.find(end_marker, start) if end_marker else len(raw)
        if end_marker and end < 0:
            raise ValueError(f"missing section {end_marker!r}")
        return raw[start:end].strip()

    summary = _between("## Control", "## Description")
    description = _between("## Description", None)
    return {
        "control_id": control_id,
        "group": group,
        "summary": summary,
        "description": description,
    }


def _default_frontmatter(parsed: dict[str, str]) -> dict:
    """Return default frontmatter from a parsed control. Minimal schema."""
    return {
        "title": f"{parsed['control_id']}: {parsed['summary']}",
        "masvs_group": parsed["group"],
        "masvs_control": parsed["control_id"],
        "summary": parsed["summary"],
        "mastg_tests": [],  # populated by scan of data/mastg/ in extract_all
    }


def _scan_mastg_dir(mastg_dir: Path) -> dict[str, list[str]]:
    """Walk data/mastg/*.md, return {MASVS-X-N: [MASTG-TEST-####, ...]}."""
    import yaml as _y
    index: dict[str, list[str]] = {}
    if not mastg_dir.is_dir():
        return index
    for p in sorted(mastg_dir.glob("MASTG-TEST-*.md")):
        text = p.read_text(encoding="utf-8")
        m = FRONTMATTER_RE.match(text)
        if not m:
            continue
        fm = _y.safe_load(m.group(1)) or {}
        test_id = fm.get("id") or p.stem
        for ctrl in fm.get("covers_masvs") or []:
            index.setdefault(ctrl, []).append(test_id)
    for ctrl in index:
        index[ctrl] = sorted(set(index[ctrl]))
    return index


def compose_frontmatter(parsed: dict[str, str],
                         existing: dict | None,
                         mastg_index: dict[str, list[str]] | None = None) -> dict:
    """
    Build the output frontmatter. UPSTREAM_KEYS come from `parsed`;
    `mastg_tests:` comes from the MASTG reverse index (overrides any existing value);
    other keys (legacy enrichment) are no longer carried — the schema is now lean.
    """
    fm = _default_frontmatter(parsed)
    # Overwrite mastg_tests from the reverse index if available
    if mastg_index is not None:
        fm["mastg_tests"] = mastg_index.get(parsed["control_id"], [])
    elif existing is not None and "mastg_tests" in existing:
        # No index provided — preserve existing as a fallback
        fm["mastg_tests"] = existing["mastg_tests"]
    return fm


def render_output(frontmatter: dict, parsed: dict[str, str]) -> str:
    """Render a full output file: YAML frontmatter + blank line + upstream body."""
    import yaml

    yaml_text = yaml.safe_dump(frontmatter, sort_keys=False, allow_unicode=True)
    body = (
        f"# {parsed['control_id']}\n\n"
        f"## Control\n\n{parsed['summary']}\n\n"
        f"## Description\n\n{parsed['description']}\n"
    )
    return f"---\n{yaml_text}---\n\n{body}"


def read_existing_frontmatter(path: Path) -> dict | None:
    """Return the YAML frontmatter dict of an existing output file, or None."""
    import yaml

    if not path.is_file():
        return None
    text = path.read_text(encoding="utf-8")
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None
    return yaml.safe_load(m.group(1))


def extract_all(source_dir: Path, dest_dir: Path,
                 mastg_dir: Path | None = None) -> list[Path]:
    """Process every controls/MASVS-*.md in source_dir, writing to dest_dir."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    mastg_index = _scan_mastg_dir(mastg_dir) if mastg_dir else None
    written: list[Path] = []
    for src in sorted(source_dir.glob("MASVS-*.md")):
        raw = src.read_text(encoding="utf-8")
        parsed = parse_upstream_control(raw)
        out_path = dest_dir / f"{parsed['control_id']}.md"
        existing = read_existing_frontmatter(out_path)
        fm = compose_frontmatter(parsed, existing=existing, mastg_index=mastg_index)
        out_path.write_text(render_output(fm, parsed), encoding="utf-8")
        written.append(out_path)
    return written


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: extract_masvs_sections.py <upstream-controls-dir> [<output-dir>] [<mastg-dir>]",
              file=sys.stderr)
        sys.exit(1)
    source = Path(sys.argv[1]).resolve()
    if not source.is_dir():
        print(f"error: source not found: {source}", file=sys.stderr)
        sys.exit(2)
    dest = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else Path("plugins/code-security-skills/data/masvs").resolve()
    mastg = Path(sys.argv[3]).resolve() if len(sys.argv) > 3 else Path("plugins/code-security-skills/data/mastg").resolve()
    written = extract_all(source, dest, mastg if mastg.is_dir() else None)
    for p in written:
        print(p)
    print(f"Wrote {len(written)} control file(s) to {dest}", file=sys.stderr)


if __name__ == "__main__":
    main()
