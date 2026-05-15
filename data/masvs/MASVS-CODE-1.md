---
title: 'MASVS-CODE-1: The app requires an up-to-date platform version.'
masvs_group: MASVS-CODE
masvs_control: MASVS-CODE-1
summary: The app requires an up-to-date platform version.
platforms:
- android
- ios
when_to_use:
- reviewing build configuration and minimum supported OS version
- checking whether the app targets EOL platform versions
threats:
- shipping on EOL OS versions that no longer receive security patches
- deprecated APIs with known security weaknesses remaining in use
mastg_tests:
- MASTG-TEST-0040
static_signals:
  android:
  - minSdkVersion below 24 without explicit justification
  - deprecated targetSdkVersion below current Android requirements
  - use of removed or deprecated APIs flagged by Lint
  ios:
  - IPHONEOS_DEPLOYMENT_TARGET below currently-supported iOS versions
  - use of @available guards for APIs no longer relevant to supported OS range
resilience_static_only: false
static_only: false
---

# MASVS-CODE-1

## Control

The app requires an up-to-date platform version.

## Description

Every release of the mobile OS includes security patches and new security features. By supporting older versions, apps stay vulnerable to well-known threats. This control ensures that the app is running on an up-to-date platform version so that users have the latest security protections.
