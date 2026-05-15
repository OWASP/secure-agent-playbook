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
when_to_use: []
threats: []
mastg_tests: []
static_signals:
  android: []
  ios: []
resilience_static_only: false
static_only: false
---

# MASVS-AUTH-1

## Control

The app uses secure authentication and authorization protocols and follows the relevant best practices.

## Description

Most apps connecting to a remote endpoint require user authentication and also enforce some kind of authorization. While the enforcement of these mechanisms must be on the remote endpoint, the apps also have to ensure that it follows all the relevant best practices to ensure a secure use of the involved protocols.
