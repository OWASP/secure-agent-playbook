---
title: 'MASVS-PRIVACY-4: The app offers user control over their data.'
masvs_group: MASVS-PRIVACY
masvs_control: MASVS-PRIVACY-4
summary: The app offers user control over their data.
platforms:
- android
- ios
when_to_use:
- reviewing in-app privacy settings and data-management flows
- auditing data-deletion and data-export implementations
threats:
- user has no mechanism to revoke previously granted permissions
- data deletion flow does not actually remove data from third-party services
mastg_tests:
- MASTG-TEST-0263
static_signals:
  android:
  - absence of in-app privacy-settings UI
  - delete-account flow that does not call third-party SDK reset() or opt-out APIs
  ios:
  - absence of privacy-settings UI in-app
  - deletion flows that do not invoke third-party SDK reset methods
resilience_static_only: false
static_only: false
---

# MASVS-PRIVACY-4

## Control

The app offers user control over their data.

## Description

Users should have control over their data. This control ensures that apps provide mechanisms for users to manage, delete, and modify their data, and change privacy settings as needed (e.g. to revoke consent). Additionally, apps should re-prompt for consent and update their transparency disclosures when they require more data than initially specified.
