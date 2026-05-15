---
title: 'MASVS-RESILIENCE-4: The app implements anti-dynamic analysis techniques.'
masvs_group: MASVS-RESILIENCE
masvs_control: MASVS-RESILIENCE-4
summary: The app implements anti-dynamic analysis techniques.
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

# MASVS-RESILIENCE-4

## Control

The app implements anti-dynamic analysis techniques.

## Description

Sometimes pure static analysis is very difficult and time consuming so it typically goes hand in hand with dynamic analysis. Observing and manipulating an app during runtime makes it much easier to decipher its behavior. This control aims to make it as difficult as possible to perform dynamic analysis, as well as prevent dynamic instrumentation which could allow an attacker to modify the code at runtime.
