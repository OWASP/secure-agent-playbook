---
title: 'MASVS-PRIVACY-3: The app is transparent about data collection and usage.'
masvs_group: MASVS-PRIVACY
masvs_control: MASVS-PRIVACY-3
summary: The app is transparent about data collection and usage.
platforms:
- android
- ios
when_to_use:
- reviewing third-party SDK presence vs. consent UI implementation
- auditing whether pre-consent telemetry hits occur at app launch
threats:
- third-party SDK initialization before consent dialog is shown
- tracking IDs collected before user opt-in
mastg_tests:
- MASTG-TEST-0262
static_signals:
  android:
  - third-party SDK init(...) calls at app start before any consent UI
  - analytics calls in Application.onCreate before consent check
  ios:
  - third-party SDK start(...) or configure(...) calls in application(_:didFinishLaunchingWithOptions:)
    before tracking-authorization-status check
resilience_static_only: false
static_only: true
---

# MASVS-PRIVACY-3

## Control

The app is transparent about data collection and usage.

## Description

Users have the right to know how their data is being used. This control ensures that apps provide clear information about data collection, storage, and sharing practices, including any behavior a user wouldn't reasonably expect, such as background data collection. Apps should also adhere to platform guidelines on data declarations.
