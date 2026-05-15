# MASVS v2.1.0 Reference Data

24 structured MASVS control files (8 groups, 24 controls) sourced from [OWASP MASVS](https://github.com/OWASP/masvs) at tag `v2.1.0`.

## Source & License

These files are derived from `controls/MASVS-*.md` in the upstream `OWASP/masvs` repository at tag `v2.1.0`. OWASP MASVS is licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). The hand-authored enrichment in this directory (`when_to_use`, `threats`, `mastg_tests`, `static_signals`, `resilience_static_only`, `static_only`) is contributed under the same license.

## File Format

Each control file has YAML frontmatter:

```yaml
---
title: "MASVS-STORAGE-1: Sensitive data is stored securely."
masvs_group: "MASVS-STORAGE"
masvs_control: "MASVS-STORAGE-1"
summary: "Sensitive data is stored securely."
platforms: [android, ios]
when_to_use:                          # task-matching triggers
  - reviewing how the app persists user credentials, tokens, or PII
threats:                              # relevant threat categories
  - sensitive data extraction from device backups
mastg_tests:                          # forward refs to OWASP MASTG (IDs only)
  - MASTG-TEST-0001
static_signals:                       # per-platform grep hints
  android:
    - "SharedPreferences without EncryptedSharedPreferences"
  ios:
    - "Keychain access flags"
resilience_static_only: false         # true for every MASVS-RESILIENCE-* control
static_only: false                    # true for PRIVACY controls needing runtime data-flow
---
```

The body preserves the upstream `# MASVS-X-N` / `## Control` / `## Description` content verbatim.

## Re-extraction Rule

`scripts/extract_masvs_sections.py` regenerates the upstream-derived keys (`title`, `masvs_group`, `masvs_control`, `summary`) and the group-derived key (`resilience_static_only`), plus the body. Every other frontmatter key is preserved verbatim across re-runs, so hand-authored enrichment survives upstream pulls.

## Usage in Skills

The `mobile-code-review` skill walks the 8 MASVS groups in priority order. For each group, the skill loads the group overview (e.g. `MASVS-STORAGE.md`, added by the Task 6 hand-authoring step) and the individual controls (e.g. `MASVS-STORAGE-1.md`), using `static_signals` as grep hints and `mastg_tests` as forward references for runtime follow-up.

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

To refresh from upstream:

```bash
rm -rf /tmp/masvs-upstream
mkdir -p /tmp/masvs-upstream
curl -sL https://github.com/OWASP/masvs/archive/refs/tags/v2.1.0.tar.gz | tar xz -C /tmp/masvs-upstream --strip-components=1
python3 scripts/extract_masvs_sections.py /tmp/masvs-upstream/controls data/masvs
```

Enrichment is preserved automatically.
