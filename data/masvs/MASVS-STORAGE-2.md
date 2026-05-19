---
title: 'MASVS-STORAGE-2: The app prevents leakage of sensitive data.'
masvs_group: MASVS-STORAGE
masvs_control: MASVS-STORAGE-2
summary: The app prevents leakage of sensitive data.
mastg_tests:
- MASTG-TEST-0011
- MASTG-TEST-0060
- MASTG-TEST-0203
- MASTG-TEST-0206
- MASTG-TEST-0215
- MASTG-TEST-0216
- MASTG-TEST-0231
- MASTG-TEST-0258
- MASTG-TEST-0281
- MASTG-TEST-0296
- MASTG-TEST-0297
- MASTG-TEST-0298
- MASTG-TEST-0313
- MASTG-TEST-0314
- MASTG-TEST-0315
- MASTG-TEST-0318
- MASTG-TEST-0319
---

# MASVS-STORAGE-2

## Control

The app prevents leakage of sensitive data.

## Description

There are cases when sensitive data is unintentionally stored or exposed to publicly accessible locations; typically as a side-effect of using certain APIs, system capabilities such as backups or logs. This control covers this kind of unintentional leaks where the developer actually has a way to prevent it.
