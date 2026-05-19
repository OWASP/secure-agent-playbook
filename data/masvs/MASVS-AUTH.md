---
title: 'MASVS-AUTH: Authentication and Authorization'
masvs_group: MASVS-AUTH
group_overview: true
controls:
- MASVS-AUTH-1
- MASVS-AUTH-2
- MASVS-AUTH-3
---

# MASVS-AUTH — Authentication and Authorization

MASVS-AUTH covers how the mobile app authenticates users to remote endpoints and to local resources (biometric unlock, device credentials). Failures here lead to account takeover, local-bypass of locked features, and broken session handling.

## What this group covers

- Protocol-level authentication (OAuth, OIDC, JWT)
- Local authentication (biometric/device credential)
- Session lifecycle (creation, refresh, invalidation, token storage)
- Authorization enforcement on both client and server

## Controls

- `MASVS-AUTH-1` — secure authentication protocol use
- `MASVS-AUTH-2` — local biometric authentication is bound to a hardware-backed key, not a bypassable boolean check
- `MASVS-AUTH-3` — sessions are correctly created, refreshed, and invalidated

See individual control files for `when_to_use`, `threats`, `static_signals`, and `mastg_tests`.
