---
title: 'MASVS-STORAGE-2: The app prevents leakage of sensitive data.'
masvs_group: MASVS-STORAGE
masvs_control: MASVS-STORAGE-2
summary: The app prevents leakage of sensitive data.
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

# MASVS-STORAGE-2

## Control

The app prevents leakage of sensitive data.

## Description

There are cases when sensitive data is unintentionally stored or exposed to publicly accessible locations; typically as a side-effect of using certain APIs, system capabilities such as backups or logs. This control covers this kind of unintentional leaks where the developer actually has a way to prevent it.
