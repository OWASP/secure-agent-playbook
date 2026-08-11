---
title: "LLM04 Supply Chain"
owasp_llm_id: "LLM04"
owasp_llm_version: "2026"
when_to_use:
  - onboarding a third-party, open-weight, or hub-hosted model
  - reviewing model artifact provenance, signing, and verification
  - auditing LoRA adapters, model merges, conversion, or quantization workflows
  - assessing serving frameworks and inference infrastructure for known CVEs
  - reviewing AI BOM / ML-BOM coverage and license compliance
  - evaluating on-device or edge model packaging and firmware trust
threats:
  - vulnerable or outdated third-party components, serving frameworks, and models
  - slopsquatting of hallucinated package names
  - tampered or backdoored pre-trained models
  - weak provenance and unsigned model artifacts
  - model namespace reuse after account deletion or transfer
  - malicious LoRA adapters and hijacked conversion/merge services
  - quantization-triggered behavior divergence
  - scanner and safe-loader bypass (corrupted pickle, ONNX graph backdoors)
  - compromised build pipelines producing self-signed trojanized artifacts
  - on-device model replacement via app repackaging
summary: "Vulnerabilities affecting the integrity of training data, models, adapters, conversion pipelines, and deployment platforms. Model artifacts, provenance, and conversion/merge workflows are first-class attack surfaces."
aisvs_mappings:
  - section: "C1.1"
    title: "Training Data Origin & Data Security"
    requirements: ["1.1.2", "1.1.3"]
  - section: "C3.1"
    title: "Model Authorization & Integrity"
    requirements: ["3.1.1", "3.1.2", "3.1.3"]
  - section: "C3.2"
    title: "Model Validation & Testing"
    requirements: ["3.2.1", "3.2.2", "3.2.3"]
  - section: "C3.5"
    title: "Pipeline Fine-Tuning"
    requirements: ["3.5.1", "3.5.3", "3.5.4"]
  - section: "C4.1"
    title: "AI Workload Sandboxing & Validation"
    requirements: ["4.1.1", "4.1.2", "4.1.3"]
  - section: "C4.3"
    title: "Edge & Distributed AI Security"
    requirements: ["4.3.2", "4.3.4", "4.3.5"]
  - section: "C6.1"
    title: "Model Artifact Integrity"
    requirements: ["6.1.1", "6.1.2", "6.1.3", "6.1.4"]
  - section: "C6.2"
    title: "AI BOM & Supply Chain Monitoring"
    requirements: ["6.2.1", "6.2.2", "6.2.3"]
  - section: "C10.1"
    title: "Component Integrity"
    requirements: ["10.1.1", "10.1.2", "10.1.3"]
  - section: "C12.5"
    title: "Training Data & Model Lifecycle Audit"
    requirements: ["12.5.3"]
---

# LLM04:2026 Supply Chain

> **Condensed summary — not OWASP's verbatim text.** This file restates [LLM04:2026](https://github.com/GenAI-Security-Project/GenAI-LLM-Top10/blob/main/2026/final/LLM04_SupplyChain.md) in condensed form for agent use. Facts, figures, and scope boundaries are preserved; wording is not. The `AISVS Controls` table and `aisvs_mappings` are derived by this repo at requirement granularity — upstream's [official appendix](https://github.com/GenAI-Security-Project/GenAI-LLM-Top10/blob/main/2026/final/LLMZZ_Appendix_AISVS_Mapping.md) maps at chapter granularity only. Quote the source, not this file.

## Description

LLM supply chains are susceptible to vulnerabilities affecting the integrity of training data, models, adapters, conversion pipelines, and deployment platforms, resulting in biased outputs, security breaches, or system failures. Where traditional software vulnerabilities focus on code flaws and dependencies, ML risks extend to third-party pre-trained models, datasets, and model artifacts, which can be manipulated through tampering, poisoning, or malicious artifact replacement.

The supply chain now includes **model artifacts, provenance, and conversion/merge workflows as first-class attack surfaces**, and on-device LLMs widen it further.

Overlap with [LLM05 Data and Model Poisoning](LLM05.md) is intentional — this entry focuses on the supply-chain aspect. Supply-chain risks specific to agentic applications, including MCP servers and tool registries, are covered by ASI04 Agentic Supply Chain Vulnerabilities.

## Potential Impacts

- Remote code execution during model load or in the serving stack
- Backdoored model behavior that passes benchmark evaluation
- Legal and compliance exposure from unmanaged dataset and model licenses
- Sensitive application data used for supplier model training under unclear T&Cs
- Cross-customer compromise on shared AI-as-a-service platforms

## Common Examples of Risk

1. **Vulnerable or outdated third-party components and models** — packages, serving frameworks, and models themselves. LLM coding assistants add a variant: they hallucinate plausible but nonexistent package names at scale, which attackers register in advance (**slopsquatting**) so unverified AI-suggested dependencies resolve to malicious code.
2. **Licensing risks** — diverse software and dataset licenses impose different usage, distribution, and commercialization requirements.
3. **Vulnerable or tampered pre-trained models** — static analysis alone cannot establish behavioral safety. Migrating away from unsafe serialization such as Python pickle reduces but does not eliminate risk: a backdoor can live in the computational graph and persist in formats widely considered safe such as ONNX, and a crafted model file can exploit memory-corruption bugs in a format's native parser (heap overflows in llama.cpp GGUF parsing, CVE-2024-23496).
4. **Weak provenance and unsigned model artifacts** — Model Cards document a model but do not prove its origin. When artifacts are not signed or hash-pinned, an attacker can replace them in transit, in storage, or at the promotion boundary — especially when pipelines resolve by a mutable reference (a `latest` tag) instead of an immutable digest.
5. **Vulnerable adapters and compromised conversion, merge, and quantization workflows** — a malicious LoRA adapter can compromise the base model's integrity. **Quantization is a distinct transformation risk**: weights can be crafted so the full-precision model evaluates benignly while the quantized artifact exhibits attacker-chosen behavior, so full-precision assurances do not transfer to the deployed artifact.
6. **On-device LLM supply-chain vulnerabilities** — compromised manufacturing, device OS/firmware exploitation, and re-packaged applications with tampered models make device integrity part of the LLM supply chain.
7. **Unclear T&Cs and data privacy policies** — model-operator terms can lead to sensitive application data being used for training, and may create copyright risk from supplier-provided material.

## Prevention and Mitigation

| # | Strategy | Description |
|---|----------|-------------|
| 1 | Vet data sources and suppliers | Including T&Cs and privacy policies. Re-assess on changes in security posture or terms. |
| 2 | Apply A06:2021 controls | Vulnerability scanning, management, and a patching policy across components, APIs, and models. **Verify that AI-suggested dependencies exist and are the intended package** before adopting them. |
| 3 | Red team and evaluate third-party models | Focused on in-scope use cases; continue in production with anomaly detection and adversarial robustness testing. |
| 4 | Maintain a signed inventory | SBOM extended to models, adapters, and datasets via AI BOM / ML-BOM (OWASP CycloneDX ML-BOM, OWASP AIBOM). Track licenses in the same inventory. |
| 5 | Verify provenance and sign artifacts | Cryptographic model signing backed by a transparency log (OpenSSF Model Signing, Sigstore) binds an artifact to a signer identity. **Signing proves integrity and origin, not safety** — combine with immutable references, provenance policy, release gates (SLSA), behavioral evaluation, and continuous upstream validation. |
| 6 | Audit collaborative development environments | Treat model conversion and merge services as high-risk promotion points. |
| 7 | Protect edge deployments | Encrypt models at the edge with integrity checks, use vendor attestation APIs, reject unrecognized firmware and untrusted device states. |

## Example Attack Scenarios

1. **Compromised packages and serving frameworks** — the December 2022 PyTorch `torchtriton` dependency-confusion attack exfiltrated data. The serving stack is part of the same surface: ShadowRay exploited unauthenticated Ray dashboards (CVE-2023-48022) into a self-propagating botnet, and Ollama CVE-2024-37032 allowed RCE via a malicious model manifest.
2. **Tampered model published to a hub** — PoisonGPT surgically modified parameters to spread misinformation while evading benchmark evaluation. The same trust gap covers attacker fine-tunes that strip safety features while preserving benign-task performance.
3. **Compromised supplier LoRA adapter** — a subtly altered adapter merged into a deployed LLM provides a covert entry point.
4. **Hijacked model conversion or merge service** — demonstrated by research hijacking the Safetensors conversion bot on Hugging Face.
5. **Model namespace reuse** — the original author deletes or transfers the account, freeing the namespace; an attacker re-registers the same `Author/ModelName` path, and pipelines resolving by name alone pull the attacker's model.
6. **Scanner, safe-loader, and safe-format bypass** — corrupted or compression-wrapped pickle streams execute before the scanner reaches the broken byte (nullifAI). PickleScan zero-days and `torch.load` `weights_only` (CVE-2025-32434) have CVEs. A ShadowLogic-style backdoor in an ONNX computational graph attaches no executable code to flag.
7. **Compromised build pipeline** — the Ultralytics attack used GitHub Actions cache injection to publish trojanized PyPI releases. Because the artifact is built and signed by the organization's own release infrastructure, it passes downstream provenance checks and scanners that only flag externally sourced components.
8. **Reverse-engineered mobile app** — an on-device model is replaced with a tampered version leading users to scam sites, redistributed via social engineering.

## AISVS Controls

| AISVS Section | Control | Key Requirements |
|---------------|---------|-----------------|
| C1.1 Training Data Origin & Data Security | Source inventory with license and origin; integrity in storage and transfer | 1.1.2, 1.1.3 |
| C3.1 Model Authorization & Integrity | Model registry, artifact signing, signature verification at admission and on load | 3.1.1, 3.1.2, 3.1.3 |
| C3.2 Model Validation & Testing | Pre-deployment testing, **quantization re-evaluation**, provider-change re-evaluation | 3.2.1, 3.2.2, 3.2.3 |
| C3.5 Pipeline Fine-Tuning | Versioned integrity-verified RLHF models, stage-to-stage verification, registered checkpoints | 3.5.1, 3.5.3, 3.5.4 |
| C4.1 AI Workload Sandboxing & Validation | Sandboxed execution, **serialization-format allow-list**, workload attestation | 4.1.1, 4.1.2, 4.1.3 |
| C4.3 Edge & Distributed AI Security | Signed on-device models validated before load; encrypted weights in hardware-backed stores | 4.3.2, 4.3.4, 4.3.5 |
| C6.1 Model Artifact Integrity | Malicious-code scanning, approved sources, integrity verification, behavioral acceptance testing | 6.1.1–6.1.4 |
| C6.2 AI BOM & Supply Chain Monitoring | Machine-readable AI BOM, cryptographic signing, build-breaking completeness checks | 6.2.1, 6.2.2, 6.2.3 |
| C10.1 MCP Component Integrity | Trusted and verified MCP components, allow-listed servers, sandboxed local servers | 10.1.1, 10.1.2, 10.1.3 |
| C12.5 Training Data & Model Lifecycle Audit | Immutable audit records for all model changes | 12.5.3 |

## Related Frameworks

- AML.T0010 — AI Supply Chain Compromise (MITRE ATLAS)
- ASI04 — Agentic Supply Chain Vulnerabilities (OWASP Top 10 for Agentic Applications)
- [A06:2021 Vulnerable and Outdated Components](https://owasp.org/Top10/A06_2021-Vulnerable_and_Outdated_Components/)

## References

- [OWASP GenAI LLM Top 10 2026](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/)
- [OWASP CycloneDX ML-BOM](https://cyclonedx.org/capabilities/mlbom/)
- [OWASP AIBOM](https://genai.owasp.org/owasp-aibom/)
- [OpenSSF Model Signing](https://openssf.org/projects/model-signing/)
- [We Have a Package for You! A Comprehensive Analysis of Package Hallucinations by Code Generating LLMs](https://arxiv.org/abs/2406.10279)
- [Exploiting LLM Quantization](https://arxiv.org/abs/2405.18137)
