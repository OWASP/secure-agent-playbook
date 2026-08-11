---
title: 'MASVS-NETWORK-2: The app performs identity pinning for all remote endpoints
  under the developer''s control.'
masvs_group: MASVS-NETWORK
masvs_control: MASVS-NETWORK-2
summary: The app performs identity pinning for all remote endpoints under the developer's
  control.
mastg_tests:
- MASTG-TEST-0068
- MASTG-TEST-0242
- MASTG-TEST-0243
- MASTG-TEST-0244
---

# MASVS-NETWORK-2

## Control

The app performs identity pinning for all remote endpoints under the developer's control.

## Description

Instead of trusting all the default root CAs of the framework or device, this control will make sure that only very specific CAs are trusted. This practice is typically called certificate pinning or public key pinning.
