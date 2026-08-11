# MASVS v2.1.0 Reference Data

24 structured MASVS control files (8 groups, 24 controls) sourced from [OWASP MASVS](https://github.com/OWASP/masvs) at tag `v2.1.0`.

## Source & License

These files are derived from `controls/MASVS-*.md` in the upstream `OWASP/masvs` repository at tag `v2.1.0`. OWASP MASVS is licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).

## File Format

Each control file has lean YAML frontmatter:

```yaml
---
title: "MASVS-STORAGE-1: Sensitive data is stored securely."
masvs_group: "MASVS-STORAGE"
masvs_control: "MASVS-STORAGE-1"
summary: "Sensitive data is stored securely."
mastg_tests:                          # derived from the sibling mastg/ dir — not hand-authored
  - MASTG-TEST-0200
  - MASTG-TEST-0201
---
```

The body preserves the upstream `# MASVS-X-N` / `## Control` / `## Description` content verbatim.

No enrichment fields are stored on the MASVS side. Threat context, verification recipes, and per-platform grep hints live in the linked MASTG test files (sibling `mastg/` directory). Caveats for RESILIENCE (static-only) and PRIVACY-2/3 (runtime data-flow required) live in `plays/mobile-code-review.md` as play rules, not as frontmatter flags.

## Re-extraction Rule

`scripts/extract_masvs_sections.py` regenerates the upstream-derived keys (`title`, `masvs_group`, `masvs_control`, `summary`) plus the body verbatim from `OWASP/masvs` at the pinned tag. `mastg_tests:` is regenerated from a scan of the sibling `mastg/` directory for each control file's `covers_masvs:` matches — so updating MASTG data automatically refreshes the MASVS reverse index on the next MASVS extraction.

## Usage in Skills

The `mobile-code-review` skill walks the 8 MASVS groups in priority order. For each group, the skill loads the group overview (e.g. `MASVS-STORAGE.md`) and the individual controls (e.g. `MASVS-STORAGE-1.md`), then resolves each control's `mastg_tests:` IDs against the sibling `mastg/` directory to pick up grep hints, verification recipes, and threat context.

## Group Index

| Group | Controls | Coverage |
|---|---|---|
| MASVS-STORAGE | 2 | Full static |
| MASVS-CRYPTO | 2 | Full static |
| MASVS-AUTH | 3 | Full static |
| MASVS-NETWORK | 2 | Full static |
| MASVS-PLATFORM | 3 | Full static |
| MASVS-CODE | 4 | Full static |
| MASVS-RESILIENCE | 4 | Static signals only — runtime verification required |
| MASVS-PRIVACY | 4 | Partial — some controls need runtime data-flow |

## Updating

To refresh from upstream (requires PyYAML — install once via `pip install -r scripts/requirements.txt`):

```bash
rm -rf /tmp/masvs-upstream && mkdir -p /tmp/masvs-upstream
curl -sL https://github.com/OWASP/masvs/archive/refs/tags/v2.1.0.tar.gz | \
    tar xz -C /tmp/masvs-upstream --strip-components=1
python3 scripts/extract_masvs_sections.py /tmp/masvs-upstream/controls data/masvs data/mastg
```

(The third positional arg points at the MASTG directory and is what enables the reverse-index derivation.)
