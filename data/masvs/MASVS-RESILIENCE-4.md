---
title: 'MASVS-RESILIENCE-4: The app implements anti-dynamic analysis techniques.'
masvs_group: MASVS-RESILIENCE
masvs_control: MASVS-RESILIENCE-4
summary: The app implements anti-dynamic analysis techniques.
mastg_tests:
- MASTG-TEST-0046
- MASTG-TEST-0048
- MASTG-TEST-0089
- MASTG-TEST-0091
- MASTG-TEST-0226
- MASTG-TEST-0227
- MASTG-TEST-0261
---

# MASVS-RESILIENCE-4

## Control

The app implements anti-dynamic analysis techniques.

## Description

Sometimes pure static analysis is very difficult and time consuming so it typically goes hand in hand with dynamic analysis. Observing and manipulating an app during runtime makes it much easier to decipher its behavior. This control aims to make it as difficult as possible to perform dynamic analysis, as well as prevent dynamic instrumentation which could allow an attacker to modify the code at runtime.
