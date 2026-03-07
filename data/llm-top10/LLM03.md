---
title: "LLM03 Supply Chain"
owasp_llm_id: "LLM03"
when_to_use:
  - evaluating third-party models or pre-trained weights before integration
  - reviewing LLM application dependencies and fine-tuning pipelines
  - assessing LoRA adapters or model merge workflows
  - auditing on-device or edge-deployed LLM applications
threats:
  - poisoned pre-trained models or LoRA adapters
  - vulnerable third-party packages in ML pipelines
  - compromised model conversion or merge services
  - malicious datasets introduced during fine-tuning
  - on-device model tampering
summary: "LLM supply chains face vulnerabilities affecting training data, models, and deployment platforms — including poisoned pre-trained models, compromised LoRA adapters, vulnerable dependencies, and tampered on-device deployments."
---

# LLM03:2025 Supply Chain

## Description

LLM supply chains face vulnerabilities affecting training data integrity, models, and deployment platforms. Risks include biased outputs, security breaches, and system failures. Unlike traditional software vulnerabilities, ML risks extend to third-party pre-trained models and datasets that can be manipulated through tampering or poisoning. The emergence of open-access LLMs, fine-tuning methods (LoRA, PEFT), and on-device LLMs have expanded the attack surface significantly.

## Common Examples

1. **Vulnerable third-party packages** — Outdated or deprecated components exploitable during model development or fine-tuning
2. **Licensing risks** — Diverse software and dataset licenses create legal compliance challenges
3. **Outdated or deprecated models** — Unmaintained models lead to unresolved security issues
4. **Vulnerable pre-trained models** — Models are binary black boxes; static inspection offers little security assurance
5. **Weak model provenance** — Limited guarantees about model origins; supplier accounts can be compromised
6. **Vulnerable LoRA adapters** — Malicious adapters can compromise base model integrity when merged
7. **Exploited collaborative development** — Shared environments for model merging and conversion can introduce vulnerabilities
8. **On-device LLM vulnerabilities** — Compromised manufacturing, device OS exploits, and app reverse-engineering
9. **Unclear terms and privacy policies** — Ambiguous data handling practices expose sensitive training data

## Prevention and Mitigation

| # | Strategy | Description |
|---|----------|-------------|
| 1 | Vet data sources | Thoroughly vet data sources and suppliers; regularly audit their security posture and terms. |
| 2 | Vulnerability scanning | Apply scanning and patching controls per OWASP A06:2021. |
| 3 | AI red teaming | Conduct comprehensive red teaming when selecting third-party models. |
| 4 | SBOM | Maintain Software Bill of Materials with signed components to detect tampering. |
| 5 | License inventory | Establish licensing inventories using BOMs with automated monitoring. |
| 6 | Verify provenance | Use models from verifiable sources with integrity checks via signing and file hashes. |
| 7 | Monitor collaboration | Monitor collaborative development environments using automated scanning. |
| 8 | Anomaly detection | Deploy adversarial robustness tests to identify tampering and poisoning. |
| 9 | Patching policies | Ensure reliance on maintained API and model versions. |
| 10 | Encrypt edge models | Encrypt edge-deployed models with integrity checks and vendor attestation. |

## Example Attack Scenarios

1. **PoisonGPT** — Attackers bypass Hugging Face safety features by directly modifying model parameters to spread misinformation.
2. **Fine-tuning for hidden triggers** — Models fine-tuned to remove safety features while scoring well on benchmarks.
3. **Compromised LoRA suppliers** — Malicious adapters merged via model merge on Hugging Face compromise integrated systems.
4. **LeftOvers (CVE-2023-4969)** — Exploitation of leaked GPU local memory to recover sensitive data from production servers.
5. **Dataset poisoning** — Attackers poison public datasets creating backdoors favoring specific companies.

## Related Frameworks

- AML.T0010 — ML Supply Chain Compromise (MITRE ATLAS)

## References

- [OWASP Top 10 for LLM Applications](https://genai.owasp.org)
- [PoisonGPT: How we hid a lobotomized LLM on Hugging Face — Mithril Security](https://blog.mithrilsecurity.io/poisongpt-how-we-hid-a-lobotomized-llm-on-hugging-face-to-spread-fake-news/)
- [Hijacking Safetensors Conversion on Hugging Face](https://hiddenlayer.com/research/silent-sabotage/)
