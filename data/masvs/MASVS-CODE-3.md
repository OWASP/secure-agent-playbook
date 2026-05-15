---
title: 'MASVS-CODE-3: The app only uses software components without known vulnerabilities.'
masvs_group: MASVS-CODE
masvs_control: MASVS-CODE-3
summary: The app only uses software components without known vulnerabilities.
platforms:
- android
- ios
when_to_use:
- reviewing dependency manifests and lockfiles for known CVEs
- cross-referencing with sca-audit for vulnerability checking
threats:
- importing libraries with known RCE or auth-bypass CVEs
- abandoned pods or packages with no maintainer responses
- transitive vulnerabilities from indirect dependencies
mastg_tests:
- MASTG-TEST-0041
static_signals:
  android:
  - outdated dependency versions in build.gradle or build.gradle.kts
  - gradle.lockfile showing libraries with known CVEs (cross-ref sca-audit)
  - use of abandoned or unmaintained libraries
  ios:
  - Podfile.lock or Package.resolved showing libraries with known CVEs
  - abandoned pods (no GitHub commits in 2+ years)
  - cross-ref sca-audit for CVE matching
resilience_static_only: false
static_only: false
---

# MASVS-CODE-3

## Control

The app only uses software components without known vulnerabilities.

## Description

To be truly secure, a full whitebox assessment should have been performed on all app components. However, as it usually happens with e.g. for third-party components this is not always feasible and not typically part of a penetration test. This control covers "low-hanging fruit" cases, such as those that can be detected just by scanning libraries for known vulnerabilities.
