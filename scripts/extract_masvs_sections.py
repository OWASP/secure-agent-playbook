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

Re-extraction rule: only the four UPSTREAM_KEYS get overwritten from upstream;
all other frontmatter keys are preserved verbatim.

Usage:
    extract_masvs_sections.py <upstream-controls-dir> [<output-dir>]
"""

import re

UPSTREAM_KEYS = ("title", "masvs_group", "masvs_control", "summary")
CONTROL_ID_RE = re.compile(r"^# (MASVS-[A-Z]+-\d+)\s*$", re.MULTILINE)


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
    if existing:
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
