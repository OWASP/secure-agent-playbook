---
title: 'MASVS-CODE-4: The app validates and sanitizes all untrusted inputs.'
masvs_group: MASVS-CODE
masvs_control: MASVS-CODE-4
summary: The app validates and sanitizes all untrusted inputs.
mastg_tests:
- MASTG-TEST-0026
- MASTG-TEST-0027
- MASTG-TEST-0043
- MASTG-TEST-0079
- MASTG-TEST-0086
- MASTG-TEST-0222
- MASTG-TEST-0223
- MASTG-TEST-0228
- MASTG-TEST-0229
- MASTG-TEST-0230
- MASTG-TEST-0337
- MASTG-TEST-0338
- MASTG-TEST-0339
---

# MASVS-CODE-4

## Control

The app validates and sanitizes all untrusted inputs.

## Description

Apps have many data entry points including the UI, IPC, the network, the file system, etc. This incoming data might have been inadvertently modified by untrusted actors and may lead to bypass of critical security checks as well as classical injection attacks such as SQL injection, XSS or insecure deserialization. This control ensures that this data is treated as untrusted input and is properly verified and sanitized before it's used.
