---
id: MASTG-TEST-0253
title: Runtime Use of Local File Access APIs in WebViews
upstream_version: v2
upstream_path: tests-beta/android/MASVS-PLATFORM/MASTG-TEST-0253.md
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

This test is the dynamic counterpart to @MASTG-TEST-0252.

## Steps

1. Run a dynamic analysis tool like @MASTG-TOOL-0001 and either:
    - enumerate instances of `WebView` in the app and list their configuration values
    - or explicitly hook the setters of the `WebView` settings, including:
        - `setJavaScriptEnabled`
        - `setAllowFileAccess`
        - `setAllowFileAccessFromFileURLs`
        - `setAllowUniversalAccessFromFileURLs`

## Observation

The output should contain a list of WebView instances and corresponding settings.

## Evaluation

The test case fails if all of the following applies (based on the [API behavior across different Android versions](../../../Document/0x05h-Testing-Platform-Interaction.md#webview-local-file-access-settings)):

- `setJavaScriptEnabled` is explicitly set to `true`.
- `setAllowFileAccess` is explicitly set to `true` (or not used at all when `minSdkVersion` < 30, inheriting the default value, `true`).
- Either `setAllowFileAccessFromFileURLs` or `setAllowUniversalAccessFromFileURLs` is explicitly set to `true` (or not used at all when `minSdkVersion` < 16, inheriting the default value, `true`).

!!! note
    `AllowFileAccess` being `true` does not represent a security vulnerability by itself, but it can be used in combination with other vulnerabilities to escalate the impact of an attack.
