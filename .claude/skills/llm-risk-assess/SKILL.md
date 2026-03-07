---
name: llm-risk-assess
description: Comprehensive LLM security assessment against OWASP Top 10 for LLM Applications 2025. Use when reviewing LLM-integrated applications, RAG pipelines, chatbots, AI agents, or GenAI features. Covers prompt injection, data poisoning, supply chain, excessive agency, and more with real-world attack scenarios and testing methodologies.
allowed-tools: Read, Grep, Glob, Bash, WebFetch, Agent
---

# LLM Risk Assessment (2025)

Comprehensive evaluation of LLM applications against OWASP Top 10 for LLM Applications 2025. Follow the detailed procedure in `plays/tier4-ai-security/llm-risk-assess.md`.

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
   - **LLM01 Prompt Injection** — Direct/indirect injection, jailbreaks, goal hijacking, delimiter bypasses
   - **LLM02 Sensitive Information Disclosure** — Training data leakage, PII exposure, system info extraction, memorized secrets
   - **LLM03 Supply Chain** — Model poisoning, malicious dependencies, insecure plugins, provenance issues
   - **LLM04 Data and Model Poisoning** — Training data poisoning, RAG poisoning, embedding manipulation
   - **LLM05 Improper Output Handling** — XSS, command injection, SQLi, path traversal via LLM outputs
   - **LLM06 Excessive Agency** — Unauthorized tool calls, permission escalation, dangerous action chains
   - **LLM07 System Prompt Leakage** — Prompt extraction attacks, secret disclosure, instruction reverse engineering
   - **LLM08 Vector and Embedding Weaknesses** — Adversarial embeddings, retrieval poisoning, similarity attacks
   - **LLM09 Misinformation** — Hallucinations, authoritative presentation, grounding failures, harmful domains
   - **LLM10 Unbounded Consumption** — Token exhaustion, cost attacks, resource exhaustion, DoS

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
