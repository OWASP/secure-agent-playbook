---
title: 'MASVS-AUTH-1: The app uses secure authentication and authorization protocols
  and follows the relevant best practices.'
masvs_group: MASVS-AUTH
masvs_control: MASVS-AUTH-1
summary: The app uses secure authentication and authorization protocols and follows
  the relevant best practices.
platforms:
- android
- ios
when_to_use:
- reviewing OAuth, OIDC, or JWT authentication flows
- auditing remote authentication endpoints from the mobile client side
- validating PKCE on OAuth public clients
threats:
- account takeover via missing JWT signature verification
- auth-code interception on public clients without PKCE
- token leakage via URL fragments
mastg_tests:
- MASTG-TEST-0017
static_signals:
  android:
  - JWT decoded with Jwts.parser().setSigningKey(...) using a hard-coded key
  - JWT.decode(...) without verify(...)
  - OAuth code flows without PKCE — no code_verifier / code_challenge
  ios:
  - JWT decoded with JWTDecode.swift without signature check
  - OAuth public clients constructed without PKCE
  - auth tokens parsed from URL fragments rather than authorization code exchange
resilience_static_only: false
static_only: false
---

# MASVS-AUTH-1

## Control

The app uses secure authentication and authorization protocols and follows the relevant best practices.

## Description

Most apps connecting to a remote endpoint require user authentication and also enforce some kind of authorization. While the enforcement of these mechanisms must be on the remote endpoint, the apps also have to ensure that it follows all the relevant best practices to ensure a secure use of the involved protocols.
