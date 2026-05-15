---
title: 'MASVS-RESILIENCE-4: The app implements anti-dynamic analysis techniques.'
masvs_group: MASVS-RESILIENCE
masvs_control: MASVS-RESILIENCE-4
summary: The app implements anti-dynamic analysis techniques.
platforms:
- android
- ios
when_to_use:
- reviewing tamper-detection and dynamic-analysis-prevention logic
- checking for Frida or hooking detection mechanisms
threats:
- dynamic patching of business logic at runtime via Frida or similar
- debugger attachment to a production build enabling logic bypass
mastg_tests:
- MASTG-TEST-0046
static_signals:
  android:
  - absence of Frida-detection patterns (no /proc/self/maps checks for frida, no dlopen
    checks)
  - no SafetyNet or Play Integrity attestation call
  ios:
  - absence of DTTJailbreakDetection or IOSSecuritySuite Frida-detection checks
  - missing checks for MobileSubstrate or Cydia artifacts
resilience_static_only: true
static_only: false
---

# MASVS-RESILIENCE-4

## Control

The app implements anti-dynamic analysis techniques.

## Description

Sometimes pure static analysis is very difficult and time consuming so it typically goes hand in hand with dynamic analysis. Observing and manipulating an app during runtime makes it much easier to decipher its behavior. This control aims to make it as difficult as possible to perform dynamic analysis, as well as prevent dynamic instrumentation which could allow an attacker to modify the code at runtime.
