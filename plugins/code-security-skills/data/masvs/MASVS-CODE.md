---
title: 'MASVS-CODE: Code Quality'
masvs_group: MASVS-CODE
group_overview: true
controls:
- MASVS-CODE-1
- MASVS-CODE-2
- MASVS-CODE-3
- MASVS-CODE-4
---

# MASVS-CODE — Code Quality

MASVS-CODE covers code-level hygiene that affects security: the platform version the app runs on, whether the app enforces its own updates, dependency CVE hygiene, and input validation at trust boundaries. Failures here typically appear as exploitable outdated clients, supply-chain CVEs, and various forms of injection.

## What this group covers

- Supported platform OS / API-level minimum
- App-update enforcement (in-app update prompts, force-update gates against a server-side minimum)
- Dependency CVE hygiene (cross-refs `sca-audit`)
- Input validation at trust boundaries; safe handling of dangerous APIs

## Controls

- `MASVS-CODE-1` — the app runs on a current, supported platform OS / API level
- `MASVS-CODE-2` — the app enforces installation of available updates
- `MASVS-CODE-3` — third-party software components are free of known CVEs
- `MASVS-CODE-4` — untrusted inputs are validated and sanitized at trust boundaries

See individual control files for `when_to_use`, `threats`, `static_signals`, and `mastg_tests`.
