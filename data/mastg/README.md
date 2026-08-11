# MASTG Reference Data

Per-test markdown files extracted from [OWASP MASTG](https://github.com/OWASP/mastg) — the Mobile Application Security Testing Guide.

## Source & License

These files are derived from `tests/` (V1) and `tests-beta/` (V2) in the upstream `OWASP/mastg` repository at the pinned commit (recorded in `upstream_tag:` in each file's frontmatter). OWASP MASTG is licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).

## V1 vs V2 selection rule

For each MASVS v2 control, the extractor resolves the relevant MASTG tests using the V1 markdown as the translation layer:

| Upstream state | Result |
|---|---|
| V1 test `status: deprecated`, `covered_by: [V2 ids]` | Extract the V2 successor(s) from `tests-beta/` with `upstream_version: v2` |
| V1 test `status: deprecated`, `covered_by: []` | Extract the V1 test with `upstream_version: v1-fallback` and a `status_note` warning that no V2 successor exists yet |
| V1 test `status: active` (rare) | Extract the V1 test with `upstream_version: v1` |
| MASVS-PRIVACY-* (no V1 predecessor) | Walk `tests-beta/{android,ios}/MASVS-PRIVACY/` and attach to the PRIVACY group via directory path |

## File Format

```yaml
---
id: MASTG-TEST-0200
title: Files Written to External Storage
upstream_version: v2                                          # or "v1" or "v1-fallback"
upstream_path: tests-beta/android/MASVS-STORAGE/MASTG-TEST-0200.md
upstream_tag: <commit-sha-or-tag>
platform: android
type: [dynamic]                                               # v2 only
weakness: MASWE-0007                                          # v2 only
profiles: [L1, L2]                                            # v2 only
covers_masvs: [MASVS-STORAGE-1]                               # join key into the sibling masvs/ dir
# For v1-fallback files only:
# status_note: "V1 test; no V2 successor authored upstream yet — content may be outdated"
# masvs_v1_id: [MSTG-STORAGE-1]
# masvs_v2_id: [MASVS-STORAGE-1]
---

## Overview
<verbatim from upstream>

## Static Analysis     (V1) — or Steps / Observation / Evaluation (V2)
<verbatim from upstream>

## Dynamic Analysis    (V1 only)
<verbatim from upstream>
```

## Re-extraction

Requires PyYAML — install once via `pip install -r scripts/requirements.txt`.

```bash
rm -rf /tmp/mastg-upstream && mkdir -p /tmp/mastg-upstream
curl -sL https://github.com/OWASP/mastg/archive/refs/heads/master.tar.gz | \
    tar xz -C /tmp/mastg-upstream --strip-components=1
TAG=$(gh api repos/OWASP/mastg/commits/master --jq .sha | head -c 7)
python3 scripts/extract_mastg_sections.py /tmp/mastg-upstream data/mastg "$TAG"
```

After re-running the MASTG extractor, also re-run the MASVS extractor so its `mastg_tests:` reverse indices stay in sync:

```bash
python3 scripts/extract_masvs_sections.py /tmp/masvs-upstream/controls data/masvs data/mastg
```

## Pinned Upstream

Current pin: see any file's `upstream_tag:` field. Update by re-running the extraction commands above against a new commit; commit the regenerated files.

## How the sibling `masvs/` dir references this

Each `MASVS-X-N.md` in the sibling `masvs/` directory has a `mastg_tests:` list with the IDs of MASTG tests that cover that control. The list is derived (the MASVS extractor scans this directory for `covers_masvs:` matches), so it stays consistent automatically.
