---
title: 'MASVS-CODE-4: The app validates and sanitizes all untrusted inputs.'
masvs_group: MASVS-CODE
masvs_control: MASVS-CODE-4
summary: The app validates and sanitizes all untrusted inputs.
platforms:
- android
- ios
when_to_use:
- reviewing data crossing trust boundaries (network to app, IPC to app, JS bridge
  to native)
- auditing use of dangerous serialization or shell execution APIs
- checking error and exception handling paths for injection risks
threats:
- command injection via Runtime.exec with user-controlled input
- deserialization of untrusted data leading to RCE
- format-string injection via user-controlled format arguments
mastg_tests:
- MASTG-TEST-0044
static_signals:
  android:
  - Runtime.exec(...) with concatenated user input
  - ObjectInputStream.readObject() of untrusted data
  - WebView.evaluateJavascript(...) with user-controlled strings
  - reflection (Class.forName) with user-controlled class names
  ios:
  - String(format:) or NSString(format:) with user-controlled format strings
  - NSKeyedUnarchiver.unarchiveTopLevelObjectWithData(...) of untrusted data
  - NSExpression.expressionWithFormat(...) from user input
resilience_static_only: false
static_only: false
---

# MASVS-CODE-4

## Control

The app validates and sanitizes all untrusted inputs.

## Description

Apps have many data entry points including the UI, IPC, the network, the file system, etc. This incoming data might have been inadvertently modified by untrusted actors and may lead to bypass of critical security checks as well as classical injection attacks such as SQL injection, XSS or insecure deserialization. This control ensures that this data is treated as untrusted input and is properly verified and sanitized before it's used.
