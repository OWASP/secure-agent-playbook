---
title: 'MASVS-NETWORK-1: The app secures all network traffic according to the current
  best practices.'
masvs_group: MASVS-NETWORK
masvs_control: MASVS-NETWORK-1
summary: The app secures all network traffic according to the current best practices.
platforms:
- android
- ios
when_to_use:
- reviewing the app's HTTP or HTTPS client setup
- auditing custom TrustManager or URLSessionDelegate implementations
- validating TLS configuration and minimum protocol version
threats:
- MITM attack against a tampered or rogue CA on the device
- TLS downgrade to HTTP via misconfigured network security config
- acceptance of any server certificate via trust-all delegate
mastg_tests:
- MASTG-TEST-0024
- MASTG-TEST-0025
static_signals:
  android:
  - network_security_config.xml permits cleartext or any-CA trust
  - custom TrustManager that accepts any cert (X509TrustManager.checkServerTrusted
    no-op)
  - OkHttp client without CertificatePinner
  - android:usesCleartextTraffic="true" in manifest
  ios:
  - NSAllowsArbitraryLoads=true in NSAppTransportSecurity
  - URLSessionDelegate.urlSession(_:didReceive:completionHandler:) calls completionHandler(.useCredential)
    without trust evaluation
  - Missing NSPinnedDomains entries in Info.plist
  - Custom SecPolicy that does not match the expected hostname
resilience_static_only: false
static_only: false
---

# MASVS-NETWORK-1

## Control

The app secures all network traffic according to the current best practices.

## Description

Ensuring data privacy and integrity of any data in transit is critical for any app that communicates over the network. This is typically done by encrypting data and authenticating the remote endpoint, as TLS does. However, there are many ways for a developer to disable the platform secure defaults, or bypass them completely by using low-level APIs or third-party libraries. This control ensures that the app is in fact setting up secure connections in any situation.
