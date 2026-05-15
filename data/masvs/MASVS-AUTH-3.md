---
title: 'MASVS-AUTH-3: The app secures sensitive operations with additional authentication.'
masvs_group: MASVS-AUTH
masvs_control: MASVS-AUTH-3
summary: The app secures sensitive operations with additional authentication.
platforms:
- android
- ios
when_to_use:
- reviewing session and token lifecycle management
- auditing logout flows for completeness
- validating refresh-token rotation implementation
threats:
- session fixation via reused tokens after authentication
- long-lived refresh tokens persisting after logout
- tokens not invalidated on the server side after logout
mastg_tests:
- MASTG-TEST-0021
- MASTG-TEST-0022
static_signals:
  android:
  - tokens persisted in SharedPreferences plaintext
  - absence of refresh-token rotation logic
  - logout that clears local state but does not call a server-side invalidate endpoint
  ios:
  - tokens stored in NSUserDefaults plaintext
  - absence of refresh-token rotation logic
  - logout-without-server-revoke pattern
resilience_static_only: false
static_only: false
---

# MASVS-AUTH-3

## Control

The app secures sensitive operations with additional authentication.

## Description

Some additional form of authentication is often desirable for sensitive actions inside the app. This can be done in different ways (biometric, pin, MFA code generator, email, deep links, etc) and they all need to be implemented securely.
