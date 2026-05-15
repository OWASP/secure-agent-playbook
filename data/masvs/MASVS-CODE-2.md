---
title: 'MASVS-CODE-2: The app has a mechanism for enforcing app updates.'
masvs_group: MASVS-CODE
masvs_control: MASVS-CODE-2
summary: The app has a mechanism for enforcing app updates.
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

# MASVS-CODE-2

## Control

The app has a mechanism for enforcing app updates.

## Description

Sometimes critical vulnerabilities are discovered in the app when it is already in production. This control ensures that there is a mechanism to force the users to update the app before they can continue using it.
