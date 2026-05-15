---
title: 'MASVS-NETWORK-1: The app secures all network traffic according to the current
  best practices.'
masvs_group: MASVS-NETWORK
masvs_control: MASVS-NETWORK-1
summary: The app secures all network traffic according to the current best practices.
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

# MASVS-NETWORK-1

## Control

The app secures all network traffic according to the current best practices.

## Description

Ensuring data privacy and integrity of any data in transit is critical for any app that communicates over the network. This is typically done by encrypting data and authenticating the remote endpoint, as TLS does. However, there are many ways for a developer to disable the platform secure defaults, or bypass them completely by using low-level APIs or third-party libraries. This control ensures that the app is in fact setting up secure connections in any situation.
