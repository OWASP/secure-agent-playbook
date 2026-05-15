---
title: 'MASVS-STORAGE-1: The app securely stores sensitive data.'
masvs_group: MASVS-STORAGE
masvs_control: MASVS-STORAGE-1
summary: The app securely stores sensitive data.
platforms:
- android
- ios
when_to_use:
- reviewing how the app persists user credentials, tokens, or PII
- auditing KeyStore/Keychain usage
- storing data in SharedPreferences / NSUserDefaults / SQLite
threats:
- sensitive data extraction from device backups
- leakage to logs or shared external storage
- unprotected files readable by other apps
mastg_tests:
- MASTG-TEST-0001
- MASTG-TEST-0003
static_signals:
  android:
  - SharedPreferences without EncryptedSharedPreferences
  - explicit MODE_WORLD_READABLE / MODE_WORLD_WRITEABLE
  - KeyStore alias usage and key purposes
  - android:allowBackup="true" without backup rules
  ios:
  - NSUserDefaults used for secrets
  - kSecAttrAccessible class on Keychain items
  - files written to Documents/ that get iCloud-backed up
  - property lists containing tokens
resilience_static_only: false
static_only: false
---

# MASVS-STORAGE-1

## Control

The app securely stores sensitive data.

## Description

Apps handle sensitive data coming from many sources such as the user, the backend, system services or other apps on the device and usually need to store it locally. The storage locations may be private to the app (e.g. its internal storage) or be public and therefore accessible by the user or other installed apps (e.g. public folders such as Downloads). This control ensures that any sensitive data that is intentionally stored by the app is properly protected independently of the target location.
