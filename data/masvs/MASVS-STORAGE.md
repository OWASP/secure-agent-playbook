---
title: "MASVS-STORAGE: Sensitive Data Storage"
masvs_group: "MASVS-STORAGE"
group_overview: true
controls: [MASVS-STORAGE-1, MASVS-STORAGE-2]
platforms: [android, ios]
static_coverage: "full"
---

# MASVS-STORAGE — Sensitive Data Storage

MASVS-STORAGE addresses how mobile applications persist sensitive data on the device — credentials, tokens, PII, and application secrets. Failures in this group expose user data to local attackers, malware, backup leakage, or other apps on the device.

## What this group covers

- Where the app stores secrets (SharedPreferences/NSUserDefaults vs. KeyStore/Keychain)
- Whether storage is encrypted and key material is protected
- Whether backup, cloud-sync, or external-storage paths leak data
- What other apps can read via shared content providers, app groups, or world-readable paths

## Source-code signals

- **Android:** `SharedPreferences` without `EncryptedSharedPreferences`; explicit `MODE_WORLD_READABLE`; `android:allowBackup="true"` without backup rules; keystore alias misuse
- **iOS:** secrets in `NSUserDefaults` or property lists; missing or weak `kSecAttrAccessible*` class; data in `Documents/` directory that is included in iCloud backup

## Controls

- `MASVS-STORAGE-1` — secure secret storage (KeyStore/Keychain)
- `MASVS-STORAGE-2` — no sensitive data leakage outside the app sandbox

See individual control files for `when_to_use`, `threats`, `static_signals`, and `mastg_tests`.
