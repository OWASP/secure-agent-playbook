---
title: 'MASVS-PLATFORM-2: The app uses WebViews securely.'
masvs_group: MASVS-PLATFORM
masvs_control: MASVS-PLATFORM-2
summary: The app uses WebViews securely.
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

# MASVS-PLATFORM-2

## Control

The app uses WebViews securely.

## Description

WebViews are typically used by apps that have a need for increased control over the UI. This control ensures that WebViews are configured securely to prevent sensitive data leakage as well as sensitive functionality exposure (e.g. via JavaScript bridges to native code).
