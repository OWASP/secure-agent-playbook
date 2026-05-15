---
title: 'MASVS-RESILIENCE-2: The app implements anti-tampering mechanisms.'
masvs_group: MASVS-RESILIENCE
masvs_control: MASVS-RESILIENCE-2
summary: The app implements anti-tampering mechanisms.
platforms:
- android
- ios
when_to_use:
- reviewing self-integrity and re-signing detection logic
- auditing anti-tamper checks on app code and resources
threats:
- repackaged APK or IPA with malicious code inserted
- runtime code injection bypassing security checks
mastg_tests:
- MASTG-TEST-0052
static_signals:
  android:
  - absence of signing-certificate verification logic
  - missing DEX integrity checks
  - no checks against applicationInfo.sourceDir modification
  ios:
  - missing entitlement or code-signing checks at runtime
  - no _dyld_image_count validation
  - no embedded provisioning-profile checks
resilience_static_only: true
static_only: false
---

# MASVS-RESILIENCE-2

## Control

The app implements anti-tampering mechanisms.

## Description

Apps run on a user-controlled device, and without proper protections it's relatively easy to run a modified version locally (e.g. to cheat in a game, or enable premium features without paying), or upload a backdoored version of it to third-party app stores. This control tries to ensure the integrity of the app's intended functionality by preventing modifications to the original code and resources.
