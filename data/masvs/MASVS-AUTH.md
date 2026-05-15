---
title: "MASVS-AUTH: Authentication and Authorization"
masvs_group: "MASVS-AUTH"
group_overview: true
controls: [MASVS-AUTH-1, MASVS-AUTH-2, MASVS-AUTH-3]
platforms: [android, ios]
static_coverage: "full"
---

# MASVS-AUTH — Authentication and Authorization

MASVS-AUTH covers how the mobile app authenticates users to remote endpoints and to local resources (biometric unlock, device credentials). Failures here lead to account takeover, local-bypass of locked features, and broken session handling.

## What this group covers

- Protocol-level authentication (OAuth, OIDC, JWT)
- Local authentication (biometric/device credential)
- Session lifecycle (creation, refresh, invalidation, token storage)
- Authorization enforcement on both client and server

## Source-code signals

- **Android:** JWTs decoded without signature verification; OAuth public-client flows missing PKCE; `BiometricPrompt.PromptInfo.Builder().setAllowedAuthenticators(BIOMETRIC_WEAK)`; tokens persisted plaintext in `SharedPreferences`
- **iOS:** JWTs decoded without signature check; `LAContext().evaluatePolicy(.deviceOwnerAuthentication)` without strong-policy hardening; tokens in `NSUserDefaults`; missing PKCE on OAuth public clients

## Controls

- `MASVS-AUTH-1` — secure authentication protocol use
- `MASVS-AUTH-2` — local biometric authentication is bound to a hardware-backed key, not a bypassable boolean check
- `MASVS-AUTH-3` — sessions are correctly created, refreshed, and invalidated

See individual control files for `when_to_use`, `threats`, `static_signals`, and `mastg_tests`.
