---
title: 'MASVS-PLATFORM-3: The app uses the user interface securely.'
masvs_group: MASVS-PLATFORM
masvs_control: MASVS-PLATFORM-3
summary: The app uses the user interface securely.
platforms:
- android
- ios
when_to_use:
- reviewing screen-capture protection on sensitive screens
- auditing pasteboard or clipboard usage for sensitive data
- checking app-switcher background snapshot behavior
threats:
- secrets observed via screenshot in app switcher
- clipboard content read by other installed apps
- UI overlay attacks on sensitive input fields
mastg_tests:
- MASTG-TEST-0035
static_signals:
  android:
  - missing FLAG_SECURE on activities displaying secrets
  - ClipboardManager used for tokens or credentials
  ios:
  - missing background-blur overlay on applicationWillResignActive
  - UIPasteboard.general used for tokens
  - sensitive views without isSecureTextEntry where applicable
resilience_static_only: false
static_only: false
---

# MASVS-PLATFORM-3

## Control

The app uses the user interface securely.

## Description

Sensitive data has to be displayed in the UI in many situations (e.g. passwords, credit card details, OTP codes in notifications). This control ensures that this data doesn't end up being unintentionally leaked due to platform mechanisms such as auto-generated screenshots or accidentally disclosed via e.g. shoulder surfing or sharing the device with another person.
