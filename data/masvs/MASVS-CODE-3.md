---
title: 'MASVS-CODE-3: The app only uses software components without known vulnerabilities.'
masvs_group: MASVS-CODE
masvs_control: MASVS-CODE-3
summary: The app only uses software components without known vulnerabilities.
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

# MASVS-CODE-3

## Control

The app only uses software components without known vulnerabilities.

## Description

To be truly secure, a full whitebox assessment should have been performed on all app components. However, as it usually happens with e.g. for third-party components this is not always feasible and not typically part of a penetration test. This control covers "low-hanging fruit" cases, such as those that can be detected just by scanning libraries for known vulnerabilities.
