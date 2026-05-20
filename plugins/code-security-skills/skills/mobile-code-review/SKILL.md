---
name: mobile-code-review
description: Security-focused review of native Android and iOS mobile app source code against OWASP MASVS v2.1.0. Use when reviewing mobile codebases, mobile PR diffs, or auditing a mobile module.
license: CC-BY-4.0
---
 
# Mobile Security Code Review

Review native Android and iOS source code for security vulnerabilities by following the full procedure in `plays/mobile-code-review.md`.

## Steps

1. **Scope & Context** — Language (Java/Kotlin/Swift/Obj-C/Dart), platform, app type, sensitive data, exposure.
2. **Platform Detection** — Fingerprint Android (AndroidManifest.xml, build.gradle) and/or iOS (Info.plist, *.xcodeproj). If only a cross-platform shell is detected, declare partial coverage.
3. **Systematic Review by MASVS Group** — For each of the 8 MASVS groups (STORAGE, CRYPTO, AUTH, NETWORK, PLATFORM, CODE, RESILIENCE, PRIVACY) in priority order:
   - Load `data/masvs/MASVS-<GROUP>-<N>.md` for the control statement and the `mastg_tests:` list.
   - For each MASTG test ID, load `data/mastg/MASTG-TEST-####.md` and apply its Static Analysis content (V1) or Steps/Observation/Evaluation (V2) to the source tree.
   - Note V1-fallback tests in findings using the file's `status_note`.
4. **Diff-Specific Analysis** (for PRs) — Focus on changed lines; verify pinning, permissions, and KeyStore/Keychain usage are not weakened.
5. **Produce Findings** — Use `templates/finding.md`. Sort by severity (CRITICAL > HIGH > MEDIUM > LOW > INFO). Deduplicate cross-group findings (cite the most specific MASVS control in `OWASP Ref`).

## Output

Scope summary (platform, languages), upstream-pointer note for MASTG IDs (`https://github.com/OWASP/mastg`, `https://mas.owasp.org/MASTG/`), findings sorted by severity using `templates/finding.md` (each finding carries an optional `MASTG references:` bullet listing any non-TEST `@MASTG-<KIND>-####` cross-refs cited in the informing tests, grouped by KIND alphabetically, IDs sorted numerically, omitted when empty), positive observations, severity count table, RESILIENCE static-only notice block, PRIVACY runtime-required caveat for findings against PRIVACY-2/PRIVACY-3, dynamic-test follow-up list (collected from `data/mastg/` entries with `type: [dynamic]` that informed findings).

## OWASP References

- OWASP MASVS v2.1.0
- OWASP MASTG (forward cross-references)
- OWASP MAS Checklist
- OWASP ASVS v5.0 (overlap items only)
- CWE-312, CWE-327, CWE-295, CWE-926, CWE-749, others per finding
