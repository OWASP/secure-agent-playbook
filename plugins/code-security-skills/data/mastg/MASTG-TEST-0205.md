---
id: MASTG-TEST-0205
title: Non-random Sources Usage
upstream_version: v2
upstream_path: tests-beta/android/MASVS-CRYPTO/MASTG-TEST-0205.md
upstream_tag: 31cec00
platform: android
covers_masvs:
- MASVS-CRYPTO-1
type:
- static
weakness: MASWE-0027
profiles:
- L1
- L2
---

## Overview

Android applications sometimes use non-random sources to generate "random" values, leading to potential security vulnerabilities. Common practices include relying on the current time, such as `Date().getTime()`, or accessing `Calendar.MILLISECOND` to produce values that are easily guessable and reproducible.

## Steps

1. Run a static analysis (@MASTG-TECH-0014) tool on the app and look for uses of non-random sources.

## Observation

The output should contain a list of locations where non-random sources are used.

## Evaluation

The test case fails if you can find security-relevant values, such as passwords or tokens, generated using non-random sources.
