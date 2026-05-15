---
title: 'MASVS-NETWORK-2: The app performs identity pinning for all remote endpoints
  under the developer''s control.'
masvs_group: MASVS-NETWORK
masvs_control: MASVS-NETWORK-2
summary: The app performs identity pinning for all remote endpoints under the developer's
  control.
platforms:
- android
- ios
when_to_use:
- reviewing pinning of high-value endpoints such as banking, payments, or auth
- auditing pin storage and certificate rotation strategy
threats:
- silent fallback to system trust if pins fail validation
- bypass via pin removal in a tampered build
- outdated pinned cert blocking the app after a CA rotation
mastg_tests:
- MASTG-TEST-0026
- MASTG-TEST-0027
static_signals:
  android:
  - missing OkHttp CertificatePinner for sensitive endpoints
  - pinning via XML config but no cleartextTrafficPermitted="false"
  - pins as Base64 SHA-256 hash without rotation comments
  ios:
  - missing NSPinnedDomains entries in Info.plist
  - missing manual URLSession validator comparing SecTrustEvaluate leaf to expected
    pins
  - pinning embedded in code without rotation strategy
resilience_static_only: false
static_only: false
---

# MASVS-NETWORK-2

## Control

The app performs identity pinning for all remote endpoints under the developer's control.

## Description

Instead of trusting all the default root CAs of the framework or device, this control will make sure that only very specific CAs are trusted. This practice is typically called certificate pinning or public key pinning.
