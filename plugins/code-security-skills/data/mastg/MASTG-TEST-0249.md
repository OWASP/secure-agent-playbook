---
id: MASTG-TEST-0249
title: Runtime Use of Secure Screen Lock Detection APIs
upstream_version: v2
upstream_path: tests-beta/android/MASVS-RESILIENCE/MASTG-TEST-0249.md
upstream_tag: 31cec00
platform: android
covers_masvs:
- MASVS-STORAGE-1
type:
- dynamic
weakness: MASWE-0008
profiles:
- L2
---

## Overview

This test is the dynamic counterpart to @MASTG-TEST-0247.

## Steps

1. Run a dynamic analysis tool like @MASTG-TOOL-0001 and look for uses of `KeyguardManager.isDeviceSecure` and `BiometricManager.canAuthenticate` APIs.

## Observation

The output should contain a list of locations where relevant APIs are used.

## Evaluation

The test case fails if an app doesn't use any API to verify the secure screen lock presence.
