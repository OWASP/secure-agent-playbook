---
title: "MASVS-CODE: Code Quality"
masvs_group: "MASVS-CODE"
group_overview: true
controls: [MASVS-CODE-1, MASVS-CODE-2, MASVS-CODE-3, MASVS-CODE-4]
platforms: [android, ios]
static_coverage: "full"
---

# MASVS-CODE — Code Quality

MASVS-CODE covers code-level hygiene that affects security: dependency currency, dangerous APIs, input validation at boundaries, and error handling that doesn't leak sensitive data. Failures here typically appear as supply-chain vulnerabilities (outdated libs with CVEs), injection of various kinds, and information disclosure via logs.

## What this group covers

- Platform/SDK support window
- Dependency CVE hygiene (cross-refs `sca-audit`)
- Input validation at all trust boundaries
- Safe error-handling and logging in release builds

## Source-code signals

- **Android:** deprecated `minSdkVersion`; outdated `dependencies {}` versions with known CVEs; `Runtime.exec` with concatenated user input; dangerous `ObjectInputStream` deserialization; `WebView.evaluateJavascript(...)` with concatenated user input; debug stack traces shipped in release `Log.d`
- **iOS:** outdated deployment target; abandoned/vulnerable pods in `Podfile.lock`; `String(format:)` with user-controlled format string; `NSKeyedUnarchiver` of untrusted input; `print(error)` in release builds

## Controls

- `MASVS-CODE-1` — the app uses supported platform versions and SDKs
- `MASVS-CODE-2` — third-party dependencies are current and free of known CVEs
- `MASVS-CODE-3` — input is validated at trust boundaries; dangerous APIs are avoided
- `MASVS-CODE-4` — errors and logs do not expose sensitive information

See individual control files for `when_to_use`, `threats`, `static_signals`, and `mastg_tests`.
