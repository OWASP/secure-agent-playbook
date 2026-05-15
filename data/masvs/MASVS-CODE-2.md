---
title: 'MASVS-CODE-2: The app has a mechanism for enforcing app updates.'
masvs_group: MASVS-CODE
masvs_control: MASVS-CODE-2
summary: The app has a mechanism for enforcing app updates.
platforms:
- android
- ios
when_to_use:
- reviewing in-app update flows and forced-upgrade gates
- auditing whether the app refuses to run on outdated versions
- validating version-check endpoints and minimum-supported-version logic
threats:
- exploitable outdated client running in the wild after a fix has shipped
- users stuck on a pre-fix build because the app lacks an update prompt
- cached APK/IPA bypass of update mechanisms via offline install
mastg_tests:
- MASTG-TEST-0040
static_signals:
  android:
  - missing AppUpdateManager (Play In-App Updates API) integration
  - no version check at app start against a minimum-supported-version endpoint
  - soft-update prompt only with no hard-update fallback path
  - manifest versionCode increments without an update-enforcement code path
  ios:
  - no version check at app launch against an App Store / minimum-supported-version endpoint
  - no force-update gate comparing Bundle.main.infoDictionary["CFBundleShortVersionString"] to a server-side minimum
  - SKStoreProductViewController launch flow without a blocking gate when below minimum version
resilience_static_only: false
static_only: false
---

# MASVS-CODE-2

## Control

The app has a mechanism for enforcing app updates.

## Description

Sometimes critical vulnerabilities are discovered in the app when it is already in production. This control ensures that there is a mechanism to force the users to update the app before they can continue using it.
