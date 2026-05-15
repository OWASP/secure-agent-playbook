---
title: 'MASVS-RESILIENCE-3: The app implements anti-static analysis mechanisms.'
masvs_group: MASVS-RESILIENCE
masvs_control: MASVS-RESILIENCE-3
summary: The app implements anti-static analysis mechanisms.
platforms:
- android
- ios
when_to_use:
- reviewing build-time obfuscation and symbol stripping configuration
- verifying that release builds cannot be trivially reverse-engineered
threats:
- trivial reverse-engineering via unobfuscated class and method names
- business logic extraction from unstripped binaries
mastg_tests:
- MASTG-TEST-0048
- MASTG-TEST-0049
static_signals:
  android:
  - missing or empty proguard-rules.pro
  - R8 disabled in release builds
  - android:debuggable="true" in release manifest
  - no isDebuggerAttached checks in sensitive code paths
  ios:
  - symbols not stripped from release binary
  - bitcode or debug info shipped in production build
  - absence of ptrace(PT_DENY_ATTACH) call
  - no sysctl(KERN_PROC, KERN_PROC_PID) debugger detection
resilience_static_only: true
static_only: false
---

# MASVS-RESILIENCE-3

## Control

The app implements anti-static analysis mechanisms.

## Description

Understanding the internals of an app is typically the first step towards tampering with it (either dynamically, or statically). This control tries to impede comprehension by making it as difficult as possible to figure out how an app works using static analysis.
