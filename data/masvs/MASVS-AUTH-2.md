---
title: 'MASVS-AUTH-2: The app performs local authentication securely according to
  the platform best practices.'
masvs_group: MASVS-AUTH
masvs_control: MASVS-AUTH-2
summary: The app performs local authentication securely according to the platform
  best practices.
platforms:
- android
- ios
when_to_use:
- reviewing biometric unlock for sensitive operations
- auditing BiometricPrompt or LAContext invocations
- verifying that bypassed biometrics actually block sensitive flows
threats:
- biometric bypass when the prompt is a UX check rather than a cryptographic gate
- weak-class biometrics accepted for high-value operations
- biometric used as the sole secret with no fallback key material
mastg_tests:
- MASTG-TEST-0018
- MASTG-TEST-0019
static_signals:
  android:
  - BiometricPrompt.PromptInfo.Builder().setAllowedAuthenticators(BIOMETRIC_WEAK)
  - BiometricPrompt.authenticate(...) called without a CryptoObject bound to a Keystore
    key
  - biometric success treated as a boolean flag rather than gating key access
  ios:
  - LAContext().evaluatePolicy(.deviceOwnerAuthentication, ...) instead of .deviceOwnerAuthenticationWithBiometrics
  - biometric not bound to SecAccessControl with .biometryCurrentSet
  - success treated as a boolean rather than as access to a key
resilience_static_only: false
static_only: false
---

# MASVS-AUTH-2

## Control

The app performs local authentication securely according to the platform best practices.

## Description

Many apps allow users to authenticate via biometrics or a local PIN code. These authentication mechanisms need to be correctly implemented. Additionally, some apps might not have a remote endpoint, and rely fully on local app authentication.
