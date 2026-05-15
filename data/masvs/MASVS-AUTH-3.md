---
title: 'MASVS-AUTH-3: The app secures sensitive operations with additional authentication.'
masvs_group: MASVS-AUTH
masvs_control: MASVS-AUTH-3
summary: The app secures sensitive operations with additional authentication.
platforms:
- android
- ios
when_to_use:
- reviewing high-risk operations (payments, account deletion, data export, key rotation)
- auditing whether sensitive operations require re-authentication beyond an initial login
- validating step-up flows for biometric or password re-confirmation before critical actions
threats:
- session abuse: an attacker with a stolen or unlocked device performs payments / account changes without an additional auth step
- privileged-action gating that relies only on initial login, allowing all-or-nothing access for the session duration
- replay of cached auth state past the point where step-up should have been required
mastg_tests:
- MASTG-TEST-0021
- MASTG-TEST-0022
static_signals:
  android:
  - BiometricPrompt invoked only at login, with no re-auth gate on sensitive code paths
  - sensitive operation methods (transferFunds, deleteAccount, exportData) called without preceding re-authentication
  - cached session tokens reused for high-risk endpoints without server-side step-up enforcement
  ios:
  - LAContext.evaluatePolicy not invoked before sensitive flows
  - sensitive operations dispatched off a stored boolean isAuthenticated rather than a fresh authentication challenge
  - reauthenticatedRecently / recent-biometric checks absent on high-risk flows
resilience_static_only: false
static_only: false
---

# MASVS-AUTH-3

## Control

The app secures sensitive operations with additional authentication.

## Description

Some additional form of authentication is often desirable for sensitive actions inside the app. This can be done in different ways (biometric, pin, MFA code generator, email, deep links, etc) and they all need to be implemented securely.
