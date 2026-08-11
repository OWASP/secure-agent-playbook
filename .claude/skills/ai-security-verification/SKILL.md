---
name: ai-security-verification
description: Comprehensive AI security verification using OWASP AI Security Verification Standard (AISVS) v1.0. Provides a structured checklist to verify security controls across the 12 chapters of AISVS, from training data integrity through input validation, agentic orchestration, MCP security, adversarial robustness, and monitoring.
allowed-tools: Read, Grep, Glob, Bash, WebFetch, Agent
---

# AI Security Verification Standard (AISVS)

Conduct comprehensive security verification of AI-driven applications using the OWASP AI
Security Verification Standard **v1.0** (June 2026) — 12 chapters, 44 sections, 191 testable
requirements across three verification levels.

## Scope First

Establish the target verification level before assessing. **L1** is the baseline for any
production AI system; **L2** is the standard for systems handling sensitive data or taking
consequential actions; **L3** covers high-assurance and regulated deployments. Report the
target level — a gap against an L3 requirement in an L1-scoped system is informational.

Mark chapters **N/A** with justification where they do not apply (e.g. C1 for systems that
consume only third-party hosted models, C10 where MCP is not in use, C9 for non-agentic
systems).

## Steps

1. **C1 — Training Data Integrity & Traceability** — Verify the training-data source
   inventory, data minimization, integrity in storage and transit, labeling platform access
   control and artifact integrity, poisoning detection, and pre-training content filtering.

2. **C2 — Input Validation** — Verify input normalization, encoding-smuggling detection,
   prompt-injection screening with blocking, length rejection (not truncation), character
   allow-lists, instruction hierarchy, special-token handling, and content/policy screening
   including non-text and cross-modal inputs.

3. **C3 — Model Lifecycle Management & Change Control** — Verify the model registry,
   artifact signing and verification at admission and load, pre-deployment safety testing,
   quantization re-evaluation, rollout/rollback, environment separation, and integrity across
   RLHF and multi-stage fine-tuning.

4. **C4 — Infrastructure, Configuration & Deployment Security** — Verify model sandboxing,
   allow-listed serialization formats, workload attestation, accelerator firmware and memory
   isolation, and edge/on-device authentication, signing, and weight encryption.

5. **C5 — Access Control & Identity** — Verify step-up authentication for high-risk AI
   operations, default-deny on AI resources, end-user authorization context enforced through
   retrieval pipelines, post-inference filtering, PDP isolation, just-in-time privilege,
   label propagation, and multi-tenant isolation.

6. **C6 — Supply Chain Security for Models** — Verify malicious-code scanning, approved
   download sources, artifact integrity verification, behavioral acceptance testing, and
   signed, complete AI BOMs.

7. **C7 — Model Behavior, Output Control & Safety Assurance** — Verify output schema
   validation and bounds, confidence estimation with low-confidence fallback, harmful-content
   and system-prompt-disclosure filtering, prevention of model-triggered outbound requests,
   and metadata-derived RAG attribution.

8. **C8 — Memory, Embeddings & Vector Database Security** — Verify per-tenant namespace
   uniqueness, immutable document metadata, scoped retrieval, pre-embedding sensitive-field
   masking, quarantine of anomalous vectors, validated memory writes, and expiry/revocation.

9. **C9 — Orchestration & Agentic Security** — Verify execution budgets and kill-switches,
   deterministic approval gates for high-impact and irreversible actions, faithful approval
   parameter display, tool sandboxing and manifest enforcement, isolation of untrusted-data
   processing from tool calling, agent cryptographic identity, fine-grained runtime
   authorization including parameter values, secrets kept out of model context, and
   fail-closed shutdown paths.

10. **C10 — Model Context Protocol (MCP) Security** — Verify trusted and allow-listed MCP
    components, sandboxed local servers, per-request token validation with OAuth 2.1 claim
    checks, no token pass-through, per-invocation authorization down to argument values,
    secure transport with Origin/Host validation, response schema validation and injection
    screening, replay detection, and re-approval on tool definition change.

11. **C11 — Adversarial Robustness** — Verify alignment and safety training, a
    version-controlled alignment test suite run per release, modality-relevant adversarial
    evaluation, membership-inference and model-inversion mitigations, extraction detection
    and response, and pre-inference anomaly gating.

12. **C12 — Monitoring, Logging & Anomaly Detection** — Verify AI interaction and policy
    decision logging, structured inference schemas, RAG retrieval logging, detection of
    jailbreak/injection/extraction patterns, granular token attribution, drift and
    hallucination monitoring, proactive-action audit trails, and immutable lifecycle records.

## Output

Use the finding format from `templates/finding.md`, with the **OWASP Ref** field carrying the
AISVS requirement ID (e.g. `AISVS v1.0 C9.2.1`). Produce:

- **AISVS Compliance Assessment** — Verification status across all 12 chapters at the stated target level
- **Security Control Evaluation** — Detailed analysis of implemented controls
- **Gap Analysis** — Missing or inadequate security measures, cited by requirement ID
- **Risk-Based Prioritization** — Critical findings requiring immediate attention
- **Compliance Roadmap** — Structured plan to reach the target verification level
- **Verification Evidence** — Documentation, test output, and configuration supporting each claim

## OWASP References

- **OWASP AI Security Verification Standard (AISVS) v1.0** — [github.com/OWASP/AISVS](https://github.com/OWASP/AISVS)
- OWASP Top 10 for LLM Applications 2025
- OWASP Top 10 for Agentic Applications 2026
- OWASP Agentic AI Threats and Mitigations
- OWASP MCP Security Cheat Sheet
- OWASP AI Testing Guide
- OWASP Application Security Verification Standard (ASVS)
- Full procedure: `plugins/ai-security-skills/plays/ai-security-verification.md`
