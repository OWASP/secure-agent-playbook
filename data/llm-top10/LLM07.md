---
title: "LLM07 Misinformation"
owasp_llm_id: "LLM07"
owasp_llm_version: "2026"
when_to_use:
  - reviewing AI systems whose output informs business, legal, clinical, or financial decisions
  - assessing coding assistants for hallucinated dependencies
  - evaluating RAG grounding and citation integrity
  - reviewing agent workflows where inferred state drives downstream action
  - assessing multi-agent systems for misinformation propagation
  - auditing human and system overreliance on fluent output
threats:
  - unsupported or false decision support
  - incorrect state inference triggering unintended actions
  - fabricated code and hallucinated package names
  - misleading summaries omitting constraints, exceptions, or risks
  - adversarially induced misinformation
  - cross-agent misinformation propagation
  - forged or misattributed evidence
  - overreliance on fluent, confident, well-structured output
summary: "An LLM produces incorrect, incomplete, unsupported, or misleading information credible enough to influence a human decision, an automated workflow, or an agent action. The core risk is that the incorrect output is trusted and acted upon."
aisvs_mappings:
  - section: "C1.3"
    title: "Training Data Quality and Security Assurance"
    requirements: ["1.3.3"]
  - section: "C7.1"
    title: "Output Format Enforcement"
    requirements: ["7.1.1"]
  - section: "C7.2"
    title: "Hallucination Detection & Mitigation"
    requirements: ["7.2.1", "7.2.2", "7.2.3"]
  - section: "C7.4"
    title: "Source Attribution & Citation Integrity"
    requirements: ["7.4.1", "7.4.2", "7.4.3", "7.4.4"]
  - section: "C8.1"
    title: "Access Controls on Memory & RAG Indices"
    requirements: ["8.1.3"]
  - section: "C9.2"
    title: "High-Impact Action Approval and Irreversibility Controls"
    requirements: ["9.2.1", "9.2.3"]
  - section: "C9.5"
    title: "Agent Authorization, Delegation, and Continuous Enforcement"
    requirements: ["9.5.1", "9.5.3"]
  - section: "C11.1"
    title: "Model Alignment, Safety, and Robustness Testing and Training"
    requirements: ["11.1.2"]
  - section: "C11.2"
    title: "Membership-Inference and Model-Inversion Mitigation"
    requirements: ["11.2.3"]
  - section: "C12.3"
    title: "Model, Data, and Performance Drift Detection"
    requirements: ["12.3.2", "12.3.3", "12.3.4"]
---

# LLM07:2026 Misinformation

> **Condensed summary — not OWASP's verbatim text.** This file restates [LLM07:2026](https://github.com/GenAI-Security-Project/GenAI-LLM-Top10/blob/main/2026/final/LLM07_Misinformation.md) in condensed form for agent use. Facts, figures, and scope boundaries are preserved; wording is not. The `AISVS Controls` table and `aisvs_mappings` are derived by this repo at requirement granularity — upstream's [official appendix](https://github.com/GenAI-Security-Project/GenAI-LLM-Top10/blob/main/2026/final/LLMZZ_Appendix_AISVS_Mapping.md) maps at chapter granularity only. Quote the source, not this file.

## Description

Misinformation occurs when an LLM or LLM-enabled application produces incorrect, incomplete, unsupported, or misleading information that appears credible enough to influence a human decision, an automated workflow, or an agent action. **The core risk is that the incorrect output is trusted and acted upon.**

In modern systems, model outputs drive tool calls, generate code, infer system state, authorize actions, and coordinate across agents. This makes misinformation a **system-level failure** that can lead to financial loss, security incidents, safety risks, or operational disruption. In agentic systems it often manifests as incorrect state, reasoning, or evidence consumed by downstream components, leading directly to unintended actions.

Misinformation can arise from hallucination, incomplete or stale context, weak grounding, ambiguous prompts, biased or corrupted data, misleading summaries, or unvalidated tool outputs. It can also be deliberately induced. Where the root cause is prompt injection, poisoning, or supply chain compromise, reference those risks separately: execution of unsafe generated code is [LLM10](LLM10.md), and registration of hallucinated package names as a supply-chain vector is [LLM04](LLM04.md). This entry focuses on the resulting failure mode — a false representation that drives a harmful decision or action.

**Overreliance remains a key factor.** Humans and systems treat fluent, confident, or well-structured outputs as authoritative. In agentic architectures this overreliance is frequently embedded in system design.

## Potential Impacts

- Financial loss from incorrect policy, refund, or payment decisions
- Safety harm in clinical, legal, or operational domains
- Security incidents from false alerts or fabricated task completion
- Supply-chain compromise via installed hallucinated packages
- Cascading failure as false state propagates across agents

## Common Examples of Risk

1. **Unsupported or false decision support** — incorrect information influences business, legal, healthcare, financial, or operational decisions.
2. **Incorrect state inference in workflows** — the LLM infers a condition has been met when it has not, triggering unintended actions.
3. **Incorrect or fabricated code and dependencies** — the model produces incorrect code recommendations or references non-existent (hallucinated) packages.
4. **Misleading summaries and critical omissions** — summaries omit key constraints, exceptions, timestamps, or risks.
5. **Adversarially induced misinformation** — attackers craft inputs causing false claims or omission of critical facts.
6. **Cross-agent misinformation propagation** — incorrect outputs propagate across agents and workflows.
7. **Forged or misattributed evidence** — fabricated or manipulated content presented as authoritative.

## Prevention and Mitigation

| # | Strategy | Description |
|---|----------|-------------|
| 1 | Ground claims before action | Require outputs to be grounded in authoritative and current sources. |
| 2 | Implement claim-check-act patterns | Separate generation from execution and verify claims before acting. |
| 3 | Validate tool calls | Check arguments, authorization, preconditions, and current state before execution. |
| 4 | Use verification signals, not just confidence | Incorporate groundedness and consistency checks. |
| 5 | Enforce runtime verification for high-impact actions | Approval workflows and system checks. |
| 6 | Detect and prevent omission failures | Require structured outputs with mandatory fields. |
| 7 | Limit blast radius | Least privilege, sandboxing, and rate limits. |
| 8 | Monitor and test for misinformation | Log claims, evidence, and outcomes; test adversarial scenarios. |
| 9 | Calibrate human and system trust | Distinguish verified facts from assumptions. |
| 10 | Adversarial evaluation and continuous testing | Regularly test workflows against misleading scenarios. |

## Example Attack Scenarios

1. **Hallucinated dependency recommendation** — a coding assistant recommends a plausible but non-existent package that an attacker pre-registered under the hallucinated name.
2. **Incorrect policy decision by agent** — a customer-service agent misreads a policy and approves a refund violating the terms.
3. **Omission in safety-critical summary** — a clinical summary omits a drug contraindication and a clinician acts on the incomplete recommendation.
4. **Adversarially induced false reasoning** — an attacker seeds a support forum with false remediation steps that a troubleshooting agent retrieves and repeats.
5. **False alert triggers automated response** — a security agent misclassifies normal traffic as intrusion and blocks a production network segment.
6. **Cross-agent trust failure** — a retrieval agent reports a customer as identity-verified when it is not, and a downstream payment agent releases funds.
7. **Fabricated task completion** — an agent reports a nightly database backup completed when it never ran, and a later restore fails.

## AISVS Controls

| AISVS Section | Control | Key Requirements |
|---------------|---------|-----------------|
| C1.3 Training Data Quality and Security Assurance | Bias evaluation for models used in security-relevant decisions | 1.3.3 |
| C7.1 Output Format Enforcement | Schema validation with rejection on mismatch — supports mandatory-field checks against omission | 7.1.1 |
| C7.2 Hallucination Detection & Mitigation | Confidence estimation, blocking or fallback below threshold, extra verification for high-risk responses | 7.2.1, 7.2.2, 7.2.3 |
| C7.4 Source Attribution & Citation Integrity | RAG attribution derived from **retrieval metadata rather than generated by the model**, claim traceability, media watermarking | 7.4.1–7.4.4 |
| C8.1 Access Controls on Memory & RAG Indices | Scope constraints on retrieval so grounding draws from the intended corpus | 8.1.3 |
| C9.2 High-Impact Action Approval | Approval gate before high-impact action; reversibility classification | 9.2.1, 9.2.3 |
| C9.5 Agent Authorization & Delegation | Runtime-enforced tool and parameter authorization; access decisions never made by the model | 9.5.1, 9.5.3 |
| C11.1 Alignment, Safety & Robustness Testing | Version-controlled alignment test suite run on every model update | 11.1.2 |
| C11.2 Membership-Inference & Model-Inversion Mitigation | Output calibration reducing overconfident predictions | 11.2.3 |
| C12.3 Model, Data & Performance Drift Detection | Hallucination detection monitors, hallucination rate as a time-series metric, distinguishing unexplained shifts from expected drift | 12.3.2, 12.3.3, 12.3.4 |

## Related Frameworks

- AML.T0048 — External Harms (MITRE ATLAS)
- ASI08 — Cascading Failures (OWASP Top 10 for Agentic Applications)

## References

- [OWASP GenAI LLM Top 10 2026](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/)
- [We Have a Package for You! A Comprehensive Analysis of Package Hallucinations by Code Generating LLMs](https://arxiv.org/abs/2406.10279)
- [NIST AI 600-1: Generative AI Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)
