---
title: 'MASVS-PLATFORM-1: The app uses IPC mechanisms securely.'
masvs_group: MASVS-PLATFORM
masvs_control: MASVS-PLATFORM-1
summary: The app uses IPC mechanisms securely.
platforms:
- android
- ios
when_to_use: []
threats: []
mastg_tests: []
static_signals:
  android: []
  ios: []
resilience_static_only: false
static_only: false
---

# MASVS-PLATFORM-1

## Control

The app uses IPC mechanisms securely.

## Description

Apps typically use platform provided IPC mechanisms to intentionally expose data or functionality. Both installed apps and the user are able to interact with the app in many different ways. This control ensures that all interactions involving IPC mechanisms happen securely.
