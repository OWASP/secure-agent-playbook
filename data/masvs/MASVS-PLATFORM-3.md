---
title: 'MASVS-PLATFORM-3: The app uses the user interface securely.'
masvs_group: MASVS-PLATFORM
masvs_control: MASVS-PLATFORM-3
summary: The app uses the user interface securely.
mastg_tests:
- MASTG-TEST-0289
- MASTG-TEST-0290
- MASTG-TEST-0291
- MASTG-TEST-0316
- MASTG-TEST-0340
- MASTG-TEST-0346
- MASTG-TEST-0347
---

# MASVS-PLATFORM-3

## Control

The app uses the user interface securely.

## Description

Sensitive data has to be displayed in the UI in many situations (e.g. passwords, credit card details, OTP codes in notifications). This control ensures that this data doesn't end up being unintentionally leaked due to platform mechanisms such as auto-generated screenshots or accidentally disclosed via e.g. shoulder surfing or sharing the device with another person.
