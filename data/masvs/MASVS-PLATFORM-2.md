---
title: 'MASVS-PLATFORM-2: The app uses WebViews securely.'
masvs_group: MASVS-PLATFORM
masvs_control: MASVS-PLATFORM-2
summary: The app uses WebViews securely.
platforms:
- android
- ios
when_to_use:
- reviewing WebView usage in the app
- auditing JavaScript-to-native bridge configurations
- checking JS injection paths from user-controlled content
threats:
- native API exposure via JS bridge enabling RCE
- XSS in WebView escalating to native access
- cross-origin message acceptance by unsecured handlers
mastg_tests:
- MASTG-TEST-0033
- MASTG-TEST-0034
static_signals:
  android:
  - WebView.addJavascriptInterface(...) exposing methods to untrusted content
  - WebSettings.setAllowFileAccessFromFileURLs(true)
  - WebView.evaluateJavascript(...) with concatenated user input
  - setMixedContentMode(MIXED_CONTENT_ALWAYS_ALLOW)
  ios:
  - WKUserContentController.add(scriptMessageHandler:) accepting messages from any
    origin
  - WKWebViewConfiguration.javaScriptEnabled = true for trusted-only content without
    origin restriction
  - missing origin checks in WKScriptMessageHandler
resilience_static_only: false
static_only: false
---

# MASVS-PLATFORM-2

## Control

The app uses WebViews securely.

## Description

WebViews are typically used by apps that have a need for increased control over the UI. This control ensures that WebViews are configured securely to prevent sensitive data leakage as well as sensitive functionality exposure (e.g. via JavaScript bridges to native code).
