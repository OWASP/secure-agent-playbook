---
title: "LLM05 Data and Model Poisoning"
owasp_llm_id: "LLM05"
owasp_llm_version: "2026"
when_to_use:
  - reviewing training, fine-tuning, or embedding pipelines for poisoning defenses
  - assessing RAG knowledge bases and ingestion pipelines for corpus poisoning
  - auditing continuous learning and automated retraining feedback loops
  - evaluating models sourced from public repositories for backdoors
  - reviewing non-weight artifacts (chat templates, tokenizer configs, adapters)
  - assessing agent persistent memory for long-term manipulation
threats:
  - training and fine-tuning data poisoning eroding refusal behavior
  - low-volume high-impact backdoor poisoning (as few as 250 documents)
  - open-source dataset supply chain poisoning
  - RAG knowledge base poisoning overriding accurate content
  - sleeper agent models with dormant trigger-activated behavior
  - agent memory and recommendation poisoning
  - malicious deserialization via bundled non-weight artifacts
  - chat template and tokenizer config tampering
  - cross-tenant contamination via shared embeddings or memory
summary: "An adversary or unsafe process manipulates data or model artifacts to embed harmful behavior, bias, or exploitable weaknesses. Poisoning targets the learning process, not a runtime bug — remediation can require revalidation, retraining, or pipeline redesign."
aisvs_mappings:
  - section: "C1.1"
    title: "Training Data Origin & Data Security"
    requirements: ["1.1.1", "1.1.2", "1.1.3", "1.1.4", "1.1.5"]
  - section: "C1.2"
    title: "Data Labeling and Annotation Security"
    requirements: ["1.2.1", "1.2.2", "1.2.3"]
  - section: "C1.3"
    title: "Training Data Quality and Security Assurance"
    requirements: ["1.3.1", "1.3.2", "1.3.4", "1.3.5"]
  - section: "C3.1"
    title: "Model Authorization & Integrity"
    requirements: ["3.1.2", "3.1.3"]
  - section: "C3.4"
    title: "Secure Development Practices"
    requirements: ["3.4.1", "3.4.2"]
  - section: "C3.5"
    title: "Pipeline Fine-Tuning"
    requirements: ["3.5.1", "3.5.2", "3.5.3"]
  - section: "C6.1"
    title: "Model Artifact Integrity"
    requirements: ["6.1.1", "6.1.4"]
  - section: "C8.2"
    title: "Embedding Sanitization & Validation"
    requirements: ["8.2.2", "8.2.3", "8.2.4", "8.2.5"]
  - section: "C8.3"
    title: "Memory Expiry & Revocation"
    requirements: ["8.3.2", "8.3.3"]
  - section: "C11.1"
    title: "Model Alignment, Safety, and Robustness Testing and Training"
    requirements: ["11.1.2", "11.1.3", "11.1.5"]
  - section: "C11.4"
    title: "Model Runtime Anomaly Detection"
    requirements: ["11.4.1", "11.4.2", "11.4.3"]
  - section: "C12.5"
    title: "Training Data & Model Lifecycle Audit"
    requirements: ["12.5.1", "12.5.2", "12.5.4"]
---

# LLM05:2026 Data and Model Poisoning

> **Condensed summary — not OWASP's verbatim text.** This file restates [LLM05:2026](https://github.com/GenAI-Security-Project/GenAI-LLM-Top10/blob/main/2026/final/LLM05_DataModelPoisoning.md) in condensed form for agent use. Facts, figures, and scope boundaries are preserved; wording is not. The `AISVS Controls` table and `aisvs_mappings` are derived by this repo at requirement granularity — upstream's [official appendix](https://github.com/GenAI-Security-Project/GenAI-LLM-Top10/blob/main/2026/final/LLMZZ_Appendix_AISVS_Mapping.md) maps at chapter granularity only. Quote the source, not this file.

## Description

Data and Model Poisoning describes attacks and failures where an adversary (or unsafe process) manipulates data or model artifacts to embed harmful behavior, bias, or exploitable weaknesses. In modern GenAI environments poisoning is not limited to "training data" in the traditional sense — it can occur anywhere data is ingested, transformed, retrieved, or reused, including pre-training, fine-tuning, embedding creation, retrieval augmentation, and model distribution. The result is a system that may still appear functional but behaves in ways that undermine trust, safety, and security.

**The key idea: poisoning targets the model's learning process, not a single runtime bug.** Unlike typical software vulnerabilities patched by fixing code, poisoning can require data revalidation, retraining, model replacement, or pipeline redesign — expensive and operationally disruptive.

Poisoning occurs across lifecycle stages:

- **Pre-training** — contaminated corpora cause the model to absorb harmful patterns or skewed representations.
- **Fine-tuning** — manipulated datasets introduce domain-specific failure modes or hidden triggers.
- **Embeddings and vectorization** — poisoning stored vectors steers retrieved content.
- **Transfer learning / model reuse** — compromised source models pass compromise downstream.
- **Continuous learning pipelines** — automated ingestion without validation lets attackers gradually shape behavior.

Models distributed through shared repositories carry risk through **bundled non-weight artifacts** — malicious deserialization (pickle), and tampering of chat templates, tokenizer configs, LoRA/PEFT adapters, and quantization artifacts. Such backdoors may leave behavior untouched until a trigger fires, creating a **sleeper agent**.

Scope: this entry covers durable corruption of persistent data or model behavior. Prompt instructions delivered through retrieved content at inference time are [LLM01](LLM01.md); attacks exploiting embedding geometry are [LLM09](LLM09.md).

## Potential Impacts

- Harmful outputs, impaired capabilities, and degraded reliability that survive standard evaluation
- Fraud bypass and financial loss in security-relevant models
- Costly forced retraining once a backdoor is discovered
- Host compromise and lateral movement via malicious deserialization
- Cross-tenant contamination in shared environments

## Common Examples of Risk

1. **Training and fine-tuning data poisoning** — a targeted variant deliberately erodes refusal behaviors while preserving general accuracy, making degradation undetectable through standard evaluation.
2. **Financial model data poisoning** — mislabeled transaction data teaches a fraud model to ignore real threats.
3. **Open-source dataset supply chain poisoning** — trigger phrases in a shared dataset propagate into every downstream model that fine-tunes on it.
4. **Low-volume high-impact backdoor poisoning** — as few as **250 poisoned documents** compromise models from 600M to 13B parameters *regardless of dataset size*.
5. **AI recommendation / memory poisoning** — hidden instructions in web content manipulate AI memory or recommendations without detection.
6. **RAG knowledge base poisoning** — a single optimized poisoned text per targeted query can override accurate content, retaining high success against paraphrasing, instructional-prevention, and detection-based defenses.
7. **Agent / multi-system poisoning** — poisoned inputs in multi-agent workflows influence behavior and data access across ecosystems.
8. **Healthcare model poisoning** — minimal poisoning of medical training data significantly alters outputs while passing standard evaluations.
9. **Malicious AI models in supply chain** — compromised models distributed via public repositories carry embedded backdoors.

## Prevention and Mitigation

| # | Strategy | Description |
|---|----------|-------------|
| 1 | Track dataset and model lineage | SBOM/ML-BOM (CycloneDX), signing and verification, continuous integrity validation across lifecycle stages. |
| 2 | Strict validation of incoming data | Vet third-party vendors; compare outputs against trusted sources to detect bias or manipulation early. |
| 3 | Protect RAG systems | Enforce trust boundaries, filter retrieved content, apply source scoring, isolate system instructions from external data. |
| 4 | Sandbox and isolate | Limit model interaction with unverified data, tools, or external systems. |
| 5 | Anomaly detection across pipelines | Statistical and AI-based detection across training, embedding, and inference; monitor training loss, outputs, and behavior for drift against defined thresholds. |
| 6 | Curated domain-specific datasets | Reduce exposure to untrusted data and cross-domain contamination when fine-tuning. |
| 7 | Least privilege and segmentation | Prevent unauthorized data injection through access controls and network segmentation. |
| 8 | Data version control | DVC or equivalent to track changes, maintain history, and enable rollback and forensics. |
| 9 | Control retraining and feedback loops | Validate incoming data, require human oversight, and rate-limit against gradual poisoning through manipulated preference signals. |
| 10 | Continuously red team for backdoors | **Do not assume safety alignment removes backdoors.** Dedicated trigger-probing is required after every alignment cycle. |
| 11 | Grounding with validation layers | Ensure retrieved content is verified before influencing outputs. |
| 12 | Treat inference artifacts as code | Chat templates, tokenizer configs, LoRA/PEFT adapters, and quantization artifacts require signing, hash verification, diff checks, and static analysis before deployment. |

## Example Attack Scenarios

1. Manipulated documents inserted into an internal knowledge repository surface in responses, driving incorrect recommendations and manipulated business decisions.
2. Hidden instructions in webpages summarized by AI tools bias the model to recommend specific products once ingested into RAG or memory.
3. Crafted inputs submitted into an automated retraining feedback loop — **no infrastructure access required, only standard UI access** — cause slow drift toward degraded accuracy and unsafe recommendations.
4. A malicious insider injects mislabeled transaction data; the model fails to detect fraud, producing losses and regulatory breach.
5. Poisoned pre-trained weights uploaded to a public repository survive standard safety training, compromising every organization that adopts them.
6. A modified chat template (GGUF package or tokenizer config) with trigger-activated conditional instructions behaves normally under benign input. Validated across 18 models and 4 inference runtimes: factual accuracy drops from 90% to 15% under trigger conditions, with URL emission exceeding 80% success.
7. A third-party model loaded via unsafe serialization executes embedded code at load, enabling host compromise and lateral movement.
8. In a shared AI environment, one tenant injects adversarial data into shared embeddings or memory layers, influencing other tenants' responses.
9. Malicious instructions injected into an agent's persistent memory over multiple sessions make it prioritize attacker-controlled logic with hidden persistence.

## AISVS Controls

| AISVS Section | Control | Key Requirements |
|---------------|---------|-----------------|
| C1.1 Training Data Origin & Data Security | Data minimization, source inventory, integrity in storage and transfer, integrity monitoring, watermarking | 1.1.1–1.1.5 |
| C1.2 Data Labeling and Annotation Security | Labeling access control, cryptographic artifact integrity, sensitive label redaction | 1.2.1, 1.2.2, 1.2.3 |
| C1.3 Training Data Quality and Security Assurance | **Poisoning detection**, label confidence thresholds, disallowed-content removal, **clean-label poisoning defenses** | 1.3.1, 1.3.2, 1.3.4, 1.3.5 |
| C3.1 Model Authorization & Integrity | Artifact signing and verification at admission and on load | 3.1.2, 3.1.3 |
| C3.4 Secure Development Practices | Unshared AI runtime components across environments; training isolated from production | 3.4.1, 3.4.2 |
| C3.5 Pipeline Fine-Tuning | Integrity-verified RLHF models, reward-hacking detection, stage-to-stage verification | 3.5.1, 3.5.2, 3.5.3 |
| C6.1 Model Artifact Integrity | Malicious-code scanning before import; behavioral acceptance testing before promotion | 6.1.1, 6.1.4 |
| C8.2 Embedding Sanitization & Validation | Outlier vector quarantine, validated memory writes, retrieval-manipulation detection, contradiction checks | 8.2.2–8.2.5 |
| C8.3 Memory Expiry & Revocation | Memory reset; quarantined content retained but excluded from retrieval | 8.3.2, 8.3.3 |
| C11.1 Alignment, Safety & Robustness Testing | Per-release alignment test suite, adversarial evaluation, harmful-content regression detection | 11.1.2, 11.1.3, 11.1.5 |
| C11.4 Model Runtime Anomaly Detection | Pre-inference anomaly detection, gating on flagged inputs, **poisoning detection and human review in the feedback pipeline** | 11.4.1, 11.4.2, 11.4.3 |
| C12.5 Training Data & Model Lifecycle Audit | Dataset lineage with transformations, labeling activity logs, write-time document tagging | 12.5.1, 12.5.2, 12.5.4 |

## Related Frameworks

- AML.T0020 — Poison Training Data (MITRE ATLAS)
- AML.T0018 — Backdoor AI Model (MITRE ATLAS)
- AML.T0070 — RAG Poisoning (MITRE ATLAS)
- ASI06 — Memory and Context Poisoning (OWASP Top 10 for Agentic Applications)

## References

- [OWASP GenAI LLM Top 10 2026](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/)
- [Sleeper Agents: Training Deceptive LLMs that Persist Through Safety Training](https://arxiv.org/abs/2401.05566)
- [Poisoning attacks on LLMs require a near-constant number of poison samples](https://arxiv.org/abs/2510.07192)
- [CISA Advisory: Securing Data for AI Systems](https://www.cisa.gov/news-events/cybersecurity-advisories/aa25-142a)
