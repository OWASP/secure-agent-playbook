---
title: "MASVS-PRIVACY: User Privacy"
masvs_group: "MASVS-PRIVACY"
group_overview: true
controls: [MASVS-PRIVACY-1, MASVS-PRIVACY-2, MASVS-PRIVACY-3, MASVS-PRIVACY-4]
platforms: [android, ios]
static_coverage: "partial"
---

# MASVS-PRIVACY — User Privacy

MASVS-PRIVACY covers data minimization, consent, and transparent handling of personal data — distinct from MASVS-STORAGE's focus on technical confidentiality. **This play covers PRIVACY only partially from source**: declared permissions, third-party SDK presence, and manifest claims are statically observable; actual data flow at runtime is deferred to a future Tier 3 `mobile-dynamic-test` skill.

## What this group covers

- Permission minimization (only what's needed)
- Third-party SDK disclosure (analytics, ads, attribution)
- User consent and tracking-transparency declarations
- Runtime data-handling discipline (the deferred part)

## Source-code signals

- **Android:** `<uses-permission>` declarations whose code paths are unused; sensitive combos like `READ_CONTACTS` + `INTERNET` without justification; declared `firebase-analytics`, `facebook-sdk`, `appsflyer`, `adjust` SDKs; broadcast receivers leaking PII
- **iOS:** `Info.plist` `Usage Description` keys with no corresponding code path; `NSContactsUsageDescription` paired with analytics SDKs; `App Tracking Transparency` framework usage; the same set of third-party SDK Pods/Packages

## Controls

- `MASVS-PRIVACY-1` — data collection is minimized and disclosed
- `MASVS-PRIVACY-2` — sensitive data is processed in compliance with applicable regulations
- `MASVS-PRIVACY-3` — third-party data sharing is disclosed and consented to
- `MASVS-PRIVACY-4` — privacy controls are observable and user-controllable

See individual control files for `when_to_use`, `threats`, `static_signals`, and `mastg_tests`.
