---
id: MASTG-TEST-0331
title: Use of Deprecated WebView APIs
upstream_version: v2
upstream_path: tests-beta/ios/MASVS-PLATFORM/MASTG-TEST-0331.md
upstream_tag: 31cec00
platform: ios
covers_masvs:
- MASVS-PLATFORM-2
type:
- static
weakness: MASWE-0072
profiles:
- L1
- L2
---

## Overview

In this test, we look for references to `UIWebView` (@MASTG-KNOW-0076), a deprecated component since iOS 12.0, in favor of `WKWebView`. `UIWebView` presents security and performance risks: it does not allow JavaScript to be fully disabled, lacks process isolation (which `WKWebView` provides), and doesn't support modern web security features like Content Security Policy (CSP).

## Steps

1. Extract the app as described in @MASTG-TECH-0058.
2. Look for references to `UIWebView` in the app using @MASTG-TECH-0070 on all executables and libraries.

## Observation

The output should contain a list of locations where `UIWebView`s are used.

## Evaluation

The test case fails if any use of `UIWebView` is found in the app.
