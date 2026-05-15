---
title: "MASVS-CODE: Code Quality"
masvs_group: "MASVS-CODE"
group_overview: true
controls: [MASVS-CODE-1, MASVS-CODE-2, MASVS-CODE-3, MASVS-CODE-4]
platforms: [android, ios]
static_coverage: "full"
---

# MASVS-CODE — Code Quality

MASVS-CODE covers code-level hygiene that affects security: the platform version the app runs on, whether the app enforces its own updates, dependency CVE hygiene, and input validation at trust boundaries. Failures here typically appear as exploitable outdated clients, supply-chain CVEs, and various forms of injection.

## What this group covers

- Supported platform OS / API-level minimum
- App-update enforcement (in-app update prompts, force-update gates against a server-side minimum)
- Dependency CVE hygiene (cross-refs `sca-audit`)
- Input validation at trust boundaries; safe handling of dangerous APIs

## Source-code signals

- **Android:** deprecated `minSdkVersion`; missing `AppUpdateManager` / Play In-App Updates; outdated `dependencies {}` versions with known CVEs; `Runtime.exec` with concatenated user input; `WebView.evaluateJavascript(...)` with user-controlled strings; dangerous `ObjectInputStream` deserialization
- **iOS:** outdated deployment target; no force-update gate at app launch; abandoned / vulnerable pods in `Podfile.lock`; `String(format:)` with user-controlled format string; `NSKeyedUnarchiver` of untrusted input

## Controls

- `MASVS-CODE-1` — the app runs on a current, supported platform OS / API level
- `MASVS-CODE-2` — the app enforces installation of available updates
- `MASVS-CODE-3` — third-party software components are free of known CVEs
- `MASVS-CODE-4` — untrusted inputs are validated and sanitized at trust boundaries

See individual control files for `when_to_use`, `threats`, `static_signals`, and `mastg_tests`.
