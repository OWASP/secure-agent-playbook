---
title: 'MASVS-STORAGE: Sensitive Data Storage'
masvs_group: MASVS-STORAGE
group_overview: true
controls:
- MASVS-STORAGE-1
- MASVS-STORAGE-2
---

# MASVS-STORAGE — Sensitive Data Storage

MASVS-STORAGE addresses how mobile applications persist sensitive data on the device — credentials, tokens, PII, and application secrets. Failures in this group expose user data to local attackers, malware, backup leakage, or other apps on the device.

## What this group covers

- Where the app stores secrets (SharedPreferences/NSUserDefaults vs. KeyStore/Keychain)
- Whether storage is encrypted and key material is protected
- Whether backup, cloud-sync, or external-storage paths leak data
- What other apps can read via shared content providers, app groups, or world-readable paths

## Controls

- `MASVS-STORAGE-1` — secure secret storage (KeyStore/Keychain)
- `MASVS-STORAGE-2` — no sensitive data leakage outside the app sandbox

See individual control files for `when_to_use`, `threats`, `static_signals`, and `mastg_tests`.
