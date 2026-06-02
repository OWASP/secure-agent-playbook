---
id: MASTG-TEST-0277
title: Sensitive Data in the iOS General Pasteboard at Runtime
upstream_version: v2
upstream_path: tests-beta/ios/MASVS-PLATFORM/MASTG-TEST-0277.md
upstream_tag: 31cec00
platform: ios
covers_masvs:
- MASVS-PLATFORM-1
type:
- dynamic
weakness: MASWE-0053
profiles:
- L2
---

## Overview

This test is the dynamic counterpart to @MASTG-TEST-0276.

In this case we'll monitor the @MASTG-KNOW-0083 for sensitive data being written to it at runtime. Note that this can be challenging to detect, as it requires the app to be running and the pasteboard to be modified while the test is being executed. You can trigger the pasteboard by manually entering sensitive data into the app, such as passwords or personal information, while the test is running. Or you can do it automatically by using a script that simulates user input or modifies the pasteboard directly.

## Steps

1. Monitor the pasteboard for sensitive data using @MASTG-TECH-0134.
2. Run the app and perform actions that may write sensitive data to the pasteboard, such as copying passwords or personal information.

## Observation

The output should contain a list of pasteboard items that were written during the test.

## Evaluation

The test case fails if sensitive data is traced during a write operation to the general pasteboard specifically.
