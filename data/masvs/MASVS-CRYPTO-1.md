---
title: 'MASVS-CRYPTO-1: The app employs current strong cryptography and uses it according
  to industry best practices.'
masvs_group: MASVS-CRYPTO
masvs_control: MASVS-CRYPTO-1
summary: The app employs current strong cryptography and uses it according to industry
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

# MASVS-CRYPTO-1

## Control

The app employs current strong cryptography and uses it according to industry best practices.

## Description

Cryptography plays an especially important role in securing the user's data - even more so in a mobile environment, where attackers having physical access to the user's device is a likely scenario. This control covers general cryptography best practices, which are typically defined in external standards.
