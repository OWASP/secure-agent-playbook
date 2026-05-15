---
title: 'MASVS-PLATFORM-1: The app uses IPC mechanisms securely.'
masvs_group: MASVS-PLATFORM
masvs_control: MASVS-PLATFORM-1
summary: The app uses IPC mechanisms securely.
platforms:
- android
- ios
when_to_use:
- reviewing exported activities, services, receivers, or providers
- auditing deep-link handlers and URL scheme inputs
- validating Intent extras flowing through the app
threats:
- arbitrary intent injection by other installed apps
- deep-link to authenticated state without verification
- content-provider exposure to other apps
mastg_tests:
- MASTG-TEST-0030
- MASTG-TEST-0031
static_signals:
  android:
  - android:exported="true" on activities, receivers, or services without android:permission
  - Intent.getStringExtra(...) flowing directly to SQL queries, file I/O, or WebView.loadUrl
  - deep-link path validation absent
  ios:
  - URL schemes registered in Info.plist without verifying scheme or host in application(_:open:url:options:)
  - universal links opening authenticated routes without verifying the route
resilience_static_only: false
static_only: false
---

# MASVS-PLATFORM-1

## Control

The app uses IPC mechanisms securely.

## Description

Apps typically use platform provided IPC mechanisms to intentionally expose data or functionality. Both installed apps and the user are able to interact with the app in many different ways. This control ensures that all interactions involving IPC mechanisms happen securely.
