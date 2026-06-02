---
title: 'MASVS-PLATFORM: Platform Interaction'
masvs_group: MASVS-PLATFORM
group_overview: true
controls:
- MASVS-PLATFORM-1
- MASVS-PLATFORM-2
- MASVS-PLATFORM-3
---

# MASVS-PLATFORM — Platform Interaction

MASVS-PLATFORM covers how the app interacts with the underlying OS — IPC (intents, URL schemes, custom URI schemes), WebView bridges, deep links, and platform UI features (screenshot prevention, pasteboard hygiene). Failures here typically allow other apps or web content to invoke the app in unintended ways.

## What this group covers

- Exported components and IPC permissions
- Deep-link / URL scheme validation
- WebView native-bridge security
- UI side-channels (screen capture, pasteboard)

## Controls

- `MASVS-PLATFORM-1` — IPC mechanisms are secured (export, permissions, validation)
- `MASVS-PLATFORM-2` — WebView and bridges are configured to resist injection
- `MASVS-PLATFORM-3` — UI is protected against side-channel observation

See individual control files for `when_to_use`, `threats`, `static_signals`, and `mastg_tests`.
