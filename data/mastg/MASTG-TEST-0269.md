---
id: MASTG-TEST-0269
title: Runtime Use Of APIs Allowing Fallback to Non-Biometric Authentication
upstream_version: v2
upstream_path: tests-beta/ios/MASVS-AUTH/MASTG-TEST-0269.md
upstream_tag: 31cec00
platform: ios
covers_masvs:
- MASVS-AUTH-2
type:
- dynamic
weakness: MASWE-0045
profiles:
- L2
---

## Overview

This test is the dynamic counterpart to @MASTG-TEST-0268.

## Steps

1. Use runtime method hooking (see @MASTG-TECH-0095) and look for uses of [`SecAccessControlCreateWithFlags`](https://developer.apple.com/documentation/security/secaccesscontrolcreatewithflags(_:_:_:_:)) and specific flags.

## Observation

The output should contain a list of locations where the `SecAccessControlCreateWithFlags` function is called including all used flags.

## Evaluation

The test case fails if the app uses `SecAccessControlCreateWithFlags` with the `kSecAccessControlUserPresence` or `kSecAccessControlDevicePasscode` flags for any sensitive data resource that needs protection.
