---
title: 'MASVS-RESILIENCE: Resilience Against Reverse-Engineering'
masvs_group: MASVS-RESILIENCE
group_overview: true
controls:
- MASVS-RESILIENCE-1
- MASVS-RESILIENCE-2
- MASVS-RESILIENCE-3
- MASVS-RESILIENCE-4
---

# MASVS-RESILIENCE — Resilience Against Reverse-Engineering

MASVS-RESILIENCE covers defenses against reverse-engineering, tampering, and runtime attacks: root/jailbreak detection, anti-debugging, anti-tamper, code obfuscation. **This play inspects static signals only** (build flags, library presence, manifest declarations); true resilience verification requires runtime/binary testing and is deferred to a future Tier 3 `mobile-dynamic-test` skill.

## What this group covers

- Debug/release build hygiene (debuggable, ProGuard/R8, symbols)
- Root/jailbreak detection presence
- Anti-debug code paths
- Anti-tamper / integrity checks

## Controls

- `MASVS-RESILIENCE-1` — the app detects and reacts to a tampered runtime
- `MASVS-RESILIENCE-2` — the app impedes static and dynamic analysis (obfuscation, anti-debug)
- `MASVS-RESILIENCE-3` — the app detects and reacts to root/jailbreak
- `MASVS-RESILIENCE-4` — the app verifies the integrity of its own code at runtime

See individual control files for `when_to_use`, `threats`, `static_signals`, and `mastg_tests`.
