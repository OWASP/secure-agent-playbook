---
id: MASTG-TEST-0279
title: Pasteboard Contents Not Expiring
upstream_version: v2
upstream_path: tests-beta/ios/MASVS-PLATFORM/MASTG-TEST-0279.md
upstream_tag: 31cec00
platform: ios
covers_masvs:
- MASVS-PLATFORM-1
type:
- static
weakness: MASWE-0053
profiles:
- L2
---

## Overview

This test checks if the app sets an expiration date for the contents of the general @MASTG-KNOW-0083 using the `UIPasteboard.setItems(_:options:)` method with the `UIPasteboard.Options.expirationDate` option. If sensitive data is left in the pasteboard without an expiration date, it can be accessed by other apps indefinitely, leading to potential data leaks.

## Steps

1. Run a static analysis scan using @MASTG-TOOL-0073 to detect usage of the [`UIPasteboard.general`](https://developer.apple.com/documentation/uikit/uipasteboard/1622106-generalpasteboard "UIPasteboard generalPasteboard") property.
2. Run a static analysis scan using @MASTG-TOOL-0073 to detect usage of the `UIPasteboard.setItems(_:options:)` method.

## Observation

The output should contain a list of locations where relevant APIs are used.

## Evaluation

The test case fails if the app uses the general pasteboard without setting an expiration date for its contents. Specifically, ensure that the `UIPasteboard.setItems(_:options:)` method is called with the `UIPasteboard.Options.expirationDate` option.
