---
title: 'MASVS-RESILIENCE-3: The app implements anti-static analysis mechanisms.'
masvs_group: MASVS-RESILIENCE
masvs_control: MASVS-RESILIENCE-3
summary: The app implements anti-static analysis mechanisms.
platforms:
- android
- ios
when_to_use: []
threats: []
mastg_tests: []
static_signals:
  android: []
  ios: []
resilience_static_only: true
static_only: false
---

# MASVS-RESILIENCE-3

## Control

The app implements anti-static analysis mechanisms.

## Description

Understanding the internals of an app is typically the first step towards tampering with it (either dynamically, or statically). This control tries to impede comprehension by making it as difficult as possible to figure out how an app works using static analysis.
