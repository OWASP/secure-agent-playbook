---
name: llm-risk-assess
description: Assess LLM-powered applications against the OWASP Top 10 for LLM Applications. Use when reviewing code that integrates LLM APIs (OpenAI, Anthropic, etc.), RAG pipelines, chatbots, AI assistants, or any LLM-based feature before deployment.
license: CC-BY-4.0
---

# LLM Risk Assessment

Evaluate an LLM application against all 10 risk categories by following the full procedure in `plays/tier4-ai-security/llm-risk-assess.md`.

## Steps

1. **Architecture Mapping** — Identify model provider, input flow (user -> preprocessing -> prompt -> LLM), output flow (LLM -> postprocessing -> rendering/action), data sources (RAG, tools, context), and action surface (tool calls, APIs, code execution).

2. **Assess Each LLM Top 10 Risk**:
   - **LLM01 Prompt Injection** — Direct and indirect injection via user input, RAG documents, tool outputs
   - **LLM02 Insecure Output Handling** — LLM output rendered as HTML (XSS), passed to shell (command injection), used in queries (SQLi), used in file paths
   - **LLM03 Training Data Poisoning** — Fine-tuning on untrusted data, RAG knowledge base poisoning
   - **LLM04 Model Denial of Service** — Missing token limits, rate limiting, timeouts, cost caps
   - **LLM05 Supply Chain** — Untrusted model sources, unaudited dependencies (LangChain, LlamaIndex), interceptable endpoints
   - **LLM06 Excessive Agency** — Unvalidated tool calls, missing human-in-the-loop, overpermissioned tools
   - **LLM07 System Prompt Leakage** — Extractable system prompts, secrets in prompts, harmful instructions if leaked
   - **LLM08 Vector and Embedding Weaknesses** — Vector DB access controls, adversarial embedding inputs, retrieval validation
   - **LLM09 Misinformation** — LLM output presented as authoritative, missing grounding, harmful hallucination domains
   - **LLM10 Unbounded Consumption** — Missing cost monitoring, per-user limits, batch rate limiting

3. **Synthesize Findings** — Assign severity based on exploitability and deployment context. Provide code locations and concrete remediation.

## Output

Architecture overview, risk matrix (all 10 categories with status), detailed findings using `templates/finding.md`, positive controls observed, and prioritized recommendations.

## OWASP References

- OWASP Top 10 for LLM Applications v2.0
- OWASP AI Exchange (owaspai.org)
- OWASP AI Testing Guide
