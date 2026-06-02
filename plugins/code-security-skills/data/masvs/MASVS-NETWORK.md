---
title: 'MASVS-NETWORK: Network Communication'
masvs_group: MASVS-NETWORK
group_overview: true
controls:
- MASVS-NETWORK-1
- MASVS-NETWORK-2
---

# MASVS-NETWORK — Network Communication

MASVS-NETWORK covers how the app secures traffic to remote endpoints — TLS configuration, certificate validation, and certificate pinning. Misconfiguration here allows MITM attacks against any TLS-bearing endpoint.

## What this group covers

- TLS configuration (cleartext allowed, minimum protocol version)
- Certificate validation (custom TrustManager / URLSessionDelegate logic)
- Certificate pinning
- Mixed-content handling in WebViews

## Controls

- `MASVS-NETWORK-1` — secure TLS configuration and certificate validation
- `MASVS-NETWORK-2` — certificate pinning where applicable

See individual control files for `when_to_use`, `threats`, `static_signals`, and `mastg_tests`.
