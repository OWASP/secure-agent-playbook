---
title: "LLM02 Sensitive Information Disclosure"
owasp_llm_id: "LLM02"
owasp_llm_version: "2026"
when_to_use:
  - reviewing LLM apps that handle PII, PHI, credentials, or confidential data
  - assessing training and fine-tuning pipelines for memorization risk
  - evaluating RAG retrieval authorization and vector-store handling
  - auditing observability, logging, and reasoning-trace capture
  - assessing regulatory exposure (GDPR, HIPAA, CCPA, EU AI Act)
  - reviewing open-weights deployments where extraction runs offline
threats:
  - training-data memorization and verbatim extraction
  - inference-time disclosure of system prompt, RAG chunks, or another session's data
  - reasoning-trace and tool-argument leakage
  - embedding inversion reconstructing source documents
  - membership inference identifying training-set records
  - side channels (token length, latency, log-probabilities, KV-cache sharing)
  - observability platforms logging full prompts and completions by default
  - aggregation of individually-permitted sources into a prohibited conclusion
summary: "An LLM system exposes confidential, regulated, privileged, or proprietary data through an unauthorized channel. Disclosure surfaces include not just the final answer but tool arguments, reasoning traces, retrieved chunks, logs, embeddings, and observable inference properties."
aisvs_mappings:
  - section: "C1.1"
    title: "Training Data Origin & Data Security"
    requirements: ["1.1.1", "1.1.2"]
  - section: "C5.2"
    title: "AI Resource Authorization & Classification"
    requirements: ["5.2.1", "5.2.2", "5.2.3", "5.2.4", "5.2.7"]
  - section: "C5.3"
    title: "Multi-Tenant Isolation"
    requirements: ["5.3.1", "5.3.2"]
  - section: "C7.3"
    title: "Output Safety"
    requirements: ["7.3.1", "7.3.2", "7.3.4"]
  - section: "C8.2"
    title: "Embedding Sanitization & Validation"
    requirements: ["8.2.1"]
  - section: "C8.3"
    title: "Memory Expiry & Revocation"
    requirements: ["8.3.1", "8.3.2"]
  - section: "C9.5"
    title: "Agent Authorization, Delegation, and Continuous Enforcement"
    requirements: ["9.5.4"]
  - section: "C11.2"
    title: "Membership-Inference and Model-Inversion Mitigation"
    requirements: ["11.2.1", "11.2.2", "11.2.3", "11.2.4", "11.2.5"]
  - section: "C11.3"
    title: "Model-Extraction Defense"
    requirements: ["11.3.2"]
  - section: "C12.1"
    title: "Request & Response Logging"
    requirements: ["12.1.1", "12.1.2"]
---

# LLM02:2026 Sensitive Information Disclosure

> **Condensed summary — not OWASP's verbatim text.** This file restates [LLM02:2026](https://github.com/GenAI-Security-Project/GenAI-LLM-Top10/blob/main/2026/final/LLM02_SensitiveInformationDisclosure.md) in condensed form for agent use. Facts, figures, and scope boundaries are preserved; wording is not. The `AISVS Controls` table and `aisvs_mappings` are derived by this repo at requirement granularity — upstream's [official appendix](https://github.com/GenAI-Security-Project/GenAI-LLM-Top10/blob/main/2026/final/LLMZZ_Appendix_AISVS_Mapping.md) maps at chapter granularity only. Quote the source, not this file.

## Description

Sensitive information disclosure occurs when an LLM-integrated system exposes confidential, regulated, privileged, or proprietary data through a channel the data subject, controller, or system owner did not authorize. **The channel is not only the final answer**: tool-call arguments, reasoning traces, retrieved chunks, multimodal output, logs, telemetry, embeddings, and observable inference properties (timing, token length, log-probabilities, confidence, cache-hit behavior) are all disclosure surfaces. Treat each as an output subject to the same classification and redaction rules.

Disclosure arises across four phases:

1. **Training-time** — a model, fine-tune, or LoRA adapter memorizes corpus content and later reproduces it. Memorization scales log-linearly with capacity, duplication, and context length. Narrow adapters memorize rare examples with high fidelity.
2. **Inference-time** — the model discloses live context (system prompt, RAG chunks, files, tool outputs, memory, another session's data), often because summarization or extraction surfaces more than was asked, including visually-redacted spans.
3. **Pipeline-time** — fine-tuning, distillation, synthetic-data generation, gradients, SDKs, and observability move sensitive data into derived artifacts.
4. **Observation-time** — adversaries infer facts from externally measurable properties without receiving content.

Two structural failures drive most incidents. **Oversharing upstream**: unscoped drives, legacy permissions, and knowledge bases feed RAG with sensitive data the model then retrieves as designed — the fix is the data surface, not the model. **Persistence**: once data influences weights, embeddings, or adapters it stays extractable after source deletion, straining GDPR Article 17 and CCPA §1798.105 erasure obligations.

**Open-weights deployments cannot rely on rate limits** — extraction, membership inference, and inversion run offline at unbounded rates.

Severity should turn on what the recipient can learn, not on whether the leak looked like natural language.

## Potential Impacts

- Regulatory breach determinations under GDPR, HIPAA, CCPA/CPRA, and the EU AI Act (high-risk obligations from August 2026)
- Verbatim reproduction of copyrighted or licensed training material
- Cross-tenant and cross-client disclosure, including attorney-client privilege waiver events
- Credential and API-key exposure from system prompts and traces
- Re-identification of individuals in training data without any record being extracted

## Common Examples of Risk

1. **Training-data memorization and extraction** — the 2023 "poem" divergence attack drove `gpt-3.5-turbo` to emit more than 10,000 unique memorized examples for roughly USD 200. Fine-tuned models and their LoRA adapters are more extractable than base models of the same scale.
2. **Inference-time context and output disclosure** — treat reasoning traces and tool arguments as outputs, not debugging leftovers. Regex and blocklist filters fall to cross-lingual, base64, and hex encodings. **Aggregation** across individually-permitted sources (budget + hiring + diligence → a pending M&A target) is a disclosure when policy prohibits the synthesized conclusion.
3. **Embedding and representation disclosure** — modern inversion reconstructs plaintext from leaked vectors, so an "embeddings-only" backup is a source-document breach. Cosine similarity does not respect ACLs; authorize *before* retrieval.
4. **Multimodal disclosure** — vision models OCR credentials and PII from screenshots, notifications, and PDF metadata. Cross-modal transformation bypasses single-modality DLP.
5. **Inference-time side channels** — SPV-MIA raised membership-inference AUC to 0.9 against fine-tuned targets. Whisper Leak classified conversation topics at >98% AUPRC across 28 production models from encrypted traffic. Prompt leakage has been shown through KV-cache sharing in multi-tenant serving.
6. **Training-pipeline disclosure** — gradient inversion, distillation, and synthetic-data carryover move examples into derived models. Fixed-epsilon DP is necessary but not sufficient without rate-limiting and query-pattern detection.
7. **Platform and ecosystem disclosure** — observability platforms log full prompts, completions, chunks, and traces by default. DeepSeek's January 2025 ClickHouse exposure leaked more than one million rows of logs and API keys.

## Prevention and Mitigation

### Tier 1: Foundational (every deployment)

| # | Strategy | Description |
|---|----------|-------------|
| 1 | Govern corpora | Provenance, classification, deduplication across near-duplicates, transliterations, and format variants. Scrub PII at ingest. |
| 2 | Minimize context | Send only task-required fields. Disable auto-context (`customer_360`, full-record append) unless justified per template. |
| 3 | Authorize before retrieval | Enforce document- and chunk-level authorization *inside the index query*, not at the application layer after retrieval. |
| 4 | System-prompt hygiene | Never store secrets, credentials, or regulated data in system prompts. |
| 5 | Sanitize with classifiers, not regex alone | Pattern matching + NER + trained classifiers; regex fails on encoded and cross-lingual output. |
| 6 | Budget queries per user and session | Disrupt enumeration and membership probing on sensitive endpoints. |
| 7 | Operational hygiene | Restrict and scrub logs and traces before APM ingestion; encrypt in transit and at rest; technically enforce no-train/no-retain. |

### Tier 2: Hardening (regulated / high-sensitivity)

| # | Strategy | Description |
|---|----------|-------------|
| 8 | DP-SGD calibrated to sensitivity | Monitor overfitting as a memorization proxy; pair with detection since fixed budgets degrade under adaptive querying. |
| 9 | Vector-store protection | Encryption, ACLs separate from document ACLs, restricted export APIs, minimum-scope k-NN, embedding-space probing detection. |
| 10 | Gate log-probabilities and confidence | Do not expose logits, confidence, or explanations on production endpoints. |
| 11 | Classify and redact reasoning traces | First-class output. Never log raw traces to unrestricted observability. |
| 12 | Side-channel defenses | Random padding and token batching for streaming; dedicated prefix caches and partitioned KV caches under co-tenancy. |
| 13 | Format-preserving encryption | For structured identifiers, with internal-versus-external routing separation and field allowlists on the external path. |
| 14 | AI-aware audit logging and join policy | SIEM integration, continuous DLP/AI-SPM, and an enforced join policy so permitted sources cannot combine into prohibited conclusions. |

### Tier 3: Advanced (regulated, classified, high-target)

| # | Strategy | Description |
|---|----------|-------------|
| 15 | Confidential computing | Intel TDX, AMD SEV-SNP, AWS Nitro Enclaves where the threat model justifies the utility and latency cost. |
| 16 | Verifiable erasure | Across raw data, embeddings, checkpoints, and adapters — validated by post-unlearning extraction and membership-inference probes. |
| 17 | Disclosure red-teaming as a release gate | Extraction, membership inference, embedding inversion, internal-state inversion, side channels, LoRA extractability. |
| 18 | Audit synthetic data and resist distillation | Probing detection, rate limits, watermarking; budget aggregate analytics. |
| 19 | Disclosure incident-response playbook | Scope by data class and affected subject; meet GDPR, HIPAA, and EU AI Act Article 73 obligations; then unlearn, retrain, or withdraw. |

## Example Attack Scenarios

1. Divergence prompts make a production model emit memorized PII, URLs, and live credentials at scale, triggering GDPR Article 33 notification.
2. A shared-inference-state defect leaks one user's medical-letter prompt into another user's reasoning trace. HIPAA 60-day notification applies.
3. Extended-thinking traces logged verbatim to a shared APM project expose retrieved PII to hundreds of engineers while the answer stays sanitized.
4. Prompt injection makes a support bot print its system prompt and an embedded vendor API key.
5. A shared legal RAG index crosses firm boundaries, synthesizing one client's privileged strategy into another's answer.
6. A leaked "embeddings-only" vector backup is reclassified as a source-document breach after inversion, restarting the 72-hour clock.
7. Whisper Leak topic inference on encrypted streaming identifies users querying medical, legal, or political topics without decryption.
8. Membership inference against a clinical fine-tune identifies training-set patients at high AUC without extracting any record.
9. A model summarizes PII hidden beneath a black-rectangle PDF redaction layer rendered over unmodified text.
10. An injected "diagnostic check" makes a code runtime encode spreadsheet content into DNS queries while the visible answer stays benign.

## AISVS Controls

| AISVS Section | Control | Key Requirements |
|---------------|---------|-----------------|
| C1.1 Training Data Origin & Data Security | Data minimization to features required for the stated purpose; source inventory with use constraints | 1.1.1, 1.1.2 |
| C5.2 AI Resource Authorization & Classification | Default-deny on AI resources, end-user context in retrieval, retrieval over memorization, post-inference filtering, label propagation to embeddings and caches | 5.2.1–5.2.4, 5.2.7 |
| C5.3 Multi-Tenant Isolation | Prevent cross-tenant observation through shared serving and compute | 5.3.1, 5.3.2 |
| C7.3 Output Safety | Block harmful content, system-prompt and backend-data disclosure, and hidden/encoded output | 7.3.1, 7.3.2, 7.3.4 |
| C8.2 Embedding Sanitization & Validation | Mask, tokenize, or drop sensitive fields before embedding | 8.2.1 |
| C8.3 Memory Expiry & Revocation | Exclude expired vectors from retrieval; support memory reset | 8.3.1, 8.3.2 |
| C9.5 Agent Authorization & Delegation | Keep secrets out of the context window, system prompts, and tool arguments | 9.5.4 |
| C11.2 Membership-Inference & Model-Inversion Mitigation | Suppress inferred sensitive attributes, extraction-sized rate limits, output calibration, DP optimization, MIA simulation | 11.2.1–11.2.5 |
| C11.3 Model-Extraction Defense | Keep raw outputs behind the backend; calibrate externally visible responses | 11.3.2 |
| C12.1 Request & Response Logging | Log interactions and policy decisions with enough detail for audit without over-capturing sensitive content | 12.1.1, 12.1.2 |

## Related Frameworks

- AML.T0024.000 — Infer Training Data Membership (MITRE ATLAS)
- AML.T0024.001 — Invert AI Model (MITRE ATLAS)
- DSGAI01 — Data oversharing (OWASP Data Security for GenAI)
- DSGAI13 — Embedding and vector-store protection (OWASP Data Security for GenAI)

## References

- [OWASP GenAI LLM Top 10 2026](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/)
- [Scalable Extraction of Training Data from (Production) Language Models](https://arxiv.org/abs/2311.17035)
- [Whisper Leak: A side-channel attack on Large Language Models](https://arxiv.org/abs/2511.03675)
- [Practical Membership Inference Attacks against Fine-tuned Large Language Models](https://arxiv.org/abs/2311.06062)
- [I Know What You Asked: Prompt Leakage via KV-Cache Sharing in Multi-Tenant LLM Serving](https://www.ndss-symposium.org/ndss-paper/i-know-what-you-asked-prompt-leakage-via-kv-cache-sharing-in-multi-tenant-llm-serving/)
