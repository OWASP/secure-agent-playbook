---
name: llm-risk-assess
description: Comprehensive LLM security assessment against OWASP Top 10 for LLM Applications 2025. Use when reviewing LLM-integrated applications, RAG pipelines, chatbots, AI agents, or GenAI features. Covers prompt injection, data poisoning, supply chain, excessive agency, and more with real-world attack scenarios and testing methodologies.
allowed-tools: Read, Grep, Glob, Bash, WebFetch, Agent
---

# LLM Risk Assessment (2025)

Comprehensive evaluation of LLM applications against OWASP Top 10 for LLM Applications 2025. Follow the detailed procedure in `plays/llm-risk-assess.md`.

## Steps

1. **Architecture & Threat Modeling**
   - Map LLM provider (OpenAI, Anthropic, local models)
   - Document data flows: user input → preprocessing → prompt construction → LLM → output processing → actions
   - Identify RAG components, tool integrations, memory systems
   - Define trust boundaries and attack surfaces

2. **Automated Security Testing**
   - Run prompt injection probes (Garak, Giskard, custom scripts)
   - Test output handling vulnerabilities
   - Scan for secrets in prompts and configurations
   - Validate vector database security

3. **Assess All 10 OWASP LLM 2025 Risks** with attack scenarios:
   - **LLM01 Prompt Injection** — Direct/indirect injection, jailbreaks, multimodal and invisible-character payloads, memory and RAG poisoning
   - **LLM02 Sensitive Information Disclosure** — Training data leakage, PII exposure, reasoning-trace and tool-argument leakage, embedding inversion, side channels
   - **LLM03 Excessive Agency** — Excessive functionality, permissions, and autonomy; unauthorized tool calls, dangerous action chains
   - **LLM04 Supply Chain** — Tampered models, weak provenance, malicious adapters, conversion/quantization and build-pipeline compromise
   - **LLM05 Data and Model Poisoning** — Training, fine-tuning, and embedding poisoning; sleeper agents; non-weight artifact tampering
   - **LLM06 Unbounded Consumption** — Token exhaustion, denial of wallet, reasoning-loop exhaustion, model extraction
   - **LLM07 Misinformation** — Hallucinations, fabricated dependencies, incorrect state inference driving agent action
   - **LLM08 Hidden Context Exposure** — System prompt, tool schema, and control-logic extraction; guardrail reverse engineering
   - **LLM09 Vector and Embedding Weaknesses** — Retrieval poisoning, embedding inversion, cross-tenant leakage, cache poisoning
   - **LLM10 Improper Output Handling** — XSS, SQLi, RCE, ANSI injection, renderer-triggered exfiltration

4. **Red Team Testing**
   - Attempt real-world attack scenarios
   - Test defense bypasses and evasion techniques
   - Validate guardrails and safety controls

## Output

Comprehensive LLM security report:
- Architecture diagram with trust boundaries
- Risk matrix (all 10 categories with severity/status)
- Detailed findings with proof-of-concept examples
- Red team test results and bypass techniques
- Remediation roadmap with code examples
- Defense validation checklist

## OWASP References

- OWASP Top 10 for LLM Applications 2025
- OWASP AI Exchange (owaspai.org)
- OWASP AI Testing Guide
- OWASP Cheat Sheet: Prompt Injection Prevention
- OWASP Prompt Injection Taxonomy (Arcanum)
