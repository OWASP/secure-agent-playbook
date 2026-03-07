---
name: prompt-injection-test
description: Test LLM-integrated applications against known prompt injection techniques, evasion methods, and attack intents using the Arcanum PI Taxonomy. Use when red-teaming AI apps, validating guardrails, or deepening LLM01 (Prompt Injection) assessments.
license: CC-BY-4.0
---

# Prompt Injection Testing

Systematically test an LLM application's prompt injection defenses by following the full procedure in `plays/tier4-ai-security/prompt-injection-testing.md`.

> Based on the [Arcanum PI Taxonomy](https://github.com/Arcanum-Sec/arc_pi_taxonomy) by Jason Haddix (Arcanum Information Security). CC BY 4.0.

## Steps

1. **Scope and Input Surface Mapping** — Identify all paths where attacker-controlled content reaches the LLM: direct (chat, API params) and indirect (file uploads, web fetches, RAG docs, tool outputs, MCP resources).

2. **Test by Attack Intent** (13 intents) — For each authorized intent, attempt to achieve the attacker's goal:
   - INT-01 System Prompt Leak, INT-02 Jailbreak, INT-03 Tool Enumeration
   - INT-04 API Enumeration, INT-05 Get Prompt Secret, INT-06 Attack Users
   - INT-07 Data Poisoning, INT-08 Denial of Service, INT-09 Discuss Harm
   - INT-10 Multi-Chain Attacks, INT-11 Generate Image, INT-12 Test Bias
   - INT-13 Business Integrity

3. **Test by Attack Technique** (18 techniques) — Apply known payload construction methods:
   - Framing, Narrative Smuggling, Cognitive Overload, Meta-Prompting
   - Russian Doll, Memory Exploitation, Act as Interpreter, Contradiction
   - End Sequences, Inversion, Rule Addition, Variable Expansion
   - Link Injection, Puzzling, Anti-Harm Coercion, ASCII/Spatial
   - Binary Streams, Spatial Byte Arrays

4. **Apply Evasion Layers** (20 evasions) — When techniques are blocked, retry with obfuscation:
   - Encoding: base64, hex, morse, cipher, reverse
   - Language: alt language, fictional language, phonetic substitution, emoji
   - Structural: JSON/XML wrapping, markdown, metacharacter confusion, whitespace, splats
   - Advanced: steganography, link smuggling, graph nodes, waveforms, case changing

5. **Execute Test Matrix** — Combine intents x techniques x evasions. Prioritize: high-impact intents first, indirect surfaces second, evasion sweeps against defenses that blocked direct attempts.

6. **Assess Results** — For each successful injection, document: severity, attack path (intent + technique + evasion + surface), exact payload, detection gap, and remediation.

7. **Defense Validation** — Check the 5-layer defense checklist: ecosystem hardening, model guardrails, prompt-layer defenses, data-layer controls, application-layer validation.

## Output

Test results summary table (intent / technique / evasion / surface / result / severity), detailed findings using `templates/finding.md`, defense coverage checklist with gaps highlighted, and prioritized recommendations.

## OWASP References

- LLM01: Prompt Injection
- LLM02: Insecure Output Handling
- LLM06: Excessive Agency
- LLM07: System Prompt Leakage
