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
import sys
from pathlib import Path

UPSTREAM_KEYS = ("title", "masvs_group", "masvs_control", "summary")
CONTROL_ID_RE = re.compile(r"^# (MASVS-[A-Z]+-\d+)\s*$", re.MULTILINE)


def parse_upstream_control(raw: str) -> dict:
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
        return raw[start:end].strip()

    summary = _between("## Control", "## Description")
    description = _between("## Description", None)
    return {
        "control_id": control_id,
        "group": group,
        "summary": summary,
        "description": description,
    }
