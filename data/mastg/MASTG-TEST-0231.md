---
id: MASTG-TEST-0231
title: References to Logging APIs
upstream_version: v2
upstream_path: tests-beta/android/MASVS-STORAGE/MASTG-TEST-0231.md
upstream_tag: 31cec00
platform: android
covers_masvs:
- MASVS-STORAGE-2
type:
- static
weakness: MASWE-0001
profiles:
- L1
- L2
- P
---

## Overview

This test verifies if an app uses logging APIs like `android.util.Log`, `Log`, `Logger`, `System.out.print`, `System.err.print`, and `java.lang.Throwable#printStackTrace`.

## Steps

1. Use either @MASTG-TECH-0014 with a tool such as @MASTG-TOOL-0110 to identify all logging APIs.

## Observation

The output should contain a list of locations where logging APIs are used.

## Evaluation

The test case fails if an app logs sensitive information from any of the listed locations.
