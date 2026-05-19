---
title: 'MASVS-NETWORK-1: The app secures all network traffic according to the current
  best practices.'
masvs_group: MASVS-NETWORK
masvs_control: MASVS-NETWORK-1
summary: The app secures all network traffic according to the current best practices.
mastg_tests:
- MASTG-TEST-0067
- MASTG-TEST-0217
- MASTG-TEST-0218
- MASTG-TEST-0233
- MASTG-TEST-0234
- MASTG-TEST-0235
- MASTG-TEST-0236
- MASTG-TEST-0237
- MASTG-TEST-0238
- MASTG-TEST-0239
- MASTG-TEST-0282
- MASTG-TEST-0283
- MASTG-TEST-0284
- MASTG-TEST-0285
- MASTG-TEST-0286
- MASTG-TEST-0295
- MASTG-TEST-0321
- MASTG-TEST-0322
- MASTG-TEST-0342
- MASTG-TEST-0343
- MASTG-TEST-0344
- MASTG-TEST-0345
---

# MASVS-NETWORK-1

## Control

The app secures all network traffic according to the current best practices.

## Description

Ensuring data privacy and integrity of any data in transit is critical for any app that communicates over the network. This is typically done by encrypting data and authenticating the remote endpoint, as TLS does. However, there are many ways for a developer to disable the platform secure defaults, or bypass them completely by using low-level APIs or third-party libraries. This control ensures that the app is in fact setting up secure connections in any situation.
