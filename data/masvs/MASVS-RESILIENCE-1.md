---
title: 'MASVS-RESILIENCE-1: The app validates the integrity of the platform.'
masvs_group: MASVS-RESILIENCE
masvs_control: MASVS-RESILIENCE-1
summary: The app validates the integrity of the platform.
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

# MASVS-RESILIENCE-1

## Control

The app validates the integrity of the platform.

## Description

Running on a platform that has been tampered with can be very dangerous for apps, as this may disable certain security features, putting the data of the app at risk. Trusting the platform is essential for many of the MASVS controls relying on the platform being secure (e.g. secure storage, biometrics, sandboxing, etc.). This control tries to validate that the OS has not been compromised and its security features can thus be trusted.
