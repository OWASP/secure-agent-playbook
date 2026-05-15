---
title: 'MASVS-CODE-2: The app has a mechanism for enforcing app updates.'
masvs_group: MASVS-CODE
masvs_control: MASVS-CODE-2
summary: The app has a mechanism for enforcing app updates.
platforms:
- android
- ios
when_to_use:
- reviewing in-app update enforcement mechanisms
- auditing whether the app can block users on vulnerable versions
threats:
- users continuing to run vulnerable app versions after a critical patch
- no mechanism to force update on discovery of a critical CVE
mastg_tests:
- MASTG-TEST-0041
static_signals:
  android:
  - absence of Google Play In-App Update API integration
  - no version-check against a remote minimum-version endpoint
  ios:
  - no forced-update logic comparing CFBundleShortVersionString to a remote minimum
    version
  - absence of App Store version check via iTunes lookup API
resilience_static_only: false
static_only: false
---

# MASVS-CODE-2

## Control

The app has a mechanism for enforcing app updates.

## Description

Sometimes critical vulnerabilities are discovered in the app when it is already in production. This control ensures that there is a mechanism to force the users to update the app before they can continue using it.
