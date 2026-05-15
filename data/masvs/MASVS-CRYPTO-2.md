---
title: 'MASVS-CRYPTO-2: The app performs key management according to industry best
  practices.'
masvs_group: MASVS-CRYPTO
masvs_control: MASVS-CRYPTO-2
summary: The app performs key management according to industry best practices.
platforms:
- android
- ios
when_to_use:
- reviewing key derivation, generation, and rotation code
- auditing storage of cryptographic key material
- validating IV and nonce uniqueness
threats:
- hard-coded keys extractable from APK or IPA
- deterministic IVs enabling chosen-plaintext attacks
- weak RNG producing predictable keys
mastg_tests:
- MASTG-TEST-0013
- MASTG-TEST-0015
static_signals:
  android:
  - hard-coded byte[] key = { ... } or "...".toByteArray() used as key material
  - IvParameterSpec(new byte[16]) or IvParameterSpec(new byte[12]) — zero-filled IV
  - new Random() (not SecureRandom) for key material
  - keys derived from non-cryptographic hash functions
  ios:
  - 'hard-coded let key: [UInt8] = [ ... ] used for crypto operations'
  - deterministic IV or nonce arrays passed to CCCrypt
  - arc4random used for cryptographic key material instead of SecRandomCopyBytes
resilience_static_only: false
static_only: false
---

# MASVS-CRYPTO-2

## Control

The app performs key management according to industry best practices.

## Description

Even the strongest cryptography would be compromised by poor key management. This control covers the management of cryptographic keys throughout their lifecycle, including key generation, storage and protection.
