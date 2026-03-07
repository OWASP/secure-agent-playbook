#!/usr/bin/env python3
"""
Extract AISVS section markdown from a single source file into a subdirectory.

Splits on ## Cx.x section headers (e.g. C1.1, C2.3) and writes each section
to <section_id>.md in the destination directory. Use for turning multi-section
AISVS source docs into one file per section under data/aisvs/.
"""

import re
import sys
from pathlib import Path


# Match ## C1.1 Title or ## 10.1 Title (TODO: fix this mismatch in upstream AISVS markdown)
SECTION_HEADER_RE = re.compile(r"^## (C?\d+\.\d+)\s+(.+)$", re.MULTILINE)


def _normalize_section_id(raw: str) -> str:
    """Ensure section ID is Cx.x (e.g. 10.1 -> C10.1)."""
    return raw if raw.startswith("C") else f"C{raw}"


def find_sections(content: str) -> list[tuple[str, str, str]]:
    """
    Parse markdown content into (section_id, title, body) tuples.
    Includes ## Cx.x or ## x.x (e.g. C1.1, 10.1). Output IDs are normalized to Cx.x.
    """
    sections: list[tuple[str, str, str]] = []
    pos = 0
    while True:
        match = SECTION_HEADER_RE.search(content, pos)
        if not match:
            break
        raw_id = match.group(1)
        section_id = _normalize_section_id(raw_id)
        title = match.group(2).strip()
        start = match.start()
        # Next section starts at next ## Cx.x or end of file
        next_match = SECTION_HEADER_RE.search(content, match.end())
        end = next_match.start() if next_match else len(content)
        body = content[start:end].strip()
        # Skip "References" or other non-Cx.x; we already only match Cx.x
        sections.append((section_id, title, body))
        pos = match.end()
    return sections


def extract(source_path: Path, dest_dir: Path) -> list[Path]:
    """
    Read source_path (single .md file), extract Cx.x sections, write each to dest_dir.
    Returns paths of written files.
    """
    if not source_path.is_file():
        raise FileNotFoundError(f"Not a file: {source_path}")
    text = source_path.read_text(encoding="utf-8")
    sections = find_sections(text)
    dest_dir = Path(dest_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for section_id, title, body in sections:
        out_path = dest_dir / f"{section_id}.md"
        out_path.write_text(body, encoding="utf-8")
        written.append(out_path)
    return written


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: extract_aisvs_sections.py <source.md> [dest_dir]", file=sys.stdout)
        print("  source.md  Path to AISVS source markdown (single file with ## Cx.x sections).", file=sys.stdout)
        print("  dest_dir   Output directory (default: data/aisvs).", file=sys.stdout)
        sys.exit(1)
    source = Path(sys.argv[1]).resolve()
    dest = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else Path("data/aisvs").resolve()
    try:
        paths = extract(source, dest)
        for p in paths:
            print(p)
        print(f"Wrote {len(paths)} section(s) to {dest}", file=sys.stderr)
    except FileNotFoundError as e:
        print(e, file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
