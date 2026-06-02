---
title: 'MASVS-CRYPTO: Cryptography'
masvs_group: MASVS-CRYPTO
group_overview: true
controls:
- MASVS-CRYPTO-1
- MASVS-CRYPTO-2
---

# MASVS-CRYPTO — Cryptography

MASVS-CRYPTO covers correct use of cryptography — algorithm choice, mode, key/IV management. Mobile apps frequently roll their own crypto or use defaults that include broken algorithms (DES, MD5), insecure modes (ECB), or hard-coded keys, all of which fully compromise the confidentiality the crypto was supposed to provide.

## What this group covers

- Algorithm and key length selection
- Mode/padding choice
- Key generation, storage, and rotation
- IV/nonce randomness

## Controls

- `MASVS-CRYPTO-1` — strong, current algorithms and modes
- `MASVS-CRYPTO-2` — secure key/IV generation and management

See individual control files for `when_to_use`, `threats`, `static_signals`, and `mastg_tests`.
