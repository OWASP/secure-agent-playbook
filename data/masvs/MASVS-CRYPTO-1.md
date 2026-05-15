---
title: 'MASVS-CRYPTO-1: The app employs current strong cryptography and uses it according
  to industry best practices.'
masvs_group: MASVS-CRYPTO
masvs_control: MASVS-CRYPTO-1
summary: The app employs current strong cryptography and uses it according to industry
  best practices.
platforms:
- android
- ios
when_to_use:
- reviewing encryption, hashing, or MAC code
- validating cipher mode and padding choices
- auditing custom crypto helpers or wrappers
threats:
- ciphertext disclosure via ECB pattern leakage
- collision attacks exploiting MD5 or SHA-1
- reversible encryption via DES or 3DES
mastg_tests:
- MASTG-TEST-0011
- MASTG-TEST-0014
static_signals:
  android:
  - Cipher.getInstance("AES/ECB/PKCS5Padding")
  - Cipher.getInstance("DES/...")  or  Cipher.getInstance("DESede/...")
  - MessageDigest.getInstance("MD5")
  - MessageDigest.getInstance("SHA-1") for security purposes
  - Mac.getInstance("HmacMD5")
  ios:
  - CC_MD5(...)
  - CC_SHA1(...)
  - CCCrypt with kCCOptionECBMode
  - kCCAlgorithmDES / kCCAlgorithm3DES
  - kCCHmacAlgMD5
resilience_static_only: false
static_only: false
---

# MASVS-CRYPTO-1

## Control

The app employs current strong cryptography and uses it according to industry best practices.

## Description

Cryptography plays an especially important role in securing the user's data - even more so in a mobile environment, where attackers having physical access to the user's device is a likely scenario. This control covers general cryptography best practices, which are typically defined in external standards.
