---
id: MASTG-TEST-0278
title: Pasteboard Contents Not Cleared After Use
upstream_version: v2
upstream_path: tests-beta/ios/MASVS-PLATFORM/MASTG-TEST-0278.md
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

This test checks if the app clears the contents of the general @MASTG-KNOW-0083 when it moves to the background or terminates. If sensitive data is left in the pasteboard, it can be accessed by other apps, leading to potential data leaks.

Apps can clear the contents of the general pasteboard by setting `UIPasteboard.general.items = []` in the appropriate lifecycle methods, such as `applicationDidEnterBackground:` or `applicationWillTerminate:`.

## Steps

1. Run a static analysis scan using @MASTG-TOOL-0073 to detect usage of the [`UIPasteboard.general`](https://developer.apple.com/documentation/uikit/uipasteboard/1622106-generalpasteboard "UIPasteboard generalPasteboard") property.
2. Run a static analysis scan using @MASTG-TOOL-0073 to detect usage of the [`UIPasteboard.setItems`](https://developer.apple.com/documentation/uikit/uipasteboard/setitems(_:options:) "UIPasteboard setItems") method.

## Observation

The output should contain a list of locations where relevant APIs are used.

## Evaluation

The test case fails if the app uses the general pasteboard and does not clear its contents when moving to the background or terminating. Specifically, it should be verified that there are calls to `UIPasteboard.setItems` with an empty array (`[]`) in the appropriate lifecycle methods.
