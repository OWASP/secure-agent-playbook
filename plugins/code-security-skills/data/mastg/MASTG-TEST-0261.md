---
id: MASTG-TEST-0261
title: Debuggable Entitlement Enabled in the entitlements.plist
upstream_version: v2
upstream_path: tests-beta/ios/MASVS-RESILIENCE/MASTG-TEST-0261.md
upstream_tag: 31cec00
platform: ios
covers_masvs:
- MASVS-RESILIENCE-4
type:
- static
weakness: MASWE-0067
profiles:
- R
---

## Overview

The test evaluates whether an iOS application is configured to allow debugging. If an app is debuggable, attackers can leverage debugging tools (see @MASTG-TECH-0084) to analyse the runtime behaviour of the app, and potentially compromise sensitive data or functionality.

## Steps

1. Use @MASTG-TECH-0111 to extract entitlements from the binary.
2. Search for the `get-task-allow` key.

## Observation

The output should contain the value of the `get-task-allow` entitlement.

## Evaluation

The test case fails if the `get-task-allow` entitlement is `true`.
