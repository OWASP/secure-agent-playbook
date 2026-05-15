---
title: "MASVS-CRYPTO: Cryptography"
masvs_group: "MASVS-CRYPTO"
group_overview: true
controls: [MASVS-CRYPTO-1, MASVS-CRYPTO-2]
platforms: [android, ios]
static_coverage: "full"
---

# MASVS-CRYPTO — Cryptography

MASVS-CRYPTO covers correct use of cryptography — algorithm choice, mode, key/IV management. Mobile apps frequently roll their own crypto or use defaults that include broken algorithms (DES, MD5), insecure modes (ECB), or hard-coded keys, all of which fully compromise the confidentiality the crypto was supposed to provide.

## What this group covers

- Algorithm and key length selection
- Mode/padding choice
- Key generation, storage, and rotation
- IV/nonce randomness

## Source-code signals

- **Android:** `Cipher.getInstance("AES/ECB/PKCS5Padding")`; `MessageDigest.getInstance("MD5")` or `"SHA-1"` for security purposes; hard-coded `byte[] key = ...` literals; `IvParameterSpec(new byte[16])`; `Random` (not `SecureRandom`) for key material
- **iOS:** `CC_MD5`/`CC_SHA1`; `CCCrypt` with `kCCOptionECBMode`; hard-coded `let key: [UInt8] = [...]`; deterministic IV/nonce; `arc4random` for key material

## Controls

- `MASVS-CRYPTO-1` — strong, current algorithms and modes
- `MASVS-CRYPTO-2` — secure key/IV generation and management

See individual control files for `when_to_use`, `threats`, `static_signals`, and `mastg_tests`.
