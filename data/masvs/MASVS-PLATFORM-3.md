---
title: 'MASVS-PLATFORM-3: The app uses the user interface securely.'
masvs_group: MASVS-PLATFORM
masvs_control: MASVS-PLATFORM-3
summary: The app uses the user interface securely.
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

# MASVS-PLATFORM-3

## Control

The app uses the user interface securely.

## Description

Sensitive data has to be displayed in the UI in many situations (e.g. passwords, credit card details, OTP codes in notifications). This control ensures that this data doesn't end up being unintentionally leaked due to platform mechanisms such as auto-generated screenshots or accidentally disclosed via e.g. shoulder surfing or sharing the device with another person.
