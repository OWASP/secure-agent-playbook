---
title: 'MASVS-AUTH-2: The app performs local authentication securely according to
  the platform best practices.'
masvs_group: MASVS-AUTH
masvs_control: MASVS-AUTH-2
summary: The app performs local authentication securely according to the platform
  best practices.
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

# MASVS-AUTH-2

## Control

The app performs local authentication securely according to the platform best practices.

## Description

Many apps allow users to authenticate via biometrics or a local PIN code. These authentication mechanisms need to be correctly implemented. Additionally, some apps might not have a remote endpoint, and rely fully on local app authentication.
