---
id: MASTG-TEST-0216
title: Sensitive Data Not Excluded From Backup
upstream_version: v2
upstream_path: tests-beta/android/MASVS-STORAGE/MASTG-TEST-0216.md
upstream_tag: 31cec00
platform: android
covers_masvs:
- MASVS-STORAGE-2
type:
- dynamic
- filesystem
weakness: MASWE-0004
profiles:
- L1
- L2
- P
---

## Overview

This test verifies whether apps correctly instruct the system to exclude sensitive files from backups by performing a backup and restore of the app data and checking which files are restored.

See @MASTG-TEST-0262 for a static analysis counterpart.

Android provides a way to start the backup daemon to back up and restore app files, which you can use to verify which files are actually restored from the backup.

## Steps

1. Start the device.
2. Install an app on your device.
3. Launch and use the app going through the various workflows while inputting sensitive data wherever you can.
4. Perform a backup and restore of the app data (@MASTG-TECH-0128).
5. Uninstall and reinstall the app but don't open it anymore.
6. Restore the data from the backup and get the list of restored files.

## Observation

The output should contain a list of files that are restored from the backup.

## Evaluation

The test case fails if any of the files are considered sensitive.
