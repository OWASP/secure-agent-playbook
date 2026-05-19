---
title: 'MASVS-PLATFORM-1: The app uses IPC mechanisms securely.'
masvs_group: MASVS-PLATFORM
masvs_control: MASVS-PLATFORM-1
summary: The app uses IPC mechanisms securely.
mastg_tests:
- MASTG-TEST-0007
- MASTG-TEST-0028
- MASTG-TEST-0029
- MASTG-TEST-0030
- MASTG-TEST-0056
- MASTG-TEST-0069
- MASTG-TEST-0070
- MASTG-TEST-0071
- MASTG-TEST-0072
- MASTG-TEST-0075
- MASTG-TEST-0254
- MASTG-TEST-0276
- MASTG-TEST-0277
- MASTG-TEST-0278
- MASTG-TEST-0279
- MASTG-TEST-0280
---

# MASVS-PLATFORM-1

## Control

The app uses IPC mechanisms securely.

## Description

Apps typically use platform provided IPC mechanisms to intentionally expose data or functionality. Both installed apps and the user are able to interact with the app in many different ways. This control ensures that all interactions involving IPC mechanisms happen securely.
