---
title: 'MASVS-NETWORK-2: The app performs identity pinning for all remote endpoints
  under the developer''s control.'
masvs_group: MASVS-NETWORK
masvs_control: MASVS-NETWORK-2
summary: The app performs identity pinning for all remote endpoints under the developer's
  control.
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

# MASVS-NETWORK-2

## Control

The app performs identity pinning for all remote endpoints under the developer's control.

## Description

Instead of trusting all the default root CAs of the framework or device, this control will make sure that only very specific CAs are trusted. This practice is typically called certificate pinning or public key pinning.
