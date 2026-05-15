---
title: 'MASVS-STORAGE-2: The app prevents leakage of sensitive data.'
masvs_group: MASVS-STORAGE
masvs_control: MASVS-STORAGE-2
summary: The app prevents leakage of sensitive data.
platforms:
- android
- ios
when_to_use:
- reviewing logs and debug output for sensitive data
- auditing shared content providers and app groups
- checking external storage paths used for sensitive files
- reviewing IPC payloads for PII leakage
threats:
- secret leakage via logs in production builds
- cross-app reading via world-readable storage
- unintended PII shared via content providers or app extensions
mastg_tests:
- MASTG-TEST-0004
- MASTG-TEST-0005
static_signals:
  android:
  - Log.d / Log.i / Log.v calls containing tokens or secrets
  - println(...) containing secrets
  - getExternalFilesDir(...) used for secrets
  - ContentProvider declared without android:permission
  - ClipboardManager used for sensitive data
  ios:
  - NSLog(...) of secrets
  - print(...) of secrets in release builds
  - app-group container reads of secrets
  - broadcasting secrets via NotificationCenter to other extensions
resilience_static_only: false
static_only: false
---

# MASVS-STORAGE-2

## Control

The app prevents leakage of sensitive data.

## Description

There are cases when sensitive data is unintentionally stored or exposed to publicly accessible locations; typically as a side-effect of using certain APIs, system capabilities such as backups or logs. This control covers this kind of unintentional leaks where the developer actually has a way to prevent it.
