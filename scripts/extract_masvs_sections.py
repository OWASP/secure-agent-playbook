#!/usr/bin/env python3
"""
Extract OWASP MASVS v2.1.0 controls from upstream (OWASP/masvs, controls/MASVS-*.md)
into per-control markdown files with YAML frontmatter under data/masvs/.

Upstream layout per file:
    # MASVS-AUTH-1
    ## Control
    <one-line statement>
    ## Description
    <body>

Output layout per file (data/masvs/MASVS-AUTH-1.md):
    ---
    title: "MASVS-AUTH-1: <statement>"
    masvs_group: "MASVS-AUTH"
    masvs_control: "MASVS-AUTH-1"
    summary: "<statement>"
    platforms: [android, ios]            # repo enrichment (preserved on re-run)
    when_to_use: [...]                   # repo enrichment (preserved on re-run)
    threats: [...]                       # repo enrichment (preserved on re-run)
    mastg_tests: [...]                   # repo enrichment (preserved on re-run)
    static_signals: {...}                # repo enrichment (preserved on re-run)
    resilience_static_only: bool         # repo enrichment (preserved on re-run)
    static_only: bool                    # repo enrichment (preserved on re-run)
    ---

    # MASVS-AUTH-1
    ## Control
    ...
    ## Description
    ...

Re-extraction rule: only the five UPSTREAM_KEYS get overwritten from upstream (the
four upstream-derived keys plus the group-derived `resilience_static_only`); every
other frontmatter key is preserved verbatim.

Usage:
    extract_masvs_sections.py <upstream-controls-dir> [<output-dir>]
"""

import re
import sys
from pathlib import Path

UPSTREAM_KEYS = ("title", "masvs_group", "masvs_control", "summary", "resilience_static_only")
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
    """Return default frontmatter from a parsed control."""
    return {
        "title": f"{parsed['control_id']}: {parsed['summary']}",
        "masvs_group": parsed["group"],
        "masvs_control": parsed["control_id"],
        "summary": parsed["summary"],
        "platforms": ["android", "ios"],
        "when_to_use": [],
        "threats": [],
        "mastg_tests": [],
        "static_signals": {"android": [], "ios": []},
        "resilience_static_only": parsed["group"] == "MASVS-RESILIENCE",
        "static_only": False,
    }


def compose_frontmatter(parsed: dict[str, str], existing: dict | None) -> dict:
    """
    Build the output frontmatter. Upstream-derived keys come from `parsed`;
    every other key is preserved verbatim from `existing` (if present), else defaulted.
    """
    fm = _default_frontmatter(parsed)
    if existing is not None:
        for key, value in existing.items():
            if key in UPSTREAM_KEYS:
                continue  # always overwrite from upstream
            fm[key] = value
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


def extract_all(source_dir: Path, dest_dir: Path) -> list[Path]:
    """Process every controls/MASVS-*.md in source_dir, writing to dest_dir."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for src in sorted(source_dir.glob("MASVS-*.md")):
        raw = src.read_text(encoding="utf-8")
        parsed = parse_upstream_control(raw)
        out_path = dest_dir / f"{parsed['control_id']}.md"
        existing = read_existing_frontmatter(out_path)
        fm = compose_frontmatter(parsed, existing=existing)
        out_path.write_text(render_output(fm, parsed), encoding="utf-8")
        written.append(out_path)
    return written


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: extract_masvs_sections.py <upstream-controls-dir> [<output-dir>]", file=sys.stderr)
        print("  upstream-controls-dir  Path to OWASP/masvs controls/ at the pinned tag", file=sys.stderr)
        print("  output-dir             Output (default: data/masvs)", file=sys.stderr)
        sys.exit(1)
    source = Path(sys.argv[1]).resolve()
    if not source.is_dir():
        print(f"error: source not found: {source}", file=sys.stderr)
        sys.exit(2)
    dest = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else Path("data/masvs").resolve()
    written = extract_all(source, dest)
    for p in written:
        print(p)
    print(f"Wrote {len(written)} control file(s) to {dest}", file=sys.stderr)


if __name__ == "__main__":
    main()
