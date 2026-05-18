---
name: mobile-code-review
description: Security-focused review of native Android and iOS mobile app source code against OWASP MASVS v2.1.0. Use when reviewing mobile codebases, mobile PR diffs, or auditing a mobile module.
license: CC-BY-4.0
---

# Mobile Security Code Review

Review native Android and iOS source code for security vulnerabilities by following the full procedure in `plays/tier1-code-analysis/mobile-code-review.md`.

## Steps

1. **Scope & Context** — Language (Java/Kotlin/Swift/Obj-C/Dart), platform, app type, sensitive data, exposure.
2. **Platform Detection** — Fingerprint Android (AndroidManifest.xml, build.gradle) and/or iOS (Info.plist, *.xcodeproj). If only a cross-platform shell is detected, declare partial coverage.
3. **Run mobsfscan** (primary detection) — `pip install mobsfscan` if missing, then `mobsfscan --json -o /tmp/mobsfscan-report.json <path>`. If unavailable, record `mobsfscan: skipped` and fall back to grep-only detection in step 4.
4. **Systematic Review by MASVS Group** (verifies mobsfscan + closes gaps):
   - MASVS-STORAGE   — secrets in shared prefs / plist, KeyStore/Keychain misuse, backup leakage
   - MASVS-CRYPTO    — weak algorithms, ECB, hard-coded keys, missing IV randomness
   - MASVS-AUTH      — local auth bypass, biometric flags, OAuth/JWT misuse
   - MASVS-NETWORK   — missing TLS pinning, allowsArbitraryLoads, custom trust managers
   - MASVS-PLATFORM  — exported components, intent injection, WebView JS interface, deep-link validation
   - MASVS-CODE      — outdated libs, missing input validation, dangerous deserialization
   - MASVS-RESILIENCE — debuggable flag, ProGuard config, root-detection lib presence. Emit static-only notice; runtime testing required.
   - MASVS-PRIVACY   — declared permissions, third-party SDK detection, sensitive-data manifest claims. Emit per-control caveat for runtime data-flow controls.
5. **Diff-Specific Analysis** (for PRs) — Focus on changed lines, verify pinning/permissions not weakened.
6. **Produce Findings** — Use `templates/finding.md`. Sort by severity (CRITICAL > HIGH > MEDIUM > LOW > INFO). Deduplicate cross-group findings (cite the most specific MASVS control in `OWASP Ref`).

## Output

Scope summary (platform, mobsfscan version or skip note), findings sorted by severity using `templates/finding.md`, positive observations, severity count table, RESILIENCE static-only notice block, PRIVACY static-only caveat, dynamic-test follow-up list.

## OWASP References

- OWASP MASVS v2.1.0
- OWASP MASTG (forward cross-references)
- OWASP MAS Checklist
- OWASP ASVS v5.0 (overlap items only)
- CWE-312, CWE-327, CWE-295, CWE-926, CWE-749, others per finding
