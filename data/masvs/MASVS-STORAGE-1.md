---
title: 'MASVS-STORAGE-1: The app securely stores sensitive data.'
masvs_group: MASVS-STORAGE
masvs_control: MASVS-STORAGE-1
summary: The app securely stores sensitive data.
mastg_tests:
- MASTG-TEST-0200
- MASTG-TEST-0201
- MASTG-TEST-0202
- MASTG-TEST-0207
- MASTG-TEST-0247
- MASTG-TEST-0249
- MASTG-TEST-0299
- MASTG-TEST-0300
- MASTG-TEST-0301
- MASTG-TEST-0302
- MASTG-TEST-0303
- MASTG-TEST-0304
- MASTG-TEST-0305
- MASTG-TEST-0306
---

# MASVS-STORAGE-1

## Control

The app securely stores sensitive data.

## Description

Apps handle sensitive data coming from many sources such as the user, the backend, system services or other apps on the device and usually need to store it locally. The storage locations may be private to the app (e.g. its internal storage) or be public and therefore accessible by the user or other installed apps (e.g. public folders such as Downloads). This control ensures that any sensitive data that is intentionally stored by the app is properly protected independently of the target location.
