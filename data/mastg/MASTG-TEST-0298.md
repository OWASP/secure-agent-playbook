---
id: MASTG-TEST-0298
title: Runtime Monitoring of Files Eligible for Backup
upstream_version: v2
upstream_path: tests-beta/ios/MASVS-STORAGE/MASTG-TEST-0298.md
upstream_tag: 31cec00
platform: ios
covers_masvs:
- MASVS-STORAGE-2
type:
- dynamic
weakness: MASWE-0004
profiles:
- L1
- L2
- P
---

## Overview

This test logs every file written to the app's data container at `/var/mobile/Containers/Data/Application/$APP_ID` to identify which files are eligible for backup. Files stored in the `tmp` or `Library/Caches` subdirectories are not logged, as they are not backed up.

## Steps

1. Use runtime method hooking (see @MASTG-TECH-0095) and look for uses of file system APIs such as `open`, `fopen`, `NSFileManager`, or `FileHandle` that create or write files.
2. Exercise the app to trigger file creation and writing.

## Observation

The output should list every file the app opens that is eligible for backup.

## Evaluation

The test case fails if any sensitive files are found in the output.
