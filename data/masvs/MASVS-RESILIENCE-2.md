---
title: 'MASVS-RESILIENCE-2: The app implements anti-tampering mechanisms.'
masvs_group: MASVS-RESILIENCE
masvs_control: MASVS-RESILIENCE-2
summary: The app implements anti-tampering mechanisms.
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

# MASVS-RESILIENCE-2

## Control

The app implements anti-tampering mechanisms.

## Description

Apps run on a user-controlled device, and without proper protections it's relatively easy to run a modified version locally (e.g. to cheat in a game, or enable premium features without paying), or upload a backdoored version of it to third-party app stores. This control tries to ensure the integrity of the app's intended functionality by preventing modifications to the original code and resources.
