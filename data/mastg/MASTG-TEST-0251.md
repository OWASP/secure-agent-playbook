---
id: MASTG-TEST-0251
title: Runtime Use of Content Provider Access APIs in WebViews
upstream_version: v2
upstream_path: tests-beta/android/MASVS-PLATFORM/MASTG-TEST-0251.md
upstream_tag: 31cec00
platform: android
covers_masvs:
- MASVS-PLATFORM-2
type:
- dynamic
weakness: MASWE-0069
profiles:
- L1
- L2
---

## Overview

This test is the dynamic counterpart to @MASTG-TEST-0250.

## Steps

1. Run a dynamic analysis tool like @MASTG-TOOL-0001 and either:
    - enumerate instances of `WebView` in the app and list their configuration values
    - or explicitly hook the setters of the `WebView` settings

## Observation

The output should contain a list of WebView instances and corresponding settings.

## Evaluation

The test case fails if all of the following applies:

- `JavaScriptEnabled` is `true`.
- `AllowContentAccess` is `true`.
- `AllowUniversalAccessFromFileURLs` is `true`.

You should use the list of content providers obtained in @MASTG-TEST-0250 to verify if they handle sensitive data.

!!! note
    `AllowContentAccess` being `true` does not represent a security vulnerability by itself, but it can be used in combination with other vulnerabilities to escalate the impact of an attack.
